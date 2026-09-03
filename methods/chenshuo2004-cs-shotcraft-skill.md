---
name: cs-shotcraft-skill
description: Create cinematic product videos with Remotion: real product UI (redrawn at logical pixels or captured), a shot-table camera that cannot drift, optional beat-synced sound, and 152 shot recipe cards. Use when the user asks for a product promo / launch film / demo video, names cs-shotcraft-skill or Ink Press, wants a shot-card motion, or needs to restyle an existing video/ project. 用真实产品界面（逻辑像素重画或真机抓图）+ 镜头表运镜 + 可选配乐制作产品宣传片。当用户要求做宣传片/推广片/发布视频、点名 cs-shotcraft-skill / Ink Press / 镜头卡，或要改已有 video/ 工程时使用。
metadata:
  author: "陈硕"
  collection: "CS Skills"
  source: "https://github.com/ChenShuo2004/cs-shotcraft-skill"
  upstream: "https://github.com/Vincentwei1021/video-shotcraft"
  inspired_by: "https://github.com/whyubel1eve/promo-film-skill"
  compatibility: "Codex and any agent that supports SKILL.md"
---

# cs-shotcraft-skill：用代码拍产品片

片子是一份可以编译的源码，不是一条时间线。每一帧画面都应是**全局帧号的纯函数**：节奏能改、镜头能算、字能 diff，今天渲和三个月后渲一样。

