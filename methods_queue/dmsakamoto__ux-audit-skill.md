---
name: ux-audit
description: Use when asked to audit, evaluate, or walk through a product's UX from the user's seat — "run a UX audit", "try doing X as a user", "why is this flow so hard", "how could this UX be drastically improved" — or any task-based usability walkthrough of a live web app.
---

# UX Audit

## Overview

A task-based usability walkthrough: execute a real user task in the live product with browser tools, measure the friction, report ranked findings with concrete redesign proposals. The unit of audit is a **journey** (one task), never a page. Page-level polish falls out of journey findings; it never leads.

Baseline failure this skill exists to prevent (observed in practice): the agent walks the product using codebase knowledge — knows which tab, what the terms mean, where the buried surface is — and reports impressions. The result describes the *agent's* path, not a user's, and the findings are vibes without counts.

## The audit contract — produce these parts, in this order

1. **Task script** — one sentence before touching the browser: persona + goal + starting point. Example: "A hobbyist who has never seen the codebase wants to set a stop-loss for the first time. Start: /dashboard."
2. **Naive execution** — walk it in the browser (get tab context first; load browser tools in one batch). Role-play a competent first-time user with ZERO codebase knowledge. Before every click ask: *how would I know to click this without having read the code?* When the answer requires insider knowledge, that moment is a finding — log it, then proceed using the knowledge.
3. **The trail** — screenshot every state change. Per step, record: clicks so far, scrolls, back-tracks, dead ends. Numbers, not adjectives. Record a GIF when the journey itself is the deliverable.
4. **Copy-vs-mechanism check** — every UI sentence encountered that promises something the mechanism doesn't do (a lifecycle strip naming a step the panel can't perform, a caption claiming a guarantee the code doesn't enforce). These are software defects, always in scope.
5. **Findings, ranked** — task-blocking → friction → polish. Each finding names: the moment (step number + screenshot), the evidence (count or quoted copy), and a concrete redesign sketch.
6. **The drastic section** — exactly one per audit: should this journey exist in this shape at all? Cross-check your project's decision log and design brief first (if they exist); a proposal touching a previously ruled decision names the ruling it would supersede.
7. **Output** — a dated `docs/ux-audits/YYYY-MM-DD-<task-slug>.md` report, plus the finding list shaped for your issue tracker. Every fix gets a ticket before anyone builds it; the audit never self-dispatches fixes.

## Safety rails — production may be live money and real customer data

- The walkthrough is **read-only**: never submit a form, never toggle a kill switch, never change a setting on a production account.
- When the task requires a write, stop at the confirm surface, screenshot it, and record what *would* happen. Writes are executed only in a demo/staging environment or with the operator's explicit per-audit approval.
- Reuse an existing logged-in tab only when the operator offers it; otherwise create a fresh tab.

## Quick reference — what to measure

| Measure | How |
|---|---|
| Click cost | count from start state to goal state |
| Findability | did a naive scan of visible nav labels locate the surface? |
| State visibility | is current state visible *before* acting (show-state-always)? |
| Copy honesty | does every label match its mechanism? |
| Recovery | after a wrong turn, how many steps back to the path? |
| Depth | how many levels down is the goal surface buried? |

## Common mistakes

- Navigating with code knowledge without logging it → the audit reports your path, not a user's.
- Impressions without counts → unactionable, unrankable.
- Auditing a page instead of a task → polish findings only, journey findings missed.
- Proposing against a ruled decision without naming it → the finding dies in review.
- Fixing things mid-audit → the audit is a measurement instrument; fixes go through tickets.
