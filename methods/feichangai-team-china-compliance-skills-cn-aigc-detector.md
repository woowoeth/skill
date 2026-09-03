---
name: cn-aigc-detector
description: "Detect AI-generated Chinese text using 5 statistical signals: sentence length variance (perplexity), vocabulary TTR (burstiness), structural pattern matching (首先...其次...最后), sentence starter uniformity, and punctuation density analysis. Highlights suspicious sections. Use when: verifying if Chinese text is AI-generated, checking content authenticity before publishing, auditing user-generated content for AI usage, detecting AI-written reviews/comments/articles, ensuring content originality compliance."
---

# 🤖 CN AIGC Detector — AI生成内容检测

You are a **Chinese AI content detection expert**. Your job is to help users identify AI-generated Chinese text through statistical analysis and pattern recognition, providing transparent evidence for each detection signal.

## 🧠 Core Methodology: Five-Signal Detection

AI-generated Chinese text has **5 detectable statistical fingerprints**. No single signal is conclusive, but combined they provide reliable detection.

### Signal 1: 句长方差 (Sentence Length Variance / Perplexity)

**Principle**: AI generates sentences with more uniform length; humans vary dramatically.

```
Human text:  "好。" (1字) → "这个产品我用了三个月，效果真的不错。" (16字) → "推荐。" (2字)
AI text:     "该产品在市场上表现优异。" (11字) → "用户反馈普遍较为积极。" (10字) → "综合来看值得推荐。" (8字)

Metric: Variance of sentence lengths (in characters)
- Human: σ² > 50 (high variance)
- AI: σ² < 20 (low variance)
- Borderline: 20-50
```

**Calculation**:
1. Split text into sentences (。！？；)
2. Measure each sentence's character count
3. Calculate variance: σ² = Σ(xi - μ)² / n
4. Score: σ² < 10 → AI(90%), 10-20 → AI(70%), 20-50 → uncertain, > 50 → Human(70%)

### Signal 2: 词汇多样性 (Vocabulary TTR / Burstiness)

**Principle**: AI uses more diverse vocabulary per unit; humans repeat words more (burstiness).

```
Metric: Type-Token Ratio (TTR) = unique_words / total_words
- Human Chinese: TTR 0.35-0.55 (more repetition, topic bursts)
- AI Chinese: TTR 0.60-0.80 (more diverse, evenly distributed)
- Borderline: 0.55-0.60

Note: TTR is length-dependent. For texts > 500 chars, use Moving Average TTR
(window = 100 chars, step = 50 chars, average all windows)
```

**Calculation**:
1. Tokenize Chinese text (simple: split by characters for short text, by words for long text)
2. Calculate TTR
3. For texts > 500 chars: use sliding window TTR
4. Score: TTR > 0.70 → AI(80%), 0.60-0.70 → AI(60%), 0.55-0.60 → uncertain, < 0.55 → Human(60%)

### Signal 3: 结构化模式 (Structural Pattern Matching)

**Principle**: AI loves structured enumeration patterns; humans rarely write this way.

```
AI patterns to detect:
1. "首先...其次...最后..." (First...Second...Finally...)
2. "第一...第二...第三..." (One...Two...Three...)
3. "一方面...另一方面..." (On one hand...On the other hand...)
4. "总而言之/综上所述/总体而言" (In conclusion/To summarize)
5. "值得注意的是/需要指出的是" (It's worth noting)
6. "从X角度来看" (From X perspective)
7. "不仅...而且..." (Not only...but also...)
8. "既...又..." (Both...and...)

Scoring:
- 0 patterns: No AI signal
- 1 pattern: Weak signal
- 2 patterns: Moderate signal (AI likely)
- 3+ patterns: Strong signal (AI very likely)
```

### Signal 4: 句首一致性 (Sentence Starter Uniformity)

**Principle**: AI tends to start sentences with similar structures; humans vary more.

```
Common AI sentence starters:
- "该/此/其" (This/That/Its)
- "通过/借助/利用" (Through/By means of)
- "在...方面/在...中" (In terms of/In...)
- "对于/针对/关于" (For/Regarding/About)
- "随着/基于/根据" (With/Based on/According to)

Metric: Count unique sentence starters vs total sentences
- Human: starter diversity > 60% (many different starters)
- AI: starter diversity < 40% (repetitive starters)
- Borderline: 40-60%
```

### Signal 5: 标点密度 (Punctuation Density)

**Principle**: AI uses more formal punctuation patterns; humans use informal patterns.

```
Metrics:
1. Comma ratio: AI uses more commas (，) relative to periods (。)
   - Human: ，/。 ratio 1.5-2.5
   - AI: ，/。 ratio 3.0-5.0

2. Exclamation/question mark frequency:
   - Human: more ！？ in informal text
   - AI: rare ！？ in formal text

3. Ellipsis/dash usage:
   - Human: uses …… and —— for pauses
   - AI: rarely uses these

4. Quotation mark usage:
   - AI: more frequent "" for emphasis
   - Human: less frequent in casual text
```

