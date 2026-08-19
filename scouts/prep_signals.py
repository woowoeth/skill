#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
备料徽章 / prep-work badge — 从 methods/ 已存档的 SKILL.md 正文本地算，零新增爬取。

# 为什么不用星数

`docs/CURATION.md` 自己写着「星数是滞后且有偏的指标，会亏待新发布、垂直、
非英语、无营销的好项目」。而 153 件上架货的星数是极端双峰
（0 星 13 件 / 1–99 星 13 件 / 100+ 星 128 件），根本不构成刻度 ——
把 `★ 0` 印在首屏上，是拿一个我们自己判定为有偏的指标去否定自己选出来的货。

替代信号是**「作者做到哪一步」**：正文里能不能看见他多做的那几步。
这不是质量分，是**可核对的事实** —— 每一条都能在正文里指出出处。

# 只有正向档 —— 这一条是硬约束，不是风格偏好

`prep_badge` 只有两个取值：`"ready"`（≥3 条证据）和 `""`（其余全部）。

一个只有一段提示词的极简 skill 可能恰恰是好东西。给它印「备料少」，
就是把星数犯过的错换个马甲再犯一次。所以：

**1–2 条证据、0 条证据、以及「根本没有存档」，三者在 feed 里的字节完全一致。**

第三种情况尤其要紧：`methods/` 现在只有 126 份存档，缺的那批正好是
`path` 字段记错、取不回 SKILL.md 的商品 —— 那是**我们自己的 bug**，
不是它们的问题。所以本模块不在商品级输出任何计数或「有没有存档」的标记：
不是靠约定不渲染，而是**前端拿不到可渲染的负面信息**。
诊断用的计数走 `prep_stats()`，只进 feed 头部的聚合统计，不进商品。

# 六条证据怎么认

| id | 认什么 | 怎么认 |
|---|---|---|
| `references` | 把知识拆进了外部参考文件 | 正文里出现 `references/` `refs/` 路径 |
| `scripts` | 附带可执行脚本 | `scripts/` 路径，或命令行里真的调本地脚本 |
| `assets` | 附带素材/模板/字体 | `assets/` `templates/` `fonts/` 路径 |
| `boundaries` | 明写自我约束 | **标题级**出现 不要/禁止/绝不/边界/误区/never… |
| `when_to_use` | 明写适用与触发条件 | 标题级，或 frontmatter description 里写了触发词/场景 |
| `evals` | 带评测 | `evals/` `eval.md` 评测集 |

