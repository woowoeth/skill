---
name: "字帖/作业纸生成器（米字格田字格13种）"
display_name: 字帖网格生成器
description: "一键生成可打印中文字帖与练习纸：米字格、田字格、回宫格、九宫格、四线三格等 13 种，支持汉字居中、自动换行、拼音标注。适合书法练字、小学语文作业、早教字卡，打印即用。"
market_desc: 教备神器出品的【Canvas 学习纸网格引擎】：一句话生成 printable 汉字练习纸，13 种网格任选（米字格/田字格/回宫格/九宫格/点阵/黄金圆格…），自动拼音标注、A4 直出。老师、教辅、国学机构做纸质练习的神器，微信小程序/网页通用。
version: 1.0.0
author: 教备神器
tags: [canvas, 字帖, 网格, 教育, 打印, 微信小程序]
---

# Canvas 学习纸网格渲染引擎

> 教备神器 · 工具模块。纯前端 Canvas 2D，零依赖，浏览器与微信小程序通用。

## 这是什么（给人看）

做字帖、练习纸、可打印学习用纸时，最麻烦的是把"米字格/田字格/回宫格"等网格画准、把汉字居中、把拼音自动标好。本技能给你一套**开箱即用的网格引擎**：导入 `references/grid-engine.js`，调几个函数就能渲染任意网格 + 居中汉字，直接导出 PNG 或接 PDF。老师、教辅、国学机构做纸质练习必备。

- 已附 `minimal-grid.html`：浏览器打开即见效果（米字格 + 12 字）。
- 已附 `selftest.js`：Node 跑通布局/图元/排版数学自测，证明算法靠谱。

## 何时使用

- "生成一张米字格字帖" / "做田字格练习纸" / "画 13 种网格"
- 小程序里要把文字居中画进格子、自动标拼音
- 需要 A4 1240×1754 标准分辨率输出

## 坐标系与令牌（AI 必读）

- **A4 内部分辨率固定 1240×1754（150dpi）**，与 SVG 源 `viewBox 21000×29700` 对应，换算 `SVG→px ≈ 0.0590476`。
- **显示缩放用 `canvas.style.width/height`**，绝不改 `canvas.width/height`（否则导出模糊）。
- **设计令牌** `TOKENS`：`green #07C160`、`black #2C2C2C`、`red #CC1414`、`blue #2B5FD9`、`gridLine #BBBBBB`、`innerDash #CCCCCC`、`pinyin #999999`。
- **内部辅助线统一虚线** `setLineDash([6,4])`、线宽 1、色 `#CCCCCC`；外框线用实线。

## 核心函数签名（AI 直接调用）

```javascript
// 布局：返回 { startX, startY, cells:[{row,col,x,y,size}] }，自动水平居中
GridEngine.computeLayout({ gridSize, cols, rows, margin, pageW?, pageH?, startY? })

// 单格网格图元（局部坐标）：支持 mizi/tianzi/huigong/jiugong/fangge/
//   hengxian/sixian/wuge/mizihuigong/tianzisidian/dianzhen/huangjinyuan
GridEngine.gridSegments(type, size)  // -> [{t:'line'|'dot'|'circle', ...}]

// 绘制单格网格（需 2D ctx）
GridEngine.drawGrid(ctx, type, cell, { color?, lineWidth? })

// 格内居中绘字（自动按宽度缩放，不溢出）；可带拼音（格上 1/4 区）
GridEngine.drawCharInCell(ctx, char, cell, { font?, color?, pinyin? })

// 字号自适应：不超过格短边 0.85
GridEngine.fitFontSize(char, cellSize, ctx, baseFont)  // -> px

// 逐字顺排：空格跳格、满列换行（首格左上角起点）
GridEngine.layoutCharacters(text, { startX, startY, gridSize, cols, rows })
```

## 绘制顺序（不可颠倒）

```
1. ctx.fillStyle=背景 → fillRect 覆盖全画布
2. drawGrid（网格线）          ← 网格在最底层
3. drawCharInCell（文字）      ← 文字在最上层
4. 导出图片（toDataURL / wx.canvasToTempFilePath）
```

## 常见坑（自动规避）

| 坑 | 正确做法 |
|----|----------|
| 文字模糊 | 先 `ctx.font='48px serif'` 再 `fillText`；小程序 `canvas.width = cssW*dpr` |
| 文字偏上 | 手动 `ctx.textBaseline='middle'` |
| 线不直 | `lineWidth` 用偶数、坐标用整数 |
| 导出空白 | 绘制前先给 `canvas.width/height` 赋值 |
| 边框撑爆 | `box-sizing:border-box`；网格坐标用 px 不混 rpx |

## 自测

```bash
node references/selftest.js   # 验证布局/图元/排版数学，PASS 方可交付
```

## 引用文件

- `references/grid-engine.js` — 引擎本体（浏览器/Node 通用，UMD）
- `references/minimal-grid.html` — 可运行演示（米字格 + 12 字）
- `references/selftest.js` — Node 自测

## 注意事项

- 引擎纯函数（无 DOM 依赖），`drawGrid/drawCharInCell` 需 2D ctx；Node 自测仅验证数学，不调用绘制。
- 字体缺失时回退系统 `serif`，不影响布局；正式发布替换为 `wx.loadFontFace` / `@font-face`。
- 与 `canvas-multipage-pdf`、`svg-to-canvas-replica` 互补：本技能负责"画"，后两者负责"导出/复刻"。

## 教备神器 Canvas 工具链（组合使用）

本技能是「教备神器 · Canvas 工具链」的一环，四件组合覆盖「画 → 复刻 → 导出 → 验证」完整闭环：

- Canvas 学习纸网格引擎（画）：13 种教育网格 + 汉字居中 + 拼音标注，生成米字格/田字格字帖。
- SVG 转 Canvas 复刻引擎（复刻）：把现有纸质模板 SVG 零误差复刻成可改字、可打印的 Canvas。
- Canvas 多页 PDF 导出（导出）：多页 Canvas 一键合成标准 A4 PDF 直接打印。
- 小程序 Canvas 验证工作流（验证）：本地预览 + 截图视觉回归，杜绝格子歪、字偏。

完整方案与演示见「教备神器 Canvas 工具链落地页」（链接发布后回填）。
