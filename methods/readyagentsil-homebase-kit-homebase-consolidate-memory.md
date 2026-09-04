---
name: homebase-consolidate-memory
description: The daily memory-consolidation routine. Use when asked to consolidate, tidy, dedupe or audit Claude's memory, or when run unattended by the scheduled homebase-consolidate job. Merges duplicates, fixes stale facts, captures what recent sessions decided, keeps the index small, and reports what changed.
---

# Consolidate memory

A reflective pass over the persistent memory so every future session starts from context
that is true, compact and current. This is judgement work, not tidying: what is durable versus
dated, what to merge, what to drop. Run it on the strongest model available.

## 0. Before touching anything

- **Say which model you are.** If it is not the strongest tier (Opus), still do the full
  routine, then say so plainly in the report. Never pass silently.
- **Find the memory.** Auto-memory lives under `~/.claude/projects/<project-slug>/memory/`
  (one folder per project; the HomeBase one is the hub). `MEMORY.md` in each is the index
  that loads at session start: one line per memory, never content.
- **Work file by file, and finish each file before starting the next.** A run can die
  mid-way (rate limit, overload, a lost connection). A half-rewritten file is worse than an
  untouched one. Write the whole file, then move on. Write the report last.

## 1. Read

Read `MEMORY.md` and skim every memory file. Note duplicates, contradictions, anything dated
that has since changed, anything referencing a file, flag or command that no longer exists
(check before you keep it).

## 2. Capture what is missing

Look at recent work for decisions, preferences, standing rules and lessons that are not yet in
memory: the last few days of session transcripts under `~/.claude/projects/*/` (read the user
turns and the assistant's final summaries, not tool output), `~/HomeBase/decisions/log.md`,
`~/HomeBase/lessons.md`, and git history of `~/HomeBase`. A decision that lives only in a
conversation is a decision that gets re-litigated.

## 3. Write, in the memory format

One fact per file, frontmatter with `name`, `description`, `metadata.type` (user | feedback |
project | reference). For feedback and project entries include **Why:** and **How to apply:**.
Link related memories with `[[name]]`. Convert relative dates to absolute. Prefer updating an
existing file over creating a near-duplicate; merge overlapping files into the richer one and
delete the other. Delete what is wrong. Store evergreen context only: never secrets, tokens,
leads, emails, or customer records.

## 4. Keep it small

`MEMORY.md` stays under 200 lines and 25KB: one line per memory with a hook that says when
it matters. Retire memories that a rule, a test or a hook now enforces (the enforcement is the
memory at that point). Compress, don't accumulate. Run `claude-md-doctor ~/.claude` and make
sure the always-on rules stay within budget too.

## 5. Verify, then report

- Every `[[link]]` in every file points at an existing `name:`.
- Every file in the folder has one line in `MEMORY.md`, and no line points at a missing file.
- Frontmatter parses on every file.

Then a short report: files merged, created, updated, deleted; facts captured; the model you
ran on; anything you could not resolve. If nothing needed changing, say that in one line.

## Unattended rules (the scheduled run)

Nobody is present to answer a prompt. The runner opens the session with all permission
prompts bypassed and a watchdog, so: no compound shell pipelines for inspection (read with
Read, search with Grep and Glob, compute with a single script), no interactive commands, no
questions to the user. If the very first response is a rate-limit or overload message, that
message IS the finding: write it to the report and stop, touching nothing.
