---
name: human-writing-l2
description: 中文商业网文自然成文与局部去模型化 Skill。基于旧 human-writing 1.9.0-L2 锁定核心重做；第一稿从源头抑制过度完成，返修只处理明确病灶。已接入 Writer Runtime 主链。
---

# Human Writing L2｜v0.2

> status: integrated
> production_wired: true
> integration_host: `skills/story-writer-runtime/SKILL.md`
> framework_mutation: AUTHORIZED_BY_KQ
> story_authority: NONE
> canon_authority: NONE
> tracking_authority: NONE
> previous_frozen_version: `versions/v0.1/`

## 0. 定位

这不是“检测 AI 词然后替换”的工具。

它只解决一件事：

> **让中文商业网文不要被模型的“完整、漂亮、对称、解释到底”冲动加工成施工稿。**

v0.2 在 v0.1 的五条 L2 原则之上新增一个总原则：

> **Completion Variance｜完成度波动。**

真人感不来自故意写残，而来自不同信息、情绪、动作、对白和段落的完成程度天然不一致。有的内容完整说明，有的只给结果；有的情绪直接说，有的让动作或对白承担；有的问题马上处理，有的只处理到足以继续行动的位置。

```text
LOCAL_COMPLETENESS: VARIABLE
UNIFORM_COMPLETENESS: UNDESIRED
```

不要为了制造“波动”故意加停顿、错字、病句、碎片对白、随机犹豫或无来源动作。

它不负责：

- 设计剧情；
- 重排事件；
- 修改人物核心；
- 补世界观；
- 补钩子；
- 改 Tracking / Canon；
- 全章统一润色；
- 为了检测率重写正文。

## 1. 两种模式

### FIRST_DRAFT

用于第一次把已经批准的当前章故事输入写成正文。

必读：

1. `references/l2-core.md`
2. `references/web-fiction.md`
3. `references/positive-writing.md`

第一稿禁止读取 `references/local-revision.md` 作为逐项自检表，也禁止为了“去 AI 味”在完成后自动再洗一遍全文。

### LOCAL_REVISION

仅当作者或上游 Reviewer 已给出：

- 具体位置；
- 具体问题；
- 最小修复目标；

才进入。

必读：

1. 当前原稿；
2. 明确 defect list；
3. `references/local-revision.md`；
4. 按需回看 `l2-core.md` / `web-fiction.md`。

只修命中区域及必要相邻内容。健康部分不顺手优化。

## 2. L2 五条核心原则

以下五条保持 v0.1 原义不变，由“完成度波动”统一解释，而不是被替换。

### 2.1 不做连续的漂亮闭合

不要让正文反复出现：

```text
铺垫
→ 对称短句
→ 总结
→ 小落点
→ 空行
→ 再来一次
```

短句、好句、落点都允许，但不能成为稳定流水线。

### 2.2 新信息不要一次推演到底

人物得到新规则、新能力、新异常、新数字时，不自动补齐：

```text
事实
→ 用途
→ 战略价值
→ 长期路线
→ 未来计划
```

人物只想到当前够用的位置即可。

### 2.3 认知颗粒不统一

有的事情多想几句，有的看见就过去；有的判断重复一下，有的直接成立。

不要把整章所有认知加工成相同长度、相同完整度、相同证明强度。

### 2.4 段落自然形成

段落不是“一条语义一个段落”。

同一人物、同一注意对象、同一时间地点、同一局部目的下的动作、观察、心理、对白后的自身动作、补充说明与短因果可以共居。

普通新信息本身不是换段理由。

### 2.5 允许普通和局部毛边

正文不要求句句有力、段段漂亮、处处完成。

允许普通词、普通连接、局部重复、不均匀注意力、没有专门落锤的段尾。

但不故意制造错字、病句、随机口语、降智、无来源动作来模拟真人。

## 3. 商业网文的“不完整权限”

允许：

- 问题不当场回答；
- 误会不马上澄清；
- 试探没有结论；
- 人物知道不对但先不处理；
- 人物只想一半；
- 对白答偏、敷衍、没接住全部问题；
- 一个主要变化托住一章；
- 证据不全部集齐；
- 人物已经够行动时停止证明；
- 事情只解决一半就切章。

核心：

> **故事底下可以闭合，正文表面不要处处闭合。**

补充：

> **Interaction Completion != Semantic Completion**

一次交流已经完成，不代表人物必须把自己的立场、原因、情绪和结论全部说完。对白只需要完成当前的人际动作。

## 4. Truth / Boundary

本 Skill 没有故事修改权。

必须保持：

- 已批准事件结果；
- 人物知识边界；
- 数字 / 能力 / 物品状态；
- 已批准因果；
- 章尾 stop；
- 禁止提前释放的信息。

如果“更自然”需要改变这些内容，停止修改并上报，不得自己圆。

## 5. 第一稿停止条件

正文自然完成当前章要求后立即停止。

不得自行执行：

- 全文 revision；
- AI 症状扫描后逐项修；
- 段落统一整理；
- 同义词替换；
- 检测率优化；
- 下一章规划。

## 6. 局部返修停止条件

命中病灶被修到不再影响阅读，同时 Truth / Boundary 未改变，即停止。

返修优先考虑：

```text
DELETE
STOP EARLIER
COMPRESS
MERGE
FLATTEN
```

不要先重写成另一句更“像人”的漂亮话。

不把一个局部问题扩张成全章重写。

## 7. 生产接入状态

当前 Skill 已由 KQ 明确批准接入：

```text
skills/story-writer-runtime/SKILL.md
```

生产路由：

```text
无 REVISION.md
→ FIRST_DRAFT

存在 REVISION.md
→ 先读 defect
→ 只有正文自然度 / 过度完成类问题才进入 LOCAL_REVISION
```

现有 `anti-ai-writing`、`banned-words` 与相关检测脚本继续保留，但默认作为按需诊断与局部修复辅助，不再要求每章写完自动全章清洗。

v0.1 已冻结保存在：

```text
skills/human-writing-l2/versions/v0.1/**
```

Writer Runtime 接入前原版已冻结保存在：

```text
skills/story-writer-runtime/versions/pre-human-writing-l2/SKILL.md
```

本 Skill 仍没有剧情、Canon、Tracking 或主仓库修改权限。