---
name: evolve-skill
description: Use when asked to evolve, improve, tune, or optimise an installed Claude Code skill against a target codebase, or when given a skill name together with a repo to test it on.
---

Improve an installed skill by measuring it, not by rewriting it from intuition.

Inputs: a skill name installed under `~/.claude/skills/`, and a target repo.
Run every command from this repo's root; `packs/` and `runs/` are relative to it.

## 1. Resolve

- Seed: `~/.claude/skills/<name>/SKILL.md` must exist. Refuse any name containing
  `:` (plugin skills are read-only). Stop and say so; never pick a substitute.
- Target repo: must exist. Note its language, build system, and whether it is a
  git checkout (decides how step 2 pins fixtures).
- Read the seed `SKILL.md` in full and list the procedures it teaches. Tasks are
  built from that list.

## 2. Generate the pack

Pack dir: `packs/<skill>-<repo-basename>/`. **If it already exists, do not
regenerate** — a hand-tuned pack is worth more than a fresh one. Skip to step 3.

Read `references/scorer-rules.md` before writing any `verify.sh`, and
`references/task-recipes.md` for task shapes and the file templates.

- 12 tasks, split 5 train / 4 val / 3 test. Every id in exactly one split.
- Every task has `task.yaml`, `prompt.md`, `setup.sh`, `verify.sh`, `solve.sh`.
  `solve.sh` is the reference solution; without it step 3 cannot run.
- **Every task carries the same `tags:` value** (use the skill name). Step 3's
  simulated solver transfers learned fixes between tasks by tag; without a shared
  tag it cannot pass val and the dry run exits 1 with `NO IMPROVEMENT`.
- Tasks span what the seed claims to cover, and at least a third target areas where
  the seed is thin or silent. A seed that already aces val leaves nothing to evolve.
- Fixtures are pinned. Git repo: `setup.sh` extracts a fixed commit with
  `git archive`. Otherwise snapshot into `fixtures/`. Never copy from a live path —
  the gate compares scores across iterations, so a moving target corrupts it.
- `config.yaml` sets `model`, `iterations`, and `budget.run_usd` explicitly. Start
  with `iterations: 4`. Never inherit the $50 default silently.

## 3. Prove the pack before spending anything

    python -m skillforge validate packs/<pack>
    python -m skillforge discriminate packs/<pack>
    python -m skillforge --runs-dir /tmp/sf-dry evolve packs/<pack> \
        --seed <name> --backend fake --iterations 2

Pass means exit 0 on all three. Do not proceed while any fails.

The first proves splits and scorers are wired. The second runs every `verify.sh`
twice — on a bare workspace and after `solve.sh` — and requires `<1.0` then `1.0`.
Only this check catches a scorer that returns the same value regardless of the
work, the failure that teaches the loop to game itself. The third proves the loop
runs end to end without touching the `claude` CLI.

A task reported `BROKEN` has a broken scorer. Regenerate it once; if still broken,
delete it and fix the splits. Never weaken a scorer to make it pass.

Clean up: `chmod -R u+w /tmp/sf-dry && rm -rf /tmp/sf-dry`

## 4. Evolve

The dry run never invoked `claude`. Before spending, confirm `command -v claude`
succeeds and the CLI is logged in.

    python -m skillforge evolve packs/<pack> --seed <name>

Report the run id as soon as it prints. Rollouts per run ≈
`iterations × (train + val) + 2 × val + 3 × test`, plus two agent calls per
iteration — with 5/4/3 and 4 iterations, 53 rollouts and 8 agent calls.

If the run is interrupted or hits `budget_exhausted`, resume it rather than
starting over:

    python -m skillforge evolve packs/<pack> --resume <run-id>

## 5. Read the result

    python -m skillforge report <run-id>

Three test scores: no-skill, seed (the current skill), and final. The only one that
decides anything is **final vs seed**. The `evolve` exit code already encodes it:
0 means final beat seed.

If the report flags **seed already scores 1.0 on val**, the loop stopped itself
after iteration 0. The tasks are too easy. Say that plainly — it is a task
difficulty problem, not a verdict on the skill — and regenerate harder tasks.

## 6. Install only a winner

Install only when `evolve` exited 0.

    mkdir -p ~/.claude/skill-backups
    cp -r ~/.claude/skills/<name> ~/.claude/skill-backups/<name>-$(date +%Y%m%d-%H%M%S)
    ls runs/<run-id>/state/skills/
    python -m skillforge install <run-id> --scope user

Backups live outside `~/.claude/skills/` so skill discovery never sees them.
`install` copies **every** directory listed by `ls` — tell the user exactly which
will be created or overwritten before running it; the backup protects only the
seed. The installed dir gains a harness-written `PURPOSE.md`; leave it.

When `evolve` exited 1, install nothing. Say so, and leave the run dir for
inspection.

## 7. Report

The three scores and the delta; the bootstrap verdict, with the caveat that a
3-task test split rarely reaches significance so it is a confidence estimate, not a
pass/fail; the `SKILL.md` diff; the backup path; total spend; the run directory.

## Rules

- Never edit anything under `~/.claude/plugins/cache/`.
- Never install a skill that did not beat its seed.
- Never back up after overwriting.
- Never regenerate a pack that already exists.
- Run dirs are sealed read-only; deleting one needs `chmod -R u+w` first.
