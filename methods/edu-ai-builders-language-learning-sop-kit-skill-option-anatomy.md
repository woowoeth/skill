---
name: skill-option-anatomy
description: 把英语阅读选择题（雅思/托福/中高考/考研/教材题）转化成可交互的"选项解剖器"HTML——让学生看见每个选项背后的出题逻辑、陷阱类型，并在多题练习后自动浮现学生的错题模式。当用户提供英语阅读题（原文+题干+选项+答案）、提到"陷阱分析""选项分析""distractor""出题逻辑""为什么选 X""为什么不选 Y""把这道题做成可视化""帮学生看清选项陷阱""error pattern""错题诊断"等场景时触发。也适用于：老师备课时把一份阅读练习卷转成学生可自学的交互工具、教研时拆解真题选项设计、给学生做错题集的诊断版本。本 skill 不只生成展示页，而是产出一个能持续追踪学生陷阱模式的练习系统。
---

# 选项解剖器 · Skill

把英语阅读选择题转化成可交互的"选项解剖器"HTML 练习系统。这套系统的核心命题：**让出题者的思维对学生显性化**——学生看到的不只是"选错了"，而是"你被哪类陷阱抓住了"。

## 这个 skill 是什么 / 不是什么

**是**：一个把"原始阅读题" → "教学法落地的可交互 HTML"的转换器
**不是**：自动生成新题、自动改编题目、自动出模拟卷

输入是老师手里已经存在的题。本 skill 的价值在于 **拆解和诊断**，不在于"造题"。

## 核心概念：陷阱类型学

英语阅读选择题（IELTS / TOEFL / 中高考 / 考研）的干扰项设计有相对收敛的几类陷阱。本 skill 内置以下 5 种类型 + 1 种正确答案模式：

| 编号 | 类型 | 中文名 | 触发信号 | 教学法对应 |
|---|---|---|---|---|
| 0 | correct | 同义改写 | 词换、限定词保留 | safe paraphrase |
| 1 | trap-1 | 范围扩大 | all / every / always / never / regardless | over-generalization |
| 2 | trap-2 | 细节偷换 | 时间/地点/数量/人物的关键词反转 | detail swap |
| 3 | trap-3 | 过度推断 | recommend / treat / prove / cure / cause | unwarranted inference |
| 4 | trap-4 | 因果倒置 / 张冠李戴 | A 的属性安到 B，correlation 说成 causation | property mis-assignment |
| 5 | trap-5 | 比较关系偷换 | 原文 A>B 变成 A<B 或 A=B | comparison reversal |

判定一个选项属于哪类陷阱时，按以下优先级判断（**从特殊到一般**）：

1. 选项是不是和原文几乎一句话对应、只换了一两个具体名词（时间/地点/数量/人物）？ → **trap-2 细节偷换**
2. 选项是不是用了 all/every/always/never/regardless 等绝对量词，而原文有限定？ → **trap-1 范围扩大**
3. 选项是不是把 A 的属性说成 B 的属性，或把 correlation 说成 causation？ → **trap-4 因果倒置/张冠李戴**
4. 选项是不是把 A>B 反转或夷平成 A<B / A=B？ → **trap-5 比较关系偷换**
5. 选项是不是包含原文从未提到的概念、强承诺动词（recommend/cure/treat/prove）、或从原文事实推出的更强结论？ → **trap-3 过度推断**
6. 选项是不是只换词不换意思和范围？ → **correct 同义改写**

如果一个选项同时满足多条，按上面优先级取**最先满足的那条**作为主类型。原因：学生只能用一个标签反思自己的错误，必须给最有代表性的那个。

## 工作流（标准 5 步）

### Step 1: 接收和澄清输入

老师可能用以下任意一种方式提供题目：

- 纯文本粘贴
- 截图 / PDF
- 只给题没给原文
- 给了题但没给答案

**判断动作**：
- 如果**没有原文**：告诉老师"选项解剖器必须有原文片段，不然没法做陷阱分析。请补充对应的原文段落"。**不要硬撑着生成**，没有原文做出来的是假分析。
- 如果**没有答案**：可以自己判断答案，但生成后明确告诉老师"我判断 X 是正确答案，请你确认"。
- 如果是**截图/PDF**：先 OCR 或视觉读取，提取干净的文本结构，再进入 Step 2。

