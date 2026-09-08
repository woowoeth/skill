---
name: check-compiler-errors
description: Run a repository's compiler or type checks and report actionable errors. Fix them only when the user requests repair; use for local compilation or type-check failures, not remote CI monitoring.
---

# Check compiler errors

## Choose the mode

Default to checking and reporting. A request to check, inspect, or explain errors does not request source edits. If the user asks to fix errors, or the current task already includes repairing them, proceed with focused fixes without asking again.

## Workflow

1. Read repository instructions and inspect the working tree. Preserve existing edits and identify the requested package or workspace.
2. Discover the actual commands from project documentation, build configuration, package scripts, or CI configuration. Reuse the project's toolchain and dependency manager. Do not assume TypeScript, npm, or a command called `typecheck`.
3. Prefer a documented check-only command. Inspect wrapper scripts for auto-fix, code generation, dependency updates, or deployment side effects before running them. If only a build is available, identify its generated outputs; checking may create ordinary build/cache artifacts but must not implicitly rewrite source or lockfiles. Do not invent success when no executable check is available.
4. Run the smallest relevant check, capturing the command, working directory, exit code, and diagnostic output. Distinguish compiler errors from missing tools, dependencies, credentials, or a failed environment setup. A timeout or incomplete run is not a pass.
5. Group actionable diagnostics by file and error category. Explain the root error before cascaded errors and identify the exact scope checked. In check mode, report the findings and stop without applying fixes.
6. In repair mode, make the smallest justified source change, preserving intended behavior. Do not hide errors through disabled checks, suppression comments, broad type casts, or weakened compiler settings. Re-run the affected check and any tests needed to verify changed behavior.
7. Stop when the requested checks pass, a product decision or unavailable dependency blocks progress, or a repeated failure yields no new evidence. Avoid unbounded retries or repeated identical commands without a relevant change.

## Scope

This is a local validation workflow. The repository may be hosted on GitHub, GitLab, or neither; no provider API is required. Reporting compiler errors does not imply permission to commit, push, create a PR/MR, or monitor remote CI. Follow any separate repository delivery instructions when those actions are already part of the user's task.

## Output

- State `PASS`, `FAIL`, or `BLOCKED`, with the command and package/workspace actually checked. A failing compiler check is `FAIL`; a check that could not run is `BLOCKED`.
- Group root diagnostics by file/category and give a concrete next step.
- In repair mode, summarize edits and recheck results. In check mode, distinguish proposed fixes from changes actually made.
- Do not claim the whole repository is clean when only one package or check ran.
