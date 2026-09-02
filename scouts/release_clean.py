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
        if not (d.get("why_zh") or "").strip():
            continue          # 没文案的不在本脚本管辖内
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


def main():
    ap = argparse.ArgumentParser(description="扫红线，干净的自动上架")
    ap.add_argument("--max", type=int, default=12, help="每轮最多处理几件（大仓库很慢）")
    ap.add_argument("--chunk", type=int, default=3, help="每批几件，分批防超时")
    ap.add_argument("--timeout", type=int, default=240, help="每批扫描超时秒数")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    held = held_items()
    if not held:
        print("[release] 库房里没有等着放行的（文案已写好的）新货")
        return
    todo = held[:a.max]
    print(f"[release] 库房 {len(held)} 件待放行，本轮处理 {len(todo)} 件")

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
