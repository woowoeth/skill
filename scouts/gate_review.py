#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""看门闸的判决，找出「修哪一处能放行最多的好货」。

## 为什么有这个

2026-09-02 店主：「你要根据过不过的原因来优化的」。
门闸每轮都把为什么过、为什么不过写进 editorial/gate_log.json —— 那不是终点，是信号。

**每一类不过，对应的修法是不一样的，而且大多数不是「把门槛调低」：**

  文案不齐：缺 limit_zh      → 修**提示词**（模型没产出这个字段），不是降门槛
  文案不齐：太短 xxx         → 修 _clamp_patch 的下限或提示词的字数要求
  局限只有 N 字（要 ≥20）     → 提示词里局限的写法示例不够具体
  品味判不了：没有上游正文     → 修**抓取**（判之前先把 SKILL.md 存下来），不是放行
  品味判不了：判官不通         → 修 secrets / 端点
  品味 N 分 < 60             → 这才是真的「它不够好」——**唯一不该动机制的一类**

把「本来能过、卡在我们自己没做好的事情上」和「它确实不够好」分开，
是这个脚本存在的全部理由。第一类每多一件，都是我们在自己挡自己的货。
"""
from __future__ import annotations
import json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "editorial", "gate_log.json")

# 归类 → (是不是我们自己的问题, 该修哪里)
KINDS = [
    (re.compile(r"文案不齐：缺"),        True,  "enrich 提示词没产出这个字段 → 改 ENRICH_PROMPT 的键清单/写法"),
    (re.compile(r"文案不齐：太短"),      True,  "模型产出太短 → 改提示词字数要求，或 _clamp_patch 加下限"),
    (re.compile(r"局限只有 \d+ 字"),     True,  "局限写得太薄 → 提示词里补更具体的正反例"),
    (re.compile(r"品味判不了.*没有上游正文"), True, "判之前没把 SKILL.md 抓下来 → 抓取要先于判品味"),
    (re.compile(r"品味判不了.*判官不通"),  True,  "LLM 端点/密钥不通 → 查 secrets"),
    (re.compile(r"品味 \d+ 分 <"),       False, "它确实不够好 —— **这一类不该动机制**"),
]


def classify(why: str) -> tuple[bool, str]:
    for pat, ours, fix in KINDS:
        if pat.search(why):
            return ours, fix
    return True, "没归类的原因 —— 先把它归类，别放着"


def main() -> int:
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--rounds", type=int, default=5, help="看最近几轮")
    a = ap.parse_args()
    if not os.path.exists(LOG):
        print("还没有 gate_log.json —— 跑一轮再来"); return 0
    doc = json.load(open(LOG, encoding="utf-8"))
    rounds = (doc.get("rounds") or [])[:a.rounds]
    if not rounds:
        print("gate_log.json 里没有轮次"); return 0
    items = [x for r in rounds for x in r.get("明细", [])]
    ok = sum(1 for x in items if x.get("过"))
    print(f"最近 {len(rounds)} 轮 · 判了 {len(items)} 件 · 过 {ok} 件 ({ok/max(len(items),1)*100:.0f}%)\n")

    ours = collections.Counter(); theirs = collections.Counter()
    fixmap: dict[str, str] = {}
    ex: dict[str, list] = collections.defaultdict(list)
    for x in items:
        if x.get("过"):
            continue
        why = x.get("为什么", "")
        is_ours, fix = classify(why)
        key = why.split("：")[0].split(" —— ")[0][:20]
        (ours if is_ours else theirs)[key] += 1
        fixmap[key] = fix
        ex[key].append(f'{x.get("title") or x.get("id")}')

    tot_ours = sum(ours.values())
    print(f"**卡在我们自己身上的 {tot_ours} 件** —— 这些本来能过：")
    for k, n in ours.most_common():
        print(f"  {n:3d}  {k}")
        print(f"       修法：{fixmap[k]}")
        print(f"       例：{'、'.join(ex[k][:3])}")
    print(f"\n它确实不够好的 {sum(theirs.values())} 件：")
    for k, n in theirs.most_common():
        print(f"  {n:3d}  {k}    {fixmap[k]}")
    if tot_ours:
        top = ours.most_common(1)[0]
        print(f"\n→ **先修这一处**：{top[0]}（挡了 {top[1]} 件）\n   {fixmap[top[0]]}")
    else:
        print("\n→ 没有卡在我们自己身上的。剩下的都是货本身不够好，那是判据在干活。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
