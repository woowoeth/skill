#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
品味 (Pinwei) — shared scout library.

The repo is the database:
  skills/<id>.json          one file per shelf item (a skill or a collection)
  skills/feed.json          aggregated feed the static site reads
  skills/rejected-feed.json 拒收榜: what got turned away, and why
  editorial/curation.json   店长文案，永远覆盖机器字段
  editorial/headline.json   每日头条，人写，机器只读
  editorial/rejected.json   人写的拒收理由，挂 docs/CURATION.md 的条款
  scouts/scan_log.json      机器扫描留痕，网站上的统计数字来自这里

Design mirrors ourword-ai/idea: scouts are fault-tolerant, every helper
swallows single-item failures, and feed.json is always regenerated from
the merged set of skills/*.json (conflict-safe).
"""
from __future__ import annotations
import os, re, sys, json, time, glob, hashlib, urllib.request, urllib.error, datetime

# 备料徽章：从 methods/ 本地正文算，零网络。
# 显式把 scouts/ 放进 path —— seo/ 和仓库根都会 import scout_lib，不能假定调用方的 cwd。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prep_signals as prep  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT, "skills")
FEED = os.path.join(SKILLS_DIR, "feed.json")
REJECTED_FEED = os.path.join(SKILLS_DIR, "rejected-feed.json")
EDITORIAL = os.path.join(ROOT, "editorial", "curation.json")
HEADLINE = os.path.join(ROOT, "editorial", "headline.json")
REJECTED = os.path.join(ROOT, "editorial", "rejected.json")
SOURCES = os.path.join(ROOT, "scouts", "sources.json")
SCAN_LOG = os.path.join(ROOT, "scouts", "scan_log.json")

# feed.json 之外，skills/ 里所有以 -feed.json 结尾的都是聚合产物，不是货
AGGREGATE_FILES = {"feed.json", "rejected-feed.json"}

GH_TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
UA = "pinwei-skill-scout/1.0 (+https://github.com/woowoeth/skill)"

# ---------------------------------------------------------------- shelves ---
# 分类是**动词开头的使用场景**，不是学科名 —— 「做图」不是「设计」，「过日子」不是「生活方式」。
#
# learn / body 是第二批加的。加它们的理由不是分类学，是**一次上新把洞照了出来**：
# 8 个格子里既没有「学」也没有「身体」，于是学习方法、升学、教辅、心理、育儿、
# 健身、中医、过敏预报全被塞进「过日子」——那一格一度占到在架的三分之一（63/198）。
# 一个装着 63 件、没有内部结构的筛子，读者点进去等于没筛。
CATEGORIES = [
    ("creative", "做图",   "Images",   "🎨"),
    ("writing",  "写字",   "Writing",  "✍️"),
    ("life",     "生活",   "Everyday", "🧺"),
    ("work",     "工作",   "Work",     "💼"),
    ("fun",      "玩乐",   "Play",     "🎲"),
]
CAT_MERGE = {
    "body": "life", "docs": "work",
    "learn": "life", "dev": "work", "meta": "work",
}
CAT_IDS = [c[0] for c in CATEGORIES]

# ---------------------------------------------------------- editorial layer ---
# 人写的字段。机器只在这些字段"没有值"时填默认空串，永远不覆盖已有内容。
# 新增字段加到这里就够了 —— refresh() 会自动保证 feed 里每件都带这些键。
EDITORIAL_TEXT_FIELDS = (
    "title_zh", "tagline_zh", "tagline_en",
    "why_zh", "why_en",
    "limit_zh", "limit_en",     # 诚实的局限：机制短板 / 平台限制 / 适用边界
    # 卡片上那一行短版局限（≤30 字，必须完整句）。**不是 limit_zh 的截断**——
    # 一句完整的诚实短处被砍成前 24 字，读起来就成了勾人往下点的钩子，诚实变成营销。
    # 详情页仍用完整的 limit_zh，两者是同一件事的两种说法，不是摘要关系。
    "limit_brief_zh", "limit_brief_en",
)

# 机器取的字段，人不写。和 EDITORIAL_TEXT_FIELDS 一样只 setdefault，不覆盖。
MACHINE_TEXT_FIELDS = (
    "repo_created_at",      # 仓库创建日 —— GET /repos/{repo}
    "skill_first_seen",     # 这个 path 下最早一次提交 —— 才是「这一件」的年龄
)

# ---------------------------------------------------------- 拒收条款 ---
# 对应 docs/CURATION.md。reject_rule 只能是这五个之一 —— 挂不上任何一条，
# 说明标准没写清，去改 CURATION.md，不要新造一条规则。
REJECT_RULES = [
    ("问一", "不是拿走就能用的商品",   "Not a take-and-use product",
     "框架/底座、教程、脚手架、别人项目自己的装修配置"),
    ("问二", "用户在别处拿得到",       "No increment over any other directory",
     "官方厂商目录、通用开发件、数量堆、已有更好同类在架"),
    ("问三", "写不出让人想装的文案",   "No copy worth writing",
     "只能憋出「一个不错的 X 工具」= 它没有值得说的点"),
    ("红线", "无条件拒",               "Hard red line",
     "攻击赋能安全工具、灰产、荐股/交易信号、价值观有害"),
    ("门槛", "机器初筛未过",           "Below the machine floor",
     "fork、命名黑名单、四条准入通道全不命中。人工可推翻"),
]
REJECT_RULE_IDS = [r[0] for r in REJECT_RULES]

CAT_KW = {
    "creative": ["art", "design", "draw", "svg", "canvas", "image", "sprite", "pixel",
                 "animation", "video", "music", "audio", "generative", "creative",
                 "diagram", "poster", "logo", "theme", "gif", "3d", "shader", "设计", "画", "视频", "配图"],
    "fun":      ["game", "play", "fun", "joke", "meme", "tarot", "fortune", "astrolog",
                 "trivia", "puzzle", "story game", "roleplay", "rpg", "chess", "quiz",
                 "emoji", "caveman", "lazy", "personality", "游戏", "塔罗", "占卜", "好玩", "整活"],
    "writing":  ["write", "writing", "writer", "rewrite", "novel", "fiction", "story",
                 "poem", "poetry", "blog", "copywriting", "translate", "translation",
                 "prose", "essay", "humanize", "humanizer", "tone", "editor", "summary",
                 "小说", "网文", "写作", "文案", "翻译", "公众号", "润色", "总结"],
    # life 里原本挂着 fitness/health/diet —— 那三个词现在归 body。
    # 留在 life 的是**吃住行玩养宠**这一路：做饭、旅行、装修、种菜、养猫、钓鱼。
    "life":     ["cook", "recipe", "travel", "trip", "meal", "journal", "diary", "habit",
                 "budget", "shopping", "gift", "wedding", "pet", "cat", "dog", "garden",
                 "baking", "coffee", "fishing", "resume", "cv", "interview prep",
                 "生活", "菜谱", "旅行", "简历", "装修", "宠物", "养猫", "种菜", "烘焙", "咖啡"],
    "learn":    ["study", "learning", "learn ", "tutor", "flashcard", "anki", "spaced repetition",
                 "exam", "quiz prep", "vocabulary", "grammar", "language learning", "ielts",
                 "toefl", "gaokao", "kaoyan", "homework", "curriculum", "syllabus", "olympiad",
                 "math tutor", "lecture", "note-taking", "memoriz",
                 "学习", "背单词", "刷题", "考研", "高考", "四六级", "升学", "志愿", "作业",
                 "辅导", "备考", "复习", "奥数", "闪卡", "记忆", "口语", "教辅"],
    "body":     ["fitness", "workout", "training plan", "strength", "hypertrophy", "running",
                 "marathon", "cycling", "swim", "yoga", "stretch", "mobility", "rehab",
                 "nutrition", "diet", "calorie", "macro", "sleep", "health", "medical",
                 "allergy", "pollen", "tcm", "acupunctur", "herbal",
                 "健身", "增肌", "减脂", "训练", "跑步", "马拉松", "拉伸", "康复", "营养",
                 "热量", "睡眠", "健康", "过敏", "花粉", "中医", "针灸", "体检", "膳食"],
    "docs":     ["docx", "pdf", "pptx", "xlsx", "spreadsheet", "slide", "presentation",
                 "word document", "excel", "report", "form", "invoice", "文档", "表格", "幻灯"],
    "work":     ["marketing", "seo", "growth", "sales", "product manag", "pm ", "roadmap",
                 "email", "slack", "notion", "crm", "analytics", "business", "legal",
                 "finance", "strategy", "meeting", "运营", "营销", "增长", "法务", "商业"],
    "dev":      ["code", "coding", "test", "tdd", "debug", "git", "deploy", "devops", "api",
                 "refactor", "typescript", "python", "rust", "sql", "database", "security",
                 "frontend", "backend", "unity", "godot", "engine", "mcp", "开发", "代码", "部署"],
    "meta":     ["skill-creator", "skill creator", "write skills", "meta", "prompt",
                 "agent memory", "context", "harness", "orchestrat", "subagent",
                 "skill pack", "评估", "元"],
}

FUN_KW = {  # what makes something 好玩 — weighted
    5: ["game", "tarot", "fortune", "meme", "joke", "caveman", "塔罗", "占卜", "整活", "玩"],
    4: ["novel", "story", "fiction", "rpg", "roleplay", "pixel", "sprite", "music",
        "poetry", "poem", "网文", "小说", "游戏"],
    3: ["art", "creative", "generative", "animation", "gif", "emoji", "design", "video",
        "draw", "fun", "lazy", "taste", "personality", "画", "设计", "好玩"],
    2: ["cook", "recipe", "travel", "gift", "wedding", "humanize", "adhd", "菜谱", "旅行"],
    1: ["visual", "theme", "canvas", "diagram", "写作", "翻译"],
}

# ------------------------------------------------------------- utilities ---
def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def round_id() -> str:
    """Unique id for one scan round. now_iso() alone collides — two runs inside
    the same second would merge into one round and the counts would be wrong."""
    return now_iso() + "-" + hashlib.md5(
        f"{os.getpid()}{time.time_ns()}".encode()).hexdigest()[:6]

def today() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

def slug(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff._-]+", "-", (s or "").strip()).strip("-._").lower()
    return s[:80] or hashlib.md5((s or "x").encode()).hexdigest()[:8]

def http_get(url: str, retries: int = 3, timeout: int = 30, token: str | None = None) -> str:
    h = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    tok = token if token is not None else GH_TOKEN
    if tok and "api.github.com" in url:
        h["Authorization"] = f"Bearer {tok}"
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=h)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            last = e
            time.sleep(2 * (i + 1))
    raise last  # type: ignore[misc]

def gh_json(url: str):
    return json.loads(http_get(url))

def has_kw(text: str, kws) -> bool:
    t = (text or "").lower()
    for k in kws:
        if re.search(r"[\u4e00-\u9fff]", k):
            if k in t:
                return True
        elif re.search(r"(?<![a-z0-9])" + re.escape(k) + r"(?![a-z0-9])", t):
            return True
    return False

# -------------------------------------------------------- SKILL.md parse ---
_FM = re.compile(r"^\ufeff?\s*---\s*\n(.*?)\n---\s*\n?", re.S)

def parse_skill_md(text: str) -> dict:
    """Extract name/description from YAML frontmatter without a YAML dep.
    Handles quoted values, folded scalars (>, >-, |) and simple multiline."""
    out = {"name": "", "description": ""}
    m = _FM.match(text or "")
    if not m:
        return out
    lines = m.group(1).splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        km = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line)
        if not km:
            i += 1
            continue
        key, val = km.group(1).lower(), km.group(2).strip()
        if val in (">", ">-", "|", "|-", ""):  # block scalar / empty → gather indented block
            block, i2 = [], i + 1
            while i2 < len(lines) and (lines[i2].startswith((" ", "\t")) or not lines[i2].strip()):
                block.append(lines[i2].strip())
                i2 += 1
            val, i = " ".join(b for b in block if b), i2 - 1
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        if key in ("name", "description") and val:
            out[key] = val.replace("\\n", " ").strip()
        i += 1
    return out

def first_heading(text: str) -> str:
    for line in (text or "").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""

# ------------------------------------------------------ classify & score ---
def infer_category(name: str, desc: str, repo_desc: str = "") -> str:
    blob = f"{name} {desc} {repo_desc}"
    scores = {c: 0 for c in CAT_IDS}
    for cat, kws in CAT_KW.items():
        dest = CAT_MERGE.get(cat, cat)
        if dest not in scores:
            dest = "fun"
        for k in kws:
            if has_kw(blob, [k]):
                scores[dest] += 2 if has_kw(f"{name} {desc[:80]}", [k]) else 1
    best = max(scores, key=lambda c: (scores[c], -CAT_IDS.index(c)))
    return best if scores[best] > 0 else "fun"

def fun_score(name: str, desc: str, stars: int = 0, pushed_days_ago: int = 999) -> float:
    blob = f"{name} {desc}"
    s = 0.0
    for w, kws in FUN_KW.items():
        for k in kws:
            if has_kw(blob, [k]):
                s += w
    s = min(s, 14.0)
    import math
    s += min(math.log10(max(stars, 1)) * 0.9, 4.5)          # popularity, capped
    if pushed_days_ago <= 7:  s += 1.5                       # freshness
    elif pushed_days_ago <= 30: s += 0.7
    return round(s, 2)

# ------------------------------------------------- bilingual fallback copy ---
CAT_ZH_VERB = {
    "creative": "让 Claude 帮你搞创作", "fun": "纯属好玩，装了不亏",
    "writing": "写字的人会喜欢", "life": "过日子用得上",
    "docs": "正经办公文档", "work": "打工人的外挂",
    "dev": "写代码的顺手工具", "meta": "调教技能的技能",
}

def zh_fallback(name: str, desc_en: str, cat: str) -> str:
    """Deterministic zh one-liner when no editorial/LLM copy exists."""
    return f"{CAT_ZH_VERB.get(cat, '一个有意思的技能')}：{name}。英文简介见下。"

# ----------------------------------------------------------- item builder ---
def make_item(*, kind: str, name: str, desc_en: str, repo: str, path: str = "",
              stars: int = 0, repo_desc: str = "", pushed_at: str = "",
              homepage: str = "", skill_count: int = 1, source: str = "scout",
              added_at: str | None = None) -> dict:
    try:
        pushed_days = (datetime.datetime.now(datetime.timezone.utc)
                       - datetime.datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))).days if pushed_at else 999
    except Exception:
        pushed_days = 999
    cat = infer_category(name, desc_en, repo_desc)
    fs = fun_score(name, desc_en + " " + repo_desc, stars, pushed_days)
    owner = repo.split("/")[0]
    sid = slug(f"{repo.replace('/', '-')}" + (f"-{name}" if kind == "skill" and path else ""))
    url = f"https://github.com/{repo}" + (f"/tree/HEAD/{path}" if path else "")
    # 安装目录名：**优先用 frontmatter 的 name**，路径末段只当兜底。
    #
    # 原来是反过来的（路径末段优先），后果不是名字难看，是**静默覆盖**：
    # skill 放在 `skill/`、`skills/`、`packages/cli/skill/` 这种通用目录里时，
    # 安装目标就成了 `~/.claude/skills/skill`。在架 6 件中招，其中 4 件都指向
    # 同一个目录 —— 装了 refly 再装 pinchbench，后者**把前者盖掉，用户不会收到任何提示**。
    #
    # 兜底顺序：name → 路径末段（且不是 skill/skills/src/lib 这类通用词）→ 仓库名。
    GENERIC_DIRS = {"skill", "skills", "src", "lib", "packages", "dist", "app", "plugin", "plugins"}
    tail = path.rstrip("/").split("/")[-1] if path else ""
    dirname = (slug(name)
               or (tail if tail and tail.lower() not in GENERIC_DIRS else "")
               or slug(repo.split("/")[-1]))
    install = {
        "clone": f"git clone --depth 1 https://github.com/{repo}.git",
        "copy":  (f"cp -r {repo.split('/')[-1]}/{path} ~/.claude/skills/{dirname}" if path
                  else f"mv {repo.split('/')[-1]} ~/.claude/skills/{dirname}"),
        "dir":   f"~/.claude/skills/{dirname}",
    }
    return {
        "id": sid, "kind": kind, "name": name,
        "title_zh": "", "tagline_zh": zh_fallback(name, desc_en, cat), "tagline_en": "",
        "desc_en": (desc_en or repo_desc or "").strip()[:400],
        "why_zh": "", "why_en": "",
        # 诚实的局限。机器写不出来，留空等人写 —— 空串在 check_curation.py 里会被点名。
        "limit_zh": "", "limit_en": "",
        "repo": repo, "owner": owner, "path": path, "url": url, "homepage": homepage,
        "stars": stars, "pushed_at": pushed_at, "skill_count": skill_count,
        "category": cat, "fun_score": fs, "pick": False,
        # **新抓的一律默认不上架。** 上架是人写完文案之后的动作，不是抓取的副作用。
        # 2026-08-20 的教训：定时进货员上了 21 件机器占位文案（中文标题/点评/局限、
        # 英文四项全空），店主一眼看出来「上新的内容也都没有，只有个标题」。
        # 根因就在这一行 —— 而 CURATION.md 第五节早就写着「自动进货只负责往候选池里
        # 放东西，**不直接上架**」。设计写对了，实现是反的。
        # 恢复上架靠 editorial/curation.json 里人写的 hide:false，或人工改这个文件。
        "hide": True,
        "source": source, "added_at": added_at or today(), "install": install,
    }

# --------------------------------------------------------------- storage ---
def read_json(path: str, default):
    """Never let a missing/broken sidecar file take the build down."""
    if not os.path.exists(path):
        return default
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[lib] unreadable {os.path.relpath(path, ROOT)}: {e}")
        return default

def write_json(path: str, data) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

def load_items() -> dict:
    items = {}
    for p in glob.glob(os.path.join(SKILLS_DIR, "*.json")):
        if os.path.basename(p) in AGGREGATE_FILES:
            continue
        try:
            with open(p, encoding="utf-8") as f:
                it = json.load(f)
            items[it["id"]] = it
        except Exception as e:
            print(f"[lib] skip bad {p}: {e}")
    return items

def save_item(it: dict) -> None:
    os.makedirs(SKILLS_DIR, exist_ok=True)
    with open(os.path.join(SKILLS_DIR, f"{it['id']}.json"), "w", encoding="utf-8") as f:
        json.dump(it, f, ensure_ascii=False, indent=1)

def apply_editorial(items: dict) -> dict:
    """editorial/curation.json overrides win over scouted fields, always."""
    cur = read_json(EDITORIAL, None)
    if not cur:
        return items
    for sid, patch in cur.get("items", {}).items():
        if sid in items:
            items[sid].update({k: v for k, v in patch.items()
                               if k != "id" and not k.startswith("_")})
    return items

def age_source(it: dict) -> str:
    """这件商品的「年龄」该报哪个日期 —— **本地零网络就能定的口径**。

    店主问的是「**这件 skill** 什么时候出现的」。仓库创建时间只在一种情况下等于它：
    这件 skill 就是仓库本体（`path` 为空）。skill 长在子目录里时，仓库可能先建了几个月，
    skill 是后加的 —— 实测样本（6 件子目录货）差 1 / 2 / 4 / 25 / 101 / 111 天。

    111 天听着不多，但**它和我们自己的时间窗同阶**：`CURATION.md` 的准入通道写着
    「新品快车道：创建 ≤7 天」「星速度：创建 ≤14 天」。拿仓库年龄当 skill 年龄，
    一个 111 天前建的仓库里上周新加的 skill 会被当成老货，它其实正命中新品快车道。

      "file"  —— 拿到了 skill_first_seen，这一件自己的首次出现时间。最准，显示。
      "repo"  —— path 为空，这件就是仓库本体，仓库创建时间就是它的年龄。显示。
      ""      —— 只有 repo_created_at 而这件长在子目录里：那是**仓库**的年龄不是
                 **它**的年龄，答非所问。**前端不显示**，而不是显示一个近似值。

    第三档是这个函数存在的理由。少了它，一半的货（在架 152 件里 78 件是子目录货）
    会顶着「repo」这个口径标签印出一个不回答问题的日期 —— 那正是
    「印在货架上的数字没核过来源」那个病的下一次发作。
    """
    if (it.get("skill_first_seen") or "").strip():
        return "file"
    if not (it.get("path") or "").strip():
        return "repo" if (it.get("repo_created_at") or "").strip() else ""
    return ""


def normalize_item(it: dict) -> dict:
    """Guarantee every shelf item carries the full editorial key set.

    setdefault, never assignment: a field the editorial layer (or an older
    scout run) already filled in is left exactly as it was. This is what makes
    it safe to add a new copy field — 713 files on disk predate limit_zh and
    must not be rewritten to get it.
    """
    for k in EDITORIAL_TEXT_FIELDS:
        it.setdefault(k, "")
    for k in MACHINE_TEXT_FIELDS:
        it.setdefault(k, "")
    # 派生，每次重建都重算 —— 补上了日期，口径自动跟着变，没有第二份真相。
    it["age_source"] = age_source(it)
    return it

# ------------------------------------------------------------- 头条 / headline ---
def build_headline(items: dict, when: str | None = None) -> tuple[dict | None, list]:
    """Resolve today's headline + the archive trail from editorial/headline.json.

    Why the history lives as an append-only array in the editorial layer:
      - 人选人写，机器不碰 —— scout 只读这个文件，永远不写，所以没有覆盖风险
      - append-only 数组天然就是归档：第 N 天的头条永远还在第 N 个位置
      - date 可以写未来 —— 到那天自动上位，头条可以提前排期
      - 只存 id 不存文案副本：商品文案改了，头条跟着改，没有第二份真相
    Returns (headline_or_None, history_list).
    """
    doc = read_json(HEADLINE, None) or {}
    rows = [h for h in doc.get("headlines", []) if isinstance(h, dict) and h.get("date") and h.get("id")]
    rows.sort(key=lambda h: h["date"])
    day = when or today()

    hist, current = [], None
    for h in rows:
        it = items.get(h["id"])
        rec = {
            "date": h["date"],
            "id": h["id"],
            "kicker_zh": h.get("kicker_zh", ""),
            "story_zh": h.get("story_zh", ""),
            "story_en": h.get("story_en", ""),
            "by": h.get("by", "店长"),
            # 冗余一点点展示字段，归档页不用再去 feed.json 里查
            "title_zh": (it or {}).get("title_zh", ""),
            "name": (it or {}).get("name", ""),
            "repo": (it or {}).get("repo", ""),
            "resolved": bool(it) and not (it or {}).get("hide"),
        }
        hist.append(rec)
        if h["date"] <= day and rec["resolved"]:
            current = dict(rec, item=it)      # 当日头条内联整件商品，首页零查找
    hist.reverse()                            # 最新在前
    if current is None and rows:
        print("[lib] headline: no usable entry for today (id missing/hidden or all dates in the future)")
    return current, hist

# ------------------------------------------------------- 拒收榜 / reject ledger ---
# 机器扫描留痕。skill_scout.discover() 里被 SKIP_REPO_PAT / _admit() 刷掉的仓库
# 原来是 `continue` 直接丢掉的，一行痕迹都没有 —— 这三个函数是给它的留痕口。
_ROUND: dict = {"scanned": 0, "admitted": [], "rejects": [], "started_at": None}

def note_scanned(n: int = 1) -> None:
    """每从搜索结果里看到一条仓库就记一次。这个数就是网站上那个「今天扫了多少」。"""
    if _ROUND["started_at"] is None:
        _ROUND["started_at"] = round_id()
    _ROUND["scanned"] += n

def note_admitted(repo: str) -> None:
    if _ROUND["started_at"] is None:
        _ROUND["started_at"] = round_id()
    if repo not in _ROUND["admitted"]:
        _ROUND["admitted"].append(repo)

def record_reject(repo: str, reason: str, rule: str = "门槛", *,
                  name: str = "", desc: str = "", stars: int = 0) -> None:
    """留痕一次机器拒收。缓存在内存里，flush_round() 时一次性落盘。"""
    if _ROUND["started_at"] is None:
        _ROUND["started_at"] = round_id()
    _ROUND["rejects"].append({
        "repo": repo, "name": name, "desc": (desc or "")[:200],
        "reject_reason_zh": reason,
        "reject_rule": rule if rule in REJECT_RULE_IDS else "门槛",
        "stars": stars, "by": "机器", "rejected_at": today(),
    })

def flush_round(note: str = "", keep_rounds: int = 400, keep_rejects: int = 600) -> dict:
    """Persist this run's scan trail to scouts/scan_log.json. Returns the round."""
    by_rule: dict = {}
    for r in _ROUND["rejects"]:
        by_rule[r["reject_rule"]] = by_rule.get(r["reject_rule"], 0) + 1
    rnd = {
        "round_id": _ROUND["started_at"] or round_id(),
        "date": today(),
        "finished_at": now_iso(),
        "scanned": _ROUND["scanned"],
        "admitted": len(_ROUND["admitted"]),
        "rejected": len(_ROUND["rejects"]),
        "by_rule": by_rule,
        "source": "scout-instrumented",   # 数字来自 scout 进程本身，可追溯
        "note": note,
    }
    log = read_json(SCAN_LOG, None) or {"_说明": "机器扫描留痕。每轮进货扫了多少、收了多少、拒了哪些。网站上的统计数字来自这里。", "rounds": [], "rejects": []}
    log.setdefault("rounds", []).append(rnd)
    log["rounds"] = log["rounds"][-keep_rounds:]
    for r in _ROUND["rejects"]:
        r["round_id"] = rnd["round_id"]
    log.setdefault("rejects", []).extend(_ROUND["rejects"])
    log["rejects"] = log["rejects"][-keep_rejects:]
    write_json(SCAN_LOG, log)
    print(f"[lib] scan round: scanned {rnd['scanned']}, admitted {rnd['admitted']}, "
          f"rejected {rnd['rejected']} {by_rule or ''}")
    _ROUND.update({"scanned": 0, "admitted": [], "rejects": [], "started_at": None})
    return rnd

_LOG_DISCOVER = re.compile(r"\[scout\] discover:\s*(\d+)\s*candidates,\s*(\d+)\s*tried,\s*(\d+)\s*items added")

def record_round_from_log(text: str, note: str = "") -> dict | None:
    """Fallback trail: recover real numbers from the scout's own stdout.

    Used until skill_scout.py calls note_scanned/record_reject directly. It is
    weaker on purpose — the scout only prints post-gate candidates, so `scanned`
    stays unknown rather than being guessed. `complete: false` marks that.
    """
    m = None
    for m in _LOG_DISCOVER.finditer(text or ""):
        pass
    if not m:
        return None
    cands, tried, added = (int(m.group(i)) for i in (1, 2, 3))
    rnd = {
        "round_id": round_id(), "date": today(), "finished_at": now_iso(),
        # 未插桩的量一律 null，不猜：scout 只打印过了门槛的候选数，
        # 搜索结果总条数和逐条拒收理由都没打印，估不出来就不写数字。
        "scanned": None, "rejected": None, "by_rule": {},
        "passed_gate": cands, "tried": tried, "admitted": added,
        "source": "scout-log-parse", "complete": False, "note": note,
    }
    log = read_json(SCAN_LOG, None) or {"rounds": [], "rejects": []}
    log.setdefault("rounds", []).append(rnd)
    log["rounds"] = log["rounds"][-400:]
    write_json(SCAN_LOG, log)
    return rnd

def build_rejected_feed(items: dict) -> dict:
    """Aggregate the rejection ledger into skills/rejected-feed.json.

    Separate file, not a branch of feed.json, because: feed.json is fetched on
    every page view and the 拒收榜 is a second page; the two have different
    owners and cadences; and a rejection list grows without bound while the
    shelf deliberately does not. feed.json still carries a small
    `rejected_summary` so the front page can print the three numbers without a
    second request.

    Every number here is computed from a file in the repo. Nothing is estimated:
    a count that is not instrumented yet comes out as null, not as a guess.
    """
    doc = read_json(REJECTED, None) or {}
    seen, human = set(), []
    for e in reversed(doc.get("entries", [])):        # 后写的覆盖先写的
        if not isinstance(e, dict) or e.get("hide"):
            continue
        repo = (e.get("repo") or "").strip()
        # 去重键是 **(repo, skill)**，不是 repo。
        #
        # 原来只按 repo 去重，于是「整仓被拒」和「同仓的另一个分支被拒」互相覆盖 ——
        # 96 条写下来的拒收只有 90 条进得了榜，**6 条静默消失**，而 rejected.json 的
        # `_去重键` 一直写着 (repo, skill)。文档写的是设计，实现是另一回事。
        # check_curation 那条「N 个 repo 重复，构建时只取最后一条」的 WARN 一直在报这件事，
        # 被当成无害提示读了很久。同一个仓库一部分上架一部分被拒是正常状态，不是矛盾。
        key = (repo, (e.get("skill") or "").strip())
        if not repo or key in seen:
            continue
        seen.add(key)
        rule = e.get("reject_rule", "")
        human.append({
            "repo": repo,
            "name": e.get("name", "") or e.get("skill", "") or repo.split("/")[-1],
            "desc": (e.get("desc") or "")[:400],
            "reject_reason_zh": e.get("reject_reason_zh", ""),
            "reject_reason_en": e.get("reject_reason_en", ""),
            "reject_rule": rule if rule in REJECT_RULE_IDS else "",
            "reject_clause": e.get("reject_clause", ""),
            "stars": e.get("stars", 0),
            "url": e.get("url") or f"https://github.com/{repo}",
            "rejected_at": e.get("rejected_at", ""),
            "by": e.get("by", "店长"),
        })
    # 09-03：一条手写的拒收把 stars 写成了 ""，整条 refresh 崩掉、上架那趟白跑 —— 排序键先归一类型
    human.sort(key=lambda r: (str(r.get("rejected_at") or ""), int(r.get("stars") or 0) if str(r.get("stars") or "0").lstrip("-").isdigit() else 0), reverse=True)

    log = read_json(SCAN_LOG, None) or {}
    rounds = [r for r in log.get("rounds", []) if isinstance(r, dict)]
    _seen_repos = {k[0] for k in seen}
    machine = [r for r in log.get("rejects", []) if isinstance(r, dict) and r.get("repo") not in _seen_repos]
    machine.sort(key=lambda r: r.get("rejected_at", ""), reverse=True)

    def _sum(key):
        vals = [r.get(key) for r in rounds if isinstance(r.get(key), int)]
        return sum(vals) if vals else None

    counts = {rid: 0 for rid in REJECT_RULE_IDS}
    for r in human + machine:
        if r.get("reject_rule") in counts:
            counts[r["reject_rule"]] += 1

    visible = [it for it in items.values() if not it.get("hide")]
    hidden = [it for it in items.values() if it.get("hide")]
    latest = rounds[-1] if rounds else None

    out = {
        "generated_at": now_iso(),
        "sources": {
            "human": "editorial/rejected.json",
            "machine": "scouts/scan_log.json",
            "standard": "docs/CURATION.md",
        },
        "stats": {
            "shelved": len(visible),
            "unshelved": len(hidden),          # 抓来了、没上架/已下架，记录仍在 skills/*.json
            "known_items": len(items),
            "known_repos": len({it.get("repo") for it in items.values() if it.get("repo")}),
            "rejected_documented": len(human),
            "rejected_machine_logged": len(machine),
            "rounds_logged": len(rounds),
            "latest_round": latest,
            "all_rounds": {"scanned": _sum("scanned"),
                           "admitted": _sum("admitted"),
                           "rejected": _sum("rejected")},
        },
        "rules": [{"rule": rid, "zh": zh, "en": en, "detail": detail, "count": counts[rid]}
                  for rid, zh, en, detail in REJECT_RULES],
        "rejected": human,
        "machine_rejects": machine,
        "unshelved_trail": sorted(
            [{"id": it.get("id"), "repo": it.get("repo"), "name": it.get("name"),
              "added_at": it.get("added_at", ""), "stars": it.get("stars", 0)}
             for it in hidden],
            key=lambda r: r.get("added_at", ""), reverse=True),
    }
    write_json(REJECTED_FEED, out)
    print(f"[lib] rejected-feed: {len(human)} written up, {len(machine)} machine-logged, "
          f"{len(hidden)} unshelved, {len(rounds)} rounds")
    return out

def refresh() -> dict:
    """Rebuild skills/feed.json (+ skills/rejected-feed.json) from the merged set."""
    items = apply_editorial(load_items())
    # normalize AFTER editorial so a human-written limit_zh can never be blanked
    for it in items.values():
        normalize_item(it)
    # 备料徽章：派生字段，构建时算，不落 skills/*.json。
    # 放在 editorial 之后 —— 徽章是事实（正文里有没有那些东西），不是文案，
    # 店长不该也不需要手写它；存档补齐后重建一次就自动更新，没有第二份真相。
    prep_ev = prep.load_all()
    prep.annotate(items, prep_ev)
    # 「店长推荐」（英文 Editor's picks）—— 首页第一眼的 12 张卡，就是这家店的脸。
    # 店主 09-03：「店长推荐你自己想一下推荐标准，我觉得至少要有图」。标准定这样（docs/CURATION.md 同步）：
    #   硬条件 ① 有作者真图，且文件真在仓里     ② 编辑读过原文挑的（editorial/editor_picks.json，理由 ≥30 字）
    #          ③ 四段文案齐全，标题不是套路开头、不是半句话   ④ 同一仓最多 1 件
    #   钉住   8/28 店主定的 12 件（editorial/picks_pinned.json）原样保留，新的只增不删
    #   排序   登记时间新的在前 → 同日先摆过了红线扫描存档的 → 再按上架时间、id 稳定
    # 09-03 同事查出：pick 标记只在 8/28 那轮门禁时打过一次，之后没有任何流程更新它，首页那组十二天没换。现在每次 refresh 重算。
    _eds = (read_json(os.path.join(ROOT, "editorial", "editor_picks.json"), {}) or {}).get("items", {})
    _scan = read_json(os.path.join(ROOT, "scouts", "scan_archive.json"), {}) or {}
    _scan = _scan.get("entries") if isinstance(_scan.get("entries"), dict) else {}   # scan_archive.json 的形状是 {"entries": {sid: …}}
    _ban = re.compile(r"^(只认|只剪|拒绝|把|一句话|一张|用)")
    _half = re.compile(r"[被的是把在和与或了到会就将向给让对从]。$")
    _REAL = ("hero", "artwork", "ours", "diagram")

    def _pick_entry(it):
        e = _eds.get((it.get("repo") or "").lower())
        if not e or len((e.get("reason") or "").strip()) < 30:
            return None
        want = [q.strip("/") for q in ([e.get("path")] if e.get("path") else []) + list(e.get("paths") or [])]
        if want and (it.get("path") or "").strip("/") not in want:
            return None
        return e

    def _has_real_cover(it):
        u = it.get("cover") or ""
        if it.get("cover_kind") not in _REAL or not u:
            return False
        if u.startswith("/skill/"):
            return os.path.exists(os.path.join(ROOT, u[len("/skill/"):]))
        return u.startswith("http")

    def _copy_ok(it):
        if any(len((it.get(k) or "").strip()) < 8 for k in ("title_zh", "tagline_zh", "why_zh", "limit_zh")):
            return False
        t = (it.get("title_zh") or "").strip()
        return not _ban.match(t) and not _half.search(t) and not any(_half.search((it.get(k) or "").strip()) for k in ("tagline_zh", "why_zh"))

    _cands = []
    for it in items.values():
        if it.get("hide"):
            continue
        e = _pick_entry(it)
        if not e or not _has_real_cover(it) or not _copy_ok(it):
            continue
        _cands.append(((e.get("picked_at") or "", 1 if it.get("id") in _scan else 0, it.get("added_at") or "", it.get("id") or ""), it))
    _cands.sort(key=lambda kv: kv[0], reverse=True)
    # 店主 09-03：「12 件不要删，只是新增」。8/28 那 12 件钉在 editorial/picks_pinned.json，不看图不看文案，原样保留；
    # 编辑挑的满足上面四条就追加，不限总数、同一仓只上一件；不再用心选补位。
    _pinned = set((read_json(os.path.join(ROOT, "editorial", "picks_pinned.json"), {}) or {}).get("ids", []))
    _top = {i for i in _pinned if i in items and not items[i].get("hide")}
    _per_repo = {(items[i].get("repo") or "").lower() for i in _top}
    for _, it in _cands:
        repo = (it.get("repo") or "").lower()
        if repo in _per_repo:
            continue
        _top.add(it["id"]); _per_repo.add(repo)
    for it in items.values():
        it["pick"] = it.get("id") in _top
    print(f"[lib] 店长推荐 {len(_top)} 件 = 钉住 {len(_top & _pinned)} + 编辑追加 {len(_top - _pinned)}（候选 {len(_cands)}）")
    visible = [it for it in items.values() if not it.get("hide")]
    # newest first (店里天天上新，新货朝前); same-day ties break by fun, then stars.
    # 完全并列的再按 id —— 否则并列项的先后取决于 glob() 的文件系统顺序，同一份数据
    # 在不同机器上会重排出不同的 feed.json，白白制造 diff 和 push 冲突。
    visible.sort(key=lambda x: x.get("id", ""))
    # 同一天之内，**有真产出物图的排前面**。
    #
    # 为什么要加这一档：「新货朝前」是对的，但它有个副作用 ——
    # 越是刚上架的越还没配上封面，于是前两屏几乎全是纯文字卡（实测：前 60 张卡里只有 3 张图）。
    # 一屏文字墙没人愿意往下滚，而这正是店主说的「你新加的并不吸引人」的机制。
    # 排序仍然是天为单位、新的在前，只是**同一天内先摆看得见东西的那些**。
    #
    # 同时**把 stars 从排序键里去掉**：我们反复认定 star 不是质量信号
    # （在架好货大量 0–50 星），D65 还实测出它在新源那批里是**反向**的
    # —— 榜首是 flutter/bun/AutoGPT 这些只是带了个 skills 目录的产品仓库。
    # 既然不是质量信号，它就不该决定读者先看到谁。去掉它不影响确定性：
    # 上面那行按 id 的排序已经兜住了并列项的稳定顺序。
    visible.sort(key=lambda x: (x.get("added_at", ""),
                               1 if x.get("cover_real") else 0,
                               x.get("fun_score", 0)), reverse=True)
    # **同一个仓库的卡片不许连着出现。**
    #
    # 店主刷货架时的原话：「里面还有很多重复的内容卡片」。查出来不是同一件重复渲染
    # （id 无重复），是**一个仓库占了一串卡**：`worldwonderer/oh-story-claudecode`
    # 一家占 6 张，六张全是网文写作、标题还都是「把…」「拆…」开头；
    # 另有 8 个仓库各占 2–3 张，合计 9 个仓库 23 张卡。连着刷过去，读起来就是重复。
    #
    # 这里只改**先后**，不下架任何一件 —— 一个仓库出六件该不该留是选品判断
    # （CURATION 问二「数量堆」），那是人读完仓库才判得了的事，不是排序能解决的。
    # 做法：按仓库分桶后轮转发牌，同仓两张之间至少隔开其余仓库各一张。
    # 排序前面那几档（收录日倒序 → 真产出物优先 → fun_score）在桶内保持不变。
    by_repo: dict[str, list] = {}
    for it in visible:
        by_repo.setdefault(it.get("repo", ""), []).append(it)
    if any(len(v) > 1 for v in by_repo.values()):
        # 做法是**按步长摊到整条流**，不是轮转发牌。
        # 轮转试过，尾部又聚回去了（末尾只剩多件仓库在互相轮，那个占 6 张的
        # 仍然连着占了 222–225）。按步长则是：一个仓库出 k 件，就把这 k 件
        # 均匀钉在 0、n/k、2n/k … 上，无论 k 多大都摊得开。
        pos = {id(it): i for i, it in enumerate(visible)}
        n = len(visible)
        keyed = []
        for g in by_repo.values():
            g.sort(key=lambda it: pos[id(it)])
            start, k = pos[id(g[0])], len(g)
            for j, it in enumerate(g):
                # 第一件留在原位（第一屏还是那批新货），其余按步长往后钉
                keyed.append((start + (0 if j == 0 else j * n / k), pos[id(it)], it))
        keyed.sort(key=lambda x: (x[0], x[1]))
        visible = [x[2] for x in keyed]

    t = today()
    headline, headline_history = build_headline(items)
    rejected = build_rejected_feed(items)
    rstats = rejected["stats"]
    feed = {
        "generated_at": now_iso(),
        "count": len(visible),
        "new_today": sum(1 for it in visible if it.get("added_at") == t),
        "picks": sum(1 for it in visible if it.get("pick")),
        "with_limit": sum(1 for it in visible if (it.get("limit_zh") or "").strip()),
        # 备料徽章的聚合数。逐件的证据条数**刻意**不进商品 —— 见 prep_signals 模块头。
        # no_archive 是我们自己的 path 欠账指标，盯着它变小，不是拿来显示的。
        "prep_stats": prep.prep_stats(items, prep_ev),
        "headline": headline,
        "headline_history": headline_history,
        "rejected_summary": {
            "feed": "rejected-feed.json",
            "shelved": rstats["shelved"],
            "unshelved": rstats["unshelved"],
            "rejected_documented": rstats["rejected_documented"],
            "latest_round": rstats["latest_round"],
        },
        "categories": [{"id": c, "zh": z, "en": e, "emoji": m,
                        "count": sum(1 for it in visible if it.get("category") == c)}
                       for c, z, e, m in CATEGORIES],
        "skills": visible,
    }
    os.makedirs(SKILLS_DIR, exist_ok=True)
    with open(FEED, "w", encoding="utf-8") as f:
        json.dump(feed, f, ensure_ascii=False, indent=1)
    ps = feed["prep_stats"]
    print(f"[lib] feed: {len(visible)} items ({feed['new_today']} new today, {feed['picks']} picks, "
          f"{feed['with_limit']} with 局限, headline={'yes' if headline else 'none'})")
    print(f"[lib] 备料齐 {ps['ready']} 件 / 有存档 {ps['archived']} / 无存档 {ps['no_archive']}")
    try:
        import write_shelf_pages
        write_shelf_pages.main()
    except Exception as e:
        print(f"[lib] shelf pages skip: {e}")
    return feed

def load_sources() -> dict:
    try:
        with open(SOURCES, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"repos": {}}

def save_sources(src: dict) -> None:
    with open(SOURCES, "w", encoding="utf-8") as f:
        json.dump(src, f, ensure_ascii=False, indent=1)

if __name__ == "__main__":
    import sys
    # `--from-log FILE` 把 scout 自己的 stdout 解析成一轮扫描留痕，然后照常重建。
    if "--from-log" in sys.argv:
        p = sys.argv[sys.argv.index("--from-log") + 1]
        try:
            with open(p, encoding="utf-8", errors="replace") as f:
                r = record_round_from_log(f.read(), note=os.path.basename(p))
            print(f"[lib] scan round from log: {r}" if r else "[lib] no discover line in log; no round recorded")
        except Exception as e:
            print(f"[lib] log parse skipped: {e}")
    refresh()
