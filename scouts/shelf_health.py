#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""货架体检 —— 按**访客所见**查，不按数据结构查。

## 为什么有这个

2026-09-02 店主连着提了三次：「很多新增的都没图」「今天没上新」「能不能别让我
每次提醒你这些弱智问题」。三次都是他先看见、我后去修 —— 等于把体检外包给了店主。

已有的 check_curation 查的是**数据是否自洽**（字段齐不齐、存档对不对得上）。
它查不出「图挂了」「今天没上新」「同一个仓连着占了六张卡」——
那些要站在访客的位置上看：**打开站点、往下拉、点进去**。

所以这份只问一句：**一个访客现在打开站，会看到什么坏东西？**
每一条都必须是他肉眼能撞见的，不是内部字段不一致。
"""
from __future__ import annotations
import json, os, subprocess, sys, collections, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scouts"))
FEED = os.path.join(ROOT, "skills", "feed.json")

PROBLEMS: list[tuple[str, str, list]] = []


def note(level: str, title: str, detail: list) -> None:
    PROBLEMS.append((level, title, detail))


def load():
    return json.load(open(FEED, encoding="utf-8"))["skills"]


def check_covers(items, sample: int) -> None:
    """没图，以及**图挂了**。字段有值不等于图能显示 —— 这两件事分开查。"""
    miss = [x for x in items if not (x.get("cover") or x.get("cover_url"))]
    if miss:
        note("坏", f"{len(miss)} 张卡没有封面（访客下拉会撞到空洞）",
             [f"第{items.index(x)+1}位 {x.get('title_zh','')[:26]}" for x in miss[:8]])
    # 指向我们自己仓的封面**查本地文件**，不发 HTTP。
    # 2026-09-02 的坑：这一步在工作流里排在 Commit 之前，本轮新写的封面还没推上去，
    # raw.githubusercontent 自然 404 —— CI 里报「4 张打不开」，本地跑全 200。
    # **那不是货坏了，是体检站错了位置，而且会每轮误报。**
    # 本地文件在不在，才是「它推上去之后能不能显示」的正确判据。
    # 自家的封面查本地文件，外部的才发 HTTP。
    # **「自家」有两种写法**，都要认：
    #   /skill/assets/covers/…                              （同源相对路径，现在用这种）
    #   https://raw.githubusercontent.com/woowoeth/skill/HEAD/…（旧的绝对路径）
    # 2026-09-02 栽过一次：改成同源相对路径之后，体检还拿它当完整 URL 去 curl，
    # 相对路径 curl 不了，15 张里 11 张报 000 —— **不是货坏了，是我改了一头没改另一头**。
    def local_rel(u: str) -> str | None:
        if u.startswith("/skill/"):
            return u[len("/skill/"):]
        marker = "/woowoeth/skill/HEAD/"
        return u.split(marker, 1)[1] if marker in u else None

    urls, missing_local = [], []
    for x in items:
        u = x.get("cover") or x.get("cover_url")
        if not u:
            continue
        rel = local_rel(u)
        if rel is not None:
            if not os.path.exists(os.path.join(ROOT, rel)):
                missing_local.append(f"{x['id']} → {rel}")
        else:
            urls.append((x["id"], u))
    if missing_local:
        note("坏", f"{len(missing_local)} 张封面写着我们仓里的路径，但文件不存在",
             missing_local[:6])
    else:
        n_ours = sum(1 for x in items if local_rel(x.get("cover") or x.get("cover_url") or "") is not None)
        print(f"  ✓ 自家仓封面 {n_ours} 张，文件都在")
    step = max(1, len(urls) // sample) if sample else 1
    probe = urls[::step][:sample] if sample else urls
    dead = []
    for i, u in probe:
        r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                            "-L", "--max-time", "20", u], capture_output=True, text=True)
        if r.stdout.strip() != "200":
            dead.append(f"{r.stdout.strip()} {i}")
    if dead:
        note("坏", f"抽查 {len(probe)} 张封面，{len(dead)} 张打不开", dead[:8])
    else:
        print(f"  ✓ 抽查 {len(probe)} 张封面全部 200")


def check_copy(items) -> None:
    """卡片上印着的每一句都得有。缺一句，访客看到的就是缺角的卡。"""
    for f, cn in (("title_zh", "标题"), ("tagline_zh", "卖点"),
                  ("why_zh", "理由"), ("limit_zh", "局限")):
        bad = [x for x in items if not (x.get(f) or "").strip()]
        if bad:
            note("坏", f"{len(bad)} 件缺{cn}（{f}）",
                 [x.get("title_zh") or x["id"] for x in bad[:6]])


def check_freshness(items) -> None:
    """今天上新了没有。**这是这家店的承诺**，没做到就是坏的。

    按「今天新出现在货架上的 id」算，**不按 added_at 算**。
    第一版按 added_at，结果刚放行的 5 件（09-01 进的货、今天才上架）
    被算成「今天 0 件」—— 访客感知的是**货架今天有没有变**，
    不是这批货哪天进的库。口径错了，体检就会在没坏的时候报坏、
    在坏的时候报好。
    """
    today = datetime.date.today().isoformat()
    now = {x["id"] for x in items}
    since = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    r = subprocess.run(["git", "log", "--format=%H", f"--until={since}T23:59:59",
                        "-1", "--", "skills/feed.json"],
                       capture_output=True, text=True, cwd=ROOT)
    base = (r.stdout or "").strip()
    if not base:
        print("  · 查不到昨天的 feed（仓库历史太浅），今日上新这条跳过")
        return
    old = subprocess.run(["git", "show", f"{base}:skills/feed.json"],
                         capture_output=True, cwd=ROOT).stdout
    try:
        prev = {x["id"] for x in json.loads(old)["skills"]}
    except Exception:
        print("  · 昨天的 feed 读不出来，今日上新这条跳过")
        return
    new_ids = now - prev
    gone = prev - now
    if not new_ids:
        note("坏", f"今天（{today}）货架一件没多 —— 昨天收盘 {len(prev)} 件，现在 {len(now)} 件",
             ["库房里有够格的就跑 scouts/release_clean.py；"
              "一件都没有说明进货或写文案那一环断了"])
    else:
        print(f"  ✓ 今天上架 {len(new_ids)} 件"
              + (f"（另有 {len(gone)} 件下架）" if gone else ""))


def check_clumping(items) -> None:
    """同一个仓连着占好几张卡，下拉时看着像重复内容。实测店主为此抱怨过。"""
    run, worst, cur = 1, (1, ""), None
    for x in items:
        r = x.get("repo")
        run = run + 1 if r == cur else 1
        cur = r
        if run > worst[0]:
            worst = (run, r)
    if worst[0] >= 4:
        note("糙", f"同一个仓连着占了 {worst[0]} 张卡：{worst[1]}", [])


def main() -> int:
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--sample", type=int, default=25, help="抽查多少张封面（0=全查）")
    a = ap.parse_args()
    items = load()
    print(f"货架体检 —— 在架 {len(items)} 件\n")
    check_covers(items, a.sample)
    check_copy(items)
    check_freshness(items)
    check_clumping(items)
    if not PROBLEMS:
        print("\n✓ 访客现在打开站，看不到坏东西")
        return 0
    print()
    bad = 0
    for level, title, detail in PROBLEMS:
        print(f"{'✗ 坏' if level == '坏' else '· 糙'}  {title}")
        for d in detail:
            print(f"       {d}")
        bad += level == "坏"
    print(f"\n{bad} 条坏 / {len(PROBLEMS)-bad} 条糙")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
