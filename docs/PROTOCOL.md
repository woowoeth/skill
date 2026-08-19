# 进货协议 / Restock Protocol

The repo is the database. One JSON per shelf item in `skills/`, aggregated into `skills/feed.json`.

## Item schema (informal)

| field | meaning |
|---|---|
| `id` | slug of repo (+skill dir). stable, filename = `<id>.json` |
| `kind` | `skill` 单品 / `collection` 合集 |
| `name` / `title_zh` | frontmatter name / 店长起的中文名 |
| `tagline_zh` / `tagline_en` | 货架一句话导购 |
| `why_zh` / `why_en` | 店长推荐理由（picks only） |
| `limit_zh` / `limit_en` | **诚实的局限**：机制上的短板、平台限制、适用边界。空串 = 还没写，`check_curation.py` 会点名。不是免责声明——「仅供参考」不算局限 |
| `desc_en` | SKILL.md frontmatter description（原文） |
| `repo` `path` `url` `homepage` | provenance |
| `stars` `pushed_at` | refreshed daily by restock。**`stars` 只供排序和门槛，不许有面向读者的出口** —— 见下面「备料徽章」 |
| `prep_badge` `prep_evidence` | 备料徽章。构建时从 `methods/` 正文算的**派生**字段，不落 `skills/*.json`，人不手写 |
| `category` | one of 8 shelves |
| `fun_score` | keyword + stars + freshness heuristic（排序用） |
| `pick` | ★ 店长推荐 |
| `hide` | 下架但保留记录 |
| `skill_count` | 合集里有几件 / 单品附带几个子技能 |
| `cover` | 封面图 URL：作者社交预览图 > README 首张真实截图 > 空（前端回退 GitHub 信息卡）。店长可在 editorial 置空否决 |
| `install` | `{clone, copy, dir, browse}` — 安装命令。**`copy` 单品必填、合集可空**，见下面「合集没有「装它」这个动作」 |
| `source` `added_at` | who stocked it, when |

## Ingest rules（防止倾倒）

1. `anthropics/skills` → 官方专柜：全部单独上架，不出合集卡。
2. 仓库根目录有 `SKILL.md` → 一件商品（单品卡，`skill_count` = 仓库内 SKILL.md 总数）。
3. 有一个子技能与仓库同名（flagship）→ 视为「一件商品带配件」，只上 flagship 单品卡。
4. 其余：≥6 个 skill 出一张合集卡；<26 个再抽 fun_score 最高的 ≤3 件当样品；≥26 个只上合集卡。
5. 名字为 template/example/sample 或 `-v数字` 结尾的跳过。
6. 新仓库准入线：≥40 星，非 fork，名字不含 awesome-/dotfiles/demo。
7. 每次进货最多 10 个新仓库 —— 小店每天上新几件，不是倒货车。

## Editorial layer

`editorial/curation.json` 的字段在每次 `feed.json` 重建时覆盖同 id 抓取项。
机器只补货，**不改店长写过的任何字**。下架 = `"hide": true`。

新增的人写字段一律加进 `scout_lib.EDITORIAL_TEXT_FIELDS`，`refresh()` 会用
`setdefault` 补齐缺的键——已经写过的值永远不会被空串盖掉，所以给 700 多个
存量文件加一个新字段不需要改任何一个文件。

编辑层现在有三个文件，各归一处，互不覆盖：

| 文件 | 谁写 | 进哪 | schema |
|---|---|---|---|
| `editorial/curation.json` | 店长 | `feed.json` 的每件商品 | `schema/skill.schema.json` |
| `editorial/headline.json` | 店长 | `feed.json` 的 `headline` / `headline_history` | `schema/headline.schema.json` |
| `editorial/rejected.json` | 内容 | `skills/rejected-feed.json` | `schema/rejected.schema.json` |

## 备料徽章 / Prep badge

`stars` 换成了「作者做到哪一步」。徽章从 `methods/` 已存档的 SKILL.md 正文本地算，
零新增爬取，实现和完整理由在 `scouts/prep_signals.py` 的模块头，标准侧在
`docs/CURATION.md` 第四节「加分项，不是门槛」。

**前端契约（照着这个写，别自己推导）**

```js
if (it.prep_badge === "ready") show("备料齐", it.prep_evidence);   // 例：["参考文件","可执行脚本","边界说明"]
// prep_badge === "" 时什么都不显示。没有第二档，没有负向档。
if ((it.limit_zh || "").trim()) show("店长读过");                   // 副信号
```

