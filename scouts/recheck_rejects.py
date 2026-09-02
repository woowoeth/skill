#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复查拒收榜 —— **拒收是永久的，上游却在变。**

2026-09-02：店主问「为什么我们网站没有 hugohe3/ppt-master」。
查拒收榜：08-20 按红线拒的，记的原文是
    # Prefer curl_cffi for TLS-fingerprint impersonation (bypasses JA3 blocking…)
去看现在的仓，同一处已经改成
    # Optional — … If installed, web_to_md.py uses it automatically;
      otherwise falls back to requests.
**从「默认用」变成了「可选，且有回退」** —— 按本店「拆了还工作吗」的判据，
那是选项不是机制，该留架加披露，不该拒收。

我们拒了一个 48k 星的仓，拒的理由两周前就不成立了，而**没有任何东西会回头看**。
这个脚本就是那个回头看的东西：把红线拒收的仓重扫一遍，
命中消失的挑出来给人复核。它不自动翻案 —— 翻案是人的事。
"""
from __future__ import annotations
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REJ = os.path.join(ROOT, "editorial", "rejected.json")


def main() -> int:
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--rule", default="红线", help="复查哪一档（默认只查红线）")
    ap.add_argument("--max", type=int, default=15)
    ap.add_argument("--out", default="/tmp/recheck.json")
    a = ap.parse_args()
    ents = [e for e in json.load(open(REJ, encoding="utf-8"))["entries"]
            if e.get("reject_rule") == a.rule]
    ents.sort(key=lambda e: -int(e.get("stars") or 0))     # 星高的先复查，影响面大
    todo = ents[:a.max]
    print(f"{a.rule} 拒收 {len(ents)} 条，本轮复查星数最高的 {len(todo)} 条\n")
    changed = []
    for e in todo:
        repo = e.get("repo")
        r = subprocess.run([sys.executable, os.path.join(ROOT, "scouts", "scan_refs.py"),
                            repo, "--no-archive"], capture_output=True, text=True)
        out = r.stdout
        hits = [l.strip() for l in out.splitlines() if l.strip().startswith("[")]
        mark = "命中消失" if not hits else f"仍有 {len(hits)} 处"
        print(f"  ★{e.get('stars',0):>6}  {repo:<44} {mark}")
        if not hits:
            changed.append({"repo": repo, "stars": e.get("stars"),
                            "原拒因": e.get("reject_reason_zh"),
                            "原文": (e.get("desc") or "")[:160]})
    json.dump(changed, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n命中消失、值得人复核的 {len(changed)} 条 → {a.out}")
    print("**这个脚本不自动翻案。** 命中消失可能是上游改好了，"
          "也可能是我们的扫描器变了口径 —— 两者要人去看原文才分得清。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
