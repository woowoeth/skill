---
name: brainstorming
description: Use before implementation when a request is ambiguous, has materially different solution paths, changes architecture or public behavior, or involves costly or irreversible decisions. Skip for small well-scoped fixes, mechanical edits, and execution of an already approved plan.
---

# Pragmatic Brainstorming

Resolve decisions that could materially change the result before implementation, without turning routine work into design ceremony.

## When to use

Use this skill when at least one condition applies:

- The goal, constraints, or success criteria are unclear.
- Multiple viable approaches have meaningful trade-offs.
- The change affects architecture, public behavior, data contracts, security, migration, or several components.
- A wrong choice would be expensive, risky, or hard to reverse.
- The user explicitly asks to brainstorm, explore options, or design a solution.

Skip it when the request is a small, well-scoped fix, a mechanical edit, a diagnosed bug with an agreed solution, or execution of an approved design or plan.

If uncertain, inspect the available context first. When a safe, local, reversible assumption is enough, state it and continue. Invoke brainstorming only when the unresolved choice could materially change scope, behavior, risk, or cost.

## Workflow

1. **Inspect context** — Read the relevant artifact, constraints, and existing decisions before asking questions.
2. **Identify the decision** — Separate material unknowns from details that can be resolved during implementation.
3. **Clarify selectively** — Ask only questions whose answers would change the approach. Batch up to three closely related questions when that is faster for the user.
4. **Compare real alternatives** — Present two or three approaches only when they are genuinely viable. State trade-offs and lead with a recommendation.
5. **Describe the design** — Scale detail to risk. Cover affected components, behavior or data flow, failure handling, and verification where relevant.
6. **Confirm material choices** — Ask for approval before implementation only when the choice changes scope, public behavior, architecture, data, or meaningful risk. If the user already selected or approved the approach, do not ask again.

## Output scale

- For a narrow decision, a short recommendation with assumptions and trade-offs is enough.
- For a substantial design, use clear sections and validate the decisions that matter.
- Write a durable design document only when the user requests it or the decision is important enough to preserve for future work.

## Principles

- Prefer evidence from the current project over hypothetical discussion.
- Do not invent alternatives merely to satisfy a fixed count.
- Keep questions and design detail proportional to uncertainty and risk.
- Use YAGNI: resolve what implementation needs now, not every possible future concern.
- Do not automatically create tasks, write or commit a design document, or invoke a planning workflow.
- Once material uncertainty is resolved, continue with implementation instead of adding another approval round.
