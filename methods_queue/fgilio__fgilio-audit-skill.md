---
name: fgilio-audit
description: >
  Coordinated, audit-only search for materially useful simplifications in data
  structures, state representation, control flow, algorithms, and ownership.
  Use when: asked to audit code for simplifications, review a PR/branch/project
  for structural complexity, or validate a multi-project feature end-to-end.
  Never edits files, runs tests, commits, or pushes.
argument-hint: "[--scope=changes|branch|project|feature] [<PR number or URL>] [<repo paths for feature scope>]"
user-invocable: true
disable-model-invocation: true
---

# fgilio-audit

An audit-only exercise. You are the coordinator: build a coverage contract, fan out bounded read-only reviews, independently verify every finding, then audit the audit. The prompt text per scope lives in `prompts/` and is the source of truth; this file only picks the scope and states the shared rules.

Based on **Aaron Francis's "Audit your codebase"** prompt (https://gist.github.com/aarondfrancis/8735edbe48532f97ee5ea818db4dbd47). `prompts/project.md` is his text verbatim; the other scopes derive from it. Full provenance: `reference.md`.

## Parsing arguments

`$ARGUMENTS` carries the invocation. Resolve:

1. **Scope** — the value of `--scope=…` if present. Accept the bare word too (`fgilio-audit branch`).
   - `changes` (default): the current or last changes. Use the uncommitted diff (staged + unstaged) if the working tree is dirty; otherwise the last commit (`HEAD~1..HEAD`). Runs `prompts/branch.md` with that diff as the PR scope.
   - `branch`: the current branch against its merge base with the target branch, and its open PR if any. Runs `prompts/branch.md`.
   - `project`: the entire codebase. Runs `prompts/project.md`.
   - `feature`: one feature implemented across several repositories, one branch/PR each. Runs `prompts/feature.md`.
2. **Target PR** (`branch` scope) — a PR number or URL if given; otherwise the open PR for the current branch, if any. Without a PR, the merge-base diff alone defines scope.
3. **Repositories** (`feature` scope) — paths or names given as arguments. If none, ask via AskUserQuestion which repos and branches make up the feature; do not guess.

State the resolved scope (and diff range, PR, or repo list) in one line before you begin.

## Shared rules (all scopes)

- Read-only. Do not edit files, run tests, implement recommendations, commit, or push. Inspection commands (`git diff`, `git log`, `grep`, reading files) are allowed.
- Workers: fresh read-only agents (Explore or general-purpose with an explicit "do not modify" brief), one distinct area each, non-overlapping boundaries. Bound concurrency to what you can coordinate. Do not interrupt slow-but-productive workers.
- The canonical scratchpad/report goes in the session scratchpad directory (`audit.md`). Never write it into the repository.
- The coordinator verifies every finding against the actual code before accepting it. Reject, narrow, or demote anything vague, duplicated, misread, out of scope, or that merely relocates complexity.
- Every accepted finding carries the full schema its prompt defines (verdict, evidence with file:line, complexity, proposal, scope, risk, validation, confidence, plus the scope-specific fields).

## Running the audit

1. Read the prompt file for the resolved scope in full.
2. Follow its numbered phases in order. For `changes`, substitute the resolved diff range wherever the prompt says "the PR" or "the diff".
3. Finish with the ranked recommendations and best first implementation slices, exactly as the prompt's completion criteria require.

## Output

Present the final report to the user: inventory summary, ranked findings (cross-project first when `feature`), explicit skips, and first slices. Keep the full scratchpad at hand in case the user wants the audit log. Write no code.
