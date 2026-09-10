---
name: figma-implement-design
description: 把 Figma 节点翻译为生产级代码，用 Figma MCP 工作流实现 1:1 视觉还原（设计上下文、截图、资源、项目约定转译）。当用户给出 Figma 链接或 node ID，或要求实现必须对齐 Figma 稿件的设计 / 组件时使用。需要可用的 Figma MCP 连接。
author: openai
version: "0.1.0"
tags:
  - design
  - figma
  - mcp
  - pixel-perfect
  - frontend
---

# 实现设计稿（Implement Design）

> 中文翻译版。原文：<https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/creative-design/figma-implement-design>（作者 openai，Apache-2.0，许可证见同目录 `LICENSE.txt`）。工具名、参数名、代码保持原样未翻译。

## 概述

本 skill 提供一套结构化流程，把 Figma 设计稿翻译为生产级代码，并达到像素级准确度。它保证与 Figma MCP server 的一致集成、设计 token 的正确使用，以及与设计稿 1:1 的视觉一致性。

## 前置条件

- Figma MCP server 已连接且可访问。
- 用户提供的 Figma URL 格式为：`https://figma.com/design/:fileKey/:fileName?node-id=1-2`
  - `:fileKey` 是文件 key。
  - `1-2` 是 node ID（要实现的那个组件或画板）。
- **或者** 在使用 `figma-desktop` MCP 时，用户可以直接在 Figma 桌面端选中节点（无需 URL）。
- 项目最好已有成熟的设计系统或组件库（优先）。

## 必走流程（Required Workflow）

**按顺序执行以下步骤，不得跳步。**

### 步骤 0：配置 Figma MCP（若尚未配置）

如果任何 MCP 调用失败并提示 Figma MCP 未连接，先停下来把它配好：

1. 添加 Figma MCP：
   - `codex mcp add figma --url https://mcp.figma.com/mcp`
2. 启用远程 MCP 客户端：
   - 在 `config.toml` 里设置 `[features].rmcp_client = true`，**或** 运行 `codex --enable rmcp_client`
3. 用 OAuth 登录：
   - `codex mcp login figma`

登录成功后，用户需要重启 codex。此时你应结束本轮回答并告知用户：重启后再试即可从步骤 1 继续。

### 步骤 1：拿到 Node ID

#### 方案 A：从 Figma URL 解析

用户给出 Figma URL 时，从中提取 file key 和 node ID，作为参数传给 MCP 工具。

**URL 格式：** `https://figma.com/design/:fileKey/:fileName?node-id=1-2`

**提取：**

- **File key：** `:fileKey`（`/design/` 之后的那一段）
- **Node ID：** `1-2`（`node-id` 查询参数的值）

**注意：** 使用本地桌面版 MCP（`figma-desktop`）时，`fileKey` 不作为参数传给工具调用。server 自动使用当前打开的文件，因此只需要 `nodeId`。

**示例：**

- URL：`https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15`
- File key：`kL9xQn2VwM8pYrTb4ZcHjF`
- Node ID：`42-15`

#### 方案 B：使用 Figma 桌面端的当前选中项（仅 `figma-desktop` MCP）

使用 `figma-desktop` MCP 且用户未提供 URL 时，工具会自动使用桌面端当前打开文件里被选中的节点。

**注意：** 基于选中项的提示方式只对 `figma-desktop` MCP server 有效。远程 server 需要 frame 或 layer 的链接才能提取上下文，且用户必须打开 Figma 桌面端并选中某个节点。

### 步骤 2：拉取设计上下文

用提取到的 file key 和 node ID 运行 `get_design_context`。

```
get_design_context(fileKey=":fileKey", nodeId="1-2")
```

它返回结构化数据，包含：

- 布局属性（Auto Layout、约束、尺寸）
- 字体规格
- 颜色值与设计 token
- 组件结构与变体
- 间距与内边距数值

**如果响应过大或被截断：**

1. 运行 `get_metadata(fileKey=":fileKey", nodeId="1-2")` 拿到高层级节点地图。
2. 从 metadata 中确认需要哪些具体子节点。
3. 用 `get_design_context(fileKey=":fileKey", nodeId=":childNodeId")` 逐个拉取子节点。

### 步骤 3：抓取视觉基准

用同样的 file key 与 node ID 运行 `get_screenshot`，拿到视觉参考。

```
get_screenshot(fileKey=":fileKey", nodeId="1-2")
```

这张截图是视觉验收的唯一事实来源（source of truth），实现全过程都要能拿到它。

### 步骤 4：下载所需资源

下载 Figma MCP server 返回的所有资源（图片、图标、SVG）。

**重要：** 遵守以下资源规则：

- 如果 Figma MCP server 为某张图片或 SVG 返回了 `localhost` 源，直接使用该源
- 不要引入或新增任何图标包 —— 所有资源都应来自 Figma 的返回数据
- 提供了 `localhost` 源时，不要使用或创建占位资源
- 资源由 Figma MCP server 内置的 assets endpoint 提供

### 步骤 5：转译为项目约定

把 Figma 的输出转译成本项目的框架、样式与约定。

**关键原则：**

- 把 Figma MCP 的输出（通常是 React + Tailwind）视为「设计与行为的表达」，而不是最终代码风格
- 用项目自己的工具类或设计系统 token 替换 Tailwind 工具类
- 复用既有组件（按钮、输入框、排版、图标容器），而不是重复造功能
- 一致地使用项目的颜色体系、字号阶梯与间距 token
- 遵守既有的路由、状态管理与数据获取模式

### 步骤 6：做到 1:1 视觉还原

向与 Figma 设计稿像素级一致的目标努力。

**准则：**

