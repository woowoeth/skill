---
name: design-consistency
description: In-app consistency audit run directly against the real codebase — not a separate design file. Flags duplicate or divergent component usage, inconsistent typography, off-palette color, and behavioral inconsistency in how forms validate, modals open, and errors are shown across flows. Use to check whether the shipped product is internally consistent with itself.
---

# /design-consistency — In-App Consistency Audit

Audits the **actual running app and codebase** for consistency. There is no separate
design file in this workflow, so consistency is evaluated against the real, shipped code
itself. This directly replaces Figma-based design-file auditing.

The question is not "does this match the mock" — that's `/drift-check`. The question is
**"is this product consistent with itself?"**

## Step 1 — Scope

Ask, batched, with the usual escape hatch:

1. **What's in scope** — whole app, or specific routes/flows/directories?
2. **Where's the design system** — component library path, tokens file, theme config? (If
   unknown, find it — but confirm what you found.)
3. **Any known, deliberate exceptions** — legacy areas mid-migration, intentionally
   distinct surfaces (marketing pages, admin panels)?
4. **Threshold** — flag everything, or only what's likely to be user-visible?

Then read the codebase properly before reporting anything: the token definitions, the
shared component library, and the real consumption sites across the in-scope area.

## The four passes

Run all four. Each finds a different class of problem.

### Pass 1 — Component usage

The highest-value pass. Look for the same UI pattern implemented more than once:

- Duplicate implementations of a shared component — a bespoke button, a hand-rolled modal,
  a second dropdown that isn't the design system dropdown
- Shared components bypassed in favour of raw markup that reimplements them
- Near-duplicate components that should be one component with a variant prop
  (`CardSmall` / `CardCompact` / `MiniCard`)
- Same component used with inconsistent props for the same intent across flows
- Components that exist in the library but are never used anywhere (dead system surface)

Report the canonical implementation and every divergence from it, with file paths.

### Pass 2 — Typography

- Font families used outside the defined set
- Font sizes, weights, and line-heights that don't map to the type scale — hardcoded
  values, arbitrary Tailwind values, one-off CSS
- The same semantic role rendered at different sizes in different places (page titles at
  three different sizes)
- Heading levels used for visual size rather than document structure

State the defined scale first, then list every divergence with its location.

### Pass 3 — Color

- Hardcoded hex, rgb, or hsl values where a token exists
- Off-palette colors — values close to but not equal to a token (`#3B82F7` vs `#3B82F6`)
- Semantic tokens misused — error red used for a non-error, brand color used as text color
- Inconsistent state colors across flows: hover, focus, disabled, error, success
- Theme gaps — values that only work in one theme when both are supported

### Pass 4 — Behavioral consistency

This is the pass most audits skip, and it's often where users actually feel the
inconsistency. Check that interaction patterns behave the same way across flows —
**functionally, not just visually**:

- **Form validation** — on blur here, on submit there? Errors inline in one form and in a
  toast in another? Different rules for the same field type?
- **Modals and drawers** — do they all close on Escape? On backdrop click? Is focus
  trapped and restored consistently? Do some block scroll and others not?
- **Errors** — inline vs. toast vs. banner vs. full-page for equivalent severities. Do
  they all offer a retry? Is the tone consistent?
- **Loading** — skeleton in one place, spinner in another, nothing in a third, for the
  same kind of wait
- **Empty states** — some have guidance and a CTA, some are a blank panel
- **Destructive actions** — confirmed in one flow, immediate in another
- **Optimistic vs. pessimistic updates** — the same action feeling instant in one place
  and slow in another
- **Navigation** — back behaviour, breadcrumbs, unsaved-changes warnings

## Report

```markdown
# Consistency audit: <scope>

**Scope.** <routes/directories covered> · **Design system.** <where it lives>
**Excluded.** <deliberate exceptions honored>

## Summary
<2–3 lines: overall health, and the one pattern causing the most divergence>

| # | Severity | Category | Location | Issue | Canonical version |
| :-- | :-- | :-- | :-- | :-- | :-- |

## Component usage
### <issue title>
**Canonical.** `<path>` — used in <n> places
**Divergent.** `<path:line>` — <what it does differently>
**Impact.** <what the user experiences>
**Fix.** <the specific consolidation>

## Typography
## Color
## Behavioral consistency
<same shape per pass>

## Systemic findings
<the patterns behind the individual issues — e.g. "the modal component has no Escape
handler, so every consumer hand-rolls one differently." Fixing these kills whole
categories of issue at once.>

## Recommended order
<by impact-to-effort. Systemic fixes first where they collapse many issues.>
```

Severity is shared with `/usability-audit` and `/drift-check`: **Blocker** (breaks the
task or accessibility), **Major** (significant friction or clear inconsistency users
notice), **Minor** (noticeable roughness), **Polish** (cosmetic nit).

## Delivery

Before finalizing, ask where the output should go — a short menu, not a blocking gate:

- **Markdown file** at a path they name — recommend `audits/consistency-<scope>.md`
- **Claude artifact** — a shareable, published page
- **Issues filed in the tracker** — group by systemic finding, not one per symptom
- **Confluence / Google Drive / Notion** — only if such a connector is actually attached
- **Terminal only**

If the user opts out of choosing, write the markdown file at the recommended default and
say plainly where you put it.

## Failure modes to avoid

- **Assuming a destination.** Never decide on the user's behalf where output lands. Ask.
- **Listing symptoms without the systemic cause.** Twelve hand-rolled modals is one
  finding about the modal component, not twelve findings.
- **Reporting duplicates as separate issues.** Group by pattern.
- **Skipping the behavioral pass** because it's harder than grepping for hex codes. It's
  the pass with the most user impact.
- **Flagging deliberate exceptions.** Honor the declared out-of-scope list.
- **Assuming the most common implementation is canonical.** Sometimes the majority is
  wrong and the design system is right. Say which you're treating as canonical, and why.
