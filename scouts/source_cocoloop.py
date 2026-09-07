#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hub.cocoloop.cn —— 店主 09-07 指的市场。7.2 万件，接口 api.cocoloop.cn/api/v1/store/skills。
列表/详情都不给 GitHub 链接，但 asset_name 是 `<author>-<repo-slug>-<version>.zip`，author 字段就是 GitHub 用户名：
拿 author + slug 去 GitHub 核一遍（存在且有 SKILL.md）→ 进候选；核不到的记下来（可能只在 cocoloop 发布，我们的管线暂不收）。
每天扫 tab=latest 三页 + tab=trending 一页（sort 只能 downloads/stars/rating/recommend）。"""
from __future__ import annotations
import json, os, re, sys, time, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEEN = os.path.join(ROOT, "editorial", "cocoloop_seen.json")
API = "https://api.cocoloop.cn/api/v1/store/skills"


def get_json(url: str):
    r = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", "pinwei-scout", url], capture_output=True)
    try:
        return json.loads(r.stdout.decode("utf-8", "replace"))
    except Exception:
        return {}


def gh_tree_has_skill(repo: str):
    r = subprocess.run(["gh", "api", f"repos/{repo}/git/trees/HEAD?recursive=1", "--jq", "[.tree[].path|select(endswith(\"SKILL.md\"))]|.[0]"], capture_output=True, text=True)
    if r.returncode != 0:
        return None
    p = r.stdout.strip().strip('"')
    return os.path.dirname(p) if p and p != "null" else None


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/tmp/cocoloop_candidates.json")
    ap.add_argument("--pages", type=int, default=3)
    a = ap.parse_args()
    seen = json.load(open(SEEN, encoding="utf-8")) if os.path.exists(SEEN) else {}
    items = []
    # 09-07 第一批 28 件读完：0 选中、5 红线、16 工具链 —— overall/latest/trending 三榜几乎全是 OpenClaw 生态的 agent 基建件。
    # 改扫它自己的分类榜：设计 / 内容创作 / 办公 / 专业 / 效率，最新榜只留一页兜住新货。
    for tab, pages in (("design", a.pages), ("content_creation", a.pages), ("office", 1), ("professional", 1), ("efficiency", 1), ("latest", 1)):
        for page in range(1, pages + 1):
            d = get_json(f"{API}?page={page}&page_size=100&sort=downloads&tab={tab}")
            its = ((d.get("data") or {}).get("items")) or []
            items += [dict(x, _tab=tab) for x in its]
            time.sleep(1)
    print(f"[cocoloop] 拉到 {len(items)} 件", flush=True)
    found, nogh, checked = {}, 0, 0
    for it in items:
        sid = str(it.get("id"))
        if sid in seen:
            continue
        author = (it.get("author") or "").strip()
        detail = get_json(f"{API}/{sid}")
        asset = ((detail.get("data") or {}).get("asset_name")) or ""
        # 包名就是 `<slug>.zip`，author 是 GitHub 用户名。先试 author/slug；不存在就在该用户下按 slug 搜仓（skill 常在合集仓里）
        slug = re.sub(r"\.zip$", "", asset, flags=re.I) or (it.get("name") or "").strip().lower().replace(" ", "-")
        repo, path = "", None
        rec = {"name": it.get("name"), "author": author, "downloads": it.get("downloads"), "stars": it.get("github_stars"), "tab": it["_tab"], "seen_at": time.strftime("%Y-%m-%d")}
        if author and slug:
            checked += 1
            cands = [f"{author}/{slug}"]
            sr = subprocess.run(["gh", "api", f"search/repositories?q=user:{author}+{slug}+in:name,description&per_page=3", "--jq", ".items[].full_name"], capture_output=True, text=True)
            cands += [x for x in sr.stdout.split() if x and x not in cands]
            for c in cands[:3]:
                p_ = gh_tree_has_skill(c)
                if p_ is not None:
                    repo, path = c, p_
                    break
                time.sleep(0.3)
            rec["repo"] = repo
            if repo:
                found[repo] = {"via": f"cocoloop:{it['_tab']}:{sid}", "stars": 0, "path": path}
                rec["github"] = True
                print(f"  + {repo}  ← {it.get('name')}（下载 {it.get('downloads')}）", flush=True)
            else:
                rec["github"] = False; nogh += 1
        else:
            nogh += 1
        seen[sid] = rec
        time.sleep(0.4)
    json.dump(seen, open(SEEN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(found, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[cocoloop] 核 GitHub {checked} 个 · 对上 {len(found)} 个 · 对不上/不在 GitHub {nogh} → {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
