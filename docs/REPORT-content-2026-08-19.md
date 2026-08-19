# 内容 · 2026-08-19 交付报告

三件事全做完。**所有数字都是本地跑出来或逐张打开看过的，没有估算。**
查证方法统一是 `git clone --filter=blob:none --depth 1`（只拉目录树不拉文件内容，
不消耗 GitHub API 配额，也不是抽样）+ raw CDN 逐件取正文。

---

## 一、path 错误：任务书的分解是错的，实际是 28 件

任务书写的是「20 件 path 空 + 1 件仓库没了 = 21」。逐个 clone 探完，真实构成是：

| 类别 | 件数 | 处理 |
|---|---|---|
| 单品 `path` 真的记错 | **4** | 已修 `path` + `url` + `install` |
| 仓库已消失 | 1 | `ourword-ai/pixelpad` **404**，产品已下架 |
| `kind=collection` | 16 | `path=''` 对合集不是错；错的是 `install.copy`，见第三节 |
| **漏存档（path 是对的）** | **7** | 已补 |

那 7 件不在原清单里：`wolke-bazi-mingli`、`neallydare-svg-iching-divination`、
`panmax-hemingway-skill`、`yangcodingmaster-photo-distill`、`joeseesun-qiaomu-campus-resume`、
`kagurananaga-official-document-writing-skill`、`chenklein26-maker-fitness-coach-rpg`。
它们仓库根就有 `SKILL.md`，纯粹是当年抓来没存档。

**结果**：`methods/` 125 → **136**。id 一个都没改（id 是文件名也是 `/i/<id>` 的线上地址）。

**「补到 147」这个目标达不到，真实上限是 137/153。** 16 件合集没有「一份正文」可存 ——
全店至今 0 件合集有 `methods/` 存档，这个约定根本不存在，不是漏了。

### 新工具：`--verify-paths`

```bash
python3 scouts/skill_scout.py --verify-paths
```

在架 152 件：单品 136 件**全部**取得回正文。**只报告，不自动改写 path** ——
一个仓库几十个 `SKILL.md`，机器判不了哪个是这张卡指的那件；用户照抄一条
**看起来对**的命令装到错的东西，比装不上更难发现。

顺带扫全库 564 件单品，发现 7 件**未上架**的也有 path 错，已记进 `docs/DEBT.md`。

### `skill_scout.py` 改了两条 ingest 逻辑

**(a) `FIXTURE_DIRS`：测试夹具不再当商品数。**
`yusufkaraaslan/Skill_Seekers` 印的 26 件里 **24 件是 `tests/golden/phase2` 的测试夹具**
（故意写坏 frontmatter 的那种），真货只有 2 件 —— 按现行规则（≥6 才出合集卡）**它根本不该是合集卡**。

**(b) `save_method` 失败不再静默。** 过去取不回正文一行日志都没有，错的 `install.copy` 一路上架。

⚠️ **这两条只对以后新进的货生效。** `restock_existing()` 只刷新 `stars`/`pushed_at`/`fun_score`
（`skill_scout.py:441`），`skill_count` 和 `kind` 对存量商品**永远不重算**。

---

## 二、封面：真产出物图只有 39/97，不是 79

**154 张全下载、逐张打开看过**，不是抽验。

`covers.json` 标 `is_real_artwork: true` 的其实是 **97 件**（79 `readme_image` + 18 `existing`），
它自己的 `stats.real_artwork` 写 79，和逐件的 flag 对不上。

| 实判 | 件数 |
|---|---|
| **真产出物图** | **39** |
| 自制宣传头图（hero banner） | 22 |
| 机制/架构示意图 | 10 |
| 其他（输入素材、第三方书封） | 2 |
| **logo / 字标 / 二维码 / 徽章 / 头像** | **16** |
| **空白 / 占位 / 坏图** | **8** |

**真产出物图 39/97 = 40%。硬假阳性 24/97 = 25%。**
**HTTP 404 = 0/154，全部 200** —— `covers.json` 的 `verified` 站得住，问题不在图取不到，在取到了没人看。

### 最难看的几张（都还挂在货架上）

- `jnmetacode-superpowers-zh`、`joeseesun-qiaomu-learning` —— **二维码**
- `wanshuiyin-anti-autoresearch` —— **微信群二维码，图上自己印着「8月25日前有效」**
- `wanshuiyin-auto-claude-code-research-in-sleep` —— 250×55 的 **Huggingface Daily Paper 徽章**
- `heygen-com-hyperframes` ×4 —— **灰底一个播放三角**的视频占位图，四件共用
- `mvanhorn-last30days` 纯灰、`alchaincyf-nuwa-skill` 全空、`khendzel-skills-janitor` 只有一行 `~/.claude $`、`yusuke710-manim-skill` 近乎全黑
- `redfox-data`、`cecil`、`caveman`、`pixel2motion`、`dev-browser`、`clawrouter`、`HWS+` —— 纯字标

