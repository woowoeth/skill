#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scouts/enrich.py — 描述补全 / 封面补全 / 宽漏斗扫描

本文件独立于 skill_scout.py 与 scout_lib.py（那两个文件另有人负责，不改）。
只用 Python 3 标准库。

三个子命令
----------
  describe   给 skills/*.json 里描述缺失的商品补描述  → editorial/descriptions.json
  covers     给缺封面 / 封面已失效的商品找真图        → editorial/covers.json
  funnel     按垂直领域跑宽漏斗，捞原始候选           → editorial/funnel_raw.json

配额现实（本文件的核心设计约束）
--------------------------------
GitHub REST API 未认证 = **60 次/小时**，而货架上有 700+ 件。
所以本文件把数据源按「花不花配额」分成两档，先榨干免费档，剩下的才动配额：

  免费档（无限，实测 60 并发请求 3.6 秒，无 429）
    - raw.githubusercontent.com/{repo}/HEAD/README.md   README 全文
    - raw.githubusercontent.com/{repo}/HEAD/{path}/SKILL.md  frontmatter
    - github.com/{owner}/{repo} 的 HTML <meta>          描述 + 社交预览图 + 带哈希的 OG 图
      （og:image:alt / twitter:title 里就是仓库 description，等价于 API 的 description 字段；
        og:image 要么是 repository-images.githubusercontent.com 的自定义社交预览图，
        要么是 opengraph.githubassets.com 的官方 OG 图 —— 一次请求同时解决任务 A 和任务 B）

  配额档（60/小时，GH_TOKEN 存在时 5000/小时）
    - GET /repos/{owner}/{repo}          description / topics / homepage / stars / pushed_at
    - GET /repos/{owner}/{repo}/readme   README（免费档拿不到时兜底，比如非 README.md 命名）
    - GET /repos/{owner}/{repo}/contents/{dir}  列 assets/ 目录找图

断点续跑：所有网络结果落 scouts/.cache/ ，重跑只打没缓存的。
限流：命中 403/429 或预算见底时**优雅退出**，打印还剩多少没跑完，已有成果照常落盘。

token：只从环境变量 GH_TOKEN / GITHUB_TOKEN 读，代码里不硬编码。
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import glob
import gzip
import hashlib
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT, "skills")
EDITORIAL = os.path.join(ROOT, "editorial")
CACHE_DIR = os.path.join(ROOT, "scouts", ".cache")

GH_TOKEN = (os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or "").strip()

UA_API = "skill-store-enrich/1.0 (+https://github.com/woowoeth/skill)"
UA_WEB = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

TODAY = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


# ------------------------------------------------------------------ 基础设施 ---
class RateLimited(Exception):
    """GitHub 配额耗尽 / 被限流。抛出后调用方应当收工落盘并报告剩余量。"""


def _log(msg: str) -> None:
    print(msg, flush=True)


def _fetch(url: str, headers: dict, timeout: int = 25, method: str = "GET",
           net_retries: int = 2) -> tuple[int, bytes, dict]:
    """一次请求。返回 (status, body, headers)。

    HTTP 错误码原样返回（调用方要靠 403/429/404 分流）；
    只有网络层抖动（DNS 抽风、连接重置、超时）才重试 —— 并发跑几千个请求时
    这类偶发错误必然出现，不重试会平白丢货。
    """
    req = urllib.request.Request(url, headers=headers, method=method)
    for i in range(net_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    try:
                        body = gzip.decompress(body)
                    except Exception:
                        pass
                return r.status, body, dict(r.headers)
        except urllib.error.HTTPError as e:
            try:
                body = e.read()
            except Exception:
                body = b""
            return e.code, body, dict(e.headers or {})
        except Exception:
            if i >= net_retries:
                raise
            time.sleep(0.6 * (i + 1))
    return 0, b"", {}


class Cache:
    """一个 json 文件一个命名空间。put 到阈值自动落盘，中断也不丢太多。"""

    def __init__(self, name: str, flush_every: int = 40):
        os.makedirs(CACHE_DIR, exist_ok=True)
        self.path = os.path.join(CACHE_DIR, f"{name}.json")
        self.flush_every = flush_every
        self._lock = threading.Lock()
        self._dirty = 0
        try:
            with open(self.path, encoding="utf-8") as f:
                self.data = json.load(f)
        except Exception:
            self.data = {}

    def get(self, key: str, default=None):
        with self._lock:
            return self.data.get(key, default)

    def has(self, key: str) -> bool:
        with self._lock:
            return key in self.data

    def put(self, key: str, val) -> None:
        with self._lock:
            self.data[key] = val
            self._dirty += 1
            need = self._dirty >= self.flush_every
        if need:
            self.flush()

    def flush(self) -> None:
        with self._lock:
            self._dirty = 0
            snap = dict(self.data)
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(snap, f, ensure_ascii=False, indent=1, sort_keys=True)
        os.replace(tmp, self.path)


class Budget:
    """GitHub API 配额账本。开跑前问一次 /rate_limit，之后本地记账。

    reserve：留几次不用，免得把配额打到 0 影响别的脚本。
    """

    def __init__(self, reserve: int = 2):
        self.reserve = reserve
        self.remaining = None      # None = 还没探测
        self.reset_at = 0
        self.spent = 0
        self.blocked = False
        self._lock = threading.Lock()

    def probe(self) -> None:
        h = {"User-Agent": UA_API, "Accept": "application/vnd.github+json"}
        if GH_TOKEN:
            h["Authorization"] = f"Bearer {GH_TOKEN}"
        try:
            st, body, _ = _fetch("https://api.github.com/rate_limit", h, timeout=15)
            core = json.loads(body).get("resources", {}).get("core", {})
            self.remaining = int(core.get("remaining", 0))
            self.reset_at = int(core.get("reset", 0))
            _log(f"[budget] GitHub API 剩余 {self.remaining}/{core.get('limit')} 次"
                 f"（{'已认证' if GH_TOKEN else '未认证'}），"
                 f"重置于 {datetime.datetime.fromtimestamp(self.reset_at).strftime('%H:%M:%S')}")
        except Exception as e:
            self.remaining = 0
            _log(f"[budget] 探测失败，按 0 处理: {e}")

    def take(self) -> None:
        with self._lock:
            if self.blocked:
                raise RateLimited("已被限流")
            if self.remaining is None:
                self.remaining = 0
            if self.remaining <= self.reserve:
                self.blocked = True
                raise RateLimited(f"配额见底（剩 {self.remaining}，保留 {self.reserve}）")
            self.remaining -= 1
            self.spent += 1

    def mark_blocked(self, why: str) -> None:
        with self._lock:
            self.blocked = True
            self.remaining = 0
        _log(f"[budget] 被限流：{why}")

    def note_headers(self, hdrs: dict) -> None:
        v = hdrs.get("X-RateLimit-Remaining")
        if v is not None:
            try:
                with self._lock:
                    self.remaining = int(v)
            except Exception:
                pass


BUDGET = Budget()


# ------------------------------------------------------------------- 数据源 ---
_raw_cache = Cache("raw_files")
_html_cache = Cache("gh_html")
_api_cache = Cache("gh_api")
_probe_cache = Cache("url_probe", flush_every=120)


def raw_file(repo: str, path: str) -> str | None:
    """raw.githubusercontent.com 取文本。不花配额。None = 404 或失败。"""
    key = f"{repo}|{path}"
    if _raw_cache.has(key):
        return _raw_cache.get(key)
    url = f"https://raw.githubusercontent.com/{repo}/HEAD/{urllib.parse.quote(path)}"
    val = None
    for attempt in range(2):
        st, body, _ = _fetch(url, {"User-Agent": UA_WEB}, timeout=20)
        if st == 200:
            val = body.decode("utf-8", "replace")
            break
        if st == 404:
            break
        time.sleep(1 + attempt)
    _raw_cache.put(key, val)
    return val


README_NAMES = ["README.md", "readme.md", "README.MD", "Readme.md",
                "README.zh-CN.md", "README_CN.md", "README.rst", "README.txt",
                ".github/README.md", "docs/README.md"]


def readme_of(repo: str) -> str | None:
    for n in README_NAMES:
        t = raw_file(repo, n)
        if t:
            return t
    return None


_META_RE = re.compile(
    r'<meta\s+(?:name|property)="(og:image|og:image:alt|twitter:title|twitter:description|description)"'
    r'\s+content="(.*?)"\s*/?>', re.S)


