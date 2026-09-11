---
name: career-learning-exam
description: 根据用户职业或技能目标生成 HTML 学习路径与带具体学习链接的模块明细课件，在学完后出 HTML 试卷、Rubric 阅卷并输出 HTML 成绩报告；支持补考与进度持久化。在用户要学某技能、做某工作、要学习计划、能力测评、结业考试、补考，或询问某岗位该学什么时使用。不用于软件测试用例或单次知识点答疑。
---

# 职业/技能学习与考试

## 何时使用

- 用户想系统学习某职业或技能（如 PHP 开发、前端、数据分析）
- 用户要求学习计划、学习路径、该学什么
- 用户学完要求出题、考试、测评、阅卷
- 用户提交答案要求判定是否通过，或要求补考
- 用户 `@` 引用 `.cursor/learning/{goal-slug}/` 下文件继续学习/考试

## 何时不用

- 单次知识点问答（直接回答即可）
- 从需求文档生成软件测试用例（用 `generate-testcases`）
- 用户只要资源推荐、不要路径与考试

## 产物格式（必须 HTML）

**用户可见交付物一律为 HTML 文件**，在浏览器中打开阅读。规范见 [reference/html-guide.md](reference/html-guide.md)。

| 阶段 | HTML 产物 | Agent 专用（非 HTML） |
|------|-----------|----------------------|
| PLAN | `{goal-slug}/index.html` + `modules/m{x}-*.html`（模块纲要） | `state.json` |
| STUDY | 深化 `modules/m{x}-*.html`（练习+自检题） | 更新 `state.json` |
| EXAM | `exams/exam-{id}.html` | `exams/exam-{id}-rubric.md` |
| GRADE | `results/result-{id}.html` | 更新 `state.json` |

首次创建 workspace 时，从本 skill 的 [assets/style.css](assets/style.css) 复制到 `{goal-slug}/assets/style.css`。

## 状态机

每次交互先判断阶段，**同一轮只做一件事**：

| 阶段 | 触发 | 动作 |
|------|------|------|
| `PLAN` | 新目标 / 无 workspace | 生成 `index.html` + 初始化 workspace |
| `STUDY` | 展开模块 / 答疑 / 练习 | 生成模块 HTML（不出完整卷） |
| `EXAM` | 开始考试 / 出题 / 补考 | 生成试卷 HTML（无答案） |
| `GRADE` | 提交答案 / 阅卷 | 生成成绩 HTML |

恢复上下文：`state.json` > 用户 `@` HTML > 对话中 `learning-state` 注释 > 询问用户。

## 阶段 PLAN：生成学习路径

### 输入

- **目标**：岗位或技能（必填）
- **可选**：当前水平、时间预算、目的（就业 / 转行 / 兴趣）、考试模式（`full` / `gate`，默认 `full`）

### 学前诊断（可选，≤5 题）

零基础或目标模糊时，先 3–5 道极短诊断或让用户自评。已有明确水平则跳过。

### 岗位类型

| job_type | 典型目标 | 考试配比（选择:简答:实操） |
|----------|----------|---------------------------|
| `programming` | 开发、运维脚本 | 25:25:50 |
| `theory` | 会计、法务、理论岗 | 40:45:15 |
| `mixed` | 产品、数据分析 | 30:40:30 |

不确定时按 `mixed`。模块骨架见 [reference/roles.md](reference/roles.md)。

### 输出规则

- 创建 `.cursor/learning/{goal-slug}/` 及 `assets/`、`modules/`、`exams/`、`results/`
- 写入 `index.html`：**`.hero` 统计区**、能力目标、模块总览表（`.table-wrap`）、**每模块 `.module-outline` 明细卡片**（含 `.module-header` 与 3 条精选链接）、里程碑、下一步、免责声明
- **同时为每个模块生成** `modules/m{x}-*.html` **纲要页**：学习目标、知识点明细、**完整资源链接表**（4–8 条真实 URL）、建议学习顺序
- 写入 `state.json`（含 `modules_generated: true`）
- 链接规范见 [reference/learning-resources.md](reference/learning-resources.md)；不确定时用 WebSearch 核实后再写入
- 对话中**仅摘要 + 文件路径**，不粘贴 HTML 全文
- 生成后尝试 `start "" "{index.html 绝对路径}"` 打开浏览器

