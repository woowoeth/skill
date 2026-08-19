#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宽漏斗 · 遍历式抓取 / wide funnel.

回答的不是「扫完了没有」——**扫完不可能**，生态 266 万条。回答的是：
**扫到哪、还剩多少没碰、为什么碰不到。** 所以每个源都要落一张覆盖率账，
拿不到的部分写清原因，不许写「已全量覆盖」。

## 源与它们的可达性（2026-08-19 实测 robots.txt，逐条核过）

| 源 | 可达性 | 依据 |
|---|---|---|
| skills.sh **sitemap** | ✅ 可枚举 | robots.txt 主动公布 `Sitemap:`，2 个分片各 10000 条 |
| skills.sh **单件页** | ✅ 可读 | robots 只禁 `/internal/ /debug-security/ /search /api/` |
| skills.sh **`/api/search`** | ❌ **robots 明令 Disallow: /api/** | 上一轮的 funnel 走的就是这个口，见模块尾注 |
| GitHub search API | ✅ 10 次/分钟（未认证） | 官方限流 |
| GitHub REST core | ⚠️ 60 次/小时（未认证） | 没 token，能省则省 |
| SkillsMP 页面 | ✅ Crawl-delay 1 | robots 允许，只禁 `/api/` `/auth/` |
| Gitee 搜索 | ❌ **拿不到** | 搜索页是 SPA，数据走 `/api/v*`，robots 明令 Disallow |
| GitCode 搜索 | ❌ **拿不到** | robots 禁 `/search` 且禁 `/*?*`（一切带查询串的 URL） |
| YouMind 画廊 | ❌ **不许抓** | robots 里 `User-agent: ClaudeBot` → `Disallow: /` |
| 小红书 / 公众号 / X | ❌ 不抓 | robots 拒；按 CURATION.md 记为「只能靠人工指路的盲区」 |

**skills.sh 的 `/api/search` 这条要单独说：** `scouts/enrich.py` 的 `cmd_funnel`
打的是 `https://skills.sh/api/search`，而 skills.sh 的 robots.txt 写着 `Disallow: /api/`。
本模块**不走那个口**，改用它自己公布的 sitemap 枚举 + 单件页读元数据 —— 更全
（sitemap 是全量清单，搜索只给命中），也不违反站点的意愿。

用法：
  python3 scouts/wide_funnel.py sitemap      # 拉 skills.sh sitemap，落 owner/repo/skill 清单
  python3 scouts/wide_funnel.py github       # GitHub 搜索 API 跑垂直词表
  python3 scouts/wide_funnel.py detail       # 给候选拉 skills.sh 单件页（装机量 + 原始描述）
  python3 scouts/wide_funnel.py coverage     # 只输出覆盖率表，不联网

零第三方依赖。所有中间产物落在 scouts/.funnel/ 下，可断点续跑。
"""
from __future__ import annotations
import os, re, sys, json, time, datetime, argparse, urllib.parse, urllib.request
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "scouts", ".funnel")
UA = "Mozilla/5.0 (compatible; ourword-skill-scout/1.0; +https://ourword.ai/skill/)"
TODAY = datetime.date.today().isoformat()

# ---------------------------------------------------------------- 垂直词表 ---
# 上一轮实测：扫约 6000 条粗筛出 164 件，其中 **159 件是中文**。这不是巧合——
# 大市场是英文爬虫、英文搜索，中文创作者的东西在那边基本不存在。所以词表以中文
# 垂直为主，每个方向给多个同义词和行话（只查一个词会漏掉一半，「八字」和「命理」
# 「排盘」捞到的是不同的人）。
#
# 前 17 组是产品给的方向；`_EXTRA` 是本轮新增的，理由写在各组注释里——
# 都来自读完 150 多份已上架正文之后看到的空白，不是拍脑袋列的。
VERTICALS: dict[str, list[str]] = {
    "公文体制内": ["公文", "公文写作", "体制内", "事业单位", "党建", "申论", "行测",
                 "公务员", "述职报告", "会议纪要", "政务", "红头文件", "材料狗"],
    "命理": ["八字", "命理", "紫微斗数", "六爻", "奇门遁甲", "塔罗", "周易", "占卜",
            "排盘", "梅花易数", "六壬", "星盘", "占星"],
    "中医": ["中医", "方剂", "针灸", "脉诊", "倪海厦", "伤寒论", "本草", "艾灸",
            "推拿", "药膳", "经络", "辨证论治"],
    "过敏慢病": ["花粉", "过敏", "哮喘", "血糖", "血压", "痛风", "甲状腺", "糖尿病",
                "慢病", "体检报告"],
    "宠物母婴": ["宠物", "养猫", "养狗", "铲屎官", "猫咪", "育儿", "母婴", "辅食",
                "绘本", "亲子", "孕期", "疫苗接种"],
    "跑团桌游": ["跑团", "trpg", "剧本杀", "桌游", "dnd", "克苏鲁", "coc跑团", "地下城主"],
    "学科竞赛": ["数学建模", "信息学奥赛", "物理竞赛", "acm", "奥数", "美赛", "数模",
                "noip", "强基计划"],
    "方言非遗": ["方言", "粤语", "闽南语", "四川话", "东北话", "上海话", "非遗",
                "汉服", "剪纸", "民俗", "节气", "皮影"],
    "农业养殖": ["农业", "种植", "养殖", "农技", "病虫害", "水产", "果树", "大棚"],
    "法律实务": ["法律", "合同审查", "劳动仲裁", "法考", "民法典", "离婚", "工伤",
                "知识产权", "普法"],
    "财税社保": ["财税", "报税", "发票", "社保", "公积金", "个税", "会计分录", "医保"],
    "考公考编考研": ["考公", "考编", "考研", "教师资格", "事业编", "调剂", "择校"],
    "房产装修": ["房产", "装修", "买房", "户型", "验房", "软装", "家装预算"],
    "钓鱼户外观鸟": ["钓鱼", "路亚", "露营", "徒步", "观鸟", "登山", "越野跑"],
    "手工": ["编织", "木工", "陶艺", "钩针", "皮具", "手账", "拼装模型"],
    "戏曲书法篆刻": ["戏曲", "京剧", "书法", "篆刻", "国画", "碑帖", "昆曲"],
    "地方生活": ["北京", "上海", "广州", "深圳", "成都", "杭州", "西安", "重庆",
                "武汉", "南京"],
    # ---- 以下为本轮新增 ----
    # 起名是中文世界最硬的刚需之一（新生儿、公司、商标），且天然带命理/音韵/字义，
    # 英文市场完全没有对应品类。上一轮词表里一个词都没有。
    "_EXTRA_起名择日": ["起名", "取名", "宝宝取名", "公司起名", "择日", "黄历", "风水",
                      "看日子"],
    # 已上架的 campus-resume / 公文类说明「中国职场的特殊形态」这条脉有货，
    # 但上一轮只查了「简历」一个词。
    "_EXTRA_中国职场": ["周报", "日报", "OKR", "绩效面谈", "述职", "简历", "面试",
                      "国企", "央企", "跳槽", "背调"],
    # 情绪/心理是中文创作者近两年最集中的自助方向，且「冷门但对的人极有用」。
    "_EXTRA_心理情绪": ["情绪", "心理咨询", "正念", "冥想", "拖延", "内耗", "原生家庭",
                      "CBT", "情绪日记", "抑郁"],
    # 上架的 fitness-coach-rpg 属这条；饮食/减脂是同一批人的相邻需求。
    "_EXTRA_饮食健身": ["菜谱", "家常菜", "减脂餐", "烘焙", "健身计划", "增肌", "轻断食",
                      "川菜", "粤菜"],
    # 中小学教育是中文互联网体量最大的垂直之一，上一轮词表完全没覆盖。
    "_EXTRA_基础教育": ["小学", "初中", "高考", "错题本", "作文批改", "家长会", "学习计划",
                      "英语启蒙"],
    # 已上架有「网文/小说做成游戏」，说明中文创作侧有人在做，但只查了「写作」。
    "_EXTRA_内容创作": ["网文", "小说", "短视频脚本", "播客", "分镜", "标题党", "选题",
                      "自媒体", "小红书文案"],
    # 二次元/手游攻略是中文社区最活跃的内容生产地之一。
    "_EXTRA_游戏二次元": ["原神", "崩坏", "攻略", "抽卡", "阴阳师", "同人", "galgame"],
    # 「里程玩家」已上架说明这类玩家型垂直有效；车/收藏是同构的中文玩家社群。
    "_EXTRA_玩家垂直": ["新能源车", "二手车", "选车", "球鞋", "乐高", "手办", "集邮",
                      "古玩", "咖啡豆"],
    # 适老与养老在中文世界是刚起来的刚需，英文市场语境完全不同。
    "_EXTRA_适老养老": ["养老", "退休", "适老化", "老年人", "养老金"],
}

# ---- 对照组 ----
# 为什么要有对照组：本轮我差点报一个**循环论证**得来的结论 ——
# 「中文候选里只有 0.3% 被 skills.sh 收录，非中文有 78%」。78% 那个数是假的，
# 因为那批非中文仓库本来就是**从 skills.sh 的 sitemap 里拿的**，100% 在里面是构造出来的。
#
# 干净地只看 GitHub 搜索独立发现的那批，中文 0.28% / 非中文 0.16% —— **没有差距**。
# 但那个非中文对照组只有 634 个，且是被中文查询顺带捞到的，不能代表英文垂直。
# 所以这里放一组**同概念的英文垂直词**做真对照：如果英文垂直也是 0.2%，
# 那么「skills.sh 漏掉中文」这个说法就不成立，成立的只是「skills.sh 漏掉 GitHub 长尾」——
# 两者对产品定位的含义完全不同，不能混。
CONTROL_EN = [
    "tarot", "astrology", "feng shui", "traditional chinese medicine", "acupuncture",
    "herbal medicine", "resume", "cover letter", "civil service exam", "bar exam",
    "tax filing", "bookkeeping", "recipe", "meal prep", "baking",
    "fishing", "birdwatching", "hiking", "knitting", "woodworking", "pottery",
    "calligraphy", "gardening", "beekeeping", "pet care", "parenting",
    "real estate", "home renovation", "car buying", "retirement planning",
]

# 「点子够怪」那一路——CURATION.md 优先收的第二类。这些不限中文。
ODD_QUERIES = [
    "skill that eats other skills", "caveman speak", "handwriting to font",
    "novel to game", "zine poster", "pixel art skill", "dream journal",
    "tarot claude skill", "feng shui skill", "constructed language",
]


# ------------------------------------------------------------------ 工具 ---
# 请求节流的**实测**记录。教训：限频不能算，要量。
# 本轮踩过 —— 纸上算「3 并发 × 0.5 秒 sleep ≈ 2 请求/秒」，实测是 4.44 请求/秒，
# 因为页面返回比估的快，sleep 根本不是瓶颈。
#
# 所以不止记内存计数，还逐条落 `scouts/.funnel/requests.jsonl`：
# `{ts, host, status}`。跑完能算**真实 QPS 和最大瞬时并发**，写进覆盖率表——
# 而不是「隔 40 秒读一次页数取差」那种二手估计。给别人服务器的负担也是个数字，
# 没核过的数字不许当结论用，这条对内对外一样。
_REQ_TS: list[float] = []
_REQ_LOG = None


def _log_req(url: str, status: int) -> None:
    global _REQ_LOG
    t = time.time()
    _REQ_TS.append(t)
    try:
        if _REQ_LOG is None:
            os.makedirs(CACHE, exist_ok=True)
            _REQ_LOG = open(os.path.join(CACHE, "requests.jsonl"), "a", encoding="utf-8")
        host = urllib.parse.urlparse(url).netloc
        _REQ_LOG.write(json.dumps({"ts": round(t, 3), "host": host, "status": status}) + "\n")
        _REQ_LOG.flush()
    except Exception:
        pass


def rate_report(path: str | None = None) -> str:
    """从 jsonl 算真实速率。**逐 host 分别算** —— 混在一起的平均值没有意义，
    对面是两台不同的服务器，各自感受到的负担才是要报的数。"""
    path = path or os.path.join(CACHE, "requests.jsonl")
    rows = []
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    if len(rows) < 2:
        return "请求数不足，无法测速"
    by: dict[str, list[float]] = {}
    for r in rows:
        by.setdefault(r["host"], []).append(r["ts"])
    out = []
    for host, ts in sorted(by.items(), key=lambda x: -len(x[1])):
        ts.sort()
        span = ts[-1] - ts[0]
        qps = len(ts) / span if span > 0 else 0
        # 最大瞬时并发的下界：任意 1 秒窗口内的最大请求数
        peak, j = 0, 0
        for i, t in enumerate(ts):
            while ts[i] - ts[j] > 1.0:
                j += 1
            peak = max(peak, i - j + 1)
        out.append(f"{host}: {len(ts)} 请求 / {span:.0f} 秒 = {qps:.2f} QPS"
                   f"（等效 crawl-delay {1 / qps if qps else 0:.2f} 秒；峰值 {peak} 请求/秒）")
    return " ｜ ".join(out)


def _get(url: str, timeout: int = 30, accept: str = "*/*") -> tuple[int, bytes]:
    """先走 urllib，证书链验不过时退回 curl。

    坑记录（`enrich.py` 里也踩过）：本机到部分站点之间有一层 TLS 拦截代理，
    它的根证书装在系统钥匙串里，curl 认，Python 自带的 OpenSSL 不认。
    退回 curl **不是关掉校验** —— curl 照样按系统信任库验，只是它认这条链。
    """
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            _log_req(url, r.status)
            return r.status, data
    except urllib.error.HTTPError as e:
        _log_req(url, e.code)
        return e.code, b""
    except Exception:
        pass
    import shutil, subprocess
    if not shutil.which("curl"):
        return 0, b""
    try:
        p = subprocess.run(
            ["curl", "-sSL", "-m", str(timeout), "-A", UA, "-H", f"Accept: {accept}",
             "-w", "\n%{http_code}", url], capture_output=True, timeout=timeout + 15)
        if p.returncode != 0:
            _log_req(url, 0)
            return 0, b""
        out = p.stdout
        i = out.rfind(b"\n")
        code = int(out[i + 1:].strip() or 0)
        _log_req(url, code)
        return code, out[:i]
    except Exception:
        return 0, b""


