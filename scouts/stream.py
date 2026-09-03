#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每天把 GitHub 新出的 SKILL.md **全部**过一遍 —— 流式，不抽样，能证明没断口。

## 为什么不是「再多翻几页」

2026-09-02 量的：filename:SKILL.md 按索引时间倒序翻满 1000 条上限（779 个不同仓），
**99% 没见过，且完全没碰到已知的边** —— 每天新索引的 SKILL.md 超过 1000 个文件，
一条查询覆盖不了一天。之前每轮翻 1 页，是在一条河里舀一勺。
店主：「不然无论如何你都会错过一些优质的 skill」。对：**只要是抽样就一定漏。**

## 怎么做到「全」

代码搜索单查询最多 1000 条。所以按路径切片，每片各 1000：
    path:skills/  ·  path:.claude/  ·  path:.agents/  ·  path:plugins/  ·  其余
每片按 indexed 倒序，从最新往回读。

## 怎么证明「没断口」——高水位法

代码搜索不给时间戳，所以不能按日期证明。用**续接**证明：
每片从最新往回读，**直到碰上上一轮已经见过的仓**为止。
  · 碰到了      → 这一片从上一轮到现在连上了，没断
  · 翻满还没碰到 → 这一片有断口（新量超过 1000），**红灯**，不许静默
第一次跑没有上一轮，所有片都会报「无锚点」——那不是断口，是起点。

每个仓记首次见到的日期。店主再指一个没收的，一查 stream_seen 就知道：
在 → 捞到了但判低了（判官的事）；不在 → 没捞到（覆盖的事）。两件事修法不同。

## 它不做的

不判品味、不写文案、不上架。只负责「一个都不漏地看见」。
判和上架交给 sweep.py 和既有管线。
"""
from __future__ import annotations
import json, os, subprocess, sys, time, urllib.parse, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEEN = os.path.join(ROOT, "editorial", "stream_seen.json")
COV = os.path.join(ROOT, "editorial", "coverage_log.json")

SLICES = [
    ("skills",  'filename:SKILL.md path:skills/'),
    ("claude",  'filename:SKILL.md path:.claude/'),
    ("agents",  'filename:SKILL.md path:.agents/'),
    ("plugins", 'filename:SKILL.md path:plugins/'),
    ("rest",    'filename:SKILL.md -path:skills/ -path:.claude/ -path:.agents/ -path:plugins/'),
]
PAGES = 10          # 每片上限 10×100 = 1000
SLEEP = 6.5         # 代码搜索 10 次/分钟


def gh(url: str) -> dict:
    r = subprocess.run(["gh", "api", url], capture_output=True)
    try:
        return json.loads(r.stdout.decode("utf-8", "replace"))
    except Exception:
        return {}


def main() -> int:
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--pages", type=int, default=PAGES)
    ap.add_argument("--out", default="/tmp/stream_new.json", help="本轮新见的仓，交给 sweep 判")
    a = ap.parse_args()

    seen = json.load(open(SEEN, encoding="utf-8")) if os.path.exists(SEEN) else {}
    prev_run = {k for k, v in seen.items() if v.get("last_run")}   # 上一轮见过的 = 锚点
    today = datetime.date.today().isoformat()
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    print(f"已见 {len(seen)} 个仓 · 上一轮锚点 {len(prev_run)} 个\n")

    new_total, report, touched = {}, [], set()
    for name, q in SLICES:
        qq = urllib.parse.quote(q)
        new_here, anchored, pages_used, hits = 0, False, 0, 0
        unreadable = ""
        for page in range(1, a.pages + 1):
            d, items = {}, []
            for attempt in range(3):                     # 空页/限频重试三次，退避
                d = gh(f"search/code?q={qq}&sort=indexed&order=desc&per_page=100&page={page}")
                items = d.get("items") or []
                if items or d.get("total_count") == 0:
                    break
                time.sleep(SLEEP * (attempt + 2))
            pages_used = page
            if not items:
                if page == 1:
                    # **这不是断口，是读不到。** 2026-09-03 CI 首轮：skills 片第 1 页就连上，
                    # 随后四片「翻 1 页 · 0 条」被我报成了断口 —— 其实是 skills 片没歇就接着
                    # 打下一片，撞了二级限频，API 回的是错误不是空结果。
                    # 断口 = 读满 10 页没碰到锚点；读不到 = API 没给数据。两个都要红，但原因不同。
                    unreadable = str(d.get("message") or "空响应")[:80]
                    print(f"  {name:<8} 读不到：{unreadable}")
                break
            for it in items:
                hits += 1
                full = (it.get("repository") or {}).get("full_name") or ""
                if not full:
                    continue
                touched.add(full)
                if full in prev_run:
                    anchored = True            # 碰到上一轮的边了
                if full not in seen:
                    seen[full] = {"first_seen": today, "slice": name,
                                  "path": it.get("path", "")}
                    new_total[full] = seen[full]
                    new_here += 1
            if anchored:
                break
            time.sleep(SLEEP)
        if unreadable:
            status = "**读不到**"
        elif not prev_run:
            status = "无锚点（首轮）"
        else:
            status = "连上" if anchored else "**断口**"
        time.sleep(SLEEP)                                # 片与片之间也歇，别撞二级限频
        report.append({"slice": name, "pages": pages_used, "hits": hits,
                       "new": new_here, "status": status})
        print(f"  {name:<8} 翻 {pages_used:>2} 页 · {hits:>4} 条 · 新 {new_here:>3} · {status}")

    # 下一轮的锚点 = 本轮真正读到的仓。旧锚点不再刷新，自然退出，锚点集才会往前走。
    for v in seen.values():
        v.pop("last_run", None)
    for full in touched:
        if full in seen:
            seen[full]["last_run"] = now
    json.dump(seen, open(SEEN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(new_total, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    gaps = [r["slice"] for r in report if r["status"] == "**断口**"]
    unread = [r["slice"] for r in report if r["status"] == "**读不到**"]
    cov = json.load(open(COV, encoding="utf-8")) if os.path.exists(COV) else {
        "_说明": "每轮流式全扫的覆盖账：每片翻了几页、新见几个、有没有连上上一轮。"
                "「断口」= 翻满上限还没碰到上一轮的边，那一片这一天没扫全 —— 必须红。",
        "runs": []}
    cov["runs"].insert(0, {"time": now, "new": len(new_total), "seen_total": len(seen),
                           "slices": report, "gaps": gaps, "unreadable": unread})
    cov["runs"] = cov["runs"][:60]
    json.dump(cov, open(COV, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"\n本轮新见 {len(new_total)} 个仓 → {a.out}")
    print(f"覆盖账 editorial/coverage_log.json · 累计见过 {len(seen)} 个")
    rc = 0
    if unread:
        print(f"\n::error::读不到的片：{', '.join(unread)} —— API 没给数据（多半是限频），"
              f"这些片这一轮**没看**。不是断口，是没读到；重跑即可。")
        rc = 1
    if gaps:
        print(f"\n::error::有断口的片：{', '.join(gaps)} —— 翻满 {a.pages} 页还没碰到上一轮的边，"
              f"这一天这些片**没扫全**。要么加密度（每天跑两次），要么再切。")
        rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
