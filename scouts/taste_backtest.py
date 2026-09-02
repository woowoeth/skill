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

JUDGE_PROMPT = """你在替一家中文 Agent Skill 精选店判货。给这一件打 0-100 分。

这家店卖的是**判断**，不是索引。店主认可的那些货有一个共同点：
**它把一件事做到了「有人真的想过这件事该怎么做」的程度** ——
它会拒绝做某些事、会说清楚产出物到哪儿为止、会在一个具体场景里给出别处拿不到的做法。
不是「功能多」，不是「star 高」，也不是题材（画画、写作、算命、报税都可以）。

店主认可的（他亲手标的）：
{pos}

店主没要的：
{neg}

给分参考：
  80-100  别处拿不到，而且它对自己的边界很清楚
  60-79   做得扎实，但换个工具也能做
  40-59   能用，泛泛，说不出非它不可的理由
  0-39    是模板/目录/基建/官方示例，或者读完说不出它到底交付什么

读下面这份上游 SKILL.md 正文，只回一个 JSON：{{"score": 0-100, "why": "不超过25字"}}
**打分，不要判是非。** 大部分东西落在 40-70 之间是正常的。

---
{body}
---"""


def body_of(i: str) -> str | None:
    # "!" 前缀 = 真负样本（拒收榜的上游正文，抓在 methods_rejected/）
    if i.startswith("!"):
        p = os.path.join(ROOT, "methods_rejected", f"{i[1:]}.md")
        return open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else None
    p = os.path.join(ROOT, "methods", f"{i}.md")
    if not os.path.exists(p):
        return None
    return open(p, encoding="utf-8", errors="replace").read()


def title_of(i: str, cur: dict) -> str:
    return ((cur.get(i) or {}).get("title_zh") or i.lstrip("!"))[:34]


def main() -> int:
    import glob
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--holdout", type=int, default=18, help="每边留出多少件")
    ap.add_argument("--shots", type=int, default=8, help="每边给几个例子")
    ap.add_argument("--verify-refs", action="store_true",
                    help="拿 taste_refs.json（店主指名、从没进过训练/留出）当新数据验门槛")
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
    # **负样本必须是「店主不要的」，不是「还没人判过的」。**
    # 2026-09-02 之前三轮测量（+1pt / +6pt / +11pt）用的都是库房当负样本 ——
    # 而库房里的货是**未判**，不是**判过不要**，里面本来就混着大量好货。
    # 拿「没判过」当「不好」，任何判据都会被压平。三轮结论都可能是这个错造出来的。
    # 真负样本：按问一/问二/问三拒收的，上游正文抓在 methods_rejected/。
    neg_dir = os.path.join(ROOT, "methods_rejected")
    neg = ["!" + f[:-3] for f in sorted(os.listdir(neg_dir))] if os.path.isdir(neg_dir) else []
    if not neg:
        print("methods_rejected/ 是空的 —— 先跑抓取，别拿库房当负样本"); return 2
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
    def judge(i: str) -> int | None:
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
            return int(json.loads(txt).get("score", -1))
        except Exception as e:
            print(f"    ! {i}: {type(e).__name__}: {e}")
            return None

    if a.verify_refs:
        # **门槛是在留出集上挑的，必须在没见过的数据上再验一次。**
        # taste_refs 里是店主 2026-09-02 指名说「这是有品味的」的四件，
        # 它们从来不在正样本池（methods/ 里没有或不在 hearts），是干净的新数据。
        refs = json.load(open(os.path.join(ROOT, "editorial", "taste_refs.json"),
                              encoding="utf-8"))["items"]
        import glob as _g, re as _re
        allm = {f[len(os.path.join(ROOT, "methods")) + 1:-3]
                for f in _g.glob(os.path.join(ROOT, "methods", "*.md"))}
        print("\n拿店主指名的那几件当新数据验门槛 ≥60：")
        hit = tot = 0
        for repo in refs:
            sl = _re.sub(r"[^a-z0-9]+", "-", repo.lower()).strip("-")
            cand = [i for i in allm if i.startswith(sl)] or \
                   [i for i in allm if i.startswith(sl.split("-")[0])]
            if not cand:
                print(f"  · {repo:<42} 没有上游正文存档，跳过"); continue
            sc = judge(cand[0]); tot += 1
            ok = sc is not None and sc >= 60
            hit += ok
            print(f"  {'✓' if ok else '✗'} {repo:<42} {sc} 分")
        print(f"\n新数据上：{hit}/{tot} 件过 ≥60 线")
        return 0
    kp = [x for x in (judge(i) for i in ho_pos) if x is not None and x >= 0]
    kn = [x for x in (judge(i) for i in ho_neg) if x is not None and x >= 0]
    if not kp or not kn:
        print("判不出来，测试无效"); return 2
    print(f"\n留出正样本 {len(kp)} 件 · 均分 {sum(kp)/len(kp):.1f} · 分布 {sorted(kp)}")
    print(f"留出负样本 {len(kn)} 件 · 均分 {sum(kn)/len(kn):.1f} · 分布 {sorted(kn)}")
    # 门槛不是拍的：把每个可能的分数线都试一遍，取区分力最大的那条。
    best = (-999, 0, 0, 0)
    for th in range(0, 101, 5):
        a = sum(1 for x in kp if x >= th) / len(kp)
        b = sum(1 for x in kn if x >= th) / len(kn)
        if (a - b) * 100 > best[0]:
            best = ((a - b) * 100, th, a, b)
    lift, th, a, b = best
    print(f"\n最佳分数线 ≥{th}：正样本过 {a*100:.0f}% · 负样本过 {b*100:.0f}%")
    print(f"**区分力 {lift:+.0f}pt**   （题材词 +1pt · 上游形态 +6pt · 上一版二元问法 −17pt）")
    print("\n" + ("→ 够格当门闸。**但门槛是在留出集上挑的，真用之前要在新一批上再验一次**，"
                  "否则就是拿留出集当训练集。" if lift >= 25 else
                  "→ 还不够格。"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