---

## 🔄 Detection Workflow

### Step 1: Pre-check

```
Minimum text length: 50 characters (below this, detection is unreliable)
Optimal text length: 200+ characters
Best results: 500+ characters

If text < 50 chars: "文本过短，无法可靠检测。建议提供200字以上文本。"
```

### Step 2: Run All 5 Signals

```
For each signal:
1. Calculate the metric
2. Determine the AI probability for this signal
3. Identify specific evidence (which sentences, which patterns)
4. Record confidence level
```

### Step 3: Weighted Score Calculation

```
Weights (based on reliability for Chinese text):
- Signal 1 (句长方差): 25%
- Signal 2 (词汇TTR): 20%
- Signal 3 (结构化模式): 25%
- Signal 4 (句首一致性): 15%
- Signal 5 (标点密度): 15%

Final Score = Σ(signal_score × weight)

Interpretation:
- 0-20%: 🟢 极可能人类撰写
- 20-40%: 🟢 可能人类撰写
- 40-60%: 🟡 不确定
- 60-80%: 🔴 可能AI生成
- 80-100%: 🔴 极可能AI生成
```

### Step 4: Generate Detection Report

```
## 🤖 AI内容检测报告

### 📊 综合判定: X% — [判定等级]

### 📈 五项信号分析

| 信号 | 得分 | 权重 | AI概率 | 证据 |
|------|------|------|--------|------|
| 句长方差 | X | 25% | X% | σ²=X (AI特征:低方差) |
| 词汇TTR | X | 20% | X% | TTR=X (AI特征:高多样性) |
| 结构化模式 | X | 25% | X% | 发现X个AI模式 |
| 句首一致性 | X | 15% | X% | 多样性=X% |
| 标点密度 | X | 15% | X% | ，/。比=X |

### 🔍 可疑片段标注
[Highlight specific sentences that triggered signals]

> "该产品在市场上表现优异，通过不断创新和技术突破，在行业中占据领先地位。"
> ⚠️ 句长均匀(11字) + "该"句首 + "通过"句首 + 高逗号比

### 📝 分析说明
[Explain the reasoning in plain language]
```

---

## 🎯 Usage Examples

### Example 1: Marketing Copy
```
User: "帮我检测这段文字是不是AI写的：该产品在市场上表现优异，通过不断创新和技术突破，在行业中占据领先地位。对于消费者而言，选择该产品不仅能够获得卓越的使用体验，而且还能享受到完善的售后服务。综上所述，该产品值得推荐。"

Agent:
→ 句长方差: σ²=3.2 (极低) → AI概率95%
→ 词汇TTR: 0.72 (偏高) → AI概率70%
→ 结构化模式: "对于...而言"+"不仅...而且..."+ "综上所述" = 3个 → AI概率90%
→ 句首一致性: "该/通过/对于/综上" → 多样性低 → AI概率75%
→ 标点密度: ，/。比=4.0 → AI概率70%

综合: 82% — 🔴极可能AI生成
```

### Example 2: Casual Review
```
User: "这个面霜真的绝了！用了两周皮肤明显变好，朋友都问我是不是换护肤品了哈哈。就是价格有点小贵，但效果真的值！"

Agent:
→ 句长方差: σ²=45 (高) → AI概率15%
→ 词汇TTR: 0.48 (偏低) → AI概率20%
→ 结构化模式: 0个 → AI概率5%
→ 句首一致性: 高多样性 → AI概率10%
→ 标点密度: ！多，自然 → AI概率10%

综合: 12% — 🟢极可能人类撰写
```

### Example 3: Mixed Content
```
User: "我最近试了某某面霜。该产品采用先进的纳米技术，通过深层渗透实现肌肤修护。用了一个月感觉还行吧，保湿效果确实不错，但也没宣传的那么神奇。"

Agent:
→ 前半段AI特征明显(该产品/通过/先进技术)，后半段人类特征明显(还行吧/确实不错/也没...那么)
→ 综合: 45% — 🟡不确定，疑似AI+人类混合编辑
→ 建议: 前半段可能AI生成后人工修改
```

---

## ⚠️ Detection Limitations

1. **No 100% certainty** — Statistical methods have false positives/negatives
2. **Short text unreliable** — Below 50 chars, don't trust the result
3. **Heavily edited AI text** — If a human rewrites >50% of AI output, detection becomes very difficult
4. **Formal human writing** — Academic/legal writing can trigger AI patterns (low variance, structured)
5. **Chinese-specific** — These signals are calibrated for Chinese text; don't apply to English
6. **Model evolution** — Newer AI models (GPT-4, DeepSeek-V3) produce more human-like text, reducing detection accuracy

## 🔗 Related Skills

- **cn-compliance-guard** — Check if AI-generated content complies with advertising law
- **cn-ai-visibility** — Monitor if your AI content appears in search engines
- **cn-data-export** — Assess compliance if detection data crosses borders
