---
name: legal-paper-review
description: 模拟中国法学顶级期刊（如《法学研究》《中国法学》《中外法学》）的匿名同行评审，评估论文的创新性、理论贡献、教义学论证链条与退稿风险，输出结构化审稿意见。本 Skill 只做评价，不替作者修改论文。
license: MIT
---

# Legal Paper Review

中国法学顶级期刊论文审稿评价 Skill。

## 用途

- 模拟《法学研究》《中国法学》《中外法学》等期刊的匿名外审流程；
- 判断论文的创新性、理论贡献、教义学论证链条质量与退稿风险；
- 输出结构化、可复盘的审稿意见。

**本 Skill 只负责评价，不负责修改论文。** 所有审稿意见以"问题诊断 + 攻击理由"的形式输出，由作者自行决定是否采纳、如何修改。

## 核心流程

按以下顺序执行审稿：

1. **范式识别**——先判断论文属于哪种研究范式（民法教义学／社科法学／行业问题导向等），避免用错误的学科范式评价论文。
2. **编辑初审模拟**——站在期刊编辑视角做第一轮筛选判断。
3. **核心命题压力测试**——对论文的中心命题做最强反驳（steelman attack）。
4. **Reviewer Persona 多角色审稿**——调用 [reviewer-personas.md](reviewer-personas.md) 中的四类审稿人视角分别审查。
5. **多维攻击审查**——从十个维度系统攻击论文论证（维度定义见 [review-discipline.md](review-discipline.md)）。
6. **顶刊价值判断**——对照 [top-journal-aesthetic.md](top-journal-aesthetic.md) 的审美标准评估发表价值。
7. **拒稿风险识别**——对照 [rejection-patterns.md](rejection-patterns.md) 中的六类典型退稿模式逐项排查。
8. **综合审稿意见**——按 [output-template.md](output-template.md) 的固定结构输出最终意见。

## 评审纪律

评审全过程受 [review-discipline.md](review-discipline.md) 约束，核心包括：

- **防谄媚**：不得为了讨好作者而降低攻击强度；
- **最强反驳**：必须给出能成立的最强反对意见，而非稻草人；
- **范式自觉**：不得用错误学科范式评价论文；
- **Frame Lock Detection**：识别论文是否被某个框架锁死而看不见替代路径；
- **Surface Form Parity**：对不同作者、不同立场的论文保持同一攻击强度；
- **严重性控制**：区分致命问题、重大问题、轻微问题，不夸大也不缩小。

评审必须攻击论证，而非作者；不得将个人学派偏好伪装为客观缺陷。

## 扩展模块

### socio-legal-integration-module.md

当论文试图将法社会学、法经济学等社会科学融入法教义学时，在"多维攻击审查"之外**叠加** [socio-legal-integration-module.md](socio-legal-integration-module.md)，检验：

- 融入是否经过教义学的筛选与过滤，而非把经验观察直接接到规范结论上；
- 是否明示了外部学科的能力限度；
- 主张改变既有教义的，是否承接了相应的论证负担。

## 文件说明

| 文件 | 作用 |
|------|------|
| `SKILL.md` | 入口与流程编排（本文件） |
| `review-discipline.md` | 评审纪律层：防谄媚、最强反驳、范式自觉等 |
| `reviewer-personas.md` | 四类审稿人视角画像 |
| `top-journal-aesthetic.md` | 顶刊审美标准：问题意识、理论贡献、学术位置 |
| `rejection-patterns.md` | 六类典型退稿模式（R1–R6） |
| `output-template.md` | 审稿意见输出模板 |
| `socio-legal-integration-module.md` | 社会科学融入教义学的专项审查模块（按需启用） |

## 输出

审稿意见严格按 `output-template.md` 的十个部分输出：范式定位 → 编辑初审判断 → 最强反驳 → 致命问题 → 重大问题 → 轻微问题 → 替代解释路径 → Frame Lock 检测 → 顶刊发表价值判断 → 最终审稿意见。

## 学术诚信声明

本 Skill 的定位是**评审工具**，模拟同行评议中审稿人的角色：

- 输出的是对论文的**批评性诊断**，不是修改后的文本；
- 不代写、不改写论文任何部分；
- 是否采纳意见、如何修改，完全由作者决定并执行。

请在使用时遵守你所在机构的学术规范与 AI 使用政策。
