#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把「店主认过的货」（心选 + 钉住的推荐 + 店主指名）写成一页简报 docs/HEARTS.md，给读原文的代理当「有品味」的定义。
scratchpad 会被清掉（09-07 cocoloop 那批代理找不到 hearts_brief.md），所以放仓里，每次 refresh 后重生成也不贵。"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
feed = {x["id"]: x for x in json.load(open(os.path.join(ROOT, "skills", "feed.json"), encoding="utf-8"))["skills"]}
hearts = json.load(open(os.path.join(ROOT, "editorial", "hearts.json"), encoding="utf-8")).get("ids", [])
pinned = json.load(open(os.path.join(ROOT, "editorial", "picks_pinned.json"), encoding="utf-8")).get("ids", [])
refs = json.load(open(os.path.join(ROOT, "editorial", "taste_refs.json"), encoding="utf-8")).get("items", {})
lines = ["# 店主认过的货（读原文挑货时，「有品味」就是这个意思）", "", "格式：分类 | 标题 | 一句点评 | 仓库。三段：心选（店主亲手标 ❤）、店长推荐里钉住的、店主指名的。", ""]
def row(x): return f"- {x.get('category')} | {x.get('title_zh')} | {(x.get('why_zh') or x.get('tagline_zh') or '')[:70]} | {x.get('repo')}"
lines += ["## 心选", ""] + [row(feed[i]) for i in hearts if i in feed] + ["", "## 店长推荐（钉住）", ""] + [row(feed[i]) for i in pinned if i in feed and i not in hearts]
lines += ["", "## 店主指名（可能还没上架）", ""] + [f"- {v.get('repo') or k}  {('· ' + v.get('note', ''))[:80]}" for k, v in refs.items()]
open(os.path.join(ROOT, "docs", "HEARTS.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(f"docs/HEARTS.md：心选 {sum(1 for i in hearts if i in feed)} · 钉住 {sum(1 for i in pinned if i in feed and i not in hearts)} · 指名 {len(refs)}")
