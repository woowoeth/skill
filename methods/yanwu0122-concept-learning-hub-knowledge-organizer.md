---
name: knowledge-organizer
description: 知识库管家——把新素材自动归纳入 concept-learning-hub 个人知识库。当用户说「把……加入知识库 / 整理进笔记库 / 收一下这些资料 / 我往 inbox 里放了东西帮我归类 / 学一个新概念并归档 / 添加学习笔记」等，且目标是本仓库的 learning-materials 时使用。职责：理解素材 → 识别所属领域 → 判断归入已有笔记还是新建 → 生成/整理笔记 → 登记 catalog.json → 重建 hub.html 门户 → 更新索引 → 自检 → 提交推送。
---

# Knowledge Organizer · 知识库管家

本 Skill 服务于 `concept-learning-hub` 仓库，把任意学习素材（网页、文章、课件、PDF 摘录、随手记录、GitHub 项目）**自动识别领域、分门别类**地收进知识库，保证库内「可搜索、可复习、可持续」。

## 知识库结构（先读这些文件了解现状）

| 文件 | 作用 |
|------|------|
| `learning-materials/catalog.json` | **数据真源**：领域清单 + 每份笔记的登记卡（领域/标签/摘要） |
| `learning-materials/hub.html` | 交互式门户（由 `rebuild_hub.py` 生成，**勿手改数据部分**） |
| `learning-materials/README.md` | 笔记清单与新增规范 |
| `inbox/` | 素材投递口：用户把原始资料放这里，等你处理 |
| `.workbuddy/skills/concept-learning-generator/` | 概念型内容的生成器（本 Skill 会调用它） |

## 输入信息

- 素材来源：`inbox/` 目录下的文件、用户粘贴的文本/链接、或用户口头描述
- 可选偏好：用户想放入的领域（不指定则由你判定）
- 输出位置：概念页 → `learning-materials/<概念>.html`；通用素材笔记 → `learning-materials/<slug>.md`

## 领域分类体系（识别后归类依据）

| domain | 领域 | 收录什么 | 判定关键词示例（仅供启发，须读内容确认） |
|--------|------|---------|--------------------------------|
| `llm` | 大模型与生成式 AI | 模型本体、上下文、提示词、RAG、微调、评估 | 大语言模型、LLM、Transformer、Token、上下文窗口、RLHF、幻觉、RAG、prompt |
| `agent` | 智能体与自动化 | Agent、工具调用、Skill、工作流、多智能体 | Agent、智能体、工具调用、Skill、技能包、工作流、MCP、函数调用 |
| `ml-basics` | 机器学习基础 | 机器学习/深度学习基础 | 机器学习、神经网络、损失函数、反向传播、过拟合、CNN |
| `engineering` | AI 工程与工具 | Git、检索、部署、评测、产品化 | Git、版本管理、评测、部署、API、向量数据库 |
| `general` | 通用与未分类 | 暂无法归类的先放这里 | — |
| `overview` | 知识地图（保留给总览/关系页） | 只登记关系说明类页面 | — |

**判定规则**：先读素材**内容**再下结论，不许只看文件名猜。拿不准 → 归 `general`，并在总结中提示用户后续细化。

## 入库流程

### 步骤 1：理解素材
- 逐个读取 `inbox/` 或用户提供的素材（网页用 WebFetch、文件直接读）。
- 提炼：核心主题是什么？属于「概念型」（适合做成标准概念页）还是「素材型」（一篇笔记/文章摘录）？

### 步骤 2：识别领域与查重
- 对照上表判定 `domain`。
- 读取 `learning-materials/catalog.json`，检查是否已有同主题笔记：
  - **已有** → 优先把新内容**并入**该笔记的对应小节（更新 summary/标签），不要制造重复页；
  - **没有** → 走步骤 3 新建。

### 步骤 3：生成 / 整理笔记
- **概念型**：加载 `concept-learning-generator` Skill，按其完整流程调研并渲染 `learning-materials/<concept>.html`（七大结构：学习目标/核心问题/个人解释/核心机制/应用场景/概念辨析/自测+来源）。
- **素材型**：整理成一份结构清晰的 Markdown 笔记存到 `learning-materials/<slug>.md`（标题、一句话主题、要点分节、个人理解、来源），slugs 全小写、连字符分词。

### 步骤 4：登记 catalog.json（分门别类的关键一步）
在 `entries` 数组**新增或更新**对应条目（overview 类页面保持 type=overview）：
```json
{
  "id": "概念英文id",
  "title": "中文标题",
  "type": "concept",
  "file": "learning-materials/<文件名>",
  "domain": "llm",
  "tags": ["中文标签1", "中文标签2"],
  "summary": "一句话主题（20~40字，能被搜索命中）",
  "added": "YYYY-MM"
}
```
- `added` 首次收录写 `YYYY-MM`；**更新已有条目时不要覆盖别人的 added**（如需记录修订可在 summary 体现）。
- 若确需新领域：先在 `domains` 注册（id 全小写英文、name/emoji/color/desc），再使用。
- 保持 JSON 合法：改动后必须用 `python -m json.tool learning-materials/catalog.json` 校验。

### 步骤 5：重建门户
```bash
python .workbuddy/skills/knowledge-organizer/scripts/rebuild_hub.py
```
该脚本读取 catalog.json，重新生成 `learning-materials/hub.html`（领域分区卡片 + 搜索 + 随机复习），保证门户与登记册一致。

### 步骤 6：更新索引
- `learning-materials/README.md` 的「笔记清单」表加/改一行；如新增领域，在表中或说明中同步。
- 若仓库根 `README.md` 的资料表格也列了笔记，一并更新（新增门户行只需一次）。

### 步骤 7：自检
1. catalog.json 是合法 JSON，且 `id` 无重复；
2. 每份新笔记文件真实存在、内容不是整段照搬素材原文；
3. hub.html 已重新生成，本地双击能打开、新卡片可见、链接能跳转到对应笔记；
4. `inbox/` 中已处理完的素材已清空或移走（保留空目录 + README 即可）；
5. 无密钥/隐私内容被纳入。

### 步骤 8：提交与推送
```bash
git add -A
git commit -m "docs(kb): 新增 <概念/笔记名>（领域：<domain>）并更新知识库门户"
git push origin main
```
网络不稳时：先用 `curl -s -o /dev/null -w '%{http_code}' https://github.com/` 探测到 200 再推，失败可挂自动重试循环（每 10 秒探测一次，恢复即推）。推送后 `git ls-remote origin main` 核对远端 HEAD 与本地一致。

## 输出

一份（或多份）归好类、登记在册的笔记 + 更新后的门户 hub.html + 提交记录。向用户总结：新增/更新了什么、归到了哪个领域、为什么这样归类（一句话）、搜索/复习入口在哪。

## 与 concept-learning-generator 的分工

- `concept-learning-generator`：负责「概念 → 结构化 HTML」的内容生产。
- `knowledge-organizer`：负责「素材 → 领域识别 → 归类入库 → 登记 → 门户」的库管理。
- 两者协作：用户说「学一个新概念」，先由 organizer 判定领域与查重，再调 generator 生产，最后 organizer 完成登记与门户更新。
