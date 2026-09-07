# 交接 · 2026-09-07 封面这一摊（humanworld-b0 → 接手的会话）

店主 15:35 定：品味仓交给另一个会话，我这边不再写这个仓。下面是**我做完的**、**没做完的**、
和**一段被冲掉需要重写的代码**。已推的都在 `4aa3289cb` 及之前。

## 一、做完了（已推，不用重做）

1. **红线命中 13 处逐行读过** —— 判决在 `editorial/scan_review.json`（原文 + 理由 + 判于）。
   **12 处是误报，而且是同一个形状：触发扫描那一行，正是这件 skill 在说「我不干这个」。**
   例：「不绕过 DRM、付费墙、地区限制」命中「绕反爬」；极验拦住就「交接给用户完成滑块验证」
   命中「绕反爬」；劝退重签名微信「实实在在地降低你机器的安全等级」命中「改厂商程序」；
   内容风险检测器自己的关键词表「盗版、侵权…」命中「取盗版」；base64 图片串凑出的子串命中「剂量」。
   真命中 1 处：`jakeyhb/football-content-ops-skill` 的抖音发布脚本用
   `--disable-blink-features=AutomationControlled`，反检测是它唯一用途 → 拒收榜（红线·绕反爬），
   `editor_picks` 里一并撤掉了。
   放行按 `release_clean.py` 的规矩**两层都写**（`skills/*.json` 的 hide 和 `curation.json`）——
   只改一层不生效，那是 09-02 栽过两次的坑。
2. **5 张 GitHub 预览卡外链**清掉转样张（底线 4：封面一律本地）。
3. **11 张配错图形的样张重出并签字** ——「出成片」配成字幕、「调车内喇叭」配成图表、
   「竞赛全流程」配成印章、「蒸馏成专家」配成剪视频。**错的图形比中性图形更糟，它在误导。**
4. **34 张真图逐张打开看过**（agent 开图 + 我复核），判决已落 `curation.json`：
   **ok 12 · replace 21 · remove 1**。清单在 `editorial/cover_verdicts_2026-09-07.json`。
5. **remove 那 1 件按底线 3 整件下架**：`Zeejay0/gathered-scenes-zine-skill` 的
   `scenes-gathered-zine-live-flow-v1-0`，封面是作者自己仓 `assets/brand/` 下的
   「专注 GPT 代充/成品号」微博广告截图。店主拍板「下架 + 留痕」，痕在
   `picks_pinned.json` 的 `_底线3下架`：**店主说一句就能加回来**；同仓另一件
   `scene-distillation-zine-v1-3` 不受影响，仍在架。

## 二、没做完的两件

### A. 70% 的封面和别人字节完全相同 ← 最要紧

量出来的（`git show 4aa3289cb` 之后的货架）：**在架 359 件里 253 件（70%）的封面和别人字节相同。**
最大几组：`document` ×31、`video_cut` ×19、`poster` ×17、`photo_to_art` ×15、`game` ×14、`chat` ×14。

**根子**：09-06 那个决定的必然后果。店主说「生成的图不要和标题描述重复」，于是改成 29 个无字
能力图形；但 227 张样张分到 29 个图形里，平均一个图形背 8 件货，**而图形是确定性画的，
同一个图形就是同一张图**。

**这也是我自己的一次误报**：09-06 我报「没图 0、每张封面都判过 ok」，字面为真，
却漏了「其中大量是同一张脸」——**量了「有没有图」，没量「这些图彼此一样不一样」。**
账本第 23、29 条那个老毛病：代理指标当结果。

**店主 09-07 拍板：先只修 ≥10 件的那几组（10 组、153 件），小组先留着。**

**做法（我写过、被并发 rebase 冲掉了，照抄即可）**：给 `scouts/make_specimens.py` 加 `--pair`
—— 主图形说「它干什么」，右下角一个小图形说「在哪个场子里」（按货的 `category` 定），
再按 id 微偏主图形的位置。**不要加随机装饰**：那是噪声，等于放弃「图形要说它干的事」。
三条硬规则不变：不要圆角、不要阴影、不要渐变（缩放会连描边一起缩，不另设线宽）。

