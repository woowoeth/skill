---
name: humanizer
description: Detects 43 surface-level AI writing patterns and rewrites text in 5 voice profiles. Use when (1) AI text reads like a chatbot, (2) preparing content for publication, (3) auditing prose for AI tells, (4) editing a file in place. Outputs a style lint score on demand. Standard modes are pure Markdown, zero dependencies; optional --deep mode adds local token-level style metrics (TTR, hapax, Gini) — descriptive statistics only, not a probability-based detector.
user-invocable: true
argument-hint: '"your text" [--mode detect|rewrite|edit|deep|compare|audit] [--voice casual|professional|technical|warm|blunt] [--file path/to/file.md] [--aggressive] [--iterate N] [--score] [--purpose essay|email|marketing|technical|general] [--edit-budget light|balanced|heavy] [--preserve facts,citations,terms,quotes,code] [--voice-sample PATH]'
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
  - Bash
---

# Humanizer: Make Text Sound Like a Human Wrote It

Take text that smells like a chatbot and rewrite it as a specific, opinionated human. Detects 43 surface AI writing patterns, reports them as a style lint density score, applies a chosen voice profile, and varies sentence-length burstiness.

North star: **LLMs regress to the statistical mean. Humans are weird, specific, and inconsistent. Write like a human.**

## Quick Reference

**Modes**

| Mode | What it does |
|:-----|:-------------|
| `detect` | Scan text, report patterns. Output a style lint score. No rewrite. |
| `rewrite` | Full transform with voice injection. Default mode. |
| `edit` | In-place file editing using the Edit tool. Minimal targeted changes. |
| `deep` | Extended rewrite with local token-level style metrics. Descriptive stats only. |
| `compare` | Produce clause change map and integrity diff. No rewrite; audit only. |
| `audit` | Style lint + mechanical transform audit + content risk check. No rewrite. |

**Voices** (full profiles: `references/voices.md`)

| Voice | Personality |
|:------|:-----------|
| `casual` | Contractions, first person, fragments |
| `professional` | Selective contractions, dry wit |
| `technical` | Precise vocabulary, code-like clarity |
| `warm` | "We" language, empathy |
| `blunt` | Shortest sentences, no hedging |

**Flags**

| Flag | Effect |
|:-----|:-------|
| `--score` | Prepend `[Style Lint: NN/100]` pattern density header |
| `--iterate N` | Loop detect → rewrite → detect until quality gates pass (max N=3) |
| `--aggressive` | Heavier rewrite, shorter sentences, more personality |
| `--purpose` | Layer content-type rules: `essay`, `email`, `marketing`, `technical`, `general` |
| `--deep` | Run token_analyzer.py for local style metrics (descriptive stats only) |
| `--edit-budget` | `light`, `balanced` (default), or `heavy` |
| `--preserve` | Comma-separated: `facts`, `citations`, `terms`, `quotes`, `code` (default: all) |
| `--voice-sample` | Path to file with the author's real writing for voice extraction |

Auto-loads `humanizer-context.md` from the working directory if present.

---

## Step 1: Parse Arguments

Extract from `$ARGUMENTS`:
- **Text**: Everything not part of a flag. If none and no `--file`, prompt for input.
- **--mode**: One of `detect`, `rewrite`, `edit`, `deep`, `compare`, `audit`. Default: `rewrite`.
- **--voice**: Voice profile. Default: infer from input register.
- **--file**: Path to a file to humanize.
- **--aggressive**: Heavier rewrite when set.
- **--iterate N**: Loop up to N times. Stop when quality gates pass or N reached.
- **--score**: Prepend style lint score header.
- **--purpose**: Content-type layering on top of voice.
- **--edit-budget**: `light` (minimal changes), `balanced` (default), `heavy` (aggressive rewrite).
- **--preserve**: Hard constraints on what to lock (default: all five enabled).
- **--voice-sample**: Extract voice features from file; do NOT fabricate demographics or history.

Proceed to Step 2.

---

## Step 2: Detect AI Patterns

**For English text:** Read `references/patterns-en.md` and scan for all 43 patterns (Content P1-P8, Language P9-P18, Communication P19-P21, Filler P22-P30, Emerging P31-P43). Track each match with location and fix suggestion.

**For Chinese text:** Read `references/patterns-zh.md` and scan for Chinese-specific patterns (Z1-Z20). Do NOT apply English trigger words to Chinese text.

**For mixed-language text:** Detect the primary language per paragraph and apply the appropriate pattern set.

**After detection:** If `--mode detect`, output the pattern report. Otherwise, proceed to Step 3 internally.

---

## Step 3: Voice Injection (for rewrite/edit/deep modes)

Read voice profiles from `references/voices.md`. Apply based on `--voice` flag (or infer from input register). When `--voice-sample` is provided, extract observable features from the sample.

Apply voice-specific contractions, transitions, sentence structures, tone, and vocabulary.

---

## Step 4: Execute Based on Mode

### Mode: `detect`
1. Scan for all applicable patterns (Step 2)
2. Output a pattern report with ID, offending text, fix suggestion
3. If `--score`, prepend `[Style Lint: NN/100]`

### Mode: `rewrite`
1. Run detection internally
2. Apply fixes for every detected pattern
3. Apply voice injection
4. Verify: no AI vocabulary, zero em dashes, sentence length variance > 30%, no formatting orphans
5. **Integrity gate:** Run `scripts/integrity_check.py` comparing original vs rewrite. Fix critical failures (numbers, URLs, citations, code blocks) before delivering.
6. Output rewritten text with change summary and (if `--score`) style lint score

