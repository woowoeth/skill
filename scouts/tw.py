#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""繁体版：把构建好的简体站整树转到 /skill/tw/。

    python3 scouts/tw.py

跟 ourword.ai 和原声那两个站同一套做法，但这个站有一处更省事：
**页面之间用的是相对链接**（`href="../../"`、`href="../兄弟条目/"`），
所以拷到 /tw/ 下面天然自洽，不用重写路径。只有 canonical / og:url /
sitemap 这些绝对地址要改。

三条必须守住的规矩（前两条是另外两个站踩出来的）：

① **占位符不能用 \\x00。** 保护 URL 不被转换时，OpenCC 底层是 C 字符串，
   遇 \\x00 直接截断 —— 主站第一版转出来的页面里 href 被正文填满，
   而页面照样渲染、构建照样通过。用私用区字符。

② **只对简体源转一次**，不对 tw/ 再转。

③ 用 s2tw 不用 s2twp：后者会替换词汇（信息→資訊、对象→物件、支持→支援）。
   这个站的正文里技术词很密，词汇替换误伤面比收益大。
"""
import os
import re
import shutil

import opencc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tw")
ALLOW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tw_allow.txt")
SITE = "https://ourword.ai/skill"

_cc = opencc.OpenCC("s2tw")

# 一简多繁里两边都讲得通、必须逐处确认的字
AMBIGUOUS = "髮隻餘覆複麵乾鬆檯曆製彆繫捲穀僕醜範衝徵"

# ── 修正表：逐条在真实语料里核对过 ──────────────────────────────
FIX = [
    # 副词「只」被当成量词「隻」。量词的用法不动：
    # 「一隻毛絨絨的你」「配一隻跟著筆尖走的手」「要多隻巨物」「那隻手」都是对的。
    ("別隻", "別只"), ("是隻", "是只"),
    # 「冷面几何」是一种设计风格（面无表情的几何），不是朝鲜冷面。
    ("冷麵幾何", "冷面幾何"),
    # 「7 天历史」被切成「天历|史」
    ("天曆史", "天歷史"),
]

# 繁体里**绝不该出现**的组合，只可能来自分词切错。
# 这一条比逐字审系统：逐字审只能看见你想到要看的字。
# 这个站的「7 天曆史」就是它扫出来的。
NEVER = (
    "繫統 髮生 髮明 髮現 髮展 髮布 髮起 髮動 髮配 髮送 髮表 髮言 髮揮 髮達 髮電 髮射 髮行 "
    "隻能 隻有 隻是 隻要 隻好 隻剩 "
    "麵對 麵臨 麵子 麵前 麵積 麵板 麵貌 麵向 麵試 "
    "乾部 乾預 乾擾 乾涉 曆史 曆程 曆來 徵服 徵途 徵戰 "
    "製度 體製 機製 控製 專製 限製 抑製 強製 調製度 "
    "鬆樹 穀歌 試捲 問捲 僕後 檯風 覆雜 覆習 姓範 彆的 彆人 醜時"
).split()

# 台湾教育部把「佈」并入「布」
POST = [("佈", "布")]

# 语言标记：转换碰不到它们（是标记不是正文），漏了就被按简体归类
LOCALE = [
    ('property="og:locale" content="zh_CN"', 'property="og:locale" content="zh_TW"'),
    # t/ 和 all/ 那些英文页上有「本页另有简体版」的声明，繁体拷贝里该指繁体
    ('property="og:locale:alternate" content="zh_CN"',
     'property="og:locale:alternate" content="zh_TW"'),
    ('"inLanguage": "zh-CN"', '"inLanguage": "zh-TW"'),
    ('"inLanguage":"zh-CN"', '"inLanguage":"zh-TW"'),
    ('"inLanguage": "zh-Hans"', '"inLanguage": "zh-Hant"'),
    # 首页那段 I18N 脚本里写死了 lang：
    #   document.documentElement.lang = lang==="zh" ? "zh-CN" : "en"
    # 静态 HTML 里的 zh-Hant 会被它在运行时覆盖回 zh-CN —— 看页面看不出来，
    # 只有在浏览器里读 documentElement.lang 才发现。
    ('.lang = lang==="zh" ? "zh-CN" : "en"', '.lang = lang==="zh" ? "zh-Hant" : "en"'),
]

URLISH = re.compile(r"^(https?:|//|/|#|\.\.?/|mailto:|data:)")
ATTR = re.compile(r'\b(href|src|action|srcset|content|url)\s*=\s*"([^"]*)"')

SKIP_DIRS = {".git", ".github", ".claude", "scouts", "seo", "schema", "skills",
             "methods", "methods_rejected", "materials", "editorial", "docs",
             "node_modules", "__pycache__", "tw"}
SKIP_FILES = {"robots.txt", "CNAME", "LICENSE", "README.md"}
TEXT_EXT = {".html", ".js", ".json", ".txt", ".xml", ".css", ".svg"}
BIN_EXT = {".png", ".jpg", ".jpeg", ".ico", ".webp", ".gif", ".woff", ".woff2", ".avif"}
URLFILE = {"sitemap.xml", "feed.xml", "llms.txt", "llms-full.txt"}

# 页面在**运行时** fetch 的数据文件。skills/ 整个目录 6.9MB 不进繁体站，
# 但首页要从 skills/feed.json 取货架 —— 不带上它，繁体首页会显示
# 「feed.json 讀取失敗，貨架這次沒裝上」，而所有静态检查都是绿的。
# 这一类只有真的打开页面才看得见，所以 check_tw.py 里专门有一条判据扫 fetch 目标。
FETCHED = ["skills/feed.json"]


def convert(text):
    if not text:
        return text
    out = _cc.convert(text)
    for a, b in FIX:
        out = out.replace(a, b)
    for a, b in POST:
        out = out.replace(a, b)
    return out


def contexts(text):
    """歧义字的三字上下文。三字而不是二字：分词错会造出合法的二字词
    （「明白髮生」里的「白髮」是正经词），二字白名单放它过就抓不到。"""
    out, n = [], len(text)
    for i, ch in enumerate(text):
        if ch in AMBIGUOUS:
            out.append((text[i - 1] if i else "　") + ch + (text[i + 1] if i + 1 < n else "　"))
    return out


def load_allow():
    if not os.path.exists(ALLOW):
        return set()
    return {l.rstrip("\n") for l in open(ALLOW, encoding="utf-8")
            if l.strip() and not l.startswith("#")}


def _protect(s):
    keep = []

    def stash(v):
        keep.append(v)
        return "%d" % (len(keep) - 1)

    def attr(m):
        name, val = m.group(1), m.group(2)
        if URLISH.match(val) or "%" in val:
            return '%s="%s"' % (name, stash(val))
        return m.group(0)

    return ATTR.sub(attr, s), keep


def _retarget(s):
    """站内**相对**链接不用动，只把绝对地址指到 /tw/ 下；hreflang 不动。"""
    holes = []
    s = re.sub(r'<link rel="alternate" hreflang[^>]*>',
               lambda m: holes.append(m.group(0)) or "%d" % (len(holes) - 1), s)
    s = s.replace(SITE + "/", SITE + "/tw/").replace(SITE + "/tw/tw/", SITE + "/tw/")
    return re.sub("(\\d+)", lambda m: holes[int(m.group(1))], s)


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    n_t = n_b = 0
    for dp, dn, fn in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT)
        if set(rel.split(os.sep)) & SKIP_DIRS:
            dn[:] = []
            continue
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if f in SKIP_FILES or f.startswith("."):
                continue
            ext = os.path.splitext(f)[1].lower()
            src = os.path.join(dp, f)
            dst = os.path.join(OUT, os.path.relpath(src, ROOT))
            if ext in TEXT_EXT:
                s = open(src, encoding="utf-8", errors="ignore").read()
                if f.endswith(".html"):
                    s = re.sub(r'<html([^>]*)\blang="[^"]*"', r'<html\1lang="zh-Hant"',
                               s, count=1)
                    if 'lang="zh-Hant"' not in s:
                        s = re.sub(r"<html\b", '<html lang="zh-Hant"', s, count=1)
                kept, keep = _protect(s)
                kept = convert(kept)
                s = re.sub("(\\d+)", lambda m: keep[int(m.group(1))], kept)
                s = _retarget(s)
                if f in URLFILE:
                    s = s.replace(SITE + "/", SITE + "/tw/").replace(SITE + "/tw/tw/", SITE + "/tw/")
                for a, b in LOCALE:
                    s = s.replace(a, b)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                open(dst, "w", encoding="utf-8").write(s)
                n_t += 1
            elif ext in BIN_EXT:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                n_b += 1
    # 运行时 fetch 的数据文件：单独带上，并且要转换（货架上的标题和点评是中文）
    for rel in FETCHED:
        src = os.path.join(ROOT, rel)
        if not os.path.exists(src):
            continue
        dst = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "w", encoding="utf-8").write(
            convert(open(src, encoding="utf-8", errors="ignore").read()))
        n_t += 1
    return n_t, n_b


# ── 语言层：hreflang + 首访跟随 + 头部切换按钮 ──────────────────
HWL_A, HWL_B = "<!--TW:LANG-->", "<!--/TW:LANG-->"

_LANG_JS = (
    "<script>(function(){try{"
    # 语言偏好的键**三个站共用**：主站、原声、品味同域，localStorage 是通的。
    # 原来各站一个键（hwx_lang / podcast_lang / skill_lang），读者在主站选了
    # 繁體，进品味还是简体 —— 同一个人同一个域，选一次却不通用。
    "var K='hwx_lang',p=location.pathname,tw=/^\\/skill\\/tw(\\/|$)/.test(p);"
    "var en=new URLSearchParams(location.search).get('lang')==='en';"
    "var cur=en?'en':(tw?'tw':'sc');"
    "var to={sc:tw?(p.replace(/^\\/skill\\/tw/,'/skill')||'/skill/'):p,"
    # 英文统一落在简体路径上：繁体页的静态文字已经转过形，再叠一层英文
    # 界面会中英繁三种混在一页。
    "tw:tw?p:p.replace(/^\\/skill/,'/skill/tw'),"
    "en:(tw?(p.replace(/^\\/skill\\/tw/,'/skill')||'/skill/'):p)+'?lang=en'};"
    "var saved=null;try{saved=localStorage.getItem(K)}catch(e){}"
    # **URL 里已经写了语言，就以 URL 为准。**
    # 原来无条件跟随浏览器语言，后果实测过：打开 /skill/tw/ 会被改写回
    # /skill/ —— 只要浏览器的语言列表里有 zh。分享出去的繁体链接全失效。
    "if(cur!=='sc'){"
    "if(!saved){try{localStorage.setItem(K,cur)}catch(e){}}"
    "}else{"
    "var L=(navigator.languages||[navigator.language||'']).join(',');"
    "var want=saved||(/zh-(hant|tw|hk|mo)/i.test(L)?'tw':(/zh/i.test(L)?'sc':'en'));"
    "if(want!=='sc'&&to[want]){location.replace(to[want]);return}"
    "}"
    "document.addEventListener('DOMContentLoaded',function(){"
    "var host=document.querySelector('.mast-side');if(!host)return;"
    # 一个下拉，三种语言。原来是两个控件：繁體（正文简繁，路径）和 EN
    # （界面语言，查询参数）。轴不同，但读者看到的是两个都写着语言的按钮，
    # 猜不出差别 —— 而且三个站三种样子，同一个人要学三次。
    #
    # 页面自己那个 #langBtn 只藏起来不删：站里的 JS 还在读它
    # （el("langBtn").textContent = t("btn")），删了会抛错。
    "var old=document.getElementById('langBtn');if(old)old.style.display='none';"
    "var sel=document.createElement('select');sel.id='langPick';sel.className='pill';"
    "sel.setAttribute('aria-label','\\u8bed\\u8a00 Language');"
    "[['sc','\\u7b80\\u4f53'],['tw','\\u7e41\\u9ad4'],['en','English']].forEach(function(kv){"
    "var o=document.createElement('option');o.value=kv[0];o.textContent=kv[1];"
    "if(kv[0]===cur)o.selected=true;sel.appendChild(o)});"
    "sel.onchange=function(){if(sel.value===cur)return;"
    "try{localStorage.setItem(K,sel.value)}catch(e){};location.href=to[sel.value]};"
    "host.insertBefore(sel,host.firstChild)})"
    "}catch(e){}})();</script>"
)



def patch_lang():
    """给简体站每一页补语言层。

    放在**简体树**上做，繁体站是拿它整树转出来的 —— 注入一次，两边天然对称。
    按钮插进 .mast-side（跟「货架」「分享」那排 pill 并排），不浮在页面上。

    注意这个站头部已经有一个 #langBtn，那是首页的 zh/en **界面文案**开关
    （`?lang=en`，只换 I18N 字典里那几句，不换正文，条目页也没有）。
    两者是不同的轴：那个切界面语言，这个切正文的简繁。所以并排放，不合并。

    hreflang 用静态 link 标签：爬虫不执行 JS，只有静态标签能让搜索引擎知道
    这两个地址是同一页的两种写法。这三行在两份拷贝里内容一样，
    所以 _retarget 必须跳过它们（它已经跳了）。
    """
    n = 0
    for dp, dn, fn in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT)
        if set(rel.split(os.sep)) & SKIP_DIRS:
            dn[:] = []
            continue
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if f not in ("index.html", "404.html"):
                continue
            path = os.path.join(dp, f)
            s = open(path, encoding="utf-8", errors="ignore").read()
            if 'http-equiv="refresh"' in s:
                continue
            if HWL_A in s:                      # 幂等：重跑不叠加
                s = re.sub(re.escape(HWL_A) + r".*?" + re.escape(HWL_B), "", s, flags=re.S)
            r = os.path.relpath(path, ROOT).replace(os.sep, "/")
            r = "/" + r[:-len("index.html")] if r.endswith("index.html") else "/" + r
            blk = (HWL_A
                   + '<link rel="alternate" hreflang="zh-Hans" href="%s%s">' % (SITE, r)
                   + '<link rel="alternate" hreflang="zh-Hant" href="%s/tw%s">' % (SITE, r)
                   + '<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, r)
                   + _LANG_JS + HWL_B)
            m = re.search(r'<meta name="viewport"[^>]*>\n?', s) or re.search(r"<head[^>]*>\n?", s)
            if not m:
                continue
            s2 = s[:m.end()] + blk + s[m.end():]
            if s2 != s:
                open(path, "w", encoding="utf-8").write(s2)
                n += 1
    return n


if __name__ == "__main__":
    print("语言层注入 %d 页" % patch_lang())
    t, b = build()
    print("繁体站 /tw/：文本 %d，二进制 %d" % (t, b))
