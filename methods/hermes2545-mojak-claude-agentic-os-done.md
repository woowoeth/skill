---
name: done
description: Verification-first task completion — gathers fresh evidence before marking a task done and archiving it. Use when the user says a task is finished or wants to close it out. Trigger words include "done", "mark this complete", "ปิดงาน", "เสร็จแล้ว".
---
1. Identify the task file in `tasks/` the user means; read its
   "Definition of done" section in full.
2. For each observable outcome listed, gather FRESH evidence right now —
   run the actual command, test, or fetch; do not reuse older output or take
   the user's word for it.
3. For nontrivial or code-related tasks, optionally spawn the `reviewer`
   subagent to adversarially check the diff and the evidence before
   proceeding.
4. Paste the fresh evidence (command + output, or URL fetch result) into the
   task file's "## Verification evidence (required before done)" section.
5. If any definition-of-done item lacks evidence or the evidence is stale/
   fabricated-looking, refuse to mark it done — tell the user exactly what's
   missing and stop here.
6. Once all items are verified: set `status: done` in the task file, then
   move the file to `tasks/archive/`.
7. Confirm to the user what was verified and where the archived file now
   lives.

Respond to the user in Thai unless they ask otherwise.