三条硬约束：

1. **只有正向档。** 一个只有一段提示词的极简 skill 可能恰恰是好东西，给它印「备料少」
   就是把星数的错误换个马甲再犯一次。
2. **不要去数证据条数。** 「1–2 条」「0 条」「根本没有正文存档」三种情况在 feed 里的
   `prep_badge` / `prep_evidence` **字节完全一致**（`""` + `[]`）—— 这是刻意设计的，
   不是巧合。前端拿不到可渲染的负面信息，所以不可能误渲染。
   逐件的证据条数只在 `scouts/prep_signals.py --json` 里，不进 feed 的商品。
3. **`stars` 不出现在任何面向读者的地方。** 它留在 feed 里只为排序和门槛。

feed 头部的 `prep_stats` 是聚合诊断：`archived` / `no_archive` / `ready` / `editor_read`。
`no_archive` 是**我们自己的存档欠账**（`path` 记错或抓来没存），盯着它变小用的，
不是商品的属性，**不要显示**。存档补齐后重建一次 feed 就自动更新，没有第二份真相。

## 合集没有「装它」这个动作

`install.copy` 是不是必填，**取决于 `kind`**：

| `kind` | `copy` | 校验 |
|---|---|---|
| `skill` | 必须有值 | 空 = **ERROR**。那是用户照抄的一行，空了这件商品就是装不上，等于没上架 |
| `collection` | **允许为空** | 空 = 正常。空时应给 `browse` |

合集为什么不能给 `mv <repo> ~/.claude/skills/<repo>`：

- 在架单品的 `install.dir` 无一例外**那一层直接含 `SKILL.md`**，agent 才认得出来。
  合集的 `mv <repo>` 落地后那一层**没有** `SKILL.md` —— **装了等于没装**。
- 一半合集的 skill 散在多个根目录（open-design 11 个根、codeArbiter 9 个），
  命令里那个「`skills` 目录」根本不存在。

所以合集只给 `clone` + `browse`，前端文案是定死的一句：

> clone 下来，挑你要的那件复制进 `~/.claude/skills/`。**这是一个合集，没有「装它」这个动作。**

`check_curation.py`【6】强制这条；还在给 `mv <repo>` 的合集会被逐件点名（WARN）。

## 流里给短的，详情给全的

瀑布流放不下完整的东西，所以每一个「给用户看的东西」都会分裂成两份：
流里那份短的，详情页那份全的。**这个分裂本身是全站最容易出诚实问题的地方**，
所以规矩统一成一条，字段和图片都照它办：

> **流里可以短、可以裁；全的那份必须真的在一次点击之外，且一刀不动。**
> 这两句是一对 —— 缺了后一句，前一句就是断章取义。

天下所有图片流都裁图，裁图不等于造假；**造假是「只有裁过的那份存在」**。
同理，`limit_brief_zh` 不是 `limit_zh` 的摘要或截断，它是同一件事的短说法，
而完整那条一个字不动地留在详情页。

两条推论，各有各的判法：

| | 「短的那份自身成立」是什么意思 | 谁判 |
|---|---|---|
| **文字**（`limit_brief_zh` / `limit_zh`） | 是完整句，不是从句子中间切开再补句号 | **脚本判得了** —— `check_curation.py`【8】 |
| **图片**（流里裁剪 / `cover` 原图） | 裁出来那块仍看得出是同类产出物 | 人逐张看；脚本只算「裁掉百分之几」，【9】 |

脚本能查的共同硬条件是**全的那份真的存在**：
只有 `limit_brief_zh` 而 `limit_zh` 是空的 = ERROR ——
卡片上那句短话代表着一条并不存在的完整局限，点进去是空的。

### 截断和夹行不是一回事

这一条是吵出来的，写下来免得下一个人再推错一遍（**我推错过**：我从这条规矩推出「图片可以裁，文字宁可不渲染」，
那是不同构的 —— 一张裁掉 50% 的图和一句夹掉 65% 的话处境完全一样）。

| | 长什么样 | 判 |
|---|---|---|
| **截断** | 砍在句子中间，**补一个句号装作说完了** | **禁止**，【8】查 |
| **夹行** | CSS `line-clamp`，**留省略号如实说「还没说完」** | 允许，和裁图同构 |

