#!/usr/bin/env python3
"""Write 原声-grade /i/<id>/ pages for every item on the shelf."""
from __future__ import annotations
import json, os, html, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED = os.path.join(ROOT, "skills", "feed.json")
OUT = os.path.join(ROOT, "i")
CAT = {
    "creative": "做图", "writing": "写字", "life": "生活", "fun": "玩乐",
    "work": "工作", "body": "生活", "learn": "生活", "docs": "工作",
    "dev": "工作", "meta": "工作",
}
MARK = """<svg viewBox="14 4 33 55" fill="currentColor" stroke="currentColor" stroke-width="2.4"
     stroke-linejoin="round" stroke-linecap="round" aria-hidden="true">
  <g transform="rotate(-7 32 32)">
    <path d="M18.6 7 L21.4 7.3 L31.1 55.8 L30.9 55.8 Z"/>
    <path d="M39.6 9 L42.4 8.7 L35.2 55.8 L35 55.8 Z"/>
  </g>
</svg>"""


def esc(s):
    return html.escape(s or "", quote=True)


def junk_lede(lede, name, title):
    s = (lede or "").strip()
    if not s:
        return True
    if "英文简介" in s or "见下" in s:
        return True
    blob = (name or "") + " " + (title or "")
    if any(x and x in s for x in (name, title) if x) and len(s) < 40:
        return True
    return False


COVER_DENY = (
    "private-user-images", "jwt=", "opengraph.githubassets",
    "camo.githubusercontent", "shields.io", "img.youtube.com",
    "i.ytimg.com", "skills.sh/b/",
)

def cover_ok(c):
    c = (c or "").strip()
    # 09-03：封面改成同源托管（/skill/assets/covers/…）之后，这里只认 http 开头 → 详情页一直没图。
    if c.startswith("/skill/"):
        # 文件得真在仓里；机器层记的托管路径有的已经没文件了（cli-cli-code-review 404），那就算没图 → 走预览卡
        if not os.path.exists(os.path.join(ROOT, c[len("/skill/"):])):
            return ""
        c = "https://ourword.ai" + c
    if not c.startswith("http"):
        return ""
    low = c.lower()
    if any(x in low for x in COVER_DENY):
        return ""
    return c

def cover_of(it):
    c = cover_ok(it.get("cover"))
    if c:
        return c
    p = os.path.join(ROOT, "skills", it["id"] + ".json")
    if os.path.exists(p):
        try:
            raw = json.load(open(p, encoding="utf-8"))
            return cover_ok(raw.get("cover"))
        except Exception:
            return ""
    return ""


