---
name: ppt-lai
license: MIT
compatibility: Requires Python 3.10+, Pillow (PIL), python-pptx; uv recommended for install.
description: >
  当用户要求把主题、提纲或材料做成 2000–2010 年代千禧年风格 PPT，或要求把现有 .pptx
  翻新为旧课件视觉时使用。交付原生可编辑的 4:3 .pptx，支持 L1/L2/L3；已有 PPT 的翻新
  路径逐字冻结内容。用户追求现代、简洁、商务或高端视觉时不要使用。
metadata:
  author: ppt-lai maintainers
  homepage: https://github.com/astro-koko/ppt-lai
---

# ppt-lai · 千禧年风格 PPT

## 任务契约

你对抗的是自己的美化本能。大模型默认会：对齐、留白、统一字体、和谐配色、提炼要点。
**在本 Skill 中，以上每一条都是被禁止的。**

千禧年风格 PPT 不是随便做坏，而是**一份被认真使用、反复传阅、年代感明确的旧课件**。所有反审美选择都要有年代依据和人物动机。

六条铁律：
1. **反审美必须有出处**：每个视觉决策都要能对应到 references 里的某条参数。
2. **一致性比混乱重要**：选定档位后全套严守该档参数矩阵。
3. **绝不出现现代元素**：无扁平化图标、无留白美学、无无衬线中文正文、无低饱和莫兰迪配色。
4. **交付即原生对象，禁止声明代交付**：标题、正文、水印等必须真实写进 spec 的文本 runs，
   禁止用“此处安排某种效果”代替实际可编辑对象。
5. **视觉可以有年代感，事实仍须准确（事实红线）**：风格只作用于展示层——视觉、语气、版式和标题可以复古；
   **时间和事实不捏造**：技术细节、版本、产品能力、日期、数据、引文、术语定义和因果关系必须真实。
   现代主题可以使用复古视觉，但 `meta.visual_era` 与 `meta.factual_era` 必须分开写；
   构建前后各完成一次事实审校，无可靠来源的精确断言改为中性描述或向用户索要材料。
6. **改造路径内容冻结（仅 retrofit）**：把**既定 .pptx** 翻新为千禧年风格时，文字逐字保留——
   不增、不减、不改、不重排语序、**不注入错别字**；「内容可丑」= 保留原文自身的丑，绝非主动制造丑。
   与 A 生成路径（content-degradation 年代化文案）严格区分；改造走 retrofit-existing-pptx（见其铁律）。

## 先路由，再执行

1. 锚定本 `SKILL.md` 所在目录为绝对 `SKILL_ROOT`；所有资源与脚本都从它解析。
2. 读 `workflows/routing.md`，根据完整意图选且只选一条路径。
3. 读所选 workflow 与它要求的 reference。不要把生成路线的文案规则带入内容冻结的翻新路线。

## Python 运行时门禁（生成或翻新前必过）

只有路由到 generate 或 retrofit、即将调用 Python 工具时才执行本节；只咨询风格不需要安装依赖。全仓只使用此 `SKILL_ROOT` 下的一份 `requirements.txt`，不为不同宿主维护副本、锁定文件或适配脚本。

使用第 1 步锚定的**绝对** `SKILL_ROOT`，并执行以下唯一序列：先确认当前宿主实际要调用的 `python3` 是 Python 3.10+，检查直接依赖；仅在导入失败时安装，最后复查。

```bash
python3 -c 'import sys; sys.version_info >= (3, 10) or sys.exit(f"需要 Python 3.10+，当前为 {sys.version}")'
if ! python3 -c 'import pptx; from PIL import Image'; then
  if command -v uv >/dev/null 2>&1; then
    uv pip install --python python3 -r "$SKILL_ROOT/requirements.txt" || true
  fi
  if ! python3 -c 'import pptx; from PIL import Image'; then
    python3 -m pip install -r "$SKILL_ROOT/requirements.txt"
  fi
fi
python3 -c 'import pptx; from PIL import Image; print("ppt-lai 运行时依赖可用")'
```

Python 版本不足、命令受限、两种安装均失败或依赖仍不可导入时，**停止构建或解析**；说明缺失条件和以上本地安装命令，不得声称已生成 `.pptx`。

## 共通不可妥协项

1. **只落实，不优化**：spec/坐标写多歪就多歪，构建阶段不做现代化修正。
2. **顺序执行**：先写内容与视觉，再写 spec；spec 未完成不构建，成品未核对不交付。
3. **门禁在构建前**：内容、事实、反现代、密度与多样性门禁任一失败，即回到相应阶段重写或重排。
4. **阻塞即停**：自定义需求不清晰时，停下问档位与风格取向，不替用户猜。

## 三档年代感（默认 L2）

- **L1 · 旧课件感**（轻度，2007–2010）
- **L2 · 祖传课件感**（浓郁，推荐，2003–2006）
- **L3 · 镇馆文物感**（考古级，2000–2002）

完整参数矩阵见 `references/patina-levels.md`——选定档位后它是最高准则。

## 交付

- 主交付物：**原生可编辑 .pptx**（4:3，经 `scripts/build_native.py` 构建）
- 文件命名：按 `references/patina.md` 命名规范
- 附一句话"课件来历说明"
- 可选（用户要院士/传家宝/老讲座味时）：院士风味包 + slogan"人没了，PPT还在"

## 按需加载地图

| 文件 | 何时读 |
|---|---|
| `references/patina-levels.md` | 第 0 步定档后必读的参数总矩阵 |
| `references/content-degradation.md` | 第 1 步，标题与叙事节奏的事实契约 |
| `references/anti-design-visual.md` | 第 2 步，年代反审美视觉（spec 硬约束） |
| `references/academic-vibe.md` | 可选，院士/传家宝/老讲座味的院士风味包 |
| `references/fact-guard.md` | 第 5 步，事实红线与对抗性审查（强制） |
| `references/native-render-spec.md` | 第 4 步，spec JSON 字段规范与自检清单 |
| `references/patina.md` | 使用痕迹效果、文件名命名规范 |
| `references/retro-interaction.md` | 经典课件叙事结构、转场/音效矩阵 |
| `scripts/build_native.py` | 第 6 步，spec → 原生 .pptx 的构建器 |
| `scripts/extract_pptx.py` | retrofit 第 2 步，解析既有 .pptx → content/inventory/verbatim |
| `workflows/retrofit-pptx.md` | retrofit 路线运行时（含内容冻结铁律） |
