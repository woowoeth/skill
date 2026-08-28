#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill 商店 — the daily scout (进货员).

Daily run (GitHub Actions):
  1. Restock: refresh stars / pushed_at for every repo already on the shelves.
  2. Discover: GitHub search (topics + fun keywords) for skill repos pushed
     in the last ~14 days that we don't stock yet.
  3. Ingest: shallow-clone each new repo, find SKILL.md files, parse
     frontmatter, and put items on the right shelf. Big packs become one
     "collection" card instead of flooding the store.
  4. Rebuild skills/feed.json.

Seed run (local): python scouts/skill_scout.py --seed /path/to/clones

Fault-tolerant: any single repo/skill failure is skipped, never aborts.
No third-party deps — stdlib + git only.
"""
from __future__ import annotations
import os, re, sys, json, time, shutil, argparse, tempfile, subprocess as sp, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scout_lib as lib  # noqa: E402

MAX_NEW_REPOS_PER_RUN = int(os.environ.get("MAX_NEW_REPOS", "5"))
MAX_SINGLES_SMALL = 3
MAX_ITEMS_PER_REPO = 3          # individual cards sampled from one multi-skill repo
COLLECTION_MIN = 6              # >= this many skills → also gets a collection card
COLLECTION_ONLY = 26            # >= this many skills → collection card ONLY
# ---- admission: 相信新鲜度 + 认真程度 + 人的判断，而非人气存量 ----
MIN_STARS_ESTABLISHED = 40      # 老仓库（>30 天）的人气底线
MIN_STARS_NEWCOMER = 3          # 新品快车道：近 7 天发布，几乎不看星
NEWCOMER_WINDOW_DAYS = 7        # “新”的定义
FAST_RISER_STARS = 25           # 星速度：14 天内涨到这个数即视为正在被认可
FAST_RISER_WINDOW_DAYS = 14
MIN_STARS_DISCOVER = MIN_STARS_ESTABLISHED   # 向后兼容旧引用


def _days_since(iso: str) -> float:
    """天数距今；解析失败返回一个大数（当作很旧）。"""
    if not iso:
        return 1e9
    try:
        from datetime import datetime, timezone
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).total_seconds() / 86400.0
    except Exception:
        return 1e9


def _admit(item: dict) -> tuple[bool, str]:
    """多信号准入。召回优先——进来的杂质靠人工巡货删，漏掉的好货无法追回。
    返回 (是否放行, 命中通道)。fork 一律拒。"""
    if item.get("fork"):
        return False, "fork"
    stars = item.get("stargazers_count", 0)
    created_age = _days_since(item.get("created_at", ""))
    pushed_age = _days_since(item.get("pushed_at", ""))

    # 通道一：新品快车道 —— 刚出生几天，还没来得及积累星，给它被看见的机会
    if created_age <= NEWCOMER_WINDOW_DAYS and stars >= MIN_STARS_NEWCOMER:
        return True, "newcomer"
    # 通道二：星速度 —— 短期内爬升快，比存量更能抓住“正在被认可”的新星
    if created_age <= FAST_RISER_WINDOW_DAYS and stars >= FAST_RISER_STARS:
        return True, "fast-riser"
    # 通道三：认真程度信号 —— 星未达标，但仓库“看起来是认真做的”，放进来让人工再判
    #   （有主页/演示、描述够长、近期仍在维护）——任一强信号 + 一点点星
    serious = 0
    if item.get("homepage"):
        serious += 1
    if len(item.get("description") or "") >= 60:
        serious += 1
    if pushed_age <= 30:
        serious += 1
    if stars >= 10 and serious >= 2:
        return True, "serious-signal"
    # 通道四（老仓库常规线）：站住了一段时间，用较高星兜底
    if stars >= MIN_STARS_ESTABLISHED:
        return True, "established"
    return False, "below-floor"
CLONE_TIMEOUT = 90

# 品味的进货通道。topic: / 安装量榜 / 官方目录 一律不当主源。
# 对标原声：固定短名单，T1 作者新作必审；合集只抽招牌件。

T1_AUTHORS = [
    # 中文创作者，国外目录站没有的增量
    "op7418",            # 歸藏
    "alchaincyf",        # 花叔
    "JimLiu",            # 宝玉
    "worldwonderer",     # 网文 / 小说变游戏
    "5tldr",
    "laolaoshiren",
    "yangcodingmaster",  # photo-distill
    "chongchonghaoman",
    "yeyulangzi",
    "neallydare",
    "wei011",
    "wr5912",
    "c1375",
    "panmax",
    "chenklein26",
    "kagurananaga",
    "jiang59991",        # 侨批
    "RollingAlei",
    "dzcmemory-web",
    "voidforall",
    "yuanzhao321",
    "seiya89757",
    "fxw-labs",
    "r0ses1r-dev",
    "KKKKhazix",         # 卡兹克：活人感长文，不是效率合集
    "BigPengSays",       # 创作者选题公式，对照用也盯新作
    "tjxj",              # 手写幻灯片 / 四格漫画
    "liamgvchi",         # 极简杂志海报
    "gnipbao",           # 本地线稿白板视频
    "oil-oil",           # 一套切开的同款图标
    "geekjourneyx",      # 禁 AI 插图的路书、公众号版式
    "hiyeshu",           # 会删心愿单的行程
    "ToBeWin",           # 手绘白板讲解
    "shpigford",         # NURBS 滑块打印件
    "dongbeixiaohuo",    # 去 AI 味中文写作
    "rubyzhu26",         # 草间 / 米罗五感壁纸
    "mocomeng-666",      # Bluey 育儿
    "bohandu",           # 冰箱剩货不放宽过敏原
    "zgdfsgd",           # 龙猫不许洗澡
    "xlt-6",             # 纸面桌游原型
    "jasonbhorne",       # 只给和弦不抄词
    "elhamid",           # 父母口述史
    "lincwang123",       # 家长配音绘本
    "ruochenlyu",        # 北京花粉
    "xxxonechen",        # 53 城花粉
    "sumanasj",          # 克苏鲁 KP
    "zzzzzzza",          # 剧本杀角色蒸馏
    "qian-gugugaga",
    "yunpeng192",        # 定金 / 订金
    "aryaminus",         # 三盘星历
    "jadel-kemo",        # 跑团 SAN 表
    "dpwelsh",           # basilisk 数谢谢
    # 单一风格 / 有立场的英文作者
    "Nutlope",           # hallmark
    "JuliusBrussee",     # caveman
    "blader",            # humanizer
    "aldegad",           # sprite-gen
    "danilo-znamerovszkij",
    "Alisa0808",         # vox-director
    "obra",              # superpowers 里能单独成件的
    "mattpocock",        # grill-me 那一档，不整库上架
    "Zeejay0",
    "Vieeeeeee",
    "yokel1121",
    "crawfordxx",
    "ayi-ai",
    "eternityspring",
    "jinchenma94",
    "liyue-aigc",
    "wnby",
    "carolinaaafy",
    "Evianis",
    "garrytan",
    "addyosmani",
    "KKenny0",
    "tluy",
    "Hiseaa",
    "TwentyfiveBTea",
    "N1kO724",
    "luji12",
    "liuzihe849-png",
    "luckdvr",
    "iamkong",
    "haorantang97",
    "liigoQi",
    "lzs0594",
    "traveler0621",
    "zhu930824",
]


T1_REPOS = [
    "JimLiu/baoyu-skills",
    "op7418/guizang-social-card-skill",
    "op7418/guizang-material-illustration",
    "op7418/guizang-ppt-skill",
    "op7418/guizang-sports-skill",
    "op7418/Humanizer-zh",
    "op7418/logo-generator-skill",
    "alchaincyf/huashu-design",
    "alchaincyf/huashu-skills",
    "KKKKhazix/khazix-skills",
    "Nutlope/hallmark",
    "tjxj/z-skills",
    "BigPengSays/bigpeng-hot-gzh",
    "5tldr/claude-skills",
    "laolaoshiren/claude-code-skills-zh",
    "obra/superpowers",
    "mattpocock/skills",
    "KKenny0/card-skill",
    "tluy/skill-zine-summary",
    "Hiseaa/eastern-ink-photo-diptych",
    "TwentyfiveBTea/ink-wash-poster",
    "N1kO724/kodak-2383-film-look",
    "luji12/handdrawn-photo-poster",
    "liuzihe849-png/ai-editorial-print-studio",
    "luckdvr/photo-riso-poster",
    "iamkong/photo-to-minimal-illustration",
    "haorantang97/antibes-holiday",
    "wnby/paper-spirit-zine",
    "LiamGvchi/gc-minimal-zine-poster",
    "Zeejay0/gathered-scenes-zine-skill",
    "yangcodingmaster/photo-distill",
]

SEARCH_QUERIES = (
    [f"repo:{r}" for r in T1_REPOS]
    + [f"user:{u} skill in:name,description" for u in T1_AUTHORS]
    + [
        "codex skill in:name,description poster OR collage OR halftone OR risograph",
        "codex OR claude skill in:name,description watercolor OR paper-cut OR hand-drawn",
        "claude OR codex skill in:name,description 插画 OR 海报 OR 手绘 OR 水彩 OR 剪纸",
        "claude OR agent skill in:name,description zine OR sticker OR risograph OR hallmark",
        "claude OR agent skill in:name,description 公文 OR 红头文件 OR GB/T 9704",
        "claude OR agent skill in:name,description 中医 OR 倪海厦 OR 方剂 OR 伤寒",
        "claude OR agent skill in:name,description 育儿 OR 养猫 OR 花粉 OR 崔玉涛",
        "claude OR agent skill in:name,description 八字 OR 周易 OR 占卜 OR 紫微 OR 侨批",
        "claude OR agent skill in:name,description 去AI味 OR 人味 OR 海明威 OR 原始人",
        "claude OR codex skill in:name,description risograph OR riso OR zine OR diptych",
        "claude OR codex skill in:name,description 水墨 OR 胶片 OR 莫兰迪 OR 剪影",
    ]
)

# 有样图、单风格的图册合集。比 skills.sh 热门榜更接近本店门闸。
TASTE_LISTS = (
    "https://raw.githubusercontent.com/tluy/skill-zine-summary/main/README.md",
)

SKIP_REPO_PAT = re.compile(
    r"awesome-|awesome$|^.*/(dotfiles|test|demo|example|template)s?$|guide|tutorial|handbook|cookbook|cheatsheet|-docs?$", re.I)

# T2 热门榜：只当候选池，过 _admit + 命名黑名单 + 官方厂牌黑名单。
# 整榜不上架。每天最多试 3 个榜上新仓。
MAX_CHART_REPOS_PER_RUN = 3
CHART_SKIP_ORGS = {
    "anthropics", "vercel", "vercel-labs", "microsoft", "google",
    "googleworkspace", "google-labs-code", "github", "huggingface",
    "shadcn-ui", "fastapi", "cursor",
}
CHART_CSV = [
    "https://raw.githubusercontent.com/LinklyAI/best-skills/main/data/latest/rankings/rising-stars.csv",
    "https://raw.githubusercontent.com/LinklyAI/best-skills/main/data/latest/rankings/trending-7d.csv",
    "https://raw.githubusercontent.com/LinklyAI/best-skills/main/data/latest/rankings/social-buzz.csv",
    "https://raw.githubusercontent.com/LinklyAI/best-skills/main/data/latest/rankings/top-repos.csv",
]
CHART_SEARCH = [
    "topic:claude-skills created:>{since} sort:stars",
    "topic:agent-skills created:>{since} sort:stars",
    "SKILL.md in:readme created:>{since} stars:>20 sort:stars",
    "topic:claude-skills pushed:>{since} stars:>80 sort:updated",
]


# ------------------------------------------------------------------ git ----
def shallow_clone(repo: str, dest: str) -> bool:
    try:
        sp.run(["git", "clone", "-q", "--depth", "1",
                f"https://github.com/{repo}.git", dest],
               check=True, timeout=CLONE_TIMEOUT,
               stdout=sp.DEVNULL, stderr=sp.DEVNULL)
        return True
    except Exception as e:
        print(f"[scout] clone failed {repo}: {e}")
        return False


# 测试夹具目录。仓库自己的单测里常放一堆 SKILL.md（故意写坏的 frontmatter、
# golden 快照），它们不是商品，但过去被一并数进 skill_count —— 于是合集卡上
# 印出来的"几十件"里有一大半是别人的测试数据。实测：yusufkaraaslan/Skill_Seekers
# 26 件里 24 件是 tests/golden/phase2 的夹具，真货只有 2 件（连合集线都够不上）。
FIXTURE_DIRS = {"tests", "test", "__tests__", "fixtures", "__fixtures__",
                "spec", "golden", "testdata"}


def find_skill_mds(root: str) -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in
                       (".git", "node_modules", "vendor", "dist", "build")
                       and d not in FIXTURE_DIRS]
        if "SKILL.md" in filenames:
            out.append(os.path.join(dirpath, "SKILL.md"))
    return sorted(out)


# --------------------------------------------------------------- ingest ----
def ingest_repo(local: str, repo: str, meta: dict, source: str) -> list[dict]:
    """Turn one cloned repo into shelf items. Returns new items (not yet saved)."""
    mds = find_skill_mds(local)
    if not mds:
        return []
    stars = int(meta.get("stars", 0))
    repo_desc = (meta.get("description") or "").strip()
    pushed = meta.get("pushed_at", "")
    homepage = meta.get("homepage") or ""
    items: list[dict] = []

    root_md = os.path.join(local, "SKILL.md")
    if root_md in mds:
        # single-product repo (extras inside are internals of the same product)
        text = open(root_md, encoding="utf-8", errors="replace").read()
        fm = lib.parse_skill_md(text)
        name = fm["name"] or lib.first_heading(text) or repo.split("/")[-1]
        items.append(lib.make_item(kind="skill", name=name,
                                   desc_en=fm["description"] or repo_desc,
                                   repo=repo, path="", stars=stars,
                                   repo_desc=repo_desc, pushed_at=pushed,
                                   homepage=homepage, skill_count=len(mds),
                                   source=source))
        return items

    parsed = []
    for md in mds:
        try:
            text = open(md, encoding="utf-8", errors="replace").read()
            fm = lib.parse_skill_md(text)
            rel = os.path.relpath(os.path.dirname(md), local).replace(os.sep, "/")
            name = fm["name"] or lib.first_heading(text) or rel.split("/")[-1]
            if name.lower() in ("template", "example", "sample"):
                continue
            if re.search(r"-v\d+$", name):        # drop versioned duplicates
                continue
            parsed.append((name, fm["description"], rel))
        except Exception as e:
            print(f"[scout] bad SKILL.md {md}: {e}")
    if not parsed:
        return []
    n = len(parsed)

    # Official shelf: stock every Anthropic skill individually, no collection card.
    if repo == "anthropics/skills":
        for name, desc, rel in parsed:
            items.append(lib.make_item(kind="skill", name=name, desc_en=desc,
                                       repo=repo, path=rel, stars=stars,
                                       repo_desc=repo_desc, pushed_at=pushed,
                                       homepage=homepage, skill_count=1, source=source))
        return items

    # Flagship rule: a sub-skill named like the repo means "one product with
    # add-ons" (caveman, ponytail, i-have-adhd...) → one product card only.
    tail = lib.slug(repo.split("/")[-1])
    flag = next((p for p in parsed if lib.slug(p[0]) == tail), None)
    if flag:
        items.append(lib.make_item(kind="skill", name=flag[0],
                                   desc_en=flag[1] or repo_desc, repo=repo,
                                   path=flag[2], stars=stars, repo_desc=repo_desc,
                                   pushed_at=pushed, homepage=homepage,
                                   skill_count=n, source=source))
        return items

    if n >= COLLECTION_MIN:
        col = lib.make_item(kind="collection", name=repo.split("/")[-1],
                            desc_en=repo_desc or f"A pack of {n} skills.",
                            repo=repo, path="", stars=stars,
                            repo_desc=repo_desc, pushed_at=pushed,
                            homepage=homepage, skill_count=n, source=source)
        col["install"] = collection_install(repo, [p[2] for p in parsed])
        items.append(col)
    if n < COLLECTION_ONLY:
        scored = sorted(parsed,
                        key=lambda p: -lib.fun_score(p[0], p[1] or "", stars))
        take = scored[:MAX_SINGLES_SMALL] if n < COLLECTION_MIN else scored[:MAX_ITEMS_PER_REPO]
        for name, desc, rel in take:
            items.append(lib.make_item(kind="skill", name=name,
                                       desc_en=desc or repo_desc, repo=repo,
                                       path=rel, stars=stars, repo_desc=repo_desc,
                                       pushed_at=pushed, homepage=homepage,
                                       skill_count=1, source=source))
    return items


COLLECTION_NOTE = ("clone 下来，挑你要的那件复制进 ~/.claude/skills/。"
                   "这是一个合集，没有「装它」这个动作。")


def skills_root(rels: list[str]) -> str:
    """合集里那些 skill 的共同上级目录 —— 覆盖不到八成就返回空（指仓库根）。

    合集卡指向仓库首页几乎没用；指向 `skills/` 这类真正装着技能的目录，
    点进去就是一份清单。但**很多仓库根本没有这么一个目录**：实测 16 件合集里
    5 件的 skill 散在 3–11 个不同的根下（open-design 11 个、codeArbiter 9 个），
    硬凑一个出来就是编。凑不出来就老实指仓库根。
    """
    from collections import Counter
    parents = [os.path.dirname(r) for r in rels]
    cnt: Counter = Counter()
    for pa in parents:
        parts = pa.split("/") if pa else []
        for i in range(len(parts) + 1):
            cnt["/".join(parts[:i])] += 1
    for cand in sorted((c for c in cnt if c), key=lambda c: -len(c.split("/"))):
        if cnt[cand] / len(rels) >= 0.8:
            return cand
    return ""


def collection_install(repo: str, rels: list[str]) -> dict:
    """合集不给 copy 命令 —— 给了就是骗人。

    `~/.claude/skills/<X>/SKILL.md` 才是被发现的路径。合集 clone 下来那一层
    没有 SKILL.md，`mv <repo> ~/.claude/skills/<repo>` 装了等于没装；
    而「把 skills/ 底下全倒进去」更糟 —— 有的合集是 519 件。
    所以只给 clone + 一个能点进去挑的指针，外加一句话说清这张卡为什么不一样。
    """
    root = skills_root(rels)
    return {
        "clone": f"git clone --depth 1 https://github.com/{repo}.git",
        "copy": "",
        "dir": "",
        "browse": f"https://github.com/{repo}" + (f"/tree/HEAD/{root}" if root else ""),
        "note": COLLECTION_NOTE,
    }


NEW_IDS: list[str] = []


def stock(items: list[dict], existing: dict, sources: dict, repo: str, meta: dict) -> int:
    added = 0
    cover = resolve_cover(repo) if items else ""
    for it in items:
        if it["id"] in existing:
            continue
        if cover:
            it["cover"] = host_cover(it["id"], cover) or cover
        if not save_method(it):
            # 取不回正文 = path 多半记错了（或仓库没了）。过去这里是静默的，
            # 于是错的 install.copy 一路上架，用户照抄装不上都没人知道。
            print(f"[scout] ! 取不回正文 {it['id']}  path={it.get('path','')!r} "
                  f"—— install.copy 可能是错的，跑 --verify-paths 复核")
        lib.save_item(it)
        existing[it["id"]] = it
        NEW_IDS.append(it["id"])
        added += 1
        print(f"[scout] + {it['kind']:<10} {it['id']}  ({it['category']}, fun {it['fun_score']})")
    sources["repos"][repo] = {"stars": meta.get("stars", 0),
                              "pushed_at": meta.get("pushed_at", ""),
                              "description": (meta.get("description") or "")[:200],
                              "last_seen": lib.today()}
    return added




# ---------------------------------------------------------------- covers ----
BADGE_PAT = re.compile(
    r"shields\.io|badgen?\b|badge|codecov|travis|circleci|appveyor|visitor|hits\.|"
    r"counter|actions/workflows|deepwiki|colab|\.svg(\?|$)|star-history", re.I)


def _img_ok(url: str) -> bool:
    import urllib.request
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "skill-store-scout"})
        with urllib.request.urlopen(req, timeout=20) as r:
            ct = r.headers.get("Content-Type", "")
            cl = int(r.headers.get("Content-Length") or 0)
            return r.status == 200 and ct.startswith("image/") and cl < 4_500_000
    except Exception:
        return False


def resolve_cover(repo: str) -> str:
    """Best real image for a repo: author's social-preview > first non-badge
    README image (usually an actual screenshot/demo). '' -> UI falls back to
    GitHub's opengraph stats card."""
    import urllib.request
    # 1) custom social preview set by the author
    try:
        req = urllib.request.Request("https://github.com/" + repo,
                                     headers={"User-Agent": "Mozilla/5.0 (skill-store)"})
        html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
        m = (re.search(r'property="og:image"\s+content="([^"]+)"', html)
             or re.search(r'content="([^"]+)"\s+property="og:image"', html))
        if m:
            u = m.group(1).replace("&amp;", "&")
            if "private-user-images" in u:
                pass
            else:
                return u
    except Exception:
        pass
    # 2) first meaningful image in rendered README
    try:
        hdr = {"Accept": "application/vnd.github.html", "User-Agent": "skill-store-scout"}
        tok = os.environ.get("GH_TOKEN", "")
        if tok:
            hdr["Authorization"] = "Bearer " + tok
        req = urllib.request.Request(f"https://api.github.com/repos/{repo}/readme", headers=hdr)
        h = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "ignore")
        cands = []
        for n, m in enumerate(re.finditer(r'<img[^>]+src="([^"]+)"', h)):
            if n >= 8:
                break
            src = m.group(1)
            if not src.startswith("http") or BADGE_PAT.search(src):
                continue
            cands.append(src)   # 不用脚本 UA 验证：GitHub 对非浏览器 UA 返 403，会误杀浏览器能正常加载的图
        if cands:
            # **不能直接取第一张。** 创意类 skill 的 examples/ 里常是「原片 → 成品」
            # 成对存放（04b-two-kids-original.jpg / 04b-two-kids-poster.jpg），
            # 按文件名顺序取第一张拿到的是**用户自己拍的原照片**，不是产出物 ——
            # photo-distill 就是这么把一张原片送上今日头条的。封面的全部意义是
            # 「产出物即证据」，放原片等于什么都没证明。
            try:
                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                from enrich import prefer_output_images
                cands = prefer_output_images(cands)
            except Exception:
                pass
            return cands[0]
    except Exception:
        pass
    # last resort: GitHub generated social card
    return "https://opengraph.githubassets.com/1/" + repo