结构类（references/scripts/assets/evals）认路径 —— 作者真的建了那个目录，
正文才会去引用它。散文类（boundaries/when_to_use）**只认标题级**：
「不要」两个字在任何一份操作手册的正文里都会出现几十次，那不是证据；
专门起一节讲「什么时候别用我」才是。
"""
from __future__ import annotations
import os, re, glob, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
METHODS_DIR = os.path.join(ROOT, "methods")

READY_AT = 3          # ≥3 条证据 = 「备料齐」。唯一的正向档。

# 中文标签给前端直接用（tooltip 列证据），英文给 llms.txt / SEO
SIGNAL_LABELS = {
    "references":  ("参考文件", "reference files"),
    "scripts":     ("可执行脚本", "runnable scripts"),
    "assets":      ("素材模板", "bundled assets"),
    "boundaries":  ("边界说明", "stated boundaries"),
    "when_to_use": ("适用条件", "when-to-use"),
    "evals":       ("自带评测", "evals"),
}
SIGNAL_ORDER = list(SIGNAL_LABELS)

# --- 结构类：认目录路径。作者真建了那个目录，正文才会引用它 ---
_PATH_PATS = {
    "references": re.compile(r"(?:^|[^\w/])(?:references?|refs)/", re.I),
    "assets":     re.compile(r"(?:^|[^\w/])(?:assets|templates?|fonts?)/", re.I),
    "evals":      re.compile(r"(?:^|[^\w/])evals?/|\bevals?\.md\b|评测集|评估集", re.I),
}
# scripts 单独一条：光提一个 .py 文件名不算（示例代码里到处都是），
# 要么有 scripts/ 目录，要么命令行里真的把本地脚本跑起来了。
_SCRIPTS_DIR = re.compile(r"(?:^|[^\w/])scripts?/", re.I)
_SCRIPTS_RUN = re.compile(r"\b(?:python3?|node|bash|sh|uv run|deno)\s+[\w./-]+\.(?:py|js|mjs|ts|sh)\b", re.I)

# --- 散文类：只认标题级 ---
_BOUNDARY = re.compile(
    r"边界|不做什么|不要|不得|禁止|严禁|绝不|禁忌|限制|约束|注意事项|误区|反面|失败|"
    r"red\s*line|do\s*not|don'?t|never|avoid|constraint|limitation|anti-?pattern", re.I)
_WHEN = re.compile(
    r"适用|不适用|何时|什么时候|使用场景|触发|适合|不适合|"
    r"when\s+to\s+use|when\s+not|use\s+cases?|applicability", re.I)
# frontmatter description 里明写触发词/触发场景，和专门起一节是同一件事
_WHEN_FM = re.compile(
    r"触发词|触发场景|触发条件|应触发|适用于|使用场景|"
    r"when\s+to\s+use|use\s+this\s+(?:skill\s+)?when", re.I)

_FM = re.compile(r"^﻿?\s*---\s*\n(.*?)\n---\s*\n?", re.S)
_HEADING = re.compile(r"^#{1,6}\s+")
_BOLD_LABEL = re.compile(r"^[-*]?\s*\*\*[^*]{2,40}\*\*\s*[:：]?\s*$")


def _frontmatter(text: str) -> str:
    m = _FM.match(text)
    return m.group(1) if m else ""


def _headings(text: str) -> str:
    """标题行 + 独占一行的加粗小标题 —— 作者用来分节的那些行。"""
    out = []
    for line in text.splitlines():
        s = line.strip()
        if _HEADING.match(s) or _BOLD_LABEL.match(s):
            out.append(s)
    return "\n".join(out)


def detect(text: str) -> list[str]:
    """一份 SKILL.md 正文 → 命中的证据 id，按固定顺序。"""
    heads = _headings(text)
    fmtext = _frontmatter(text)
    hits = set()
    for sig, pat in _PATH_PATS.items():
        if pat.search(text):
            hits.add(sig)
    if _SCRIPTS_DIR.search(text) or _SCRIPTS_RUN.search(text):
        hits.add("scripts")
    if _BOUNDARY.search(heads):
        hits.add("boundaries")
    if _WHEN.search(heads) or _WHEN_FM.search(fmtext):
        hits.add("when_to_use")
    return [s for s in SIGNAL_ORDER if s in hits]


def archive_path(item_id: str) -> str:
    return os.path.join(METHODS_DIR, f"{item_id}.md")


def load_all() -> dict[str, list[str]]:
    """methods/*.md → {item_id: [证据 id, ...]}。读不到就不在字典里 —— 空着是诚实。"""
    out: dict[str, list[str]] = {}
    for p in sorted(glob.glob(os.path.join(METHODS_DIR, "*.md"))):
        sid = os.path.basename(p)[:-3]
        try:
            with open(p, encoding="utf-8") as f:
                out[sid] = detect(f.read())
        except Exception as e:
            print(f"[prep] unreadable methods/{sid}.md: {e}")
    return out


def badge_for(evidence: list[str] | None) -> tuple[str, list[str]]:
    """证据 → (badge, 前端可显示的证据表)。

    这个函数是那条硬约束的落地点：不到档就返回 ("", []) ——
    「1–2 条」「0 条」「没有存档（evidence is None）」三种输入，输出完全一样，
    前端拿不到任何能渲染成负面的信息。
    """
    if evidence and len(evidence) >= READY_AT:
        return "ready", list(evidence)
    return "", []


def annotate(items: dict, evidence_map: dict[str, list[str]] | None = None) -> dict:
    """给每件商品挂 prep_badge / prep_evidence / prep_evidence_en。

    派生字段，构建时算，不落 skills/*.json：
      - 712 个文件一个都不用改，也不会和 editorial 层抢字段
      - 存档补齐（现 126 → path 修完应到 147）后重建一次就自动更新，没有第二份真相
    """
    ev = evidence_map if evidence_map is not None else load_all()
    for sid, it in items.items():
        badge, shown = badge_for(ev.get(sid))
        it["prep_badge"] = badge
        it["prep_evidence"] = [SIGNAL_LABELS[s][0] for s in shown]
        it["prep_evidence_en"] = [SIGNAL_LABELS[s][1] for s in shown]
    return items


def prep_stats(items: dict, evidence_map: dict[str, list[str]] | None = None) -> dict:
    """聚合统计 —— 只进 feed 头部，不进商品。

    `no_archive` 在这里是**我们自己的欠账指标**（path 记错取不回正文），
    不是商品的属性。它进 feed 是为了盯着它变小，不是为了显示。
    """
    ev = evidence_map if evidence_map is not None else load_all()
    shelved = [it for it in items.values() if not it.get("hide")]
    per_signal = {s: 0 for s in SIGNAL_ORDER}
    ready = no_archive = 0
    for it in shelved:
        e = ev.get(it["id"])
        if e is None:
            no_archive += 1
            continue
        for s in e:
            per_signal[s] += 1
        if len(e) >= READY_AT:
            ready += 1
    return {
        "shelved": len(shelved),
        "archived": len(shelved) - no_archive,
        "no_archive": no_archive,
        "ready": ready,
        "editor_read": sum(1 for it in shelved if (it.get("limit_zh") or "").strip()),
        "ready_at": READY_AT,
        "per_signal": per_signal,
    }


def _main() -> None:
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import scout_lib as lib
    items = lib.apply_editorial(lib.load_items())
    for it in items.values():
        lib.normalize_item(it)
    ev = load_all()
    st = prep_stats(items, ev)
    if "--json" in sys.argv:
        print(json.dumps(st, ensure_ascii=False, indent=1)); return
    print("备料徽章 · 实测（全部来自 methods/ 本地存档，无网络）")
    print(f"  上架 {st['shelved']} 件 · 有正文存档 {st['archived']} · 无存档 {st['no_archive']}（我们的 path 欠账）")
    print(f"  「备料齐」（≥{st['ready_at']} 条证据）{st['ready']} 件"
          f" —— 占有存档的 {100*st['ready']/max(st['archived'],1):.0f}%，占上架的 {100*st['ready']/max(st['shelved'],1):.0f}%")
    print(f"  副信号「店长读过」（limit_zh 非空）{st['editor_read']} 件")
    print("  逐条命中（分母 = 有存档的件数）：")
    for s in SIGNAL_ORDER:
        n = st["per_signal"][s]
        print(f"    {SIGNAL_LABELS[s][0]:6s} {n:3d}/{st['archived']}  {100*n/max(st['archived'],1):4.0f}%")
    dist: dict[int, int] = {}
    for it in items.values():
        if it.get("hide"):
            continue
        e = ev.get(it["id"])
        if e is not None:
            dist[len(e)] = dist.get(len(e), 0) + 1
    print("  证据条数分布：" + " · ".join(f"{k} 条 {dist[k]} 件" for k in sorted(dist)))


if __name__ == "__main__":
    _main()
