#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给封面生成 800px 宽的 WebP 派生图，站上只引派生图。

为什么：卡片封面在手机上显示 177×122，详情页 350×242，而原图中位 1200×600、
平均 788 KB，最大的接近 4 MB。首页一次要下 9.4 MB 图片——首屏卡片是空白的，
读者看到的是一排灰框。800px 宽在 DPR2 下对两处都有余量。

原图留着不动（materials 的凭据），站上引 assets/covers/w800/<stem>.webp；
派生图缺失时前端 onerror 回退原图，所以这一步失败也不会开天窗。

用法：python3 scouts/make_thumbs.py [--all]
默认只处理 skills/feed.json 里在用的本地封面；--all 处理 assets/covers 下全部。
"""
import json, os, sys, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "covers"
OUT = SRC / "w800"
MAXW = 800
Q = 80


def wanted():
    if "--all" in sys.argv:
        return sorted(p for p in SRC.iterdir() if p.is_file())
    feed = json.load(open(ROOT / "skills" / "feed.json", encoding="utf-8"))
    out = []
    for it in feed.get("skills", []):
        c = (it.get("cover") or "").strip()
        if not c:
            continue
        c = c[len("/skill/"):] if c.startswith("/skill/") else c
        p = ROOT / c
        if p.is_file() and p.parent == SRC:
            out.append(p)
    return sorted(set(out))


def main():
    OUT.mkdir(exist_ok=True)
    src_tot = out_tot = 0
    n = skipped = 0
    for p in wanted():
        dst = OUT / (p.stem + ".webp")
        src_tot += p.stat().st_size
        if dst.exists() and dst.stat().st_mtime >= p.stat().st_mtime:
            out_tot += dst.stat().st_size; skipped += 1; continue
        try:
            im = Image.open(p)
            im.load()
        except Exception as e:
            print("  跳过（打不开）:", p.name, str(e)[:40]); continue
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA" if "A" in im.mode or im.mode == "P" else "RGB")
        if im.width > MAXW:
            im = im.resize((MAXW, max(1, round(im.height * MAXW / im.width))), Image.LANCZOS)
        im.save(dst, "WEBP", quality=Q, method=6)
        out_tot += dst.stat().st_size
        n += 1
    print("生成 %d 张（跳过已是最新的 %d 张）" % (n, skipped))
    print("原图 %.1f MB → 派生 %.1f MB（%.0f%%）" % (
        src_tot / 1048576, out_tot / 1048576, 100 * out_tot / max(1, src_tot)))


if __name__ == "__main__":
    main()
