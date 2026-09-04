---
name: web-ppt
description: 制作现代、带精美动效的网页版 PPT（Web PPT）：Vue 3 + Vite 前端、Go go:embed 静态服务器，构建为单个可离线双击运行的 exe。三种风格 × 45 套主题——风格 A「电子杂志 × 电子墨水」（衬线大标题 + WebGL 流体背景）、风格 B「瑞士国际主义」（无衬线极致字号对比 + 点阵网格 + 22 版式锁）、风格 C「主题工坊」（token 化多主题系统，完全消费主题的圆角/阴影/渐变/display 字体）。动效库：27 个 CSS 入场动画 + 26 种 Motion recipes + 20 个 Canvas FX 持续动效（知识图谱/星域/粒子/烟花…）。内置 Chart.js 图表、highlight.js 代码高亮、ESC 总览宫格。键盘：方向键翻页。
when_to_use: >
  用户要做任何演示类内容时使用——网页PPT、Web PPT、网页幻灯片、演示网页、翻页演示、
  幻灯片网站、演讲稿伴演示；或把已有 PPT/大纲/文档内容做成"比 PowerPoint 动效更强"、
  "离线单文件演示程序（exe）"的网页版演示。
  风格线索词同样命中：杂志风、瑞士风/Swiss Style、小红书图文风、赛博风、极简风、日式风、
  新闻播报风、路演/汇报/教学/技术分享等讲演场景。用户没提关键词但内容显然是演示讲稿时，
  优先考虑本 skill（普通 Word/PDF 文档诉求不归本 skill）。
---

# Web PPT（Vue + Go 网页幻灯片）

制作横向翻页的网页版 PPT。前端 Vue 3 + Vite，后端 Go `go:embed` 静态服务器，交付**单个离线可执行文件**：双击 → 本地服务（127.0.0.1 随机端口）→ 自动打开浏览器。演示设备无需任何运行时。全部字体经 @fontsource 打包内嵌、动效引擎与图表库经 npm 打包——离线即全保真。

## 架构：三层 CSS × 三种风格

```
tokens.css            统一 token 底座（颜色/字体/间距/缓动/动画）+ 运行时 chrome（deck 条带/导航/总览）
  └ themes/*.css      45 套主题（[data-theme] 作用域，纯 token 覆盖，构建期全量打包；换主题 = 改 style.js 的 THEME 后重建）
      └ 风格层        magazine.css（A）/ swiss.css（B）/ studio.css（C）——同一份 token，三种消费方式
```

**关键概念**：主题定义"值"（颜色/字体/圆角/阴影），风格定义"怎么用"（A 强制衬线大标题不吃圆角阴影、B 强制无衬线直角不吃渐变、C 全盘接受）。所以任何主题可用于任何风格，效果各不相同但都协调。

## 三种风格（一份 deck 只能选一种，不可混用）

| | 风格 A · 电子杂志 | 风格 B · 瑞士国际主义 | 风格 C · 主题工坊 |
|---|---|---|---|
| 气质 | Monocle 杂志感、叙事、人文 | Helvetica Forever、信息驱动、数据 | 百变：随主题从极简白到赛博霓虹 |
| 字体 | 衬线标题（Noto Serif SC / Playfair）+ 等宽元数据 | 全程无衬线（Inter / Noto Sans SC），字号越大字重越轻（200） | display 字体由主题决定（Archivo Black / Oswald / Space Grotesk / Playfair…） |
| 背景 | WebGL 双背景：暗页全息色散 / 亮页银色涡流 | canvas 模式默认；可开 WebGL 极细网格 | 无 WebGL；氛围用 Canvas FX（gradient-blob/constellation…） |
| 主题 | 45 套任选（themes-all.md） | 45 套任选（主题只换 accent 与灰阶倾向，纸底不变） | 45 套任选（圆角/阴影/渐变/字体全部生效） |
| 布局 | 10 种（layouts.md） | 22 种锁定版式 S01-S22（swiss-layout-lock.md + layouts-swiss.md） | 31 种（layouts-studio.md） |
| 动效 | 5 种 recipe + 27 CSS 动画 + 20 FX | 21 种 recipe + 27 CSS 动画 + 20 FX | 27 CSS 动画 + 20 FX（无 recipes，CSS 通道即全部） |
| 独有 | pipeline 分步推进页 | 版式锁 + 数据可视化版式（bar-tower/measure-up） | 图表页（ChartBox）/ 代码页（CodeBlock）最佳载体 |

