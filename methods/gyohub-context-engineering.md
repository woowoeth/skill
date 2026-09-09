---
name: context-engineering
description: Scaffolds a portable context-engineering kit to cut coding-agent token waste: AGENTS.md, scoped rules, .agents/skills (bug-fix, test-targeted, log-triage), compression scripts, and thin Cursor/Claude Code/Copilot/Antigravity adapters. Use when starting a project, setting up context engineering, AGENTS.md, CLAUDE.md, token efficiency, Agent Skills, or generating agent files and folders in Cursor, Claude Code, or Google Antigravity.
---

# Context Engineering Kit

Scaffolds the ebook's layered architecture into the target project: a short persistent contract, scoped rules, on-demand skills, and scripts that compress evidence before it becomes context.

Works in **Cursor**, **Claude Code**, and **Google Antigravity**. Shared source of truth: `AGENTS.md` + `.agents/skills/`. Keep tool adapters thin. Do not copy the same text into five files.

To **work** in a repo that already has the kit, use the sibling skill `context-engineering-work` — not this one.

## Where this skill must live

| Tool | Personal install | Invoke |
|---|---|---|
| Cursor | `~/.cursor/skills/context-engineering/` | `/context-engineering` |
| Claude Code | `~/.claude/skills/context-engineering/` | `/context-engineering` |
| Antigravity | `~/.gemini/config/skills/` and `~/.gemini/antigravity/skills/` | `/context-engineering` |

Claude Code does **not** read `~/.cursor/skills/` or user-level `.agents/skills/`. Without a copy in `~/.claude/skills/`, this skill will not appear in Claude.

Antigravity discovers **workspace** skills in `.agents/skills/` (the kit source). The scaffold skill itself must be installed globally. Nested `SKILL.md` files inside this package are named `SKILL.template.md` so Antigravity does not steal the `/context-engineering` slash command. The slash name is exactly `/context-engineering`.

Install for all tools:

```bash
bash "<skill-dir>/scripts/install.sh"
```

`<skill-dir>` = the directory that contains this `SKILL.md`.

## When to apply

- New project or a repo without `AGENTS.md` / `.agents/skills/`
- Request to cut token waste, set up context engineering, or configure the agent
- Request to generate `AGENTS.md`, rules, skills, or multi-agent adapters

## Workflow

Copy and track:

```
Kit Progress:
- [ ] 1. Resolve target and inventory
- [ ] 2. Detect stack
- [ ] 3. Run scaffold (do not invent files from memory)
- [ ] 4. Adapt the minimum to the project
- [ ] 5. Domain skills only if asked or the pattern already repeats
- [ ] 6. Report what was created and what was left out
```

### 1. Resolve target and inventory

Target = project directory (cwd unless the user names another path).

List what already exists; do not read full file bodies:

- `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`
- `.cursor/rules/`, `.claude/rules/`, `.agents/rules/`, `.github/instructions/`
- `.agents/skills/` (source + Antigravity discovery), `.claude/skills/` (Claude), `.github/skills/`

**Do not overwrite** an existing file without confirmation. The scaffold skips conflicts; use `--force` only if the user asks.

### 2. Detect stack

Quick signals (do not walk the whole repo):

| Signal | Extra rule |
|---|---|
| `tsconfig.json` / `*.ts` | `typescript` |
| `package.json` with React/Next/Remix/Vite | `react` |
| `package.json` without TS | `javascript` |
| `pyproject.toml` / `requirements.txt` | `python` |
| `pom.xml` / `build.gradle*` | `java` |
| `go.mod` | `go` |
| Prisma, Drizzle, TypeORM, SQLAlchemy, JPA, Flyway | `database` |
| auth, payment, billing, crypto in the code | `security` |

Always generate: `token-efficiency` + the three skills + scripts.

Mapping details: [references/stack-map.md](references/stack-map.md).

### 3. Run the scaffold

Skill path = the directory of this `SKILL.md`.

```bash
bash "<skill-dir>/scripts/scaffold.sh" --target "<project-root>"
```

Options:

| Flag | Effect |
|---|---|
| `--rules typescript,react,database` | Force rules (skip detection) |
| `--adapters cursor,claude,copilot,antigravity` | Which thin adapters to create (default: all four) |
| `--force` | Overwrite existing files |
| `--dry-run` | List planned writes only |

The script copies templates and installs:

```
AGENTS.md
.cursor/rules/token-efficiency.mdc
.cursor/rules/<stack>.mdc
.agents/skills/{bug-fix,test-targeted,log-triage}/     # Cursor, Copilot, Antigravity
.agents/rules/token-efficiency.md                      # Antigravity always_on
.agents/rules/<stack>.md                               # Antigravity trigger: glob
.claude/skills/<name> -> ../../.agents/skills/<name>   # Claude Code discovers only here
.claude/rules/<stack>.md                               # paths:; do not copy the contract
scripts/context/{test-compact,log-skim,diff-stat}.sh
CLAUDE.md          # @AGENTS.md + pointer; Claude reads CLAUDE.md, not AGENTS.md
.github/copilot-instructions.md
```

Do not create `.github/skills/`. Do not copy skill bodies into `.claude/skills/` — **symlink** (fall back to a copy only if `ln` fails). Do not copy skills into `.agent/skills/` (legacy Antigravity path).

Do not create `docs/architecture.md` or product dumps. That invites the agent to read an encyclopedia.

### 4. Adapt the minimum

After scaffold, change only what the template cannot know:

1. Canonical test command in `test-targeted` (the script already tries to detect it).
2. Scoped-rule globs if the code is not under default paths.
3. In `AGENTS.md`, at most 1–2 non-obvious repo constraints. **Cap: ~250 words.** Strip architecture, schema, runbooks, and external APIs if someone tries to add them.

`CLAUDE.md` imports `@AGENTS.md` (Claude Code does not read `AGENTS.md` on its own). `.claude/rules/` mirrors scoped rules only, with `paths:`. `.agents/rules/` is the Antigravity native rule layer (`trigger: always_on` / `glob`). Do not paste the contract into `CLAUDE.md` again.

### 5. Domain skills

Do not generate them on the first setup. Create only when:

- the user asks explicitly, or
- a module already needs the same procedure on repeating tasks (checkout, ingestion, billing, etc.)

For each domain skill: copy [templates/skills/_domain/SKILL.template.md](templates/skills/_domain/SKILL.template.md) to `.agents/skills/<name>/SKILL.md`, set `name`/`description` (include a concrete “Use when…”), keep the body short, add a script or `references/` only if it compresses context. Without that skill, the agent does not load that domain.

### 6. Final report

Keep it short:

- files created
- files skipped (already existed)
- detected stack
- configured test command
- what was left out on purpose (product docs, domain skills, per-IDE copies)

## Golden rules when generating

- Persistent = universal behavior. Conditional = globbed rule or skill.
- If an instruction matters in ~10% of tasks, it does not belong in `AGENTS.md`.
- Scripts process the deterministic work (log, diff, test). The LLM reasons on the slice.
- Compatibility ≠ copying 200 lines into five files.

## Do not

- Turn prompts into images, “caveman” phrasing that drops intent, or minification that strips semantics
- Attach extra files “just in case”
- Put schema, deploy, or long examples in the global rule
- Default to the full test suite
