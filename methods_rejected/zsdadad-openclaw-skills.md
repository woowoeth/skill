---
name: diagram-tools
description: 图表工具集 - 生成各种图表 (支持 Mermaid/Graphviz)
version: 1.1.0
author: OpenClaw
tags: [diagram, chart, image, visualization, graph, mermaid, mindmap]
category: visualization
---

# Diagram Tools

图表工具集，生成各种可视化图表。

## 功能

### 1. Mermaid 图表
使用 Mermaid CLI 生成各类图表：
- **Flowchart**: `graph TD` / `graph LR`
- **Sequence**: `sequenceDiagram`
- **Class**: `classDiagram`
- **State**: `stateDiagram-v2`
- **ER**: `erDiagram`
- **Gantt**: `gantt`
- **Pie**: `pie`
- **Mindmap**: `mindmap`
- **Timeline**: `timeline`
- **Git graph**: `gitGraph`
- **Quadrant**: `quadrantChart`

### 2. Graphviz 图表
使用 Graphviz 生成：
- 流程图
- 架构图
- 思维导图

### 3. 数据图表
- 柱状图、折线图、饼图等

## 使用方法

### Mermaid 图表

```bash
# 基本命令
mmdc -i input.mmd -o output.png -t dark -b transparent

# 高清输出
mmdc -i input.mmd -o output.png -t dark -b transparent -s 2
```

### Graphviz 图表

```python
from graphviz import Digraph
dot = Digraph()
dot.node('A', '节点A')
dot.node('B', '节点B')
dot.edge('A', 'B')
dot.render('output', format='png')
```

### 思维导图 (Mermaid mindmap)

```mermaid
mindmap
  root((主题))
    分支1
      子主题A
    分支2
      子主题B
```

## 支持的图表类型

| 类型 | 语法前缀 |
|------|----------|
| 流程图 | `graph TD`, `graph LR` |
| 时序图 | `sequenceDiagram` |
| 类图 | `classDiagram` |
| 状态图 | `stateDiagram-v2` |
| ER图 | `erDiagram` |
| 甘特图 | `gantt` |
| 饼图 | `pie` |
| 思维导图 | `mindmap` |
| 时间线 | `timeline` |
| 四象限 | `quadrantChart` |

## 主题配置

自定义颜色：

```json
{
  "theme": "base",
  "themeVariables": {
    "primaryColor": "#1976d2",
    "lineColor": "#666666",
    "secondaryColor": "#4caf50",
    "tertiaryColor": "#ff9800"
  }
}
```

## 提示

- 使用 `graph LR` 表示从左到右，`graph TD` 表示从上到下
- 保持节点标签简短
- 使用子图分组相关组件
- 高清输出使用 `-s 2` 或 `-s 3`
