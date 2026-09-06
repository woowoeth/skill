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
        # 2026-09-06 店主定的底线（docs/COVERS.md）：**每一件在架的都必须有图。**
        # 此前这条是「注意」不是「坏」，理由是「一条永远红着的红灯会被人学会忽略」——
        # 结果就是它黄了两个月，货架上一半的卡没有脸（162/319）。
        # 红灯被忽略的解法不是把它调成黄灯，是把红的原因清掉。
        note("坏", f"{len(miss)} 张卡没有封面 —— 底线是每件都要有图；取不到作者的图就自己装上跑一遍截产出物，连这都做不到的下架",
             [f"第{items.index(x)+1}位 {x.get('title_zh','')[:26]}" for x in miss[:8]])
    # 外链封面：会死（private-user-images 是带签名会过期的地址），也让每个访客去 ping 第三方。
    # 一律本地化到 assets/covers/，站上只引自家路径。
    ext = [x for x in items if (x.get("cover") or "").startswith("http")]
    if ext:
        note("坏", f"{len(ext)} 张封面还是外链 —— 迟早死图；下载到 assets/covers/ 再引本地路径",
             [f"{x['id'][:40]} → {x['cover'][:60]}" for x in ext[:8]])
    # 每张图都要**有人打开看过**并判过 ok（docs/COVERS.md「判决怎么落地」）。
    # 字段齐不等于图对：二维码、赞助广告、作者头像、雪豹照片，从数据上一个都看不出来，
    # 只有看图才知道。判成 replace 的也算坏 —— 图不对，只是还没换。
    # 每张自家封面都要有 w800 派生图。没有的话，卡片先请求 w800/*.webp 撞 404，再
    # onerror 回退到 800KB 的原图 —— 首屏一排灰框、几百个 404。这就是「图打不开」
    # 在读者眼里的样子，而原图明明在盘上。派生图缺失多半是顺序错了：
    # make_thumbs 跑在 refresh 之前，按旧 feed 出的图。收口用 scouts/covers_publish.py。
    nothumb = []
    for x in items:
        c = x.get("cover") or ""
        if c.startswith("/skill/assets/covers/") and "/w800/" not in c:
            stem = os.path.splitext(os.path.basename(c))[0]
            if not os.path.exists(os.path.join(ROOT, "assets", "covers", "w800", stem + ".webp")):
                nothumb.append(x)
    if nothumb:
        note("坏", f"{len(nothumb)} 张封面没有 w800 派生图 —— 卡片会先 404 再回退原图，首屏一排灰框；跑 scouts/covers_publish.py",
             [x["id"][:48] for x in nothumb[:8]])
    # 封面必须有人打开看过（cover_verdict=ok）。但进货是自动的、判图是人做的，两者不同步：
    # 2026-09-06 早上这条闸第一次在 CI 上红，就是一件当轮新到的货 —— 它没坏，只是还没轮到人看。
    # 按 2026-09-02 的「先发后审」：新到货 48 小时内没判记「糙」，过了 48 小时还没人看才是「坏」。
    # 已经判了 replace / remove 却还挂着的，不享受宽限 —— 那是判完没执行。
    def _age_days(x):
        d = x.get("added_at") or x.get("cover_tried_at") or ""
        try:
            return (datetime.date.today() - datetime.date.fromisoformat(d[:10])).days
        except ValueError:
            return 999
    unj = [x for x in items if (x.get("cover") or "") and x.get("cover_verdict") != "ok"]
    fresh = [x for x in unj if not x.get("cover_verdict") and _age_days(x) <= 2]
    stale = [x for x in unj if x not in fresh]
    if fresh:
        note("糙", f"新到货 {len(fresh)} 张封面还没人过目（48 小时内，先发后审）—— 巡货时逐件看图写 cover_verdict",
             [f"{x['id'][:40]} · {(x.get('cover_verdict_why') or '')[:40]}" for x in fresh[:8]])
    if stale:
        byv = collections.Counter(x.get("cover_verdict") or "未判" for x in stale)
        note("坏", f"{len(stale)} 张封面没有过目判 ok（{'、'.join(f'{k} {v}' for k, v in byv.most_common())}）",
             [f"{x['id'][:40]} · {x.get('cover_verdict') or '未判'} · {(x.get('cover_verdict_why') or '')[:36]}" for x in stale[:8]])
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


def check_coverage() -> None:
    """流式全扫：**每一片**在最近 30 小时内有没有一轮「连上」。
    片是分班跑的（一班一片），所以不能只看最新一轮，要按片各自找最近一次成功。"""
    cov = os.path.join(ROOT, "editorial", "coverage_log.json")
    if not os.path.exists(cov):
        note("坏", "还没有覆盖账（stream.py 一次都没跑过）—— 「每天新发的都扫一遍」目前是空话", [])
        return
    runs = (json.load(open(cov, encoding="utf-8")).get("runs") or [])
    now = datetime.datetime.now(datetime.timezone.utc)
    ok_slices, bad = {}, []
    for r in runs:
        t = datetime.datetime.strptime(r["time"], "%Y-%m-%dT%H:%MZ").replace(tzinfo=datetime.timezone.utc)
        if (now - t).total_seconds() > 30 * 3600:
            break
        for sl in r.get("slices", []):
            if sl["status"] in ("连上", "无锚点（首轮）") and sl["slice"] not in ok_slices:
                ok_slices[sl["slice"]] = r["time"]
    for name in ("skills", "claude", "agents", "plugins", "rest"):
        if name not in ok_slices:
            bad.append(name)
    if bad:
        note("坏", f"这些片 30 小时内没有一轮接上：{', '.join(bad)} —— 那一段的新 SKILL.md 没看全", [])
    else:
        print(f"  ✓ 五片 30 小时内都接上过：" + " · ".join(f"{k}@{v[5:16]}" for k, v in ok_slices.items()))


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
    check_coverage()
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