def host_cover(sid: str, url: str) -> str:
    """Save a cover into assets/covers so the shelf does not depend on hotlinks."""
    if not url or not sid:
        return url
    if "woowoeth/skill" in url and "/assets/covers/" in url:
        return url
    dest_dir = os.path.join(lib.ROOT, "assets", "covers")
    os.makedirs(dest_dir, exist_ok=True)
    ext = "png"
    low = url.lower()
    if ".jpg" in low or "jpeg" in low:
        ext = "jpg"
    elif ".webp" in low:
        ext = "webp"
    path = os.path.join(dest_dir, f"{sid}.{ext}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 pinwei-cover"})
        data = urllib.request.urlopen(req, timeout=25).read()
        if len(data) < 800:
            return url
        open(path, "wb").write(data)
        return f"https://raw.githubusercontent.com/woowoeth/skill/HEAD/assets/covers/{sid}.{ext}"
    except Exception as e:
        print("[cover] host skip", sid, e)
        return url


# ---------------------------------------------------------------- enrich ----
LLM_KEY = os.environ.get("LLM_API_KEY", "").strip()
LLM_BASE = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1").strip().rstrip("/")
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o-mini").strip()

ENRICH_PROMPT = """你是「Skill 商店」店长，为一件候选 Agent Skill 写货架文案。这家店只留精品，文案要让人"一眼想装"。

三个字段各司其职，**不许互相重复**：

- title_zh：**一句话说清这是什么**（12~24 个汉字）。不是外号、不是产品名。
  ✗ 错：「女娲造 skill」「技能饕餮」——用户不知道那是啥
  ✓ 对：「把任何人的思维方式蒸馏成一个能装的 skill」
- tagline_zh：**用户为什么要装**（40~58 字，占满两行）。写痛点/场景/反差 + 一个别处没有的具体细节。
  禁止复述功能列表，禁止「实用利器」「效率神器」这类空话。
- why_zh：**它到底好在哪**（30~52 字）。机制上的差异点。可以有态度。
- limit_zh：**不装的理由**（一句诚实局限，必写）。
- tagline_en / why_en：英文版，同义但地道，各 ≤115 / ≤130 字符。

基建、官方四件套、合集目录、写不出钩子的，title_zh 设为 "SKIP"。

商品信息：
name: {name}
repo: {repo}
kind: {kind}
description: {desc}

只输出一个 JSON 对象，含 title_zh, tagline_zh, tagline_en, why_zh, why_en 五个键。"""


