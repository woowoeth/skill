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
import os, re, sys, json, time, shutil, argparse, tempfile, subprocess as sp, urllib.parse

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

SEARCH_QUERIES = [
    "topic:claude-skills sort:updated",
    "topic:claude-code-skills sort:updated",
    "topic:agent-skills sort:updated",
    "claude skill game OR fun OR creative in:name,description sort:updated",
    "SKILL.md skill in:readme claude sort:updated",
    # 新品/新星专用：按创建时间倒序，让刚出生、还没积累星的好货进入结果
    "topic:claude-skills sort:created",
    "topic:agent-skills sort:created",
    "SKILL.md agent skill in:readme sort:created",
    "claude skill in:name,description sort:created",
]

SKIP_REPO_PAT = re.compile(
    r"awesome-|awesome$|^.*/(dotfiles|test|demo|example|template)s?$|guide|tutorial|handbook|cookbook|cheatsheet|-docs?$", re.I)


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


def find_skill_mds(root: str) -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in
                       (".git", "node_modules", "vendor", "dist", "build")]
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
        items.append(lib.make_item(kind="collection", name=repo.split("/")[-1],
                                   desc_en=repo_desc or f"A pack of {n} skills.",
                                   repo=repo, path="", stars=stars,
                                   repo_desc=repo_desc, pushed_at=pushed,
                                   homepage=homepage, skill_count=n, source=source))
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


NEW_IDS: list[str] = []


def stock(items: list[dict], existing: dict, sources: dict, repo: str, meta: dict) -> int:
    added = 0
    cover = resolve_cover(repo) if items else ""
    for it in items:
        if it["id"] in existing:
            continue
        if cover:
            it["cover"] = cover
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
        if m and "repository-images.githubusercontent.com" in m.group(1):
            return m.group(1)
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
        for n, m in enumerate(re.finditer(r'<img[^>]+src="([^"]+)"', h)):
            if n >= 8:
                break
            src = m.group(1)
            if not src.startswith("http") or BADGE_PAT.search(src):
                continue
            return src   # 不再用脚本 UA 验证：GitHub 对非浏览器 UA 返 403，会误杀浏览器能正常加载的图
    except Exception:
        pass
    return ""


# ---------------------------------------------------------------- enrich ----
LLM_KEY = os.environ.get("LLM_API_KEY", "").strip()
LLM_BASE = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1").strip().rstrip("/")
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o-mini").strip()

ENRICH_PROMPT = """你是「Skill 商店」店长，为一件新上架的 Agent Skill 写中英双语货架文案。这是一家只留精品的小店，文案要让人「一眼想试」，不要正确的废话。

硬性要求（超限即失败）：
- title_zh：中文名，≤8 个汉字。贴切、可有趣，不生造成语。
- tagline_zh：一句钩子，中文 40~58 字（务必两行、不超 58）。写「具体场景/痛点/反差 + 一个别处没有的细节」，禁止「实用利器」「效率神器」「必备工具」这类空话。
- tagline_en：英文钩子，严格 ≤115 个英文字符（含空格；宁短勿超）。与中文同义但地道，不要逐字翻译。
- why_zh：一句点评，中文 30~52 字。只说「它到底比同类强在哪」——机制或差异点，诚实具体，不吹不堆形容词。
- why_en：英文点评，≤130 个英文字符。

只输出一个 JSON 对象，含 title_zh, tagline_zh, tagline_en, why_zh, why_en 五个键，不要 markdown、不要解释。

商品信息：
name: {name}
repo: {repo}
kind: {kind}
description: {desc}"""


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
        patch["title_zh"] = patch["title_zh"][:8]
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
                     ("title_zh", "tagline_zh", "tagline_en", "why_zh", "why_en")
                     if c.get(k) and str(c[k]).strip()}
            patch = _clamp_patch(patch)
            if patch:
                it.update(patch)
                lib.save_item(it)
                done += 1
        except Exception as e:  # never let copywriting break the restock
            print(f"[scout] enrich {sid}: {e}")
    print(f"[scout] enrich: {done}/{len(ids)} items copywritten by {LLM_MODEL}")




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


# ------------------------------------------------------------- discover ----
def discover(existing: dict, sources: dict) -> int:
    known = set(sources["repos"]) | {it["repo"] for it in existing.values()}
    candidates: dict[str, dict] = {}
    for q in SEARCH_QUERIES:
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
    authors = sorted({r.split("/")[0] for r in sources.get("repos", {})})
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", help="seed from a directory of pre-cloned repos")
    ap.add_argument("--meta", default="", help="json map full_name -> {stars,description,pushed_at}")
    ap.add_argument("--no-discover", action="store_true")
    ap.add_argument("--no-restock", action="store_true")
    ap.add_argument("--suggest", nargs="+", metavar="owner/repo",
                    help="人工通道：直接收录指定仓库，完全绕过星门槛（仅 fork 与命名黑名单仍生效）")
    ap.add_argument("--enrich-missing", action="store_true",
                    help="给所有在架、仍是占位/缺文案的商品补写文案（用 LLM_* secrets）")
    a = ap.parse_args()
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
        lib.save_sources(sources)
        lib.refresh()
        return
    if not a.no_restock:
        restock_existing(existing, sources)
    if not a.no_discover:
        radar = watch_authors(existing, sources)
        if radar:
            suggest_repos(radar[:4], existing, sources)   # 已验证作者的新作，绕过星门槛
        discover(existing, sources)
    enrich_items(NEW_IDS, existing)
    lib.save_sources(sources)
    lib.refresh()


if __name__ == "__main__":
    main()