def _save(name: str, obj) -> str:
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    return p


def _load(name: str, default):
    p = os.path.join(CACHE, name)
    if not os.path.exists(p):
        return default
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


# --------------------------------------------------------------- sitemap ---
def cmd_sitemap(_args) -> None:
    """skills.sh 自己公布的全量清单。这是我们能拿到的最诚实的分母。"""
    st, body = _get("https://www.skills.sh/sitemap.xml", accept="application/xml")
    if st != 200:
        print(f"[funnel] sitemap 索引取不到（HTTP {st}），放弃这个源，不猜数")
        return
    shards = re.findall(r"<loc>([^<]+)</loc>", body.decode("utf-8", "replace"))
    skill_shards = [s for s in shards if "sitemap-skills" in s]
    print(f"[funnel] sitemap 索引：{len(shards)} 个分片，其中 skill 分片 {len(skill_shards)} 个")
    rows, per_shard = [], {}
    for s in skill_shards:
        st, body = _get(s, timeout=90, accept="application/xml")
        if st != 200:
            print(f"[funnel] ! 分片取不到 {s} (HTTP {st}) —— 这一片的量记为未知，不估算")
            per_shard[s] = None
            continue
        urls = re.findall(r"<loc>([^<]+)</loc>", body.decode("utf-8", "replace"))
        per_shard[s] = len(urls)
        for u in urls:
            p = u.replace("https://www.skills.sh/", "").split("/")
            if len(p) == 3:
                rows.append(p)
        print(f"[funnel] {s.rsplit('/', 1)[-1]:24s} {len(urls)} 条")
    repos = sorted({f"{o}/{r}" for o, r, _ in rows})
    _save("sitemap_index.json", {"rows": rows, "per_shard": per_shard})
    print(f"[funnel] 合计 {len(rows)} 件 skill / {len(repos)} 个仓库 / "
          f"{len({r[0] for r in rows})} 个 owner")
    if per_shard and all(v == 10000 for v in per_shard.values() if v is not None):
        print("[funnel] ⚠ 每个分片都正好 10000 条 —— 这多半是分片上限，"
              "**不能**据此说「skills.sh 一共就这么多」。总量未知，如实记未知。")


