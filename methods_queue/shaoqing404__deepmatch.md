---
name: deepmatch
description: 面向求职者的岗位描述深度调研与证据化匹配技能。用于引导应届生、求职新手或转岗者完成个人信息采集、当前简历澄清、岗位录入、公司与岗位调研、证据标签化匹配、是否值得投递判断、面试准备、能力摸底、补完计划和多轮面试迭代，尤其适合人工智能、解决方案、产品工程、智能体、工作流、应用交付等复杂岗位。
---

# DeepMatch

DeepMatch 帮助用户判断一个岗位是否值得投入，以及应该如何准备。它是 Markdown 优先的流程技能，不是在线服务、简历生成器或通用面试话术库。

应用人工智能设计内核：暴露不确定性、来源、置信度和用户控制权。区分检索事实与模型推理。

## 启动步骤

1. 识别当前人工智能编程环境：
   - Codex：使用 Codex 工具；如需委派调研或子任务调研，遵守当前 Codex 委派协议。
   - Claude Code：可用时使用工作流模式或子任务式调研。
   - 其它工具：按 Markdown 串行执行。
2. 创建或定位本地 `workspace/`。永远不要提交用户工作区数据。
3. 从 `templates/` 复制需要的模板。
4. 阅读 `references/input-contracts.md` 和 `references/workflow.md`。
5. 持续反问，直到 `PROFILE.md`、`RESUME.md` 和目标 `JOB_JD.md` 足够可用。

## 必需输入

DeepMatch 需要两类候选人材料：

- `PROFILE.md`：简历无法充分表达的个人信息，包括动机、限制、工作方式、优势、弱信号、职业方向、当前处境和需要反问的不明确部分。
- `RESUME.md`：用户当前简历，是高度压缩的公开职业材料。

每个岗位还需要：

- `JOB_JD.md`：岗位来源平台、公司、岗位名、地点、薪资范围、职责、要求、用户兴趣程度和面试时间线。

如果输入不完整，继续建立 `已知 / 缺失 / 假设` 小节，并提出高影响问题。

## 证据标签

所有调研和匹配报告都使用这些标签：

- `retrieved_fact`：来自岗位描述、公司官网、公告、新闻、招聘页或公开资料
- `candidate_claim`：来自用户、简历、作品集或个人信息
- `inference`：基于证据推理得出，但来源没有直接说明
- `needs_verification`：合理但证据不足，需要继续验证

## 工作流程

1. 个人信息：在 `PROFILE.md` 中建立非简历语境，对模糊、压缩、高影响信息进行充分反问。
2. 当前简历：在 `RESUME.md` 中保存简历，默认它不完整，需要个人信息补充解释。
3. 岗位录入：为每个岗位创建目录并填写 `JOB_JD.md`。
4. 调研计划：联网前先写 `RESEARCH_PLAN.md`。
5. 深度调研：写 `COMPANY_ROLE_REPORT.md`，包含来源、日期、置信度和不确定性。
6. 匹配判断：写 `MATCH_REPORT.md`，包含评分、风险、匹配结论和是否值得冲。
7. 面试准备：写 `INTERVIEW_PREP.md`；能力摸底第一轮不得提前给答案。
8. 面试证据输入：用户提供或确认后的文本化面试证据（转写、模型建议、用户复盘、模拟/TTS、招聘方沟通）归档到 `INTERVIEW_EVIDENCE.md`；先处理失败状态，再更新准备材料。
9. 持续迭代：在招聘沟通、初面、技术面、业务面、终面、录用、拒绝或放弃后更新 `ITERATION_LOG.md`。

## 参考文档

按需读取：

- `references/input-contracts.md`：启动条件、全部输入、缺失处理和不可直接给强结论的情况。
- `references/workflow.md`：完整流程和工作区状态。
- `references/tool-routing.md`：Codex、Claude Code 和其它工具的执行方式。
- `references/deepsearch-playbook.md`：调研问题、搜索对象和来源标准。
- `references/matching-rubric.md`：评分维度和推荐逻辑。
- `references/interview-iteration.md`：面试准备和多轮迭代。
- `references/evidence-confidence.md`：证据标签、置信度和失败处理。

## 输出规则

每次岗位分析都必须以这些内容收尾：

- 建议：`strong pursue`、`selective pursue`、`low priority` 或 `avoid`
- 置信度
- 前三条理由
- 前三条风险
- 接下来三步行动

如果置信度低，优先输出验证清单，而不是给出武断结论。