def page(it, prev=None, nxt=None, related=None):
    title = it.get("title_zh") or it.get("name") or it["id"]
    cat_id = it.get("category") or ""
    cat = CAT.get(cat_id, cat_id)
    why = (it.get("why_zh") or "").strip()
    raw_lede = (it.get("tagline_zh") or "").strip()
    lede = "" if junk_lede(raw_lede, it.get("name"), title) else raw_lede
    limit = (it.get("limit_zh") or "").strip()
    repo = it.get("repo") or ""
    owner = it.get("owner") or (repo.split("/")[0] if repo else "")
    added = (it.get("added_at") or "")[:10]
    gh = it.get("url") or ("https://github.com/" + repo if repo else "")
    url = "https://ourword.ai/skill/i/%s/" % it["id"]
    related = related or []
    rel = []
    for o in related[:3]:
        rel.append('<a href="../%s/">%s</a>' % (esc(o["id"]), esc(o.get("title_zh") or o.get("name") or o["id"])))
    related_html = ('<div class="box"><p class="hd">同类 Skill</p><div class="rel">%s</div></div>' % "".join(rel)) if rel else ""

    ins = it.get("install") or {}
    cmds = [ins[k] for k in ("clone", "copy") if ins.get(k)]
    cover = cover_of(it)
    # 店主 09-03：「详情页把封面图也放进去，如果有的话，没有的话就放 github url 预览卡」。
    # 卡片上不铺预览卡；详情页一次只看一件，预览卡是这个仓的门脸，放。
    cover_is_og = False
    if not cover and it.get("repo"):
        cover = "https://opengraph.githubassets.com/pinwei/%s" % it["repo"]
        cover_is_og = True

    # 封面引 800px 宽的 WebP 派生图（scouts/make_thumbs.py 生成）。详情页这张显示
    # 350×242，原图却是 1200-2500 宽、平均 788 KB。派生图缺失就回退原图。
    def _thumb(u):
        import re as _re
        m = _re.match(r"^(https://ourword\.ai/skill/assets/covers/|/skill/assets/covers/)([^/]+)\.[A-Za-z0-9]+$", u or "")
        return (m.group(1) + "w800/" + m.group(2) + ".webp") if m else u
    _t = _thumb(cover)
    _fb = (' data-full="%s" onerror="if(this.dataset.full){this.src=this.dataset.full;delete this.dataset.full}else{this.remove()}' % esc(cover)) if _t != cover else ' onerror="this.remove()'
    media = ('<img class="cover%s" src="%s" alt=""%s">' % (" og" if cover_is_og else "", esc(_t), _fb)) if cover else ""

    uses_map = {
        "creative": [
            "把我手上这张按它的规矩重做，风格不许换。",
            "只要成品，过程里的解释可以没有。",
            "做完对照应用范围，越界的那一稿丢掉。",
        ],
        "writing": [
            "按它的句式改这一段，能删就删。",
            "先标出越界的句子，再重写，不要通篇润色。",
            "写完对照应用范围，串味就停。",
        ],
        "life": [
            "按我给的现场条件出方案，条件不够就说做不到。",
            "不要写成对谁都适用的攻略。",
            "结论里把限制写在最前面。",
        ],
        "fun": [
            "按规则玩一轮，把依据留在结果里。",
            "编不出来就停，不要圆。",
            "玩完对照应用范围，别拿它当正事工具。",
        ],
        "work": [
            "按它的流程走完这一件，不要跳步骤。",
            "输出要能进仓库或工单，不要只给感想。",
            "做完对照应用范围，越权的活另找工具。",
        ],
    }
    uses = ["就按「%s」这一件来做，不要中途改风格。" % title] + uses_map.get(cat_id, uses_map["creative"])
    uses_html = "".join("<li>%s</li>" % esc(x) for x in uses)
    scope = limit or ""
    if scope:
        scope = "用在「%s」这一格。%s" % (cat, scope)
    else:
        scope = "用在「%s」。超出这一格，它不会变聪明。" % cat

    cmd_html = []
    for c in cmds:
        cmd_html.append(
            '<div class="cmd"><code>%s</code>'
            '<button type="button" data-copy="%s">复制</button></div>'
            % (esc(c), esc(c))
        )

    tags = [x for x in (owner, "店长推荐" if it.get("pick") else "") if x]
    tag_html = "".join('<span class="tag">%s</span>' % esc(t) for t in tags)

    pull = ""
    purpose = why
    if lede and why and lede not in why:
        purpose = lede + "。" + why if not lede.endswith("。") else lede + why
    elif lede and not why:
        purpose = lede
    body_sec = ('<section class="sec"><h2>做什么用</h2><p>%s</p></section>' % esc(purpose)
                if purpose else "")
    limit_sec = '<section class="sec"><h2>应用范围</h2><p>%s</p></section>' % esc(scope)
    uses_sec = '<section class="sec"><h2>如何使用</h2><ul class="uses">%s</ul></section>' % uses_html
    install_sec = ('<section class="sec"><h2>安装</h2><div class="cmds">%s</div></section>'
                   % "".join(cmd_html) if cmd_html else "")
    who_box = ""

    sib = []
    if prev:
        sib.append('<a href="../%s/">← %s</a>' % (
            esc(prev["id"]), esc(prev.get("title_zh") or prev.get("name") or prev["id"])))
    else:
        sib.append("<span></span>")
    if nxt:
        sib.append('<a href="../%s/">%s →</a>' % (
            esc(nxt["id"]), esc(nxt.get("title_zh") or nxt.get("name") or nxt["id"])))
    else:
        sib.append("<span></span>")

    desc = (lede or why or title)[:160]
    og_img = ""
    if cover:
        og_img = ('<meta property="og:image" content="%s">'
                  '<meta name="twitter:image" content="%s">' % (esc(cover), esc(cover)))
    ld = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": title,
        "description": desc,
        "url": url,
        "applicationCategory": cat or "AgentSkill",
        "operatingSystem": "Claude Code, Codex, Agent Skills",
        "isPartOf": {"@type": "WebSite", "name": "品味", "url": "https://ourword.ai/skill/"},
    }
    if owner:
        ld["author"] = {"@type": "Person", "name": owner}
    if cover:
        ld["image"] = cover
    if gh:
        ld["codeRepository"] = gh

    return """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s — 品味</title>
<meta name="description" content="%s">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="keywords" content="品味, Agent Skill, Claude Code, %s, %s">
<link rel="canonical" href="%s">
<link rel="alternate" type="application/rss+xml" title="品味" href="https://ourword.ai/skill/feed.xml">
<link rel="icon" type="image/svg+xml" href="https://ourword.ai/skill/icon.svg">
<link rel="apple-touch-icon" sizes="180x180" href="https://ourword.ai/skill/apple-touch-icon.png">
<link rel="stylesheet" href="../../assets/item.css?v=12">
<style>
img.cover{display:block;width:100%%;height:auto;margin:14px 0 6px;border-radius:12px;border:1px solid var(--rule,#e2ddd0);background:#eae7de}
img.cover.og{aspect-ratio:2;object-fit:cover}
.wrap{padding-left:max(20px,env(safe-area-inset-left))!important;padding-right:max(20px,env(safe-area-inset-right))!important}
</style>
<meta property="og:type" content="article">
<meta property="og:site_name" content="品味">
<meta property="og:locale" content="zh_CN">
<meta property="og:title" content="%s — 品味">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
%s
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%s — 品味">
<meta name="twitter:description" content="%s">
<script type="application/ld+json">%s</script>
<meta name="theme-color" content="#f4efe6">
</head>
<body>
<header class="wrap mast">
  <div class="mast-top">
    <a class="brand" href="../../">
      %s
      <b>品味</b>
    </a>
    <nav class="mast-side">
      <a class="pill" href="../../">货架</a>
      <button class="pill" type="button" id="share" data-url="%s">分享</button>
    </nav>
  </div>
  <p class="slogan">帮你发现有品位的 Skills</p>
</header>

<div class="wrap ep-grid">
  <article>
    <div class="kicker">
      <span class="src">%s</span>
      <span>%s</span>
      <span class="date">%s</span>
    </div>
    <h1 class="ttl">%s</h1>
    %s
    <div class="tags">%s</div>
    %s
    %s
    %s
    %s
    %s
    %s
  </article>
  <aside class="aside">
    %s
    <div class="box">
      <dl class="kv">
        <dt>分类</dt><dd>%s</dd>
        <dt>作者</dt><dd>%s</dd>
        <dt>上架</dt><dd>%s</dd>
      </dl>
      <a class="pill" href="%s" rel="noopener">在 GitHub 查看</a>
    </div>
    %s
  </aside>
  <nav class="foot fam">
    <a href="https://ourword.ai/">人类生存法则</a>
    <a href="https://ourword.ai/podcast/">原声播客</a>
    <a href="https://ourword.ai/skill/" aria-current="page">品味 Skill</a>
  </nav>
  <nav class="foot">%s</nav>
</div>
<script>
(function(){
  function copy(t, btn, done){
    var old = btn.textContent;
    function ok(){ btn.textContent = done || '已复制'; btn.classList.add('on');
      setTimeout(function(){ btn.textContent=old; btn.classList.remove('on'); }, 1400); }
    if(navigator.clipboard) navigator.clipboard.writeText(t).then(ok, ok); else ok();
  }
  document.addEventListener('click', function(e){
    var s = e.target.closest('#share');
    if(s){ copy(s.getAttribute('data-url'), s, '已分享'); return; }
    var c = e.target.closest('[data-copy]');
    if(c) copy(c.getAttribute('data-copy'), c);
  });
})();
</script>
</body>
</html>
""" % (
        esc(title),
        esc(desc),
        esc(cat),
        esc(owner),
        esc(url),
        esc(title),
        esc(desc),
        esc(url),
        og_img,
        esc(title),
        esc(desc),
        json.dumps(ld, ensure_ascii=False, separators=(",", ":")),
        MARK,
        esc(url),
        esc(cat),
        esc(owner),
        esc(added),
        esc(title),
        ('<p class="lede">%s</p>' % esc(lede)) if lede else "",
        tag_html,
        media,
        pull,
        body_sec,
        limit_sec,
        uses_sec,
        install_sec,
        who_box,
        esc(cat),
        esc(owner),
        esc(added),
        esc(gh),
        related_html,
        "".join(sib),
    )