# ---------------------------------------------------------- GitHub 搜索 ---
GH_SEARCH = ("https://api.github.com/search/repositories?q={q}"
             "&sort=updated&order=desc&per_page=100&page={page}")
# 未认证 10 次/分钟。留 15% 余量，别把别人的额度也用光。
GH_SLEEP = 7.0


def gh_search(term: str, page: int = 1) -> tuple[int | None, list[dict]]:
    """返回 (total_count, items)。取不到就返回 (None, []) —— None 表示未知，不是 0。"""
    q = urllib.parse.quote(f'{term} skill')
    st, body = _get(GH_SEARCH.format(q=q, page=page), timeout=40,
                    accept="application/vnd.github+json")
    if st != 200:
        return None, []
    try:
        d = json.loads(body)
        return d.get("total_count"), d.get("items", [])
    except Exception:
        return None, []


def _absorb(done: dict, group: str, term: str, items: list[dict]) -> None:
    for it in items:
        full = it.get("full_name", "")
        if not full:
            continue
        r = done["repos"].setdefault(full, {
            "repo": full, "stars": it.get("stargazers_count", 0),
            "desc": (it.get("description") or "")[:300],
            "pushed_at": (it.get("pushed_at") or "")[:10],
            "created_at": (it.get("created_at") or "")[:10],
            "fork": bool(it.get("fork")), "lang": it.get("language") or "",
            "topics": it.get("topics") or [], "groups": [], "terms": [],
        })
        if group not in r["groups"]:
            r["groups"].append(group)
        if term not in r["terms"]:
            r["terms"].append(term)


