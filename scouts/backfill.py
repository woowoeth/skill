#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""存量回填 —— 流扫只看「最新索引」，几天前建的仓永远碰不到，这条补它。

## 量过的事实（2026-09-03）
- 店主指名 14 件里 12 件是 5–35 天前推送的：流扫结构上看不见。
- 代码搜索切不动存量：580 万个 SKILL.md，连 path:skills/ size:3000..3500 都 7.6 万。
- **仓库搜索按创建日切可以**：created:2026-09-02 + skill（名/描述/README）+ ≥3 星 = 126 个，
  验前 40 个：**16 个有 SKILL.md 且从没见过**（含 op7418/guizang-yingzao-skill 55★、
  gozen3ji/consulting-pptx-skill 106★），已知 0 个。40% 命中，全是漏网。

## 边界（不装作没有）
- 依赖「skill」这个词出现在名字/描述/README —— goldie 那类一个 skill 字都没有的仍看不见。
  这条是**补流扫**的，不是替代；两条加起来才接近全。
- ≥3 星是为了省 tree 调用（每个候选一次），不是品味判断。1 星的好货靠流扫（它不看星）。

产出交给 sweep 判品味，不直接上架。
"""
from __future__ import annotations
import json, os, subprocess, sys, time, urllib.parse, datetime, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEEN = os.path.join(ROOT, "editorial", "backfill_seen.json")


def gh(u: str) -> dict:
    r = subprocess.run(["gh", "api", u], capture_output=True)
    try:
        return json.loads(r.stdout.decode("utf-8", "replace"))
    except Exception:
        return {}


def known() -> set[str]:
    k = set()
    for f in glob.glob(os.path.join(ROOT, "skills", "*.json")):
        if f.endswith(("feed.json", "rejected-feed.json")):
            continue
        try:
            k.add((json.load(open(f, encoding="utf-8")).get("repo") or "").lower())
        except Exception:
            pass
    for p in ("editorial/stream_seen.json", "editorial/sweep_seen.json", "editorial/backfill_seen.json"):
        fp = os.path.join(ROOT, p)
        if os.path.exists(fp):
            k |= {x.lower() for x in json.load(open(fp, encoding="utf-8"))}
    try:
        k |= {(e.get("repo") or "").lower()
              for e in json.load(open(os.path.join(ROOT, "editorial", "rejected.json"), encoding="utf-8"))["entries"]}
    except Exception:
        pass
    return k


def main() -> int:
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--days", type=int, default=21)
    ap.add_argument("--from-day", type=int, default=1, help="从几天前开始往回数（默认 1 = 昨天）")
    ap.add_argument("--walk", type=int, default=0, help="游标模式：从 editorial/backfill_cursor.json 记的位置继续往回走 N 天，走到 --max-age 绕回 22 天处")
    ap.add_argument("--max-age", type=int, default=240)
    ap.add_argument("--cjk-or-stars", type=int, default=-1, help="只给「名字/描述含汉字」或「星 ≥ 此值」的仓验树（-1 = 全验）。深回看用 3")
    ap.add_argument("--min-stars", type=int, default=3)
    ap.add_argument("--low-pages", type=int, default=2, help="低星段（0..min_stars-1）每天再搜几页（每页 100）")
    ap.add_argument("--out", default="/tmp/backfill_candidates.json")
    a = ap.parse_args()
    k = known()
    seen = json.load(open(SEEN, encoding="utf-8")) if os.path.exists(SEEN) else {}
    today = datetime.date.today()
    found, checked, nosk = {}, 0, 0
    CURSOR = os.path.join(ROOT, "editorial", "backfill_cursor.json")
    if a.walk:
        # 09-04 漏网回归：店主发现过的 92 件里 21 件一条通道都碰不到，全是建于 3–7 月、低星、一次性作者的中文生活件。
        # 流扫只看新索引、回填只看三周 —— 老仓没人回头看。游标模式每班往回走 N 天，走到 --max-age 绕回来。
        cur = json.load(open(CURSOR, encoding="utf-8")) if os.path.exists(CURSOR) else {"next_day": 22}
        a.from_day = int(cur.get("next_day", 22)); a.days = a.walk
        if a.from_day > a.max_age:
            a.from_day = 22
        print(f"[backfill] 深回看游标：从 {a.from_day} 天前往回走 {a.days} 天")
    _CJK = __import__("re").compile(r"[\u4e00-\u9fff]")
    for d in range(a.from_day, a.from_day + a.days):
        day = (today - datetime.timedelta(days=d)).isoformat()
        q = urllib.parse.quote(f"created:{day} skill in:name,description,readme stars:>={a.min_stars}")
        items = []
        for page in (1, 2, 3):
            r = gh(f"search/repositories?q={q}&sort=stars&order=desc&per_page=100&page={page}")
            it = r.get("items") or []
            items += it
            if len(it) < 100:
                break
            time.sleep(2.2)
        # 09-03 晚：心选 73 件里 12 件不到 3 星 —— 好货常常是零星几颗星，≥3 的门槛把它们筛在门外。
        # 低星段（0–2 星）每天再搜 --low-pages 页全收，不按语言筛（店主：「低星不含汉字也可能有价值」）；验树那步照旧。
        if a.min_stars > 0 and a.low_pages > 0:
            q2 = urllib.parse.quote(f"created:{day} skill in:name,description,readme stars:0..{a.min_stars - 1}")
            for page in range(1, a.low_pages + 1):
                r2 = gh(f"search/repositories?q={q2}&sort=updated&order=desc&per_page=100&page={page}")
                low = r2.get("items") or []
                items += low
                if len(low) < 100:
                    break
                time.sleep(2.2)
        new_day = 0
        for it in items:
            full = it["full_name"]
            if full.lower() in k or full in seen:
                continue
            if a.cjk_or_stars >= 0 and it.get("stargazers_count", 0) < a.cjk_or_stars and not _CJK.search(full + " " + (it.get("description") or "")):
                continue   # 深回看只验树「含汉字或有点星」的，别把 API 配额烧在几万个英文开发件上
            t = gh(f"repos/{full}/git/trees/HEAD?recursive=1")
            paths = [x.get("path", "") for x in (t.get("tree") or [])]
            sk = [p for p in paths if p.endswith("SKILL.md")]
            checked += 1
            seen[full] = {"day": day, "stars": it.get("stargazers_count", 0), "skill_md": len(sk)}
            if sk:
                found[full] = {"via": f"backfill:{day}", "stars": it.get("stargazers_count", 0),
                               "path": os.path.dirname(sorted(sk, key=lambda x: (x.count('/'), len(x)))[0])}
                new_day += 1
            else:
                nosk += 1
            time.sleep(0.4)
        print(f"  {day}  搜到 {len(items):3d} · 验树 {sum(1 for v in seen.values() if v['day']==day):3d} · 有 SKILL.md 且没见过 {new_day:3d}", flush=True)
        time.sleep(2.2)
    if a.walk:
        json.dump({"next_day": a.from_day + a.days, "updated": today.isoformat()}, open(CURSOR, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(seen, open(SEEN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(found, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n{a.days} 天 · 验树 {checked} 个 · 有 SKILL.md 且没见过 **{len(found)}** 个 · 没 SKILL.md {nosk} → {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