def _clamp_cjk(text: str, limit: int) -> str:
    """中文超限时截到 limit，尽量切在标点处，末尾补句号。"""
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[:limit - 1]
    for i in range(len(cut) - 1, max(0, len(cut) - 12), -1):
        if cut[i] in "，。；、！？":
            return cut[:i + 1] if cut[i] in "。！？" else cut[:i] + "。"
    return cut.rstrip("，、；") + "。"


def _clamp_en(text: str, limit: int) -> str:
    """英文超限时截到 limit，切在词边界，末尾补句号。"""
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[:limit - 1].rsplit(" ", 1)[0].rstrip(",;:—- ")
    if not cut.endswith((".", "!", "?")):
        cut += "."
    return cut


def _clamp_patch(patch: dict) -> dict:
    """把模型产出的文案硬性压进规范长度——模型不听字数指令，代码兜底。"""
    if patch.get("title_zh"):
        patch["title_zh"] = patch["title_zh"][:26]
    if patch.get("tagline_zh"):
        patch["tagline_zh"] = _clamp_cjk(patch["tagline_zh"], 58)
    if patch.get("why_zh"):
        patch["why_zh"] = _clamp_cjk(patch["why_zh"], 52)
    if patch.get("tagline_en"):
        patch["tagline_en"] = _clamp_en(patch["tagline_en"], 115)
    if patch.get("why_en"):
        patch["why_en"] = _clamp_en(patch["why_en"], 130)
    return patch