def cmd_github(args) -> None:
    if args.control:
        terms = [("_对照组英文垂直", t) for t in CONTROL_EN]
    else:
        terms = [(g, t) for g, ts in VERTICALS.items() for t in ts]
        if not args.no_odd:
            terms += [("_怪点子", t) for t in ODD_QUERIES]
    done = _load("github_raw.json", {"repos": {}, "queries": {}})

    if args.paginate:
        # 单页上限 100，命中更多的查询**默认是漏掉的**。GitHub 搜索最多给到
        # 1000 条（10 页），再往后接口自己就不给了 —— 那部分记进覆盖率表，不假装拿到了。
        gmap = {t: g for g, t in terms}
        capped = [(t, v) for t, v in done["queries"].items()
                  if (v.get("total_count") or 0) > v.get("returned", 0)]
        print(f"[funnel] 需要翻页的查询 {len(capped)} 条")
        for t, v in sorted(capped, key=lambda x: -(x[1]["total_count"] or 0)):
            pages = min(10, -(-(v["total_count"]) // 100))
            got = v.get("returned", 0)
            for pg in range(1 + v.get("pages_done", 1), pages + 1):
                total, items = gh_search(t, pg)
                if total is None:
                    # 失败也要退避。第一版这里直接 break 进下一条查询，**不 sleep**，
                    # 于是连续几条失败会挤成一个突发 —— 实测把 api.github.com 的
                    # 峰值顶到 4 请求/秒，而我自己定的是 7 秒一条。
                    # 失败最可能的原因就是被限流，这时候更该慢，不是更快。
                    print(f"[funnel] ! {t} 第 {pg} 页取不到，退避后停在这里，如实记")
                    time.sleep(GH_SLEEP * 3)
                    break
                _absorb(done, gmap.get(t, v.get("group", "?")), t, items)
                got += len(items)
                v["returned"] = got
                v["pages_done"] = pg
                print(f"[funnel] 翻页 {t:14s} p{pg} +{len(items):3d} → 累计取回 {got}/{total}")
                time.sleep(GH_SLEEP)
            v["capped_at"] = 1000 if (v["total_count"] or 0) > 1000 else None
            _save("github_raw.json", done)
        _save("github_raw.json", done)
        print(f"[funnel] 翻页完成。去重仓库 {len(done['repos'])} 个")
        print(f"[funnel] 限频自查：{rate_report()}")
        return

    todo = [(g, t) for g, t in terms if t not in done["queries"]]
    print(f"[funnel] 词表 {len(terms)} 条，已跑 {len(terms) - len(todo)} 条，本次跑 {len(todo)} 条")
    print(f"[funnel] 未认证搜索限流 10 次/分钟，每条间隔 {GH_SLEEP}s，预计 {len(todo) * GH_SLEEP / 60:.0f} 分钟")
    for i, (group, term) in enumerate(todo, 1):
        total, items = gh_search(term)
        if total is None:
            print(f"[funnel] ! {term} 取不到（限流或网络），记未知，继续")
            time.sleep(GH_SLEEP * 2)
            continue
        done["queries"][term] = {"group": group, "total_count": total,
                                 "returned": len(items), "pages_done": 1}
        _absorb(done, group, term, items)
        print(f"[funnel] [{i}/{len(todo)}] {group:16s} {term:14s} "
              f"total={total:<7d} 取回 {len(items):3d}  累计仓库 {len(done['repos'])}")
        if i % 20 == 0:
            _save("github_raw.json", done)
        time.sleep(GH_SLEEP)
    _save("github_raw.json", done)
    print(f"[funnel] 完成。去重仓库 {len(done['repos'])} 个，查询 {len(done['queries'])} 条")
    print(f"[funnel] 限频自查：{rate_report()}")


# --------------------------------------------- skills.sh 单件页（装机量）---
LD_APP = re.compile(r'<script type="application/ld\+json">(\{"@context".*?"SoftwareApplication".*?)</script>', re.S)
LD_COUNT = re.compile(r'"userInteractionCount":\s*(\d+)')


def skill_page(owner: str, repo: str, skill: str) -> dict | None:
    """读 skills.sh 单件页里的 JSON-LD：真实装机量 + 原始 description。

    装机量是几千人用脚投票，按上一轮实测这是最可靠的信号
    （真实安装量 > frontmatter description > README 首段 > 星数）。
    """
    url = f"https://www.skills.sh/{owner}/{repo}/{skill}"
    st, body = _get(url, timeout=40)
    if st != 200:
        return None
    t = body.decode("utf-8", "replace")
    m = LD_APP.search(t)
    installs = None
    c = LD_COUNT.search(t)
    if c:
        installs = int(c.group(1))
    desc = ""
    if m:
        try:
            desc = (json.loads(m.group(1)).get("description") or "").strip()
        except Exception:
            blob = m.group(1)
            d = re.search(r'"description":"(.*?)","', blob)
            desc = d.group(1) if d else ""
    return {"owner": owner, "repo": repo, "skill": skill, "url": url,
            "installs": installs, "desc": desc}


def cmd_detail(args) -> None:
    targets = _load("detail_targets.json", [])
    if not targets:
        print("[funnel] 没有 detail_targets.json —— 先跑 sitemap/github 并生成候选清单")
        return
    out = _load("detail.json", {})
    todo = [t for t in targets if "/".join(t) not in out]
    print(f"[funnel] 待拉 {len(todo)} 件（已有 {len(out)}）")
    for i, (o, r, s) in enumerate(todo, 1):
        d = skill_page(o, r, s)
        key = f"{o}/{r}/{s}"
        out[key] = d or {"owner": o, "repo": r, "skill": s, "installs": None,
                         "desc": "", "_note": "页面取不到，留空不猜"}
        if i % 25 == 0:
            _save("detail.json", out)
            print(f"[funnel] {i}/{len(todo)} …")
        time.sleep(args.delay)
    _save("detail.json", out)
    got = sum(1 for v in out.values() if v.get("installs") is not None)
    print(f"[funnel] 完成 {len(out)} 件，其中拿到装机量 {got} 件，取不到 {len(out) - got} 件（留空）")


# ------------------------------------------- skills.sh 仓库页（装机量全量）---
# 一次仓库页请求就能拿到：仓库总装机量 + 每件 skill 的装机量 + 件数。
# 比逐件拉单件页省 8 倍请求（20000 件 skill 只分布在 2447 个仓库上）。
# 逐个 <a> 块解析。**不要**写成一条跨块的贪婪正则 —— 那样第一行会被前面的
# href 吃掉（实测 29 件只解析出 28 件，静默少一件正是我们最该避免的错法）。
ANCHOR_RE = re.compile(r'<a class="group grid[^"]*"\s+href="/([^/"]+)/([^/"]+)/([^"]+)"')
CELL_RE = re.compile(r'<h3[^>]*>([^<]+)</h3>.*?'
                     r'<span class="font-mono text-sm text-foreground">([\d.]+[KM]?)</span>', re.S)
TOTAL_RE = re.compile(r'</svg>([\d.]+[KM]?)<!-- --> total installs')
DESC_RE = re.compile(r'<meta name="description" content="([^"]*)"')


def _num(s: str) -> int:
    """把 "6.6K" / "122.1K" / "3" 变成整数。

    注意：站点显示的就是**四舍五入后的缩写**，1.2K 的真值可能是 1150-1249 中任何一个。
    所以入库时同时记 `installs_rounded: true` —— 这个数只能用来排序和分档，
    不能当精确值印出去。这正是我们已经踩过三次的那类坑（拿没核过精度的数当卖点）。
    """
    s = s.strip()
    mult = 1
    if s.endswith("K"):
        mult, s = 1000, s[:-1]
    elif s.endswith("M"):
        mult, s = 1000000, s[:-1]
    try:
        return int(float(s) * mult)
    except Exception:
        return 0


def repo_page(full: str) -> dict | None:
    st, body = _get(f"https://www.skills.sh/{full}", timeout=40)
    if st != 200:
        return None
    t = body.decode("utf-8", "replace")
    skills, anchors = [], list(ANCHOR_RE.finditer(t))
    for i, m in enumerate(anchors):
        o, r, sk = m.group(1), m.group(2), m.group(3)
        if f"{o}/{r}" != full:
            continue
        end = anchors[i + 1].start() if i + 1 < len(anchors) else min(len(t), m.end() + 1200)
        c = CELL_RE.search(t, m.end(), end)
        if not c:
            continue
        skills.append({"skill": sk, "name": c.group(1).strip(), "installs": _num(c.group(2))})
    tot = TOTAL_RE.search(t)
    d = DESC_RE.search(t)
    return {"repo": full, "total_installs": _num(tot.group(1)) if tot else None,
            "installs_rounded": True, "skills": skills,
            "meta_desc": d.group(1) if d else ""}


def cmd_repos(args) -> None:
    import concurrent.futures as cf
    sm = _load("sitemap_index.json", {})
    repos = sorted({f"{o}/{r}" for o, r, _ in sm.get("rows", [])})
    if not repos:
        print("[funnel] 先跑 sitemap")
        return
    out = _load("repo_pages.json", {})
    todo = [r for r in repos if r not in out]
    print(f"[funnel] skills.sh 仓库页 {len(repos)} 个，已有 {len(out)}，本次拉 {len(todo)}")

    def one(full):
        time.sleep(args.delay)
        return full, repo_page(full)

    done = 0
    with cf.ThreadPoolExecutor(args.workers) as ex:
        for full, d in ex.map(one, todo):
            out[full] = d or {"repo": full, "total_installs": None,
                              "skills": [], "_note": "页面取不到，留空不猜"}
            done += 1
            if done % 100 == 0:
                _save("repo_pages.json", out)
                print(f"[funnel] {done}/{len(todo)} …")
    _save("repo_pages.json", out)
    ok = sum(1 for v in out.values() if v.get("total_installs") is not None)
    print(f"[funnel] 完成 {len(out)} 个仓库，拿到装机量 {ok} 个，取不到 {len(out) - ok} 个（留空）")
    print(f"[funnel] 限频自查：{rate_report()}")


# --------------------------------------------------------------- 候选池 ---
# 机器只负责**筛掉**，挑不出。这一段的产出是「候选池 + 足够的信号」，
# 排序只是为了让人按顺序读，**不是打分决定上架**。判断那关永远是人在把。
CJK = re.compile(r"[\u4e00-\u9fff]")
# 对应 docs/CURATION.md 第四节的命名黑名单 + 问一里的「不是商品」那几类。
NAME_DENY = re.compile(
    r"(^|[-_/])(awesome|dotfiles|template|templates|boilerplate|starter|scaffold|"
    r"tutorial|tutorials|guide|guides|handbook|cheatsheet|cheat-sheet|course|"
    r"example|examples|demo|playground|sandbox|test|tests|workshop|learning|"
    r"study|notes|blog|portfolio|resume-template)($|[-_/])", re.I)


# ---- 红线 · 绕反爬 ----
# CURATION.md 红线第二条：「恶意代码、**绕反爬**、批量盗号等灰产」。
# 本轮新加，因为已经踩过两次：`browser-act`（CLI 自带 solve-captcha 上传验证码图）、
# `story-long-scan`（随件附带解码番茄字体反爬的脚本）。两件都有正当目的、其中一件
# 还在局限里如实披露了 —— **如实披露不豁免行为本身**，字体混淆和验证码是比
# robots.txt 更明确的「别抓」信号。
#
# 分两档，因为「爬虫」本身不是红线，**绕过对方的防抓措施**才是：
#   HARD —— 命中即记红线，理由里引出命中的原词，不做「可能」的措辞
#   SOFT —— 只标记待人看，不自动拒；单独一个「爬虫」「reverse engineering」不定罪
RED_SCRAPE_HARD = re.compile(
    r"(反爬|绕过反爬|破解反爬|字体反爬|字体加密|字形还原|滑块验证|验证码识别|打码平台|"
    r"过验证码|自动过码|风控绕过|签名逆向|sign\s*算法逆向|"
    r"bypass\s*(anti[- ]?bot|captcha|cloudflare|waf|rate\s*limit)|"
    r"captcha\s*(solver|solving|bypass)|solve[-_ ]?captcha|anti[- ]?detect|"
    r"undetected[-_ ]?chromedriver|cf[-_ ]?clearance)", re.I)
RED_SCRAPE_SOFT = re.compile(
    r"(逆向|爬虫|抓取|采集|scraper|scraping|crawler|headless\s*browser|"
    r"reverse[- ]engineer)", re.I)


def _chinese_ratio(text: str) -> float:
    t = (text or "").strip()
    return (len(CJK.findall(t)) / len(t)) if t else 0.0


def cmd_candidates(_args) -> None:
    sys.path.insert(0, os.path.join(ROOT, "scouts"))
    import scout_lib as lib

    items = lib.apply_editorial(lib.load_items())
    on_shelf = {i["repo"].lower() for i in items.values() if not i.get("hide")}
    known = {i["repo"].lower() for i in items.values()}
    seen = {r.lower() for r in lib.load_sources().get("repos", {})}

    gh = _load("github_raw.json", {"repos": {}, "queries": {}})
    pages = _load("repo_pages.json", {})
    sm = _load("sitemap_index.json", {})
    sm_repos = {f"{o}/{r}" for o, r, _ in sm.get("rows", [])}

    pool: dict[str, dict] = {}
    for full, r in gh["repos"].items():
        pool[full] = dict(r, found_by=["github-search"])
    for full in sm_repos:
        rec = pool.setdefault(full, {"repo": full, "stars": 0, "desc": "", "groups": [],
                                     "terms": [], "fork": False, "found_by": []})
        if "skills.sh-sitemap" not in rec["found_by"]:
            rec["found_by"].append("skills.sh-sitemap")
    for full, pg in pages.items():
        if full not in pool or not pg:
            continue
        pool[full]["installs"] = pg.get("total_installs")
        pool[full]["installs_rounded"] = True
        pool[full]["skill_count_sh"] = len(pg.get("skills") or [])
        pool[full]["top_skills"] = sorted(pg.get("skills") or [],
                                          key=lambda x: -(x.get("installs") or 0))[:5]
        if not pool[full].get("desc"):
            pool[full]["desc"] = pg.get("meta_desc", "")

    rejects, cands = [], {}
    for full, r in pool.items():
        low = full.lower()
        if low in known or low in seen:
            continue                                  # 已在库，不进候选，也不算拒收
        if r.get("fork"):
            rejects.append((full, r, "fork，不是原作", "门槛"))
            continue
        if NAME_DENY.search(full.split("/")[-1]):
            rejects.append((full, r, f"命名黑名单命中：{full.split('/')[-1]}", "门槛"))
            continue
        blob = f"{full} {r.get('desc', '')} {' '.join(s.get('name', '') for s in r.get('top_skills', []))}"
        hard = RED_SCRAPE_HARD.search(blob)
        if hard:
            rejects.append((full, r, f"随件绕过目标站的防抓措施（命中「{hard.group(0)}」）", "红线"))
            continue
        r["cjk"] = round(_chinese_ratio(r.get("desc", "")), 3)
        r["is_cn"] = bool(CJK.search(blob))
        # SOFT 只标记，不定罪 —— 单独一个「爬虫」不是红线，**绕过防抓**才是。
        # 标了的这批要人去读正文和 scripts/ 再判，别让机器替人下红线判决。
        soft = RED_SCRAPE_SOFT.search(blob)
        r["needs_scrape_review"] = bool(soft)
        if soft:
            r["scrape_hint"] = soft.group(0)
        cands[full] = r

    # 排序只为「人按什么顺序读」：装机量 > 中文 > 星数。**不是分数，不决定上架。**
    order = sorted(cands.values(), key=lambda r: (-(r.get("installs") or 0),
                                                  not r.get("is_cn"), -(r.get("stars") or 0)))
    _save("candidates_raw.json", {"candidates": order, "rejects": rejects})
    print(f"[funnel] 候选池 {len(cands)} 个仓库（机器筛掉 {len(rejects)} 个）")
    print(f"[funnel] 其中带中文信号 {sum(1 for r in cands.values() if r.get('is_cn'))} 个，"
          f"拿到装机量 {sum(1 for r in cands.values() if r.get('installs'))} 个")
    hardn = sum(1 for x in rejects if x[3] == "红线")
    softn = sum(1 for r in cands.values() if r.get("needs_scrape_review"))
    print(f"[funnel] 红线·绕反爬：直接拒 {hardn} 个；另有 {softn} 个带爬虫相关词，"
          f"**只标记不定罪**，要人读正文和 scripts/ 再判")
    print(f"[funnel] 在架仓库 {len(on_shelf)} 个，库内已知 {len(known)} 个，scout 见过 {len(seen)} 个")


# ----------------------------------------------------------- 交付：导出 ---
def cmd_export(_args) -> None:
    """把候选池导成 editorial/candidates.json。

    **它不是货架，是待读清单。** 机器只负责筛掉和排序，挑不出——
    所以这份文件里没有任何「分数」字段，`rank_by` 只说明按什么排的，
    免得下一个读它的人（或者半年后的我）把排序当成推荐。
    """
    raw = _load("candidates_raw.json", {})
    cands = raw.get("candidates", [])
    if not cands:
        print("[funnel] 先跑 candidates")
        return
    out = []
    for r in cands:
        out.append({
            "repo": r["repo"],
            "url": f"https://github.com/{r['repo']}",
            "desc": (r.get("desc") or "")[:300],
            "stars": r.get("stars", 0),
            "installs": r.get("installs"),
            "installs_rounded": bool(r.get("installs") is not None),
            "skill_count_sh": r.get("skill_count_sh"),
            "top_skills": [{"skill": x["skill"], "installs": x["installs"]}
                           for x in (r.get("top_skills") or [])],
            "is_cn": bool(r.get("is_cn")),
            "verticals": r.get("groups", []),
            "matched_terms": r.get("terms", [])[:8],
            "found_by": r.get("found_by", []),
            "pushed_at": r.get("pushed_at", ""),
            "repo_created_at": r.get("created_at", ""),
            "skill_first_seen": "",
            "age_source": "repo" if r.get("created_at") else "",
            "needs_scrape_review": bool(r.get("needs_scrape_review")),
            "scrape_hint": r.get("scrape_hint", ""),
        })
    doc = {
        "_说明": "宽漏斗候选池。**不是货架，是待读清单。** 机器只负责筛掉（fork/"
                "命名黑名单/红线·绕反爬）和排序，挑不出——挑那关永远是人在把。",
        "_排序": "installs 降序 → 有中文信号优先 → stars 降序。这是「人按什么顺序读」，"
                "不是打分，更不是推荐。",
        "_装机量": "installs 来自 skills.sh 仓库页，站点显示的就是四舍五入缩写"
                 "（6.6K / 122.1K），所以 installs_rounded 恒为 true —— "
                 "**只能排序分档，不能当精确值印出去**。",
        "_年龄": "repo_created_at 是仓库建仓时间，对合集和多 skill 仓库答非所问；"
               "skill_first_seen（该 SKILL.md 首次提交时间）要 GitHub token 才拿得到，"
               "现在一律留空并标 age_source: repo。**不估算。**",
        "_待人判": "needs_scrape_review=true 的，描述或 skill 名里出现了爬虫相关词。"
                 "单独一个「爬虫」不是红线，**绕过对方防抓措施**才是——"
                 "这批要人读正文和 scripts/ 再判，机器不替人下红线判决。",
        "generated_at": TODAY,
        "count": len(out),
        "rank_by": "installs desc, cn first, stars desc",
        "candidates": out,
    }
    path = os.path.join(ROOT, "editorial", "candidates.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    cn = sum(1 for x in out if x["is_cn"])
    withi = sum(1 for x in out if x["installs"])
    print(f"[funnel] 写出 editorial/candidates.json：{len(out)} 个候选仓库"
          f"（中文 {cn} · 有装机量 {withi} · 待判绕反爬 "
          f"{sum(1 for x in out if x['needs_scrape_review'])}）")


# ------------------------------------------------------------- 覆盖率表 ---
BLOCKED = [
    ("Gitee 搜索", "拿不到", "搜索页是 SPA，数据走 /api/v*，robots.txt 明令 Disallow: /api/v*；"
                          "/explore 带查询串返回 405"),
    ("GitCode 搜索", "拿不到", "robots.txt 同时禁 /search 和 /*?*（一切带查询串的 URL）"),
    ("YouMind 画廊", "不许抓", "robots.txt 里 User-agent: ClaudeBot → Disallow: /"),
    ("skills.sh /api/search", "不走", "robots.txt Disallow: /api/ —— 上一轮 enrich.py 的 funnel 走的是这个口"),
    ("小红书 / 公众号 / X", "不抓", "robots 拒；按 CURATION.md 记为只能靠人工指路的盲区"),
]


def cmd_coverage(_args) -> None:
    sm = _load("sitemap_index.json", {})
    gh = _load("github_raw.json", {"repos": {}, "queries": {}})
    det = _load("detail.json", {})
    rows = sm.get("rows", [])
    sm_repos = {f"{o}/{r}" for o, r, _ in rows}
    print("\n═══ 覆盖率 / Coverage ═══\n")
    print("【可达的源】")
    if rows:
        print(f"  skills.sh sitemap   可枚举 {len(rows)} 件 skill / {len(sm_repos)} 个仓库")
        ps = sm.get("per_shard", {})
        if ps and all(v == 10000 for v in ps.values() if v is not None):
            print("                      ⚠ 每片正好 10000 = 疑似分片上限，站点总量**未知**")
    else:
        print("  skills.sh sitemap   未跑")
    if gh["queries"]:
        tot = [v["total_count"] for v in gh["queries"].values() if v["total_count"] is not None]
        ret = sum(v["returned"] for v in gh["queries"].values())
        print(f"  GitHub 搜索         {len(gh['queries'])} 条查询，"
              f"接口报总命中 {sum(tot)}（含跨查询重复），实际取回 {ret} 条 → 去重 {len(gh['repos'])} 个仓库")
        capped = [t for t, v in gh["queries"].items() if (v['total_count'] or 0) > v['returned']]
        if capped:
            print(f"                      ⚠ {len(capped)} 条查询命中数超过单页 100 上限，"
                  f"**没有翻页**，这部分是已知漏掉的")
    else:
        print("  GitHub 搜索         未跑")
    pg = _load("repo_pages.json", {})
    if pg:
        ok = sum(1 for v in pg.values() if v and v.get("total_installs") is not None)
        nsk = sum(len((v or {}).get("skills") or []) for v in pg.values())
        print(f"  skills.sh 仓库页    拉了 {len(pg)}/{len(sm_repos) or '?'} 个仓库，"
              f"拿到装机量 {ok} 个（取不到 {len(pg) - ok} 个，留空不猜），"
              f"覆盖到 {nsk} 件 skill 的逐件装机量")
    if det:
        got = sum(1 for v in det.values() if v.get("installs") is not None)
        print(f"  skills.sh 单件页    拉了 {len(det)} 件，拿到装机量 {got} 件")
    print("\n【我们给对方服务器的负担（实测，不是估算）】")
    print("  " + rate_report())
    print("  ⚠ 本轮前段的请求没有时间戳（插桩是中途加的），上面这个数是**后段的实测值**，"
          "不代表全程")
    print("\n【拿不到的源，以及为什么】")
    for name, state, why in BLOCKED:
        print(f"  {name:24s} {state:6s} {why}")
    print("\n分母说明：生态号称 266 万条 skill，本轮枚举到的是上面这些数。"
          "**没有任何一个源可以说「已全量覆盖」。**\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sitemap", "github", "repos", "candidates", "export", "detail", "coverage"])
    ap.add_argument("--no-odd", action="store_true", help="跳过「点子够怪」那组英文查询")
    ap.add_argument("--control", action="store_true",
                    help="只跑英文垂直对照组，用来检验「skills.sh 漏掉的是中文，还是漏掉整条长尾」")
    ap.add_argument("--paginate", action="store_true",
                    help="只跑翻页：把命中数超过单页 100 的查询补齐（GitHub 最多给 1000 条）")
    ap.add_argument("--delay", type=float, default=0.5, help="每页间隔秒数（礼貌限速）")
    ap.add_argument("--workers", type=int, default=3, help="并发数，别调大，对面是别人的服务器")
    main_args = ap.parse_args()
    {"sitemap": cmd_sitemap, "github": cmd_github, "repos": cmd_repos,
     "candidates": cmd_candidates, "export": cmd_export, "detail": cmd_detail,
     "coverage": cmd_coverage}[main_args.cmd](main_args)


if __name__ == "__main__":
    main()
