---
name: agent-model-router
description: 列出 provider、选择模型、启动多个 agent 时必须使用。触发词：列出 provider、有哪些模型、选择模型、启动多个 agent、并行、多个专家、多维度、分别评估。
when_to_use: 只要用户要启动 2 个或以上 Agent/子智能体，无论措辞如何，都必须先弹出 AskUserQuestion 让用户为每个 Agent 选择 provider 和模型，再启动 Agent。
---

# ⚠️ 强制规则

**只要用户要启动 2 个或以上 Agent/子智能体，必须先执行本技能的步骤，禁止跳过直接启动 Agent。**

## 步骤 1：获取可用 Provider

运行此技能目录下的 `scripts/router.py` 脚本：

```bash
python scripts/router.py list
```

## 步骤 2：弹出选择界面

使用 `AskUserQuestion` 工具为每个 Agent 让用户选择 provider 和模型。选项中标注排行榜排名（如"文本第1"、"代码第5"）帮助用户决策。

## 步骤 3：使用选择结果启动 Agent

根据用户选择，启动 Agent 时在 prompt 中指定 provider 和模型。

## 其他命令

| 命令 | 说明 |
|------|------|
| `python scripts/router.py search <关键词>` | 搜索模型 |
| `python scripts/router.py rankings` | 查看排行榜 |

详细排行榜数据见 `references/model-rankings.md`。
