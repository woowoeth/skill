#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""skillsmp.com 当进货口。店主 2026-09-03：「这个网站也全扫一遍，看看有什么值得加」。

## 它给什么、不给什么（openapi.json 量过）
- 只有一个接口 GET /api/v1/skills/search，**q 必填** —— 没有「列出全部」，只能按关键词捞。
- limit ≤ 50，sortBy ∈ {stars, recent}，language 可筛（zh / en …）。
- 匿名 50 次/天，且实测每分钟约 10 次就 429 —— 请求间隔要 ≥7s。号称 2,000,000+ 个 skill —— 「全扫」在这个接口上不成立，
  能做的是：一组宽泛关键词 × {recent, stars} × {zh, en}，去重成 owner/repo，和已知集合比。
- 返回里 githubUrl 常带 /tree/main/… 子路径（一个仓多条），要归并到仓。
- 注意 stars 字段是**仓的星**（affaan-m/ECC 244512★ 下面挂几十条同星记录），不是 skill 的热度。

预算：每班跑一组（≈12 次请求），五班合计 ≈ 48 次 < 50。产出交给 sweep 判品味，不直接上架。
"""
from __future__ import annotations
import json, os, sys, time, glob, urllib.parse, urllib.request, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEEN = os.path.join(ROOT, "editorial", "skillsmp_seen.json")
API = "https://skillsmp.com/api/v1/skills/search"

# 宽泛关键词，不是题材白名单：目的是覆盖，不是筛口味（题材白名单 08-31 已证伪 +1pt）
QUERIES = ["skill", "workflow", "generate", "写", "生成", "照片", "视频", "文档", "分析", "设计", "海报", "prompt"]


def known() -> set[str]:
    k = set()
    for f in glob.glob(os.path.join(ROOT, "skills", "*.json")):
        if f.endswith(("feed.json", "rejected-feed.json")): continue
        try: k.add((json.load(open(f, encoding="utf-8")).get("repo") or "").lower())
        except Exception: pass
    for p in ("editorial/stream_seen.json", "editorial/sweep_seen.json", "editorial/backfill_seen.json", "editorial/skillsmp_seen.json"):
        fp = os.path.join(ROOT, p)
        if os.path.exists(fp): k |= {x.lower() for x in json.load(open(fp, encoding="utf-8"))}
    try: k |= {(e.get("repo") or "").lower() for e in json.load(open(os.path.join(ROOT, "editorial", "rejected.json"), encoding="utf-8"))["entries"]}
    except Exception: pass
    return k


def repo_of(url: str) -> str:
    m = re.match(r"https?://github\.com/([^/\s]+/[^/\s#?]+)", url or "")
    return m.group(1).rstrip(".git") if m else ""


def fetch(q: str, sort: str, lang: str, limit: int = 50) -> list[dict]:
    u = f"{API}?" + urllib.parse.urlencode({"q": q, "sortBy": sort, "language": lang, "limit": limit})
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "pinwei-scout"}), timeout=30) as r:
            d = json.loads(r.read())
        data = d.get("data") or {}
        return data.get("skills") if isinstance(data, dict) else (data or [])
    except Exception as e:
        print(f"  ! {q}/{sort}/{lang}: {type(e).__name__} {str(e)[:60]}")
        return []


def main() -> int:
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--shard", type=int, default=0, help="第几班（0-4），每班跑 QUERIES 的一段，凑不满 50 次/天")
    ap.add_argument("--langs", default="zh,en")
    ap.add_argument("--out", default="/tmp/skillsmp_candidates.json")
    a = ap.parse_args()
    k = known()
    seen = json.load(open(SEEN, encoding="utf-8")) if os.path.exists(SEEN) else {}
    per = max(1, len(QUERIES) // 5 + 1)
    qs = QUERIES[a.shard * per:(a.shard + 1) * per] if 0 <= a.shard < 5 else QUERIES
    found, req = {}, 0
    for q in qs:
        for sort in ("recent", "stars"):
            for lang in a.langs.split(","):
                items = fetch(q, sort, lang); req += 1
                for it in items:
                    repo = repo_of(it.get("githubUrl", ""))
                    if not repo or repo.lower() in k or repo in found: continue
                    found[repo] = {"via": f"skillsmp:{q}/{sort}/{lang}", "stars": int(it.get("stars") or 0),
                                   "name": it.get("name"), "path": ""}
                    seen[repo] = {"first_seen": time.strftime("%Y-%m-%d"), "q": q}
                time.sleep(7)     # 实测 1.2s 间隔第 10 次就 429：匿名不是只有日限，还有分钟级限
    json.dump(seen, open(SEEN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(found, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"skillsmp 第 {a.shard} 班：{len(qs)} 个词 × 2 排序 × {len(a.langs.split(','))} 语言 = {req} 次请求 · 没见过的仓 {len(found)} 个 → {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