### Step 2: 解析题目结构

对每道题，抽出以下字段：

```
{
  meta: [考试类型, 题型, 难度估计],  // 例如 ['IELTS Reading', '细节题', '难度 ★★★☆☆']
  passage: 原文片段（要包含所有选项对应到的位置）,
  stem: 题干（如 "According to the passage, ..."）,
  options: [
    { letter: 'A', text: '...', isCorrect: false },
    ...
  ]
}
```

**关键判断**：原文片段要给得**完整**——所有 4 个选项各自对应到的原文位置都要包含进去。如果原文太长，至少要包含每个选项对应的那 1-2 句话。

### Step 3: 对每个选项做陷阱判定

对每个干扰项（非正确答案）做以下分析，按本 SKILL.md "陷阱类型学"小节的优先级判定：

```
{
  letter: 'A',
  verdict: 'trap' | 'correct',
  trapType: 1 | 2 | 3 | 4 | 5 | 0,  // 0 表示正确答案
  passageLink: '该选项对应到原文的哪一段',  // 用 id 标识
  analysis: {
    source: {
      text: '原文怎么说（用中文解释）',
      quote: '原文直接引用（英文原句）'
    },
    twist: {
      text: '选项怎么处理（中文解释扭曲在哪）'
    },
    chain: [
      { from: '原文词1', to: '选项词1' },
      { from: '原文词2', to: '选项词2' }
    ],
    hookText: '出题者想抓你哪个认知漏洞（中文）',
    train: '老师可以怎么训练学生避开这个陷阱（中文，具体可操作）'
  }
}
```

**chain 数组的设计原则**：
- 每一项是一次"词级扭曲"
- 对**正确答案**：列出"同义改写"的词对（如 consumption → intake）
- 对**陷阱选项**：列出"被偷换的关键词"（如 morning → evening）
- 通常 1-3 个词对就够；超过 3 个说明你在硬凑

**hookText 和 train 的写法**：
- hookText 不要写"这道题考察 X"——写"学生为什么会上当"
- train 必须是**可操作建议**：圈某类词、回原文做某个动作、形成某个反射

### Step 4: 标注高亮位置

为了让 HTML 能做"原文 ↔ 选项"同步高亮，需要标注：

**原文里**：用 `<span class="seg" data-seg="ID">...</span>` 包住每段会被某个选项对应到的内容。每段 seg 一个唯一 ID（如 'core' / 'timing' / 'caveat'）。

**选项里**：用 `{ t: '词', kw: 'twist-A' }` 标注被扭曲的关键词，用 `{ t: '词', kw: 'match-B' }` 标注正确答案的匹配词。命名规则：
- `twist-{letter}`：陷阱选项里被扭曲的词（会高亮成黄色 + 红色下划线）
- `match-{letter}`：正确选项里的同义改写词（会高亮成绿色）

每个选项的 `passageLink` 字段指向原文里对应的 seg ID。

### Step 5: 生成 HTML

读取 `assets/template.html`，把上面所有题目组装成 JavaScript 的 `QUESTIONS` 数组，替换模板里 `/* INJECT_QUESTIONS_HERE */` 标记，输出为最终 HTML 文件。

**多题打包规则**：
- 老师给的是同一份练习的多道题 → 打包成一个 HTML
- 老师给的是不同主题/不同来源的题 → 也可以打包成一个 HTML，但在 meta 里标注清楚
- 单题也可以生成 HTML，但错题模式仪表盘要等到 ≥3 题之后才有意义，可以提示老师"建议批量生成 3 道以上才能看出错题模式"

输出文件命名：`option-anatomy-{topic}.html` 或老师指定的名字。

## 完整示例

老师输入：

> 帮我把这道雅思题做成选项解剖器：
>
> 原文：Recent studies have shown that moderate caffeine consumption — defined as 200 to 400 milligrams per day — appears to improve short-term memory in healthy adults under 60. However, researchers caution that the effect diminishes significantly in older participants...
>
> Q: According to the passage, which is true about caffeine and memory?
> A. Caffeine improves memory in all adults regardless of age.
> B. Moderate caffeine intake can enhance short-term memory in younger healthy adults.
> C. Drinking caffeine in the evening produces the strongest memory benefit.
> D. Researchers recommend caffeine as a treatment for memory loss.
>
> 答案: B

