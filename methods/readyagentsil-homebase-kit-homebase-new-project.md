---
name: homebase-new-project
description: Start a brand-new project the HomeBase way. Use when the user says "new project", "start a repo", "set up a project", "create a new app", or opens an empty folder and wants it wired up. Asks the few questions only they can answer, then creates the GitHub repo, the short CLAUDE.md, the sharded CI, the two watchers, branch protection and the INDEX row, and proves it with a green first run.
---

# New project, the HomeBase way

One pass, no follow-ups. The result is a repo where the first PR already runs the parallel
CI, the aggregate `ci` check gates `main`, the watchers exist, and HomeBase knows about it.

## 1. Ask, as one form, only what you cannot infer

Ask these together in one message (the user prefers a form to a chat), with sensible defaults
shown so a blank answer is fine:

| Question | Default |
|---|---|
| Project name (repo name, kebab-case) | required |
| One-line description | required |
| GitHub owner (org or user) | the paid org if the login belongs to one (`gh api user/orgs --jq '.[].login'`, then `gh api orgs/<org> --jq .plan.name`); else the user |
| Visibility | private |
| Stack | node (also: python, go, other) |
| Local path | `~/<project-name>` |
| Parent venture / group, or standalone | standalone |
| Does the test suite need a database? | no |
| Test shards | 4 |

Infer everything else. Check the plan before promising Enterprise features:
`gh api orgs/<owner> --jq .plan.name` (a user account answers with an error; treat as free).

## 2. Create the repo and the skeleton

```bash
mkdir -p <path> && cd <path> && git init -b main
gh repo create <owner>/<name> --<visibility> --description "<one line>" --source=. --remote=origin
```

Then, from `~/HomeBase/templates/`:

- `project-claude-md.md` → `CLAUDE.md`. Fill status, stack, run and test commands, and leave
  only the pointer rows for docs that exist. Under 200 lines, always.
- `docs-history.md` → `docs/history/README.md`, first entry "repo created" with the date.
- `docs/plans/` with an empty `README.md` saying one doc per batch of work, asks recorded
  verbatim the turn they arrive.
- `rules/EXAMPLE-migrations.md` → `.claude/rules/` only if the stack has migrations; else skip.
- `ci/ci.yml` → `.github/workflows/ci.yml`, with the `# ADJUST` lines set for the stack,
  the database service uncommented if needed, and the shard count set in all three places.
- `ci/ci-watch.sh` and `ci/pr-watch.sh` → `tools/`, `chmod +x`.
- A minimal runnable project for the stack: for node, `package.json` with `lint`,
  `typecheck` and `test` scripts and one real passing test, so the first CI run is green for
  a real reason, not an empty one. Never ship a `test` script that exits 0 without running
  anything: the shard-parity step refuses a shard with zero tests, on purpose.
- `.gitignore` for the stack.

## 3. Protect `main` and set the merge rules

Push first (`git add -A && git commit -m "…" && git push -u origin main`), then:

```bash
gh repo edit <owner>/<name> --enable-auto-merge --delete-branch-on-merge --enable-squash-merge --enable-merge-commit=false --enable-rebase-merge=false
```

```bash
gh api -X PUT repos/<owner>/<name>/branches/main/protection --input - <<'EOF'
{"required_status_checks":{"strict":true,"contexts":["ci"]},
 "enforce_admins":false,"required_pull_request_reviews":null,"restrictions":null,
 "required_linear_history":true,"allow_force_pushes":false,"allow_deletions":false}
EOF
```

If the protection call answers 403 ("upgrade to Pro or make this repository public"), the
repo is private under a free personal account. Say so plainly, and offer the two real fixes
(recreate under the paid org, or make it public). If the user declines both, record in the
project's `CLAUDE.md` that `pr-watch.sh` is the gate: it detects the missing protection and
merges only when every check on the head is green, instead of arming auto-merge.

On Enterprise Cloud, also try a merge-queue ruleset; if the API refuses, the baseline above is
the answer and say so. The template's `on: merge_group:` trigger is what makes the queue work;
never remove it:

```bash
gh api -X POST repos/<owner>/<name>/rulesets --input - <<'EOF'
{"name":"main merge queue","target":"branch","enforcement":"active",
 "conditions":{"ref_name":{"include":["refs/heads/main"],"exclude":[]}},
 "rules":[{"type":"merge_queue","parameters":{"merge_method":"SQUASH","max_entries_to_build":5,
   "min_entries_to_merge":1,"max_entries_to_merge":5,"min_entries_to_merge_wait_minutes":1,
   "grouping_strategy":"ALLGREEN","check_response_timeout_minutes":60}}]}
EOF
```

## 4. Prove it with a real PR

Open a branch with a one-line change, push, open a PR, and run the CI watcher harness-tracked:

```bash
tools/ci-watch.sh <pr-number>
```

Its exit is the proof. When it exits 0, arm the merge watcher the same way:

```bash
tools/pr-watch.sh <pr-number>
```

When that exits 0 the PR is merged and the train works. If either exits nonzero, fix the cause
in this session; do not report "set up" with a red first run.

## 5. Put it on the map

- Add the row to `~/HomeBase/INDEX.md` (name, path, status "building", one line).
- If it belongs to a venture, add it under that venture in `~/HomeBase/context/company.md`.
- One dated line in `~/HomeBase/decisions/log.md` if a real decision was made (stack, owner).
- Run `claude-md-doctor` in the new repo and show the table.

## 6. Report

One table: repo URL, CI run URL (green), protection applied (baseline or merge queue), PR
merged, INDEX row added. Then hand over to spec-driven planning (for example the GSD
`new-project` flow) for what the project should actually do.
