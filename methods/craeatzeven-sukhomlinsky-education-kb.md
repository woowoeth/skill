---
name: sukhomlinsky-education-kb
description: 按教育主题检索苏霍姆林斯基教育思想与案例的纯 Markdown 知识库。用于回答“苏霍姆林斯基怎么看后进生/家校合作/劳动教育/美育/教师成长”等问题，或按主题阅读带出处的思想与案例。先读 INDEX.md，再进入 topics/ 与 cards/。
---

# Sukhomlinsky Education KB — Agent 入口

这是一个**可移植的纯 Markdown 知识库**，不是本地私有笔记。任何支持 `SKILL.md` 的 agent（Codex / Claude / Hermes / skills.sh / 通用工具）都可以把它作为技能加载。

## 路由规则（Agent 必读）

1. **先读 [`INDEX.md`](INDEX.md)**，不要直接凭记忆回答。
2. 用户问某个教育主题（如“后进生”“家校合作”）→ 读对应 `topics/<slug>.md`。
3. 用户问某条具体观点/案例的出处 → 从主题页或 INDEX 找到 `cards/<id>.md`，按 `source` + `ref` 核验。
4. 用户要求扩展新主题 → 遵循 [`docs/production-guide.md`](docs/production-guide.md) 与 [`schemas/README.md`](schemas/README.md)，不得无源添加内容。

## 内容纪律

- 引用原文时只做短摘录，并保留 `ref` 出处。
- 中文转述、注释、应用建议必须与原文/出处分离呈现。
- 未挂卡片的断言只能作为“编辑者建议”，不可冒充苏霍姆林斯基原意。
