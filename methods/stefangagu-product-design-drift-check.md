---
name: drift-check
description: Compares the actual shipped implementation against the design mocks or prototypes it was based on (from /design-proto or /quick-proto) and reports where they have diverged. Primarily for developers validating that what shipped matches what was agreed, but usable by anyone checking alignment. Use when asking whether the built feature still matches the design it came from.
---

# /drift-check — Implementation vs. Design-Mock Drift Detection

Compares what shipped against what was designed, and reports where they diverged.

Mainly used by **developers** validating that the implementation matches what was
designed and agreed — but like every skill here, anyone can run it. Designers and PMs use
it to check alignment before sign-off.

The complement to `/design-consistency`: that skill asks "is the app consistent with
itself," this one asks "does the app match its design intent."

## Scope note — why this is narrower than a traditional drift check

When prototypes are built via `/design-proto` (Track A, in-repo), there is **no separate
design file to drift from in the first place**. The prototype and the implementation are
the same artifact lineage, so this comparison is catching drift introduced *after* handoff
— not translating between two disconnected formats.

That makes Track A drift checks fast and precise: usually a git diff between the prototype
branch or commit and what's on main now.

Track B (`/quick-proto`) drift checks are inherently fuzzier — a low-fi grayscale
prototype was never meant to specify visual detail. Judge Track B against **flow, states,
structure, and content**, and explicitly do **not** report styling divergence as drift.
That would be comparing against something the prototype never claimed to specify.

This asymmetry is itself a natural argument for Track A adoption — worth stating in the
report when it comes up.

## Step 1 — Establish both sides

Ask, batched, with the usual escape hatch:

1. **The design reference** — prototype branch, commit, PR, artifact, spec document, or
   screenshots. Which track produced it?
2. **The implementation** — branch, route, or running URL.
3. **What was deliberately changed** after handoff, and why? Known, agreed deviations are
   not drift — they're decisions, and mislabelling them destroys trust in the report.
4. **How strict?** Pixel-level, or structural/behavioral only? (Structural is the sensible
   default; pixel-level only makes sense against a Track A reference.)

Then read both sides properly. For Track A, prefer an actual diff — it's exact.

## Step 2 — Compare across four dimensions

### Structure
Screens present and missing · layout and hierarchy · component choices · placement of
primary and secondary actions · responsive behaviour.

### States
The dimension most likely to have drifted, because states are added under delivery
pressure. Loading · empty · error · success · partial · disabled · permission-denied ·
long-content and overflow. Designed but not built, and built but never designed — both
are drift, and the second is often the more interesting one.

### Behaviour
Interaction patterns · validation timing and rules · transitions and navigation · what
happens on failure · optimistic vs. pessimistic updates · focus and keyboard handling.

### Content
Copy changes (labels, errors, empty-state text) · terminology consistency · data actually
displayed vs. designed · truncation and formatting.

For each divergence, decide honestly which of these it is — this classification is the
most useful part of the report:

- **Regression** — the implementation is worse than the design. Fix it.
- **Improvement** — the implementation is better; the design was wrong or incomplete.
  Update the design reference, don't "fix" the code.
- **Constraint** — engineering hit something real (API shape, performance, platform
  limit). Document it and design around it.
- **Undocumented decision** — someone made a reasonable call that just never got written
  down. Write it down.

Not all drift is bad. A report that treats every difference as a defect will be ignored
by the second sprint.

## Step 3 — Report

```markdown
# Drift check: <feature>

**Design reference.** <source> (Track A / Track B) · **Implementation.** <branch/route>
**Comparison strictness.** <structural | pixel-level>
**Agreed deviations excluded.** <what the user flagged as intentional>

## Summary
<2–3 lines: overall alignment, and the most consequential divergence>

| # | Severity | Type | Area | Designed | Implemented |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | Major | Regression | Error state | Inline message + retry | Generic toast, no retry |

## Divergences

### 1. <Title>
**Designed.** <what the reference specified> — <reference location>
**Implemented.** <what actually shipped> — `<file:line>` or route
**Type.** Regression | Improvement | Constraint | Undocumented decision
**User impact.** <concretely, what's different for the person using it>
**Recommended action.** Fix the code | Update the design | Document the decision

<repeat, severity descending>

## Matches
<what aligned — brief. Especially valuable on Track A checks, where it's usually most of it.>

## Design reference updates needed
<where the implementation is right and the reference is stale>
```

Severity is shared with the other audit skills: **Blocker**, **Major**, **Minor**,
**Polish**.

## Delivery

Before finalizing, ask where the output should go — a short menu, not a blocking gate:

- **Markdown file** at a path they name — recommend `audits/drift-<feature>.md`
- **Claude artifact** — a shareable, published page
- **Comments on the PR** that introduced the drift
- **Issues filed in the tracker** for the regressions only
- **Confluence / Google Drive / Notion** — only if such a connector is actually attached
- **Terminal only**

If the user opts out of choosing, write the markdown file at the recommended default and
say plainly where you put it.

## Failure modes to avoid

- **Assuming a destination.** Never decide on the user's behalf where output lands. Ask.
- **Treating every difference as a defect.** Classify each one. Improvements exist.
- **Pixel-comparing a Track B prototype.** It never claimed to specify styling. Reporting
  grayscale-vs-brand-color as drift makes the whole report noise.
- **Missing the drift of omission.** A designed state that was silently never built is the
  most common and most expensive drift. Check the state list explicitly.
- **Re-flagging agreed deviations.** Honor the declared list, every time.
- **Only reporting code-side fixes.** Sometimes the correct output is "update the design
  reference" — say so.
