---
name: environment-probe
description: Probe a fresh sandbox or cloud dev box in under a minute, confirm what is already known about it, write the findings to a notes file, and report before any code is written. Use at the very start of a session, and again if a run command or port stops working.
---

# Environment probe

Goal: in one command, learn what this box has, write it down, and report it in five lines. No code, no installs, no fixes during the probe.

## Step 0: bring the skills onto the box

Attachments live only in the current chat; files on disk live for the whole session and can be @-mentioned from any chat. So the first command of the session is:

```bash
[ -d .agent/skills ] || git clone -q --depth 1 https://github.com/arthurkatcher/agent-skills .agent/skills; ls .agent/skills
```

If the clone fails (no network), say so in one line and ask me to attach the SKILL.md files instead. Do not retry more than once.

Skills on the box after that:

- `.agent/skills/environment-probe/SKILL.md` this file.
- `.agent/skills/coding-practices/SKILL.md` how code gets written, tested, and reviewed. Read it before any code.
- `.agent/skills/docs-lookup/SKILL.md` current library docs from the terminal, when an API is uncertain.

Reference them by path in every new chat. Frame requests as coding work ("run the probe", "implement slice 1 per the notes").

## Step 1: run the probe

```bash
bash .agent/skills/environment-probe/scripts/probe.sh
```

Read-only. Prints runtime versions, files, tasks.json, README run lines, package manifests, ports, sudo, CPU/RAM/disk, network reachability (npm, PyPI, GitHub, docs API), and which services exist.

## Step 2: write the notes file

Create `.agent/NOTES.md` and put the five-line report in it under a `## Environment` heading. This file is the session's memory: every new chat reads it first, and every finished slice appends to it. Sections, in order:

```markdown
## Environment      the five-line report from the probe
## Task             the task restated in one paragraph, plus explicit out-of-scope
## Plan             numbered slices, each with its acceptance check
## Log              one line per finished slice: what shipped, test command run, result
## Open risks       what could still be wrong, and how we would know
```

Rules for the notes: append, do not rewrite history. Keep each entry to one or two lines. When a chat starts with "read the notes", the first action is to read `.agent/NOTES.md` and say in one line where the work stands.

## Step 3: report (five lines, nothing else)

1. Runtime: which of Node / Python is present, versions.
2. Scaffold: empty root, or what is already there (app, tests, README, tasks.json) and the documented run command.
3. Preview: which port the run command uses, and whether it is one of the open ports.
4. Network and sudo: yes/no each.
5. Recommendation: the stack for this task in one sentence, using what is already installed.

Then stop and wait for the plan.

## Share a running app (only when asked, last minutes)

```bash
bash .agent/skills/environment-probe/scripts/share.sh 8000
```

Prints a public `https://….trycloudflare.com` URL for the app on that port. No account or token involved. Start it in a second terminal tab.

## Postgres on the box (only if the task needs it; SQLite is the default)

```bash
bash .agent/skills/environment-probe/scripts/postgres.sh 5432 app
```

Installs PostgreSQL via apt (disabling the broken third-party apt source first), starts it on the given port, creates role and database `app`/`app`, and prints `DATABASE_URL`. About two minutes. Report the last three lines of its output.

## Known facts about this kind of sandbox (verify with the probe, do not re-derive)

- Project root is `/projects/challenge` on this platform. The "run project" terminal tab runs `.vscode/tasks.json`. The root is a git repo; the Diff pane shows the working tree against HEAD, so commit per finished slice.
- 2 vCPU, 12 GB RAM, ~13 GB disk. Passwordless sudo, apt-get works.
- Full outbound internet: npm, PyPI, GitHub, raw.githubusercontent.com, context7.com.
- Python images: Python 3.13 + uv + git, Node may be absent. Node images ship their own Node. Installing Node via apt takes ~2 min and gives Node 18; last resort only.
- No Docker, Postgres, or Redis. Everything runs in-process.
- Browser pane renders what listens on 3000, 3030, 5000, 6001, 8000 or 8080. Bind to 0.0.0.0.
- SQLite is the default store. Python `sqlite3` is built in. Node: `npm i sqlite3` (prebuilt) works; `better-sqlite3` fails on Node 18; Node 22+ has `node:sqlite`.
- `npm i` and `uv pip install` are fast. Every dependency needs a one-line reason.

## Rules during the probe and after

- Do not touch environment variables that are not ours. Platform keys in the env belong to the sandbox assistant, not the task.
- Do not install global tooling "to be safe". Install what the current slice needs, when it needs it.
- One server per port. `pkill -f "node|flask|uvicorn"` before a restart.
