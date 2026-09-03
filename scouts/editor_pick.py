#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把编辑读过原文挑的货登记到 editorial/editor_picks.json，并打印可以直接交给 --suggest 的仓库列表。
用法：editor_pick.py picks.json   （[{repo, path, reason, note}]，reason ≥30 字否则拒登）
"""
import json, os, sys, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "editorial", "editor_picks.json")
d = json.load(open(P, encoding="utf-8")) if os.path.exists(P) else {"items": {}}
items = d.setdefault("items", {})
new = json.load(open(sys.argv[1], encoding="utf-8"))
today = datetime.date.today().isoformat()
ok, bad = [], []
for x in new:
    r = (x.get("reason") or "").strip()
    if len(r) < 30:
        bad.append((x["repo"], len(r))); continue
    k = x["repo"].lower()
    items[k] = {"repo": x["repo"], "path": x.get("path", ""), "paths": x.get("paths", []), "reason": r, "note": x.get("note", ""), "picked_at": today, "by": "编辑（Claude）读原文"}
    ok.append(x["repo"])
json.dump(d, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"登记 {len(ok)} 件；理由不足 30 字拒登 {len(bad)}：{bad}")
print("交给管线：", " ".join(ok))
