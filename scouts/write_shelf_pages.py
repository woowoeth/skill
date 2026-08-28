#!/usr/bin/env python3
"""Write a readable /i/<id>/ page for every item currently on the shelf."""
from __future__ import annotations
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED = os.path.join(ROOT, "skills", "feed.json")
OUT = os.path.join(ROOT, "i")
CAT = {
    "creative": "做图", "fun": "玩", "writing": "写文章", "life": "过日子",
    "body": "养身体", "work": "上班用", "learn": "学东西", "dev": "做图",
    "meta": "店长位",
}

CSS = """
:root{--bg:#e7ece8;--card:#f6f8f6;--ink:#16201b;--ink-2:#3d4a43;--ink-3:#5e6e66;
  --line:#cfd8d2;--accent:#2d6a4f;--serif:'Songti SC','Source Han Serif SC','Noto Serif CJK SC',Georgia,serif;
  --sans:-apple-system,BlinkMacSystemFont,'PingFang SC',system-ui,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.7 var(--sans)}
a{color:inherit}.wrap{max-width:720px;margin:0 auto;padding:28px 20px 72px}
.top{display:flex;align-items:baseline;gap:12px;margin-bottom:28px}
.top b{font:600 28px/1 var(--serif)}.top i{font:16px/1 var(--serif);font-style:normal;color:var(--ink-3)}
.top a.back{margin-left:auto;font-size:13px;color:var(--ink-3);text-decoration:none}
.plate{aspect-ratio:16/10;border-radius:14px;padding:22px 20px;display:flex;flex-direction:column;justify-content:flex-end;
  background:radial-gradient(120% 80% at 100% 0%,rgba(45,106,79,.18),transparent 55%),
             linear-gradient(165deg,#d7e0d9,#c5d1c8 60%,#b4c2b8);margin:0 0 22px}
.plate .c{font:600 11px/1 var(--sans);letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);margin-bottom:10px}
.plate .t{font:600 22px/1.3 var(--serif)}
.cover{width:100%;border-radius:14px;margin:0 0 22px;display:block}
h1{font:600 28px/1.3 var(--serif);margin:0 0 12px}
.why,.limit{margin:0 0 16px;color:var(--ink-2)}
.limit{padding-top:14px;border-top:1px solid var(--line);color:var(--ink-3);font-size:14px}
.cmds{margin:22px 0;display:grid;gap:8px}
.cmd{font:13px/1.5 ui-monospace,Menlo,monospace;background:var(--card);border:1px solid var(--line);
  border-radius:10px;padding:10px 12px;overflow:auto}
.row{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0 0}
.row button,.row a{border:1px solid var(--line);background:var(--card);border-radius:999px;
  padding:7px 12px;font:600 12px/1 var(--sans);text-decoration:none;cursor:pointer;color:var(--ink-2)}
"""

def esc(s):
    return html.escape(s or "", quote=True)

def page(it):
    title = it.get("title_zh") or it.get("name") or it["id"]
    cat = CAT.get(it.get("category") or "", it.get("category") or "")
    cover = it.get("cover") or ""
    why = it.get("why_zh") or it.get("tagline_zh") or ""
    limit = it.get("limit_zh") or ""
    ins = it.get("install") or {}
    cmds = [ins.get("clone"), ins.get("copy")]
    url = f"https://ourword.ai/skill/i/{it['id']}/"
    media = (f'<img class="cover" src="{esc(cover)}" alt="">'
             if cover else
             f'<div class="plate"><div class="c">{esc(cat)}</div><div class="t">{esc(title)}</div></div>')
    cmd_html = "".join(f'<div class="cmd">{esc(c)}</div>' for c in cmds if c)
    gh = it.get("url") or f"https://github.com/{it.get('repo','')}"
    return f"""<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} — 品味</title>
<link rel="canonical" href="{esc(url)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(why[:120])}">
<meta property="og:url" content="{esc(url)}">
<style>{CSS}</style>
</head><body><div class="wrap">
<div class="top"><a href="../../"><b>品味</b></a><i>帮你发现有品位的 Skills</i>
<a class="back" href="../../">← 货架</a></div>
{media}
<h1>{esc(title)}</h1>
<p class="why">{esc(why)}</p>
<p class="limit">{esc(limit)}</p>
<div class="cmds">{cmd_html}</div>
<div class="row">
<button type="button" id="share">分享</button>
<a href="{esc(gh)}" rel="noopener">仓库</a>
</div>
</div>
<script>
var u={json.dumps(url)};
document.getElementById('share').onclick=function(){{
  var b=this, old=b.textContent;
  function ok(){{b.textContent='已复制链接';setTimeout(function(){{b.textContent=old}},1400)}}
  if(navigator.clipboard) navigator.clipboard.writeText(u).then(ok,ok); else ok();
}};
</script>
</body></html>
"""

def main():
    feed = json.load(open(FEED, encoding="utf-8"))
    n = 0
    for it in feed.get("skills") or []:
        if it.get("hide"):
            continue
        d = os.path.join(OUT, it["id"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(it))
        n += 1
    print(f"[pages] wrote {n} shelf pages under i/")

if __name__ == "__main__":
    main()