### `existing` 那 18 件是系统性错标，不是个别看走眼

`covers.json` 的 tier 表把 `repo_social_preview` 判 `is_real_artwork: **false**`，
却把 `existing` 整档判 `true` —— 而 18 件 `existing` 里 **11 件的图源正是
`repository-images.githubusercontent.com`，就是社交预览图**。同一种东西，两个结论。

更直接的：

- `adrianpunk-punk-skill-punk-cover` / `punk-avatar` 的图源是 **`opengraph.githubassets.com`**
  —— 字面意义上的 GitHub OG 卡片，被标成了真产出物图
- `hugohe3-ppt-master` 用 `gcdn.moonshot.cn` 的 **Kimi 赞助商 banner**
- `twostraws` 用 `hackingwithswift.com` 的站外 banner
- `alchaincyf-huashu-design` 用 **YouTube 缩略图**
- `bitwize-music` 用 weserv 代理的 `github.com/bitwize-music.png` **组织头像**
  （URL 里明写 `h=60&w=60&mask=circle`，一张 60px 头像放大当封面）

**根因**：`existing` 档等于假设旧数据是对的，**没有人打开看过**。

### 还有一个没人问但更要命的：重复封面

**36 件商品挤在 13 张图上。** 最狠的是 `worldwonderer-oh-story-claudecode` 的
**8 件共用同一张编辑器截图**；`heygen` 4 件、`vstack` 3 件、`novel-to-game` 3 件。

`PRODUCT.md` 第三节第 2 条要杀的就是「重复封面」。原样落地等于把渐变色块换成
**同一张截图印 8 次** —— 病没治，只换了张脸。

### 落地方式

**没有碰 `skills/*.json` 的 `cover`**，全部走 `editorial/curation.json`
（`apply_editorial` 对所有键 `update`，不只文本字段，所以零代码改动就进 feed；
`skill.schema.json` 没设 `additionalProperties: false`，加字段不违规）。

每件在架商品拿到三个字段：

```json
"cover": "<URL 或空>",
"cover_kind": "artwork | hero | diagram | other | og",
"cover_real": true
```

规则：`artwork` 留图并标 `cover_real: true`；`hero`/`diagram`/`other` 留图但
`cover_real: false`（作者真画的，比 OG 卡强，但不是产出物证据）；
**`logo`/`blank` 一律撤图**，`cover` 置空回退 OG 卡 —— 一张空白灰图比 OG 卡差，
留着就是 `PRODUCT.md` 说的「最差的选择」。

重复图：**同一张只留在 id 最短的那件上**，其余 23 件撤图并记 `cover_dup_of`，可追溯可翻回。

**前端契约（照着写，别自己推导）**

```js
if (it.cover) render(it.cover);          // cover 为空 = 回退 GitHub OG 卡
if (it.cover && it.cover_real) mark();   // 只有这一档是「真产出物图」
// cover_kind 描述的是候选图的性质；cover 为空但 cover_kind === "artwork"
// 表示「它本来有真图，因为和 cover_dup_of 那件重复才撤下」——不要据此渲染任何东西。
```

`cover_kind` 分布（在架 152）：`og` 79 · `artwork` 39 · `hero` 22 · `diagram` 10 · `other` 2。
实际有图 58 件，其中 `cover_real === true` 的 **27 件**。

**在架 152 件的实际分布**：有图 58 件（产出物 27 · 宣传图 21 · 示意图 8 · 其他 2），回退 OG 卡 94 件。

⚠️ **给 UX 的关键数**：真产出物图 39 张，其中 12 张是重复图，
**实际能撑起「产出物即封面」的只有 27 件 = 18%**。
「图现在是常态不是例外」这个前提，**按真产出物算不成立**；
按「有任何真图」算才成立（58/152 = 38%）。这个区别直接决定版式。

---

## 三、局限：152/152 全部写完

`check_curation.py` 现在 **0 件缺 `limit_zh`**。

20 条新写的每一条都引正文里能指出出处的具体事实。几个例子：

- `arbiterforge-codearbiter` —— 许可证是 **AGPL v3** 不是 MIT；167 份 `SKILL.md` 只对应
  62 个名字，`core/surface` 那 23 件是本体，`ca`/`ca-codex`/`ca-pi` 是同源生成的副本
