#!/usr/bin/env python3
"""选品自问自答 —— 把用户访谈那五问搬到「我们怎么选货」上，**答案自己算，不写死**。

## 为什么做成脚本而不是文档

任务书里那句「上架 153 件」在文档里躺了一天，每个新同事进来读到的都是它。
**一份数字会过期的文档，比没有文档更糟。** 所以这五问的答案由脚本现算。

## 五问从哪来

来自一套用户访谈框架。它最锋利的一条是：

> **请用户共享屏幕，看他实际怎么用，而不是让他描述。**
> 针对具体模块问，不要问「整体怎么样」——「整体」这种问法会得到「挺好的」这种废话。

搬到选品上，逐条对应：

| 访谈那一问 | 搬到选品上 | 我们的可量指标 |
|---|---|---|
| ① 让他共享屏幕，别听他描述 | **真跑一遍，别读它的自我介绍** | `cover_kind=='ours'` 的件数 |
| ② 之前用什么工具？哪里不够好 | **在这件之前，读者拿什么凑** | 点评里说出替代方案的件数 |
| ③ 不问「整体怎么样」 | **点评必须具体到能引用** | 点评里出现赞美形容词的件数 |
| ④ 最希望下个版本加什么 | **货架上哪一格整片是空的** | 已实测为空的场景 |
| ⑤ 付费意愿必须直接问 | **要 5 美元一次，你还装吗** | 人判，脚本只给分母 |

第 ⑤ 问那条「先问满意的、再问不满意的，最后才问钱」的顺序也搬过来了：
本脚本的输出顺序就是这个顺序 —— **先摆做到的，再摆没做到的，最后问值不值。**

用法：`python3 scouts/selection_interview.py`（纯本地，零网络）
"""
from __future__ import annotations
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED = os.path.join(ROOT, "skills", "feed.json")

# ---- ③ 的判据。词表是**手读 12 条之后**改出来的，不是想出来的 ----------------
#
# 第一版判据是「有没有数字/引号/硬规则」，跑出来「83 件一条具体信号都没有」。
# 手读那 83 件的前 12 条，发现判据本身错了：
#   「它的密度规矩：底部留白等于浪费学生的考试资源，能塞就塞满」—— 具体，被漏判
#   「权威性拉满」「研究得很透」「痛点被它按住了」—— 空泛，没被抓到
# **指标和肉眼读不一致时，肉眼赢。** 下面这张词表就是那次手读的产物。
VAGUE = re.compile(
    r"拉满|很透|研究得透|按住了|聪明一档|强一档|出品[。，]|痛点被|真能|挺好|不错|优秀|"
    r"专业|强大|全面|丰富|完善|实用|好用|贴心|用心|细致|靠谱|高质量|值得一试|体验好|"
    r"做得好|讲得细|到位|扎实|水平高|够硬|能打")
# 「XX 出品」单独算一档：它是拿作者的名气当理由，而不是说出这件东西做了什么。
BY_NAME = re.compile(r"[一-龥A-Za-z]{2,8}出品")
# ② 有没有说出「在这件之前拿什么凑」
ALT = re.compile(r"比|别处|同类|而不是|不是拿|换掉|替代|原来|以前|通常|大多|一般人|多数|别的")


def _in_quotes(text: str, i: int) -> bool:
    """命中点是不是落在引号里。"""
    for m in re.finditer(r"[「『\"“][^」』\"”]{1,40}[」』\"”]", text):
        if m.start() < i < m.end():
            return True
    return False


def _vague_hit(w: str):
    """空泛词命中，但**引号里的不算** —— 那是引文，不是夸奖。

    实测三处假阳性，而且三处都是这件 skill **明令禁止**的说法被引来当例子：
      「可以说『不错』『这周挺稳』，不许说『你完成得真棒』」
      「『经得住反例』…比『高质量』这类词实在得多」
    把引文算成夸奖，等于把「它不许说废话」判成「我们在说废话」——正好判反。
    同一个修法在 check_curation 的【13】里已经用过（引号里的中文不算漏翻）。
    """
    for m in VAGUE.finditer(w):
        if not _in_quotes(w, m.start()):
            return m
    return None


