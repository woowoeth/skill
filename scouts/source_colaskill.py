#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""colaskill.com —— 店主 09-07 指的市场。静态站（Astro）：首页卡片 /<slug>/，每页底部带 GitHub 仓链接。
扫法：首页取所有卡片 → 逐页取 github.com/owner/repo → 没见过的进候选。每天一遍，几十个请求。"""
from __future__ import annotations
import json, os, re, sys, time, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEEN = os.path.join(ROOT, "editorial", "colaskill_seen.json")
BASE = "https://colaskill.com"


def get(url: str) -> str:
    r = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", "pinwei-scout", url], capture_output=True)
    return r.stdout.decode("utf-8", "replace")


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="/tmp/colaskill_candidates.json"); a = ap.parse_args()
    seen = json.load(open(SEEN, encoding="utf-8")) if os.path.exists(SEEN) else {}
    home = get(BASE + "/")
    slugs = sorted(set(re.findall(r'class="skill-card-link" href="/([^/"]+)/"', home)))
    print(f"[colaskill] 首页卡片 {len(slugs)} 个", flush=True)
    found = {}
    for slug in slugs:
        if slug in seen:
            continue
        page = get(f"{BASE}/{slug}/")
        repos = sorted({m.rstrip(".").removesuffix(".git") for m in re.findall(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)", page)})
        seen[slug] = {"repos": repos, "seen_at": time.strftime("%Y-%m-%d")}
        for r in repos:
            # 09-07 第一轮：55 条里 20 条是 colaskill 把 ResumeSkills 的子目录当成了仓（gh api 404），核一下仓存在再收
            ok = subprocess.run(["gh", "api", f"repos/{r}", "--jq", ".full_name"], capture_output=True, text=True)
            if ok.returncode != 0:
                continue
            found[r] = {"via": f"colaskill:{slug}", "stars": 0, "path": ""}
        print(f"  {slug}: {repos}", flush=True)
        time.sleep(0.5)
    json.dump(seen, open(SEEN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(found, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[colaskill] 新候选 {len(found)} 个 → {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
