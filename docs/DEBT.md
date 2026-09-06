# 欠账台账 / Known debt

> 已经查证过、但**这一轮刻意没修**的东西。写在这里是为了不再"静默丢弃"——
> 只留在聊天记录里的发现，等于没发现。
> 每条必须写清：**是什么 · 怎么查证的 · 为什么现在不修 · 什么时候必须修**。

---

## 1. 7 件未上架商品的 `path` 记错

`python3 scouts/skill_scout.py --verify-paths` 扫全库单品时探到的。这 7 件
`hide: true`（不在架），所以线上看不见，但**它们的 `install.copy` 是错的**——
哪天要上架，先修 path 再说。

| id | repo | 现在的 path | 现象 |
|---|---|---|---|
| `costiash-eliviz-eliviz` | costiash/eliviz | `skills/eliviz` | raw 404 |
| `ctxrs-ctx-ctx-agent-history-search` | ctxrs/ctx | `plugins/ctx-agent-history-search/skills/ctx-agent-history-search` | raw 404 |
| `mariusyvard-nulltohero-audit` | MariusYvard/NullToHero | `skills/audit` | raw 404 |
| `mariusyvard-nulltohero-inspect` | MariusYvard/NullToHero | `skills/inspect` | raw 404 |
| `mariusyvard-nulltohero-siteasy` | MariusYvard/NullToHero | `skills/siteasy` | raw 404 |
| `vinta-hal-9000-best-practices` | vinta/hal-9000 | `skills/hal-skills/best-practices` | raw 404 |
| `vinta-hal-9000-bump-plugin-version` | vinta/hal-9000 | `.claude/skills/bump-plugin-version` | raw 404 |

**为什么不现在修**：不在架，改了没有用户可见的收益；而且探真实位置要一个个
clone 看目录树，成本不低于重新过一遍三问。
**什么时候必须修**：这 7 件里任何一件要上架之前。
**怎么复核**：`python3 scouts/skill_scout.py --verify-paths`（只报告，不改数据）。

---

## 2. `yusufkaraaslan-skill_seekers` 的形态要重新判

`skill_count` 印的是 26，其中 **24 件是 `tests/golden/phase2` 下的测试夹具**
（故意写坏 frontmatter 的那种），真货只有两件：`skills/skill-seekers` 和
`distribution/claude-plugin/skills/skill-builder`。

`find_skill_mds` 已加 `FIXTURE_DIRS` 排除，但**这只对以后新进的货生效**——
`restock_existing()` 只刷新 `stars` / `pushed_at` / `fun_score`，
**`skill_count` 和 `kind` 对存量商品永远不会重算**。所以这张卡不会自己变回单品，
要人去判：按现行规则（≥6 件才出合集卡）它够不上合集，得重新过一遍三问。

---

## 3. `skill_count` 已核过 16 件合集，其余仍是没核过的数

在架的 16 件合集，我逐个 `git clone --filter=blob:none --depth 1` 数过真实的 SKILL.md，
按「排除测试夹具 → 排除同名宿主副本」的口径订正了 11 件（`skills/*.json` 的 `skill_count`）：

| id | 原 | 现 |
|---|---|---|
| `nexu-io-open-design` | 531 | 372 |
| `arbiterforge-codearbiter` | 175 | 62 |
| `wanshuiyin-auto-claude-code-research-in-sleep` | 187 | 82 |
| `yusufkaraaslan-skill_seekers` | 26 | **2** |
| `jame581-godotprompter` | 65 | 57 |
| `dongbeixiaohuo-writing-agent` | 9 | **3** |
| `browser-act-skills` | 103 | 102 |
| `bitwize-music-studio-claude-ai-music-skills` | 53 | 52 |
| `heygen-com-hyperframes` | 16 | **26** |
| `nowork-studio-notfair` | 42 | **52** |
| `artokun-comfyui-mcp` | 37 | **39** |

**注意最后三行是往上改的**——原来的数不只是虚高，是**根本没核**，两个方向都错。

`check_curation.py` 现在报的「9 件 `skill_count` 大于 40」全都在这 16 件里，
数字本身已经核过了。剩下的是**选品问题不是数据问题**：一件合集印着 372 或 102，
按 `CURATION.md` 问二「大而全的数量堆」该不该收，要人来判。

**没核过的是单品那一侧**：`skill_count` 对单品表示「附带几个子技能」，
711 件里没有任何一件核过。目前没有任何前端出口用到它，所以不急。

