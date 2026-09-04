#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重新生成歧义字白名单（审阅记录）。

**先看 check_tw.py 报出来的新增条目再跑这个**——它会把当前 tw/ 里所有上下文
一次性登记成「已审」，没看就跑等于把这道闸关掉。
正常流程：上架新条目 → scouts/tw.py → scouts/check_tw.py 报出新增的几条
→ 人看一眼 → 跑这个。
"""
import os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tw as TW  # noqa: E402
ROOT = os.path.dirname(HERE)
TAG = re.compile(r"<script.*?</script>|<style.*?</style>", re.S)
cnt = collections.Counter()
for dp, dn, fn in os.walk(os.path.join(ROOT, "tw")):
    for f in fn:
        if f not in ("index.html", "404.html"):
            continue
        s = open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read()
        cnt.update(TW.contexts(" ".join(re.findall(r">([^<>]+)<", TAG.sub("", s)))))
p = os.path.join(HERE, "tw_allow.txt")
hdr = ""
if os.path.exists(p):
    hdr = "".join(l for l in open(p, encoding="utf-8") if l.startswith("#"))
if not hdr:
    hdr = ("# 繁体转换里「两种写法都讲得通」的字，逐处登记过的三字上下文。\n"
           "# 这不是词典，是**审阅记录**：每一行表示「这处我看过，是对的」。\n"
           "# 新条目上架会带来新的几条，check_tw.py 会报出来；看完再跑本脚本。\n")
open(p, "w", encoding="utf-8").write(hdr + "\n".join(sorted(cnt)) + "\n")
print("白名单 %d 条 → scouts/tw_allow.txt" % len(cnt))
