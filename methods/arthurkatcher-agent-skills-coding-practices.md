---
name: coding-practices
description: Always-on rules for writing, changing, testing, and reviewing code in any language. Use on every coding task and before claiming any work is done.
---

# Coding Practices

## Primary bias to correct

Working code is not automatically good code, and a confident claim is not evidence.

## Decision rules

- No production code without a failing test first. The loop, one behavior at a time:
  1. Write the test.
  2. Run it. Confirm it fails, and fails because the behavior is missing, not because of a typo or import error.
  3. Write the least code that makes it pass.
  4. Run the full suite, not just the new test file. Confirm the new test passes and nothing else broke.
  5. Refactor only with the suite green, then run it again.
  Code written before its test gets deleted and rewritten from the test.
- Test at seams: the public interface where behavior is observed. Never private methods, never internal collaborators. Real collaborators over mocks; a mock is a last resort, not a convenience. Expected values come from the spec, never from the code under test.
- A test covers one behavior, is named for that behavior, uses realistic inputs, and would fail without the implementation. Happy path first, then every error case the task named.
- Never weaken or skip a failing test to get green. Fix the code or report the conflict.
- Read local context before editing: names, layout, wiring, error style, test style, and whether the logic already exists. Search before you write. Local idiom beats generic preference.
- Put code with the unit that owns the responsibility, not the file that is open. Mirror the two or three most similar existing artifacts. Wire new files in completely.
- One job per unit, at every scale. Describe it in one sentence without "and", "also", or "then".
- Prefer deep modules: lots of behavior behind a small interface. Reject wrappers, helpers, layers, and split-outs that add names without hiding real complexity.
- Dependencies point inward. Business rules never name the database, framework, ORM, request object, or vendor SDK. All SQL lives in the data layer.
- Deduplicate only copies that must always change together.
- Names are precise, in domain vocabulary, one term per concept. No `data`, `helper`, `utils`, `_v2`, `_new`, `_final`.
- Functions do one thing at one level of abstraction. No boolean flags, no output parameters. Commands separate from queries.
- Errors are handled where a decision can be made, propagated with cause otherwise, never swallowed. Validate at the boundary; trust the inside.
- Comments say why, in one to three lines. A comment that explains the flow is a request to rename or split.
- Every changed line traces to the request. Targeted edits, never whole-file regeneration. Mention unrelated smells; do not fix them silently.
- No new dependency without a reason you would repeat to a reviewer. Verify every API against the installed version, not memory.
- Nothing left behind: no dead code, no TODOs for in-scope work, no commented-out blocks, no stubs presented as done.

## Trigger rules

- A function mixes setup, validation, computation, and side effects → split the phases.
- The same few parameters keep traveling together → they are a type.
- One change forces edits across many files → a boundary is missing; fix ownership, not symptoms.
- Adding a helper, layer, option, or callback → prove it removes complexity for callers, or drop it.
- A bug is found → reproduce it with a failing test, then fix.
- Tempted to rewrite → take the next small behavior-preserving step instead.
- Async, locks, or shared state appear → make ownership, ordering, and cleanup explicit; test the timing path.

## Before claiming done

1. Identify the command that proves the claim.
2. Run it fresh and in full.
3. Read the whole output and the exit code.
4. Confirm it actually supports the claim.
5. Only then state it, with the evidence. Never "should", "probably", "seems to".

A bug fix is proven by the original symptom failing, then passing. A subagent's report is not evidence; check the diff. If a check cannot run, say what did not run and what risk remains.

## Before and after shipping

Run the full test suite before any deploy; a red suite blocks the deploy. After the deploy, exercise the feature against the running system, not the code, and report exactly what was checked and what was not.

## Final checklist

- Test seen failing before the code existed?
- Every changed line traces to the request?
- New code in the owning unit, fully wired?
- Verification run fresh, output quoted, gaps named?
- Suite green before deploy, feature exercised live after?
- One risk line: what could still be wrong, and how would we know?
