#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从「品味参照」反推发现：心选 + 店长推荐 + 店主指名 + 编辑亲挑 = 这家店认过的货。

店主 2026-09-03 晚：「为什么每次我能发现你却发现不了……基于店长推荐和心选重构你的发现系统，
目标是不错过任何一个精品，不加入任何一个垃圾」。

当晚复盘店主指名的 8 件：5 件我的系统**从来没见过**——不是判错，是没碰到：
  · 流扫只看 GitHub 最近索引的 SKILL.md，建于 7 月中的仓永远碰不到；
  · 回填只回看三周、只收 ≥3 星；
  · 两条道都是「按时间捞新的」，没有一条是「按这家店认过的货往外找」。
  其中 gnipbao/story-to-handdrawn-video 的作者 gnipbao 架上早就有一件 —— 同作者这条线一直没人走。

三条通道，每天跑：
  ① 同作者：参照货的作者名下所有仓，凡有 SKILL.md 的都进候选。好作者会连着出好货。
  ② 同题材：从参照货的标题/描述/仓名抽词（中英文都要），拿去搜仓（不限创建日期）。
  ③ 相邻仓：GitHub 的「同一作者 star 过 / fork 自」拿不到，用参照仓 README 里链到的其它 GitHub 仓代替。
输出 {repo: {via, stars, path}}，和其它通道一样交给判官 + 编辑阅读。
"""
from __future__ import annotations
import json, os, re, sys, time, subprocess, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEEN = os.path.join(ROOT, "editorial", "refs_seen.json")
STOP = set("skill skills claude codex agent agents ai the and for with your you 一个 一张 一份 一句 一次 把 用 给 让 不 的 了 是 和 与 或 在 从 到 就 也 都 会 能 要 有 没 这 那 它 你 我 他 们 上 下 里 中 出 来 去 做 看 说 写 生成 工具 助手 系统 专业 智能 token tokens create generate generated review language notes image images vault research design video writing 合集里只 挑这 只挑 这一件 编辑 心选 同仓 一件 那件 这件 读者 拿到 直接 自动 一套 一本 一条 全程 不是 而是 每次 先出 才写 出的 一份 一句 一个 一张".split())


def sh(cmd: list[str]) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def gh_json(path: str):
    out = sh(["gh", "api", path])
    try:
        return json.loads(out) if out else {}
    except Exception:
        return {}


def refs() -> list[dict]:
    """这家店认过的货：心选 / 钉住的推荐 / 店主指名 / 编辑亲挑，去重后返回 {repo, title, desc}。"""
    feed = {x["id"]: x for x in json.load(open(os.path.join(ROOT, "skills", "feed.json"), encoding="utf-8"))["skills"]}
    ids = set(json.load(open(os.path.join(ROOT, "editorial", "hearts.json"), encoding="utf-8")).get("ids", []))
    ids |= set(json.load(open(os.path.join(ROOT, "editorial", "picks_pinned.json"), encoding="utf-8")).get("ids", []))
    out, seen = [], set()
    for i in ids:
        x = feed.get(i)
        if x and x["repo"].lower() not in seen:
            seen.add(x["repo"].lower()); out.append({"repo": x["repo"], "title": x.get("title_zh") or "", "desc": (x.get("tagline_zh") or "") + " " + (x.get("desc_en") or "")})
    for fn in ("taste_refs.json", "editor_picks.json"):
        d = json.load(open(os.path.join(ROOT, "editorial", fn), encoding="utf-8")).get("items", {})
        for k, v in d.items():
            repo = v.get("repo") or k
            if repo.lower() not in seen:
                seen.add(repo.lower()); out.append({"repo": repo, "title": v.get("reason", "")[:40], "desc": v.get("note", "")})
    return out


def known() -> set[str]:
    k = set()
    for fn in ("stream_seen.json", "sweep_seen.json", "backfill_seen.json", "refs_seen.json"):
        p = os.path.join(ROOT, "editorial", fn)
        if os.path.exists(p):
            d = json.load(open(p, encoding="utf-8"))
            k |= {x.split("#")[0].split("@")[0].lower() for x in (d if isinstance(d, dict) else [])}
    k |= {x["repo"].lower() for x in json.load(open(os.path.join(ROOT, "skills", "feed.json"), encoding="utf-8"))["skills"]}
    try:
        k |= {(e.get("repo") or "").lower() for e in json.load(open(os.path.join(ROOT, "editorial", "rejected.json"), encoding="utf-8"))["entries"] if isinstance(e, dict)}
    except Exception:
        pass
    return k


def tree_skill_path(repo: str):
    t = gh_json(f"repos/{repo}/git/trees/HEAD?recursive=1")
    allp = [x.get("path", "") for x in (t.get("tree") or []) if x.get("type") == "blob"]
    paths = [p for p in allp if p.endswith("SKILL.md")]
    if not paths:
        return None
    # 09-04 R2 验证：kangarooking 名下 21 个「拆书生成器」批量产出的仓，每个只有 SKILL.md + test-prompts.json，
    # 拆掉指令什么都不剩，0/24 选中。这种形状的仓不算候选 —— 好作者连着出好货，生成器不算作者。
    names = {os.path.basename(p).lower() for p in allp}
    if len(allp) <= 4 and names <= {"skill.md", "test-prompts.json", "readme.md", "license", ".gitignore"}:
        return None
    return os.path.dirname(sorted(paths, key=lambda p: (p.count("/"), len(p)))[0])


def lane_authors(rf: list[dict], k: set[str], budget: int) -> dict:
    """① 同作者名下所有仓。"""
    out, authors = {}, []
    for r in rf:
        a = r["repo"].split("/")[0]
        if a.lower() not in {x.lower() for x in authors}:
            authors.append(a)
    print(f"[refs] 同作者通道：{len(authors)} 位作者", flush=True)
    for a in authors:
        if len(out) >= budget:
            break
        repos = gh_json(f"users/{a}/repos?per_page=100&sort=updated") or []
        if isinstance(repos, dict):
            repos = []
        for rp in repos:
            full = rp.get("full_name", "")
            if not full or full.lower() in k or rp.get("fork"):
                continue
            p = tree_skill_path(full)
            k.add(full.lower())
            if p is not None:
                out[full] = {"via": f"refs:author:{a}", "stars": rp.get("stargazers_count", 0), "path": p}
                print(f"  + {full}  ★{rp.get('stargazers_count', 0)}  ← 同作者 {a}", flush=True)
            time.sleep(0.3)
        time.sleep(0.5)
    return out


def terms_from(rf: list[dict], n: int) -> list[str]:
    """② 从参照货抽题材词：仓名里的英文词 + 标题/描述里的中文 2–4 字词，按频次取前 n。"""
    from collections import Counter
    c = Counter()
    for r in rf:
        name = r["repo"].split("/")[-1]
        for w in re.split(r"[-_.\s]+", name.lower()):
            if len(w) >= 4 and w not in STOP and not w.isdigit():
                c[w] += 1
        text = (r.get("title") or "") + " " + (r.get("desc") or "")
        for w in re.findall(r"[一-鿿]{2,4}", text):
            if w not in STOP:
                c[w] += 1
        for w in re.findall(r"[A-Za-z]{5,}", text):
            w = w.lower()
            if w not in STOP:
                c[w] += 1
    return [w for w, _ in c.most_common(n)]


def lane_terms(rf: list[dict], k: set[str], budget: int, n_terms: int) -> dict:
    out = {}
    terms = terms_from(rf, n_terms)
    print(f"[refs] 同题材通道：{len(terms)} 个词 → {', '.join(terms[:20])}…", flush=True)
    for t in terms:
        if len(out) >= budget:
            break
        q = urllib.parse.quote(f"{t} skill in:name,description,readme")
        r = gh_json(f"search/repositories?q={q}&sort=updated&order=desc&per_page=30")
        for rp in r.get("items") or []:
            full = rp.get("full_name", "")
            if not full or full.lower() in k or rp.get("fork"):
                continue
            p = tree_skill_path(full)
            k.add(full.lower())
            if p is not None:
                out[full] = {"via": f"refs:term:{t}", "stars": rp.get("stargazers_count", 0), "path": p}
                print(f"  + {full}  ★{rp.get('stargazers_count', 0)}  ← 词「{t}」", flush=True)
            time.sleep(0.3)
        time.sleep(2.2)
    return out


def lane_links(rf: list[dict], k: set[str], budget: int) -> dict:
    """③ 参照仓 README 里链到的其它 GitHub 仓。"""
    out = {}
    for r in rf:
        if len(out) >= budget:
            break
        md = sh(["curl", "-sL", "--max-time", "15", f"https://raw.githubusercontent.com/{r['repo']}/HEAD/README.md"])
        for full in set(re.findall(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)", md)):
            full = full.rstrip(".").removesuffix(".git")
            if full.lower() in k or full.lower() == r["repo"].lower() or "/" not in full:
                continue
            p = tree_skill_path(full)
            k.add(full.lower())
            if p is not None:
                out[full] = {"via": f"refs:link:{r['repo']}", "stars": 0, "path": p}
                print(f"  + {full}  ← {r['repo']} 的 README 链过去", flush=True)
            time.sleep(0.3)
    return out


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/tmp/refs_candidates.json")
    ap.add_argument("--budget", type=int, default=60, help="每条通道最多收多少个新仓")
    ap.add_argument("--terms", type=int, default=40)
    ap.add_argument("--lanes", default="authors,terms,links")
    a = ap.parse_args()
    rf = refs(); k = known()
    seen = json.load(open(SEEN, encoding="utf-8")) if os.path.exists(SEEN) else {}
    print(f"[refs] 参照货 {len(rf)} 件 · 已知仓 {len(k)}", flush=True)
    found = {}
    if "authors" in a.lanes:
        found.update(lane_authors(rf, k, a.budget))
    if "terms" in a.lanes:
        found.update(lane_terms(rf, k, a.budget, a.terms))
    if "links" in a.lanes:
        found.update(lane_links(rf, k, a.budget))
    for full in found:
        seen[full] = found[full]["via"]
    json.dump(seen, open(SEEN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(found, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n[refs] 新候选 {len(found)} 个 → {a.out}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