用户说「展开 Mx」或「深化 Mx」进入 STUDY，在已有纲要页上追加练习、常见误区与 3 道自检题。

## 阶段 STUDY：模块深化与练习

- 读取已有 `modules/m{x}-*.html`；若无则按 PLAN 纲要规范先生成
- **追加**：常见误区、1–2 个练习任务（含验收标准）、3 道自检题
- 纲要页已有的知识点与资源链接可补充，勿删除已有有效链接
- 自检题不得原样用于结业考
- 更新 `state.json`（`phase: STUDY`，记录 `modules_studied`）；禁止出完整结业卷

## 阶段 EXAM：出题

基于 `state.json` 中的模块列表，生成 `exams/exam-{id}.html` 与 `exams/exam-{id}-rubric.md`。

### 试卷规则

- 总题 15–25 道，满分 100；覆盖所有模块；核心模块题量 ≥ 40%
- 难度：基础 40% / 中等 40% / 进阶 20%
- 考试题映射模块知识点，**不得与自检题原题相同**
- HTML 试卷：每题 `.question` 区块；选择题用 `.options`；简答/代码题用 `<textarea class="answer-area">`
- Rubric 与参考答案**只写入** `-rubric.md`，**禁止**出现在 HTML 试卷中

### 整卷 vs 闯关

- `full`：一次出全卷 HTML
- `gate`：每次只出当前模块 3–5 题 HTML，该模块 ≥80% 解锁下一模块

Rubric 格式见 [reference/rubric-examples.md](reference/rubric-examples.md)。

## 阶段 GRADE：阅卷与判定

按 `-rubric.md` 评分，生成 `results/result-{id}.html`。

### 通过条件（同时满足）

1. 总分 ≥ 80
2. 每个核心模块 ≥ 60%
3. 无大题（≥8 分）得 0 分

### 成绩 HTML 须含

- **`.score-hero`**：大号总分、结论 badge（pass / fail）
- 模块得分表（`.table-wrap`）与 score-bar
- 逐题得分与解析
- 未通过：复习清单 + 补考说明（最多 2 次补考）
- 通过：后续进阶建议

## 对话回复格式

1. 简短摘要（阶段、做了什么、结论若已阅卷）
2. 生成的 HTML 绝对路径（可点击）
3. 下一步操作提示
4. HTML 注释块（与 `state.json` 同步，降级恢复用）：

```html
<!-- learning-state
goal: php-backend
phase: PLAN
job_type: programming
modules: [M1,M2,M3,M4,M5,M6]
core: [M2,M3,M4]
exam_mode: full
attempt: 0
-->
```

## 质量自检

- [ ] 用户可见产物均为 HTML，引用 Google Fonts + `assets/style.css`，无 inline style
- [ ] `index.html` 含 `.hero` + `.stats`；`results/*.html` 含 `.score-hero`
- [ ] 表格用 `.table-wrap` 包裹；模块卡片含 `.module-header` + `.module-id`
- [ ] PLAN 已为每个模块生成纲要 HTML，且每模块 ≥4 条可点击真实学习链接
- [ ] `index.html` 含每模块 `.module-outline` 与链到对应模块页
- [ ] 试卷 HTML 无答案；Rubric 仅在 `-rubric.md`
- [ ] `state.json` 与 learning-state 注释已同步
- [ ] 对话未重复粘贴 HTML 全文
- [ ] 考试题与自检题无原题复用
- [ ] 结论明确，未使用「官方认证」表述

## 参考

- HTML 规范：[reference/html-guide.md](reference/html-guide.md)
- **学习链接与模块明细**：[reference/learning-resources.md](reference/learning-resources.md)
- 样式表：[assets/style.css](assets/style.css)
- 岗位模板：[reference/roles.md](reference/roles.md)
- Rubric 示例：[reference/rubric-examples.md](reference/rubric-examples.md)
- 流程示例：[examples.md](examples.md)
