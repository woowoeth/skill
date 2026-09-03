#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""editorial/*.json 冲突时按条目三方合并，不再整份取一侧。

09-03 事故：sweep 在 CI 里 rebase 时 curation.json 冲突，git_sync 按「非生成文件取 theirs」把整份换成
CI 那侧（它 checkout 时还没有我下午写进去的 46 条封面字段）—— 一次 sweep 提交抹掉了全部真图，预览卡回到线上。
规则：以 ours（已在 main 上的）为底，theirs 里**相对 base 改过的键**才盖上去；两侧都改同一键取 theirs
（那是正在重放的提交，通常更新）。顶层非 dict 的键同样按「theirs 改过才盖」处理。
用法：merge_json.py BASE OURS THEIRS OUT
"""
import json, sys

def load(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return {}

def merge(base, ours, theirs):
    if not (isinstance(base, dict) and isinstance(ours, dict) and isinstance(theirs, dict)):
        return theirs if theirs != base else ours
    out = dict(ours)
    for k in set(base) | set(theirs):
        b, t = base.get(k), theirs.get(k)
        if t == b:
            continue                    # theirs 没动这个键 → 留 ours
        if k not in theirs:
            out.pop(k, None); continue  # theirs 删了
        o = ours.get(k)
        if isinstance(t, dict) and isinstance(o, dict):
            out[k] = merge(b if isinstance(b, dict) else {}, o, t)
        else:
            out[k] = t
    return out

if __name__ == "__main__":
    base, ours, theirs, out = sys.argv[1:5]
    m = merge(load(base), load(ours), load(theirs))
    json.dump(m, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[merge_json] 合并 {out}")
