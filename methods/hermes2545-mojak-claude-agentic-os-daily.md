---
name: daily
description: Start-of-day planning routine — reads GOALS.md, BACKLOG.md, and open tasks/, then proposes today's top 3 priorities with a verification plan each. Use when the user wants to start their day or plan what to work on. Trigger words include "daily", "start my day", "เริ่มวัน", "วันนี้ทำอะไรดี".
---
1. Read `GOALS.md` in full (Now / Next / Someday).
2. Read `BACKLOG.md` and note how many items are waiting.
3. List open tasks: every file in `tasks/` (not `tasks/archive/`) whose
   `status` is not `done`.
4. Cross-reference open tasks and backlog items against `GOALS.md` → `## Now`
   to judge priority. Prefer tasks that serve a current goal.
5. Propose today's top 3 priorities. For each, include:
   - what it is and why it's a priority today (link to a GOALS.md item or
     task file path)
   - a concrete verification plan (what command/output will prove it's done)
6. If `BACKLOG.md` has unprocessed items, offer to run `/backlog` to convert
   them into task files.
7. Do not create or edit any files yourself in this skill — this is a
   read-and-propose step; act only if the user confirms a next step.

Respond to the user in Thai unless they ask otherwise.
