# -*- coding: utf-8 -*-
"""把判官的封面判决写进 editorial/curation.json。

    python3 scouts/apply_cover_verdicts.py <judge_out_*.json ...>

判决三种（标准见 docs/COVERS.md）：
  ok       图对得上技能 → cover_verdict=ok
  replace  技能行、图不行 → cover_verdict=replace（图先留着，等换；货架体检会把它算成坏）
  remove   封面是二维码/广告 → hide=true 下架，并把 cover 置空

为什么写进 curation.json 而不是 skills/*.json：curation 是覆盖层，
scout_lib.refresh() 重建 feed 时它永远赢；写进 skills/*.json 的会被下一轮抓取覆盖。
"""
import io, json, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUR = os.path.join(ROOT, "editorial", "curation.json")


def main(paths):
    cur = json.load(io.open(CUR, encoding="utf-8"))
    items = cur.setdefault("items", {})
    today = datetime.date.today().isoformat()
    n = {"ok": 0, "replace": 0, "remove": 0}
    for p in paths:
        for v in json.load(io.open(p, encoding="utf-8")):
            sid, verdict = v["id"], v["verdict"]
            if verdict not in n:
                print("跳过未知判决", sid, verdict); continue
            e = items.setdefault(sid, {})
            e["cover_verdict"] = verdict
            e["cover_verdict_why"] = v.get("why", "")
            e["cover_kind_seen"] = v.get("kind_seen", "")
            e["cover_judged_at"] = today
            if verdict == "remove":
                e["hide"] = True
                e["hide_why"] = "封面是二维码/广告：" + v.get("why", "")
                e["cover"] = ""
            n[verdict] += 1
    io.open(CUR, "w", encoding="utf-8").write(json.dumps(cur, ensure_ascii=False, indent=1))
    print("写入 curation.json：ok %d · replace %d · remove %d（已下架）" % (n["ok"], n["replace"], n["remove"]))


if __name__ == "__main__":
    main(sys.argv[1:])