- 以 Figma 保真度为优先，精确匹配设计稿
- 避免硬编码数值 —— 有 Figma 设计 token 就用 token
- 当设计系统 token 与 Figma 规格冲突时，优先设计系统 token，但用最小幅度的间距或尺寸调整去对齐视觉
- 遵循 WCAG 无障碍要求
- 按需补充组件文档

### 步骤 7：对照 Figma 验收

在标记完成之前，把最终 UI 与 Figma 截图做对照验收。

**验收清单：**

- [ ] 布局一致（间距、对齐、尺寸）
- [ ] 排版一致（字体、字号、字重、行高）
- [ ] 颜色完全一致
- [ ] 交互态按设计工作（hover、active、disabled）
- [ ] 响应式行为符合 Figma 约束
- [ ] 资源渲染正确
- [ ] 满足无障碍标准

## 实现规则（Implementation Rules）

### 组件组织

- 把 UI 组件放在项目指定的设计系统目录下
- 遵循项目的组件命名约定
- 除非动态值确实必要，否则避免内联样式

### 设计系统集成

- 只要可能，**始终**使用项目设计系统中的组件
- 把 Figma 设计 token 映射到项目设计 token
- 存在匹配组件时，扩展它而不是新建
- 为加入设计系统的新组件补文档

### 代码质量

- 避免硬编码数值 —— 抽成常量或设计 token
- 保持组件可组合、可复用
- 为组件 props 加 TypeScript 类型
- 为导出的组件写 JSDoc 注释

## 示例

### 示例 1：实现一个按钮组件

用户说：「实现这个 Figma 按钮组件：https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15」

**动作：**

1. 解析 URL，得到 fileKey=`kL9xQn2VwM8pYrTb4ZcHjF`、nodeId=`42-15`
2. 运行 `get_design_context(fileKey="kL9xQn2VwM8pYrTb4ZcHjF", nodeId="42-15")`
3. 运行 `get_screenshot(fileKey="kL9xQn2VwM8pYrTb4ZcHjF", nodeId="42-15")` 作为视觉参考
4. 从 assets endpoint 下载按钮用到的图标
5. 检查项目是否已有按钮组件
6. 有则扩展出新变体；没有则按项目约定新建组件
7. 把 Figma 颜色映射到项目设计 token（例如 `primary-500`、`primary-hover`）
8. 对照截图校验内边距、圆角、排版

**结果：** 与 Figma 设计一致的按钮组件，并已接入项目设计系统。

### 示例 2：搭一个仪表盘布局

用户说：「搭这个仪表盘：https://figma.com/design/pR8mNv5KqXzGwY2JtCfL4D/Dashboard?node-id=10-5」

**动作：**

1. 解析 URL，得到 fileKey=`pR8mNv5KqXzGwY2JtCfL4D`、nodeId=`10-5`
2. 运行 `get_metadata(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId="10-5")` 理解页面结构
3. 从 metadata 识别主要区块（header、sidebar、内容区、卡片）及其子节点 ID
4. 对每个主要区块运行 `get_design_context(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId=":childNodeId")`
5. 运行 `get_screenshot(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId="10-5")` 拿整页截图
6. 下载全部资源（logo、图标、图表）
7. 用项目的布局原语搭出整体布局
8. 尽可能用既有组件实现每个区块
9. 对照 Figma 约束校验响应式行为

**结果：** 与 Figma 设计一致的完整仪表盘，含响应式布局。

## 最佳实践

### 永远从上下文开始

不要基于假设实现。先拉 `get_design_context` 和 `get_screenshot`。

### 增量验收

实现过程中要频繁验收，而不是只在最后。这样能尽早发现问题。

### 记录偏离

如果必须偏离 Figma 设计（例如为了无障碍或技术限制），在代码注释里写明原因。

### 复用优于重建

新建组件前先找已有组件。代码库的一致性比精确复刻 Figma 更重要。

### 设计系统优先

拿不准时，优先项目的设计系统模式，而不是字面照搬 Figma。

## 常见问题与解法

### 问题：Figma 输出被截断

**原因：** 设计过于复杂或嵌套层级太多，单次响应返回不完。
**解法：** 用 `get_metadata` 拿节点结构，再用 `get_design_context` 逐个拉取指定节点。

### 问题：实现后设计与稿子不一致

**原因：** 实现代码与原始 Figma 设计存在视觉差异。
**解法：** 与步骤 3 的截图并排比对，检查设计上下文数据里的间距、颜色、排版数值。

### 问题：资源加载不出来

**原因：** Figma MCP server 的 assets endpoint 不可访问，或 URL 被改写。
**解法：** 确认 Figma MCP server 的 assets endpoint 可访问。server 以 `localhost` URL 提供资源，直接原样使用，不要修改。

### 问题：设计 token 值与 Figma 不同

**原因：** 项目设计系统 token 的取值与 Figma 设计中指定的不同。
**解法：** 项目 token 与 Figma 数值不一致时，为保持一致性优先用项目 token，同时微调间距 / 尺寸以维持视觉保真。

## 理解「实现设计」这件事

Figma 实现工作流为「设计稿 → 代码」建立了一条可靠路径：

**对设计师：** 有信心实现在像素级准确度上与设计稿一致。
**对开发者：** 一套结构化方法，消除猜测、减少来回返工。
**对团队：** 一致、高质量的交付，并保持设计系统的完整性。

遵循这套流程，就能保证每一份 Figma 设计都以同样细致的标准被实现。

## 延伸资料

- [Figma MCP Server 文档](https://developers.figma.com/docs/figma-mcp-server/)
- [Figma MCP Server 工具与提示](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)
- [Figma Variables 与设计 token 指南](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma)
