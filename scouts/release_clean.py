#!/usr/bin/env python3
"""
自动放行 —— 把「文案写好了、只差扫红线」的新货扫一遍，干净的自动上架。

## 为什么有这个脚本

2026-09-01：enrich 修好了、19 件文案全写出来了，货架却一件没多。
因为新货默认 hide=True，要等红线扫描；而扫描一直是手动跑的。
结果是「自动进货 + 自动写文案 + 手动放行」——中间那道手动，让整条链名义自动、实际停摆。

## 边界：机器只放行「没命中」的

scan_refs.py 的设计原则是「不下判决，不自动拒收」——机器给的是「这一行你去看」，判决是人的事。
这个脚本严格守住那条线：

  · 扫完**没有任何命中** → 自动放行（不需要判断，没东西可判断）
  · 扫出命中          → **留库房**，等人读原文再定（哪怕看起来像误报）
  · 扫不动（超时/404）→ **留库房**，不当作干净

宁可漏放，不可错放：一件好货晚一天上架没什么，一件带毒的上架了要人命。
"""
from __future__ import annotations
import argparse, glob, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


# 门禁：直接用 skill_scout 里那一份，避免两条上架路径各长各的标准。
# 读不到就用等价的本地实现，并**明说是兜底**——不要静默降级到更松的判据。
try:
    sys.path.insert(0, HERE)
    from skill_scout import GATE_FIELDS as _GF, _taste_pass as _tp

    def _gate_ok(d: dict) -> bool:
        return bool(_tp(d))
except Exception as _e:                                   # pragma: no cover
    print(f"[release] ! 读不到 skill_scout 的门禁（{_e}），用本地等价实现兜底")
    _GF = ("title_zh", "tagline_zh", "why_zh", "limit_zh")

    def _gate_ok(d: dict) -> bool:
        if d.get("kind") == "collection":
            pass                                          # 合集不再一刀切拒
        if not all(len((d.get(k) or "").strip()) >= 8 for k in _GF):
            return False
        return len((d.get("limit_zh") or "").strip()) >= 20


def held_items() -> list[dict]:
    """留库房、但文案已经写好的 —— 只差扫红线这一步。"""
    out = []
    for f in glob.glob(os.path.join(ROOT, "skills", "*.json")):
        if f.endswith("feed.json"):
            continue
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if not d.get("hide"):
            continue
        # **和 same_day_shelf 用同一把尺子。** 2026-09-02 改。
        # 原来这里只看 why_zh，而同轮上架那条路要求 GATE_FIELDS 四句齐 + limit_zh≥20 ——
        # **一个货架两套标准**，结果 13 件没有 limit_zh 的货从这条路进了架，
        # 触发守卫【14】「机器占位文案上架」。
        # 门禁只能有一处定义，这里 import 过来，不再各写各的。
        if not _gate_ok(d):
            continue          # 文案不齐的不在本脚本管辖内
        d["_file"] = f
        out.append(d)
    return out


def already_scanned() -> set:
    """scan_archive.json 是守卫判断「扫过没有」的依据。"""
    p = os.path.join(HERE, "scan_archive.json")
    if not os.path.exists(p):
        return set()
    try:
        a = json.load(open(p, encoding="utf-8"))
    except Exception:
        return set()
    rows = a if isinstance(a, list) else a.get("scans", a.get("items", []))
    return {(r.get("repo"), r.get("path", "")) for r in rows if isinstance(r, dict)}


