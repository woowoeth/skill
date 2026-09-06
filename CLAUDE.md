# 品味（ourword.ai/skill）— 给在这个仓库里干活的每一个 agent

这是一家**精选** AI skills 的店，卖的是判断，不是数量。先读三份标准，再动手：

| 你要做的事 | 先读 | 一句话 |
|---|---|---|
| 决定收不收一件 skill | `docs/CURATION.md` | 三问都过才收；**可留可不留的，一律不留** |
| 给一件 skill 配图 / 判一张图 | `docs/COVERS.md` | 遮住标题，看图能不能猜出它干什么；**每件在架的都必须有图** |
| 改数据、改字段、改流程 | `docs/PROTOCOL.md` | 字段是契约；`cover_kind` 是用户可见文案，改它等于改一句话 |
| 想知道哪些坑已经踩过 | `docs/DECISIONS-2026-09-06.md` `docs/DECISIONS-2026-08-19.md` `docs/DEBT.md` | 店主拍板的原话和理由都在，别再问一遍 |

## 五条不许破的底线（2026-09-06 店主定）

1. **在架的每一件都要有图。** 取不到作者的产出物图，就用站方样张（`python3 scouts/make_specimens.py`）；连这都做不到的下架。没图不是「糙」，是「坏」。
2. **图必须有人打开看过。** 判决写在 `editorial/curation.json` 的 `cover_verdict`（`ok` / `replace` / `remove`）。字段齐不等于图对 —— 二维码、赞助广告、作者头像、雪豹照片，从数据上一个都看不出来。**不要用像素统计代替看图**，试过，作废。进货是自动的、看图是人做的：新到货 48 小时内没判记「糙」，过了才「坏」；CI 自动配的样张（`--ci`）verdict 留空，**巡货时逐件看图签字**。
3. **封面上有二维码或广告的，整件下架**（`remove`），不是换图。图在告诉你这个技能是什么。
4. **封面一律本地文件**（`assets/covers/`），不许外链。外链会死，也让每个访客去 ping 第三方。
5. **改了封面之后跑 `python3 scouts/covers_publish.py`**，不要单跑 `make_thumbs.py` —— 派生图必须按**重建后**的 feed 出，顺序反了线上就是几百个 404 加一排灰框。

体检：`python3 scouts/shelf_health.py`（站在访客的位置看）· `python3 scouts/check_curation.py`（数据自洽）· `python3 scouts/check_tw.py`（繁体站）。**红着的不许推。**

## 站方样张（`cover_kind: specimen`）的规矩

- **图上一个字都没有。** 卡片底下已经印着标题和描述，图里再写一遍等于同一句话说两遍（店主原话）。
- 用能力图形说话：视频剪成帧、书拆成块、照片变贴纸。29 个图形在 `scouts/make_specimens.py` 的 `MOTIFS`，按它**干的事**分派；拿不准用 `make`（中性）。**一个错的图形比中性图形更糟，它在误导。**
- 不要圆角、不要阴影、不要渐变，一套只许一个 accent（`#8b3d2f`）。
- 样张不算「真图」，进不了店长推荐。图注由 `index.html` 的 `capSpecimen` 和 `scouts/write_shelf_pages.py` 的 `CAPS` 负责，写明「站方样张，不是产出物截图」。
- 只要取得到作者的产出物图，就不该用样张。做图类技能优先「我们自己装上跑一遍」（`cover_kind: ours`）。

## 店主的信号高于一切判据

- `editorial/hearts.json` 里的是店主亲手标过心的；`editorial/picks_pinned.json` 是他钉住的精选。**任何机器判据或复审把它们判掉，是判据错，不是它们错** —— 恢复上架，理由留作备注（`cull_note`）。唯一例外：封面是二维码/广告（那是底线 3），下架但要在 `picks_pinned.json` 留痕说明。
- 店主看一眼说「不行」的东西，不要解释为什么它其实可以。他是第一个用户。

## 提交

用 `bash scouts/git_sync.sh "<message>"`：先提交源，rebase 时生成物取一侧、`editorial/*.json` 按条目三方合并，rebase 完从源重生成再推。`i/` `tw/` `skills/feed.json` `sitemap.xml` `llms*.txt` 全是生成物，不要手改。**rebase 合进上游改动之后要重跑 `scouts/tw.py`**，否则 `check_tw` 的 hreflang 对不上。