def gh_html_meta(repo: str) -> dict:
    """抓 github.com/{repo} 的 HTML <meta>。不花 API 配额。

    一次请求同时拿到：
      - description（og:image:alt / twitter:title，就是仓库简介）
      - og:image（自定义社交预览图 或 官方 OG 图的带哈希地址）

    注意：`opengraph.githubassets.com/1/{owner}/{repo}` 这种猜的路径在本机实测常年 429，
    而 HTML 里给出的带哈希地址实测 200 + image/png，所以必须走 HTML 拿真地址。
    """
    if _html_cache.has(repo):
        return _html_cache.get(repo) or {}
    out: dict = {}
    st, body, _ = _fetch(f"https://github.com/{repo}",
                         {"User-Agent": UA_WEB, "Accept": "text/html", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"},
                         timeout=25)
    if st == 200:
        html = body.decode("utf-8", "replace")
        meta = {}
        for k, v in _META_RE.findall(html):
            meta.setdefault(k, _unescape(v.strip()))
        out["ok"] = True
        out["og_image"] = meta.get("og:image", "")
        # 描述：GitHub 把它拼成 "<desc> - owner/repo" 或 "Contribute to owner/repo ..."
        desc = meta.get("og:image:alt") or meta.get("twitter:description") or meta.get("description") or ""
        out["description"] = _clean_gh_desc(desc, repo)
        title = meta.get("twitter:title", "")
        if title.startswith("GitHub - ") and ":" in title:
            full = title.split(":", 1)[1].strip()
            if len(full) > len(out["description"]):
                out["description"] = full
        m = re.search(r'<span[^>]*id="repo-stars-counter-star"[^>]*title="([\d,]+)"', html)
        if m:
            out["stars"] = int(m.group(1).replace(",", ""))
        m = re.search(r'<relative-time[^>]*datetime="([^"]+)"', html)
        if m:
            out["pushed_at"] = m.group(1)
        m = re.search(r'"repositoryTopics"[^]]*?\]', html)
        out["topics"] = re.findall(r'/topics/([a-z0-9-]+)"', html)[:12]
    elif st in (403, 429):
        out = {"ok": False, "status": st}
    else:
        out = {"ok": False, "status": st}
    _html_cache.put(repo, out)
    return out


def _unescape(s: str) -> str:
    import html as _h
    return _h.unescape(s)


_GH_BOILER = re.compile(
    r"\s*(Contribute to [^.]+ development by creating an account on GitHub\.?"
    r"|GitHub is where [^.]+ builds software\.?"
    r"|Create an account on GitHub[^.]*\.?)\s*", re.I)


def _clean_gh_desc(s: str, repo: str) -> str:
    """GitHub 的 meta 里塞了两截垃圾，都要剥掉：

      前后缀 "- owner/repo"（它把仓库名拼进 og:image:alt）
      样板句 "Contribute to owner/repo development by creating an account on GitHub."
             —— 仓库没写 description 时它整句就是这个；写了的话它会**接在真描述后面**，
             所以不能只判断开头，必须整句删。
    """
    s = (s or "").strip()
    if not s:
        return ""
    s = _GH_BOILER.sub(" ", s)
    s = re.sub(r"\s*-\s*" + re.escape(repo) + r"\s*$", "", s)
    s = re.sub(r"\s*-\s*" + re.escape(repo.split("/")[0]) + r"/[\w.\-]*\.\.\.\s*$", "", s)
    s = re.sub(r"\s*\.\.\.$", "", s)
    return re.sub(r"\s+", " ", s).strip(" .·—-")


def gh_api(path: str) -> dict | list | None:
    """GitHub REST。**花配额**。403/429 立刻把预算标死并抛 RateLimited。"""
    if _api_cache.has(path):
        return _api_cache.get(path)
    BUDGET.take()
    h = {"User-Agent": UA_API, "Accept": "application/vnd.github+json"}
    if GH_TOKEN:
        h["Authorization"] = f"Bearer {GH_TOKEN}"
    st, body, hdrs = _fetch("https://api.github.com" + path, h, timeout=25)
    BUDGET.note_headers(hdrs)
    if st in (403, 429):
        BUDGET.mark_blocked(f"{st} on {path}")
        raise RateLimited(f"{st} on {path}")
    if st == 404:
        _api_cache.put(path, None)
        return None
    if st != 200:
        return None
    try:
        val = json.loads(body)
    except Exception:
        return None
    _api_cache.put(path, val)
    return val


def gh_api_repo(repo: str) -> dict | None:
    """任务 A 第 1 层兜底：GET /repos/{owner}/{repo}"""
    d = gh_api(f"/repos/{repo}")
    if not isinstance(d, dict):
        return None
    return {
        "description": d.get("description") or "",
        "topics": d.get("topics") or [],
        "homepage": d.get("homepage") or "",
        "stars": d.get("stargazers_count", 0),
        "pushed_at": d.get("pushed_at") or "",
        "og_image": d.get("open_graph_image_url") or "",
        "default_branch": d.get("default_branch") or "HEAD",
        "archived": bool(d.get("archived")),
        "fork": bool(d.get("fork")),
    }


def gh_api_readme(repo: str) -> str | None:
    """任务 A 第 2 层兜底的 API 版本：GET /repos/{owner}/{repo}/readme
    （只在 raw 那套命名全落空时才动用，因为它花配额）"""
    import base64
    d = gh_api(f"/repos/{repo}/readme")
    if not isinstance(d, dict) or not d.get("content"):
        return None
    try:
        return base64.b64decode(d["content"]).decode("utf-8", "replace")
    except Exception:
        return None


# ------------------------------------------------------------- Markdown 解析 ---
_FM = re.compile(r"^﻿?\s*---\s*\n(.*?)\n---\s*\n?", re.S)


def skillmd_frontmatter(text: str) -> dict:
    """不引 YAML 依赖，只取 name / description（含折叠行）。"""
    m = _FM.match(text or "")
    if not m:
        return {}
    out, key, buf = {}, None, []
    for line in m.group(1).split("\n"):
        km = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if km:
            if key:
                out[key] = " ".join(x.strip() for x in buf).strip()
            key, buf = km.group(1).lower(), [km.group(2)]
        elif key and line.startswith((" ", "\t")):
            buf.append(line)
        elif line.strip() == "":
            continue
    if key:
        out[key] = " ".join(x.strip() for x in buf).strip()
    for k in ("name", "description"):
        if k in out:
            out[k] = out[k].strip().strip("'\"").strip()
    return out


_BADGE_HOSTS = (
    "img.shields.io", "shields.io", "badge.fury.io", "travis-ci", "circleci.com",
    "codecov.io", "coveralls.io", "app.netlify.com", "vercel.com/button",
    "badgen.net", "forthebadge.com", "img.badgesize.io", "isitmaintained.com",
    "api.star-history.com", "star-history.com", "contrib.rocks",
    "buymeacoffee.com", "ko-fi.com", "opencollective.com", "patreon.com",
    "hitscounter", "visitor-badge", "profile-counter", "komarev.com",
    "deepwiki.com", "mseep.net", "img.buymeacoffee.com", "gitpod.io",
    "codespaces", "colab.research.google.com/assets", "cursor.com/deeplink",
    "camo.githubusercontent.com",  # 代理地址不稳定，宁可不要
)
_BADGE_PATH_HINT = re.compile(
    r"(badge|shield|logo\.(svg|png)$|icon\.(svg|png)$|star-history|sponsor|donate|"
    r"qrcode|qr-code|wechat-?(group|qr)|weixin|discord\.svg|twitter\.svg|license|"
    r"devicon|/icons?/|/logos?/|favicon|avatar)",
    re.I)

_MD_IMG = re.compile(r"!\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+[\"'][^\"']*[\"'])?\s*\)")
_HTML_IMG = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']", re.I)
_IMG_EXT = re.compile(r"\.(png|jpe?g|webp|gif|svg|avif)(\?|#|$)", re.I)


def readme_images(md: str, repo: str) -> list[str]:
    """按出现顺序抽 README 里的图，滤掉徽章，相对路径转 raw 绝对地址。

    这一层最有价值：很多 skill 的 README 头图放的就是**产出物示例**
    （海报、像素图、图表），那才是「品味」的证据，不是又一张灰色 OG 卡片。
    """
    if not md:
        return []
    urls: list[str] = []
    for m in re.finditer(r"!\[[^\]]*\]\([^)]*\)|<img[^>]+>", md):
        chunk = m.group(0)
        got = _MD_IMG.findall(chunk) or _HTML_IMG.findall(chunk)
        for u in got:
            u = u.strip()
            if u and u not in urls:
                urls.append(u)
    out = []
    for u in urls:
        a = _abs_image_url(u, repo)
        if a and a not in out:
            out.append(a)
    return prefer_output_images(out)


# 「原片 → 成品」对照目录在创意类 skill 里非常常见（examples/ 下同时放
# 04b-two-kids-original.jpg 和 04b-two-kids-poster.jpg）。按文件名顺序取第一张，
# 取到的就是**输入的原照片**，不是产出物 —— photo-distill 就这么错上了今日头条。
# 封面的全部意义是「产出物即证据」，放一张用户自己拍的原片，等于什么都没证明。
_INPUT_MARK = re.compile(r"[-_.](original|input|before|source|src|raw|orig)(?=[-_.]|$)", re.I)
_OUTPUT_MARK = re.compile(r"[-_.](poster|after|output|out|result|final|done|rendered|preview)(?=[-_.]|$)", re.I)


def prefer_output_images(urls: list[str]) -> list[str]:
    """把「输入」那张往后排，「产出物」那张往前排。**只重排，不丢弃** ——
    丢弃会让一个只有原片、没有成品的仓库连候选都没有；重排则永远不会更差。

    两条规则，弱的那条也保留是因为很多仓库只给单边命名：
      1. 同目录同前缀存在 xxx-original / xxx-poster 这种配对 → 原片降到最后
      2. 没有配对时，文件名带 output/poster/result 的整体优先于带 original/input 的
    """
    if len(urls) < 2:
        return urls

    def parts(u: str) -> tuple[str, str]:
        path = u.split("?")[0]
        d, _, f = path.rpartition("/")
        return d, f.rsplit(".", 1)[0]

    # 规则 1：找出「有成品配对」的原片
    outs: dict[tuple[str, str], str] = {}
    for u in urls:
        d, stem = parts(u)
        m = _OUTPUT_MARK.search(stem)
        if m:
            outs[(d, stem[:m.start()])] = u
    paired_inputs = set()
    for u in urls:
        d, stem = parts(u)
        m = _INPUT_MARK.search(stem)
        if m and (d, stem[:m.start()]) in outs:
            paired_inputs.add(u)

    def rank(u: str) -> int:
        if u in paired_inputs:
            return 3                       # 有成品在，原片压到最后
        _, stem = parts(u)
        if _OUTPUT_MARK.search(stem):
            return 0
        if _INPUT_MARK.search(stem):
            return 2
        return 1

    return sorted(urls, key=lambda u: (rank(u), urls.index(u)))


def _abs_image_url(u: str, repo: str) -> str | None:
    u = u.strip().strip("'\"")
    if not u or u.startswith(("data:", "#", "mailto:")):
        return None
    low = u.lower()
    if any(h in low for h in _BADGE_HOSTS):
        return None
    if _BADGE_PATH_HINT.search(low):
        return None
    if u.startswith("//"):
        u = "https:" + u
    if u.startswith("http://") or u.startswith("https://"):
        # github blob 链接转 raw
        m = re.match(r"https?://github\.com/([^/]+/[^/]+)/(?:blob|raw)/([^/]+)/(.+)$", u)
        if m:
            return f"https://raw.githubusercontent.com/{m.group(1)}/{m.group(2)}/{m.group(3)}"
        if "private-user-images.githubusercontent.com" in low:
            return None          # 带 JWT，几分钟就过期，实测线上已 404
        if not _IMG_EXT.search(u) and "githubusercontent" not in low and "githubassets" not in low:
            return None
        return u
    # 相对路径
    p = u.lstrip("./").lstrip("/")
    if not _IMG_EXT.search(p):
        return None
    return f"https://raw.githubusercontent.com/{repo}/HEAD/" + urllib.parse.quote(p)


_MD_STRIP = [
    (re.compile(r"```.*?```", re.S), " "),
    (re.compile(r"~~~.*?~~~", re.S), " "),
    (re.compile(r"<!--.*?-->", re.S), " "),
    (re.compile(r"!\[[^\]]*\]\([^)]*\)"), " "),
    (re.compile(r"<img[^>]*>", re.I), " "),
    (re.compile(r"<br\s*/?>", re.I), " "),
    (re.compile(r"</?(div|p|center|table|tr|td|th|h[1-6]|a|b|strong|em|i|span|sub|sup|picture|source|details|summary|font)[^>]*>", re.I), " "),
    (re.compile(r"\[([^\]]*)\]\([^)]*\)"), r"\1"),
    (re.compile(r"[*_`>#]+"), " "),
]

_NOISE_LINE = re.compile(
    r"^\s*(\||[-=]{3,}|<|\[!|license|mit\b|apache\b|star history|table of contents|目录|"
    r"english|中文|日本語|한국어|installation|install\b|快速开始|quick start)", re.I)


_LANG_WORDS = ("english", "简体中文", "繁體中文", "繁体中文", "中文", "日本語", "한국어",
               "español", "français", "deutsch", "português", "русский")


def _looks_like_nav(s: str) -> bool:
    """导航条 / 语言切换条不是介绍。

    README 顶部常见：「[English] | [ 中文 ] | [ 日本語 ]」「📖 官方文档 | 🚀 快速开始 | 💬 QQ 群」。
    剥掉 markdown 语法后它们看着就是一段够长的文本，会被当成首段捡走 ——
    而且带中文，还会顶掉真正的英文描述。所以必须单独认出来。
    """
    low = s.lower()
    if sum(1 for w in _LANG_WORDS if w in low) >= 2:
        return True
    parts = [p.strip(" []()") for p in re.split(r"[|·•]", s) if p.strip(" []()")]
    if len(parts) >= 3 and sum(len(p) for p in parts) / len(parts) <= 14:
        return True
    return False


def first_paragraph(md: str, min_len: int = 24, max_len: int = 320) -> str:
    """README 首段「人话」介绍。

    要滤掉的东西比想象多：居中的 HTML 头图块、一排徽章、语言切换链接、目录、
    「Contribute to ...」样板句。策略是逐段清洗后挑第一段够长的散文。
    """
    if not md:
        return ""
    txt = md
    m = _FM.match(txt)
    if m:
        txt = txt[m.end():]
    for pat, rep in _MD_STRIP:
        txt = pat.sub(rep, txt)
    blocks = re.split(r"\n\s*\n", txt)
    best = ""
    for b in blocks:
        lines = [l.strip() for l in b.split("\n") if l.strip()]
        lines = [l for l in lines if not _NOISE_LINE.match(l)]
        s = " ".join(lines)
        s = re.sub(r"\s+", " ", s).strip(" -—·:：|")
        if len(s) < min_len:
            continue
        if s.count("http") >= 3 or _looks_like_nav(s):
            continue
        letters = re.sub(r"[^\w一-鿿]", "", s)
        if len(letters) < min_len * 0.6:
            continue
        best = s
        break
    if len(best) > max_len:
        cut = best[:max_len]
        for sep in ("。", "！", "？", ". ", "; "):
            i = cut.rfind(sep)
            if i > max_len * 0.5:
                cut = cut[:i + len(sep)]
                break
        best = cut.strip()
    return best


def has_cjk(s: str) -> bool:
    return bool(re.search(r"[一-鿿]", s or ""))


# --------------------------------------------------------------- URL 探活 ---
def url_is_image(url: str, timeout: int = 15, throttle_retries: int = 0) -> tuple[bool, str]:
    """确认一个地址真能出图。缓存结果，重跑不再打网。

    429 的坑：opengraph.githubassets.com 会对同一个出口 IP 限速，返回 200 的
    text/html 提示页或直接 429 —— 实测同一个地址第一次 429、隔 4 秒重试就 200 image/png。
    所以 429 **不缓存**，并且允许调用方要求退避重试；否则会把好图误判成死链。
    """
    if _probe_cache.has(url):
        v = _probe_cache.get(url)
        return bool(v and v.get("ok")), (v or {}).get("ct", "")
    ok, ct, throttled = False, "", False
    for attempt in range(throttle_retries + 1):
        ok, ct, throttled = _probe_once(url, timeout)
        if ok or not throttled:
            break
        time.sleep(4 * (attempt + 1))
    if throttled and not ok:
        return False, "throttled"     # 不缓存：这是我们这边被限速，不是图坏了
    _probe_cache.put(url, {"ok": ok, "ct": ct, "at": TODAY})
    return ok, ct


def _probe_once(url: str, timeout: int) -> tuple[bool, str, bool]:
    ct = ""
    for method in ("HEAD", "GET"):
        try:
            st, body, hdrs = _fetch(url, {"User-Agent": UA_WEB, "Accept": "image/*,*/*"},
                                    timeout=timeout, method=method)
        except Exception:
            return False, "", True    # 网络层挂了：当可重试，不写死结论
        ct = (hdrs.get("Content-Type") or "").split(";")[0].strip().lower()
        if st == 200 and (ct.startswith("image/") or ct == "application/octet-stream"):
            return True, ct, False
        if st == 200 and method == "GET" and body[:4] in (b"\x89PNG", b"\xff\xd8\xff\xe0", b"GIF8", b"RIFF"):
            return True, "image/*", False
        if st == 429 or (st == 200 and ct == "text/html"):
            return False, ct, True    # 限速页，不是死链
        if st in (403, 404):
            return False, ct, False
    return False, ct, False


ASSET_DIRS = ["assets", "images", "img", "docs", "examples", "example", ".github", "media", "static", "screenshots"]
ASSET_NAMES = ["cover", "preview", "banner", "hero", "screenshot", "demo", "example", "og", "social"]
ASSET_EXTS = ["png", "jpg", "webp", "svg", "gif"]


def probe_assets(repo: str, path: str = "", budgeted_listing: bool = False) -> str | None:
    """任务 B 第 4 层：skill 目录里的 assets/ examples/ preview.* 。

    两条路：
      - API 列目录（准，但一个目录一次配额；60/小时下只够十几件，所以默认关，
        用 --use-api-listing 打开，或者有 GH_TOKEN 时才划算）
      - **免费**的固定文件名探测：raw.githubusercontent.com 的 HEAD 不限流，
        30 个候选名并发探，实测比列目录还快。
    """
    base = (path or "").strip("/")
    if budgeted_listing:
        for d in ("assets", "examples", "images"):
            sub = f"{base}/{d}" if base else d
            try:
                lst = gh_api(f"/repos/{repo}/contents/{urllib.parse.quote(sub)}")
            except RateLimited:
                budgeted_listing = False
                break
            if isinstance(lst, list):
                for it in lst:
                    n = (it.get("name") or "").lower()
                    if it.get("type") == "file" and _IMG_EXT.search(n) and not _BADGE_PATH_HINT.search(n):
                        u = it.get("download_url")
                        if u and url_is_image(u)[0]:
                            return u
    cands: list[str] = []
    dirs = ([base] if base else []) + [f"{base}/{d}" if base else d for d in ASSET_DIRS[:4]]
    for d in dirs:
        for n in ASSET_NAMES[:4]:
            for e in ASSET_EXTS[:3]:
                p = f"{d}/{n}.{e}" if d else f"{n}.{e}"
                cands.append(f"https://raw.githubusercontent.com/{repo}/HEAD/{urllib.parse.quote(p)}")
    # 按顺序保留优先级，但并发探活：先并发判定，再按原顺序取第一个活的
    alive: dict[str, bool] = {}
    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        for u, ok in zip(cands, ex.map(lambda x: url_is_image(x)[0], cands)):
            alive[u] = ok
    for u in cands:
        if alive.get(u):
            return u
    return None


# ------------------------------------------------------------------- 货架 ---
AGGREGATE_FILES = {"feed.json", "rejected-feed.json"}


def load_shelf(scope: str = "shelf") -> list[dict]:
    """读货 + **套上 editorial/curation.json 的人工层**。

    这一步不能省：skills/*.json 里每件都是 hide=false，真正的上架与否写在
    editorial/curation.json（564 件 hide=true）。不套人工层就会把 712 件全当在架，
    把配额和时间浪费在 558 件下架货上。

    scope: "shelf" = 只算在架的（当前 154 件）；"all" = 全部抓回来的。
    """
    items: dict[str, dict] = {}
    for f in sorted(glob.glob(os.path.join(SKILLS_DIR, "*.json"))):
        if os.path.basename(f) in AGGREGATE_FILES:
            continue
        try:
            with open(f, encoding="utf-8") as fh:
                it = json.load(fh)
            if it.get("id"):
                items[it["id"]] = it
        except Exception as e:
            _log(f"[shelf] 读不动 {f}: {e}")
    try:
        with open(os.path.join(EDITORIAL, "curation.json"), encoding="utf-8") as fh:
            cur = json.load(fh).get("items", {})
        for k, v in cur.items():
            if k in items and isinstance(v, dict):
                items[k].update(v)
    except Exception as e:
        _log(f"[shelf] 人工层没读到（{e}），退回把全部当在架")
    vals = list(items.values())
    if scope == "all":
        return vals
    return [i for i in vals if not i.get("hide")]


def save_json(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)
    _log(f"[out] 写入 {os.path.relpath(path, ROOT)}  ({os.path.getsize(path)/1024:.0f} KB)")


def pmap(fn, items, workers=8):
    """并发跑，单条失败不拖垮整批；RateLimited 冒到外层由调用方收工。"""
    res = []
    with concurrent.futures.ThreadPoolExecutor(workers) as ex:
        futs = {ex.submit(fn, it): it for it in items}
        for fu in concurrent.futures.as_completed(futs):
            try:
                res.append(fu.result())
            except RateLimited:
                res.append(None)
            except Exception as e:
                it = futs[fu]
                tag = it.get("id") or it.get("repo") if isinstance(it, dict) else str(it)
                _log(f"[warn] {tag}: {type(e).__name__} {str(e)[:70]}")
                res.append(None)
    return res


# =============================================================== 任务 A：描述 ===
THIN_DESC = 80          # 少于这个长度的 desc_en 基本等于没说话


def desc_missing(it: dict) -> bool:
    """两类需要补料的货：

    1. desc_en 太短或压根没有 —— 就是 skills.sh 搜索接口不返描述留下的坑
       （「A pack of 127 skills.」「claude code skills」这种等于没有）
    2. 文案还是占位（tagline_zh 里带「英文简介见下」、没有 title_zh/why_zh）——
       这类按 CURATION.md 五「抓取与文案必须同时做」是欠账，人工写文案前需要原料
    """
    d = (it.get("desc_en") or "").strip()
    t = (it.get("tagline_zh") or "").strip()
    if len(d) < THIN_DESC:
        return True
    if "见下" in t or not (it.get("title_zh") or "").strip():
        return True
    return False


def cmd_describe(args) -> None:
    shelf = load_shelf(args.scope)
    targets = [it for it in shelf if desc_missing(it)] if not args.all else shelf
    if args.limit:
        targets = targets[:args.limit]
    _log(f"[describe] 范围={args.scope}，{len(shelf)} 件，缺描述 {len(targets)} 件"
         f"{'（--all，全量重跑）' if args.all else ''}")

    BUDGET.probe()
    out_path = os.path.join(EDITORIAL, "descriptions.json")
    try:
        with open(out_path, encoding="utf-8") as f:
            prev = json.load(f).get("items", {})
    except Exception:
        prev = {}

    # ---- 免费层：SKILL.md frontmatter + README 首段 + github.com HTML meta ----
    def work(it):
        rid, repo, path = it["id"], it["repo"], (it.get("path") or "")
        rec = {"repo": repo, "path": path, "layers": {}}
        smd = raw_file(repo, (path.rstrip("/") + "/SKILL.md") if path else "SKILL.md")
        if smd:
            fm = skillmd_frontmatter(smd)
            if fm.get("description"):
                rec["layers"]["skillmd"] = fm["description"][:600]
        meta = gh_html_meta(repo)
        if meta.get("description"):
            rec["layers"]["repo_meta"] = meta["description"][:600]
        for k in ("topics", "stars", "pushed_at"):
            if meta.get(k):
                rec[k] = meta[k]
        md = readme_of(repo)
        if md:
            p = first_paragraph(md)
            if p:
                rec["layers"]["readme"] = p
        return rid, rec

    got = pmap(work, targets, workers=args.workers)
    _raw_cache.flush(); _html_cache.flush()

    recs = {rid: rec for rid, rec in [g for g in got if g]}

    # ---- 配额层：只给免费层全落空的补 REST API（描述/topics/homepage/星/推送时间）----
    still = [rid for rid, r in recs.items() if not r["layers"]]
    _log(f"[describe] 免费层跑完：{len(recs) - len(still)}/{len(recs)} 拿到描述；"
         f"{len(still)} 件仍空，转 GitHub REST API")
    api_done, api_left = 0, 0
    if still and not args.no_api:
        for i, rid in enumerate(still):
            try:
                d = gh_api_repo(recs[rid]["repo"])
            except RateLimited as e:
                api_left = len(still) - i
                _log(f"[describe] REST 层提前收工：{e}；还有 {api_left} 件没跑")
                break
            if d:
                if d.get("description"):
                    recs[rid]["layers"]["api"] = d["description"]
                for k in ("topics", "homepage", "stars", "pushed_at"):
                    if d.get(k):
                        recs[rid][k] = d[k]
                api_done += 1
            # API README 兜底（仅当仍无描述且预算还在）
            if not recs[rid]["layers"]:
                try:
                    md = gh_api_readme(recs[rid]["repo"])
                except RateLimited:
                    api_left = len(still) - i
                    break
                if md:
                    p = first_paragraph(md)
                    if p:
                        recs[rid]["layers"]["api_readme"] = p
    _api_cache.flush()

    # ---- 定稿：挑一条最好的 ----
    PRIORITY = ["skillmd", "repo_meta", "api", "readme", "api_readme"]
    filled = 0
    for rid, r in recs.items():
        L = r["layers"]
        # 中文优先：讲中文的商品用中文描述才有意义。
        # 但只有「够长的中文」才配插队 —— 短碎片顶掉一句完整英文描述是净亏。
        zh = [k for k in PRIORITY if has_cjk(L.get(k, "")) and len(L.get(k, "")) >= 20]
        order = zh + [k for k in PRIORITY if k not in zh]
        pick = next((k for k in order if L.get(k)), None)
        if pick:
            r["description"] = L[pick]
            r["description_source"] = pick
            r["lang"] = "zh" if has_cjk(L[pick]) else "en"
            filled += 1
        else:
            r["description"] = ""
            r["description_source"] = None
    prev.update(recs)
    save_json(out_path, {
        "generated_at": TODAY,
        "note": "机器抓来的原料，供人工写标题/简介/点评用。不是直接上架文案。",
        "stats": {"targets": len(targets), "filled": filled, "empty": len(recs) - filled,
                  "api_spent": BUDGET.spent, "api_unfinished": api_left},
        "items": prev,
    })
    from collections import Counter
    c = Counter(r.get("description_source") for r in recs.values())
    _log(f"[describe] 补上 {filled}/{len(targets)}，仍空 {len(recs)-filled}；来源分布 {dict(c)}")
    _log(f"[describe] 消耗 API {BUDGET.spent} 次；未跑完 {api_left} 件")


# =============================================================== 任务 B：封面 ===
COVER_TIERS = {
    "readme_image": ("真产出物图", True),
    "repo_asset": ("真产出物图", True),
    "existing": ("原有封面（已验活）", True),
    "repo_social_preview": ("仓库自定义社交预览图", False),
    "github_og": ("GitHub 官方 OG 卡片", False),
}


def reverify_covers(rounds: int = 4) -> None:
    """把 editorial/covers.json 里没验过的重验一遍——**串行 + 退避**。

    并发验 opengraph.githubassets.com 是自找 429：几个线程同时打同一台，
    本来能出图的也被限成 text/html 提示页。所以这一遍一条一条走，中间歇着。
    """
    path = os.path.join(EDITORIAL, "covers.json")
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    c = doc["covers"]
    for _ in range(rounds):
        bad = [k for k, v in c.items() if not v.get("verified")]
        if not bad:
            break
        _log(f"[verify] 待重验 {len(bad)} 件")
        for k in bad:
            u = c[k].get("cover_url") or ""
            if not u:
                continue
            _probe_cache.data.pop(u, None)
            ok, ct = url_is_image(u, throttle_retries=4)
            c[k]["verified"], c[k]["content_type"] = bool(ok), ct
            time.sleep(1.5)
    n = sum(1 for v in c.values() if v.get("verified"))
    doc["stats"]["verified"], doc["stats"]["unverified"] = n, len(c) - n
    save_json(path, doc)
    _probe_cache.flush()
    _log(f"[verify] 验活通过 {n}/{len(c)}；仍未验过 "
         f"{[k for k, v in c.items() if not v.get('verified')]}")


def cmd_covers(args) -> None:
    if args.verify_only:
        return reverify_covers()
    shelf = load_shelf(args.scope)
    targets = shelf if args.all else [it for it in shelf if not (it.get("cover") or "").strip()]
    # 已有封面里带 JWT 的（private-user-images）几分钟就过期，实测线上已 404，一律当缺封面
    dead = [it for it in shelf if "private-user-images.githubusercontent.com" in (it.get("cover") or "")]
    if not args.all:
        have = {i["id"] for i in targets}
        targets += [it for it in dead if it["id"] not in have]
    if args.limit:
        targets = targets[:args.limit]
    _log(f"[covers] 范围={args.scope}，{len(shelf)} 件；已有封面 {sum(1 for i in shelf if i.get('cover'))} 件；"
         f"其中 {len(dead)} 件是会过期的 private-user-images 链接（当缺图处理）")
    _log(f"[covers] 本轮目标 {len(targets)} 件")

    BUDGET.probe()

    def work(it):
        rid, repo, path = it["id"], it["repo"], (it.get("path") or "")
        rec = {"repo": repo, "path": path, "cover_url": "", "source": "",
               "is_real_artwork": False, "candidates": []}

        # 0) 原有封面还活着就留着（但 JWT 那批直接跳过）
        cur = (it.get("cover") or "").strip()
        if cur and "private-user-images.githubusercontent.com" not in cur:
            ok, _ = url_is_image(cur)
            if ok:
                rec.update(cover_url=cur, source="existing", is_real_artwork=True)
                return rid, rec
            rec["dead_existing"] = cur

        # 3) README 第一张图 —— 最有价值的一层，先跑。
        #    多 skill 仓里，**这个 skill 自己目录下的 README 优先于仓库根 README**：
        #    根 README 那张图讲的是整个合集，本 skill 的图才是它自己的产出物。
        imgs: list[str] = []
        if path:
            for n in ("README.md", "readme.md", "README.zh-CN.md"):
                sub = raw_file(repo, f"{path.rstrip('/')}/{n}")
                if sub:
                    imgs += [u for u in readme_images(sub, repo) if u not in imgs]
                    break
        md = readme_of(repo)
        imgs += [u for u in readme_images(md or "", repo) if u not in imgs]
        # 本仓的图永远排在外链图前面：外链多半是别人的技术 logo，不是这件东西的产出物
        own = f"raw.githubusercontent.com/{repo}/".lower()
        imgs.sort(key=lambda u: 0 if own in u.lower() else 1)
        rec["candidates"] = imgs[:6]
        for u in imgs[:6]:
            if url_is_image(u)[0]:
                rec.update(cover_url=u, source="readme_image", is_real_artwork=True)
                rec["cross_repo"] = own not in u.lower()
                return rid, rec

        # 4) skill 目录 / assets 常见文件名探测（免费）
        a = probe_assets(repo, path, budgeted_listing=args.use_api_listing)
        if a:
            rec.update(cover_url=a, source="repo_asset", is_real_artwork=True)
            return rid, rec

        # 2) 仓库自定义社交预览图 + 1) 官方 OG 图 —— 一次 HTML 请求两个都有
        meta = gh_html_meta(repo)
        og = meta.get("og_image") or ""
        if "repository-images.githubusercontent.com" in og:
            rec.update(cover_url=og, source="repo_social_preview", is_real_artwork=False)
            return rid, rec
        if og:
            rec.update(cover_url=og, source="github_og", is_real_artwork=False)
            return rid, rec
        # HTML 也没拿到就退回猜的 OG 地址（本机常年 429，但浏览器端可用）
        rec.update(cover_url=f"https://opengraph.githubassets.com/1/{repo}",
                   source="github_og_unverified", is_real_artwork=False)
        return rid, rec

    got = pmap(work, targets, workers=args.workers)
    _raw_cache.flush(); _html_cache.flush(); _probe_cache.flush(); _api_cache.flush()
    recs = {rid: rec for rid, rec in [g for g in got if g]}

    # ---- 收尾验活：每一条选中的封面都亲自拉一遍 ----
    # OG 图那一档要带退避重试：opengraph.githubassets.com 会限同一出口 IP 的速，
    # 不重试会把好图误报成死链（实测第一次 429、隔 4 秒就 200 image/png）。
    def verify(kv):
        rid, r = kv
        u = r.get("cover_url") or ""
        if not u:
            r["verified"] = False
            return rid
        ok, ct = url_is_image(u, throttle_retries=3 if "opengraph.githubassets.com" in u else 0)
        r["verified"] = bool(ok)
        r["content_type"] = ct
        return rid
    _log("[covers] 收尾验活（OG 那档带退避重试）…")
    pmap(verify, list(recs.items()), workers=4)
    _probe_cache.flush()
    unverified = [k for k, r in recs.items() if not r.get("verified")]

    from collections import Counter
    c = Counter(r["source"] for r in recs.values())
    real = sum(1 for r in recs.values() if r["is_real_artwork"] and r["source"] != "existing")
    og_only = sum(1 for r in recs.values() if r["source"] in ("github_og", "github_og_unverified", "repo_social_preview"))
    none = sum(1 for r in recs.values() if not r["cover_url"])

    out_path = os.path.join(EDITORIAL, "covers.json")
    save_json(out_path, {
        "generated_at": TODAY,
        "note": ("id → 封面候选。**不写回 skills/*.json**，由人工/上架流程决定采用哪些。"
                 "is_real_artwork=true 表示这是仓库自己的图（README 头图或 assets 里的产出物示例），"
                 "false 表示只是 GitHub 生成的 OG 卡片 —— 后者比渐变色块强，但不是品味的证据。"),
        "tiers": {k: {"label": v[0], "is_real_artwork": v[1]} for k, v in COVER_TIERS.items()},
        "stats": {"targets": len(targets), "by_source": dict(c),
                  "real_artwork": real, "og_or_preview_only": og_only, "none": none,
                  "verified": len(recs) - len(unverified), "unverified": len(unverified)},
        "covers": recs,
    })
    _log(f"[covers] 来源分布 {dict(c)}")
    _log(f"[covers] 真产出物图 {real} 件 / 只有 OG 或社交预览 {og_only} 件 / 完全没有 {none} 件")
    _log(f"[covers] 验活通过 {len(recs)-len(unverified)}/{len(recs)}；没验过的 {len(unverified)} 件：{unverified[:10]}")


# =========================================================== 任务 C：宽漏斗 ===
VERTICAL_QUERIES = [
    # 公文 / 体制内
    "公文", "公文写作", "materialgw", "体制内", "事业单位", "党建", "申论", "行测",
    "公务员", "述职报告", "会议纪要", "政务",
    # 命理 / 周易
    "命理", "八字", "周易", "紫微斗数", "塔罗", "算命", "风水", "奇门遁甲", "六爻", "起名",
    "bazi", "ziwei", "iching", "fengshui",
    # 中医 / 健康 / 过敏
    "中医", "针灸", "方剂", "养生", "食疗", "过敏", "体质", "舌诊", "经络",
    "tcm", "acupuncture", "allergy",
    # 宠物 / 母婴
    "宠物", "猫", "狗", "养猫", "铲屎官", "育儿", "母婴", "辅食", "绘本", "亲子",
    "pet care", "parenting",
    # 跑团 / 竞赛
    "跑团", "trpg", "dnd", "剧本杀", "桌游", "数学建模", "竞赛", "acm", "奥赛", "考研",
    # 方言 / 非遗
    "方言", "粤语", "闽南语", "四川话", "东北话", "非遗", "汉服", "书法", "篆刻", "国画",
    "戏曲", "剪纸", "民俗", "节气",
    # 其它中文垂直
    "小红书", "公众号", "微信", "抖音", "简历", "相亲", "彩礼", "法考", "医保", "社保",
]


def _http_text(url: str, timeout: int = 30) -> str:
    """先走 urllib；证书链验不过时退回 curl。

    坑记录：本机到 skills.sh 之间有一层 TLS 拦截代理（Think Beyond Forward Trust CA）。
    它的根证书装在 macOS 钥匙串里，curl 认，Python 3.14 自带的 OpenSSL 不认
    （报 "Missing Authority Key Identifier"，把根证书喂给它也没用）。
    所以这里退回 curl —— **不是关掉校验**，curl 照样按系统信任库验，只是它认这条链。
    curl 也没有时就放弃这个查询，不影响其它源。
    """
    try:
        st, body, _ = _fetch(url, {"User-Agent": UA_WEB, "Accept": "application/json"}, timeout=timeout)
        if st == 200:
            return body.decode("utf-8", "replace")
        return ""
    except Exception:
        pass
    import shutil, subprocess
    if not shutil.which("curl"):
        return ""
    try:
        p = subprocess.run(["curl", "-sS", "-m", str(timeout), "-A", UA_WEB,
                            "-H", "Accept: application/json", url],
                           capture_output=True, timeout=timeout + 10)
        return p.stdout.decode("utf-8", "replace") if p.returncode == 0 else ""
    except Exception:
        return ""


def skills_sh_search(q: str, limit: int = 50) -> list[dict]:
    raise RuntimeError(
        "skills.sh /api/ 被其 robots.txt 明令 Disallow，本函数已停用。\n"
        "改走 sanctioned 路径：robots.txt 主动公布的 sitemap（sitemap-skills-*.xml）\n"
        "+ 仓库页 /owner/repo（robots 允许，且一次请求就给全仓装机量）。\n"
        "见 scouts/wide_funnel.py。产品裁决 D15，2026-08-19。"
    )
    # 原实现（违规，保留作痕迹，勿恢复）：
    # url = ("https://skills.sh/api/search?q=" + urllib.parse.quote(q) + f"&limit={limit}")
    txt = _http_text(url)
    if not txt:
        return []
    try:
        return json.loads(txt).get("skills", []) or []
    except Exception:
        return []


NON_REPO_HOSTS = ("skills.sh", "smithery.ai", "modelscope.cn", "volces.com", "aliyun",
                  "italent.cn", "italent.link", "moonshot.cn", "coze.cn", "bytedance")


def cmd_funnel(args) -> None:
    shelf = load_shelf("all")
    on_shelf = {i["repo"].lower() for i in shelf}
    _log(f"[funnel] {len(VERTICAL_QUERIES)} 组垂直查询 × skills.sh")

    raw: dict[str, dict] = {}
    scanned = 0
    for q in VERTICAL_QUERIES:
        hits = skills_sh_search(q, args.per_query)
        scanned += len(hits)
        for h in hits:
            src = (h.get("source") or "").strip()
            sid = h.get("id") or ""
            if not src:
                continue
            rec = raw.setdefault(sid, {
                "skill_id": sid, "name": h.get("name") or h.get("skillId") or "",
                "source": src, "installs": h.get("installs", 0), "queries": []})
            if q not in rec["queries"]:
                rec["queries"].append(q)
        _log(f"[funnel] {q:<12} → {len(hits)} 条（累计去重 {len(raw)}）")
        time.sleep(0.25)

    # 分流：GitHub 仓库 vs 平台内资产（后者按 CURATION.md 三-平台画廊：只当情报，不当货源）
    gh, platform = {}, {}
    for sid, r in raw.items():
        s = r["source"]
        if any(h in s for h in NON_REPO_HOSTS) or s.count("/") != 1:
            platform[sid] = r
        else:
            r["repo"] = s
            r["on_shelf"] = s.lower() in on_shelf
            gh[sid] = r

    _log(f"[funnel] 扫到 {scanned} 条命中，去重 {len(raw)} 条：GitHub 仓库 {len(gh)} 条 / "
         f"平台内资产 {len(platform)} 条（不当货源）")

    # 免费层补元数据：github.com HTML（描述 + 星）
    repos = sorted({r["repo"] for r in gh.values() if not r["on_shelf"]})
    _log(f"[funnel] 未上架仓库 {len(repos)} 个，拉元数据（免费层）…")

    def meta(rp):
        m = gh_html_meta(rp)
        return rp, m

    ms = dict(x for x in pmap(meta, repos, workers=args.workers) if x)
    _html_cache.flush()
    for r in gh.values():
        m = ms.get(r.get("repo")) or {}
        r["desc"] = m.get("description", "")
        r["stars"] = m.get("stars", 0)
        r["pushed_at"] = m.get("pushed_at", "")
        r["alive"] = bool(m.get("ok"))

    save_json(os.path.join(EDITORIAL, "funnel_raw.json"), {
        "generated_at": TODAY,
        "queries": VERTICAL_QUERIES,
        "stats": {"hits": scanned, "unique": len(raw), "github_repos": len(gh),
                  "platform_assets": len(platform),
                  "already_on_shelf": sum(1 for r in gh.values() if r["on_shelf"])},
        "github": gh,
        "platform_only": platform,
    })


# ------------------------------------------------------------------- main ---
def main() -> None:
    ap = argparse.ArgumentParser(description="描述 / 封面 / 宽漏斗 补全器")
    ap.add_argument("cmd", choices=["describe", "covers", "funnel"])
    ap.add_argument("--limit", type=int, default=0, help="只处理前 N 件（调试用）")
    ap.add_argument("--all", action="store_true", help="全量重跑，不只跑缺的")
    ap.add_argument("--no-api", action="store_true", help="完全不碰 GitHub REST API（纯免费层）")
    ap.add_argument("--verify-only", action="store_true",
                    help="covers：不重新找图，只把 editorial/covers.json 里没验过的串行重验（专治 429）")
    ap.add_argument("--use-api-listing", action="store_true",
                    help="covers：用 API 列 assets/ 目录（准，但一个目录一次配额；未认证 60/小时基本不够，建议配 GH_TOKEN 再开）")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--per-query", type=int, default=50, help="funnel：每组查询取多少条")
    ap.add_argument("--scope", choices=["shelf", "all"], default="shelf",
                    help="shelf=只跑在架的（套 editorial/curation.json 的 hide）；all=全部抓回来的")
    a = ap.parse_args()
    t0 = time.time()
    try:
        {"describe": cmd_describe, "covers": cmd_covers, "funnel": cmd_funnel}[a.cmd](a)
    except RateLimited as e:
        _log(f"[abort] 限流退出：{e}")
    finally:
        for c in (_raw_cache, _html_cache, _api_cache, _probe_cache):
            c.flush()
        _log(f"[done] {a.cmd} 用时 {time.time()-t0:.0f}s，API 消耗 {BUDGET.spent} 次，"
             f"剩余 {BUDGET.remaining}")


if __name__ == "__main__":
    main()