```python
# 紧跟现有 TPL 之后加：
TPL2 = """<!doctype html><meta charset="utf-8">
<style>html,body{margin:0;width:%(w)dpx;height:%(h)dpx;background:%(paper)s;overflow:hidden}
svg{position:absolute;left:0;top:0;width:%(w)dpx;height:%(h)dpx}</style>
<svg viewBox="-600 -400 1200 800" xmlns="http://www.w3.org/2000/svg">
  <rect x="-600" y="-400" width="1200" height="800" fill="%(paper)s"/>
  <g transform="translate(%(dx)d,%(dy)d) scale(1.00)">%(motif)s</g>
  <g transform="translate(%(sx)d,%(sy)d) scale(0.26)">%(second)s</g>
</svg>"""

SECOND = {   # 类别 → 第二个图形（说这件货在哪个场子里）
    "creative": "poster", "work": "document", "life": "calendar", "fun": "game",
    "meta": "code", "writing": "font", "docs": "book_to_blocks", "learn": "whiteboard",
    "body": "fitness", "dev": "code",
}

PAIR = False        # 放在 def render_all 之前

# render_all 里，把 pg.set_content(TPL % …) 换成：
            if PAIR:
                import hashlib as _h
                sec = SECOND.get((it.get("category") or "").strip(), "make")
                if sec == m:                       # 主次撞了就退回中性，别画两遍同一个东西
                    sec = "make" if m != "make" else "document"
                seed = int(_h.md5(it["id"].encode()).hexdigest()[:8], 16)
                dx, dy = (seed % 25) - 12, (seed // 25 % 21) - 10
                pg.set_content(TPL2 % dict(w=W, h=H, paper=PAPER, motif=MOTIFS[m],
                                           second=MOTIFS[sec], dx=dx, dy=dy - 26,
                                           sx=430, sy=300))
            else:
                pg.set_content(TPL % dict(w=W, h=H, paper=PAPER, motif=MOTIFS[m]))

# main() 里 ci = "--ci" in argv 之后加：
    global PAIR
    PAIR = "--pair" in argv
```

**⚠️ 我这一版有个已知不足，你接手时要先解决它，否则等于白跑**：那 10 个大组里，
**同组的货往往连 `category` 也一样**（31 件 `document` 全是 `writing`），于是第二个图形也相同，
只剩 ±12px 的偏位 —— 那不叫「不一样」，那叫「同一张图挪了个位置」。
我用它跑了 153 件，结果只出了 15 张不同的图（其实那次是代码被冲掉、老模板在跑，
但即使代码在，按这个逻辑也好不了多少）。

**建议的解法**（按代价从低到高，任选或叠加）：
1. **先把主图形分散开**：31 件 `document` 里真正是「出文档」的其实不多 —— 逐条读标题重派，
   `translate`（改写成另一种语体）、`resume`、`slides`、`whiteboard`、`seal`、`research` 都能分走一批。
   这一步最值：它同时修了「撞脸」和「图形不准」。
2. 第二个图形不要只看 `category`，改看**它的产出物或题材**（从 `title_zh` 判），能拉开得多。
3. 真要靠构图变化，就变得**够多**：主图形的元素个数 / 疏密 / accent 落在哪个子元素，
   而不是整体挪位。**判据是「两张摆在一起，人会不会说这是同一张」——只能看图判。**

改完必跑 `python3 scouts/covers_publish.py`（`refresh` → 派生图，顺序不能反），
然后 `python3 scouts/shelf_health.py` + `python3 scouts/check_curation.py`，红着的不许推。

### B. 判「换」的 21 张还没换图

清单和理由在 `editorial/cover_verdicts_2026-09-07.json`（`verdict: replace`）。两类占多数：

- **7 张是 GitHub 仓库 README 的社交卡截图** —— `docs/COVERS.md` 明说不接受（那不是产出物，是仓库名片）
- **4 张是作者的招牌图 / 吉祥物 / 文字 logo** —— 好看，但遮住标题猜不出它干什么

处置顺序按 `docs/COVERS.md` 的四档：先 `repo_covers` 找作者的真产出图 → 没有就
「我们自己装上跑一遍」截产出物（`cover_kind: ours`，四档里最强的一档，见 `docs/DEBT.md` 第 6 条）
→ 都不行才落样张，且图形要配准。

## 三、两个坑，别再踩

1. **两个会话不能同时动同一个仓。** 我 15:2x 写进 `make_specimens.py` 的 `--pair` 代码，
   被另一个会话 15:32 的 `git_sync` rebase 冲掉了，磁盘和 git 里都没有 —— 上面那段是从我
   自己的上下文里抄回来的。动手前先 `git log -1`，看有没有别人刚提交。
2. **`scouts/git_sync.sh` 在 UTF-8 locale 下会因为提交信息里的中文括号报
   `MSG（: unbound variable`** ——`"$MSG（rebase 后重生成生成物）"` 那一行，bash 把
   `（` 当成变量名的一部分了。`export LC_ALL=en_US.UTF-8` 之后必现，不设 locale 就正常。
   **这是脚本的 bug，值得单独修一次**（把 `$MSG` 写成 `${MSG}`）。

## 四、还欠着的两笔（不在这一摊里，但别忘）

- 扫货那条流水线的 `agents` 片 **30 小时没接上班**，`shelf_health` 一直红着这一条。CI 排班问题。
- 阅读队列还剩 1,644 件。按 09-07 过堂的命中率（判官 ≥80 与 70–79 都是 12–15%，
  店主名单 38%），**建议不再读队列尾巴**，只读店主名单和 T1 作者发的新仓 —— 见 `docs/TASTE-PASS.md`。
