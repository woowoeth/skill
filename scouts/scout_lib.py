#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill 商店 — shared scout library.

The repo is the database:
  skills/<id>.json   one file per shelf item (a skill or a collection)
  skills/feed.json   aggregated feed the static site reads

Design mirrors ourword-ai/idea: scouts are fault-tolerant, every helper
swallows single-item failures, and feed.json is always regenerated from
the merged set of skills/*.json (conflict-safe).
"""
from __future__ import annotations
import os, re, json, time, glob, hashlib, urllib.request, urllib.error, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT, "skills")
FEED = os.path.join(SKILLS_DIR, "feed.json")
EDITORIAL = os.path.join(ROOT, "editorial", "curation.json")
SOURCES = os.path.join(ROOT, "scouts", "sources.json")

GH_TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
UA = "skill-store-scout/1.0 (+https://github.com/woowoeth/skill-store)"

# ---------------------------------------------------------------- shelves ---
CATEGORIES = [
    ("creative", "创意画室", "Creative Studio", "🎨"),
    ("fun",      "玩乐杂货", "Fun & Games",     "🎮"),
    ("writing",  "文房小铺", "Writing Desk",    "✍️"),
    ("life",     "生活日用", "Daily Life",      "🧺"),
    ("docs",     "文档柜台", "Documents",       "📄"),
    ("work",     "打工必备", "Work & Growth",   "💼"),
    ("dev",      "开发五金", "Dev Hardware",    "🔧"),
    ("meta",     "元技能",   "Meta Skills",     "🧬"),
]
CAT_IDS = [c[0] for c in CATEGORIES]

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
    "life":     ["cook", "recipe", "travel", "trip", "fitness", "health", "meal", "diet",
                 "journal", "diary", "habit", "budget", "shopping", "gift", "wedding",
                 "resume", "cv", "interview prep", "生活", "菜谱", "旅行", "简历", "健康"],
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
        for k in kws:
            if has_kw(blob, [k]):
                scores[cat] += 2 if has_kw(f"{name} {desc[:80]}", [k]) else 1
    best = max(scores, key=lambda c: (scores[c], -CAT_IDS.index(c)))
    return best if scores[best] > 0 else "dev"

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
    dirname = (path.rstrip("/").split("/")[-1] if path else repo.split("/")[-1]) or slug(name)
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
        "repo": repo, "owner": owner, "path": path, "url": url, "homepage": homepage,
        "stars": stars, "pushed_at": pushed_at, "skill_count": skill_count,
        "category": cat, "fun_score": fs, "pick": False, "hide": False,
        "source": source, "added_at": added_at or today(), "install": install,
    }

# --------------------------------------------------------------- storage ---
def load_items() -> dict:
    items = {}
    for p in glob.glob(os.path.join(SKILLS_DIR, "*.json")):
        if os.path.basename(p) == "feed.json":
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
    if not os.path.exists(EDITORIAL):
        return items
    try:
        with open(EDITORIAL, encoding="utf-8") as f:
            cur = json.load(f)
    except Exception as e:
        print(f"[lib] editorial unreadable: {e}")
        return items
    for sid, patch in cur.get("items", {}).items():
        if sid in items:
            items[sid].update({k: v for k, v in patch.items() if k != "id"})
    return items

def refresh() -> dict:
    """Rebuild skills/feed.json from the merged item set."""
    items = apply_editorial(load_items())
    visible = [it for it in items.values() if not it.get("hide")]
    # newest first (店里天天上新，新货朝前); same-day ties break by fun, then stars
    visible.sort(key=lambda x: (x.get("added_at", ""), x.get("fun_score", 0), x.get("stars", 0)), reverse=True)
    t = today()
    feed = {
        "generated_at": now_iso(),
        "count": len(visible),
        "new_today": sum(1 for it in visible if it.get("added_at") == t),
        "picks": sum(1 for it in visible if it.get("pick")),
        "categories": [{"id": c, "zh": z, "en": e, "emoji": m,
                        "count": sum(1 for it in visible if it.get("category") == c)}
                       for c, z, e, m in CATEGORIES],
        "skills": visible,
    }
    os.makedirs(SKILLS_DIR, exist_ok=True)
    with open(FEED, "w", encoding="utf-8") as f:
        json.dump(feed, f, ensure_ascii=False, indent=1)
    print(f"[lib] feed: {len(visible)} items ({feed['new_today']} new today, {feed['picks']} picks)")
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
    refresh()
