---
name: physics-paper-principles
description: >-
  Graduate-level physics and mathematics prose principles: sentence clarity,
  narrative arc, physically led definitions, and math-logic types. Use when
  writing or reviewing physics-paper LaTeX. Pair with physics-paper-editing
  for the coworker-loop workflow and physics-paper-editing-section for whole
  sections. Not a process skill — no marks, Tasks, or merge.
---

# Physics paper principles

**Domain rules** for what good physics/mathematics prose looks like. Pair with **`physics-paper-editing`** (short-passage coworker loop) and **`physics-paper-editing-section`** (whole-section orchestrator).

**Not in scope:** marks, snapshots, verifier Tasks, `OVERALL`, merge, or pace — those live in the editing skills.

**Litmus test (every principle):** Would this still apply if the coworker loop, construction marks, and background checkers disappeared?

## Agent read order

| When | Read |
|------|------|
| **Always** | Principle map below |
| **This skill referenced alone** | This skill’s files only. Do not read and follow **`physics-paper-editing`**. |
| **Writing or reviewing a sentence / local passage** | [sentence.md](sentence.md) |
| **Anything longer than one sentence** | + [narrative.md](narrative.md) |
| **Math, equations, logical argument, or a named-object definition** | + [math.md](math.md) |
| **Introducing or rewriting a named physical/protocol object** | + [physical-lead.md](physical-lead.md) **first** |
| **Running the coworker loop / section edit** | **`physics-paper-editing`** or **`physics-paper-editing-section`** — this skill is canon, not the process |

**When this skill is referenced alone,** do not read and follow **`physics-paper-editing`**. First reply: say which layer(s) govern the passage (sentence / narrative / math / physical lead).

When **`physics-paper-editing`** is also attached, that skill’s first-reply and loop rules win; use this file as drafting canon.

## When to use

- Writing or reviewing LaTeX physics or mathematics prose at graduate level
- Introducing a named object in a physics or protocol story
- Judging whether a formula’s prose is faithful, or whether a definition is physically led
- Construction-phase drafting where the editing harness must **not** run (principles still apply)

**Route elsewhere:** running the marked draft → background-verify → merge loop → **`physics-paper-editing`**. Whole `\section{...}` or **>12 sentences** through that loop → **`physics-paper-editing-section`**.

---

## Principle map

Four layers. Numeric IDs match the detail files (sentence **1–14**, narrative **groups 1–4**, math **types 0–4**).

| Layer | Question | File |
|-------|----------|------|
| **Sentence** | Does each sentence say one clear thing, in an order a reader can follow? | [sentence.md](sentence.md) |
| **Passage** | Does the unit have one message and a logical arc? | [narrative.md](narrative.md) |
| **Math** | Is every statement well-typed and logically/faithfully stated? | [math.md](math.md) |
| **Named objects** | Is the lead an operational membership test, not a construction recipe? | [physical-lead.md](physical-lead.md) |

```
Sentence (1–14) ─┬─ Passage groups 1–4
                 └─ Math types 0–4 ── Physical lead (named objects)
```

**Cross-cutting (stated once, pointed to elsewhere):**

| Topic | Canonical |
|-------|-----------|
| Pronouns, SVO, voice, “For A, it does B”, clause-must-claim | sentence **1, 4, 9, 10, 14** |
| Cross-boundary reminders | sentence **2** (passage-scale: narrative group 2 signposting) |
| Undefined terminology | sentence **3** |
| Declare setup; do not hypothesize | sentence **7** (passage-scale: narrative group 2 model setup) |
| Confusion-on-first-read ordering (tiers 1–3) | sentence **13** |
| Prose vs math | sentence **12** + math Type 2 |
| Physical lead / construction-as-definition | [physical-lead.md](physical-lead.md) |
| Purpose-first (intent → natural language → formula) | [math.md](math.md) Type 2 |
| Detect tests (how to see a violation) | Detect column in [sentence.md](sentence.md); Detect lines in [narrative.md](narrative.md); Required products in [math.md](math.md) |

Apply every principle in the open file(s) in order. Name it, state how it applies. If one does not apply, say **not applicable** and why. Do not skip, merge, or abbreviate. Coworker-loop **workers** invert this lookup (artifact first) — see **`physics-paper-editing`**.

---

## How these files relate to editing

| This skill | Editing skills |
|------------|----------------|
| What the prose should be | How a draft is marked, checked, and merged |
| Principle → Detect lookup | Artifact → principles worker loop (same names) |
| Diagnose a missing operational criterion | **Definition halt** — do not ship a construction-only definition |
| Flag unfaithful prose or a false relation | **BLOCKER / SUGGEST** mapping in `physics-paper-editing` `severity.md` |

**Sibling sync:** this skill and **`physics-paper-editing`** are a paired split (canon vs harness). Changing a Detect test name, Required product, or principle ID here requires the same name in the editing skill’s worker **artifact → principles** list, **same pass**. Changing a worker artifact or its principle list requires this Detect column still to point at that artifact. Grep the sibling for the old name before finishing. Drift is a bug. Do not copy Detect paragraphs into prompts — name the test; require the same artifact label.

Do not invent an operational criterion you cannot stand behind. Diagnosis is always possible; generation is not.

## File map

| File | Role |
|------|------|
| **SKILL.md** | Map, litmus, pairing |
| [sentence.md](sentence.md) | 14 sentence principles + Detect column |
| [narrative.md](narrative.md) | Four passage-level groups + Detect lines |
| [math.md](math.md) | Statement types, type-specific checks, Required products |
| [physical-lead.md](physical-lead.md) | Named physical/protocol objects; membership-without-recipe |

## Related skills

| Skill | When |
|-------|------|
| **physics-paper-editing** | Coworker loop on a passage **≤12 sentences** |
| **physics-paper-editing-section** | Whole `\section{...}` or **>12 sentences** through that loop |
| **sc-qubit-research** | Research-trust principles for notes (pair this skill for sentence-level note prose) |

## Out of scope

- Marks, snapshots, verifier Tasks, `OVERALL`, merge, pace, fast-polish scoping
- BibTeX, figure files, or equations-only blocks with no prose claims
- Inventing a physical membership test the author has not supplied