**选型**：叙事/观点/人文/行业观察 → A；数据/产品/方法论/技术汇报 → B；用户点名某种视觉风格（小红书风/赛博风/日式极简/新闻播报…）或想频繁换装 → C。用户没说就按内容定并告知你的选择。

## 共享能力（三风格都有）

- **动效库 73 种**（27 CSS 入场 + 26 Motion recipes + 20 Canvas FX）——**默认配方克制使用**（见工作流 §3 配方表），目录与写法只在加料时查 `animations.md`；FX 用法 `<CanvasFx name="…" />`，进页启动离页销毁，颜色随主题
- **ChartBox**（Chart.js）+ **CodeBlock**（highlight.js）：components-charts.md 按需查
- **`H`/`?` 帮助浮层**（成品不常驻快捷键）/ `ESC` 总览 / `?slide=N` 直达
- 数字滚动：`<span class="counter" data-to="1248">0</span>` 进页自动 0→目标

## 工作流程

### 0. 需求访谈（先于一切 · 问清为止 · 问答式收敛）

不要拿到需求就开写。以问答方式**逐维度摸清需求——不限轮数，一次只问一个问题，问清为止**；所有关键维度都清晰（或用户明确交由你定）后，输出**蓝图卡**请用户确认，确认后才动手。完整维度清单、话术与反模式见 `references/requirements-guide.md`。

**对话纪律（违反即败笔）**：
1. 一次只问一个问题、一问一收——保持对话感，不抛问卷；追问围绕真实信息缺口展开
2. 给选项永远 ≤3 个，且用"视觉选项卡"结构（模板见 §0 末尾）呈现——每个选项=中文气质名＋一行色卡＋气质词＋适合场景＋与另两项的差异；**禁止**只丢 slug/预设编号（P07/aurora 最多括号备注）、禁止术语（风格 A/B/C、token、预设包）问用户
3. 用户明确说「你定/随便」的**维度** → 对该维度落定并一句话告知理由，不再追问它；但**内容理解不允许 defer**——素材必须读完、结构必须理清，这是访谈的一部分；「你定」只豁免被点名维度，不代表全盘跳过
4. 不为问而问：某维度已清晰就推进下一维度；同维度不重复追问同一件事
5. 蓝图卡是开工闸门：确认后才动手；确认后若发现重大理解偏差 → 回到访谈修正，不硬写
6. **提问下限（防"问太少"）**：动手前至少问清 4 个核心缺口——①内容要点与结构 ②观众与场合（基调）③时长与页数（节奏）④视觉倾向（含配色好恶，是"求稳"还是"想抓眼球"）。某项信息素材/需求已自带才算清晰；不得因"内容看着好懂"就不问。全部清晰（或用户一次讲清）后，仍要在蓝图卡里把四项复述一遍让用户确认
7. **无交互执行**：当前会话用户无法回复（无人值守/自动执行/明确说"直接做"）时，不做无效提问——按内容推断 + 快速决策表一次性落定全部维度，并在开工同一回复里列出"替你定的 N 项＋理由＋想改随时可改"，交付时再次提示：想换主题/风格只需改 style.js 一处后重出，1 分钟可完成

**访谈维度（按序覆盖，全部清晰即可开工，轮数不限）**：
1. **内容本体**：先通读素材/大纲；问清核心信息、章节划分与每章要点（不理解内容不开工）
2. **场合与观众** → 基调（内部汇报/技术分享/路演/教学/图文/叙事/庆典——映射表见 guide）
3. **内容气质** → 定风格：数据论证→B、叙事人文→A、教学拆解→C、宣言冲击→C 大胆主题
4. **时长与页数** → 节奏（5-10 分钟 8-12 页 / 15 分钟 ≈10-12 / 30 分钟 18-22 / 60 分钟 25-40）
5. **视觉意象** → 给 3 个有名字有理由的候选（意象词表见 guide）
6. **素材与配图**：有无图片/数据/logo；无素材则声明用图形化表达
7. **交付形态**：交付 exe / 网页 / 图文竖版（3:4）——不需要逐字稿/口播稿（该功能已移除，页面不写 notes）

