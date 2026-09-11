---
name: inbox-triage
description: Triage the user's email inbox — surface what needs replies, archive the noise, draft responses on request. Use for "check my email", "what's in my inbox", "clean up my inbox", or scheduled inbox sweeps.
---

# Inbox Triage

Turn an unread pile into three clear piles. Requires Gmail (or another mail
toolkit) connected — if it isn't, call `request_connection` first.

## Procedure

1. Fetch recent unread (default: last 24h or since last triage).
2. Classify each into exactly one bucket:
   - **Needs you** — a real person asked something, a deadline moved, an
     invite awaits RSVP. These are the point of the triage.
   - **FYI** — worth knowing, no action. Summarize in one line.
   - **Noise** — newsletters, automated notifications, marketing. Name them
     only as a count ("14 newsletters").
3. Present **Needs you** as cards: sender, subject, what they're asking, and
   how long a reply would take. Offer to draft the top one.
4. Offer bulk actions, never take them unasked: "I can archive the 14
   newsletters — say the word."

## Rules

- Never mark, archive, or delete anything without an explicit user instruction.
  Triage reads; it does not touch.
- Quote the actual ask when summarizing — "Maya: can you send the one-pager by
  Friday?" beats "Maya emailed about the one-pager".
- If the inbox is empty or all noise, say so in one line and stop. A clean
  inbox is a result, not a failure.
