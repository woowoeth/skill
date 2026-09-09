---
name: kit-setup
description: Configure this kit for your own forge, tracker, and project layout — writes ~/.claude/kit.env, generates your CLAUDE.md from the template, and verifies the result. Use when adopting the kit on a new machine or pointing it at different infrastructure.
user-invocable: true
argument-hint: ""
---

# Kit Setup

Point the kit at the adopter's infrastructure. This produces **two files they
own** and touches nothing else:

- `~/.claude/kit.env` — the configuration `lib/kit.sh` reads on every call
- `<projects-root>/CLAUDE.md` — their conventions, generated from
  `reference/CLAUDE.md.template`

## What this skill must NOT do

**Never rewrite the kit's own `agents/`, `commands/`, or `skills/` files.**

It is tempting — the prose in those files mentions Gitea, containers, and
1Password — but rewriting them is a trap:

- They are the *upstream source*. An adopter whose copies were rewritten in
  place can never pull an update without a merge conflict in every file.
- The variable parts are not find-and-replace. `/rollout`'s deploy section is a
  set of alternatives that the model chooses between at runtime by inspecting
  the repo. Replacing that with one branch makes it *less* capable, not more.
- These files are instructions for a model, not code. A model reads "if the repo
  has a CI workflow, watch the run; if it needs secrets you can't inject, hand
  the user the command" and picks correctly. That conditional is the feature.

So: generate configuration and generate their CLAUDE.md. Leave the kit alone.

## Step 1: Detect what you can, ask only what's left

Look before asking. Infer and then confirm, rather than interrogating:

```bash
command -v gh && gh auth status          # GitHub CLI present and authenticated?
ls ~/.gitea-token 2>/dev/null            # a Gitea token on disk?
git -C . remote get-url origin           # what forge does the current repo use?
ls -d ~/*/ | head -20                    # plausible project roots
```

Ask about anything you could not determine. Keep it to one round of questions:

- **Projects root** — where do projects live? (`KIT_PROJECTS_ROOT`; colon-separated
  if more than one)
- **Forge** — Gitea or GitHub? Which org or user owns the repos?
- **Tracker** — `tasks-md` (a `TASKS.md` per project, nothing to install) or
  `todolist`? Default to `tasks-md` unless they already run a tracker.
- **Secrets** — how do production secrets reach a running process? A secret
  manager's `run` wrapper, CI-injected, or a local `.env`?
- **Tests** — the command that runs the test suite.

## Step 2: Write `~/.claude/kit.env`

Use the `: "${VAR:=value}"` form throughout, so an explicitly exported variable
still overrides the file. Write only the variables that differ from the
defaults, and never a credential — a token belongs in a file the config
*points at*.

```bash
mkdir -p ~/.claude
cat > ~/.claude/kit.env <<'EOF'
# Written by /kit-setup. Read by lib/kit.sh on every call.
# Uses := so anything exported in the environment still wins.

: "${KIT_PROJECTS_ROOT:=$HOME/code}"
: "${KIT_FORGE:=github}"
: "${KIT_FORGE_ORG:=your-org}"
: "${KIT_TRACKER:=tasks-md}"
EOF
```

Confirm it took effect — this prints the resolved configuration and whether each
credential file is readable, never a credential itself:

```bash
source "${KIT_LIB:-$HOME/.claude/lib/kit.sh}" && kit_config
```

## Step 3: Generate their CLAUDE.md

Copy `reference/CLAUDE.md.template` to the projects root and fill every
`<PLACEHOLDER>` from the answers in step 1.

**Delete the sections that do not apply.** An instruction describing
infrastructure they do not run is worse than no instruction, because an agent
will try to follow it. If they have no test/prod split, cut the environments
table. If secrets are CI-injected, cut the local secrets section.

Show them the result and get approval before writing it — this file governs
every future session in that tree.

## Step 4: Verify, and be honest about what is unverified

```bash
scripts/selfcheck.sh                  # dry run: every function, every backend
scripts/selfcheck.sh --live --repo <them>/<throwaway>   # only with their say-so
```

The dry run proves the calls are well-formed. It does **not** prove they work
against their forge — only `--live` against a throwaway repo does that. Say
which of the two you ran.

Then offer the smallest real exercise:

```bash
scripts/init-project.sh <a-throwaway-name>
```

That creates the three-worktree layout, the remote repo, and branch protection —
the whole PR-only guarantee — in one command they can inspect and delete.

## Step 5: Report

Tell them:

- The two files created, and what each controls
- Their effective configuration (`kit_config`)
- **What is still theirs to fill in** — the `<PLACEHOLDER>`s you could not answer
  and any CLAUDE.md section you left as a stub
- Whether branch protection actually applied. On GitHub it needs admin, and
  private repos need a paid plan; when it fails, PR-only merges become a
  convention the agents follow rather than a rule the forge enforces. That
  distinction matters and should not be glossed.