def main():
    feed = json.load(open(FEED, encoding="utf-8"))
    items = [it for it in (feed.get("skills") or []) if not it.get("hide")]
    n = 0
    for i, it in enumerate(items):
        prev = items[i - 1] if i else None
        nxt = items[i + 1] if i + 1 < len(items) else None
        d = os.path.join(OUT, it["id"])
        os.makedirs(d, exist_ok=True)
        same = [x for x in items if x.get("category")==it.get("category") and x["id"]!=it["id"]][:3]
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(it, prev, nxt, same))
        n += 1
    keep = {it["id"] for it in items}
    dropped = 0
    for folder in (OUT, os.path.join(ROOT, "zh", "i")):
        if not os.path.isdir(folder):
            continue
        for name in os.listdir(folder):
            p = os.path.join(folder, name)
            if os.path.isdir(p) and name not in keep:
                shutil.rmtree(p)
                dropped += 1
    print("[pages] wrote %s article pages, pruned %s stale" % (n, dropped))
    seo = os.path.join(ROOT, "seo")
    if seo not in sys.path:
        sys.path.insert(0, seo)
    here = os.getcwd()
    try:
        os.chdir(ROOT)
        import build_seo
        build_seo.main()
    except Exception as e:
        print("[pages] seo skip:", e)
    finally:
        os.chdir(here)


if __name__ == "__main__":
    main()