Claude 的响应流程：

1. **Step 1**：原文 + 题 + 选项 + 答案齐全，进入 Step 2
2. **Step 2**：解析出 meta=['IELTS Reading', '细节题', '难度 ★★★☆☆']
3. **Step 3**：对四个选项做判定
   - A: 含 "all" + "regardless" → 优先级匹配 trap-1（范围扩大）
   - B: 正确，分析改写链 consumption→intake / improve→enhance / under 60→younger
   - C: morning 被换成 evening → trap-2（细节偷换）
   - D: 含 "recommend" + "treatment for memory loss" → trap-3（过度推断）
4. **Step 4**：原文标注 seg='core'（核心结论句）、seg='timing'（关于早上的句子）；A、C、D 的扭曲词分别标 kw
5. **Step 5**：注入模板，输出 option-anatomy-caffeine.html

读取 `assets/template.html` 获取完整模板结构。在 `assets/example-question.js` 里有一份完整的 question 对象示例，新手可以照着改。

## 边界与例外

**Skill 处理不了 / 应该转出去的情况**：

- **判断题（T/F/NG）**：本 skill 当前只处理 4 选项的选择题。如果老师给的是判断题，告诉老师"目前选项解剖器只支持 4 选项的题目，T/F/NG 题的陷阱分类不同（主要是'信息缺失'类陷阱），需要单独的工具"。
- **填空题 / 简答题**：完全不适用，告诉老师这不是选项解剖器的设计场景。
- **听力 / 口语题**：本 skill 是阅读题专用。听力题可以借用同样的陷阱类型学，但需要不同的 HTML 模板（带音频）。
- **题目质量明显有问题（如有两个正确答案、原文不充分）**：先告诉老师题目本身有问题，而不是硬生成。

**易判错的情况**：

- 一个选项同时是 trap-1 + trap-3（既范围扩大又有强承诺动词）→ 按优先级取 trap-1
- 选项里的"差异"看起来像是 trap-2（细节偷换），但实际是 trap-4（张冠李戴 A 和 B 的属性）→ 看是不是有"两个或更多概念被混淆"，有则是 trap-4
- 选项完全正确但是用词刁钻 → 还是 correct，不要为了"避免太简单"就把它判成陷阱

## 教学法依据（写给老师）

这套陷阱类型学不是我发明的。背后的研究脉络：

- **Test-wiseness research**（Millman, Bishop & Ebel, 1965 起的传统）：把"应试技能"作为一种可教的元认知能力
- **Distractor analysis**（Haladyna 的多选题设计研究）：从出题者视角分析干扰项的认知陷阱模式
- **Metacognitive scaffolding**（Schraw & Moshman 1995, Pintrich 2002）：让学习者**意识到**自己的认知陷阱，是迁移学习的关键

本 skill 把这些研究里的"陷阱模式"做成 **学生可见、可操作、可统计的认知工具**。这就是"教学法落地"的具体形态。

## 输出之后告诉老师什么

生成 HTML 之后，给老师以下信息：

1. **文件路径**：HTML 在哪
2. **每道题的陷阱分布概览**：让老师快速 sanity check"这题我判成 trap-1，你同意吗"
3. **使用建议**：
   - 给学生用之前，老师自己点一遍每个选项的解剖，确认教学法说明符合自己的判断
   - 学生练完之后，看顶部的"错题模式"，对学生最常踩的陷阱类型做针对性精讲
4. **可扩展提示**：如果题目数量少（<3 道），提示老师批量生成更多题才能让错题模式仪表盘有意义

## 设计细节备忘

- HTML 模板基于 EduOS 视觉系统（cream 背景 / dot-grid / hard shadow / Caveat 手写 + Space Mono 标签 + Noto Sans SC 正文）。**不要换风格**——视觉一致性是 EduOS 品牌资产的一部分。
- 错题模式仪表盘和陷阱类型学卡片默认是**折叠状态**。它们是"辅助参考"，不抢主流程。
- 选项卡片**初始视觉中性**——绝对不要在学生答题前给颜色 indicator。这是教学法核心：学生必须先做判断。
