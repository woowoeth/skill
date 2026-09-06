---
name: code-atlas
description: Code Atlas — generate and grep an AST repo map. Use when locating where a feature is implemented, finding a symbol's file and line range, analyzing the blast radius of a change via reverse references, finding API route definitions and call sites, or checking map freshness / rescanning. 在代码库中找功能实现、查符号定义、看改动影响面、找 API 端点时用。機能の実装場所を探す、シンボル定義、変更の影響範囲、API エンドポイント検索に使う。Supports TS/JS/TSX/JSX, Python, Go, Dart/Flutter, Kotlin/Java/Android, Swift, C/C++. Slash commands: /code-atlas build, /code-atlas check, /code-atlas merge (recipes below).
---

# Code Atlas

Generate and query a repo's AST map: a Markdown index with a freshness header, searched with grep
instead of reading files wholesale. Retrieval techniques live in this directory's README.md
(the tool manual); this file carries only the procedure and the map's semantics.

## Install (first run)

Preferred (npm package): `npm install -g code-atlas && code-atlas install` — the installer copies
the skill into every agent skills directory it detects (`~/.claude/skills`, `~/.agents/skills`,
`~/.codex/skills`, `~/.config/opencode/skills`; when none exists it creates `~/.agents/skills`)
and installs dependencies there.

Manual alternative — clone into the skills directory and install dependencies:
```
git clone <repo-url> ~/.agents/skills/code-atlas && cd ~/.agents/skills/code-atlas && npm install
```
Node >= 18 is the only requirement. Dart grammar prebuilds ship with the package
(macOS arm64/x64 need no toolchain; Linux/Windows fall back to a postinstall source build
until CI prebuilds land, requiring a C toolchain).

## Slash-command recipes

Free-text requests map onto exactly three actions. `<SKILL_DIR>` is the directory holding this
SKILL.md (contains `bin/code-atlas.mjs`); if it has no `node_modules/`, run `npm install` in it first.

### /code-atlas build [目录]

Scan or rebuild the map:
```
node <SKILL_DIR>/bin/code-atlas.mjs -d <dir> -n <module-name> -o <output.md>
```
- `<dir>` defaults to the current repo root; without `-o` the map lands at
  `<dir>/.repo_map_<name>.md` — prefer `docs/ast-maps/<name>-ast-map.md` unless the user gives a path.
- One language only: `--languages dart` (value domain in `--help`); combine maps with `--merge`.
- Done when: stdout prints `✅ Generated` and the header's five fields are non-empty —
  `# Architecture Map` / `# Source Path` / `# Source Commit` / `# Worktree` / `# Languages`.

### /code-atlas check

Freshness check only — report, never rescan:
- Read the existing map's header; compare `# Source Commit:` with `git -C <repo> rev-parse HEAD`
  and `# Worktree:` with `clean`.
- Done when: you answer explicitly **fresh** or **stale** with the evidence, e.g.
  `fresh (commit abc1234, worktree clean)` / `stale (map @abc1234 ≠ HEAD @def5678; worktree dirty)`.
  Reusable only when the commit equals HEAD and the worktree is clean; otherwise run
  `/code-atlas build` before answering location questions from this map.

### /code-atlas merge <地图文件...>

Merge previously generated maps:
```
node <SKILL_DIR>/bin/code-atlas.mjs --merge <map.md ...> -n <name> -o <merged.md>
```
- Done when: stdout prints `✅ Merged`.

## Querying the map

Grep the map file; never read source files wholesale:
- Find a definition: `grep ' <Name>$' map.md` (symbol rows carry `[Lstart-Lend]`, then Read precisely)
- Blast radius: `grep '^🔗 <module-path>' map.md` (reverse references: who imports it)
- File dependencies: `grep '^📁 <file> .*imports(' map.md` (🌐 section)
- API endpoints: `grep '/api/<path>' map.md` (📡 section; api-route definitions / api-call sites, heuristic)
- Library consumers: grep the package name across 🔗/🌐 rows

Done when: every locate-style answer lands on `file:line`, with the line taken from the map or
from a Read the map pointed to.

## Map semantics (consult while querying)

- Symbol section: `📁 <repo-relative-path> [Lstart-Lend] <label> <name>`; label glossary in README.md.
- 🌐 Import graph: file → dependency modules (relative imports normalized to repo-relative paths).
- 🚪 File symbol index: all symbol names per file (truncated past 25).
- 🔗 Reverse references: module ← files importing it (list truncated past 10; provably external
  dependencies collapse to `(N importers, external)`).
- 📡 API paths: heuristic; Dart matching is line-level and misses calls spanning multiple lines.
- ⚠️ Diagnostics: scan-time problems; **when non-empty, weigh it together with any query conclusion**.

## Known boundaries

- Vue SFC / Objective-C have no grammar and are not indexed; TS path aliases (`@/`) are not resolved.
- References not provably external (Python bare names, Java/Kotlin package paths) keep their full
  importer lists in 🔗.
- The map is an index, not ground truth: after locating a line range, Read the code to confirm.
