---
name: backfill
description: >
  Imports months of history into the Nous graph in bulk — in a deliberate SOURCE ORDER (CRM →
  outbound → meetings → Gmail → Stripe), then enriches and ICP-scores every account. Use when
  setting up a workspace, or when the user says "backfill my history", "import the last 6 months",
  "pull all my past calls". Runs on THIS agent's tokens. Resumable and idempotent — safe to stop
  and re-run. For a single just-finished call, use sync instead.
---

# Nous backfill — import history in bulk, in the right order

A backfill is not "loop over every connected tool." The **order** is the whole game: account-
*creating* sources run before account-*enriching* ones, so every later source *matches into* the
graph the earlier ones built instead of forking duplicates. Read
**`references/backfill-order.md`** for the full strategy and the reasoning — it is canonical. Each
item within a stage goes through the **same per-item procedure as `sync`** (extract → `record` /
`record_insight`; Nous resolves + scores). The extraction rules are identical:
`../sync/references/claim-extraction.md` and `../sync/references/insight-extraction.md`.

## Run the stages IN ORDER (skip any whose source isn't connected)

Onboarding's discovery told you which connectors exist. Run only those, in this sequence, and say in
the report which stages you skipped.

- **Stage 0 · Ask: is there a CRM?** The answer shapes the run (stage data now, or Stripe later).
- **Stage 1 · CRM** (HubSpot / Attio / Pipedrive / Salesforce) — *creates the backbone.* Import
  companies→accounts, contacts→people, deals→`deal.stage`/`deal.value`, and owners. The only source
  besides Stripe that carries **pipeline stage**. Everything downstream matches into these accounts.
- **Stage 2 · Outbound** (Instantly / HeyReach / Smartlead / Lemlist / EmailBison) — *creates from
  replies.* Import contacted leads and especially **logged responses**: each reply → create/match the
  contact, record the interaction + `discovery` (campaign/channel). Runs before meetings so a later
  meeting matches the person instead of duplicating them.
- **Stage 3 · Meetings = notetaker + calendar** — *notetaker creates, calendar corroborates.* Run
  each notetaker transcript (Fireflies / Granola / Fathom) through the per-item procedure below.
  Calendar (Google Calendar / Calendly / Cal.com) supplies the real **date/time** and confirms
  attendee emails; treat it as enrichment of the notetaker's meetings.
- **Stage 4 · Gmail** — *enrich-only, NEVER create.* Attach interactions/intel **only to
  accounts/people already in the graph** from Stages 1–3. Do not spawn an account from an arbitrary
  sender. (This is why the creators run first — they define "known," and Gmail fills known.)
- **Stage 5 · Stripe** (optional, last) — *the revenue truth.* If there's no CRM (or to confirm one),
  ask the user to connect Stripe to learn who actually **closed-won** and the real amount, so
  stage-less accounts get a stage.

**Then the final pass — enrich, then score** (this is what fixes "not ICP'd, not enriched"): first
enrich firmographics so accounts are *scoreable* (domain → industry / size), then `score` every
account against the ICP set in onboarding. Do this LAST — scoring needs both an ICP model and enriched
features. If no ICP exists, say so and skip; don't block the report.

## Mechanics per stage — the loop (oldest → newest, in batches)

For each connected source, in the order above, repeatedly:
1. **Watermark** — per source, find where a prior run stopped (`~/.nous/backfill.json`, or ask Nous).
   Resume from there; first run starts at the window's oldest edge. **Window defaults to 6 months.**