### Mode: `edit`
1. Read `--file`, run detection
2. Apply targeted edits via Edit tool; preserve existing human voice
3. **Integrity gate:** Verify critical content preserved
4. Output edit summary

### Mode: `deep`
1. Run `scripts/token_analyzer.py` for pre-rewrite style metrics
2. Execute style-informed rewrite using metrics as guidance (lower TTR → vary word choice; higher AI vocab → trim boilerplate)
3. Run `scripts/integrity_check.py`
4. Re-run `scripts/token_analyzer.py` for post-rewrite comparison
5. Output before/after metrics table and rewritten text

### Mode: `compare`
1. Run `scripts/clause_align.py` and `scripts/integrity_check.py`
2. Output clause change map + integrity diff
3. No rewrite performed

### Mode: `audit`
1. Run style lint (Step 2)
2. Check mechanical artifacts: typo injection, casing anomalies, homoglyph chars, batch synonym replacements
3. Run integrity check
4. Output structured audit report with each dimension separate

---

## Step 5: Final Quality Check

Before presenting output:

1. **Integrity gate passed.** Critical content must be preserved.
2. **Read aloud.** Does it sound like a person?
3. **Opening hook.** No boring overview sentences.
4. **Ending.** No generic positive wrap-ups.
5. **AI vocabulary purge.** Kill any surviving blacklist words.
6. **Zero em dashes (U+2014).** Replace with commas, colons, or hyphens.
7. **Sentence length variance.** No 3+ consecutive sentences of similar length.
8. **"Who wrote this?"** Could a reader picture a specific person?
9. **No mechanical artifacts.** No injected typos, casing anomalies, homoglyph chars, or batch synonym replacements.

### Scoring (when `--score` is set)

`score = 4 × patterns_hit + 25 × (1 - burstiness_normalized) + 15 × (vocabulary_blacklist_ratio)`, clamped 0-100.

This is a **rule-density heuristic**, not an AI-generation probability. It measures how many surface patterns the text triggers, not what any specific detector would score.

| Range | What it means |
|:------|:--------------|
| 0-20 | Very few surface AI patterns detected |
| 21-40 | Minor tells, easy to clean |
| 41-60 | Multiple patterns detected |
| 61-80 | Many structural tells |
| 81-100 | Dense AI writing patterns |

### Iterate handling (`--iterate N`)
Re-run detection + integrity check on output. If significant patterns remain (> 3) OR integrity fails, recurse (max N). Stop when all quality gates pass.

### Content-Type Overrides (`--purpose`)
- `essay`: no contractions, formal headings, structured arguments
- `email`: greetings allowed, signoff allowed, no markdown
- `marketing`: short paragraphs, concrete benefits, one CTA
- `technical`: code blocks preserved, precise jargon, numbers over adjectives
- `general`: no overrides (default)

---

## Reference Files

| File | Content |
|:-----|:--------|
| `references/patterns-en.md` | Full P1-P43 English pattern catalog with triggers and fixes |
| `references/patterns-zh.md` | Chinese-specific patterns (Z1-Z20) |
| `references/voices.md` | Voice profiles and voice-sample extraction protocol |
| `references/pangram4-notes.md` | Pangram 4 paper: facts, limits, and prohibited over-extrapolations |
| `references/guo2025-notes.md` | Guo et al. (2025): distributional observations (research notes) |
| `references/tail-token-smuggling.md` | ⛔ DEPRECATED — do not use |
| `scripts/integrity_check.py` | Content integrity checker |
| `scripts/clause_align.py` | Clause-level alignment and change map |
| `scripts/token_analyzer.py` | Document-level style metrics (descriptive statistics) |

## Examples

### Example 1: Technical Documentation

**Before:**
> This comprehensive guide delves into the intricacies of our authentication system. The platform leverages cutting-edge JWT technology to provide a seamless, secure, and robust authentication experience. Additionally, it features a pivotal role-based access control system that serves as a testament to our commitment to security.

**After (`--voice technical`):**
> The auth system uses JWTs. Tokens expire after 15 minutes; refresh tokens last 7 days. Role-based access control restricts API endpoints by user role: admin, editor, and viewer each see different data. The token rotation logic is in `src/auth/refresh.ts`.

### Example 2: Blog Post

**Before:**
> In today's rapidly evolving technological landscape, artificial intelligence is reshaping how we think about creativity. This groundbreaking shift represents a pivotal moment in human history, one that underscores the intricate interplay between innovation and artistic expression.

**After (`--voice casual`):**
> I've been messing around with AI image generators for about six months now, and I still can't decide if I love them or if they make me uneasy. The outputs are technically impressive. But there's something missing — like eating a perfect-looking meal that has no flavor.

### Example 3: Social Media

**Before:**
> Excited to announce that I've taken on a pivotal new role at TechCorp! This incredible opportunity represents a significant milestone in my professional journey. #NewBeginnings #Innovation #Leadership

**After (`--voice professional`):**
> Started at TechCorp this week. Leading their developer tools team — 12 engineers, ~400 internal users. First week has been drinking from the firehose. If anyone has advice on the first 90 days in eng leadership, I'm all ears.

---

*Write like a human. Be weird, specific, inconsistent.*