def scan(batch: list[dict], out_json: str, timeout: int) -> list[dict]:
    jobs = [{"repo": d["repo"], "path": d.get("path", "")} for d in batch]
    jf = os.path.join(os.environ.get("RUNNER_TEMP", "/tmp"), "release_batch.json")
    json.dump(jobs, open(jf, "w", encoding="utf-8"), ensure_ascii=False)
    try:
        subprocess.run([sys.executable, os.path.join(HERE, "scan_refs.py"),
                        "--file", jf, "--json", out_json],
                       cwd=ROOT, timeout=timeout,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        print(f"[release] 这批扫描超时（{timeout}s）—— 留库房，不当作干净")
    if not os.path.exists(out_json):
        return []
    d = json.load(open(out_json, encoding="utf-8"))
    return d if isinstance(d, list) else d.get("results", d.get("items", []))


def shelved_unscanned() -> list[dict]:
    """**已经在架、但还没扫过红线的。** 先发后审的「审」就是审这一批。

    2026-09-02 店主定了先发后审：文案齐就当轮上架，红线扫描挪到上架之后。
    好处是货架每天真的会动；代价是有命中的货会在架上停留最多一轮。
    **那个代价只有在「审真的发生」时才可接受** —— 所以这个函数每轮都跑，
    扫出命中的当场撤下并写 unshelf_reason，不能悄悄消失。
    """
    try:
        arch = set(json.load(open(os.path.join(ROOT, "scouts", "scan_archive.json"),
                                  encoding="utf-8"))["entries"])
    except Exception:
        arch = set()
    live = {x["id"] for x in json.load(open(os.path.join(ROOT, "skills", "feed.json"),
                                            encoding="utf-8"))["skills"]}
    out = []
    for f in glob.glob(os.path.join(ROOT, "skills", "*.json")):
        if f.endswith(("feed.json", "rejected-feed.json")):
            continue
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d["id"] in live and d["id"] not in arch:
            d["_file"] = f
            out.append(d)
    return out


def pull_down(items: list[tuple[dict, str]]) -> None:
    """撤下并留痕。**两层都要写** —— 人工层 curation.json 永远覆盖机器层，
    只改 skills/*.json 的 hide 不生效（2026-09-02 栽过两次）。"""
    cur_p = os.path.join(ROOT, "editorial", "curation.json")
    cur = json.load(open(cur_p, encoding="utf-8"))
    for d, why in items:
        f = d.get("_file")
        d2 = {k: v for k, v in d.items() if k != "_file"}
        d2["hide"] = True
        json.dump(d2, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        e = cur["items"].setdefault(d["id"], {})
        e["hide"] = True
        e["unshelf_reason"] = f"先发后审：上架后补扫命中红线 —— {why}"
    json.dump(cur, open(cur_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def main():
    ap = argparse.ArgumentParser(description="扫红线，干净的自动上架")
    ap.add_argument("--max", type=int, default=12, help="每轮最多处理几件（大仓库很慢）")
    ap.add_argument("--chunk", type=int, default=3, help="每批几件，分批防超时")
    ap.add_argument("--timeout", type=int, default=240, help="每批扫描超时秒数")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    # 先发后审：**先审在架的**（它们已经对访客可见，风险在这边），
    # 审完还有余额再顺手放行库房里的。
    onshelf = shelved_unscanned()
    held = held_items()
    todo = (onshelf + held)[:a.max]
    if not todo:
        print("[release] 在架的都扫过了，库房也没有文案齐的新货")
        return
    print(f"[release] 在架待补扫 {len(onshelf)} 件 · 库房待放行 {len(held)} 件"
          f" —— 本轮处理 {len(todo)} 件（在架的排前面）")
    live_ids = {x["id"] for x in json.load(open(os.path.join(ROOT, "skills", "feed.json"),
                                                encoding="utf-8"))["skills"]}

    released, kept = [], []
    tmp = os.path.join(os.environ.get("RUNNER_TEMP", "/tmp"), "release_scan.json")
    for i in range(0, len(todo), a.chunk):
        batch = todo[i:i + a.chunk]
        if os.path.exists(tmp):
            os.remove(tmp)
        res = scan(batch, tmp, a.timeout)
        by = {(r.get("repo"), r.get("path", "")): r for r in res}
        for d in batch:
            r = by.get((d["repo"], d.get("path", "")))
            if r is None:
                kept.append((d, "没扫到（超时或读不动）"))
                continue
            hits = r.get("hits") or []
            if hits:
                first = ""
                for h in hits[:1]:
                    fs = h.get("found") or []
                    if fs:
                        first = f'{h.get("file","")}: {fs[0].get("label","")} 第{fs[0].get("line","?")}行'
                kept.append((d, f"命中 {len(hits)} 处 · {first}"))
            else:
                released.append(d)
        time.sleep(1)

    # 在架的有命中 → 撤下；库房的有命中 → 本来就没上架，留着即可。
    pull = [(d, why) for d, why in kept if d["id"] in live_ids]
    if pull and not a.dry:
        pull_down(pull)
    if pull:
        print(f"\n[release] **撤下 {len(pull)} 件**（先发后审：上架后补扫命中红线）：")
        for d, why in pull:
            print(f'   ✗ {d.get("title_zh") or d.get("name")}  ({d["repo"]})  —— {why}')
    for d in released:
        if a.dry:
            continue
        f = d.pop("_file")
        d["hide"] = False
        json.dump(d, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"\n[release] 自动放行 {len(released)} 件：")
    for d in released:
        print(f'   ✓ {d.get("title_zh") or d.get("name")}  ({d["repo"]})')
    if kept:
        print(f"\n[release] 留库房 {len(kept)} 件（等人读原文再定）：")
        for d, why in kept:
            print(f'   · {d.get("title_zh") or d.get("name")}  ({d["repo"]})  —— {why}')
    rest = len(held) - len(todo)
    if rest > 0:
        print(f"\n[release] 库房还剩 {rest} 件排队，下轮继续")


if __name__ == "__main__":
    main()