**快速决策表**（只用于视觉落定，且仅在**用户明确授权你定风格/主题**时使用；内容结构/观众/时长等维度不在此表，仍按访谈问清。任何落定都给"告知句"，用户随时可反悔改选）：
| 场景线索 | 默认落定（求稳） | 想惊艳时改给（同纪律更出挑） | 告知句式（示例） |
|---|---|---|---|
| 技术/开发者内容 | P07 极光科技 | P08 东京夜话 | 「技术内容按极光科技这组清爽偏深风格做；想要更夜店就换东京夜话——改 style.js 一处重出即可」 |
| 汇报/商务/投资人 | P04 克莱因蓝 | P05 安全橙 | 「商务汇报用瑞士国际主义，数据最有说服力；想更醒目选安全橙，纪律不变」 |
| 叙事/观点/人文 | P01 墨水经典 | P09 小红书图文风 | 「这个内容适合杂志叙事的质感」 |
| 教学/新手向/内容杂 | P11 学术论文 | P12 赛博终端 | 「教学场景选清晰耐看的风格」 |
| 完全没线索 | P01 墨水经典 | 大胆系三选一选项卡 | 「默认走墨水经典——通用不易出错；想抓眼球的话，我从霓虹/孟菲斯/赛博里给你三个选项卡挑」 |

**「稳 or 惊艳」是必问的视觉倾向**：用户给不出意象时至少问这一句，别直接上安全牌（这是"配色墨守"最常见的来源）。

**蓝图卡（动手前必给用户）**：
```
📋 蓝图卡 · 确认后开工
- 预设包：P07 极光科技（风格 C × aurora）
- 页数/节奏：14 页 · 3 章 · 呼吸页在第 4/9 页
- 每页形态：封面/目录/章1×4/呼吸/章2×5/总结/致谢
- 动效基调：fade 系 + 数字滚动；FX 全 deck 1 个（封面）
- 配图：无素材，图形化表达
- 换装：定稿后可 1 分钟换主题重出 exe
```
用户点头 → 进入下方正式工作流；用户改某行 → 只改对应行再确认一次；若确认后发现重大理解偏差 → 回到访谈修正维度，再更新蓝图卡，不硬写。

**视觉选项卡模板**（风格/主题/意象候选一律用此结构给用户，禁止平铺名字或只丢编号）：
```
候选 1 · 极光之夜（预设包 P07 极光科技）
  色卡  深空蓝紫底 × 电光青 accent，玻璃感微光
  气质  清爽偏深、科技感    适合  技术分享/产品发布
  差异  三者中最沉稳清晰；候选 2 更霓虹、候选 3 更温暖
✅ 推荐（理由：内容偏技术演示，深底高对比投影更清楚）
```
每项候选必须真实存在（themes-all.md / 预设包）或明确标注"需融合派生新调"（流程见 themes-all.md 顶部）；给 3 个就要横向对比着给，并始终标出推荐项与理由。

### 1. 搭脚手架
复制本 skill 的 `assets/scaffold/` 到目标目录，`npm install`（网络不畅加 `--registry=https://registry.npmmirror.com`）。

### 2. 选风格 + 主题（改 3 处，值取自蓝图卡）
1. `src/style.js` 的 `STYLE`（magazine/swiss/studio）+ `THEME`（预设包主主题）——主题即定稿，不满意 = 改 THEME 一行重建（1 分钟）
2. `src/main.js` 的风格样式导入（三选一；tokens/animations/themes 已统一导入不要动）
3. `src/slides/index.js` 的示例页导入
4. `index.html` 背景色防白闪（跟随所选主题主底色）与 `<title>`

### 3. 写页面（核心）
1. **先读对应 layouts 文档**：A → `layouts.md`；B → `swiss-layout-lock.md`（版式锁，必读）+ `layouts-swiss.md`；C → `layouts-studio.md`
2. 布局骨架是纯 HTML：粘进 `SlideXxx.vue` 的 `<template>`，改文案即可；**不要发明模板外的类名**，自定义用 `style="..."` 内联
3. 动效：**先按下方默认配方表配，再按"加料规则"决定是否升级**；写法速查（data-anim / data-animate / CanvasFx / counter）见 animations.md
4. 图片放 `public/images/`（命名 `{页号}-{语义}.{ext}`），骨架里 `src="images/01-cover.jpg"`
5. `npm run dev` 实时预览
6. **主题节奏**：A 必做（每页 `light`/`dark`/`hero light`/`hero dark` 之一，连续 3 页同明暗不允许，每 3-4 页一个 hero）；B 每页写 `data-layout="Sxx"`；C 每 4-6 页插一个 `.slide.inverse` 反色节奏页。生成后 grep 自检

