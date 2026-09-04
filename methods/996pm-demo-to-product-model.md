---
name: demo-to-product-model
description: 将产品 Demo 开发资料、迭代沟通、git commit 和 Demo 代码逆向为可审阅的 Product Model。用于从 Demo 抽取页面、功能、字段、状态、流程、数据、权限、冲突和待确认问题；不负责一次性生成完整 PRD 或原型，后续可交给 product-model-to-prd。
---

# Demo to Product Model

## 使用时机

当用户提供产品 Demo 代码、运行地址、开发提示资料、迭代沟通记录或 git commit，并希望从 Demo 逆向产出结构化产品资料、PRD 输入、页面清单、状态机、数据字典、权限矩阵、缺口清单时，使用本 skill。

本 skill 的输出可单独使用，也可作为 `product-model-to-prd` 的输入。

## 核心原则

* 不直接生成完整 PRD 和原型。
* 先做产品事实抽取，再生成可审阅的 Product Model。
* 每轮只创建、编辑或追加一个交付文档，避免一次性长输出。
* 每个结论必须标注来源：`已实现`、`已确认`、`合理推断`、`建议补充`、`待确认`、`不纳入本期`。
* 代码和运行 Demo 是最高优先级事实源；沟通记录和需求资料用于解释意图；推断内容不能伪装成事实。
* 遇到高风险缺口时暂停，向用户索要确认或让用户审阅阶段产物。

## 推荐工作目录

在用户指定的项目目录下创建：

```text
.product-model/
    00-input-inventory.md
    00-agent-prompts.md
    01-demo-facts.md
    02-change-log-analysis.md
    03-product-model.md
    04-gaps-and-questions.md
    05-coverage-report.md
    product-model.json
```

## 执行流程

### Step 0：初始化工作区

使用 `scripts/init_workspace.py` 创建 `.product-model/` 和模板文件。只初始化，不填充详细内容。

### Step 1：资料盘点

只编辑 `00-input-inventory.md`。

必须输出：

* 已获得资料
* 资料路径或来源
* 覆盖度评估
* 关键缺口
* 需要用户补充的资料

完成后停止，提示用户审阅或继续。

### Step 1A：自动提取当前项目开发提示输入

只创建或覆盖 `00-agent-prompts.md`。

如果用户没有显式提供完整开发提示资料，直接运行一次 `scripts/extract_agent_prompts.py <当前产品 Demo 项目路径>`。这一步不需要 Agent 自己读取会话文件、判断会话结构或浏览历史记录；脚本会按当前项目路径匹配 WorkBuddy、Codex 和 Claude Code 的本机会话，只输出用户提示词摘要。

不要直接把 Claude Code、Codex、WorkBuddy 等产品的完整会话 JSON/JSONL 读进上下文，也不要把完整会话内容复制进 `00-agent-prompts.md`。

`00-agent-prompts.md` 只保存：

* 用户输入摘要
* 必要的短摘录
* 来源文件路径
* 未能自动获取的原因

默认覆盖：

* WorkBuddy：根据当前项目路径编码匹配 `~/.workbuddy/projects/{项目路径编码}/**/*.jsonl`，提取 `<user_query>...</user_query>` 标签内的内容。
* Codex：扫描 `~/.codex/archived_sessions/**/*.jsonl` 和 `~/.codex/sessions/**/*.jsonl`，用 `cwd` 匹配当前项目路径，提取 `payload.type=user_message` 的文本。
* Claude Code：根据当前项目路径编码匹配 `~/.claude/projects/{项目路径编码}/*.jsonl`，提取 `type=user` 且 `message.content` 为字符串的内容；非字符串内容通常是工具调用或工具结果，不提取。

如果脚本未找到相关记录，只在 `00-agent-prompts.md` 记录“未能自动获取”，不要编造开发提示；后续以 Demo 代码、运行效果、需求资料和 git commit 继续分析。

### Step 2：Demo 产品事实抽取

只编辑或追加 `01-demo-facts.md`。

必须抽取：

* 路由与页面
* 组件与页面区块
* 按钮和操作
* 表单字段和表格列
* API、mock、schema、类型定义
* 状态变量和条件渲染
* 页面跳转
* 弹窗、抽屉、Toast、确认框
* 已实现的空态、加载态、错误态、成功态
* 权限判断和本地存储

大型项目分多轮处理：每轮只分析一个模块、一个目录或一组相关页面。

### Step 3：需求演进分析

只编辑 `02-change-log-analysis.md`。

分析需求资料、沟通记录和 git commit，识别：

* 重要需求变更
* 功能增删
* 交互调整
* 被废弃或推迟的需求
* Demo 与资料冲突
* 仍未完成的需求

### Step 4：生成 Product Model

只编辑 `03-product-model.md` 和必要时的 `product-model.json`。

Product Model 必须包含：

* 产品概述
* 用户角色
* 使用场景
* 信息架构
* 页面模型
* 功能模型
* 数据模型
* 状态机
* 页面流
* 权限矩阵
* 规则模型
* 异常与边界条件
* 待确认问题

### Step 5：缺口与待确认

只编辑 `04-gaps-and-questions.md`。

重点识别：

* 状态机缺口
* 权限缺口
* 数据校验缺口
* 异常态缺口
* 核心流程终态缺口
* 高风险操作缺口
* Demo 与需求冲突

完成后暂停，要求用户确认优先级高的问题。

### Step 6：覆盖校验

只编辑 `05-coverage-report.md`。

必须检查：

* Demo 页面 → Product Model 页面
* Demo 操作 → Product Model 功能或页面操作
* Demo 字段 → 数据字典或页面字段
* Demo 状态 → 状态模型或缺口清单
* Demo 跳转 → 页面流

## 脚本

* `scripts/init_workspace.py`：初始化工作区和模板文件。
* `scripts/extract_agent_prompts.py`：按当前项目路径匹配 WorkBuddy、Codex、Claude Code 本机会话，流式提取用户提示输入，输出 `00-agent-prompts.md`；只写用户输入摘要和必要摘录，不写完整会话。
* `scripts/scaffold_product_model.py`：从结构化 JSON 草案生成 Product Model Markdown 骨架。
* `scripts/coverage_check.py`：基于简单 JSON 输入生成覆盖校验 Markdown。

## 模板索引

* `templates/input_inventory.md`
* `templates/agent_prompts.md`
* `templates/demo_facts.md`
* `templates/change_log_analysis.md`
* `templates/product_model.md`
* `templates/gaps_and_questions.md`
* `templates/coverage_report.md`

## 质量门禁

进入下一个 skill 前，应满足：

* 页面清单覆盖 Demo 页面。
* 操作清单覆盖主要可交互元素。
* 字段清单覆盖表单、表格、详情展示字段。
* 状态清单区分业务状态与 UI 状态。
* 高风险推断进入待确认清单。
* Product Model 可以被用户审阅，而不是只存在于对话中。

## 与下游 skill 串联

当用户需要继续生成 PRD 时，将以下内容交给 `product-model-to-prd`：

* `.product-model/03-product-model.md`
* `.product-model/product-model.json`，如果存在
* `.product-model/04-gaps-and-questions.md`
* `.product-model/05-coverage-report.md`

当 PRD 已完成并需要生成原型时，再将 PRD 产物交给 `prd-to-prototype`。
