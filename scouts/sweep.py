#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自己去找有品味的货 —— 把「发现」和「判品味」接起来。

## 为什么有这个

2026-09-02 店主：「你要去不断迭代自己，不要每次让我告诉你哪些漏掉了，
你要自己有能力发现漏掉的有品味的 skill」。

那天之前我把两半都造好了，却**从来没接起来**：
  · discover_by_artifact.py 已经翻出 1276 个从没进过库的仓
  · 品味判据已经回测到 +61pt（真负样本），店主指名的四件新数据 3/4 过
**我有渔网也有秤，却一次都没拿秤去称过网里的鱼。**

这个脚本就是那根接线：
  候选池 → 取上游 SKILL.md → 判品味 → 高分的落库并留档 → 低分的记下分数不再重判

## 它不做的事

**不自动上架。** 上架仍走既有那条（文案齐 + 品味 ≥ TASTE_MIN + 红线扫过）。
这里只负责「把值得写文案的挑出来」——把 LLM 写文案的钱花在可能过闸的货上，
而不是给 1276 个仓每个都写一遍。

## 怎么知道它有没有用

`--audit`：拿 editorial/taste_refs.json（店主指名说「这是有品味的」的那些）回测——
**当初是他告诉我的，现在这套能不能自己找到。** 找不到就报出来，
那说明缺的是通道不是判据（或者反过来），而不是「再加几条搜索词」。
"""
from __future__ import annotations
import json, os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scouts"))
SEEN = os.path.join(ROOT, "editorial", "sweep_seen.json")


def gh(url: str) -> dict:
    r = subprocess.run(["gh", "api", url], capture_output=True)
    try:
        return json.loads(r.stdout.decode("utf-8", "replace"))
    except Exception:
        return {}


def skill_md(repo: str) -> tuple[str, str]:
    """取仓里最浅的那份 SKILL.md。返回 (路径, 正文)，取不到返回 ("","")。"""
    r = subprocess.run(["gh", "api", f"repos/{repo}/git/trees/HEAD?recursive=1",
                        "--jq", '.tree[].path|select(endswith("SKILL.md"))'],
                       capture_output=True)
    paths = r.stdout.decode("utf-8", "replace").split()
    if not paths:
        return "", ""
    p = sorted(paths, key=lambda x: (x.count("/"), len(x)))[0]
    c = subprocess.run(["curl", "-sL", "--max-time", "30",
                        f"https://raw.githubusercontent.com/{repo}/HEAD/{p}"],
                       capture_output=True)
    body = c.stdout.decode("utf-8", "replace")
    return (p, body) if len(body) > 300 and not body.startswith("404") else (p, "")


def main() -> int:
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--candidates", default="/tmp/artifact_candidates.json")
    ap.add_argument("--max", type=int, default=40, help="每轮判多少个（判官要花钱）")
    ap.add_argument("--min-score", type=int, default=70,
                    help="高于这个分才值得写文案。比上架门槛 60 高一档——"
                         "上架那关还有红线和文案要过，这里宁可少放")
    ap.add_argument("--audit", action="store_true",
                    help="拿店主指名的那些回测：这套现在能不能自己找到它们")
    a = ap.parse_args()

    import skill_scout as S
    if not S.LLM_KEY:
        print("没有 LLM_API_KEY —— 判品味要在配了 key 的地方跑（CI）")
        return 2

    seen = json.load(open(SEEN, encoding="utf-8")) if os.path.exists(SEEN) else {}

    if a.audit:
        refs = json.load(open(os.path.join(ROOT, "editorial", "taste_refs.json"),
                              encoding="utf-8"))["items"]
        print("拿店主指名的那些回测 —— 当初是他告诉我的，现在这套能不能自己判出来：\n")
        hit = tot = 0
        for repo in refs:
            path, body = skill_md(repo)
            if not body:
                print(f"  · {repo:<44} 取不到 SKILL.md（{path or '树里没有'}）"); continue
            sc, why = S.taste_score({"id": "", "_body": body}) if False else _score(S, body)
            tot += 1; ok = sc >= a.min_score; hit += ok
            print(f"  {'✓' if ok else '✗'} {repo:<44} {sc:>3} 分  {why}")
        print(f"\n{hit}/{tot} 件能被现在这套判到 ≥{a.min_score}")
        if hit < tot:
            print("**没判到的那些，是这套还缺的东西** —— 先看是通道没捞到，还是判据给低了，"
                  "别急着调分数线。")
        return 0

    cands = json.load(open(a.candidates, encoding="utf-8")) if os.path.exists(a.candidates) else {}
    todo = [r for r in cands if r not in seen][:a.max]
    print(f"候选池 {len(cands)} 个 · 判过 {len(seen)} 个 · 本轮判 {len(todo)} 个\n")
    keep = []
    for n, repo in enumerate(todo, 1):
        path, body = skill_md(repo)
        if not body:
            seen[repo] = {"score": -1, "why": "取不到 SKILL.md"}
            print(f"  {n:3d} ·   —  {repo}  取不到 SKILL.md"); continue
        sc, why = _score(S, body)
        seen[repo] = {"score": sc, "why": why, "path": path}
        mark = "★" if sc >= a.min_score else " "
        print(f"  {n:3d} {mark} {sc:>3}  {repo}  —— {why}")
        if sc >= a.min_score:
            keep.append({"repo": repo, "path": os.path.dirname(path), "score": sc, "why": why})
        time.sleep(1)
    json.dump(seen, open(SEEN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    out = "/tmp/sweep_keep.json"
    json.dump(keep, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n≥{a.min_score} 分的 {len(keep)} 个 → {out}")
    print(f"判过的留档 editorial/sweep_seen.json（{len(seen)} 个，不再重判）")
    if keep:
        print("\n下一步：把它们交给 --suggest 走完整管线（写文案 → 判品味 → 扫红线 → 上架）")
        print("  python3 scouts/skill_scout.py --suggest " + " ".join(k["repo"] for k in keep[:12]))
    return 0


def _score(S, body: str) -> tuple[int, str]:
    """直接拿正文去判（候选还没落库，没有 methods/ 存档）。判 TASTE_VOTES 遍取中位，和管线口径一致。"""
    n = max(1, int(__import__("os").environ.get("TASTE_VOTES") or 3))
    votes, why = [], ""
    for _ in range(n):
        sc, w = _score_once(S, body)
        if sc < 0:
            return sc, w
        votes.append(sc); why = why or w
    votes.sort()
    return votes[len(votes) // 2], why


def _score_once(S, body: str) -> tuple[int, str]:
    import urllib.request
    prompt = S.TASTE_PROMPT.format(body=body[:6000])
    ant = S.LLM_KEY.startswith("sk-ant-") or "anthropic" in S.LLM_BASE
    if ant:
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
        txt = (resp["content"][0]["text"] if ant else resp["choices"][0]["message"]["content"])
        txt = txt.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        d = json.loads(txt)
        return int(d.get("score", -1)), str(d.get("why", "")).strip()[:40]
    except Exception as e:
        return -1, f"{type(e).__name__}"


if __name__ == "__main__":
    sys.exit(main())