**默认动效配方（先克制，后加料）**：73 种效果是目录不是自助餐。下表是每种内容页的默认配置——默认只做这些，不要自行加戏：

| 页面形态 | 默认配方 | 加料规则（仅内容需要强调时才升级，全 deck ≤2 处） |
|---|---|---|
| 封面/章节呼吸页 | kicker fade-down + 标题 rise-in + 副标 fade-up | 可加 1 个氛围 FX（opacity ≤ .6） |
| 目录/卡片网格 | 容器 stagger-list | 不升级 |
| 正文要点/双栏 | fade-up（自动 stagger） | directional（A）/ duo-mirror（B）作对照页 |
| KPI/统计 | counter 数字滚动 + fade-up | counter-explosion FX 仅"破纪录"页 |
| 图表页 | 图表自带 900ms 动画 + fade-up | 不升级（图表自身即动效） |
| 代码/终端页 | fade-up（代码块整体） | typewriter-multi FX 仅启动日志场景 |
| 表格/清单 | fade-up | 不升级 |
| 引语页 | A：quote recipe 逐行；B/C：fade-up | 不升级 |
| 致谢页 | zoom-pop + 可选 confetti-cannon（B/C） | — |

**三禁令**：一页入场动画"族类" >2 = 乱；一页 FX >1 = 乱；普通数据页上 glitch/3D/爆炸 = 华而不实。
（族类口径：方向性淡入 fade-up/fade-left/fade-right/fade-down 算**同一族**——双栏对照模板"标题 fade-up + 左卡 fade-left + 右卡 fade-right"是合规默认，不叠加计数；rise/drop/zoom/blur/glitch/typewriter/parallax 等各算一族。）

### 4. 构建交付
```
npm run build
go build -ldflags "-s -w" -o 演示名称.exe .
```
细节与交叉编译见 `references/golang-server.md`。

### 5. 验证（交付前必做）
双击 exe 逐页检查，并完整走一遍：
- `← → ↑ ↓ / Space / PgUp PgDn` 翻页、`Home/End` 首末页
- **翻页手感**：新页从空白滑入、落定后内容按动画显现——全程无"先完整闪现再全体闪没重入"；**往返翻页（回访已看过的页）同样无闪现**；快速连翻（连续按 → / 快速滚轮）不丢页、动画不叠播乱播
- `ESC` 总览宫格（点缩略图跳页）
- pipeline 页（A）按 `→` 分步推进
- FX 页进出多次无卡顿（canvas 已销毁）；图表页数据正确
- 无控制台报错、文字不溢出、图片不压分页组件

无界面环境：`./xxx.exe -no-browser -addr 127.0.0.1:18080` + `curl` 探活（期望 200）。

## 风格 B 硬规则（违反即失去瑞士感）

1. 全程无衬线；一份 deck 只有一个 accent 色，不许多色高亮
2. 直角纯色：禁止渐变/阴影/圆角（rule 横线除外）；hairline 分割用 1px
3. 极致字号对比：主标题与正文 ≥ 8:1；大字字重 200（越大越细），小字 500-600（越小越粗）
4. 中文大标题先分档（≤8 字 6.4vw 档位表见 layouts-swiss.md），不要直接套英文 hero 字号
5. 正文页只能用登记过的 S01-S22 版式，每页写 `data-layout="Sxx"`；不发明新结构
6. 卡片三类 token 互斥（card-fill/card-ink/card-accent），多卡并列统一样式，最多一张 accent 突出
7. 演示最小字号：正文 ≥18px、卡片描述 ≥16px、meta ≥14px；放不下就删文案/拆页/换版式
8. 图标用 Lucide 棱角风格，不手画 SVG 圆点；装饰点阵/矩阵严格在 grid 内
9. Windows 雅黑无 200 字重，`is-win` 类会自动补偿 300——不要手动写死 font-weight:200 内联

## 风格 A 硬规则（违反即失去杂志感）

1. 大标题必须衬线（h-hero/h-xl 走 --serif-zh）；正文非衬线；元数据等宽
2. 不用阴影、不用浮动卡片；层级靠字号 + 字体对比 + 网格留白
3. WebGL 背景只在 hero 页透出（遮罩已预设），普通页几乎看不见
4. 图片只用标准比例（16:10/4:3/3:2/1:1/16:9），网格图用 `h-22/h-26` 固定高度，禁 `align-self:end`
5. 中文大标题 ≤ 5 字且 nowrap；chrome（栏目标签，跨页稳定）与 kicker（本页钩子，每页不同）不要写同一句话
6. 用 Lucide，不用 emoji

