#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""封面文件和记录对账并修复：文件不存在 / 尺寸和记录不符（多半是被 CI 用 OG 预览卡同名覆盖了）。
- 有 cover_src 的（repo_covers 取的真图）：从 cover_src 重新下载，记录改成实际尺寸；下不到就下卡。
- 没 cover_src 的：文件是 1200×600/630（预览卡）或小于 300 宽（图标）→ 下卡；否则记录改成实际尺寸。"""
import json, os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skill_scout as S, repo_covers as R
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
f = json.load(open(os.path.join(ROOT, "skills", "feed.json"), encoding="utf-8"))["skills"]
cur = json.load(open(os.path.join(ROOT, "editorial", "curation.json"), encoding="utf-8"))
fixed = down = 0
for x in f:
    u = x.get("cover") or ""
    if not u.startswith("/skill/"):
        continue
    p = os.path.join(ROOT, u.replace("/skill/", "", 1))
    if not os.path.exists(p):
        # 同 id 换过后缀（PNG→JPEG 压缩）而记录没跟上：先找兄弟文件
        alts = [q for q in glob.glob(os.path.join(ROOT, "assets", "covers", x["id"] + ".*")) if os.path.getsize(q) > 20000]
        if alts:
            p = alts[0]; e = cur["items"].setdefault(x["id"], {}); e["cover"] = "/skill/" + os.path.relpath(p, ROOT)
            print(f"  ~ 换后缀 {x['id'][:44]:44s} → {os.path.basename(p)}")
    real = S.cover_dims(p) if os.path.exists(p) else None
    if real and (real[0], real[1]) == (x.get("cover_w"), x.get("cover_h")):
        continue
    e = cur["items"].setdefault(x["id"], {})
    src = e.get("cover_src")
    ok = R.try_download(x["id"], [src]) if src else None
    if ok:
        _, out, (w, h) = ok
        e.update({"cover": "/skill/" + os.path.relpath(out, ROOT), "cover_w": w, "cover_h": h}); fixed += 1
        print(f"  ↻ 重下 {x['id'][:44]:44s} {w}x{h}")
    elif real and real not in ((1200, 600), (1200, 630)) and real[0] >= 300 and not src:
        e.update({"cover_w": real[0], "cover_h": real[1]}); fixed += 1
        print(f"  = 改记录 {x['id'][:44]:44s} {x.get('cover_w')}x{x.get('cover_h')} → {real[0]}x{real[1]}")
    else:
        e.update({"cover": "", "cover_kind": "none"}); down += 1
        for k in ("cover_w", "cover_h", "cover_src", "cover_real"): e.pop(k, None)
        e["cover_note"] = f"09-03 对账：文件{'不存在' if not real else f'是 {real[0]}x{real[1]}'}，和记录不符且拿不回真图，下卡"
        print(f"  ✗ 下卡 {x['id'][:44]:44s} {e['cover_note'][-30:]}")
json.dump(cur, open(os.path.join(ROOT, "editorial", "curation.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"修 {fixed} · 下卡 {down}")