def main() -> None:
    feed = json.load(open(FEED, encoding="utf-8"))
    live = feed["skills"]
    n = len(live)
    ran = [x for x in live if x.get("cover_kind") == "ours"]
    art = [x for x in live if x.get("cover_real")]
    archived = len(glob.glob(os.path.join(ROOT, "methods", "*.md")))
    vague = [x for x in live if _vague_hit(x.get("why_zh") or "")]
    byname = [x for x in live if BY_NAME.search(x.get("why_zh") or "")
              and not _in_quotes(x.get("why_zh") or "",
                                 BY_NAME.search(x.get("why_zh") or "").start())]
    alt = [x for x in live
           if ALT.search((x.get("why_zh") or "") + (x.get("tagline_zh") or ""))]
    brief = [x for x in live if (x.get("limit_brief_zh") or "").strip()]

    def pct(k): return f"{100*k/n:.0f}%" if n else "—"

    print(f"选品自问自答 · 在架 {n} 件 · 生成于 {feed.get('generated_at','?')[:16]}")
    print("顺序照访谈那条规矩：**先问满意的，再问不满意的，最后才问钱。**")

    print("\n" + "="*66)
    print("先摆做到的")
    print("="*66)
    print(f"  局限写齐          {feed.get('with_limit',0)}/{n}  ({pct(feed.get('with_limit',0))})")
    print(f"  读过正文（存档）  {archived} 份")
    print(f"  拒收理由写下来    {feed.get('rejected_summary',{}).get('rejected_documented',0)} 条")
    print(f"  说出了替代方案    {len(alt)}/{n}  ({pct(len(alt))})   ← ② 「之前你拿什么凑」")

    print("\n" + "="*66)
    print("再摆没做到的")
    print("="*66)
    print(f"\n① **真跑过，还是只读过？**（访谈那条「让他共享屏幕，别听他描述」）")
    print(f"   我们自己装上真跑出来的封面 `ours`：**{len(ran)} 件**  ({pct(len(ran))})")
    print(f"   作者仓库里的产出物样张 `artwork`：{len(art)} 件")
    print(f"   → 正文存档 {archived} 份只证明**读过**。读过 ≠ 跑过。")
    print(f"   → 这是我们唯一抄不走的东西（没有目录站真装真跑），也是现在分数最低的一项。")

    print(f"\n③ **点评里有多少句是「挺好的」？**")
    print(f"   出现赞美形容词：**{len(vague)} 件**  ({pct(len(vague))})")
    print(f"   其中拿作者名气当理由（「XX 出品」）：{len(byname)} 件")
    if vague:
        print("   逐条列出（这一栏必须能逐条列出，不然就是又一句「整体挺好」）：")
        for x in vague:
            hit = _vague_hit(x["why_zh"]).group(0)
            print(f"     [{hit}] {x['id'][:44]:<44} {x['why_zh'][:46]}")

    print(f"\n③b **卡片上那行短版局限**：{len(brief)}/{n}  ({pct(len(brief))})")
    print(f"   自查法：把短版单独读一遍 —— **如果它读起来比完整那句更「安全」，就是写错了。**")

    print(f"\n④ **哪一格整片是空的**（逐片扫过之后的实测，不是感觉）")
    for s in ("收纳 / 搬家 / 家务（100 命中，真阳性 0）",
              "理财 / 记账 / 买房租房（147 命中，真阳性 0）",
              "追剧 / 看书 / 播客 / 音乐消费（43 命中，真阳性 0）",
              "汽车 / 驾驶 / 通勤（18 命中，真阳性 0）",
              "婚礼 / 白事 / 份子钱（搜到 0 个仓）"):
        print(f"     · {s}")
    print("   → 两条教训：**关键词命中数和真阳性数几乎无关**（命中最多的两片，"
          "一片是数百件同轴、一片真阳性为零）；**候选池对某些场景是瞎的**"
          "（穿搭 17 个命中全是误命中，换 `/search/repositories` 一搜就有 26 个仓）。")

    print("\n" + "="*66)
    print("最后才问钱")
    print("="*66)
    print(f"""
⑤ **「要 5 美元一次，你还装吗」** —— 这一问脚本答不了，只给分母：在架 {n} 件。

   为什么要直接问：读者装一件 skill 的成本不是钱，是**信任 + 装机 + 一次失望**。
   而我们收的每一件都在花掉这三样里的第三样。所以选品时对自己直接问：

     · **这件如果要 5 美元一次，我自己会不会掏？** 掏，才配上架。
     · **它替读者省掉的是什么？** 说不出省掉的具体动作，就是没想清楚。
     · **它失败的时候，读者付出的是什么？** 说不出代价，`limit_zh` 就没写完。

   这一问放在最后，理由和访谈里一样：**先把满意的和不满意的都摆出来，
   答案才不会是恭维。** 前面四问都答完之后再问这一句，会刷掉不少「看着不错」的东西。
""")
    print("="*66)
    print("这份东西自己也要接受第 ③ 问：**上面每一栏都能逐条点名，没有一栏是「整体挺好」。**")


if __name__ == "__main__":
    main()
