# Judgment Engineering Skill

## Purpose

Use this skill when the user asks the AI to evaluate a claim, assess a trend, judge the reliability of information, compare competing explanations, make a forecast, or support a decision under uncertainty.

The goal is not to produce a fluent answer. The goal is to transform claims, information, and intuition into verifiable judgments.

In Chinese contexts, this skill is called：**判断力工程**。

---

## Core Principles

1. Do not turn the first reaction into the final judgment.
2. Classify the problem before answering.
3. Rewrite vague claims into verifiable questions.
4. Operationalize key concepts before using them.
5. Distinguish original sources, secondary sources, social signals, and AI summaries.
6. Maintain competing hypotheses instead of defending one explanation too early.
7. Search for counterevidence and failure conditions.
8. Express uncertainty using probabilities, ranges, or confidence levels.
9. Separate judgment quality from outcome quality.
10. Produce a judgment log for later review when the stakes are meaningful.

---

## When to Use

Use this skill for:

- claim evaluation;
- trend analysis;
- market, career, education, technology, product, or strategy judgment;
- article reliability review;
- information source audit;
- AI-generated answer verification;
- decision memo drafting;
- forecast and retrospective analysis.

Do not use this skill as a substitute for professional legal, medical, financial, or safety advice. For high-stakes domains, use it only to structure questions, evidence, assumptions, and risks.

---

## Problem Types

Classify the task into one or more types:

| Type | Description | Example |
|---|---|---|
| fact | Whether something happened or is true | Did the company announce this? |
| concept | Whether a concept is clear and useful | What does “consumption downgrade” mean? |
| forecast | What may happen in the future | Will AI reduce junior developer jobs? |
| value | What should be preferred | Should young people marry early? |
| action | What the user should do | Should I switch careers? |
| system | How a system or mechanism changes | How does AI reshape software teams? |

If the problem is mixed, say so explicitly.

---

## Mandatory Workflow

Follow this workflow unless the user explicitly asks for a lightweight answer.

### Step 1: Extract the Original Claim

Preserve the original claim before rewriting it.

### Step 2: Classify the Problem

Identify whether it is a fact, concept, forecast, value, action, or system judgment.

### Step 3: Rewrite as a Verifiable Question

A good verifiable question contains:

- object;
- time horizon;
- metric;
- threshold;
- data source or evidence type;
- boundary conditions.

### Step 4: Operationalize Key Concepts

For each key concept, define:

- meaning;
- non-meaning;
- observable indicators;
- adjacent concepts;
- counterexamples.

### Step 5: Generate Competing Hypotheses

List at least three hypotheses when the issue is uncertain or complex.

### Step 6: Build an Evidence Matrix

Use a matrix that shows which evidence supports or weakens which hypothesis.

### Step 7: Search for Counterevidence

List what would falsify or weaken the current judgment.

### Step 8: Express Probability and Confidence

Use probabilities or confidence ranges. Avoid absolute language unless the issue is a verified fact with strong evidence.

### Step 9: Give Action Boundaries

Separate:

- observe;
- verify;
- small experiment;
- reversible action;
- irreversible decision;
- professional consultation required.

### Step 10: Produce a Judgment Log

For important tasks, output a judgment log for later review.

---

## Standard Output Template

```markdown
# 判断力工程分析

## 1. 原始观点

## 2. 问题类型

## 3. 可验证改写

## 4. 关键概念与操作化

| 概念 | 定义 | 可观察指标 | 边界/反例 |
|---|---|---|---|

## 5. 竞争性假设

| 假设 | 说明 | 初始可能性 |
|---|---|---:|

## 6. 证据矩阵

| 证据 | 来源等级 | 支持/削弱哪些假设 | 备注 |
|---|---|---|---|

## 7. 反证与失效条件

## 8. 概率判断

## 9. 行动建议

## 10. 复盘计划

## 11. 判断日志
```

---

## Source Quality Levels

| Level | Source Type | Use |
|---|---|---|
| A | original documents, official data, filings, laws, papers, primary datasets | strong evidence, but check definitions |
| B | reputable institutional reports, professional databases | useful evidence, check methodology and incentives |
| C | journalism, expert interviews, company communications | useful but needs corroboration |
| D | social media, influencer content, screenshots, anonymous claims | only as leads |
| E | AI summaries without sources | not independent evidence |

---

## Risk Levels

| Level | Description | Required Behavior |
|---|---|---|
| L1 | low-stakes everyday judgment | standard judgment card |
| L2 | career, education, product, organization | full hypotheses, evidence, counterevidence, boundaries |
| L3 | investment, legal, medical, financial, major business | cite limitations, require authoritative sources and human confirmation |
| L4 | irreversible or high-loss decisions | structure the issue only; do not give final decision |

---

## Failure Modes to Avoid

- Answering before classifying the problem.
- Using a beautiful concept without operationalizing it.
- Treating multiple rewrites of the same source as independent evidence.
- Only listing evidence that supports the user’s framing.
- Giving binary conclusions for probabilistic issues.
- Ignoring time horizon and metric.
- Confusing “good outcome” with “good decision.”
- Giving high-stakes advice without boundary and limitation statements.
- Failing to create a review plan.

---

## Minimal Mode

When the user asks for a quick version, use the 30-second format:

```markdown
1. 这到底在判断什么？
2. 关键概念是否清楚？
3. 证据从哪里来？
4. 有没有反面解释？
5. 暂时判断：<概率/置信度 + 边界>
```

---

## Full Mode

When the issue is important or ambiguous, use the full judgment engineering analysis template.

---

## Retrospective Rule

For any judgment with a future outcome, always include:

- review date;
- observable outcome metrics;
- update triggers;
- what would prove the judgment wrong;
- what lesson should be added to the skill if the judgment fails.
