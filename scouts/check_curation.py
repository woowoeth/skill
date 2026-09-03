#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
品味 — 编辑层体检 / editorial layer check.

回答十一个问题，全部基于仓库里的真实文件，不估算：
  1. 上架的每一件，局限（limit_zh）写了没有？缺多少件？
  2. editorial/rejected.json 合不合 schema/rejected.schema.json？
  3. editorial/headline.json 选的 id 真的在架上吗？有没有一天两条？
  4. feed.json 和 rejected-feed.json 是不是当前 skills/*.json 重建出来的？
  5. 备料徽章命中多少？有多少件因为我们没存下正文而算不出来？
  6. install.copy 抄下来真能装上吗？（单品必须有；合集刻意留空）
  7. 可爬层印出的 skill_count 有没有大到该重过一遍选品？（数字已核过，等的是判断）
  8. 卡片上那行短版局限是完整句还是伪装的截断？年龄口径和数据对得上吗？
  9. 上站的封面里有没有混进按 D4/D10 不该上站的（og / logo / 二维码 / 空白）？
  10. 我们自己写的推荐语里，有没有在替某件东西宣传红线行为？
  13. 英文四件套齐不齐？英文文案里有没有星数、有没有回落成仓库文件名、有没有漏翻或被截断？

用法:
  python3 scouts/check_curation.py                # 报告，不改任何文件
  python3 scouts/check_curation.py --list         # 顺带列出缺局限的每一件
  python3 scouts/check_curation.py --json         # 机器可读
  python3 scouts/check_curation.py --strict       # 有 ERROR 时退出码 1（CI 用）

退出码: 0 = 没有 ERROR（--strict 下 WARN 也放行）；1 = 有 ERROR。
标准零第三方依赖，schema 校验是手写的子集（type/enum/required/pattern/
minLength/maxLength/additionalProperties），够覆盖这两个 schema。
"""
from __future__ import annotations
import os, re, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scout_lib as lib  # noqa: E402

ERRORS: list[str] = []
WARNS: list[str] = []

# limit_zh 的长度分两档，因为「太长」是两件不同的事：
#
#   ≤140  版式目标。**长度是版式约束，不是质量问题** —— 卡片版式此刻正在重做，
#         按一个还不存在的版式去削内容，砍掉的是事实。所以超过它只报 WARN。
#   >210  硬上限。到这个长度它已经不是「一条局限」而是一段话，
#         多半是把点评或简介写进了局限字段 —— 那是真的数据问题，报 ERROR。
#         一个从不触发的上限等于没有上限，所以这一档必须留在 ERROR。
LIMIT_SOFT = 140
LIMIT_HARD = 210

def err(m: str) -> None:  ERRORS.append(m)
def warn(m: str) -> None: WARNS.append(m)


# ------------------------------------------------ 手写的 JSON Schema 子集 ---
def validate(node, schema: dict, defs: dict, path: str, out: list) -> None:
    if not isinstance(schema, dict):
        return
    if "$ref" in schema:
        ref = schema["$ref"].split("/")[-1]
        return validate(node, defs.get(ref, {}), defs, path, out)

    t = schema.get("type")
    if t == "object" and not isinstance(node, dict):
        out.append(f"{path}: 应为 object，实为 {type(node).__name__}"); return
    if t == "array" and not isinstance(node, list):
        out.append(f"{path}: 应为 array，实为 {type(node).__name__}"); return
    if t == "string" and not isinstance(node, str):
        out.append(f"{path}: 应为 string，实为 {type(node).__name__}"); return
    if t == "integer" and not isinstance(node, int):
        out.append(f"{path}: 应为 integer，实为 {type(node).__name__}"); return
    if t == "boolean" and not isinstance(node, bool):
        out.append(f"{path}: 应为 boolean，实为 {type(node).__name__}"); return

    if "enum" in schema and node not in schema["enum"]:
        out.append(f"{path}: {node!r} 不在允许值 {schema['enum']} 里")

    if isinstance(node, str):
        pat = schema.get("pattern")
        if pat and not re.search(pat, node):
            out.append(f"{path}: {node!r} 不符合 pattern {pat}")
        if "minLength" in schema and len(node) < schema["minLength"]:
            out.append(f"{path}: 太短（{len(node)} < {schema['minLength']}）")
        if "maxLength" in schema and len(node) > schema["maxLength"]:
            out.append(f"{path}: 太长（{len(node)} > {schema['maxLength']}）")

    if isinstance(node, int) and not isinstance(node, bool) and "minimum" in schema:
        if node < schema["minimum"]:
            out.append(f"{path}: {node} < 最小值 {schema['minimum']}")

    if isinstance(node, dict):
        props = schema.get("properties", {})
        for k in schema.get("required", []):
            if k not in node or node[k] in ("", None):
                out.append(f"{path}: 缺必填字段 {k}")
        if schema.get("additionalProperties") is False:
            for k in node:
                if k not in props and not k.startswith("_"):
                    out.append(f"{path}: 多出未知字段 {k}")
        for k, v in node.items():
            if k in props:
                validate(v, props[k], defs, f"{path}.{k}", out)

    if isinstance(node, list) and "items" in schema:
        for i, v in enumerate(node):
            validate(v, schema["items"], defs, f"{path}[{i}]", out)


def check_against(doc, schema_file: str, label: str) -> None:
    p = os.path.join(lib.ROOT, "schema", schema_file)
    sch = lib.read_json(p, None)
    if not sch:
        err(f"{label}: 读不到 schema/{schema_file}")
        return
    out: list[str] = []
    validate(doc, sch, sch.get("$defs", {}), label, out)
    for m in out:
        err(m)


# --------------------------------------------------------------- 1. 局限 ---
def check_limits(show_list: bool) -> dict:
    items = apply_all(load_all())
    shelved = [it for it in items.values() if not it.get("hide")]
    missing = [it for it in shelved if not (it.get("limit_zh") or "").strip()]
    weak = [it for it in shelved
            if (it.get("limit_zh") or "").strip()
            and len((it["limit_zh"]).strip()) < 8]
    generic = [it for it in shelved
               if re.search(r"仅供参考|自行判断|请谨慎|注意安全|因人而异",
                            it.get("limit_zh") or "")]

    print("\n【1】局限字段 limit_zh")
    print(f"  上架 {len(shelved)} 件 · 有局限 {len(shelved) - len(missing)} 件 · "
          f"缺 {len(missing)} 件（{100 * len(missing) / max(len(shelved), 1):.1f}%）")
    if missing:
        warn(f"{len(missing)}/{len(shelved)} 件上架商品还没有 limit_zh")
        if show_list:
            for it in sorted(missing, key=lambda x: x.get("added_at", ""), reverse=True):
                print(f"    - {it['id']}  {it.get('title_zh') or it.get('name')}")
        else:
            for it in sorted(missing, key=lambda x: x.get("added_at", ""), reverse=True)[:8]:
                print(f"    - {it['id']}  {it.get('title_zh') or it.get('name')}")
            if len(missing) > 8:
                print(f"    …… 还有 {len(missing) - 8} 件（加 --list 全列）")
    if weak:
        warn(f"{len(weak)} 件的 limit_zh 短于 8 字，多半是敷衍")
        for it in weak[:5]:
            print(f"    [短] {it['id']}: {it['limit_zh']!r}")
    if generic:
        warn(f"{len(generic)} 件的 limit_zh 是通用免责声明，不是这件东西真实的局限")
        for it in generic[:5]:
            print(f"    [空话] {it['id']}: {it['limit_zh']!r}")
    # 长度分两档 —— 见下面的注释，这是刻意的区分，不是放水。
    over_soft = [it for it in shelved if LIMIT_SOFT < len(it.get("limit_zh") or "") <= LIMIT_HARD]
    over_hard = [it for it in shelved if len(it.get("limit_zh") or "") > LIMIT_HARD]
    if over_soft:
        warn(f"{len(over_soft)} 件的 limit_zh 超过 {LIMIT_SOFT} 字版式目标（卡片版式定稿后再削）")
        for it in over_soft[:5]:
            print(f"    [超目标] {it['id']}: {len(it['limit_zh'])} 字")
    if over_hard:
        err(f"{len(over_hard)} 件的 limit_zh 超过 {LIMIT_HARD} 字硬上限"
            f" —— 那不是一条局限，是一段话，多半把点评或简介写进来了")
        for it in over_hard[:5]:
            print(f"    [超上限] {it['id']}: {len(it['limit_zh'])} 字")
    at_ceiling = [it for it in shelved if len(it.get("limit_zh") or "") == 120]
    if at_ceiling:
        print(f"  提示：{len(at_ceiling)} 件正好卡在旧的 120 字上限上 —— "
              f"是照着上限写出来的，不是自然写完的，版式定稿后值得回看有没有被削掉事实")
    return {"shelved": len(shelved), "missing": len(missing),
            "weak": len(weak), "generic": len(generic),
            "over_soft": len(over_soft), "over_hard": len(over_hard)}


def load_all() -> dict:
    return lib.load_items()

def apply_all(items: dict) -> dict:
    items = lib.apply_editorial(items)
    for it in items.values():
        lib.normalize_item(it)
    return items


# ------------------------------------------------------------- 2. 拒收榜 ---
def check_rejected(items: dict) -> dict:
    print("\n【2】拒收榜 editorial/rejected.json")
    if not os.path.exists(lib.REJECTED):
        warn("editorial/rejected.json 不存在 —— 拒收榜是空的，构建管线会照常跑")
        return {"entries": 0}
    doc = lib.read_json(lib.REJECTED, None)
    if doc is None:
        err("editorial/rejected.json 不是合法 JSON")
        return {"entries": 0}
    check_against(doc, "rejected.schema.json", "rejected")

    entries = [e for e in doc.get("entries", []) if isinstance(e, dict)]
    # 这两条检查的粒度是 **(repo, skill)**，不是 repo。
    #
    # 原来两条都按 repo 比，于是 rejected.json 里 `_去重键` 写明的正常状态
    # —— 「同一个仓库一部分上架一部分被拒」—— 被判成了矛盾和重复。
    # 同一个 repo-only 假设当时还长在 build_rejected_feed 里，让 96 条拒收只有 90 条进得了榜。
    # **修一处不算修完：同一个错误假设会同时长在管线和守卫里，而守卫报出来的话正好把你引开。**
    seen, dupes = set(), []
    shelved = {(it.get("repo"), it.get("name") or "") for it in items.values() if not it.get("hide")}
    shelved_repos = {r for r, _ in shelved}
    for e in entries:
        r = e.get("repo", "")
        sk = (e.get("skill") or "").strip()
        key = (r, sk)
        if key in seen:
            dupes.append(f"{r}" + (f"（{sk}）" if sk else "（整仓）"))
        seen.add(key)
        # 整仓被拒（skill 留空）却还有货在架 = 真矛盾。
        # 指名某一件被拒，只有那一件也在架上才算矛盾。
        if (r in shelved_repos) if not sk else ((r, sk) in shelved):
            what = r if not sk else f"{r} 的 {sk}"
            err(f"拒收榜里的 {what} 同时还在架上 —— 收了又说拒了，站上会自相矛盾")
        reason = e.get("reject_reason_zh", "")
        if re.fullmatch(r"\s*(不满足|未通过|不符合)?\s*(问一|问二|问三|红线|门槛)\s*[。.]?\s*", reason):
            err(f"{r}: reject_reason_zh 只复述了条款名，没说这一件为什么被拒")
    by_rule: dict = {}
    for e in entries:
        by_rule[e.get("reject_rule", "?")] = by_rule.get(e.get("reject_rule", "?"), 0) + 1
    print(f"  {len(entries)} 条 · 按条款 {by_rule or '（空）'}")
    if dupes:
        warn(f"{len(dupes)} 条 (repo, skill) 重复（构建时只取最后写的那条）：{dupes[:5]}")
    return {"entries": len(entries), "by_rule": by_rule}


# --------------------------------------------------------------- 3. 头条 ---
def check_headline(items: dict) -> dict:
    print("\n【3】头条 editorial/headline.json")
    if not os.path.exists(lib.HEADLINE):
        warn("editorial/headline.json 不存在 —— 首页没有头条位，其余照常")
        return {"headlines": 0}
    doc = lib.read_json(lib.HEADLINE, None)
    if doc is None:
        err("editorial/headline.json 不是合法 JSON")
        return {"headlines": 0}
    check_against(doc, "headline.schema.json", "headline")

    rows = [h for h in doc.get("headlines", []) if isinstance(h, dict)]
    days: dict = {}
    for h in rows:
        d, sid = h.get("date", ""), h.get("id", "")
        days.setdefault(d, []).append(sid)
        if sid and sid not in items:
            err(f"头条 {d} 指向不存在的 id：{sid}")
        elif sid and items[sid].get("hide"):
            err(f"头条 {d} 指向已下架的商品：{sid}")
    for d, ids in days.items():
        if len(ids) > 1:
            err(f"{d} 有 {len(ids)} 条头条，同一天只能有一条：{ids}")
    cur, hist = lib.build_headline(items)
    print(f"  {len(rows)} 条历史 · 今日头条：{cur['id'] if cur else '（无）'}")
    if rows and not cur:
        warn("有头条条目，但今天没有一条可用（日期都在未来，或指向的商品已下架）")
    return {"headlines": len(rows), "today": (cur or {}).get("id", "")}


# ------------------------------------------------------------- 4. 新鲜度 ---
def check_freshness() -> None:
    print("\n【4】构建产物")
    for path in (lib.FEED, lib.REJECTED_FEED):
        rel = os.path.relpath(path, lib.ROOT)
        d = lib.read_json(path, None)
        if d is None:
            warn(f"{rel} 不存在或读不出 —— 跑 python3 scouts/scout_lib.py 重建")
            continue
        extra = (f"count={d['count']}" if "count" in d
                 else "stats=" + json.dumps({k: v for k, v in d.get("stats", {}).items()
                                             if isinstance(v, int)}, ensure_ascii=False))
        print(f"  {rel}: generated_at={d.get('generated_at')} {extra}")
    feed = lib.read_json(lib.FEED, None) or {}
    on_disk = len([it for it in apply_all(load_all()).values() if not it.get("hide")])
    if feed and feed.get("count") != on_disk:
        err(f"feed.json 说 {feed.get('count')} 件，skills/*.json 现在是 {on_disk} 件 —— feed 过期了")


# ----------------------------------------------------------- 6. 安装命令 ---
# `install.copy` 是用户照抄的那一行，抄错了这件商品就是装不上 —— 全站最不该出错的字段。
# 但「必填」只对单品成立：
#   单品   copy 空   = ERROR。装不上等于没上架。
#   合集   copy 空   = 正常。合集的 `mv <repo> …` 落地后那层没有 SKILL.md，
#                     装了等于没装；一半合集的 skill 还散在多个根目录，
#                     「那个 skills 目录」根本不存在。合集给 clone + browse 指针。
_MV_REPO = re.compile(r"^\s*mv\s+\S+\s+~/\.claude/skills/")

def check_install(items: dict) -> dict:
    print("\n【6】安装命令 install")
    shelved = [it for it in items.values() if not it.get("hide")]
    singles = [it for it in shelved if it.get("kind") != "collection"]
    colls = [it for it in shelved if it.get("kind") == "collection"]

    def copy_of(it):
        return ((it.get("install") or {}).get("copy") or "").strip()

    bad_single = [it for it in singles if not copy_of(it)]
    coll_mv = [it for it in colls if _MV_REPO.match(copy_of(it))]
    coll_empty = [it for it in colls if not copy_of(it)]
    coll_no_browse = [it for it in coll_empty
                      if not ((it.get("install") or {}).get("browse") or "").strip()]

    print(f"  单品 {len(singles)} 件 · copy 齐 {len(singles) - len(bad_single)} · 缺 {len(bad_single)}")
    print(f"  合集 {len(colls)} 件 · copy 留空（新规则）{len(coll_empty)} · "
          f"还在给 mv <repo> 的 {len(coll_mv)}")
    if bad_single:
        err(f"{len(bad_single)} 件单品的 install.copy 是空的 —— 用户照抄装不上，等于没上架")
        for it in bad_single[:8]:
            print(f"    [无 copy] {it['id']}")
    if coll_mv:
        warn(f"{len(coll_mv)} 件合集还在给 `mv <repo> ~/.claude/skills/…` —— "
             f"那一层里没有 SKILL.md，装了等于没装。按新规则应改成 clone + browse，copy 留空")
        for it in coll_mv[:8]:
            print(f"    [合集给了 mv] {it['id']}  (skill_count={it.get('skill_count')})")
    if coll_no_browse:
        warn(f"{len(coll_no_browse)} 件合集 copy 留空但也没有 install.browse —— "
             f"用户 clone 完不知道下一步去哪挑")
        for it in coll_no_browse[:8]:
            print(f"    [无 browse] {it['id']}")
    return {"singles": len(singles), "single_no_copy": len(bad_single),
            "collections": len(colls), "coll_mv": len(coll_mv),
            "coll_empty": len(coll_empty), "coll_no_browse": len(coll_no_browse)}


# ------------------------------------------------------------ 10. 红线 ---
# 起因是一次真实的漏网：`browser-act-skills` 的卖点是「穿过反爬墙」，CLI 自带
# solve-captcha 还会上传验证码图 —— 它在架上待了两个多小时，期间还有人给它**重写过点评**。
#
# 关键的一句（产品复盘的原话）：
#   **红线不是被机器漏过的，是被「它解决了真问题」这个好理由盖过去的。**
#
# 所以这个守卫的判据不是「这东西是干什么的」——那是人的判断，机器判不了，也不该判。
# 判据是**我们自己的推荐语里有没有在替它宣传红线行为**：
#
#   命中在 title_zh / tagline_zh / why_zh  = 我们在替它说好话的地方出现了红线词 → 最重
#   命中在 desc_en / name / limit_zh 等    = 原作者的话，或我们在如实写局限 → 提醒
#
# 这个分法有个好性质：**它查的是我们的嘴，不是它的成分。** 一个防御向的安全 skill
# （CURATION 明写可以收）不会在我们的推荐语里出现「免杀」「C2 架构」，
# 而一件真该拒的东西，我们只要写得出让人想装的文案，就一定会写到那些词上。
#
# 词表分两档，因为精度不一样：
#   强词  单独出现就基本不会认错（免杀 / shellcode / C2 架构 / 绕过反爬 / 撞库 / PUA）
#   弱词  有正当用法，必须靠上下文（红队 —— 「红队你的 PRD」是战略复盘；渗透 / 漏洞 / OSINT）
# 强词进我们的推荐语 = ERROR；弱词、或强词只出现在原文里 = WARN 点名等人看。
RED_STRONG = {
    "绕反爬/验证码": r"反爬|绕过.{0,6}(?:爬|检测|风控|封锁|人机)|验证码|captcha|anti-?bot",
    "攻击赋能":     r"免杀|shellcode|C2\s*(?:架构|框架|服务)|横向移动|提权|EDR\s*(?:绕过|evasion)",
    "灰产/盗号":    r"盗号|撞库|接码|养号|群控|批量注册|刷单",
    "荐股/交易信号": r"荐股|买入信号|卖出信号|交易信号|涨跌预测|抄底|牛股",
    "价值观有害":   r"\bPUA\b|舔狗",
}
RED_WEAK = {
    "攻击赋能": r"红队|red.?team|渗透|漏洞利用|exploit|OSINT|侦察自动化|逆向工程.{0,6}保护",
}
# 「不绕反爬」「不做荐股」这类否认句不算命中 —— 那是在写局限，正是我们要的东西。
# 否定词和命中词之间**允许隔几个字**，且不跨句读。
# 原来是 `(?:不|没有|拒绝…)\s*$`，要求否定词紧贴命中词 ——
# 这是这条守卫第三次在否定句上误报。第三次的原文是：
#   「财报是用来排除企业的，**不是**用来发现牛股的，有疑就杀 —— 和选股工具正好反」
# 「不是」和「牛股」之间隔着「用来发现」四个字，`\s*$` 接不住，
# 于是一句「它跟选股工具正好相反」被判成「我们在替它宣传荐股」。
# 跨句读就不算这一句在否定它了，所以用 `[^。；\n]{0,8}$` 而不是 `.{0,8}$`。
RED_NEGATED = (r"(?:不|不会|不是|没有|拒绝|不支持|不做|不帮|无法|不能|禁止|绝不"
               r"|排除|相反|正好反)[^。；\n]{0,8}$")
# 否定标记也可能出现在红线词**后面**：「遇到验证码**就停**」「碰到风控**就撤**」。
# 原来只看前面 12 个字，于是把一句「它不这么干」的褒奖判成了「我们在替它宣传」。
# 这是本店最想褒奖的那一类行为（D41：它减负、它认栽，它不隐身），
# 守卫却正好对它开火 —— 差点因此去改一句本来没问题的文案。
RED_NEGATED_AFTER = (r"^\s*(?:就|便|即)?\s*(?:停|撤|退出|放弃|收手|停手|停下|作罢)"
                     r"|^[^。；\n]{0,10}?(?:就停|就撤|停手|不换身份|不重复|不绕|不破解|不硬试|不代劳)")
OUR_COPY = ("title_zh", "tagline_zh", "why_zh")          # 我们替它说好话的地方
THEIR_TEXT = ("name", "desc_en", "tagline_en", "why_en", "limit_zh", "limit_brief_zh")


def _red_hits(it: dict, fields, table) -> list[tuple[str, str, str]]:
    out = []
    for f in fields:
        t = it.get(f) or ""
        if not isinstance(t, str):
            continue
        for cat, pat in table.items():
            for m in re.finditer(pat, t, re.I):
                if re.search(RED_NEGATED, t[max(0, m.start() - 12):m.start()]):
                    continue
                if re.search(RED_NEGATED_AFTER, t[m.end():m.end() + 14]):
                    continue
                out.append((cat, f, t[max(0, m.start() - 16):m.end() + 16]))
    return out


def check_red_lines(items: dict) -> dict:
    print("\n【10】红线自查（查我们自己的推荐语，不是查它的成分）")
    shelved = [it for it in items.values() if not it.get("hide")]
    hard, soft = [], []
    for it in shelved:
        strong_ours = _red_hits(it, OUR_COPY, RED_STRONG)
        rest = (_red_hits(it, THEIR_TEXT, RED_STRONG)
                + _red_hits(it, OUR_COPY, RED_WEAK)
                + _red_hits(it, THEIR_TEXT, RED_WEAK))
        if strong_ours:
            hard.append((it, strong_ours))
        elif rest:
            soft.append((it, rest))
    print(f"  在架 {len(shelved)} 件 · 推荐语里出现强红线词 {len(hard)} 件 · 仅原文/局限里出现 {len(soft)} 件")
    if hard:
        err(f"{len(hard)} 件在**我们自己写的推荐语**里出现了红线词 —— "
            f"那不是它是什么的问题，是我们在替它宣传。红线从来不是被机器漏过的，"
            f"是被「它解决了真问题」这个好理由盖过去的")
        for it, hits in hard[:6]:
            print(f"    [我们在宣传] {it['id']}")
            for cat, f, ctx in hits[:3]:
                print(f"        [{cat}] {f}: …{ctx}…")
    if soft:
        warn(f"{len(soft)} 件的原文或局限里提到红线相关行为 —— 多半是如实写局限（那是我们要的），"
             f"但值得人扫一眼确认不是在描述它真会去做的事")
        for it, hits in soft[:6]:
            cat, f, ctx = hits[0]
            print(f"    [待人看] {it['id']}  [{cat}] {f}: …{ctx}…")
    return {"shelved": len(shelved), "in_our_copy": len(hard), "in_their_text": len(soft)}


# --------------------------------------------------------- 9. 封面上站 ---
# D4 / D10 的上站规则：`artwork` 允许竖幅大画幅；`hero`/`diagram` 收窄；
# **`og` 和 `other` 不上站**。`other` 是 logo / 二维码 / 空白 / 坏图 / 别人的书封 ——
# 让它上站，正是 D10 最怕的那个失败模式：「被漂亮图骗进去，装完发现产出不长那样」。
# 2026-08-31 店主定的封面优先级：**优先取仓库里的图，没有才用默认预览卡**。
# 所以 og（GitHub 自动生成的社交预览卡）从「不上站」改成「兜底可上站」。
#
# 改之前我按旧规则把 54 张 og 卡全撤了，在架有封面 129 → 75。**规则是店主的，不是我的。**
# 但兜底不等于没有优先级：og 是最后一档，仓库里有真图就该换掉它 —— 见【21】。
COVER_OFF_SITE = ("other",)

# D22 的画幅档（原 D10 是对称区间，产品自己纠了：**横竖不是同一件事**——
# 竖裁掉的是海报的头和脚，横裁掉的是两侧空白，不该用同一个数）：
#   横向一律 2.0（artwork 也不放宽 —— 3200×800 限到 2.0 得 130px 的框，
#                 限到 3.2 只有 82px 的条；瀑布流里框比条有用，宁可少露）
#   竖向只给 artwork 放到 0.45（其余保持 1.0，不给竖幅）
# D10 的旧数：产出物图允许竖幅大画幅，宣传头图和示意图收窄。
# **注意力给证据，不给宣传图。** 落在区间外的不是坏数据，是卡片得裁剪 —— 见下面的裁剪率。
#
# 规矩是一对，缺了后半条前半条就成了断章取义：
#
#   **流里可以裁，详情页必须给原比例。**
#
# 天下所有图片流都裁图，裁图不等于造假 —— **造假是「只有裁过的那份存在」**。
# 原图一点就有，裁剪就只是版式问题，不是诚实问题。
#
# 这和 `limit_brief_zh` 是同一个形状：**流里给短的，详情给全的，短的那份必须自身成立。**
# 图片这边「自身成立」= 裁出来那块仍看得出是同类产出物（逐张看，脚本判不了）；
# 文字那边「自身成立」= 是完整句不是截断（脚本判得了，见【8】）。
# 两边共同的硬条件是**全的那份真的在一次点击之外** —— 这一条脚本能查的那半在【8】。
COVER_TIERS = {"artwork": (0.45, 2.0), "hero": (1.0, 2.0), "diagram": (1.0, 2.0)}
# 只有这一档报 WARN：**我们声称是产出物证据的图**被裁掉三成以上。
# 其余（hero/diagram 的横幅超限）是设计上就该被裁进框里的东西，报了也没人会处理 ——
# 那种恒为误报的输出留在报告行里，不进待办。
CROP_ALERT_PCT = 30      # 只用在报告行里，不再触发 WARN —— 理由见 check_covers

# 作者自己的仓库域名。**这条不变量比「宽高对账」硬得多，而且零网络**（UX 提）：
#
#   声称是作者产出物的图，**必须托在作者自己的仓库里。**
#
# 宽高对账（`scouts/verify_covers.py`）只能发现「图被人动过」；
# 域名能发现「**这图从来就不是他的**」—— 后者才是我们真正在声明的东西。
# 真实发生过：`hugohe3-ppt-master` 的 cover 曾是 `gcdn.moonshot.cn/.../kimi-en.png`
# 一张 Kimi 赞助商广告，标着 `artwork` + `cover_real=true`，宽高记得完全正确 ——
# **宽高对账给它开了绿灯**，因为它确实是 3200×800。前端还在它下面印
# 「作者仓库里的产出示例——这就是它做出来的东西」。
#
# 顺带这条也管隐私：非作者仓库的图意味着**每个访客的浏览器都要去 ping 一次第三方**。
# 一个卖信任的站，不该为一张缩略图让所有读者被第三方看一眼 —— 所以哪怕不声称是证据，也要点名。
# 「这是输入，不是输出」—— 文件名层面的痕迹。**这个失败模式真发生过两次**：
#   `yangcodingmaster-photo-distill` 的封面曾是 `04b-two-kids-original.jpg`（输入原片），
#   而这件 skill 干的事正是把照片蒸馏成海报 —— 货架上给人看的是它的**输入**。
#   产品是靠读文件名里那个 `-original` 发现的，所以这条痕迹值得机器盯着。
#
# **只报 WARN，因为文件名是旁证不是证据**：叫 `*-input.jpg` 的文件在别人仓库里
# 也可能真是产出物。命中就点名让人打开看一眼，不判死。
# `before-after` / `before_after` 排除掉 —— 那是**成品对比图**，是产出物的典型形态；
# 实测就误伤过一次（`resume-before-after-comparison.png` 是 1 张 BEFORE + 6 张 AFTER 的
# 简历改版展示，`artwork` 一个字没错），所以这个复合词必须先摘出去。
LOOKS_INPUT = re.compile(
    r"(?:^|[-_/])(?:original|orig|input|source|src|raw|sample-in)(?:[-_.]|$)"
    r"|(?<!after[-_])(?:^|[-_/])before(?:[-_.](?!after))", re.I)

OWN_HOST = re.compile(r"(?:^|\.)(?:raw|repository-images|user-images|avatars)"
                      r"\.githubusercontent\.com$|(?:^|\.)github\.com$", re.I)

# 只比域名不够 —— **我们自己的仓库也在 githubusercontent 上。**
# 我们自己装上跑出来的截图放进 woowoeth/skill 之后，域名检查会放它过去，
# 而那条不变量的本意是「图在**作者**仓库里」。通过的理由是错的。
# 所以从 URL 里抠出 owner/repo 和商品的 `repo` 比：
#   对得上   → 作者自己的图
#   是本店的 → 我们自己跑出来的截图，**另一类证据**，要有自己的 cover_kind，见下
#   都不是   → 别人的图
OUR_REPO = "woowoeth/skill"
_GH_PATH = re.compile(
    r"^(?:https?://)?(?:raw\.githubusercontent\.com|github\.com)/([^/]+)/([^/]+)", re.I)

def cover_owner_repo(url: str) -> str:
    m = _GH_PATH.match((url or "").strip())
    return f"{m.group(1)}/{m.group(2)}" if m else ""

def check_covers(items: dict) -> dict:
    print("\n【9】封面上站规则 cover_kind / cover_real")
    shelved = [it for it in items.values() if not it.get("hide")]

    def cov(it):
        return (it.get("cover") or "").strip()

    live = [it for it in shelved if cov(it)]
    by_kind: dict = {}
    for it in live:
        k = it.get("cover_kind") or ""
        by_kind[k] = by_kind.get(k, 0) + 1
    off = [it for it in live if (it.get("cover_kind") or "") in COVER_OFF_SITE]
    claim = [it for it in shelved if it.get("cover_real") and not cov(it)]

    hidden = [it for it in items.values() if it.get("hide")]
    print(f"  下架留痕 {len(hidden)} 件（`hide: true`，记录留在 skills/*.json，"
          f"feed 构建时才过滤 —— 所以 feed 里查不到它们不等于记录被删了）")
    print(f"  在架 {len(shelved)} · 上站封面 {len(live)} 张 —— " + " · ".join(
        f"{k or '（无 kind）'} {v}" for k, v in sorted(by_kind.items(), key=lambda t: -t[1])))
    if off:
        err(f"{len(off)} 张封面的 cover_kind 属于不上站的 {COVER_OFF_SITE} 却挂着 cover URL —— "
            f"按 D4/D10 它们应当无图。上站总数可能是对的，但明细里混进了不该上的")
        for it in off[:8]:
            print(f"    [不该上站] kind={it.get('cover_kind')} {it['id']}"
                  f"{'  ★推荐位' if it.get('pick') else ''}")
            print(f"        {cov(it)[:100]}")
    if claim:
        err(f"{len(claim)} 件 cover_real=true 但 cover 是空的 —— 号称有产出物图却没有图")
        for it in claim[:5]:
            print(f"    [有名无图] {it['id']}")

    # 图托在谁家：声称是产出物 ⇒ 必须是作者自己的仓库。
    from urllib.parse import urlparse
    # 2026-09-03：封面改成同源相对路径 /skill/assets/covers/… 之后，urlparse 的 netloc 是空串，
    # OWN_HOST 匹不到，40 张自家托管的图被报成「不在作者自己的仓库里」。
    # 不是图错了，是我改了一头没改另一头（和 shelf_health 里同一个坑）。相对路径 = 我们自己的仓。
    def _host_ok(u: str) -> bool:
        return u.startswith("/skill/") or bool(OWN_HOST.search(urlparse(u).netloc or ""))
    foreign = [it for it in live if not _host_ok(cov(it))]
    # 域名对了但仓库不对：混进来的是别人（含我们自己）仓库里的图
    ours, other_repo = [], []
    for it in live:
        if it in foreign:
            continue
        orp = OUR_REPO if cov(it).startswith("/skill/") else cover_owner_repo(cov(it))
        if not orp or orp.lower() == (it.get("repo") or "").lower():
            continue
        (ours if orp.lower() == OUR_REPO else other_repo).append((it, orp))
    claimed = [it for it in foreign if it.get("cover_real")]
    if claimed:
        err(f"{len(claimed)} 张声称是产出物证据（cover_real=true）的图**不在作者自己的仓库里** —— "
            f"这图从来就不是他的。宽高对账查不出这个：赞助广告的宽高也可以记得完全正确")
        for it in claimed[:5]:
            print(f"    [不是他的图] {it['id']}\n        {cov(it)[:96]}")
    if other_repo:
        err(f"{len(other_repo)} 张封面托在 GitHub 上、但不是这件商品的仓库 —— "
            f"域名对不代表来源对")
        for it, orp in other_repo[:5]:
            print(f"    [仓库不符] {it['id']}: 图在 {orp}，商品是 {it.get('repo')}")
    if ours:
        # 「图托在我们仓里 ⇒ 我们自己截的」这个推断 09-01 就证明是错的：仓里托的还有
        # 转存的作者作品（artwork）和 GitHub 自动生成的预览卡（og）。
        # 09-03 把 /skill/ 相对路径算进自家仓之后，这条一下子从 37 跳到 152 —— 其中 103 张是 og。
        # og 的来源是确定的（GitHub 生成，1200×600），不该被要求标成 ours；
        # artwork 的来源分不出来（转存 vs 自截），09-01 已记为「没有出处记录就不判」。
        # 所以这里只盯真正说不清的：kind 为空的。
        wrong_kind = [(it, o) for it, o in ours if (it.get("cover_kind") or "") not in ("ours", "og", "artwork", "hero", "diagram")]
        print(f"  我们自己跑出来的截图 {len(ours)} 张（图在 {OUR_REPO}）")
        if wrong_kind:
            err(f"{len(wrong_kind)} 张是我们自己截的图，但 cover_kind 不是 `ours` —— "
                f"详情页图注会印成「作者仓库里的产出示例」，那是把我们做的事说成作者做的。"
                f"自截图是**更强**的证据（我们真装真跑过），但它需要自己那句话")
            for it, o in wrong_kind[:5]:
                print(f"    [自截图标错] {it['id']}: kind={it.get('cover_kind')!r}")
    rest = [it for it in foreign if not it.get("cover_real")]
    if rest:
        warn(f"{len(rest)} 张上站图托在第三方域名上 —— 每个访客的浏览器都会去 ping 一次那个第三方。"
             f"一个卖信任的站不该为一张图让所有读者被第三方看一眼")
        for it in rest[:5]:
            print(f"    [第三方请求] {it['id']}  {urlparse(cov(it)).netloc}")

    # 文件名像「输入」而我们声称它是产出物证据 —— 旁证，点名让人打开看一眼
    looks_in = [it for it in live
                if it.get("cover_real")
                and LOOKS_INPUT.search(cov(it).rsplit("/", 1)[-1])]
    if looks_in:
        warn(f"{len(looks_in)} 张标着产出物证据的封面，文件名像是**输入**而不是输出 —— "
             f"打开看一眼。这个错真发生过：photo-distill 曾把 `-original` 输入原片当产出物挂在头条")
        for it in looks_in:
            print(f"    [疑似输入] {it['id']}\n        {cov(it).rsplit('/', 1)[-1]}")

    # 方向性不变量：`cover_real=true` ⇒ `cover_kind=="artwork"`。**只有这一个方向。**
    # 反方向不成立也不该成立：`artwork` 但 `cover_real=false` 有 11 件，
    # 那是同一张图被同仓库多件共用后去重掉的（`cover_dup_of`），不是矛盾。
    #
    # 为什么现在需要它：D22 之后产品的裁决是「artwork 被裁 ≥30% 的那 2 张先降
    # `cover_kind` 到 `hero`，不换图 —— 我们没能力替作者找一张更方正的产出物图，
    # 而「证据」这个声明是我们自己给的，**收回它比裁着用它诚实**」。
    # 那个动作是**两个字段一起改**：kind 降了、`cover_real` 忘了降，
    # 结果就是一件 `hero` 顶着「这是产出物证据」的标记 —— 半途而废的降级比不降级更糟，
    # 因为它看起来已经处理过了。
    # `ours`（我们自己装上跑出来的截图）也是产出物证据 —— 而且是更强的那种，
    # 所以它和 `artwork` 一样有资格带 cover_real=true。
    EVIDENCE_KINDS = ("artwork", "ours")
    wrong_real = [it for it in shelved
                  if it.get("cover_real") and (it.get("cover_kind") or "") not in EVIDENCE_KINDS]
    if wrong_real:
        err(f"{len(wrong_real)} 件 cover_real=true 但 cover_kind 不在 {EVIDENCE_KINDS} 里 —— "
            f"宣传图/示意图顶着「这是产出物证据」的标记。降 kind 时 cover_real 要跟着降")
        for it in wrong_real[:5]:
            print(f"    [假证据] {it['id']}: kind={it.get('cover_kind')!r} real=True")

    # 两套尺寸字段并存 = 两份真相。规范名是 cover_w / cover_h。
    dup_dim = [it for it in shelved
               if ("cover_w" in it and "cover_width" in it)
               or ("cover_h" in it and "cover_height" in it)]
    if dup_dim:
        err(f"{len(dup_dim)} 件同时带 cover_w/h 和 cover_width/height —— 两套尺寸字段就是两份真相，"
            f"前端读规范名那一套，另一套写对了也没人看得见")
        for it in dup_dim[:5]:
            print(f"    [两套尺寸] {it['id']}: "
                  f"cover_w/h={it.get('cover_w')}×{it.get('cover_h')} "
                  f"cover_width/height={it.get('cover_width')}×{it.get('cover_height')}"
                  + ("  ←两者还不一致" if (it.get("cover_w"), it.get("cover_h"))
                     != (it.get("cover_width"), it.get("cover_height")) else ""))

    # 画幅档（D10）。落在区间外**不是数据错**，是卡片得裁剪或留白 ——
    # 所以报 WARN 并算出裁掉多少：裁掉一半等于换了一张图，那才是 UX 要单独看的。
    eps = 1e-3
    crop = []
    for it in live:
        w, h = it.get("cover_w"), it.get("cover_h")
        if not (isinstance(w, int) and isinstance(h, int) and h > 0):
            continue
        lo, hi = COVER_TIERS.get(it.get("cover_kind") or "", (0.0, 99.0))
        r = w / h
        if lo - eps <= r <= hi + eps:
            continue
        tgt = hi if r > hi else lo
        loss = round(100 * (1 - (tgt / r if r > hi else r / tgt)))
        crop.append((loss, it, f"{w}×{h}", round(r, 2)))
    crop.sort(key=lambda t: -t[0])
    nodim = [it for it in live if not isinstance(it.get("cover_w"), int)]
    # **刻意是报告行，不是 WARN。** 两个都不选的理由（UX 提，我接受）：
    #   跟前端的常量 → 守卫拿他的常量去量他的常量，**定义上不可能失败**，
    #                  而且同一组数字存在两处两种语言，靠人记着同步 —— 正是我们刚
    #                  夸他不做的那件事（前端别存文案副本）的另一个方向。
    #   守 D10 原文   → 15 条里 12 条是设计上就没人会处理的，恒为误报。
    #                  「一个当前唯一输出是误报的守卫就是噪音」这条纪律对我自己也算。
    # 画幅数值属于卡片渲染，本来就该跟版式走，不该固化成跨模块契约 ——
    # 那是给一个只有一个消费者的常量加远程审批流程。
    # 真正该守的不变量在 scouts/verify_covers.py：**cover 里必须是原图，不是预裁版。**
    if crop:
        print(f"  参考（不是待办）：按 D22 画幅档量，{len(crop)} 张需要裁剪或留白。"
              f"实际画幅由版式定，裁多少读者点一下就看到原图 —— 裁剪是版式问题不是诚实问题，"
              f"**前提是详情页给原比例、一刀不裁**")
        for loss, it, dim, r in crop[:8]:
            print(f"    裁掉 {loss:2d}%  {(it.get('cover_kind') or '?'):8s} {dim:10s} 比 {r:<5} {it['id']}")
    # **这一档原来是 WARN，撤了。** 理由（UX 提，我接受）：
    #   ① 查过那 2 张的 `candidates`，**都没有可换的图**（0 个 / 1 个且就是现用那张），
    #      所以「换一张」这个修法不存在；
    #   ② 剩下的修法「改 `cover_kind` 到 hero」现在**是在页面上撒谎** ——
    #      `cover_kind` 已经不是内部标记，它直接决定详情页的图注文案
    #      （`artwork` → 「这就是它做出来的东西」/ `hero` → 「作者自制的头图」）。
    #      为了消警报去改它，等于改一句给读者看的话。
    #   ③ 更要紧的是：把「赞助广告冒充产出物」框成「裁掉 50%」，
    #      **会把人引向错的修法**（少裁一点、换个 kind），而正解是 `cover` 置空。
    # 一个把人引向错修法的警报，比没有警报更糟。裁剪留在报告行里。
    if nodim:
        warn(f"{len(nodim)} 张上站图没有 cover_w/cover_h —— 版式算不出画幅档，只能靠加载后回流")
    return {"live": len(live), "by_kind": by_kind, "off_site": len(off),
            "real_without_image": len(claim), "wrong_real": len(wrong_real),
            "foreign_host": len(foreign), "foreign_claimed": len(claimed),
            "ours_shots": len(ours), "wrong_repo": len(other_repo),
            "looks_input": len(looks_in),
            "dup_dim": len(dup_dim),
            "out_of_tier": len(crop), "heavy_crop": sum(1 for c in crop if c[0] >= 30),
            "no_dim": len(nodim)}


# ------------------------------------------- 8. 短版局限 / 年龄口径 ---
# `limit_brief_zh` 是卡片上唯一那行诚实话。它最容易坏的方式**不是写得差，是被截断**：
# 一句完整的短处砍成前 24 字，读起来就成了勾人往下点的钩子 —— 诚实变成营销。
# 所以这里查的是「它是不是一句话」，不是「它长不长」。
BRIEF_MAX = 30
_SENT_END = "。！？!?"
_GENERIC = r"仅供参考|自行判断|请谨慎|注意安全|因人而异"

def check_brief_and_age(items: dict) -> dict:
    print("\n【8】短版局限 limit_brief_zh · 年龄口径 age_source")
    shelved = [it for it in items.values() if not it.get("hide")]
    have = [it for it in shelved if (it.get("limit_brief_zh") or "").strip()]
    over = [it for it in have if len(it["limit_brief_zh"].strip()) > BRIEF_MAX]
    unfinished = [it for it in have if it["limit_brief_zh"].strip()[-1] not in _SENT_END]
    generic = [it for it in have if re.search(_GENERIC, it["limit_brief_zh"])]

    # 截断检测：去掉句末标点后如果正好是 limit_zh 的前缀，看那个切点在原文里是不是句子边界。
    # 不是边界 = 从句子中间切开又补了个句号，那是伪装成完整句的截断。
    truncated, first_sentence = [], []
    for it in have:
        b = it["limit_brief_zh"].strip()
        full = (it.get("limit_zh") or "").strip()
        if not full:
            continue
        stem = b.rstrip(_SENT_END)
        if not stem or not full.startswith(stem):
            continue
        nxt = full[len(stem):len(stem) + 1]
        if nxt and nxt in _SENT_END:
            first_sentence.append(it)      # 取了完整版的第一句 —— 合法，但值得回看
        else:
            truncated.append(it)           # 从句子中间切的

    print(f"  在架 {len(shelved)} · 写了短版 {len(have)} · 缺 {len(shelved) - len(have)}")
    if over:
        err(f"{len(over)} 件的 limit_brief_zh 超过 {BRIEF_MAX} 字 —— 卡片上它头顶还压着一整条点评")
        for it in over[:5]:
            print(f"    [超长] {it['id']}: {len(it['limit_brief_zh'])} 字")
    if unfinished:
        err(f"{len(unfinished)} 件的 limit_brief_zh 没有句末标点 —— 要求是完整句，不是短语")
        for it in unfinished[:5]:
            print(f"    [不成句] {it['id']}: {it['limit_brief_zh']!r}")
    if truncated:
        err(f"{len(truncated)} 件的 limit_brief_zh 是从 limit_zh 句子中间切开再补句号的 —— "
            f"那是伪装成完整句的截断，正是这个字段要防的东西")
        for it in truncated[:5]:
            print(f"    [伪完整句] {it['id']}: {it['limit_brief_zh']!r}")
    if generic:
        err(f"{len(generic)} 件的 limit_brief_zh 是通用免责，不是这件东西真实的短处")
    # 成对性：流里给短的、详情给全的 —— 全的那份必须真的存在，否则「点进去看完整版」是空头承诺。
    orphan = [it for it in have if not (it.get("limit_zh") or "").strip()]
    if orphan:
        err(f"{len(orphan)} 件只有短版 limit_brief_zh 而没有完整版 limit_zh —— "
            f"卡片上那句短话代表着一条并不存在的完整局限，点进详情页是空的")
        for it in orphan[:5]:
            print(f"    [无完整版] {it['id']}: {it['limit_brief_zh']!r}")
    if first_sentence:
        warn(f"{len(first_sentence)} 件的 limit_brief_zh 就是 limit_zh 的第一句原文 —— "
             f"合法，但请确认这条真的是「最能劝退错的人的那一条」，而不是图省事取了开头")
        for it in first_sentence[:5]:
            print(f"    [取了第一句] {it['id']}: {it['limit_brief_zh']!r}")

    # --- 年龄口径 ---
    src = {}
    for it in shelved:
        src[it.get("age_source", "")] = src.get(it.get("age_source", ""), 0) + 1
    have_repo = sum(1 for it in shelved if (it.get("repo_created_at") or "").strip())
    have_file = sum(1 for it in shelved if (it.get("skill_first_seen") or "").strip())
    subdir = sum(1 for it in shelved if (it.get("path") or "").strip())
    print(f"  年龄：repo_created_at 有 {have_repo} 件 · skill_first_seen 有 {have_file} 件 · "
          f"子目录货 {subdir} 件（对这些，仓库年龄答非所问）")
    print(f"  age_source 分布：" + " · ".join(
        f"{k or '（空=不显示）'} {v}" for k, v in sorted(src.items())))
    # 口径和数据必须对得上，否则前端会照着一个假标签显示日期
    bad = [it for it in shelved
           if (it.get("age_source") == "repo" and ((it.get("path") or "").strip()
                                                   or not (it.get("repo_created_at") or "").strip()))
           or (it.get("age_source") == "file" and not (it.get("skill_first_seen") or "").strip())]
    if bad:
        err(f"{len(bad)} 件的 age_source 和实际数据不符 —— 口径标签一旦说谎，"
            f"前端就会照着它印一个答非所问的日期")
        for it in bad[:5]:
            print(f"    [口径不符] {it['id']}: source={it.get('age_source')!r} "
                  f"path={it.get('path')!r} repo={it.get('repo_created_at')!r} "
                  f"file={it.get('skill_first_seen')!r}")
    return {"brief_have": len(have), "brief_over": len(over),
            "brief_unfinished": len(unfinished), "brief_truncated": len(truncated),
            "brief_first_sentence": len(first_sentence), "brief_orphan": len(orphan),
            "age_repo": have_repo, "age_file": have_file, "age_src": src,
            "age_mismatch": len(bad)}


# --------------------------------------------------- 7. 货架上印的数字 ---
# 星数、evals、skill_count 已经是同一个病的第三次发作：**印给用户看的数字没有核过来源。**
# 规矩写在 editorial/feedback.json 的 patterns 里，这里是它的可执行部分。
#
# skill_count 是唯一还对外印出的数字（星数已经断了前端出口）。
#
# **这段话被自己纠正过两次，两次错的都不是数字是措辞** —— 同 D39/D43 那一族病，
# 所以订正过程留在这里，比结论有用：
#
#   一、「印在卡片上」是错的。首页 `index.html` 里 `skill_count` 一次都没出现。
#       真正的出口是**可爬层**：详情页 `i/<id>/index.html` 和 `llms.txt` /
#       `llms-full.txt` 里那句 `The repository ships N skills in total.`
#       （`seo/build_seo.py`）。说错出口 = 让人去改一个根本没印它的地方。
#
#   二、「含测试夹具，尚未收窄」是过期的。`skill_scout.find_skill_mds` 早就带着
#       `FIXTURE_DIRS`（tests / golden / fixtures / testdata …）排除了。
#       它只对新进的货生效，存量不重算 —— 但那是「存量待刷」，不是「口径没定」。
#
#   三、「没人核过」是错的，而且错得最重。`docs/DEBT.md` 记着：在架合集**逐个
#       `git clone --filter=blob:none --depth 1` 数过真实的 SKILL.md**，订正了 11 件，
#       **其中 3 件是往上改的**（原来的数不只虚高，是两个方向都错）。
#
# 所以这条 WARN 剩下的真内容只有一句：**数字核过了，选品判断还没做。**
# 一件印着几十件的合集，按 `CURATION.md` 问二「大而全的数量堆」该不该留，
# 要人读了仓库内容才判得了 —— **那是需要人判断的事，不是我们的欠账。**
# 把「等人判」写成「没人核」，就是把一件已经做完的工作重新记成缺口。
COUNT_SUSPECT = 40

def check_counts(items: dict) -> dict:
    print("\n【7】货架上印的数字 skill_count")
    shelved = [it for it in items.values() if not it.get("hide")]
    fat = sorted((it for it in shelved if (it.get("skill_count") or 0) > COUNT_SUSPECT),
                 key=lambda x: -(x.get("skill_count") or 0))
    zero = [it for it in shelved if not (it.get("skill_count") or 0)]
    total = sum(it.get("skill_count") or 0 for it in shelved)
    print(f"  在架 {len(shelved)} 件，对外印出的 skill 数合计 {total}"
          f"（口径：仓库里 SKILL.md 的总数，ingest 已排除 tests/golden/fixtures，存量不重算）")
    print(f"  出口不是首页卡片，是可爬层：详情页 i/<id>/ 和 llms.txt 里那句 "
          f"「The repository ships N skills in total.」")
    if fat:
        warn(f"{len(fat)} 件的 skill_count 大于 {COUNT_SUSPECT} —— **数字本身已经核过**"
             f"（docs/DEBT.md：在架合集逐个 clone 数过，订正 11 件，其中 3 件是往上改的），"
             f"这里不是数据欠账。剩下的是**选品判断**：一件印着几十件的合集，"
             f"按 CURATION 问二「大而全的数量堆」该不该留，要人读了仓库内容才判得了")
        for it in fat[:8]:
            print(f"    [{it.get('skill_count'):>4} 件] {it['id']}  ←（等人判，不是等人核）")
    if zero:
        warn(f"{len(zero)} 件的 skill_count 是 0 或缺失 —— 可爬层那句会印出「0 skills」")
        for it in zero[:5]:
            print(f"    [0] {it['id']}")
    return {"total_printed": total, "suspect": len(fat), "zero": len(zero),
            "suspect_at": COUNT_SUSPECT}


# ------------------------------------------------------------- 5. 备料徽章 ---
def check_prep(items: dict) -> dict:
    """备料徽章的实测数 —— 全部本地算，不发一个请求。"""
    import prep_signals as prep
    print("\n【5】备料徽章 prep_badge")
    ev = prep.load_all()
    st = prep.prep_stats(items, ev)
    print(f"  上架 {st['shelved']} · 有正文存档 {st['archived']} · 无存档 {st['no_archive']}")
    print(f"  「备料齐」（≥{st['ready_at']} 条证据）{st['ready']} 件"
          f"（占有存档的 {100*st['ready']/max(st['archived'],1):.0f}%，占上架的 {100*st['ready']/max(st['shelved'],1):.0f}%）")
    print("  逐条命中（分母 = 有存档的件数）：" + " · ".join(
        f"{prep.SIGNAL_LABELS[s][0]} {st['per_signal'][s]}" for s in prep.SIGNAL_ORDER))
    # 无存档要分两种，混在一起报会把一个结构性事实报成本店欠账：
    #   合集（kind=collection）本来就没有「一份正文」可存 —— 全店至今 0 件合集有存档，
    #     这个约定从来不存在，不是漏了。审计逐个 clone 验过：仓库全在，是 404 在根目录的 SKILL.md。
    #   单品缺档才是真欠账（path 记错 / 抓来没存）。
    no_arch = [it for it in items.values()
               if not it.get("hide") and ev.get(it["id"]) is None]
    coll_na = [it for it in no_arch if it.get("kind") == "collection"]
    solo_na = [it for it in no_arch if it.get("kind") != "collection"]
    if coll_na:
        print(f"  其中 {len(coll_na)} 件是合集，合集没有「一份正文」可存 —— "
              f"结构性事实，不是欠账，不必修")
    if solo_na:
        warn(f"{len(solo_na)}/{st['shelved']} 件**单品**取不回 SKILL.md 正文 —— "
             f"这才是我们自己的存档欠账（path 记错 / 抓来没存）。"
             f"它们和「证据不足」在前端不可区分，所以不会被惩罚，但也拿不到本该拿到的徽章")
    elif st["no_archive"]:
        print(f"  单品缺档 0 件 —— 本店在这一项上没有欠账")
    # 徽章会不会只是星数换个马甲？这里把它算出来，不猜。
    buckets = {"0": [], "1-99": [], "100+": []}
    for it in items.values():
        if it.get("hide"):
            continue
        e = ev.get(it["id"])
        if e is None:
            continue
        s = it.get("stars", 0)
        buckets["0" if s == 0 else ("1-99" if s < 100 else "100+")].append(len(e))
    print("  与星数的关系（备料齐占比，看徽章有没有变成星数的马甲）：")
    for k, v in buckets.items():
        if v:
            print(f"    ★{k:5s} n={len(v):3d}  备料齐 {sum(1 for x in v if x >= st['ready_at'])} 件"
                  f"（{100*sum(1 for x in v if x >= st['ready_at'])/len(v):.0f}%）")
    picks = [it for it in items.values() if it.get("pick") and not it.get("hide")]
    got = [it for it in picks if len(ev.get(it["id"]) or []) >= st["ready_at"]]
    if picks and not got:
        warn(f"推荐位 {len(picks)} 件里一件都没拿到备料徽章 —— 首屏还是空的。"
             f"徽章解决不了推荐位，那里能用的信号只有「店长读过」")
    return st


# --------------------------------------------------- 13. 英文一等公民 ---
# 转向全球 C 端之后，英文版必须能**独立成立**：它不是中文的回落，回落一次
# 就是给英文读者一张缺角的卡片。前十二项守卫里没有一项管英文 —— 这一节补上。
#
# 四条，每条对应一次真实发作，不是照着「应该查什么」想出来的：
#
#   A. 四件套缺失。title_en / tagline_en / why_en / limit_en 是英文卡片的全部内容，
#      缺任何一条，英文读者看到的就是空行或中文。逐件点名，ERROR。
#
#   B. 英文文案里的星数。产品的四条设计硬判断第一条就是「杀掉星数」——
#      星数是滞后且有偏的指标，会亏待新发布、垂直、非英语、无营销的好项目，
#      而我们自己的选品标准正是靠这一条才收得下那些 ★0 的中文垂直货。
#      **这条已经复发过一次**：中文侧清干净之后，英文侧还留着 5 处，
#      是人工一条条读出来的。人读得出来的东西，机器就该替人读。
#
#      只抓**带数字的星数**，不抓 `star` 这个词本身。理由是实测的，不是推想的：
#        - `Flying Star`  —— 玄空飞星的英译，在架的风水那件正文里就有
#        - `earns a star` —— 「值一颗星」的比喻
#        - `start / restart / starts / starting` —— 在架 20 多处，全是正常英文
#      抓词 = 至少 20 条误报；抓「数字 + star」= 5 条全中、0 误报。
#      **一个当前唯一输出是误报的守卫就是噪音（D24）**，所以口径必须窄到只剩那个被禁的东西。
#
#   C. 标题回落成标识符。前端曾经在英文版印出 `city-salary`、`codex-ppt` 这种
#      **仓库文件名**当标题 —— 那是 `name` 字段，不是标题。它不会触发 A（字段非空），
#      也不会触发任何长度检查（长度正常），**从数据上唯一能认出来的痕迹就是它的形状**：
#      跟 `name` / `id` 一模一样，或者全小写 + 连字符 + 没有空格。
#
#   D. 英文里的中文字符。说明漏翻了 —— 但**不是所有中文都是漏翻**：
#      在架实测的 3 处 CJK 全部是**原样引用**（`情绪模块.md` / `节奏.md` 是这件 skill
#      要读的真实文件名，`[待补` 是它往大纲里写的字面标记）。把这三处报成「漏翻」，
#      错的不是数字是**性质** —— 同 D39/D43 那一族病。
#      所以文件名（后接 .md/.json/…）、反引号内、方括号/引号内的中文一律先摘出去，
#      单列成一行陈述让人自己看；**剩下的散文才报 WARN**。
#
#   E.（顺手，同一次扫描里发现的）英文文案被截断。三条英文局限停在 240 字整、
#      末尾没有句末标点，其中 `liamgvchi` 中文写的是「还不像就**直说没做到**」，
#      英文切在 `then say` —— **被切掉的正好是那句诚实话**。
#      这就是 D23/D26 那个失败模式的英文版：诚实变成营销，而且连破绽都没有了。
#      中文侧的 `limit_brief_zh` 已经有「是不是完整句」这一档 ERROR，英文侧一直没有。
EN_FIELDS = ("title_en", "tagline_en", "why_en", "limit_en")

# 只匹配「数字挨着 star」和星号本身。`\d` 是这条规则的全部精度来源。
EN_STARS = re.compile(
    r"★|☆"
    r"|\b\d[\d,.]*\s*[kKmM]?[\s‐-―-]*stars?\b"
    r"|\bstars?\b\s*[:：]?\s*\d",
    re.I)

# 全小写 + 至少一个 . _ - 分隔 + 没有空格 = 仓库文件名的形状，不是标题的形状。
EN_IDENT = re.compile(r"^[a-z0-9]+([._-][a-z0-9]+)+$")

_CJK = re.compile(r"[㐀-䶿一-鿿豈-﫿]+")
# 原样引用的三种形态：后接扩展名 / 反引号内 / 方括号·引号内
_FILE_EXT = re.compile(r"^\s*\.(md|markdown|json|ya?ml|txt|py|js|ts|csv|html?|xlsx?|toml|ini)\b", re.I)
_SENT_END_EN = ".!?\"”』」)】"


def _cjk_literal_reason(text: str, m: re.Match) -> str:
    """这一段中文是不是**原样引用**（文件名 / 字面标记）？是就返回理由，不是就返回 ""。"""
    after = text[m.end():]
    if _FILE_EXT.match(after):
        return "文件名"
    before = text[:m.start()]
    if before.count("`") % 2 == 1:                     # 落在一对反引号中间
        return "反引号内的字面量"
    # `before[-1:] in "…"` 会在 before 为空时返回 True（空串是任何串的子串）——
    # 那样一整段纯中文文案会被当成「字面标记」放过，正是这条守卫最该抓的东西。
    # 造假数据时抓到的，所以这里必须先判非空。
    if (before and before[-1] in "[【「“\"'（(") or (after and after[0] in "]】」”\"'）)"):
        return "方括号/引号里的字面标记"
    return ""


def check_english(items: dict) -> dict:
    print("\n【13】英文一等公民 title_en / tagline_en / why_en / limit_en")
    shelved = [it for it in items.values() if not it.get("hide")]
    print(f"  在架 {len(shelved)} 件")

    # --- A. 四件套缺失 ---
    missing: dict[str, list[str]] = {}
    for f in EN_FIELDS:
        gone = [it["id"] for it in shelved if not (it.get(f) or "").strip()]
        if gone:
            missing[f] = gone
    if missing:
        for f, ids in missing.items():
            err(f"{len(ids)} 件缺 {f} —— 英文版这一行是空的，英文读者拿到的是缺角的卡片")
            for i in ids:
                print(f"    [缺 {f}] {i}")
    else:
        print(f"  四件套：{ ' · '.join(f + ' 齐' for f in EN_FIELDS) }")

    # --- B. 星数 ---
    stars = []
    for it in shelved:
        for f in EN_FIELDS:
            v = it.get(f) or ""
            for m in EN_STARS.finditer(v):
                stars.append((it["id"], f, m.group(0),
                              v[max(0, m.start() - 30):m.end() + 30]))
    if stars:
        err(f"{len(stars)} 处英文文案里印着星数 —— 「杀掉星数」是产品的设计硬判断，"
            f"中文侧清干净之后英文侧复发过一次，这里逐处点名")
        for i, f, hit, ctx in stars:
            print(f"    [星数] {i} · {f} · {hit!r}")
            print(f"           …{ctx}…")
    else:
        print("  星数：0 处 —— 干净")

    # --- C. 标题回落成标识符 ---
    ident = []
    for it in shelved:
        t = (it.get("title_en") or "").strip()
        if not t:
            continue
        why = ""
        if t.lower() == (it.get("name") or "").strip().lower():
            why = "跟 name 一模一样"
        elif t.lower() == (it.get("id") or "").strip().lower():
            why = "跟 id 一模一样"
        elif EN_IDENT.match(t):
            why = "全小写 + 连字符 + 无空格，是仓库文件名的形状"
        if why:
            ident.append((it["id"], t, why))
    if ident:
        err(f"{len(ident)} 件的 title_en 回落成了标识符 —— 那是仓库文件名，不是标题。"
            f"英文读者看到的是 `city-salary` 这种东西，它不回答「这是什么」")
        for i, t, why in ident:
            print(f"    [标识符标题] {i}: {t!r} —— {why}")
    else:
        print("  标题回落：0 件")

    # --- D. 中文残留 ---
    leak, quoted = [], []
    for it in shelved:
        for f in EN_FIELDS:
            v = it.get(f) or ""
            for m in _CJK.finditer(v):
                reason = _cjk_literal_reason(v, m)
                row = (it["id"], f, m.group(0), reason)
                (quoted if reason else leak).append(row)
    if quoted:
        print(f"  英文里的中文：{len(quoted)} 处是原样引用（不是漏翻，不报）：")
        for i, f, s, reason in quoted:
            print(f"    [{reason}] {i} · {f} · {s!r}")
    if leak:
        warn(f"{len(leak)} 处英文文案里残留中文散文 —— 漏翻了，英文读者读不懂这一段")
        for i, f, s, _ in leak:
            print(f"    [漏翻] {i} · {f} · {s!r}")
    elif not quoted:
        print("  英文里的中文：0 处")

    # --- E. 被截断 ---
    # 标题不在此列：英文标题本来就不带句号。
    cut = []
    for it in shelved:
        for f in ("tagline_en", "why_en", "limit_en"):
            v = (it.get(f) or "").strip()
            # 句末标点允许在收尾引号 / 括号**里面** ——
            # `…never 'Great job completing all those tasks!'` 是写完了的句子，
            # 感叹号在引号内，最后一个字符是引号。原来只看最后一个字符，
            # 于是把一句完整的话报成截断。**差点因此去改一句本来没问题的文案 ——
            # 改文案迎合守卫，和在句读处切得干净一样，是把问题藏起来。**
            tail = v.rstrip("'\"’”)]}»")
            if v and (not tail or tail[-1] not in _SENT_END_EN):
                cut.append((it["id"], f, len(v), v[-34:]))
    if cut:
        err(f"{len(cut)} 处英文文案没有英文句末标点 —— 要么是被截断（不是写完了），"
            f"要么句末标点还留着中文的。中文侧 limit_brief_zh 早就有这一档，"
            f"英文侧一直没有；被切掉的往往正好是最后那句诚实话")
        for i, f, n, tail in cut:
            print(f"    [截断] {i} · {f} · {n} 字 · 结尾 …{tail!r}")
    else:
        print("  截断：0 处")

    return {"shelved": len(shelved),
            "missing": {f: len(v) for f, v in missing.items()},
            "stars": len(stars), "ident_titles": len(ident),
            "cjk_leak": len(leak), "cjk_quoted": len(quoted), "truncated": len(cut)}



# ---------------------------------------------------------------------------
# 【18】心选件被下架却没写理由
#
# 2026-08-28 那次提标准（「Gate the shelf: slogan + 8/10 taste filter」→
# 「Cut shelf to 48」）把在架从 279 砍到 48，其中**包含店主亲手标的 73 件里的 57 件**，
# 而 57 件**一件都没写理由**。到 08-31 才被发现，中间三天货架是 104 件、每天照跑。
#
# editorial/hearts.json 自己的第三条写着：
#   「任何新判据都要拿这批回测：判据把它们判掉了，是判据错，不是它们错。」
#
# 这条守卫不禁止下架心选件 —— 店主的判断也会变，货也会烂掉。
# 它只要求**写一行为什么**。理由要动手写；整批 hide 什么都不用写。
# **闸门装在「什么都不做就会出错」的那一侧。**
def check_hearted_hidden(items: dict):
    hearts = (lib.read_json(os.path.join(lib.ROOT, "editorial", "hearts.json"), None) or {})
    ids = set(hearts.get("ids") or [])
    silent, withreason = [], []
    for i in sorted(ids):
        it = items.get(i)
        if not it or not it.get("hide"):
            continue
        why = (it.get("unheart_reason") or "").strip()
        (withreason if len(why) >= 10 else silent).append((i, why))
    print("\n【18】心选件下架要写理由")
    print(f"  店主标过 {len(ids)} 件 · 在架 {len(ids) - len(silent) - len(withreason)} · "
          f"下架且写了理由 {len(withreason)} · **下架却没写理由 {len(silent)}**")
    for i, _ in silent[:12]:
        print(f"  [没写理由] {i}")
    for i, why in withreason[:6]:
        print(f"  [已判过] {i} — {why}")
    if silent:
        print("  补法：在 editorial/curation.json 该件下写 unheart_reason（至少 10 字）")
    return silent


def main() -> None:
    show_list = "--list" in sys.argv
    as_json = "--json" in sys.argv
    strict = "--strict" in sys.argv

    print("品味 · 编辑层体检")
    print(f"仓库: {lib.ROOT}")
    items = apply_all(load_all())
    lim = check_limits(show_list)
    rej = check_rejected(items)
    hl = check_headline(items)
    check_freshness()
    prep = check_prep(items)
    inst = check_install(items)
    cnts = check_counts(items)
    brief = check_brief_and_age(items)
    cov = check_covers(items)
    red = check_red_lines(items)
    eng = check_english(items)
    shelf = [it for it in items.values() if not it.get("hide")]
    verdicts = check_verdict_in_limits(shelf)
    gen_dirs, clashes = check_install_dirs(list(items.values()))
    bare = check_no_placeholder(list(items.values()))
    unheart = check_hearted_hidden(items)
    if unheart:
        err(f"{len(unheart)} 件店主亲手标过的货被下架却没写理由 —— "
            f"hearts.json 第三条：判据把这批判掉了，是判据错，不是它们错。"
            f"真要下架就写 unheart_reason")
    # 库房积压：进了货、没人写文案，所以永远上不了架。
    # 这个数只有变大没有变小时，说明进货和文案之间断了（多半是 LLM_API_KEY 没配）。
    # 2026-08-31 发现时是 720 件，断了 13 天没人看见 —— 因为它以前不是一个数字。
    _backlog = [i for i, it in items.items()
                if it.get("hide") and not (it.get("title_zh") or "").strip()]
    print(f"\n【19】库房积压（有货没文案，上不了架）\n  {len(_backlog)} 件")
    if len(_backlog) > 200:
        warn(f"库房积压 {len(_backlog)} 件「有货没文案」—— 进货和文案之间多半断了。"
             f"先查 LLM_API_KEY 配没配（gh secret list -R woowoeth/skill），"
             f"再决定这批怎么消化：**别一次倒进货架**")
    # 【20】在架却没有封面 —— 待办清单，不是判决。
    # 两个正样本组一致显示封面是货架的标准（在架 99% 有 · 库房 28%），
    # 但拿它当入闸条件会砍掉 42% 的心选（30 件心选没封面）。
    # **缺封面是待办，不是判决**，所以这里只列不拦。
    _nocover = [i for i, it in items.items()
                if not it.get("hide") and not (it.get("cover") or it.get("cover_url"))]
    _hearts = set((lib.read_json(os.path.join(lib.ROOT, "editorial", "hearts.json"), None)
                   or {}).get("ids") or [])
    _nc_heart = [i for i in _nocover if i in _hearts]
    print(f"\n【20】在架没封面（待办，不拦车）\n  {len(_nocover)} 件 · 其中店主标过的 {len(_nc_heart)} 件")
    for i in _nc_heart[:8]:
        print(f"  [心选缺封面] {i}")
    if _nocover:
        warn(f"{len(_nocover)} 件在架没封面（其中心选 {len(_nc_heart)} 件）—— "
             f"在架货 99% 有封面、库房只有 28%，封面是这个货架的标准之一。"
             f"**但它是待办不是判决**：拿它当入闸条件会砍掉 42% 的心选")
    # 【21】还在靠默认预览卡兜底的（待办，不拦车）
    _og = [i for i, it in items.items()
           if not it.get("hide") and (it.get("cover_kind") or "") == "og" and (it.get("cover") or "")]
    print(f"\n【21】还在用默认预览卡兜底\n  {len(_og)} 件 —— 优先级是「仓库里的图 > 预览卡」")
    if _og:
        warn(f"{len(_og)} 件封面还是 GitHub 默认预览卡 —— 能上站（店主 2026-08-31 定的兜底），"
             f"但仓库里有真图就该换掉它")
    # 【22】封面文件和记录对不上 —— 09-03 店主：「卡片图下面多了一条灰色」。CI 把预览卡同名覆盖了真图，
    # 记录还是真图的宽高，容器按真图撑开、装的是 1200×600 的卡。这条不是待办，是事故：亮红。
    _mis = []
    for _it in (items.values() if isinstance(items, dict) else items):
        _u = (_it.get("cover") or "")
        # 只看在架、且记录了宽高的：没记宽高的是【20】/宽高守卫的事，不在架的没人看
        if _it.get("hide") or not _u.startswith("/skill/") or not (_it.get("cover_w") and _it.get("cover_h")):
            continue
        _p = os.path.join(lib.ROOT, _u[len("/skill/"):])
        if not os.path.exists(_p):
            _mis.append((_it["id"], "文件不存在")); continue
        try:
            import skill_scout as _S
            _wh = _S.cover_dims(_p)
        except Exception:
            _wh = None
        if _wh and (_wh[0], _wh[1]) != (_it.get("cover_w"), _it.get("cover_h")):
            _mis.append((_it["id"], f"记录 {_it.get('cover_w')}x{_it.get('cover_h')} 文件 {_wh[0]}x{_wh[1]}"))
    print(f"\n【22】封面文件 vs 记录\n  {len(_mis)} 件对不上")
    for _m in _mis[:12]:
        print(f"    {_m[0]}  {_m[1]}")
    if _mis:
        err(f"{len(_mis)} 件封面文件和记录的宽高对不上（或文件不存在）—— 容器按记录撑开、装的是别的图，卡下面就是一条灰。"
            f"跑 scouts/repair_covers.py")
    # 【23】编辑挑的（editor_picks）理由要 ≥30 字，否则门闸不认，等于白挑
    _eds = (lib.read_json(os.path.join(lib.ROOT, "editorial", "editor_picks.json"), {}) or {}).get("items", {})
    _short = [k for k, v in _eds.items() if len((v.get("reason") or "").strip()) < 30]
    print(f"\n【23】编辑挑的 {len(_eds)} 件 · 理由不足 30 字 {len(_short)} 件")
    if _short:
        err(f"{len(_short)} 件编辑挑的理由不到 30 字（门闸不认）：{', '.join(_short[:5])}")
    # 【24】店长推荐：每一件都得有作者真图（文件真在）且四段文案齐 —— 店主 09-03：「至少要有图」。标准见 scout_lib.refresh()。
    # pick 由 refresh() 在内存里重算、只落进 feed.json；skills/*.json 里那些是 8/28 的遗留，读它会误报
    _feed_items = (lib.read_json(os.path.join(lib.ROOT, "skills", "feed.json"), {}) or {}).get("skills", [])
    _pinned_ids = set((lib.read_json(os.path.join(lib.ROOT, "editorial", "picks_pinned.json"), {}) or {}).get("ids", []))
    _picks = [_it for _it in _feed_items if _it.get("pick") and _it.get("id") not in _pinned_ids]   # 钉住的 12 件店主定的，不检查
    _bad_pick = []
    for _it in _picks:
        _u = _it.get("cover") or ""
        _ok_cover = _it.get("cover_kind") in ("hero", "artwork", "ours", "diagram") and _u and (
            os.path.exists(os.path.join(lib.ROOT, _u[len("/skill/"):])) if _u.startswith("/skill/") else _u.startswith("http"))
        _ok_copy = all(len((_it.get(k) or "").strip()) >= 8 for k in ("title_zh", "tagline_zh", "why_zh", "limit_zh"))
        if not (_ok_cover and _ok_copy):
            _bad_pick.append((_it["id"], "没真图" if not _ok_cover else "文案缺"))
    print(f"\n【24】店长推荐（编辑追加的）{len(_picks)} 件 · 不合格 {len(_bad_pick)} 件 · 另钉住 {len(_pinned_ids)} 件不检查")
    if _bad_pick:
        err(f"{len(_bad_pick)} 件店长推荐没有真图或文案不齐：{_bad_pick[:5]} —— 推荐位是店的脸，refresh() 应该已经筛掉，查 scout_lib")
    badnames = check_upstream_names(items)
    badtitles = check_title_shape(items)
    if badtitles:
        warn(f"{len(badtitles)} 件的标题只有禁令、没说「你拿到手的是什么」—— "
             f"实测这一类的心选率 9%，说出产出物的是 43%（docs/CURATION.md 问三·补）")
    unscanned, stale_scan, unverif_scan, old_scan = check_scan_archive(items)
    # 新旧分档。**一条永远红着的 ERROR 会被人学会忽略，那比没有它更糟。**
    #
    # 这条守卫上线那一刻，在架 226 件里 226 件都没有扫描存档 —— 如果一律判 ERROR，
    # 构建从此永远是红的，而「反正它一直红」这句话一旦成立，这条守卫就死了
    # （同一天已经有过一个从不执行的守卫，它比没有守卫更糟，因为让人以为有人在看着）。
    #
    # 所以：**从 SCAN_MANDATORY_FROM 起上架的，没扫过 = ERROR 阻断；
    # 那天之前的存量，WARN + 报出还剩多少件。** 存量清零那天这一档自然消失，
    # 不需要谁记得回来删。
    SCAN_MANDATORY_FROM = "2026-08-20"          # 扫描器落地当天，从这天起上架必须先扫
    new_unscanned = [i for i in unscanned
                     if (items[i].get("added_at") or "") >= SCAN_MANDATORY_FROM]
    old_unscanned = [i for i in unscanned if i not in set(new_unscanned)]
    if new_unscanned:
        err(f"{len(new_unscanned)} 件是 {SCAN_MANDATORY_FROM} 起上架的、却没有红线扫描存档 —— "
            f"没扫过的东西不该在架上（scouts/scan_refs.py 扫完自动落盘）")
    if old_unscanned:
        warn(f"存量欠账：{len(old_unscanned)} 件（{SCAN_MANDATORY_FROM} 之前上架的）"
             f"还没过红线扫描 —— 这一档是 WARN 不是 ERROR，因为一条永远红着的 ERROR "
             f"会被人学会忽略。清零办法：scouts/scan_refs.py --file <picks.json>")
    if stale_scan:
        err(f"{len(stale_scan)} 件的扫描存档已作废：扫过之后正文存档又变了 —— "
            f"扫的是旧正文，等于没扫这一版")
    if old_scan:
        warn(f"{len(old_scan)} 件是用旧版判据扫的 —— **旧尺子扫过 ≠ 按现在的判据扫过**。"
             f"这不是 ERROR（旧尺子扫过不等于有问题），但欠账要可见："
             f"隐形的欠账比红着的守卫危险。补法见【16】末尾")
    if unverif_scan:
        warn(f"{len(unverif_scan)} 件的扫描版本无法本地核验（缺 methods/ 正文存档）—— "
             f"读不到不等于有问题，但也不等于已核对")
    if bare:
        err(f"{len(bare)} 件在架却没人写过文案 —— 上架是人写完文案之后的动作，不是抓取的副作用")
    if badnames:
        warn(f"{len(badnames)} 件的上游 frontmatter name 不是小写连字符 —— "
             f"装机目录和 name 会对不上，必须在 limit 里披露，不许静默上架")
    # 【11】的严重程度是 D36 定的：「命中即 ERROR，逼人回去重过三问」。
    # 【12】D46 没写档位 —— 不替产品发明一个，按点名处理。
    if verdicts:
        err(f"{len(verdicts)} 件的 limit_zh 已经等于一份判决书 —— "
            f"诚实局限写出了该拒的理由，然后这件还在架上。回去重过三问")
    if gen_dirs:
        warn(f"{len(gen_dirs)} 件装进了通用目录（skill/ skills/ src/ …）—— "
             f"安装目标会互相静默覆盖，用户不会收到任何提示")
    if clashes:
        warn(f"{len(clashes)} 组安装目录重名 —— 装了后一个，前一个被静默覆盖")

    # ---- 自查：每一个 check_* 都必须真的被 main() 叫到 ----
    #
    # 这不是洁癖。这个文件已经犯过**两次**同一个错：守卫定义在
    # `if __name__ == "__main__": main()` 之后，于是从来没执行过一次，
    # 而裁决文档里写着它「命中 0，干净上线」（D52 记的是【11】【12】）。
    # 修 D52 时我把入口挪到了当时的文件末尾，并在旁边写下「入口必须留在文件最末」——
    # **然后把新加的【14】追加在了它后面，一模一样地重造了这个 bug。**
    #
    # 靠「记住把入口放最后」防不住，因为出错的方式是「在末尾追加代码」，
    # 而那正是加新守卫时最自然的动作。所以改成静态自查：
    # 扫本模块所有 check_* 函数，凡是没出现在 main() 源码里的，立刻红。
    # **一个从不执行的守卫比没有守卫更糟：它让人以为那一面已经有人看着了。**
    # 判据是「**在本文件里有没有任何地方调用它**」，不是「main() 里有没有」——
    # 有的守卫是被别的守卫调的（check_against 由 check_rejected 调用 schema 校验），
    # 只看 main() 会把它误报成死代码。要抓的那个 bug 是「定义了、谁都没调」。
    import inspect as _insp
    _mod = _insp.getsource(_insp.getmodule(main))
    _defined = sorted(n for n, o in list(globals().items())
                      if n.startswith("check_") and callable(o))
    _never = []
    for n in _defined:
        # 去掉它自己的 def 行，再看还有没有 `n(` 出现
        _rest = _mod.replace(f"def {n}(", "")
        if f"{n}(" not in _rest:
            _never.append(n)
    if _never:
        err(f"{len(_never)} 个守卫定义了但 main() 从来没调用：{_never} —— "
            f"从不执行的守卫比没有守卫更糟")

    print("\n" + "=" * 60)
    for m in ERRORS:
        print(f"ERROR  {m}")
    for m in WARNS:
        print(f"WARN   {m}")
    print(f"\n{len(ERRORS)} error / {len(WARNS)} warn")

    if as_json:
        print(json.dumps({"limits": lim, "rejected": rej, "headline": hl, "prep": prep, "install": inst, "counts": cnts, "brief_age": brief, "covers": cov, "red_lines": red, "english": eng,
                          "errors": ERRORS, "warns": WARNS}, ensure_ascii=False, indent=1))
    sys.exit(1 if (ERRORS and strict) else 0)


# ---------------------------------------------------------------------------
# 【11】局限里的判决书 —— 查我们自己的嘴，不是查它的成分
#
# 由存量审计发现的流程漏点，不是眼力漏点：
#   blockrunai-clawrouter 的 limit_zh 写着「自动生成 EVM 私钥并明文落盘，
#   还捆着真金白银下注 Polymarket 的工具」——**然后它还在架上**。
#   donchitos 的 limit_zh 写着「它是一整个项目模板，不是能一件件拆下来装的商品」
#   ——而「不是商品」正是选品问一的原话。
#
# 也就是说：诚实局限字段已经把该拒的理由写出来了，但写完之后**没有一个动作
# 把它送回三问**。红线和问一被降级成了「卡片上的一句卖诚实的文案」。
#
# 这条守卫不判商品的成分（那是人的活），只判**我们自己写下的那句话是不是
# 已经等于一份判决书**。命中就 ERROR，逼人回去重过三问。
# ---------------------------------------------------------------------------
VERDICT_PATTERNS = [
    # 「不是 skill」曾经在这里，收窄掉了：agnix 的局限写「校验不是 skill 做的，
    # 是 Rust 二进制做的」——说的是谁做校验，不是它自己不是商品。
    # 一个当前唯一输出是误报的守卫就是噪音（同 D24 的纪律）。
    (r"不是(能一件件拆下来装的)?商品|一整个项目模板|它(本身)?(是|就是)(一个)?框架", "问一 · 局限里已自述不是商品"),
    (r"私钥|助记词|明文落盘|抽(取)?(浏览器)? ?cookie|登录 ?cookie|凭据", "红线 · 局限里已自述涉及凭据"),
    (r"下注|真金白银|下单|交易执行|荐股", "红线 · 局限里已自述涉及金融执行"),
    (r"绕(过)?反爬|anti-?bot|验证码识别|打码", "红线 · 局限里已自述绕过防抓措施"),
    (r"指针壳|全是壳|没有一件拎得出", "问二 · 局限里已自述是数量堆"),
]

def check_verdict_in_limits(items):
    hits = []
    for it in items:
        lim = (it.get("limit_zh") or "")
        for pat, why in VERDICT_PATTERNS:
            m = re.search(pat, lim)
            # 否认句不算判决书 —— 「它明写**不**绕反爬」说的是它不干那件事，
            # 那正是我们要的局限写法，罚它就是在罚诚实。【10】早就有这一档
            # （RED_NEGATED），【11】一直没接上；接上线之前造假数据试出来的。
            if m and not re.search(RED_NEGATED, lim[max(0, m.start() - 12):m.start()]):
                hits.append((it.get("id"), why, lim[:90]))
                break
    print("\n【11】局限里的判决书（我们自己写下的、已等于判决的话）")
    if not hits:
        print("  在架商品里 0 件 —— 干净")
        return []
    for i, why, lim in hits:
        print(f"  [回去过三问] {i}")
        print(f"      {why}")
        print(f"      limit_zh: {lim}…")
    return hits


# ---------------------------------------------------------------------------
# 【12】安装目录碰撞
#
# 生态是**扁平命名空间**：两件来自不同仓库的 skill 可以在 frontmatter 里叫同一个名字
# （实测有两件都叫 deep-research）。装了一个再装另一个，**前一个被静默覆盖，
# 用户不会收到任何提示**。
#
# 这不是我们的 bug，但受伤的是照我们的安装命令抄的人，所以我们得管：
# 碰撞的一律加作者前缀消歧，并在 install.note_zh 里说明「跟原名不一致是故意的」。
#
# 另有一类是我们自己造的：安装目录取了路径末段，而末段是 skill/ skills/ src/
# 这种通用词——曾有 4 件都指向 ~/.claude/skills/skill。根因已在
# scout_lib.make_item 修掉（优先用 frontmatter 的 name），这里做回归防线。
# ---------------------------------------------------------------------------
GENERIC_INSTALL_DIRS = {"skill", "skills", "src", "lib", "packages", "dist",
                        "app", "plugin", "plugins", "template"}

def check_install_dirs(items):
    from collections import Counter
    live = [it for it in items if not it.get("hide")]
    dirs = [((it.get("install") or {}).get("dir") or "", it) for it in live]
    generic = [(it.get("id"), d) for d, it in dirs
               if d.rstrip("/").split("/")[-1].lower() in GENERIC_INSTALL_DIRS]
    cnt = Counter(d for d, _ in dirs if d)
    clash = {d: [it.get("id") for dd, it in dirs if dd == d] for d, n in cnt.items() if n > 1}
    print("\n【12】安装目录碰撞")
    print(f"  在架 {len(live)} 件 · 装进通用目录 {len(generic)} 件 · 目录重名 {len(clash)} 组")
    for i, d in generic:
        print(f"  [通用目录] {i} → {d}")
    for d, ids in clash.items():
        print(f"  [碰撞] {d}")
        for i in ids:
            print(f"      {i}")
    return generic, clash


# ---------------------------------------------------------------------------
# 【14】机器占位文案上架 —— 这条不该由店主替我们发现
#
# 2026-08-20：定时进货员自动上架了 21 件，中文标题/点评/局限、英文四项全空。
# 店主一眼看出来：「上新的内容也都没有，只有个标题」。
#
# 而 CURATION.md 第五节早就写着：
#   「不许『先抓一批、以后再补文案』。那样货架上会长期堆着机器占位文案，
#    用户看到的就是一坨没人管的东西 —— 这是本店犯过的最大错误。」
#   「自动进货（GitHub Actions）只负责往**候选池**里放东西，**不直接上架**。」
#
# 设计写对了，实现是反的（make_item 默认 hide=False，文案靠 LLM_API_KEY 现场写，
# key 没配就整段 except 跳过）。根因已修成默认 hide=True。
# 这条守卫是第二道：**万一又有别的路径把没文案的东西送上架，构建期就红。**
# ---------------------------------------------------------------------------
def check_no_placeholder(items):
    live = [it for it in items if not it.get("hide")]
    need = ("title_zh", "why_zh", "limit_zh")
    bare = [(it.get("id"), [f for f in need if not (it.get(f) or "").strip()])
            for it in live]
    bare = [(i, miss) for i, miss in bare if miss]
    print("\n【14】机器占位文案上架")
    print(f"  在架 {len(live)} 件 · 缺人写文案的 {len(bare)} 件")
    for i, miss in bare:
        print(f"  [没人写过文案] {i} — 缺 {'/'.join(miss)}")
    if bare:
        print("  上架是人写完文案之后的动作，不是抓取的副作用。补文案，或 hide 掉。")
    return bare


# ---------------------------------------------------------------------------
# 【15】上游 frontmatter 的 name 不合小写连字符命名
#
# 本机每一个已装 skill 的 name 都是 `^[a-z0-9]+(-[a-z0-9]+)*$`，但查不到一份
# 能引用的规范原文，**所以这条不断言「装不上」，只要求披露**：
#   · 装机目录来自 slug(name)，name 带空格/括号/中文时，目录和 frontmatter 必然对不上
#   · 读者拿到的是一条会让他困惑的命令，而困惑的成本由他承担
# 触发这条的两件（`陈石营养师 (Mars Chen)`、`贴纸拼图-照片记忆卡skill`）已经在
# limit 里写清了事实和改法。以后的新货必须照做，不许静默上架。
#
# 数据源是 methods/ 里已存档的 SKILL.md 正文 —— **本地零网络**。
# 没有存档的不报（读不到 ≠ 有问题，见 prep_signals 模块头的同一条原则）。
# ---------------------------------------------------------------------------
NAME_OK = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def check_upstream_names(items: dict):
    live = {i: it for i, it in items.items() if not it.get("hide")}
    bad, archived = [], 0
    for sid, it in sorted(live.items()):
        path = os.path.join(lib.ROOT, "methods", f"{sid}.md")
        if not os.path.exists(path):
            continue
        archived += 1
        try:
            with open(path, encoding="utf-8") as f:
                head = f.read(4000)
        except Exception:
            continue
        m = re.search(r"^---\s*\n(.*?)\n---", head, re.S)
        if not m:
            continue
        n = re.search(r"^name:\s*(.+)$", m.group(1), re.M)
        if not n:
            continue
        raw = n.group(1).strip().strip("\"'")
        if NAME_OK.fullmatch(raw):
            continue
        # 分级：**读者装的时候会不会困惑**，不是「合不合正则」。
        #   · 带中文 / 空格 / 括号 → 装机目录和 frontmatter 必然对不上，必须披露
        #   · 纯 ASCII 只是大小写或下划线（AnythingButLaw、my_skill）→ 只报，不催披露
        #     limit_zh 那块地是留给真短处的，不该被一个大小写差异占掉
        soft = raw.isascii() and not any(c in raw for c in " ()[]{}/\\")
        lz = (it.get("limit_zh") or "") + (it.get("limit_en") or "")
        disclosed = ("frontmatter" in lz) or ("name" in lz and "改成" in lz)
        bad.append((sid, raw, disclosed or soft, soft))
    print("\n【15】上游 frontmatter 的 name 是否合小写连字符命名")
    print(f"  在架 {len(live)} 件 · 有正文存档 {archived} · 不合规 {len(bad)}")
    for sid, raw, ok, soft in bad:
        mark = "仅大小写/下划线，不催" if soft else ("已披露" if ok else "**未披露**")
        print(f"  [{mark}] {sid} — name: {raw!r}")
    undisclosed = [b for b in bad if not b[2]]
    if undisclosed:
        print("  未披露的：把事实和改法写进 limit_zh / limit_en，装机目录换成 ASCII slug。")
    return undisclosed


# ---------------------------------------------------------------------------
# 【16】没扫过的东西上不了架 —— 把「记得去跑一遍扫描器」变成机器保证
#
# 2026-08-20 的事故：全架 226 件红线复查下架 6 件，最险的两件是
# 「附子不麻不昏即剂量不够」（把中毒前驱症状写成加量信号）和
# 「电话/远程急救｜破格救心汤原方，附子200g起步」。而 `scouts/scan_refs.py`
# 当时是个**手动**工具 —— 新货全靠选货的人自己记得去跑。
#
# 「靠人记得」在这个文件里已经失效过很多次（拒收榜去重键按 repo 不按 (repo,skill)、
# 守卫定义了没人调、前端扔掉流水线算好的排序）。所以这条守卫不再要求人记得，
# 它要求**磁盘上有证据**：
#
#   · 在架却在 scouts/scan_archive.json 里没有条目 → ERROR。没扫过就不该在架上。
#   · 有条目，但 method_sha256 和当前 methods/<id>.md 对不上 → ERROR。
#     正文存档被重新抓取刷新过，那份扫描结果作废了 —— 扫的是旧正文。
#   · 有条目但指纹为空（扫描当时本地没有正文存档）→ 单独报，不混进上面两档。
#     **读不到 ≠ 有问题，但也 ≠ 已核对**（同 prep_signals 的原则），
#     所以它必须有自己的一行，不许静默计入「干净」。
#
# 为什么比的是本地 sha 而不是上游 sha：比上游要联网，而每次构建都联网这条路是错的。
# 扫描是抓取期的事（那时本来就在联网），守卫只查存档。上游 sha 也存了
# （upstream_tree_sha / skill_md_blob_sha），留给下一次联网扫描去比。
# ---------------------------------------------------------------------------
SCAN_ARCHIVE = os.path.join(lib.ROOT, "scouts", "scan_archive.json")


_SCANNER_NOW = ""


def _scanner_now() -> str:
    """当前 scouts/scan_refs.py 的判据段指纹。读不到就返回空串 —— 空不参与比较。"""
    try:
        import importlib.util
        sp = os.path.join(lib.ROOT, "scouts", "scan_refs.py")
        spec = importlib.util.spec_from_file_location("_sr", sp)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        return m.scanner_sha256()
    except Exception:
        return ""


def _method_sha256(sid: str) -> str:
    import hashlib
    f = os.path.join(lib.ROOT, "methods", f"{sid}.md")
    if not os.path.exists(f):
        return ""
    with open(f, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def check_scan_archive(items: dict):
    live = {i: it for i, it in items.items() if not it.get("hide")}
    global _SCANNER_NOW
    _SCANNER_NOW = _scanner_now()
    doc = lib.read_json(SCAN_ARCHIVE, None) if os.path.exists(SCAN_ARCHIVE) else None
    ent = (doc or {}).get("entries") or {}

    never, stale, unverifiable, old_scanner = [], [], [], []
    for sid in sorted(live):
        row = ent.get(sid)
        if not isinstance(row, dict):
            never.append(sid)
            continue
        archived = (row.get("method_sha256") or "").strip()
        now = _method_sha256(sid)
        if not archived or not now:
            unverifiable.append((sid, "扫描时无正文存档" if not archived else "正文存档已删除"))
        elif archived != now:
            stale.append((sid, row.get("scanned_at", "?")))
        # 尺子换了也算欠账 —— 和「货的正文变了」是两件事，两件都要有指纹。
        # 2026-08-21 补：那天加了「改你agent的规矩」和「悄悄收钱」两张表，
        # 全店 277 件立刻都成了「用旧扫描器扫的」，而守卫一声不响。
        # **隐形的欠账比红的守卫危险。** 这里只 WARN 不 ERROR：
        # 旧尺子扫过 ≠ 有问题，但也 ≠ 按现在的判据扫过。
        if isinstance(row, dict):
            sc = (row.get("scanner_sha256") or "").strip()
            if sc != _SCANNER_NOW:
                old_scanner.append((sid, sc or "无记录"))

    print("\n【16】扫描存档（没扫过的东西上不了架）")
    print(f"  在架 {len(live)} 件 · 有扫描存档 {len(live) - len(never)} · "
          f"没有存档 {len(never)} · 存档对不上当前正文 {len(stale)} · 版本无法本地核验 {len(unverifiable)}")
    if not os.path.exists(SCAN_ARCHIVE):
        print(f"  存档文件还不存在：{os.path.relpath(SCAN_ARCHIVE, lib.ROOT)}")
    for sid in never[:12]:
        print(f"  [没扫过] {sid}")
    if len(never) > 12:
        print(f"      …另外 {len(never) - 12} 件")
    for sid, when in stale[:12]:
        print(f"  [存档作废] {sid} — 扫于 {when}，之后正文存档变过")
    if len(stale) > 12:
        print(f"      …另外 {len(stale) - 12} 件")
    for sid, why in unverifiable[:8]:
        print(f"  [无法核验] {sid} — {why}")
    for sid, sc in old_scanner[:6]:
        print(f"  [旧尺子扫的] {sid} — 存档记的判据版本 {sc}，当前 {_SCANNER_NOW}")
    if len(old_scanner) > 6:
        print(f"      …另外 {len(old_scanner) - 6} 件")
    if never or stale or old_scanner:
        print("  补法：python3 scouts/scan_refs.py <owner/repo>[:path]  —— 扫完自动落盘")
        print("  批量：把 [{repo, path}] 写成 JSON，python3 scouts/scan_refs.py --file picks.json")
    return never, stale, unverifiable, old_scanner


# ---------------------------------------------------------------------------
# 【17】标题只有禁令、没说「你拿到手的是什么」
#
# 2026-08-21 店主标了 73 件当参考标准，数据把这条钉死了（整体心选率 29%）：
#   说出产出物 43%（75 件） · 两者都无 28% · **只有禁令 9%（54 件）**
# 分批控制后更狠：8-20/21 那批「只有禁令」的 38 件只被标中 2 件（5%）。
#
# **这个坏结果是我们自己造出来的。** 任务书里「好标题里都有一个不该出现在这里的
# 东西 —— 一个具体到你会愣一下的细节或**禁令**」被当成唯一判据，于是选货偏向
# 「有硬禁令的」，标题又把禁令摆在最显眼处，产出物被挤出去。
# 「不许 X」回答的是「它不干什么」，而读者要的是「我能拿到什么」。
#
# 这条是 WARN 不是 ERROR：产出物词表永远不全，硬拦会逼人往标题里塞关键词，
# 那比现在更糟。它的作用是**点名让人重读那一句**。
# ---------------------------------------------------------------------------
# 产出物词表。**补了「量词 + 名词」这一档**，因为我自己给的示范通不过我自己的守卫：
#   「照冰箱剩货给**三道菜**，凑不满也不放宽过敏原」
# ——「三道菜」就是产出物，但动词/名词白名单看不见它，`不放` 又命中禁令，
# 于是这条守卫点名了 CURATION.md 里我自己写的正面例子。
# 做文案那位为了让它下来，被迫往标题里加了个「挑出」——
# **那正是这条守卫的注释里自己预警过的：硬拦会逼人往标题里塞关键词。**
TITLE_OUT = re.compile(
    r"做成|生成|出图|出片|出整套|产出|变成|画|写成|做出|拍|剪|排版|算|查|挑|配|录|"
    r"海报|地图|网页|PPT|封面|壁纸|简历|清单|报告|字帖|贴纸|视频|脚本|图谱|方案|"
    r"复盘|路书|笔记|文章|提示词|配方|参数|档案|台账|图|"
    # 实测补：`排成`（词表里只有 `排版`）、`版式`、`短篇`、`长篇`。
    # 「把 Markdown **排成公众号版式**，内联样式不再莫名崩掉」明明说了产出物，却被点名 ——
    # 这正是「词表永远不全」的例子，所以这条守卫是 WARN、件数不是 KPI。
    r"排成|版式|短篇|长篇|封面图|字幕|歌词|曲|谱|贴图|模板|"
    # 实测再补：`Word` / `PPT` 已有但 `Word` 没有 —— 「读你的项目出一整套软著申请 Word」
    # 明明说了产出物却被点名。**词表不全是常态**，所以这条守卫是 WARN、件数不是 KPI。
    r"Word|Excel|pptx|docx|xlsx|EPUB|STL|STEP|SVG|PDF|vsdx|一整套|一套|"
    # 量词 + 名词：「三道菜」「一份清单」「两三套造型」「一张图」
    # 量词表里**不放「轮」「次」「遍」** —— 那是过程计数不是产出物。
    # 实测：加了「轮」之后，坏例子「**不许**说『有什么可以帮你』，先反问**三轮**的咖啡顾问」
    # 也过了 —— 一个修假阳性的补丁造出了假阴性。
    r"[一二三四五六七八九十两几]\s*(?:道|份|张|套|页|条|本|幅|篇|副|个)(?![质点])")
TITLE_BAN = re.compile(
    r"不许|不准|禁止|绝不|拒绝|只准|不肯|严禁|不给|不替|不写|不看|不认|不放|"
    r"不凭|不问|不算|不外包|不再|不让")


def check_title_shape(items: dict):
    live = [it for it in items.values() if not it.get("hide")]
    # **店主亲手标过的一律豁免。**
    # 这批是判据的来源，不是判据的对象 —— 机器不许再判一遍人已经判过的。
    # 实测这条豁免是必要的：`aryaminus-astro`「拒绝凭记忆报出一个行星位置的占星师」
    # 形状上确实是「只有禁令」，但店主标了它。**判据把基准判掉了，是判据不够，不是它错。**
    hearted = set((lib.read_json(os.path.join(lib.ROOT, "editorial", "hearts.json"), None)
                   or {}).get("ids") or [])
    bad, acked = [], []
    for it in sorted(live, key=lambda x: x.get("id", "")):
        if it.get("id") in hearted:
            continue
        t = it.get("title_zh") or ""
        # 「禁令即产物」豁免 —— 2026-08-21 补，rokokol/slop-stop 逼出来的。
        # 那件的标题是「它把题解了但不给你看，只一级级放提示」：以禁令开头，
        # 但**这件货的产物就是那个禁令** —— 一个宁可不给答案、只给阶梯提示的导师。
        # 「不给你看」在说你拿到什么，和「不联网、不外传、不替你写」不是一回事。
        #
        # 先例就在上面那段注释里：店主标过的 aryaminus-astro
        # 「拒绝凭记忆报出一个行星位置的占星师」形状上也是「只有禁令」。
        # **店主自己的基准里就有一件「禁令即产物」** —— 那是判据缺区分，不是货错。
        #
        # 豁免要付代价：**只打标记不写理由的仍然算命中。**
        # 不然这个字段就成了「消 WARN 开关」，而改文案迎合守卫和改守卫迎合文案
        # 是同一种病（见 docs/CURATION.md）。
        why = (it.get("title_ban_is_product") or "").strip()
        if TITLE_BAN.search(t) and not TITLE_OUT.search(t):
            if len(why) >= 10:
                acked.append((it.get("id"), t, why))
                continue
            bad.append((it.get("id"), t))
    print("\n【17】标题只有禁令、没说「你拿到手的是什么」")
    print(f"  在架 {len(live)} 件 · 店主已标（豁免）{len(hearted)} · "
          f"只有禁令没说产出物 {len(bad)} 件")
    for i, t in bad[:20]:
        print(f"  [没说产出物] {i} — {t}")
    if len(bad) > 20:
        print(f"  …另有 {len(bad)-20} 件")
    for i, t, why in acked:
        print(f"  [禁令即产物·已判过] {i} — {t}")
        print(f"        理由：{why}")
    print("  **这个件数不是 KPI。** 词表永远不全，把它当指标追会逼人往标题里塞关键词 ——")
    print("  要看的是那几条标题本身回答没回答「装了它你拿到手的是什么」。")
    return bad


# 入口必须留在文件的**真正**最末。见 main() 末尾那段自查 ——
# 光靠这句注释拦不住「在末尾追加新守卫」，所以那里加了静态检查。
if __name__ == "__main__":
    main()