def enrich_items(ids: list[str], existing: dict) -> None:
    """LLM copywriting for newly stocked items. No-op unless LLM_API_KEY is set.
    Writes into the machine layer (item files); editorial still overrides everything."""
    if not LLM_KEY or not ids:
        if ids:
            print(f"[scout] enrich: skipped ({len(ids)} new items, LLM_API_KEY not set)")
        return
    import urllib.request
    done = 0
    for sid in ids:
        it = existing.get(sid)
        if not it:
            continue
        prompt = ENRICH_PROMPT.format(name=it.get("name", ""), repo=it.get("repo", ""),
                                      kind=it.get("kind", ""), desc=(it.get("desc_en") or "")[:600])
        anthropic = LLM_KEY.startswith("sk-ant-") or "anthropic" in LLM_BASE
        if anthropic:
            model = (os.environ.get("LLM_MODEL") or "claude-haiku-4-5").strip()
            base = LLM_BASE if "anthropic" in LLM_BASE else "https://api.anthropic.com"
            body = json.dumps({"model": model, "max_tokens": 800,
                               "messages": [{"role": "user", "content": prompt}]}).encode()
            req = urllib.request.Request(base + "/v1/messages", data=body, method="POST",
                                         headers={"x-api-key": LLM_KEY,
                                                  "anthropic-version": "2023-06-01",
                                                  "Content-Type": "application/json"})
        else:
            body = json.dumps({"model": LLM_MODEL, "temperature": 0.4,
                               "messages": [{"role": "user", "content": prompt}]}).encode()
            req = urllib.request.Request(LLM_BASE + "/chat/completions", data=body, method="POST",
                                         headers={"Authorization": "Bearer " + LLM_KEY,
                                                  "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                resp = json.loads(r.read())
                txt = (resp["content"][0]["text"] if anthropic
                       else resp["choices"][0]["message"]["content"])
            txt = txt.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            c = json.loads(txt)
            patch = {k: str(c[k]).strip() for k in
                     ("title_zh", "tagline_zh", "tagline_en", "why_zh", "why_en", "limit_zh")
                     if c.get(k) and str(c[k]).strip()}
            patch = _clamp_patch(patch)
            if patch.get("title_zh", "").strip().upper() == "SKIP":
                it["hide"] = True
                lib.save_item(it)
                print(f"[scout] {sid}: 文案写不出 → 按标准不上架")
                continue
            if patch:
                it.update(patch)
                lib.save_item(it)
                done += 1
        except Exception as e:  # never let copywriting break the restock
            print(f"[scout] enrich {sid}: {e}")
    print(f"[scout] enrich: {done}/{len(ids)} items copywritten by {LLM_MODEL}")


TASTE_RE = re.compile(
    r"插画|海报|手绘|水彩|剪纸|小红书|公文|八字|命理|去AI|人味|短剧|剧本|分镜|"
    r"漫画|手写|zine|poster|illustration|humanizer|hallmark|caveman|risograph|"
    r"watercolor|comic|封面|种草|育儿|中医|风水|占卜|网文|贴纸|涂鸦|仙侠|"
    r"杜蕾斯|莫兰迪|编辑稿|文物|动效|诗意", re.I)
JUNK_RE = re.compile(
    r"harness|runtime|orchestr|marketplace|templates?|crm|seo audit|"
    r"agentic framework|coding agent fleet|official skill|"
    r"全自动发布|简历包装|办公套件", re.I)


def _taste_pass(it: dict) -> str:
    """同一轮能不能上架。返回空串=拒，否则是通道名。"""
    if it.get("kind") == "collection":
        return ""
    repo = (it.get("repo") or "")
    owner = repo.split("/")[0] if repo else ""
    blob = " ".join([
        it.get("name") or "", it.get("desc_en") or "",
        it.get("title_zh") or "", repo,
    ])
    if JUNK_RE.search(blob) or (hasattr(sys.modules[__name__], "_chart_skip") and _chart_skip(repo)):
        if owner not in set(T1_AUTHORS):
            return ""
    if owner in set(T1_AUTHORS):
        return "t1-author"
    if TASTE_RE.search(blob):
        return "object"
    if float(it.get("fun_score") or 0) >= 8 and TASTE_RE.search(blob):
        return "fun+object"
    return ""


def _local_copy(it: dict) -> dict:
    """没有 LLM 时：必须已经有能读的中文标题，才用描述补另外两句。英文半截不上架。"""
    title = (it.get("title_zh") or "").strip()
    if sum(1 for c in title if "\u4e00" <= c <= "\u9fff") < 2:
        return {}
    if "英文简介" in title or "见下" in title:
        return {}
    desc = (it.get("why_zh") or it.get("tagline_zh") or it.get("desc_zh") or "").strip()
    if "英文简介" in desc or "见下" in desc:
        desc = ""
    if not desc:
        desc = title + "。装之前先看应用范围。"
    return {
        "title_zh": title[:28],
        "tagline_zh": it.get("tagline_zh") or _clamp_cjk(desc, 36),
        "why_zh": it.get("why_zh") or _clamp_cjk(desc, 80),
        "limit_zh": it.get("limit_zh") or "超出它声明的那一格，产物会串味。对不上就卸。",
    }


def same_day_shelf(ids: list[str], existing: dict) -> int:
    """原声同款：进货和上架同一轮。过门禁且三句文案齐了就 hide:false，写进 curation。"""
    if not ids:
        return 0
    cur = lib.read_json(lib.EDITORIAL, {"items": {}})
    if not isinstance(cur, dict):
        cur = {"items": {}}
    items = cur.setdefault("items", {})
    up = 0
    for sid in ids:
        it = existing.get(sid)
        if not it:
            continue
        lane = _taste_pass(it)
        if not lane:
            it["hide"] = True
            lib.save_item(it)
            print(f"[shelf] 拒 {sid}")
            continue
        blob = (it.get("title_zh") or "") + (it.get("tagline_zh") or "") + (it.get("why_zh") or "")
        if "英文简介" in blob or "见下" in blob or sum(1 for c in (it.get("title_zh") or "") if "\u4e00" <= c <= "\u9fff") < 2:
            it["title_zh"] = it["tagline_zh"] = it["why_zh"] = it["limit_zh"] = ""
        if not (it.get("title_zh") and it.get("why_zh") and it.get("limit_zh")):
            it.update({k: v for k, v in _local_copy(it).items() if not it.get(k)})
        if not (it.get("title_zh") and it.get("why_zh") and it.get("limit_zh")):
            it["hide"] = True
            lib.save_item(it)
            print(f"[shelf] 缺文案留库房 {sid}")
            continue
        if (it.get("title_zh") or "").strip().upper() == "SKIP":
            it["hide"] = True
            lib.save_item(it)
            continue
        it["hide"] = False
        lib.save_item(it)
        patch = items.get(sid, {})
        patch.update({
            "title_zh": it.get("title_zh", ""),
            "why_zh": it.get("why_zh", ""),
            "limit_zh": it.get("limit_zh", ""),
            "tagline_zh": it.get("tagline_zh", ""),
            "hide": False,
            "gate_score": 8,
            "category": it.get("category", ""),
        })
        items[sid] = patch
        up += 1
        print(f"[shelf] 上架 {sid} via {lane}")
    if up:
        cur.setdefault("gate", {})["same_day"] = True
        lib.write_json(lib.EDITORIAL, cur)
    print(f"[shelf] same-day {up}/{len(ids)}")
    return up




# -------------------------------------------------------------- restock ----
def restock_existing(existing: dict, sources: dict) -> None:
    """Refresh stars / pushed_at for repos already on the shelves (cheap, 1 call/repo)."""
    repos = sorted({it["repo"] for it in existing.values()})
    for repo in repos:
        try:
            d = lib.gh_json(f"https://api.github.com/repos/{repo}")
            stars, pushed = d.get("stargazers_count", 0), d.get("pushed_at", "")
            for it in existing.values():
                if it["repo"] == repo:
                    it["stars"], it["pushed_at"] = stars, pushed
                    it["fun_score"] = lib.fun_score(it["name"], it.get("desc_en", ""), stars)
                    lib.save_item(it)
            sources["repos"].setdefault(repo, {})
            sources["repos"][repo].update({"stars": stars, "pushed_at": pushed,
                                           "last_seen": lib.today()})
            time.sleep(0.35)
        except Exception as e:
            print(f"[scout] restock skip {repo}: {e}")


def _chart_skip(full: str) -> bool:
    owner = full.split("/")[0].lower()
    name = full.split("/")[-1].lower()
    if owner in CHART_SKIP_ORGS:
        return True
    if SKIP_REPO_PAT.search(full):
        return True
    if name in {"vscode", "claude-code", "ui", "skills", "agents", "plugins"}:
        return True
    return False


def _fetch_chart_repos() -> list[str]:
    """rising / 7 日趋势 / 社交热度 / 星榜。只抽 owner/repo，不信它的分数。"""
    import csv, io, urllib.request
    seen, out = set(), []
    for url in CHART_CSV:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            raw = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
        except Exception as e:
            print(f"[chart] skip csv {url.split('/')[-1]}: {e}")
            continue
        rows = csv.DictReader(io.StringIO(raw))
        for row in rows:
            repo = (row.get("repo") or row.get("github") or row.get("full_name") or "").strip()
            repo = repo.removeprefix("https://github.com/").rstrip("/")
            if repo.count("/") != 1 or repo in seen:
                continue
            seen.add(repo)
            out.append(repo)
    return out


def watch_charts(existing: dict, sources: dict) -> int:
    """热门榜监视。候选进 discover 同一套 clone + stock，不上架官方厂牌。"""
    from datetime import datetime, timedelta, timezone
    known = set(sources.get("repos", {})) | {it["repo"] for it in existing.values()}
    known |= {k.lower() for k in known}
    candidates: dict[str, dict] = {}

    for repo in _fetch_chart_repos():
        if repo.lower() in known or _chart_skip(repo):
            continue
        try:
            it = lib.gh_json(f"https://api.github.com/repos/{repo}")
        except Exception:
            continue
        if not it or it.get("fork"):
            continue
        ok, lane = _admit(it)
        if not ok:
            continue
        full = it.get("full_name") or repo
        candidates[full] = {
            "stars": it.get("stargazers_count", 0),
            "description": it.get("description") or "",
            "pushed_at": it.get("pushed_at", ""),
            "created_at": it.get("created_at", ""),
            "homepage": it.get("homepage") or "",
            "lane": "chart-" + lane,
        }
        time.sleep(0.25)

    since = (datetime.now(timezone.utc) - timedelta(days=14)).strftime("%Y-%m-%d")
    for tmpl in CHART_SEARCH:
        q = tmpl.format(since=since)
        try:
            url = ("https://api.github.com/search/repositories?q="
                   + urllib.parse.quote(q) + "&order=desc&per_page=15")
            for it in lib.gh_json(url).get("items", []) or []:
                full = it.get("full_name") or ""
                if not full or full.lower() in known or full in candidates or _chart_skip(full):
                    continue
                ok, lane = _admit(it)
                if not ok:
                    continue
                candidates[full] = {
                    "stars": it.get("stargazers_count", 0),
                    "description": it.get("description") or "",
                    "pushed_at": it.get("pushed_at", ""),
                    "created_at": it.get("created_at", ""),
                    "homepage": it.get("homepage") or "",
                    "lane": "trend-" + lane,
                }
            time.sleep(3 if lib.GH_TOKEN else 8)
        except Exception as e:
            print(f"[chart] search skip [{q[:40]}]: {e}")

    ranked = sorted(candidates.items(),
                    key=lambda kv: -lib.fun_score(kv[0], kv[1]["description"], kv[1]["stars"]))
    added, tried = 0, 0
    for repo, meta in ranked:
        if tried >= MAX_CHART_REPOS_PER_RUN:
            break
        tried += 1
        print(f"[chart] candidate {repo} (★{meta['stars']}, via {meta.get('lane')})")
        tmp = tempfile.mkdtemp(prefix="ss_chart_")
        try:
            if not shallow_clone(repo, tmp):
                continue
            items = ingest_repo(tmp, repo, meta, source="chart")
            added += stock(items, existing, sources, repo, meta)
        except Exception as e:
            print(f"[chart] ingest skip {repo}: {e}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    print(f"[chart] {len(candidates)} passed floor, {tried} tried, {added} items added")
    return added


# ------------------------------------------------------------- discover ----
def taste_list_repos() -> list[str]:
    found = []
    pat = re.compile(r"https://github.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")
    for url in TASTE_LISTS:
        try:
            raw = lib.http_get(url) if hasattr(lib, "http_get") else None
            if raw is None:
                req = urllib.request.Request(url, headers={"User-Agent": "pinwei-scout"})
                raw = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
            for owner, name in pat.findall(raw or ""):
                if owner.lower() in {"tluy"}:
                    continue
                found.append(f"{owner}/{name}")
        except Exception as e:
            print("[taste-list]", url, e)
    # stable unique
    out, seen = [], set()
    for r in found:
        k = r.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    print(f"[taste-list] {len(out)} repos from anthologies")
    return out


def discover(existing: dict, sources: dict) -> int:
    known = set(sources["repos"]) | {it["repo"] for it in existing.values()}
    candidates: dict[str, dict] = {}
    extra = [f"repo:{r}" for r in taste_list_repos()]
    for q in list(SEARCH_QUERIES) + extra:
        try:
            url = ("https://api.github.com/search/repositories?q="
                   + urllib.parse.quote(q) + "&order=desc&per_page=20")
            for it in lib.gh_json(url).get("items", []):
                full = it["full_name"]
                if full in known or full in candidates:
                    continue
                if SKIP_REPO_PAT.search(full):
                    continue
                ok, lane = _admit(it)
                if not ok:
                    continue
                candidates[full] = {"stars": it.get("stargazers_count", 0),
                                    "description": it.get("description") or "",
                                    "pushed_at": it.get("pushed_at", ""),
                                    "created_at": it.get("created_at", ""),
                                    "homepage": it.get("homepage") or "",
                                    "lane": lane}
            time.sleep(3 if lib.GH_TOKEN else 8)
        except Exception as e:
            print(f"[scout] search skip [{q[:40]}]: {e}")

    ranked = sorted(candidates.items(),
                    key=lambda kv: -lib.fun_score(kv[0], kv[1]["description"], kv[1]["stars"]))
    added_total, tried = 0, 0
    for repo, meta in ranked:
        if tried >= MAX_NEW_REPOS_PER_RUN:
            break
        tried += 1
        print(f"[scout] candidate {repo} (★{meta['stars']}, via {meta.get('lane','?')})")
        tmp = tempfile.mkdtemp(prefix="ss_")
        try:
            if not shallow_clone(repo, tmp):
                continue
            items = ingest_repo(tmp, repo, meta, source="daily-scout")
            added_total += stock(items, existing, sources, repo, meta)
        except Exception as e:
            print(f"[scout] ingest skip {repo}: {e}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    print(f"[scout] discover: {len(candidates)} candidates, {tried} tried, {added_total} items added")
    return added_total


# ----------------------------------------------------------------- seed ----
def seed(seed_dir: str, meta_file: str) -> None:
    """Local bootstrap from pre-cloned repos. dir names: owner--repo or owner_repo."""
    metas = json.load(open(meta_file, encoding="utf-8")) if os.path.exists(meta_file) else {}
    existing, sources = lib.load_items(), lib.load_sources()
    for d in sorted(os.listdir(seed_dir)):
        local = os.path.join(seed_dir, d)
        if not os.path.isdir(local):
            continue
        repo = d.replace("--", "/", 1) if "--" in d else d.replace("_", "/", 1)
        meta = metas.get(repo, {})
        try:
            items = ingest_repo(local, repo, meta, source="seed")
            stock(items, existing, sources, repo, meta)
        except Exception as e:
            print(f"[seed] skip {repo}: {e}")
    lib.save_sources(sources)
    lib.refresh()



# ------------------------------------------------------- 作者雷达 ----
def watch_authors(existing: dict, sources: dict, limit_per_author: int = 5) -> list[str]:
    """已验证作者雷达：店里每上架一个作者，就盯住他之后发的新仓库。
    好作者会持续产出好东西 —— 这条线的信噪比远高于关键词搜索，
    也是唯一能在「刚发布、零星、没打 topic」阶段就发现新品的自动通道。"""
    from datetime import datetime, timezone
    authors = sorted(set(T1_AUTHORS) | {
        r.split("/")[0] for r in T1_REPOS
    })
    have = {r.lower() for r in sources.get("repos", {})}
    found = []
    for u in authors:
        try:
            items = lib.gh_json(
                f"https://api.github.com/users/{u}/repos?sort=created&direction=desc&per_page={limit_per_author}")
        except Exception:
            continue
        for it in items or []:
            full = it.get("full_name", "")
            if not full or full.lower() in have or it.get("fork"):
                continue
            if SKIP_REPO_PAT.search(full):
                continue
            name = full.split("/")[-1].lower()
            if name in (".github", full.split("/")[0].lower()) or name.endswith(("-site", "-website", "-releases", "-templates")):
                continue                       # 门面/发布通道仓库，不是商品
            age = _days_since(it.get("created_at", ""))
            if age > 60:
                continue
            desc = (it.get("description") or "").lower()
            signal = it.get("stargazers_count", 0) >= 5 or any(
                k in desc for k in ("skill", "agent", "claude", "codex", "mcp"))
            if not signal:
                continue
            found.append((full, it.get("stargazers_count", 0), age,
                          (it.get("description") or "")[:90]))
    found.sort(key=lambda x: x[2])            # 越新越靠前
    for full, st, age, desc in found:
        print(f"[radar] 已验证作者新作 {full} (★{st}, {age:.0f}天前) {desc}")
    return [f[0] for f in found]


def save_method(it: dict) -> bool:
    """把 SKILL.md 正文存到 methods/<id>.md —— 让"方法"在站上可见、可复制。
    这是本店和普通目录站的核心差别：不只告诉你有这个东西，而是把方法本身摊开。
    走 raw CDN，不消耗 API 配额。"""
    import urllib.request
    path = it.get("path", "").rstrip("/")
    url = f"https://raw.githubusercontent.com/{it['repo']}/HEAD/" + (path + "/SKILL.md" if path else "SKILL.md")
    dst = os.path.join("methods", it["id"] + ".md")
    os.makedirs("methods", exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            txt = r.read().decode("utf-8", "ignore")
        if len(txt) > 60000:
            txt = txt[:60000] + "\n\n…（正文过长，已截断，完整版见仓库）"
        with open(dst, "w", encoding="utf-8") as f:
            f.write(txt)
        return True
    except Exception:
        return False


def suggest_repos(repos: list[str], existing: dict, sources: dict) -> None:
    """人工通道：一个真人觉得值得推荐，本身就是最高质量的信号。
    直接 clone + 收录，绕过星门槛；仍尊重 fork/命名黑名单，避免明显垃圾。"""
    for repo in repos:
        repo = repo.strip().removeprefix("https://github.com/").rstrip("/")
        if SKIP_REPO_PAT.search(repo):
            print(f"[scout] suggest 拒绝（命名黑名单）: {repo}")
            continue
        meta = {"stars": 0, "description": "", "pushed_at": ""}
        try:
            info = lib.gh_json(f"https://api.github.com/repos/{repo}")
            if info.get("fork"):
                print(f"[scout] suggest 拒绝（fork）: {repo}")
                continue
            meta = {"stars": info.get("stargazers_count", 0),
                    "description": info.get("description") or "",
                    "pushed_at": info.get("pushed_at", "")}
        except Exception as e:
            print(f"[scout] suggest 无法读取元数据 {repo}: {e}")
        tmp = tempfile.mkdtemp(prefix="sg_")
        try:
            if not shallow_clone(repo, tmp):
                print(f"[scout] suggest clone 失败: {repo}")
                continue
            items = ingest_repo(tmp, repo, meta, source="human-suggested")
            n = stock(items, existing, sources, repo, meta)
            print(f"[scout] suggest 收录 {repo}: +{n} 件（★{meta['stars']}，绕过星门槛）")
        except Exception as e:
            print(f"[scout] suggest 失败 {repo}: {e}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


# 探路候选。**顺序即优先级**，前面的先试。
# 为什么要有这张表：`path` 记错时，光报错不给候选，人还是得一个个 clone 去找。
# `.claude/skills/<name>` 排在很前面是实测出来的 —— 作者把 skill 装在自己项目里
# 是最常见的布局之一，而它以点开头，肉眼扫仓库首页根本看不见。
PATH_CANDIDATES = (
    "", "{name}", "skills/{name}", ".claude/skills/{name}", ".agents/skills/{name}",
    "plugin/skills/{name}", "plugins/{name}/skills/{name}", "skill", "skills",
    "src/skills/{name}", "packages/cli/skill", "claude-runtime/skills/{name}",
)


def probe_path(repo: str, name: str, timeout: int = 15) -> list[str]:
    """挨个试候选位置，返回**所有**能取回 SKILL.md 的路径。

    返回全部而不是第一个 —— 一个仓库里同名 skill 出现在多处（`.claude/skills/x`
    和 `plugins/y/skills/x`）是常态，机器判不了哪个是这张卡指的那件。
    给人一张候选清单去选，比替人挑一个然后可能挑错强。
    """
    import urllib.request
    seen, hits = set(), []
    for tpl in PATH_CANDIDATES:
        rel = tpl.format(name=name).strip("/")
        if rel in seen:
            continue
        seen.add(rel)
        url = (f"https://raw.githubusercontent.com/{repo}/HEAD/"
               + (rel + "/SKILL.md" if rel else "SKILL.md"))
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            urllib.request.urlopen(req, timeout=timeout).read(1)
            hits.append(rel)
        except Exception:
            pass
    return hits


def verify_paths() -> int:
    """复核每件在架商品的 path 是否真能取回 SKILL.md。

    只报告，**不自动改**。探到"真实位置"是猜的（一个仓库里可能有几十个
    SKILL.md，哪个才是这张卡指的那件，机器判不了），猜错比不改更糟 ——
    用户照抄一条看起来对的命令装到错的东西，比装不上更难发现。
    合集（kind=collection）本来就没有单一 SKILL.md，不算欠账，单列。
    """
    import urllib.request
    # 必须过一遍编辑层：hide 大多写在 editorial/curation.json 里，
    # 只读 skills/*.json 会把 559 件未上架的也当成在架。
    items = lib.apply_editorial(lib.load_items())
    shelved = [it for it in items.values() if not it.get("hide")]
    bad, cols = [], []
    for it in sorted(shelved, key=lambda x: x["id"]):
        if it.get("kind") == "collection":
            cols.append(it); continue
        path = (it.get("path") or "").rstrip("/")
        url = (f"https://raw.githubusercontent.com/{it['repo']}/HEAD/"
               + (path + "/SKILL.md" if path else "SKILL.md"))
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            urllib.request.urlopen(req, timeout=20).read(1)
        except Exception as e:
            bad.append((it, getattr(e, "code", str(e))))
    print(f"[verify] 在架 {len(shelved)} 件：单品 {len(shelved)-len(cols)} · 合集 {len(cols)}")
    for it, why in bad:
        print(f"[verify] ✗ {it['id']}  repo={it['repo']} path={it.get('path','')!r} ({why})")
        print(f"           install.copy = {it.get('install', {}).get('copy', '')}")
        hits = probe_path(it["repo"], it.get("name", ""))
        if hits:
            print(f"           候选位置（探到 {len(hits)} 处，**要人选，不自动改**）: "
                  + " | ".join(repr(h) for h in hits))
        else:
            print("           候选位置：一处都探不到 —— 多半是仓库没了或改名了")
    print(f"[verify] 单品里取不回正文的 {len(bad)} 件"
          + ("（这些的 install.copy 不可信）" if bad else "，全部可取"))
    print(f"[verify] 合集 {len(cols)} 件不参与本项 —— 合集没有单一 SKILL.md，"
          "它们的 install.copy 是另一个问题，见 docs/PROTOCOL.md")
    return 1 if bad else 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", help="seed from a directory of pre-cloned repos")
    ap.add_argument("--meta", default="", help="json map full_name -> {stars,description,pushed_at}")
    ap.add_argument("--no-discover", action="store_true")
    ap.add_argument("--no-charts", action="store_true")
    ap.add_argument("--no-restock", action="store_true")
    ap.add_argument("--suggest", nargs="+", metavar="owner/repo",
                    help="人工通道：直接收录指定仓库，完全绕过星门槛（仅 fork 与命名黑名单仍生效）")
    ap.add_argument("--verify-paths", action="store_true",
                    help="复核在架商品的 path 能不能取回 SKILL.md（只报告，不改数据）")
    ap.add_argument("--enrich-missing", action="store_true",
                    help="给所有在架、仍是占位/缺文案的商品补写文案（用 LLM_* secrets）")
    a = ap.parse_args()
    if a.verify_paths:
        sys.exit(verify_paths())
    if a.seed:
        seed(a.seed, a.meta)
        return
    existing, sources = lib.load_items(), lib.load_sources()
    if a.enrich_missing:
        miss = [sid for sid, it in existing.items()
                if not it.get("hide") and (not it.get("why_zh") or "见下" in it.get("tagline_zh", ""))]
        print(f"[scout] enrich-missing: {len(miss)} 件在架占位货待补")
        enrich_items(miss, existing)
        lib.refresh()
        return
    if a.suggest:
        suggest_repos(a.suggest, existing, sources)
        enrich_items(NEW_IDS, existing)
        same_day_shelf(NEW_IDS, existing)
        lib.save_sources(sources)
        lib.refresh()
        return
    if not a.no_restock:
        restock_existing(existing, sources)
    if not a.no_discover:
        radar = watch_authors(existing, sources)
        if radar:
            suggest_repos(radar[:4], existing, sources)   # 已验证作者的新作，绕过星门槛
        # 图册名单直接进货，不走 GitHub 仓库搜索（repo:owner/name 几乎搜不到）
        taste = [r for r in taste_list_repos()
                 if r not in sources.get("repos", {})
                 and r.lower() not in { (it.get("repo") or "").lower() for it in existing.values() }]
        if taste:
            print(f"[taste] {len(taste)} unseen, taking {min(4, len(taste))}")
            suggest_repos(taste[:4], existing, sources)
        if not a.no_charts:
            watch_charts(existing, sources)
        discover(existing, sources)
    enrich_items(NEW_IDS, existing)
    same_day_shelf(NEW_IDS, existing)
    lib.save_sources(sources)
    lib.refresh()


if __name__ == "__main__":
    main()
