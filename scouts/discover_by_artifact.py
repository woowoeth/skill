#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按「它是不是一件 skill」找货，而不是按「它是什么题材」猜。

## 为什么有这个

2026-09-02 店主拿三个仓来问「为什么我们网站没有这些」。查下来：
两个**从来没进过库**，连候选都不是。

原因在进货口。SEARCH_QUERIES 十一条，条条是题材词：
    poster OR collage OR halftone OR risograph
    插画 OR 海报 OR 手绘 OR 水彩 OR 剪纸
    中医 OR 倪海厦 · 八字 OR 周易 · 育儿 OR 养猫 …
**那就是 TASTE_RE 那张白名单** —— 我在 08-31 拿店主的 73 件心选证伪过它
（通过率 33%，非心选 32%，+1pt，等于没有区分力），把它从**门闸**里拿掉了，
却留着它当**进货口**，还专门写了一句「这条我先标出来，没动」，然后没回来。

`touchine-ojo/OJO-Design-Skills` 的描述是
「Reusable UI/UX design skills for AI coding agents」——
不含任何一个题材词，**我们的任何一条查询都不可能返回它**。
实测：题材查询前 30 没有它；通用查询前 30 也没有它（65 星，挤不进去）；
只有精确搜仓名才找得到。**它不是被判掉的，是结构上看不见。**

## 换的思路

skill 的定义特征是**仓里有 SKILL.md**，不是它画水彩还是算八字。
所以用 GitHub 代码搜索按 `filename:SKILL.md` 枚举，切片取量，
按仓去重，交给既有管线（验 SKILL.md → 文案门闸 → 红线扫描）。
实测 `filename:SKILL.md repo:touchine-ojo/OJO-Design-Skills` → 命中 1 条，
这条路够得着它。

**题材词不是删掉，是降级**：它仍然可以当「优先看哪些」的排序信号，
但不该再当「能不能被看见」的开关。
"""
from __future__ import annotations
import json, os, subprocess, sys, time, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 切片：GitHub 代码搜索单查询最多回 1000 条，所以用互不相同的第二关键词切开。
# 这些词**不是题材**，是 SKILL.md 里普遍会出现的结构性字段和常见动词 ——
# 目的是覆盖面，不是筛口味。
SLICES = [
    "user-invocable", "allowed-tools", "license", "trigger", "workflow",
    "output", "checklist", "template", "reference", "example",
    "install", "usage", "prompt", "agent", "codex",
]


def gh(url: str) -> dict:
    r = subprocess.run(["gh", "api", url], capture_output=True)
    if r.returncode:
        return {}
    try:
        return json.loads(r.stdout.decode("utf-8", "replace"))
    except Exception:
        return {}


def known_repos() -> set[str]:
    out = set()
    import glob
    for f in glob.glob(os.path.join(ROOT, "skills", "*.json")):
        if f.endswith(("feed.json", "rejected-feed.json")):
            continue
        try:
            out.add((json.load(open(f, encoding="utf-8")).get("repo") or "").lower())
        except Exception:
            pass
    try:
        for e in json.load(open(os.path.join(ROOT, "editorial", "rejected.json"),
                               encoding="utf-8"))["entries"]:
            out.add((e.get("repo") or "").lower())
    except Exception:
        pass
    return out


def main() -> int:
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--pages", type=int, default=2, help="每个切片翻几页（每页 100）")
    ap.add_argument("--out", default="/tmp/artifact_candidates.json")
    a = ap.parse_args()

    seen = known_repos()
    print(f"已知仓 {len(seen)} 个（含拒收榜）—— 只报没见过的\n")
    found: dict[str, dict] = {}
    for term in SLICES:
        q = urllib.parse.quote(f'filename:SKILL.md "{term}"')
        new_here = 0
        for page in range(1, a.pages + 1):
            d = gh(f"search/code?q={q}&per_page=100&page={page}")
            items = d.get("items") or []
            if not items:
                break
            for it in items:
                full = (it.get("repository") or {}).get("full_name") or ""
                if not full or full.lower() in seen or full in found:
                    continue
                found[full] = {"via": term}
                new_here += 1
            time.sleep(2)          # 代码搜索限频比 REST 严，慢一点换稳
        print(f"  {term:<16} 新增 {new_here:3d}  （累计 {len(found)}）")
    json.dump(found, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n没见过的仓 {len(found)} 个 → {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
