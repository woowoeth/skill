#!/usr/bin/env python3
"""Write 原声-grade /i/<id>/ pages for every item on the shelf."""
from __future__ import annotations
import json, os, html, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED = os.path.join(ROOT, "skills", "feed.json")
OUT = os.path.join(ROOT, "i")
CAT = {
    "creative": "做图", "fun": "玩", "writing": "写文章", "life": "过日子",
    "body": "养身体", "work": "上班用", "learn": "学东西", "dev": "做图",
    "meta": "店长位",
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


def page(it, prev=None, nxt=None):
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
    ins = it.get("install") or {}
    cmds = [ins[k] for k in ("clone", "copy") if ins.get(k)]
    cover = cover_of(it)

    media = ('<img class="cover" src="%s" alt="">' % esc(cover)) if cover else ""

    cmd_html = []
    for c in cmds:
        cmd_html.append(
            '<div class="cmd"><code>%s</code>'
            '<button type="button" data-copy="%s">复制</button></div>'
            % (esc(c), esc(c))
        )

    tags = [x for x in (owner, "店长推荐" if it.get("pick") else "") if x]
    tag_html = "".join('<span class="tag">%s</span>' % esc(t) for t in tags)

    pull = ('<aside class="pull"><span class="lbl">点评</span>%s</aside>' % esc(why)
            if why else "")
    limit_sec = ('<section class="sec"><h2>局限</h2><p>%s</p></section>' % esc(limit)
                 if limit else "")
    install_sec = ('<section class="sec"><h2>安装</h2><div class="cmds">%s</div></section>'
                   % "".join(cmd_html) if cmd_html else "")

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

    return """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s — 品味</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<link rel="icon" type="image/svg+xml" href="../../icon.svg">
<link rel="stylesheet" href="../../assets/item.css?v=10">
<style>
.wrap{padding-left:max(20px,env(safe-area-inset-left))!important;padding-right:max(20px,env(safe-area-inset-right))!important}
</style>
<meta property="og:type" content="article">
<meta property="og:site_name" content="品味">
<meta property="og:title" content="%s — 品味">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
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
    %s
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
  </article>
  <aside class="aside">
    <div class="box">
      <dl class="kv">
        <dt>分类</dt><dd>%s</dd>
        <dt>仓库</dt><dd>%s</dd>
        <dt>上架</dt><dd>%s</dd>
      </dl>
      <a class="pill" href="%s" rel="noopener">打开仓库</a>
    </div>
  </aside>
  <nav class="foot">%s</nav>
</div>
<script>
(function(){
  function copy(t, btn){
    var old = btn.textContent;
    function ok(){ btn.textContent='已复制'; btn.classList.add('on');
      setTimeout(function(){ btn.textContent=old; btn.classList.remove('on'); }, 1400); }
    if(navigator.clipboard) navigator.clipboard.writeText(t).then(ok, ok); else ok();
  }
  document.addEventListener('click', function(e){
    var s = e.target.closest('#share');
    if(s){ copy(s.getAttribute('data-url'), s); return; }
    var c = e.target.closest('[data-copy]');
    if(c) copy(c.getAttribute('data-copy'), c);
  });
})();
</script>
</body>
</html>
""" % (
        esc(title),
        esc((lede or why)[:160]),
        esc(url),
        esc(title),
        esc((lede or why)[:160]),
        esc(url),
        MARK,
        esc(url),
        media,
        esc(cat),
        esc(owner),
        esc(added),
        esc(title),
        ('<p class="lede">%s</p>' % esc(lede)) if lede else "",
        tag_html,
        pull,
        limit_sec,
        install_sec,
        esc(cat),
        esc(repo),
        esc(added),
        esc(gh),
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
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(it, prev, nxt))
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


if __name__ == "__main__":
    main()