- `dongbeixiaohuo-writing-agent` —— 9 份 `SKILL.md` 其实是**同样三件**放在
  `.claude`、`claude-runtime`、`plugins` 三处
- `jnmetacode-superpowers-zh` —— 20 件里 14 件是 `obra/superpowers` 的翻译；
  它自称覆盖 23 款工具，但 **v1.7.10 更新日志自己写着** Aider、Kiro、Hermes「此前装了等于没装」
- `zexuanw958-svg-travel-plan-viz` —— 地图引的是 **Leaflet CDN**，
  所谓「离线可读」保得住文字和时间轴，**地图那块断网就是空的**（正好戳中它自己的卖点）
- `lijigang-ljg-skills` —— 产出直接写进 `~/Documents/notes` 的 Org 文件，
  **文件头的 author 写死「李继刚」**，还要过 `org-lint` 和 Denote 校验
- `khendzel-skills-janitor` —— 它**会真动手删**，左滑就把 MCP server 从配置文件里移除

长度：中文 109–139 字（软上限 140），英文 ≤277（软上限 280）。

---

## 四、合集 install（产品已拍板）

16 件全改成 `clone` + `browse` + **空 `copy`**，`note` 用产品定的原话：

> clone 下来，挑你要的那件复制进 `~/.claude/skills/`。这是一个合集，没有「装它」这个动作。

`browse` 指真实技能目录：**11 件指得了**（`skills`、`plugins/travel-hacking-toolkit/skills`、
`.claude/skills`…），**5 件指不了就指仓库根** —— 它们的 skill 散在多个根目录下，凑一个出来就是编。

`skill_scout.py` 加了 `collection_install()` + `skills_root()`，以后新进的合集自动是这个形状。

**判断依据**（数据说的不是推想）：在架 136 件能装的单品，`install.dir` 指的目录
**无一例外直接含 `SKILL.md`**；合集给的 `mv <repo> …` 落地后那层没有，装了等于没装。
换成「把 `skills/` 底下全倒进去」更糟：`open-design` 372 件、`wanshuiyin` 82 件。

---

## 五、`skill_count` 订正 11 件

按「排除测试夹具 → 排除同名宿主副本」的口径，逐个 clone 数出来的：

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

**最后三行是往上改的** —— 原来的数不只是虚高，是**根本没核**，两个方向都错。

---

## 六、留在台账里的（`docs/DEBT.md`）

1. 7 件**未上架**商品的 `path` 记错 —— 不在架，上架前必须先修
2. `yusufkaraaslan-skill_seekers` 真货只有 2 件，**按现行规则不该是合集卡**，要重新过三问
3. `skill_count`：16 件合集已核过；单品那一侧 711 件一件没核（目前无前端出口，不急）
4. `editorial/covers.json` **自己的标注还是错的** —— 我在 curation 层落地了正确判定，
   但没改 covers.json，谁再读它还会被误导

## 七、一件要产品判的

`browser-act-skills` 的 CLI 自带 `solve-captcha`，会把验证码图片上传到官方接口；
目录里 103 件绝大多数是按站点写死的抓取件（1688、Airbnb、TikTok…）。
`CURATION.md` 红线里有「绕反爬」。skill 正文自己写了
「operational boundary = what the user can manually do in their browser…
never bypassing authentication or access controls」。
**这条边界在不在线内，是选品判断，我没有自己动它，写在这里等人判。**

---

## 动过的文件

| 文件 | 改了什么 |
|---|---|
| `skills/*.json`（4 件） | `path` / `url` / `install` 修正 |
| `skills/*.json`（16 件合集） | `install` 改成 clone + browse + 空 copy |
| `skills/*.json`（11 件合集） | `skill_count` 按实数订正 |
| `methods/*.md` | 新增 11 份存档（125 → 136） |
| `editorial/curation.json` | 20 条 `limit_zh`/`limit_en`；152 件的 `cover`/`cover_kind`/`cover_real`/`cover_dup_of` |
| `scouts/skill_scout.py` | `FIXTURE_DIRS`、`skills_root()`、`collection_install()`、`verify_paths()`、`save_method` 失败告警 |
| `docs/DEBT.md` | 新建 |
| `docs/REPORT-content-2026-08-19.md` | 本文件 |

**没动**：`index.html`、`design/`、`seo/`、`schema/`、`scouts/scout_lib.py`、
`editorial/covers.json`、`editorial/feedback.json`、`docs/PROTOCOL.md`、`docs/CURATION.md`。
**没有 `git commit`，没有 `push`。**
