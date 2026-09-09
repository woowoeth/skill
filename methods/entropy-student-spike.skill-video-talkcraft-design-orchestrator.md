---
name: video-talkcraft-design-orchestrator
description: 上层视频制作编排 Skill。动态读取并调用 Vincentwei1021/video-talkcraft 的现行流程，不复制、不修改其内部规则；仅增加两个用户交互点：开工时一次性收集 TalkCraft 必需输入并同步选择视觉风格，以及 SHOTBOOK 完成后进行用户确认并提示可补充素材。可将 VoltAgent/awesome-design-md 中的 DESIGN.md 作为视觉风格来源。其余制作、Recipe、Remotion、渲染、验收与交付规则全部以当前 video-talkcraft 为准。
---

# TalkCraft Design Orchestrator（TalkCraft 视觉编排器）

## 目标

这是一个**上层编排 Skill**，不是 `video-talkcraft` 的分叉、复制版或改写版。

它只负责：

1. 在 `video-talkcraft` 正式开工时，用**同一次用户交互**收集 TalkCraft 当前要求的必需输入，并同步让用户选择视觉风格。
2. 在 `SHOTBOOK` 生成完成、进入实现前增加一次**用户确认 + 素材补充提醒**。

除此之外，**所有规则、输入要求、素材采集、SHOTBOOK 格式、Recipe 选卡、TSX 复制、运动命门、Remotion 实现、渲染、音效、质检、审片、交付等，全部由当前版本的 `video-talkcraft` 决定。**

---

## 上游依赖（禁止内嵌）

### A. 视频制作主 Skill

- Repository: `https://github.com/Vincentwei1021/video-talkcraft`
- Authority: 当前版本 `SKILL.md` 及其引用的 `references/`、`template/`、`scripts/`

### B. 可选视觉风格库

- Repository: `https://github.com/VoltAgent/awesome-design-md`
- Authority: 当前仓库中的 `DESIGN.md` 风格文件

### 更新兼容规则

每次调用本 Skill 时：

1. **先读取当前可用的 `video-talkcraft/SKILL.md`，不得依赖本文件中对其流程的历史摘要。**
2. 识别 `video-talkcraft` 当前要求用户提供的必需输入；如果当前仍为“口播稿 + 与之逐字一致的成品配音”，则按当前规则执行；若上游未来变化，以最新上游为准。
3. 用户选择 `awesome-design-md` 风格时，再读取该仓库当前对应的 `DESIGN.md`。
4. 不把上游 `SKILL.md`、Recipe、TSX、DESIGN.md 复制进本 Skill 作为固定快照。
5. 上游若更新流程名称或步骤编号，以语义位置为准：
   - 入口交互发生在正式制作开始前；必需输入收集与风格选择必须合并为同一次询问。
   - SHOTBOOK 用户确认插入在“SHOTBOOK 已完成”与“Remotion / Recipe 实现开始”之间。
6. 除本 Skill 明确声明的两个插入点外，出现任何规则差异时，**以上游当前 `video-talkcraft` 为准**。

---

# 调用流程

## Step 0 — 先加载 video-talkcraft

完整读取当前 `video-talkcraft/SKILL.md` 以及执行当前任务所要求读取的 references。

识别当前上游要求的必需输入，但**不要先单独询问输入、再单独询问风格**。

随后执行本 Skill 的【插入点 ①】。

---

# 插入点 ① — 一次性收集必需输入 + 选择视觉风格

正式制作开始前，第一次需要向用户索取信息时，必须将以下两类内容放在**同一条询问**中：

### A. video-talkcraft 当前要求的必需输入

以当前上游为准。

若当前要求仍为：

- 口播稿
- 与口播稿逐字一致的成品配音（wav/mp3）

则同时请用户上传 / 提供这两项。

如果用户已经在当前会话中提供其中一项，不要重复索要，只补齐缺失项。

### B. 同步选择视觉风格

在同一次询问中，让用户从以下三类中选择：

#### 1. TalkCraft 默认风格

完全使用当前 `video-talkcraft` 自己的视觉语言规则与领域风格派生流程。

#### 2. awesome-design-md 风格

从 `VoltAgent/awesome-design-md` 当前 DESIGN.md 库中选择一种设计语言，用作本片的**视觉皮肤来源**。

向用户简要给出少量代表性例子即可，不要一次罗列全库。例如：

- **Apple**：大量留白、克制、产品感、电影化图片。
- **Runway**：深色电影感、编辑部 / 影展气质。
- **Nike**：超大字、黑白强对比、全幅摄影、冲击力强。
- **Stripe**：轻盈、精致、渐变、现代科技感。
- **Linear**：极简、精确、深色 + 紫色点缀。
- **Notion**：温暖极简、柔和表面、编辑感。
- **Spotify**：深色、高饱和绿色、粗体、音乐视觉感。
- **WIRED**：杂志 / 报刊编辑风、信息密度高。

示例必须以 `awesome-design-md` 当前实际存在的 DESIGN.md 为准；若库已变化，以当前内容更新例子。

如果用户选择该类但尚未指定具体 DESIGN.md，则让用户从推荐项中选择，或根据用户明确描述的目标风格定位到一个 DESIGN.md 后请用户确认。

#### 3. 用户自定义 / 上传设计风格

用户可以提供任意一种：

- DESIGN.md
- 设计规范文档
- 截图 / 参考图
- 品牌视觉规范
- 文字描述的风格要求

按 `video-talkcraft` 当前“用户明确指定风格”的规则处理。

