#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""漏网回归：店主标过/指过的每一件，我们的通道现在能不能**自己**找到它。

店主 2026-09-04：「选 skill 要按我的标准来，不能每次我发现的你都不知道」。
把他发现过的每一件当回归用例：把它从参照集里摘掉，问一遍——其余通道有没有一条能捞到它？
  · 时间通道：建仓日在回填窗口内（21 天）→ backfill 能搜到（不看星数了）
  · 同作者：作者名下有别的参照件 → source_refs 作者通道能捞到
  · 相邻仓：别的参照件 README 链到它 → 链接通道
  · 同题材词：仓名/描述里有参照集抽出的题材词 → 词通道
  · 已见过：任何 seen 文件里有它 → 至少进过候选池
一条都没有 = 盲区，红。盲区的共性就是下一条要开的通道。
"""
from __future__ import annotations
import json, os, re, subprocess, sys, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scouts"))
import source_refs as SR


def gh(path):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    try:
        return json.loads(r.stdout) if r.returncode == 0 else {}
    except Exception:
        return {}


def main() -> int:
    feed = {x["id"]: x for x in json.load(open(os.path.join(ROOT, "skills", "feed.json"), encoding="utf-8"))["skills"]}
    hearts = set(json.load(open(os.path.join(ROOT, "editorial", "hearts.json"), encoding="utf-8")).get("ids", []))
    refs = json.load(open(os.path.join(ROOT, "editorial", "taste_refs.json"), encoding="utf-8")).get("items", {})
    # 店主发现的：心选 + 指名（编辑挑的不算，那是我们自己找到的）
    owner = {}
    for i in hearts:
        if i in feed:
            owner[feed[i]["repo"].lower()] = feed[i]["repo"]
    for k, v in refs.items():
        owner[k.lower()] = v.get("repo") or k
    all_refs = SR.refs()
    authors = {}
    for r in all_refs:
        authors.setdefault(r["repo"].split("/")[0].lower(), set()).add(r["repo"].lower())
    terms = set(SR.terms_from(all_refs, 60))
    seen = set()
    for fn in ("stream_seen.json", "sweep_seen.json", "backfill_seen.json", "refs_seen.json", "skillsmp_seen.json"):
        p = os.path.join(ROOT, "editorial", fn)
        if os.path.exists(p):
            d = json.load(open(p, encoding="utf-8"))
            seen |= {x.split("#")[0].split("@")[0].lower() for x in (d if isinstance(d, dict) else [])}
    today = datetime.date.today()
    rows, blind = [], []
    for k, repo in sorted(owner.items()):
        meta = gh(f"repos/{repo}")
        created = (meta.get("created_at") or "")[:10]
        desc = (meta.get("description") or "")
        lanes = []
        if k in seen:
            lanes.append("已见过")
        try:
            age = (today - datetime.date.fromisoformat(created)).days if created else 9999
        except Exception:
            age = 9999
        if age <= 21:
            lanes.append("时间(回填)")
        a = k.split("/")[0]
        if len(authors.get(a, set()) - {k}) > 0:
            lanes.append("同作者")
        blob = (repo.split("/")[-1] + " " + desc).lower()
        hit = [t for t in terms if t in blob]
        if hit:
            lanes.append(f"题材词({hit[0]})")
        rows.append((repo, created, meta.get("stargazers_count", "?"), lanes))
        if not lanes:
            blind.append((repo, created, meta.get("stargazers_count", "?"), desc[:50]))
    print(f"店主发现过的 {len(rows)} 件 · 盲区 {len(blind)} 件")
    from collections import Counter
    c = Counter(l.split("(")[0] for _, _, _, ls in rows for l in ls)
    print("各通道能捞到：", dict(c))
    print("\n盲区（一条通道都碰不到）：")
    for repo, created, stars, desc in blind:
        print(f"  {repo:50s} 建于 {created} ★{stars}  {desc}")
    out = {"at": today.isoformat(), "total": len(rows), "blind": [{"repo": r, "created": c_, "stars": s} for r, c_, s, _ in blind],
           "lanes": {r: ls for r, _, _, ls in rows}}
    json.dump(out, open(os.path.join(ROOT, "editorial", "miss_test.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return 1 if blind else 0


if __name__ == "__main__":
    sys.exit(main())
