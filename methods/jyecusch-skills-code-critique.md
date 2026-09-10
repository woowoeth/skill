---
name: code-critique
description: Ruthlessly review code, a diff, a PR, or a codebase for unnecessary code, accidental complexity, misuse-prone APIs, and poor reviewability. Use whenever asked to review, critique, or audit code quality, architecture, or a pull request — and consult it before writing significant new code so it passes review the first time.
---

# Code Critique

Review whatever code you're pointed at. Report only violations. No praise, no restating what the code does. If asked to fix rather than review, apply the fixes.

Report every finding regardless of how expensive its fix is: a rename rippling through fifty call sites is still a finding — state it with its blast radius and let the human set the churn budget. Never trade a finding away against "minimal code" silently; goal 1 constrains the code you write, not the problems you report. A scoped request ("review the comments this branch adds") narrows what you *fix*, not what you may *flag*.

Each finding: location — problem — concrete fix — principle violated. For example:

> `src/auth.ts:42` — `buildAuthContext(data)` accepts arbitrary data and is only safe if `verifySession()` was called first (temporal coupling). Fix: merge into `authContextFromToken(token)` that verifies internally, and stop exporting `AuthContext` so that's the only way to get one. *(misuse-resistance)*

Judge against four goals:

1. **Minimal code.** Flag anything not needed for the actual job: boilerplate, speculative generality, layers that only forward calls, dead configuration. Extra code is justified only when it serves goals 2–4.
2. **Essential complexity only.** Essential complexity is inherent to the problem; accidental complexity comes from our tools and choices (Brooks). Flag the accidental kind. Structure, names, and types should minimize the cognitive load of whatever essential complexity remains.
3. **Misuse resistance.** Interfaces must be easy to use correctly and hard to use incorrectly. Apply the `misuse-resistance` skill.
4. **Reviewability (local reasoning).** Humans review diffs (GitHub PR UI) seeing only a few lines of context, and they verify code against what names and types *claim* — under time pressure, nobody opens distant definitions. Anything whose correctness can't be verified from the visible lines alone — misleading names, invisible preconditions, action at a distance, nesting whose governing conditions sit above the fold, comments whose referents live outside the file — will slip mistakes past human review.

Where the code touches their domains, also apply: `naming`, `un-nesting`, `self-documenting-code`, `writing-comments`, `type-driven-design`, `abstraction-and-coupling`, `composition-over-inheritance`, `dependency-injection`, `state-and-pipelines`. When *writing or amending* code (not just reviewing), `writing-comments` and `naming` govern every comment and identifier you produce, and `type-driven-design` governs every type and signature.

For every public API, ask: what's the worst mistake a competent but rushed developer could plausibly make here? If the design permits the mistake, flag it — "the docs say not to" is not a defense.