### 标准首次询问形式

当当前 `video-talkcraft` 的必需输入仍为口播稿与成品配音时，用户看到的入口应接近：

> 请同时提供：①口播稿；②与口播稿一致的成品配音（wav/mp3）。同时请选择本次视频视觉风格：A. TalkCraft 默认；B. awesome-design-md 中的风格；C. 上传 / 描述自定义设计风格。

不要把这一步拆成“先上传输入 → 再问风格”两个独立确认节点。

---

## 风格接入边界

无论选择默认 / awesome-design-md / 自定义，都**不得改变 `video-talkcraft` 的 Recipe 运动实现规则**。

如果选择外部风格：

1. 将所选设计语言转换 / 映射为 `video-talkcraft` 当前允许的风格档 / theme / 蒙皮信息。
2. 只影响上游允许修改的视觉皮层，例如颜色、字体气质、字重、圆角、描边、投影、材质、图表视觉、素材气质、卡片外观等。
3. Recipe 的时序、缓动、几何比例、运动方向、层级关系及其他上游定义的“运动命门”继续严格遵守 `video-talkcraft` 当前规则。
4. 若 DESIGN.md 中存在面向网页交互、响应式布局等与视频无关的规则，只提取可映射到视频视觉语言的部分；不得因此扩展或改写 TalkCraft 的制作流程。

输入与风格确定后，**恢复执行当前 `video-talkcraft` 原流程**，直到 SHOTBOOK 完整生成并通过上游要求的实现前检查。

---

# 插入点 ② — SHOTBOOK 完成后的用户确认与素材提醒

当 `video-talkcraft` 已完成本片 `SHOTBOOK`，但尚未进入 Recipe / Remotion 正式实现时，暂停一次并向用户展示 / 概括 SHOTBOOK，要求用户确认。

## 必须提醒的内容

除正常确认 SHOTBOOK 外，必须特别标出其中涉及以下素材的镜头，并提醒：

> 如果你有更合适的自有素材，可以现在上传，我会优先替换进这些镜头；如果不提供，则继续按照 `video-talkcraft` 原本的素材采集与制作流程执行。

### 推荐用户补充的素材类型

只列出本片 SHOTBOOK 实际相关的类型，可从以下范围选择：

- **人物 / 主播素材**：真人出镜、数字人成品、人物录制视频。
- **B-roll 视频**：产品实拍、场景视频、过程演示、生活 / 工作环境等。
- **图片 / 照片**：产品图、人物照片、事件照片、海报、插画等。
- **网页 / UI / 软件素材**：指定页面、产品界面、App / 网站截图来源。
- **品牌素材**：Logo、品牌图形、包装、官方视觉资产。
- **证据素材**：用户希望明确出现在视频里的数据图、报告、文章、原始截图、资料页面。
- **其他 SHOTBOOK 已指定的真实素材**。

不要为了提醒而要求用户必须上传素材。

## 用户响应分支

### 用户确认，且未提供新素材

立即恢复 `video-talkcraft` 原流程。

- 原 Skill 该自动采集的素材继续自动采集。
- 原 Skill 该使用的 B-roll / 图片 / 截图 / 纯动效策略保持不变。
- 不再增加额外素材审批步骤。

### 用户确认，并提供了素材

1. 将用户素材替换到 SHOTBOOK 中对应或最合适的素材位。
2. 更新受影响镜头的素材路径 / 素材记录以及上游要求同步更新的相关文件。
3. 对替换后的素材重新执行 `video-talkcraft` 当前要求的素材体检 / preflight。
4. 不改变镜头意图、Recipe 运动命门或其他上游规则，除非素材客观上要求按 `video-talkcraft` 规则重新选卡或重新排版。
5. 完成后继续 `video-talkcraft` 原流程。

### 用户要求修改 SHOTBOOK

按用户明确意见修改受影响镜头，并重新执行 `video-talkcraft` 当前要求的 SHOTBOOK / preflight 检查；通过后再继续。

---

# 之后的执行

插入点 ② 完成后：

**完全恢复当前版本 `video-talkcraft` 的流程。**

本 Skill 不再增加任何新的确认、渲染步骤、审片规则或交付规则。

若 `video-talkcraft` 自身要求后续与用户进行选择 / 确认，则严格照上游当前规则执行。

---

# 禁止事项

- 禁止修改上游 `video-talkcraft` 仓库内容。
- 禁止修改 `awesome-design-md` 仓库内容。
- 禁止在本 Skill 内维护一份 `video-talkcraft` 流程副本并声称等价。
- 禁止把“必需输入收集”和“视觉风格选择”拆成两个顺序询问节点。
- 禁止重新实现 Recipe 动画以替代上游模板。
- 禁止因为选择 DESIGN.md 而跳过 TalkCraft 的 SHOTBOOK、选卡、preflight、渲染或验收规则。
- 禁止把“用户可上传素材”变成“用户必须上传素材”。
- 禁止在用户未提供新素材时改变上游原本的素材处理策略。

---

# 用户看到的最简流程

```text
一次性入口交互：
上传 / 提供 TalkCraft 必需输入 + 同时选择视觉风格
        ↓
按最新 video-talkcraft 制作
        ↓
SHOTBOOK 完成
        ↓
用户确认分镜 + 提醒可上传对应素材
        ↓
未上传 → 原 TalkCraft 流程继续
已上传 → 替换对应素材并重新体检
        ↓
恢复最新 video-talkcraft 全部后续流程
        ↓
最终视频
```
