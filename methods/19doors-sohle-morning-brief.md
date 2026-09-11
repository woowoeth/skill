---
name: morning-brief
description: Compile a morning briefing across the user's connected tools — overnight email, today's calendar, urgent items. Use when asked for a brief, digest, summary of the day, or when running as a scheduled morning task.
---

# Morning Brief

Produce a briefing the user can act on in under two minutes. It runs when they
may have just woken up — lead with what changed overnight, not with greetings.

## Gather

Use whichever of these are connected; skip the rest silently:

1. **Calendar** (googlecalendar) — today's events, with times in the user's
   timezone. Note gaps: "45 min free between 11:00 and 12:30".
2. **Gmail** — unread/overnight mail. Rank by sender importance and urgency
   cues (deadline words, direct questions, calendar invites).
3. **Notion** — pages edited since yesterday that mention the user or are due.
4. **GitHub** — PRs awaiting the user's review, failed CI on their branches.
5. **Slack** — unread mentions and DMs only, not channel noise.

## Compose

- **Headline** (one line): the single most important thing. If nothing is
  urgent, say so plainly — never manufacture urgency.
- **"Overnight, N things changed"** — one card per item: what it is, who it's
  from, why it matters, in at most two sentences each.
- **Today** — the calendar as a tight list with times.
- **One suggestion** — the highest-leverage next action you can take for them
  ("I can draft the reply to Maya — say go"). Exactly one.

## Rules

- Total length: short. This is a scan, not a report.
- Times always in the user's timezone.
- If a source errors or is empty, omit it — don't narrate failures.
- When running as a scheduled task, end by asking nothing; the user reads this
  asynchronously. A single offered action is fine, a question battery is not.
