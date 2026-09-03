#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把某条提交里 curation.json 的封面字段抄回当前 curation.json（CI 整份覆盖后的补救，可重复跑）。
用法：restore_cover_fields.py <commit>
只抄 cover / cover_kind / cover_w / cover_h / cover_src / cover_real / cover_note，
且只抄那条提交里「有 cover_src（真图）」或「cover_kind=none 且 cover 为空（明确下卡）」的条目。"""
import json, subprocess, sys
F = ("cover", "cover_kind", "cover_w", "cover_h", "cover_src", "cover_real", "cover_note")
commit = sys.argv[1]
old = json.loads(subprocess.check_output(["git", "show", f"{commit}:editorial/curation.json"]))["items"]
cur = json.load(open("editorial/curation.json", encoding="utf-8"))
n = 0
for k, v in old.items():
    if v.get("cover_src") or (v.get("cover_kind") == "none" and v.get("cover") == ""):
        e = cur["items"].setdefault(k, {})
        before = {f: e.get(f) for f in F}
        for f in F:
            if f in v: e[f] = v[f]
            else: e.pop(f, None)
        if before != {f: e.get(f) for f in F}: n += 1
json.dump(cur, open("editorial/curation.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"[restore] 从 {commit[:9]} 抄回 {n} 条封面字段")