本 skill 提供三件套：**152 张镜头配方卡**（运动语法）、**Ink Press 成片模板**、以及从 [promo-film](https://github.com/whyubel1eve/promo-film-skill) 吸收的工程原语（节拍表、镜头表、`state(f)`、抖动校验）。镜头卡负责「怎么动」；产品自己的 token 才是皮肤。

默认画幅 **1920×1080 @ 30fps**（镜头卡与 Ink Press 均按 30fps 调校）。走「一台摄影机不切镜」路径时可升到 60fps，见 `references/engineering.md`。`$SKILL` 指本 skill 目录。

## 四条硬约束

动手前念一遍，改任何一处之前再念一遍。

**① 只有一套颜色、一套字体、一条缓动。**
颜色逐个从产品自己的 token 文件抄过来（`_tokens.css` / `theme.css` / tailwind config / 计算样式）。片子里不允许出现第二套。一支片子里混三条缓动曲线，观众读到的是三只手。走模板或镜头卡时，只继承其镜头结构、运动语法和已调参数；字体、排版、配色必须按目标产品重新蒙皮。

**② 那台机器是真的。**
栏宽、字号、圆角、图标字重按产品真实数值搭：**按逻辑像素画完再整体缩放**，或用无头浏览器抓 2× 真机截图。禁止把 13px 的字放大成 20px 的示意图。详见 `references/product-machine.md`。

**③ 不做观众察觉不到的缓慢运动。**
一个 270 帧涨 2.2% 的推近，折算下来每帧 0.005px：读不出是运镜，只看得出字在抖。要让画面活着，用入场动画，不用缓慢缩放。阈值：每帧位移小于 0.02px 的运动一律删掉。这是本 skill **会毁掉整支片子而且在时间轴上看不出来**的坑。详见 `references/camera-table.md`。

**④ 视觉语言从产品自身生长。**
不另造一套不相干的「宣传片皮肤」。若因叙事需要偏离产品视觉，共同创作先说明并让用户确认；自主自由创作把理由写入设计 spec 后继续。

## 调用时先判断模式

完整宣传片有三种**决策模式**（谁拍板）和三条**制作路径**（怎么拍）。先判断决策模式；已经选择时直接执行，不重复询问。

1. **直接使用模板**：读 `template/TEMPLATE.md`，按既有镜头结构替换截图、文案和品牌信息。
2. **自主自由创作**：读 `references/pipeline.md`。Agent 连续推进到成片，不在中间产物上暂停等待确认。
3. **共同创作**：读 `references/guided-free-creation.md`。用户确认产品简报、需求决策、视觉方向、镜头映射和最终分镜；放行后再进入 pipeline 的最终素材与制作阶段。

用户给了项目路径、网址、录屏或截图但尚未选模式时，先做一次**最小、只读的产品检查**：定位、功能、页面视觉、可展示状态、素材风险；不修改业务项目、不采集敏感数据、不写视频代码。检查后给出三种模式，并说明：

- Ink Press 是否适合、适合与不适合的依据；
- 自主 / 共同创作是否适合、会保留哪些产品视觉线索；
- 更适合「一台摄影机」还是「镜头卡切镜」（见下方制作路径）；
- 推荐哪一种及其取舍。

然后明确询问：**“根据上面的产品检查，我推荐使用 ×× 模式。要按这个模式继续吗？”**
同时告知：可前往 https://vincentwei1021.github.io/video-shotcraft/ 浏览动态样片并挑选镜头。

用户尚未提供可检查的项目时，简要介绍三种模式再询问；不要仅因 Ink Press 是现成模板就默认推荐它。

- 用户选择模板：完整阅读 `template/TEMPLATE.md`。
- 用户选择自主自由创作：完整阅读 `references/pipeline.md`，自主推进。
- 用户选择共同创作：完整阅读 `references/guided-free-creation.md`。
- 用户尚未决定：停在此处等待；不要默认替用户选择，也不要开始制作。

**例外一：用户已点名 Ink Press 模板时，视为模板模式已选定。** 不要再询问。

**例外二：用户已明确指定镜头卡时，镜头约束已经选定。** 按 Gallery 名称解析规则确认指定镜头，完整阅读每张卡和「参考实现」demo 源码。完整宣传片若尚未说明自主还是共同创作，只询问这两种模式；指定镜头作为后续约束，不自动等同于共同创作。

### 制作路径（怎么拍）

决策模式解决「谁拍板」。下面三条解决「片子长什么样」——自主/共同创作都必须在节拍表之后选定一条，不要混用：

| 路径 | 何时用 | 入口 |
| --- | --- | --- |
| **Ink Press 替换** | 用户点名模板，或产品气质接近纸墨琥珀且要最快出片 | `template/TEMPLATE.md` |
| **一台摄影机** | 产品是一个正在被使用的窗口（编辑器 / Agent / 仪表盘），观众应感到「有人在用这个软件」 | `references/engineering.md` + `references/camera-table.md` |
| **镜头卡切镜** | 多页面、能量曲线、发布会式收尾，或用户点名了镜头卡 | `references/pipeline.md` + `references/shots/` |

一台摄影机路径：**全片不切镜**，窗口从第二场出现到倒数第二场淡出，换场靠推、拉、摇和文案交接。切镜路径才使用 152 张配方卡；一种动画手法全片只当一次主角。

## 流程

### 1. 先定「讲哪几件事」，再定时长

一件事一个节拍，一个节拍 3～9 秒，全片 6～8 个节拍、30～45 秒。写成一张表：

| 讲什么 | 起始帧 | 时间 |
| --- | --- | --- |
| 开场 | 0 | 0:00 |
| …… | 90 | 0:03 |

判据是**减法**：这个版本独有的事才进片子。列不满六件就做 30 秒，不要用凑数的功能撑到 45 秒。共同创作把这张表交给用户确认；自主自由创作写入设计 spec 后继续。

### 2. 搭工程

新片住在产品仓库的 `video/`（或用户指定目录），**自己一份 `package.json` 和 `node_modules`**，不跟应用共用。从 `$SKILL/assets/film/` 拷 `anim.ts`、`camera.ts`、`scene.tsx`、`frames.mjs`、`jitter-check.mjs`、`remotion.config.ts`。走镜头卡切镜时再 copy `$SKILL/assets/lib/` 里需要的组件（PageCam 等）。走 Ink Press 则从 `template/` 起步。细则见 `references/engineering.md`。

### 3. 抄产品：设计 token 与那台机器

`references/product-machine.md`。先建 `design.ts`（颜色/字体/阴影，全部有出处），再决定界面素材：

- **重画**（默认，可动、可插值、特写仍是矢量清晰）；
- **Playwright 抓真机截图**（流程复杂、数据真实性本身是卖点、或 2.5D PageCam 需要纹理时）。

这一步做扎实，后面每一场都是白捡；这一步糊弄，后面每一场都要打补丁。

### 4. 时间轴写成纯函数；运镜写成镜头表

`references/engineering.md` 与 `references/camera-table.md`。

- `story.ts` 导出节拍表 `B` 和 `state(f)`：窗口里发生的一切（文件树长出几行、指针在哪、对话框开了多少）都是全局帧号的纯函数。想重排节奏，只改 `B` 里那几个数字。
- 运镜写成**镜头表**（`at` / `move` / `px,py` / `k` / `cx,cy`），保持段由 `makeCamera()` 自动生成。不要写成五条独立关键帧轨道——漏一个保持点，窗口就会以每帧几百分之一像素漂移，字会抖，时间轴上看不出来。
- 镜头卡切镜路径：每镜仍用纯函数驱动；PageCam 关键帧之间必须有明确的 hold，禁止无保持点的慢漂。

### 5. 实现镜头

模板路径按 `TEMPLATE.md` 替换。一台摄影机路径：场景组件只画文案，**不画产品**。镜头卡路径：用 `gallery/api/library.json` 校验卡名 → 读配方卡全文 → 按「参考实现」读准确 demo TSX → copy 对应 `assets/lib/` 组件。凭卡名新写＝放弃全部调校积累。

每个镜头只讲一个动效。关键信息落定后必须呼吸：品牌字标 hold ≥1s，批量动效收尾静止 0.5s，每一场最后一件事做完之后留 0.7～1.3 秒收口，不留第二秒。

### 6. 配乐（可选 —— 先问用户要不要）

**默认不配，问过再做。** 多数推广片在社交平台上是静音自动播放的，信息必须全在画面里；配错了乐的推广片，比没配乐伤害大。**无声是一个完整的交付，不是半成品。**

用户说不要：工程里不留 BGM 层、`music` 脚本或 `public/bgm.mp3`。SFX 仍可按 `references/sound-design.md` 钉在动作上。

用户说要：

- 有指定曲子或要卡点 → 先读 `references/music-beat-sync.md`，再分镜；
- 没有指定、只要「宣传片气质」→ `references/sound-design.md` 选型，或用 `$SKILL/assets/film/scripts/lib/synth.mjs` 纯代码合成（无第三方采样，可商用）；
- 终渲固定交付两版：带 BGM + 无 BGM（保留 SFX），靠 `bgm` inputProp 从同一时间线渲出。

### 7. 审片，再出片

`references/camera-table.md` 与 `references/final-review.md`。

1. `SCALE=0.5 COMP=<id> node scripts/frames.mjs <关键帧…>` 批量出图看构图，不要靠反复全片 render。
2. 停稳段落跑抖动校验：`SCALE=1 node scripts/frames.mjs 460 461 462 463` 然后 `node scripts/jitter-check.mjs --crop=W:H:X:Y 460 461 462 463`。四个哈希必须相同。
3. 交付前派一个干净上下文的 subagent 按 `references/final-review.md` 做独立终检。
4. 成片交付后默认询问一次是否导出剪映工程；需要则读 `references/jianying-export.md`。

## 何时读哪个文件

| 时机 | 读 |
|------|----|
| 项目启动且模式未定 | 最小只读检查，然后提供三种决策模式并推荐制作路径 |
| 自主自由创作 | pipeline.md（阶段 0–7，不逐阶段等待确认） |
| 共同创作 | guided-free-creation.md（确认阶段 0–3），再从 pipeline.md 阶段 4 继续 |
| 一台摄影机路径 | engineering.md + camera-table.md + product-machine.md |
| 走模板路线 | template/TEMPLATE.md 全文 |
| 分镜 / 选镜头卡 | sequences/；shots/ 全部 frontmatter；选中的卡读全文 |
| 逐镜头实现 | 该镜头卡全文 + 准确 demo 源码 + assets/lib/ 对应组件 |
| 用户已选 BGM | music-beat-sync.md（先分析再分镜） |
| 声音设计 | sound-design.md + assets/audio/ |
| 验收 | final-review.md + aesthetic-rules.md + camera-table.md 的抖动校验 |
| 成片交付后（剪映） | jianying-export.md |

## 资产使用方式

- `assets/film/` **copy 进新项目**（不 import 本库）：`anim.ts`（`t` / `enter` / `track`，全片两条缓动）、`camera.ts`（镜头表 → 摄影机，保持段自动生成）、`scene.tsx`（文案交接）、`scripts/frames.mjs`、`scripts/jitter-check.mjs`。要配乐才拷 `scripts/lib/synth.mjs`。来源与许可见 `assets/film/NOTICE.md`。
- `assets/lib/` 组件同样 copy 后修改：PageCam、ClipCard、DigitRoll、FlashCut、Caption、FlatPanel、VerticalTicker、helpers。FlatPanel 与 helpers/camera 需要 `three` + `@react-three/fiber` + `@remotion/three`。
- `assets/scripts/capture-template.mjs` 复制后改顶部 CONFIG。
- `assets/audio/` 免费商用（见 audio/ATTRIBUTION.md）：`bgm/` 备选；`sfx/<类别>/` 149 个音效分 16 类。词汇表 sparkle 的目录名是 `light/`。
- `demos/` 各卡实现源码；`template/` 完整可渲染工程。
- `gallery/` 优先给在线版 https://vincentwei1021.github.io/video-shotcraft/library.html 。

需要小黄角色时，先用 `cs-xiaohuang-skill` 产出合格资产，再把已验收的角色图作为叙事元素融入镜头；不要在宣传片里现场「设计」角色。

## 收尾清单

出片前逐条过，任一条不过就别发：

- [ ] 停稳段落里，窗口区域**逐像素**帧帧相同（`jitter-check.mjs`）
- [ ] 文案没有压在窗口上：算过 `cx - px·k` 和 `cx + (shellW - px)·k`，或镜头卡路径下字幕有效字高达标（Q11）
- [ ] 摄影机到位之后文案才进场
- [ ] 每一场最后一件事做完之后留 0.7～1.3 秒收口；品牌字标 hold ≥1s
- [ ] 全片只有一套颜色、一条缓动；片子里的数字（体积、版本、域名）跟真实产品对得上
- [ ] 要不要配乐问过用户了；配了的话重音与节拍起始帧对齐，并交付无 BGM 版
- [ ] 静音播放看不看得懂
- [ ] 独立 subagent 已按 final-review.md 出带帧号证据的报告
- [ ] 项目 README 写清楚「想改什么去改哪个文件」、这支片子已经讲过什么、踩过的坑（原样保留）

## 什么时候不要用这个 skill

- 要真人出镜、要实拍素材 → 这是拍摄，不是渲染
- 只是把现成视频剪一剪、加个字幕 → 直接 ffmpeg
- 只要一张图（封面 / OG 图）→ 那是静态图的活，别为它搭视频工程
- 产品还没有稳定的视觉 token → 先把设计系统定下来，否则片子里那台机器是假的
- 纪录片、长篇泛剪辑、口播混剪 → 超出本 skill 范围