## 4. 封面里那 24 件硬假阳性还挂在 `editorial/covers.json` 里

`covers.json` 把 97 件标成 `is_real_artwork: true`，逐张打开看过之后
24 件是 logo / 字标 / 二维码 / 徽章 / 空白坏图。
`editorial/curation.json` 里已经按逐张判定落地（`cover_kind` / `cover_real`），
**但 `covers.json` 自己的标注没改**——它是上一轮的产物，谁再读它还是会被误导。

### 「真产出物图有多少件」有两个数，别混用

同一个词量的是两件事，两边都要挂口径，否则大的那个会被后来人当成小的那个用：

| 数 | 量的是什么 | 怎么算 |
|---|---|---|
| **39** | `cover_kind == "artwork"` —— 逐张看过、判定为产出物的**全部**，**含因重复被撤图的** | `jq '[.items[]\|select(.cover_kind=="artwork")]\|length' editorial/curation.json` |
| **27** | `cover_real == true` 且 `cover` 非空 —— **真正能被读者看到的** | `python3 scouts/check_curation.py`【9】 |

差的那些是 `cover_dup_of`：图是真的，但同一张已经挂在另一件上，同屏印两次就是
`PRODUCT.md` 要杀的「重复封面」。

**39 是最容易被误用的那个数** —— 它听起来像「我们有 39 张产出物图」，
而读者实际看得到的是 27。**对外只报 27。**

逐张判定存档：见 `editorial/curation.json` 的 `cover_kind` 字段。

## 5. 判成「换」的 79 张封面，现在挂的是站方样张，其中几张作者仓里其实有更好的图

**是什么。** 2026-09-06 四个判官逐张看图（`docs/COVERS.md` 标准），157 张现有封面里
79 张判 `replace`。为了守住「每件都要有图」的底线，这 79 件当天全换成了站方样张
（`cover_kind: specimen`）。但判官的批注里有几件，作者仓里明明有对得上的产出物，只是
现在这张选错了或裁错了：

- `onlyfl-wow-gongwen-writing`：红头文件被 WPS 工具栏和字幕条包住，**裁出文件本体即可**
- `dacnay816y62-hub-chinese-poster-skill`：敦煌海报本身合格，只是右下角压着小红书账号水印，**去作者仓找无水印原图**
- `coleam00-excalidraw-diagram-skill`：我们自己跑的，线条太直、字太多，**手绘风 + 少字 + 横版重出一张**
- `zhlmi-moodboard-alignment`：我们自己截的方向稿页，**只截底部色板那段**
- `yokel1121-*-dark-fashion`：五张样张里只有一张是暗黑时装，**换成那一张**

**怎么查证的。** `editorial/curation.json` 里 `cover_verdict == "replace"` 的条目，
`cover_verdict_why` 是判官看到的东西；上面五条的批注原文在
`scouts` 那轮的 judge_out_*.json（scratchpad，已不在仓里）—— 关键结论抄在这儿了。

**为什么现在不修。** 这五件每件都是一次手工作业（裁图 / 翻仓 / 重跑），而当天的目标是
先让 314 件全部有一张不误导的图。样张不误导，只是不如产出物。

**什么时候必须修。** 下次碰这几件里任何一件的时候顺手修；或者攒够十件一起做。
修法：把作者产出物放进 `assets/covers/<id>.<ext>`，curation 里改 `cover / cover_kind
(artwork|hero) / cover_verdict=ok / cover_verdict_why`，然后 `python3 scouts/covers_publish.py`。

## 6. 做图类技能，站方样张不如「我们自己跑一遍截的产出物」

**是什么。** 在架 314 件里 `creative`（做图）占 132 件，其中几十件现在是能力图形样张。
这类技能的产出物本身就是图 —— 真装上跑一遍截出来（`cover_kind: ours`，图注「我们自己
装上、真跑了一遍」）是四档里唯一能背书的一档，也最能回答「它做出来长什么样」。

**怎么查证的。** `python3 scouts/make_specimens.py --replace --tally` 的分派表：
`photo_to_art` 25、`poster` 25、`video_cut` 31 —— 这三类几乎全是可以跑出图的。

**为什么现在不修。** 每件要装、要跑、要截、要判，是按件计的手工活；而且不少要
图像模型的 key。当天没有这个预算。

**什么时候必须修。** 每天上新一件的时候，新上架的做图类技能**直接**按 `ours` 出图，
不再走样张；存量的从店长推荐那几件开始，逐件替换。