差别不在砍掉多少，在**有没有假装完整**。省略号是那句「点进去还有」的可见证据；
补上的句号是相反的东西 —— 它在说「就这些了」。在句读处切得干净只让这件事更难被发现，不是解决它。

**所以「字段还没铺满就整块不渲染」是错的选择**：那样卡片上一条诚实短处都没有，
比一条夹了行的诚实短处差得多。宁可夹行。

### 夹行安全的写法：坏消息放句首

夹行唯一真实的危险是**可见的那半读起来比整句更让人安心** ——
比如「不需要额外依赖」可见、「但要自备付费 key」被夹掉。

这个危险**脚本查不好**（夹在第几个字取决于列宽和字号，数据里看不见），所以它是写法约束不是校验项。
**2026-08-19 一次性实测**（在架 149 条 `limit_zh`）：夹到 30 字 0 件、48 字 1 件、60 字 0 件命中这个形状。
**这组数没有脚本可复算 —— 我刻意没给它加检查**（当时唯一的命中是误报，一个只产出误报的守卫就是噪音），
所以它是一次抽样，不是现状，别当成现在还成立。风险当时基本不存在，但那是运气，不是机制。机制是这条写法：

> **把最能劝退错的人的那一句放在最前面。** 前 30 字必须自己就构成劝退。

它和 D3 那条「留最能劝退错的人的那一条，不是最短的那一条」是同一个要求，
只是从「选哪条」推进到「那条怎么排」。照它写，夹在哪儿都不会反转意思。

**`artwork` 不因宽高比降级。** 画幅档是版式约束，不是准入过滤：
3:1 的横幅该被裁进框里，不是被拒收。画幅数值属于卡片渲染，**跟着版式走**
（D22：横向一律 2.0 · 竖向只给 `artwork` 放到 0.45 —— 横竖不对称，因为
竖裁掉的是海报的头和脚，横裁掉的是两侧空白）。

### 图片这边脚本该守的是哪一条

**不是「会不会被裁」。** 那是渲染事实：裁多少读者点一下就看到原图；
而且守卫拿前端的常量去量前端的常量，**定义上不可能失败** —— 那不是守卫。
所以【9】里「N 张需要裁剪」是**报告行**，不是待办；
只有一种情况报 WARN：**标着 `artwork`（我们声称是产出物证据）的图要裁掉 ≥30%** ——
证据被裁掉三成以上，该换图或该改 `cover_kind`。

**第一条是「声称是产出物的图，必须托在作者自己的仓库里」。** 零网络，`check_curation.py`【9】查。
这条比宽高对账**硬得多**：宽高只能发现「图被人动过」，域名能发现「**这图从来就不是他的**」。
真实教训：`hugohe3-ppt-master` 的 `cover` 曾是一张 `gcdn.moonshot.cn` 的 Kimi 赞助广告，
标着 `artwork` + `cover_real=true`，**宽高记得完全正确，所以宽高对账给它开了绿灯** ——
而详情页正在它下面印「作者仓库里的产出示例，这就是它做出来的东西」。
顺带这条也管隐私：第三方域名意味着每个访客的浏览器都要去 ping 一次那个第三方。

**另外：`cover_kind` 已经不是内部标记，是用户可见文案**（详情页图注由它决定）。
**动它要当改文案来动。** 为了消掉一条警报把 `artwork` 降成 `hero`，
是改了一句给读者看的话 —— 如果那张图既不是产出物也不是作者头图，改完仍然是假的。

**第二条是「`cover` 里必须是原图，不是预裁版」。** 这条跟版式常量无关，怎么调都成立，
而且它是「详情页给原比例、一刀不裁」唯一可能被悄悄破掉的方式 ——
URL 没变、`cover_w`/`cover_h` 没变，只有字节变了，**从数据上看不出来**。

`scouts/verify_covers.py` 查它：拉封面头 64KB，解出真实宽高，和 `cover_w`/`cover_h` 对账。
单独一个脚本、不塞进 `check_curation.py`，因为它要联网 ——
把网络请求塞进本地体检会让体检变慢又变脆，CI 里一超时就红一次，
最后大家开始忽略它，那比没有守卫更糟。

实测（`python3 scouts/verify_covers.py`，随时可复算）：上站封面 55 张 ——
**一致 55 · 不一致 0 · 量不出 0 · 拉不到 0**，含 4 张 SVG 按 `viewBox` 量。

## 印在货架上的数字

