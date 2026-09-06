# -*- coding: utf-8 -*-
"""封面改完之后的收口，**顺序不能反**：先重建 feed，再出派生图。

    python3 scouts/covers_publish.py

2026-09-06 踩的坑：make_thumbs.wanted() 读的是 skills/feed.json 里在用的封面路径。
我先跑了 make_thumbs 再跑 refresh —— 派生图按**旧** feed 出的，新 feed 指向的 155 张
封面在 w800/ 里根本没有。线上每张卡先请求 w800/*.webp 撞 404，再 onerror 回退原图：
首屏一排灰框、几百个 404、原图 800KB 一张地下。店主看到的「图打不开」多半就是这个。

所以收口只做两步、只按这个顺序：refresh() → make_thumbs。任何改了 editorial/curation.json
里 cover 的脚本（apply_cover_verdicts / make_specimens / repo_covers）跑完都该接这一步。
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)


def main():
    import scout_lib as lib
    lib.refresh()                                   # ① feed 成为唯一真相
    r = subprocess.run([sys.executable, os.path.join(HERE, "make_thumbs.py")], cwd=ROOT)   # ② 按 feed 出派生图
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
