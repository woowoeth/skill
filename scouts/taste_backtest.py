#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LLM 判品味，先拿店主标过的货做留出测试 —— **验完再用，不验就不用。**

## 为什么要先测

2026-09-02 量过两轮，两轮都失败：
    题材关键词（TASTE_RE）      心选 33% / 非心选 32%  →  +1pt
    上游 SKILL.md 形态特征       最好的一条            →  +6pt
（形态特征包括：正文长度、拒答语密度、反模式章节、表格数、结构化步骤数、
  是否说了产出物。「说了产出物」甚至是 −15pt。）

**便宜的文本启发式做不了这个判断。** 所以剩下的候选只有一个：让 LLM 读上游正文来判。
但 LLM 判得准不准同样是个可测的问题，**不能因为它听起来聪明就直接上**。

## 怎么测

正样本：editorial/hearts.json 的 73 件 + editorial/taste_refs.json 里店主指名的。
负样本：库房里有上游正文存档、且不在正样本里的。
从两边各留出一部分**不给模型看**，用剩下的当 few-shot 例子，然后让它判留出集。

判它是否有用的标准，就是前两轮用的同一把尺子：
    **正样本通过率 − 负样本通过率**
+1pt 和 +6pt 都已经证明没用。这一轮如果低于 +25pt，就不该拿它自动排序 ——
一个和随机差不多的排序器，比没有排序器更糟：它会让人以为前面的更值得看。
"""
from __future__ import annotations
import json, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scouts"))

JUDGE_PROMPT = """你在替一家中文 Agent Skill 精选店的店主做初筛。这家店只留「有品味」的货。

店主认可的例子（他亲手标的）：
{pos}

他没要的例子：
{neg}

现在读这一件的上游 SKILL.md 正文，只回答一个 JSON：{{"keep": true/false, "why": "不超过30字"}}
判的是**店主会不会认可它**，不是它有没有用。

---
{body}
---"""


def body_of(i: str) -> str | None:
    p = os.path.join(ROOT, "methods", f"{i}.md")
    if not os.path.exists(p):
        return None
    return open(p, encoding="utf-8", errors="replace").read()


def title_of(i: str, cur: dict) -> str:
    return ((cur.get(i) or {}).get("title_zh") or i)[:34]


def main() -> int:
    import glob
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--holdout", type=int, default=18, help="每边留出多少件")
    ap.add_argument("--shots", type=int, default=8, help="每边给几个例子")
    a = ap.parse_args()

    cur = json.load(open(os.path.join(ROOT, "editorial", "curation.json"),
                         encoding="utf-8"))["items"]
    hearts = set(json.load(open(os.path.join(ROOT, "editorial", "hearts.json"),
                                encoding="utf-8"))["ids"])
    live = {x["id"] for x in json.load(open(os.path.join(ROOT, "skills", "feed.json"),
                                            encoding="utf-8"))["skills"]}
    have = [f[len(os.path.join(ROOT, "methods")) + 1:-3]
            for f in glob.glob(os.path.join(ROOT, "methods", "*.md"))]
    pos = [i for i in have if i in hearts]
    neg = [i for i in have if i not in hearts and i not in live]
    random.seed(20260902)
    random.shuffle(pos); random.shuffle(neg)
    ho_pos, ho_neg = pos[:a.holdout], neg[:a.holdout]
    shot_pos, shot_neg = pos[a.holdout:a.holdout + a.shots], neg[a.holdout:a.holdout + a.shots]
    print(f"正样本 {len(pos)} · 负样本 {len(neg)}")
    print(f"留出各 {len(ho_pos)}/{len(ho_neg)} 件（**不给模型看**）· few-shot 各 {len(shot_pos)}/{len(shot_neg)} 件\n")

    try:
        import skill_scout as S
    except SystemExit as e:
        print(f"skill_scout 自检没过：{e}"); return 2
    if not S.LLM_KEY:
        print("没有 LLM_API_KEY —— 这个测试要在配了 key 的地方跑（CI）。")
        print("本地只做干跑，打印将要发出去的第一个提示词的头部：\n")
        p = JUDGE_PROMPT.format(
            pos="\n".join("- " + title_of(i, cur) for i in shot_pos),
            neg="\n".join("- " + title_of(i, cur) for i in shot_neg),
            body=(body_of(ho_pos[0]) or "")[:400])
        print(p[:900]); return 0

    import urllib.request
    def judge(i: str) -> bool | None:
        b = body_of(i)
        if not b:
            return None
        prompt = JUDGE_PROMPT.format(
            pos="\n".join("- " + title_of(x, cur) for x in shot_pos),
            neg="\n".join("- " + title_of(x, cur) for x in shot_neg),
            body=b[:6000])
        anthropic = S.LLM_KEY.startswith("sk-ant-") or "anthropic" in S.LLM_BASE
        if anthropic:
            url = (S.LLM_BASE if "anthropic" in S.LLM_BASE else "https://api.anthropic.com") + "/v1/messages"
            data = json.dumps({"model": S.LLM_MODEL, "max_tokens": 200,
                               "messages": [{"role": "user", "content": prompt}]}).encode()
            hdr = {"x-api-key": S.LLM_KEY, "anthropic-version": "2023-06-01",
                   "Content-Type": "application/json"}
        else:
            url = S.LLM_BASE + "/chat/completions"
            data = json.dumps({"model": S.LLM_MODEL, "max_tokens": 200,
                               "messages": [{"role": "user", "content": prompt}]}).encode()
            hdr = {"Authorization": "Bearer " + S.LLM_KEY, "Content-Type": "application/json"}
        try:
            with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=hdr,
                                                               method="POST"), timeout=60) as r:
                resp = json.loads(r.read())
            txt = (resp["content"][0]["text"] if anthropic
                   else resp["choices"][0]["message"]["content"])
            txt = txt.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            return bool(json.loads(txt).get("keep"))
        except Exception as e:
            print(f"    ! {i}: {type(e).__name__}: {e}")
            return None

    kp = [judge(i) for i in ho_pos]
    kn = [judge(i) for i in ho_neg]
    kp = [x for x in kp if x is not None]; kn = [x for x in kn if x is not None]
    if not kp or not kn:
        print("判不出来，测试无效"); return 2
    a_rate = sum(kp) / len(kp); b_rate = sum(kn) / len(kn)
    lift = (a_rate - b_rate) * 100
    print(f"\n留出正样本通过 {sum(kp)}/{len(kp)} = {a_rate*100:.0f}%")
    print(f"留出负样本通过 {sum(kn)}/{len(kn)} = {b_rate*100:.0f}%")
    print(f"**区分力 {lift:+.0f}pt**   （题材词 +1pt · 形态特征 +6pt，都已证明没用）")
    print("\n" + ("→ 够格拿来给候选排序（但仍然只排序，不自动上架）" if lift >= 25 else
                  "→ **不够格。** 和随机差不多的排序器比没有更糟：它会让人以为前面的更值得看。"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
