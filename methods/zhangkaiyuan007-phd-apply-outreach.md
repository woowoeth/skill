---
name: outreach
description: This skill should be used when a student asks to "email a professor", "contact a potential advisor", "write to a PhD supervisor", "should I email this professor", "cold email for PhD", "follow up with a professor", or runs /outreach. It reads each professor's own page on the day to decide whether an email is welcome, required in a set format, optional, routed to a form, or unwanted; then drafts one email per professor around one paper the student confirms reading, in the shape of the emails universities publish as good, and keeps a sent log with a single permitted follow-up. It never emails anyone whose page says not to, never templates across professors, and never claims the student read a paper.
argument-hint: "[<professor id or name> | list | status | follow-up <id>]"
allowed-tools:
  - Bash(node ${CLAUDE_SKILL_DIR}/scripts/*)
  - Bash(ls *)
---

# /outreach — contacting professors

The first decision is whether to send an email at all. Most US robotics and machine-learning faculty pages read in the research say not to and ask to be named in the statement of purpose; every Hong Kong page invites email in a set format; Singapore splits by institution. So the skill routes first, from the professor's page read on the day, and only then drafts: one professor at a time, one paper the student has actually read, one ask, one screen.

Part of the `phd-apply` plugin. Skill directory: `${CLAUDE_SKILL_DIR}`; shared helpers in `${CLAUDE_PLUGIN_ROOT}/lib/`. Data home `~/.phd-apply/` (override with `PHD_APPLY_HOME`):

```
~/.phd-apply/cache/professors/<id>.json   findaphd records; this skill adds email_policy
~/.phd-apply/outreach/<id>/               scan-<date>.json, policy.json, draft.md, draft.json, sop-paragraph.md, sent.json, sent-<date>.md
~/.phd-apply/outreach/status.md           every professor: route, sent, replies, next step
~/.phd-apply/documents/cv/cv-<region>.pdf the CV to attach (from /cv)
```

Arguments: `$ARGUMENTS`

- nothing or `list` → `node ${CLAUDE_SKILL_DIR}/scripts/policy.mjs --list`, then ask which professor to start with (suggest the top of the latest findaphd report).
- a professor id or name → the per-professor flow below.
- `status` → `node ${CLAUDE_SKILL_DIR}/scripts/log.mjs status`.
- `follow-up <id>` → Phase 4.

Speak the student's language. Tone: a senior labmate who has sent and received these emails, short and concrete, one `💡 Tip:` line per step.

## Phase 1 — Route (read the page today)

```bash
node ${CLAUDE_SKILL_DIR}/scripts/policy.mjs <id>
```

The scan fetches the homepage, lab page, university profile and any linked join/prospective/opportunities/contact page, and prints every sentence that looks like a contact rule, the email addresses and forms it saw, and the admission model for the institution. Read the sentences and classify per `${CLAUDE_SKILL_DIR}/references/routing.md`: `do_not_email`, `email_required_format`, `email_optional`, `form`, `unknown` (page read, silent) or `blocked`. If a page came back `blocked`, `js_only` or `unreachable`, do not guess: give the student the URL, ask what it says, and record it with `--reader student`. Blocked is not absent.

```bash
node ${CLAUDE_SKILL_DIR}/scripts/policy.mjs <id> --set --classification email_required_format \
  --quote "<the sentence, verbatim>" --url <page> --subject "phd application" --attachments CV,transcript --details nationality --contact-email <addr>
```

Tell the student the route in one sentence with the quote. For `do_not_email`, say so plainly and move to the statement paragraph; for `form`, give the URL.

💡 Tip: "Hiring signal: unknown" from findaphd means nothing was stated, not that they are closed; the ask in the email is how you find out.

## Phase 2 — The paper and the student's words

Show the record's recent papers (`research.recent_publications`, with links). Ask which one the student has read. If none, stop: suggest the two most relevant and wait; the skill never writes "I read your paper" for an unread paper. When they have read one, ask what they thought, in one or two sentences, and use their sentence as written.

Then the experience paragraph: two to four sentences in the student's own words about what they built and the result, closest first to this professor's work. Offer the profile's research bullets as raw material, never as the paragraph. Save a reusable version to `profile.outreach.experience_paragraph` if they want, and edit it per professor.

If the page says to contact only with "specific questions or research ideas", ask for the question; without one there is no email.

💡 Tip: One sentence that shows you understood the paper beats three that praise it.

## Phase 3 — Draft, check, send, log

```bash
node ${CLAUDE_SKILL_DIR}/scripts/draft.mjs <id> --paper "<title fragment or n>" --reaction "<their sentence>" --experience "<their paragraph>" [--question "..."] [--term "autumn 2028"] [--nationality "..."]
```

The script assembles the email in the published shape (`references/email-shape.md`): required subject line verbatim or a "Prospective PhD student" subject, formal greeting, name, stage and program in the first sentence, the paper and their reaction, their paragraph, one ask chosen from the page's recruiting status, attachments or links as the page requires, signature. It writes `draft.md` with a "before sending" list and the country calendar (HKPFS end of November for Hong Kong; NUS, NTU and SUTD windows for Singapore), and `sop-paragraph.md` for the statement in every case.

It refuses: no policy checked today; a page that says not to email; a reused reaction; a near-identical body; a third email into one department; missing nationality or attachments the page requires; over 350 words. Read the draft with the student, change only what they ask, and re-run with the new arguments rather than editing the file. When they have sent it from their own mail client:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/log.mjs sent <id>
node ${CLAUDE_SKILL_DIR}/scripts/log.mjs reply <id> --date 2027-10-03 --summary "..." --tone positive
```

💡 Tip: Send on a weekday morning in the professor's time zone, and expect silence to be common and impersonal: audit studies of 6,500 professors found reply rates depend more on who is asking than on the message.

## Phase 4 — Follow up once

```bash
node ${CLAUDE_SKILL_DIR}/scripts/draft.mjs <id> --follow-up --paper <n> --reaction "<same>"
node ${CLAUDE_SKILL_DIR}/scripts/log.mjs sent <id> --follow-up
```

Allowed only seven or more days after the original, only once, and only if there was no reply. After that, silence is the answer (Evans), and the professor can still be named in the statement.

## Rules

- **Route before drafting**, from the page read today; store the quote, URL and date on the record.
- **Never email anyone whose page says not to.** Produce the statement paragraph instead and explain why.
- **One professor, one paper, the student's own reaction and paragraph.** No template bodies; no more than two professors in one department; no attachment where the page forbids it; every required detail complied with verbatim.
- **Never invent** a reading, a result or a project. If the student has not read the paper yet, wait.
- **One follow-up**, after a week, never a second.
- Keep the sent log honest: the CV version attached, the paper cited and the replies, so later statements match what was said.
- Keep the student informed at each phase boundary with one or two sentences and one tip. Do not narrate tool calls.

## Files

- `references/routing.md` — the six classifications with the quotes behind them, what is stored, how the ask and attachments follow the page
- `references/email-shape.md` — the published good examples, timing, follow-up, the audit-study evidence, the refusals
- `references/admission-models.json` — supervisor-led versus committee-led by country and institution, with sources and verification status
- `scripts/policy.mjs` — page scan on the day, classification storage, `--list`
- `scripts/draft.mjs` — the email, form content or statement paragraph, with every refusal
- `scripts/log.mjs` — sent log, replies, status table