## 风格 C 硬规则（违反即失去主题工坊的意义）

1. 颜色/圆角/阴影/渐变**只走 token**（`var(--accent)` 等），禁止内联写死 hex——主题由 `style.js` 的 `THEME` 统一定，内联色会脱离主题换装体系
2. 一页一个主容器层级：`.deck-header`（页眉）+ 主内容 + `.deck-footer`（页脚/页码），chrome 跨页稳定
3. 深色节奏页用 `.slide.inverse`，不要自己内联黑底；inverse 页上卡片自动适配
4. 卡片三变体（`card`/`card-soft`/`card-outline`）+ `card-accent` 点睛，一页卡片区最多一种主变体 + 一张 accent
5. FX 一页最多 1 个；氛围类（gradient-blob 等）配 `opacity:.4-.6` 垫底，主视觉类（knowledge-graph 等）给 ≥40vh
6. 图表页标题先给结论，图表是证据；饼图 ≤6 块、雷达 ≤8 轴 ≤3 序列（components-charts.md 图表纪律）
7. display 字体是主题的个性——不要在页面里覆盖 font-family，换气质应该换主题

## 技术红线

- `go:embed` 是**编译期**嵌入：每次改完前端必须 `npm run build` + `go build`，旧 exe 不热更新（调试期可 `go run . -dir dist`）
- 三套风格 CSS 类名冲突（.h-hero 等同名不同义），**严禁同时导入**两个风格 CSS
- npm 依赖白名单：`vue / motion / lucide / chart.js / highlight.js / @fontsource-*`（已备齐）；不要引入 vue-router/pinia/UI 库/其他图表库
- 主题文件只覆盖 token（+ 少量主题特有装饰规则）；改主题文件后 `themes/index.css` 与 `themes/catalog.js` 必须同步登记
- 瑞士风 canvas-mode（默认）下没有 WebGL；要去掉 `style.js` 里 `canvasMode: true` 才启用网格背景
- 交付物 exe 未签名，Windows SmartScreen 首次运行会提示——提前告知用户"更多信息→仍要运行"

## 何时读哪个参考文件

**主流程必读**（按顺序，其余按需）

| 文件 | 何时读 |
|---|---|
| `references/requirements-guide.md` | §0 需求访谈时**必读**（4 问脚本/决策矩阵/话术/反模式/蓝图卡模板） |
| `references/style-presets.md` | 访谈收敛到预设包时读对应一组（12 组验证组合 + 避坑） |
| `references/layouts.md` | 风格 A 写每页前**必读** |
| `references/swiss-layout-lock.md` → `layouts-swiss.md` | 风格 B 写每页前**必读** |
| `references/layouts-studio.md` | 风格 C 写每页前**必读**（31 布局骨架） |
| `references/checklist.md` | 交付前逐项自检（P0 级必须全过） |
| `references/golang-server.md` | 构建与交付阶段 |

**按需查阅**（用到再读，不预读）

| 文件 | 何时读 |
|---|---|
| `references/animations.md` | 动效配方表要"加料"时查具体写法（27 CSS + 26 recipes + 20 FX） |
| `references/components-charts.md` | 用 ChartBox / CodeBlock / CanvasFx 时 |
| `references/components.md` | 风格 A/B 组件细节（callout/stat/pipeline 等） |
| `references/themes-all.md` | 用户明确要自由组合主题时（45 套目录；默认场景不必读） |
| `references/content-strategy.md` | 用户有大纲策略诉求（路演结构/文案公式/情绪弧）或要做 10+ 页大 deck 时 |
| `references/style-authoring.md` | 新增主题/风格时（skill 维护向，日常不用读） |

## 交付物

1. `演示名称.exe`——拷到任意设备双击即演
2. 操作说明（页面内不常驻显示，按 `H` 或 `?` 呼出帮助浮层）：
   `→`/`←`、`↑`/`↓`、`空格`/`PgUp`/`PgDn` 翻页，`Home`/`End` 首末页，`ESC` 总览；URL 加 `?slide=N` 直达第 N 页
3. （可选）源码目录
