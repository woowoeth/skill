---
name: backlog
description: Converts BACKLOG.md inbox items into task files under tasks/, using tasks/_template.md. Use when the user wants to process, triage, or clear their backlog/inbox. Trigger words include "process backlog", "clear my backlog", "จัดการ backlog".
---
1. Read `BACKLOG.md` and list every item under the inbox (skip the header and
   instruction lines, and the two `- ตัวอย่าง:` example lines unless the user
   explicitly wants those processed too).
2. For each real item:
   a. Derive a short slug (lowercase, hyphenated) from the item text.
   b. Create `tasks/<yyyy-mm-dd>-<slug>.md` (today's date) by copying
      `tasks/_template.md` and filling in:
      - title from the item text
      - `status: todo`
      - `created: <today>`
      - `goal:` — link to a matching `## Now`/`## Next` item in `GOALS.md`
        if one clearly applies, else `-`
   c. Leave "Definition of done" and "Verification evidence" for the user to
      refine, but propose a first-draft observable outcome.
3. After creating the task file for an item, remove that item's line from
   `BACKLOG.md`.
4. When all items are processed, summarize what was created: list each new
   `tasks/<file>.md` path with its title and goal link.
5. Never mark a created task `done` — this skill only triages, it does not
   complete work.

Respond to the user in Thai unless they ask otherwise.