2. **Pull the next batch** (20–50 items) from the watermark forward, within the window.
3. **For each item, run the `sync` per-item procedure** — including step-2 attendee resolution, so
   every fact lands on the RIGHT person (by email), never piled on one host entity:
   - resolve external attendees → identifiers (email → LinkedIn URL → domain); key each person by the
     SAME identifier every item so repeats collapse into ONE record (the engine resolves; you stay
     consistent — see the sync skill's resolution rule)
   - `record` identity attributes per attendee (step 2b): `first_name`/`last_name`, `job_title`, plus
     `domain` from the email and `company` name IF found — this is what gives each person a name and
     **materializes + links their company account** (skip our own side + free-email domains)
   - stash the raw → `raw/<account-slug>/<YYYY-MM-DD>-<source>-<id>.md` (one folder per account; see
     `../sync/references/raw-storage.md`), compute `content_hash`
   - `record` the interaction (`observed_at` = the item's REAL date, `external_id` = `<id>:interaction`,
     `source_ref`)
   - extract facts → `record` each Intel fact **against its person**, `external_id` = `<id>:intel:<index>`
   - extract insights → `record_insight`
   - write a one-line brief → `briefs/<account>/<date>-<id>.md` (git only)
4. **Retry, then quarantine.** Transient error (connection closed, timeout, 5xx) → retry up to 3
   times; still failing → add the id to a `quarantine` list and continue. Never let one item stall the run.
5. **Report progress** every ~50 items (`"420/1,200 meetings imported…"`) and **checkpoint the
   watermark** after every batch, so a stop/crash never loses ground.

At the end of each stage, report its quarantine list so a re-run can retry just those items.

## Cost & size discipline
- This runs on the user's tokens; a deep history can be thousands of items. Before a large run, give a
  rough size ("~1,200 meetings over 6 months") so they know the scale.
- Cap the work per invocation if it's very large; checkpoint and tell the user they can **re-run to
  continue** — every write is idempotent, so resuming never double-files.

## On completion (after all stages + the enrich/score pass)
1. **Trigger the reporting distillation.** A backfill records the raw material for both reporting
   surfaces — objection/pain Intel (via `record`) that becomes `role-report`'s deal-blockers, and
   product/positioning/market/buyer insights (via `record_insight`) that become `market-read`'s
   themes — but the distilled layers are built server-side, not at write time. Company **themes**
   re-synthesize lazily the next time `market-read` reads them (no action). The **objection handlers**
   behind `role-report` are built by a weekly job, so after a bulk import ask Nous to run the
   intelligence pass now (the server's `runIntelligenceOnce`) rather than wait a week. If no trigger
   is exposed yet, tell the user role-report will populate on the next weekly run.
2. **Hand off to the report:** run `review-pipeline` ("N accounts, M meetings, $X pipeline"). Name the
   stages you ran and skipped ("no CRM connected — stages unknown without a CRM or Stripe"). When
   called from `onboard`, that skill owns the closing report — just return the counts.

Reporting needs volume by design: the objection matcher needs ≥5 objections and theme synthesis drops
tiny 1–3-item themes — a thin backfill may not populate reporting until enough recurs.

## Rules
- **Order is the strategy.** Creators (CRM → outbound → meetings) before enrichers (Gmail, Stripe).
  Structured stage before free text. Gmail NEVER creates accounts. See `references/backfill-order.md`.
- **Stage & closed/won come only from CRM or Stripe.** With neither, accounts stay stage-unknown —
  that's correct, not a bug.
- **Attribution over volume.** Each item resolves its own attendees and files each fact on the right
  person (by email) — never dump a meeting's facts onto its host entity. One right beats ten wrong.
- **Retry, then quarantine — never stall.** Up to 3 retries, then quarantine and continue.
- **Idempotent + resumable, always.** Every observation carries a stable `external_id` from the source
  item id, so re-running skips what's filed. NEVER restart from zero — read the watermark.
- **`observed_at` is the item's REAL date**, never now — the point of backfill is a correct timeline.
- **Raw → git, structure → Nous.** Never send a transcript or a full brief to Nous.
- **Never invent.** A thin item may yield only its interaction and no facts — that's correct.
- **You never merge/resolve identities.** Observe against a precise `focus`; the engine resolves.
- **Score last.** Enrich firmographics, then `score` against the ICP — never before both exist.
