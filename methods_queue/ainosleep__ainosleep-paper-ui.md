---
name: ainosleep-paper-ui
description: Build or restyle websites, product interfaces, dashboards, editors, admin panels, portfolios, landing pages, and local HTML prototypes with the AINoSleep Paper UI design system — a warm paper-and-ink editorial workbench with a light and a dark theme. Use when the user asks for AINoSleep Paper UI, the paper workbench style, warm paper UI, editorial or print-inspired interface design, or wants consistent reuse of its tokens, typography, texture, navigation, cards, tables, forms, editor panels, outputs, and responsive patterns.
license: MIT
---

# AINoSleep Paper UI

一套「纸张工作台」设计系统。把它当成可以直接落到代码里的实现系统，不是拿来找感觉的视觉参考。

隐喻是**摊在安静工作台上的一份编辑任务书**：淡淡的绘图网格、奶油色纸张、深墨色备忘录、蓝色技术批注、红色校对标记、鼠尾草绿完成信号。

## 开工顺序

1. 先看目标项目：框架、已有组件、现有 token、响应式结构。**不要在别人的设计系统上硬套这一套。**
2. 选布局、字体、颜色、密度之前，读 [references/visual-system.md](references/visual-system.md)。
3. 做表单、编辑器、导航、卡片、表格、对话框、输出面板、状态之前，读 [references/component-catalog.md](references/component-catalog.md)。
4. 交付之前，跑一遍 [references/quality-bar.md](references/quality-bar.md)。
5. 把 `assets/paper-ui.css` **复制进目标项目**，改掉引用路径。绝不能让目标项目在运行时依赖 Skill 目录。

## 该抄哪个文件

| 你要做的事 | 用这个 |
|---|---|
| 任何新项目 | `assets/paper-ui.css` —— 唯一需要复制的系统文件 |
| 想要一个能直接改的空白骨架 | `assets/examples/starter/` |
| 想看每个部件长什么样、有哪些状态 | `assets/examples/gallery/` |
| 想看完整产品怎么用这套系统 | `assets/reference-app/` |
| 想看非应用类页面怎么用 | `assets/examples/personal-homepage/` |

`paper-ui.css` 自包含：没有 `@import`、没有 CDN 字体、没有 `url()` 外链、没有构建步骤。一个文件复制走就行。

`reference-app/` 是这套系统被提取出来的那个真实产品（Interface Brief Studio），作为**冻结的完整范例**保留。它有自己的应用外壳样式表，不要拿它当系统文件复制。

## 硬规则

- **保住可辨识的那一家子**：暖色网格画布、奶油纸张、墨色面板、编辑式衬线标题、克制的蓝色动作、红色批注、鼠尾草绿完成、细线、小圆角。
- **用语义 token，不要写死颜色**。确实有新的语义需求才加 token。
- **布局服从产品**。复用视觉语言，不要把每个页面都塞进同一个侧栏外壳。个人主页不需要伪装成应用。
- **先用原生语义 HTML**。button、a、label、fieldset、dialog、table、原生表单控件保持键盘可用。
- **表单和编辑器是一等公民**。label、帮助文字、必填/错误信息、hover、focus、disabled、空、保存中、已保存，该有的都要有。
- **控件是内嵌的书写面**：`--control` 填充、`--line-strong` 边框、`--radius-sm`、蓝色焦点环。不要换成通用白盒子或大药丸输入框。
- **颜色必须表意**：蓝色只给主动作、焦点、选中、活动状态和链接；红色给必填、警示、破坏性动作和编辑批注；鼠尾草绿给完成、已保存、成功。
- **表面层级要安静**：canvas → paper-low → paper → paper-high/control → 墨色备忘录/输出。
- **深度只靠表面色差和细线**，阴影只给浮层（dialog、toast、tooltip）。
- **不要编造**个人经历、指标、客户 logo、评价或产品成果。演示内容必须明确标为演示。
- **除非用户明确要求发布或部署，结果只留在本地。**

## 深色模式：夜间工作台

两个入口都要留：系统偏好 `prefers-color-scheme` + 手动 `[data-theme]`，手动优先。`paper-ui.css` 里已经写好了。

深色不是把浅色反相。隐喻是**关掉顶灯，只剩台灯下的那张纸**：画布退到最深，纸仍然是这个空间里最亮的平面，蓝色提亮以维持对比度。墨色备忘录在深色下变成比纸**更深**的一层，而不是反过来变亮。

### 切换主题必须先关过渡

这是一定会踩的坑，而且只有真的点一下才发现得了。

实测（Chrome）：运行时改 `data-theme` 之后，带 `transition` 的属性会保留**旧的绘制结果**。`getComputedStyle` 已经返回新颜色，但屏幕上还是旧颜色，滚动强制重绘也刷不掉。表现是 `.card`、按钮、输入框留着上一个主题的底色，和周围已经换新的部分对不上；严重时前景和背景挤到一起没法读。

**首次加载不受影响**，页面从头渲染是正确的 —— 所以看代码、看静态截图、跑构建都发现不了，只有真的去点那个切换按钮才会暴露。

`paper-ui.css` 提供了 `.theme-switching`，切换时这样用：

```js
function setTheme(next) {
  const root = document.documentElement;
  root.classList.add("theme-switching");     // 临时 transition: none
  root.setAttribute("data-theme", next);
  void root.offsetHeight;                     // 强制重算
  requestAnimationFrame(() => root.classList.remove("theme-switching"));
  localStorage.setItem("paper-ui:theme", next);
}
```

再在 `<head>` 里放一小段同步脚本读 `localStorage`，避免刷新时闪一下白。写法见 `assets/examples/starter/index.html`。

## 让页面好看的那些件

这套系统的"好看"不来自渐变和阴影，来自**编辑设计的真实工具箱**。需要的时候用，不要一次全堆上：

- **质感**：`.paper-canvas` 绘图网格 + SVG 噪点纸纹；`.paper-sheet` 内压痕；`.ruled` 稿纸横线文本域；`.taped` 纸角胶带；`.letterpress` 活字微光
- **排版**：`.dropcap` 首字下沉、`.pull-quote` 大引言、`.margin-note` 页边红批注、`.labeled-rule` 带标签分隔线、`.watermark` 水印页码、`.seal` 印章
- **数据**：`table`、`.metric` / `.metric-value`、`.meter` 量表、`.sparkline` 迷你折线、`.tag` 标签、`.status` 状态点
- **反馈**：`.callout` 内联提示条、`.skeleton` 骨架屏、`.tooltip` 纯 CSS 气泡、`dialog`、`.toast`

## 按页面类型选结构

### 产品界面 / 编辑器
用完整的工作台词汇：顶栏、流程侧栏、纸张编辑器、流程导轨、墨色实时备忘、标签页、输出纸、对话框、状态反馈。

### 个人主页 / 作品集
从 `examples/personal-homepage/` 起步。保留视觉家族，但信息结构改成概览、作品、方法、联系。**不要为了复用侧栏就把主页做成假应用。**

### 落地页 / 内容页
用编辑式纸张、项目卡、folio 标签、头注和一个明确的主动作。导航不服务内容时就减掉应用外壳。

### Dashboard
用 `.metric-row` + `table` + `.meter` + `.sparkline`。数字用等宽字体和 `tabular-nums`，让列对齐。一屏只留一个焦点指标。

## 明确不要做的

蓝紫渐变、玻璃拟态、霓虹色、通用 SaaS 模板感、大药丸输入框、过度圆角卡片、纯白页面底、只有无衬线的层级、厚重阴影、硬黑边框、无意义的装饰色、不服务内容的应用外壳。