星数、evals、`skill_count` 已经是同一个病的三次发作：**印给用户看的数字没有核过来源。**
`skill_count` 现在的口径是「仓库里 `SKILL.md` 的总数」，把测试夹具和示例全算进来了 ——
`Skill_Seekers` 卡片上印 26 件，其中 24 件是 `tests/golden/phase2` 里故意写坏的测试夹具
（**内容 2026-08-19 clone 后逐个看出来的；本机核不了，要 clone 仓库** ——
所以这个数不挂脚本名，挂的是谁量的、怎么量的）。
**在卡片上印含测试夹具的数量，正好踩自己「问二·大而全的数量堆」那条拒收线。**

**先分清哪种数字。** 这条规矩只管**会变的数**（实测量：几件、几张、百分之几），
不管**不会变的数**（阈值和常量：140 字上限、≥3 条证据、裁掉 ≥30%）——
阈值是规矩本身的一部分，给它挂复算命令是噪音。判据很简单：
**明天再跑一次会不会变？会变就挂命令；不会变就是阈值。**
没有脚本可挂的实测（比如一次性抽样），**挂日期和量的人** —— 带日期的实测不冒充现状。

规矩（完整版在 `editorial/feedback.json` 的 `patterns`）：**任何要给用户看的会变的数字，
三条同时满足才准印 —— ①能重跑（脚本名写在数字旁边）②能对账（脚本列得出明细：
这 26 件是哪 26 件）③明细有人真看过一眼。** 数字本身不可审，明细才可审；
一个口径错的脚本照样跑得很顺。`check_curation.py`【7】把 `skill_count` 大于 40 的逐件点名。

## 头条 / Headline

`editorial/headline.json` 是一个 append-only 数组，每条 `{date, id, story_zh}`。
机器**只读不写**。构建时取 `date <= 今天` 里最新且商品仍在架的一条当当日头条
（`feed.headline`，内联整件商品，首页零查找），其余全进 `feed.headline_history`
（最新在前，归档页直接用）。`date` 可以写未来——到那天自动上位，可以提前排期。
只存 id 不存文案副本：商品文案改了头条跟着改，没有第二份真相。

## 拒收榜 / Rejection ledger

`skills/rejected-feed.json` 独立于 `feed.json`：feed 每次开页都要拉，拒收榜是第二个
页面；两者作者和更新节奏不同；而且拒收列表会无限增长，货架**刻意**不会。
`feed.json` 里只带一个 `rejected_summary`，够首页印那三个数字，不用发第二个请求。

两个来源汇进去：
- `editorial/rejected.json` —— 人写的，每条挂 `reject_rule`（问一/问二/问三/红线/门槛）
- `scouts/scan_log.json` —— 机器扫描留痕，每轮扫了多少、收了多少、拒了哪些

**数字不许估算。** 没插桩的量输出 `null`，不输出猜的数。`rounds[].source` 标明
这一轮的数字是 `scout-instrumented`（scout 进程自己记的）还是 `scout-log-parse`
（从 scout 的 stdout 回收的，`complete: false`）。

`unshelved_trail` 是抓来了但没上架/已下架的留痕（`hide: true` 的那些），
它们在 `skills/*.json` 里一直都在，只是过去从不出现在任何 feed 里。

### 机器拒收怎么留痕

`skill_scout.discover()` 里被 `SKIP_REPO_PAT` 和 `_admit()` 刷掉的仓库，过去是
`continue` 直接丢掉的，一行痕迹都没有。`scout_lib` 现在提供留痕口：

```python
lib.note_scanned()                                    # 每看到一条搜索结果
lib.note_admitted(full)                               # 放行
lib.record_reject(full, "命名黑名单：awesome-", "门槛", stars=...)   # 拒收
lib.flush_round()                                     # 一轮结束，落盘
```

在接上之前，workflow 走的是弱一档的回收路径：`python scouts/scout_lib.py
--from-log <scout 的 stdout>`，从 scout 自己打印的 `[scout] discover: …` 行里
取真实数字。它只拿得到「过了门槛的候选数 / 试过几个 / 上架几件」，
拿不到「一共扫了多少」和逐条理由，所以那两项就是 `null`。

## Conflict-safe commits

Per-item files commit first（文件名唯一，rebase 永不冲突）；`feed.json` 永远从合并后的全量重建再推送，失败则 reset → 重建 → 重试（同 ourword-ai/idea 的成熟套路）。
