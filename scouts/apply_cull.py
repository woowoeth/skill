# -*- coding: utf-8 -*-
"""把「三问」复审的下架判决写进 editorial/curation.json。

    python3 scouts/apply_cull.py <cull_out.json>

输入是复审员按 docs/CURATION.md 三问逐件判的结果：
  {"id": ..., "verdict": "keep|remove", "which": 1|2|3|0, "why": "..."}

remove → hide=true，并记下是哪一问没过、为什么、何时。keep 不写任何东西
（不留「keep」标记 —— 上架是默认状态，不需要盖章；只有下架需要留痕）。

两道保险：
  · pick 为 true 的（店主亲手挑的）跳过，哪怕复审员判了 remove —— 店主的判断赢。
  · 已经 hide 的不重复写。

写进 curation.json 而不是 skills/*.json：curation 是覆盖层，重建 feed 时永远赢。
"""
import datetime
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUR = os.path.join(ROOT, "editorial", "curation.json")
FEED = os.path.join(ROOT, "skills", "feed.json")
Q = {1: "问一·不是拿走就能用的商品", 2: "问二·别处也拿得到", 3: "问三·写不出让人想装的文案"}


def main(path):
    verdicts = json.load(io.open(path, encoding="utf-8"))
    feed = {x["id"]: x for x in json.load(io.open(FEED, encoding="utf-8"))["skills"]}
    cur = json.load(io.open(CUR, encoding="utf-8"))
    items = cur.setdefault("items", {})
    today = datetime.date.today().isoformat()
    n_rm = n_skip_pick = n_keep = 0
    for v in verdicts:
        sid = v["id"]
        if v.get("verdict") != "remove":
            n_keep += 1
            continue
        if (feed.get(sid) or {}).get("pick") or (items.get(sid) or {}).get("pick"):
            n_skip_pick += 1
            print("  跳过（店主精选）：", sid)
            continue
        e = items.setdefault(sid, {})
        if e.get("hide"):
            continue
        e["hide"] = True
        e["hide_why"] = "%s：%s" % (Q.get(v.get("which"), "三问未过"), v.get("why", ""))
        e["culled_at"] = today
        n_rm += 1
    io.open(CUR, "w", encoding="utf-8").write(json.dumps(cur, ensure_ascii=False, indent=1))
    print("下架 %d · 保留 %d · 精选免检 %d" % (n_rm, n_keep, n_skip_pick))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
