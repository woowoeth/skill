---
name: findaphd
description: This skill should be used when a student asks to "find a PhD advisor", "find professors for my PhD", "match me with supervisors", "who should I apply to for a PhD", "which labs fit my background", or runs /findaphd. It interviews the student (or reads a dropped resume), discovers professors from recent papers via OpenAlex, enriches each one with homepage, ORCID and grant data using parallel subagents, and writes a ranked, country-filterable report, playing a sound when done.
argument-hint: "[resume.pdf | profile URL | new | filter --country US | more]"
allowed-tools:
  - Bash(node ${CLAUDE_SKILL_DIR}/scripts/*)
  - Bash(${CLAUDE_SKILL_DIR}/scripts/notify.sh *)
  - Bash(mkdir *)
  - Bash(cp *)
  - Bash(ls *)
---

# /findaphd — PhD advisor matching

Match a student with professors the way a careful senior colleague would: understand the student first, find who is actually publishing on their problem right now, verify each person from primary sources, then rank and explain. Mainland China institutions are never included; Hong Kong institutions and HKUST (Guangzhou) are. Google Scholar is never scraped (it has no API); the report links to a Scholar search instead.

Part of the `phd-apply` plugin. Skill directory: `${CLAUDE_SKILL_DIR}`. Shared helpers live in `${CLAUDE_PLUGIN_ROOT}/lib/` and the scripts import them directly. Data home: `~/.phd-apply/`, shared with every other skill in the plugin (override with `PHD_APPLY_HOME`).

```
~/.phd-apply/profile.json                 the student profile, shared by every phd-apply skill
~/.phd-apply/cache/professors/<id>.json   enriched professor records, reused for 90 days
~/.phd-apply/runs/<YYYY-MM-DD-HHMM>/      profile.json, candidates.json, raw/, enriched/, adjustments.json, report.md, report.html
```

Arguments: `$ARGUMENTS`

- A file path (PDF/DOCX/MD) → resume flow. A URL → profile-page flow. `new` or nothing → interview (if `~/.phd-apply/profile.json` exists, offer to reuse or update it first).
- `filter ...` → re-render the latest run with those `report.mjs` options, no new analysis.
- `more` → extend the latest run with more candidates.

Speak the student's language (answer in Chinese if they write Chinese). Keep the tone of a helpful senior labmate: short, concrete, one `💡 Tip:` line per step.

## Phase 1 — Profile

Follow `${CLAUDE_SKILL_DIR}/references/interview.md`. Read dropped PDFs with the Read tool; fetch links with WebFetch. Confirm the summary, then write the profile:

```json
{
  "created_at": "ISO", "name": null, "status": "master's student", "phd_start_year": 2027, "degree_target": "PhD",
  "interests": ["..."], "interest_statement": "paragraph", "keywords": ["..."],
  "queries": ["4-6 specific search phrases, confirmed by the student"],
  "projects": [{"title": "", "url": "", "summary": ""}],
  "publications": [{"title": "", "venue": "", "year": 2025, "role": "first author", "url": ""}],
  "education": [{"institution": "", "degree": "", "major": "", "gpa": null, "years": ""}],
  "experience": [{"what": "", "where": "", "duration": ""}], "awards": [], "skills": [],
  "countries": ["US", "GB"],            // ISO codes in preference order, or ["ANY"]
  "preferences": {"advisor_stage": "no preference", "group_size": "no preference", "funding": "must be fully funded", "notes": ""},
  "max_candidates": 30, "years_back": 3, "resume_path": null,
  "summary": "3-5 sentences for the enrichment agents: who the student is, what they want to work on, what they bring."
}
```

Create the run directory `~/.phd-apply/runs/<YYYY-MM-DD-HHMM>/`, save `profile.json` there and as `~/.phd-apply/profile.json`.

## Phase 2 — Discover, then screen

```bash
node ${CLAUDE_SKILL_DIR}/scripts/discover.mjs --run <run-dir> --max 70
```

Ask for roughly twice as many candidates as will be analysed, because the next step throws some away. Discovery searches each chosen country separately (a single combined filter lets the largest country crowd out the others), infers the core topics of the field from the retrieved papers themselves, drops authors outside that field and authors who look like students, corrects institutions using the author's own affiliation record, and shares the slots out in the student's stated country order.

Useful flags: `--years 4` to widen the window, `--min-align 0.35` to loosen the topic filter for an interdisciplinary student, `--floor 0.3` to give minor countries a larger share.

**Then screen the list by hand.** Automatic filters cannot tell an assistant professor running a robot-learning lab from a postdoc, a surgical-robotics professor or an education researcher whose papers matched the word "learning". Reading the evidence can:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/screen.mjs --run <run-dir> --view
node ${CLAUDE_SKILL_DIR}/scripts/screen.mjs --run <run-dir> --keep A123,A456,...
```

The view prints each candidate's topics, recent matched paper titles and flags. Keep the people whose recent titles actually match the student's problem and who can supervise a PhD. Drop industry researchers with no university post, anyone whose main affiliation is outside the chosen countries, and anyone who never appears as last or corresponding author unless their record is clearly senior. Aim to keep 25-35. The full list stays in `candidates.full.json`, and `--restore` puts it back.

Show the student a short summary: how many candidates, from which countries, how many are already cached, the top eight names with institutions, and anything you dropped for a reason they would want to know (a whole country coming back thin, for example). Then state the estimate:

> Each professor takes an agent about 5 minutes of real research (homepage, lab pages, grants). Batches of 4 run in parallel, so expect roughly 20 minutes for 20-30 professors, and around 60k tokens per professor. You will hear a sound when it is done.

Ask whether to proceed, widen (`--max`, more queries, `--years`), or narrow (countries, or a quick first pass of 15).

## Phase 3 — Enrich (parallel subagents)

1. `mkdir -p <run-dir>/raw <run-dir>/enriched`.
2. For candidates marked cached, copy the cache file: `cp ~/.phd-apply/cache/professors/<id>.json <run-dir>/enriched/`. Their facts are reused, but their `fit` block was scored for an earlier profile, so pass their ids as `{{CACHED_IDS}}` to a batch below to be re-scored for this student without re-fetching.
3. Split the remaining ids into batches of 4 (3-5). Build one prompt per batch from `${CLAUDE_SKILL_DIR}/references/enrich-prompt.md`, filling `{{STUDENT_SUMMARY}}` (profile `summary` plus interests, projects one-liners, countries in order, preferences), `{{IDS}}`, `{{CACHED_IDS}}` (spread cached ids over the batches, or "none"), `{{RUN_DIR}}`, `{{SKILL_DIR}}` (= `${CLAUDE_SKILL_DIR}`), `{{TODAY}}`.
4. Launch **all batches in a single message** with the Agent tool (`subagent_type: general-purpose`, description `enrich batch k/n`). Tell the student the batches are running and the estimate; do not poll, wait for the completion notifications.
5. As batches finish, note their one-line results. When all are done: `node ${CLAUDE_SKILL_DIR}/scripts/validate.mjs <run-dir>/enriched/*.json`. For any invalid or missing id, launch one retry batch with just those ids. Then copy every valid record into the cache: `cp <run-dir>/enriched/*.json ~/.phd-apply/cache/professors/`.

## Phase 4 — Rank, report, notify

```bash
node ${CLAUDE_SKILL_DIR}/scripts/report.mjs --run <run-dir>
```

Calibrate across batches: read the JSON of the top 12 and any record whose score looks out of line with its rationale (different subagents drift). Where a score should change, write `<run-dir>/adjustments.json` as `{"<id>": {"fit_score": 74, "note": "one clause"}}` and re-run `report.mjs`. Do not rewrite subagent records by hand.

Then:

```bash
${CLAUDE_SKILL_DIR}/scripts/notify.sh "findaphd: N professors ranked"
```

Present to the student, in this order: a table of the top 10 (rank, fit, name, title, institution, country, hiring signal); two or three sentences on the pattern (which subfield and countries dominate, who is clearly recruiting); the paths to `report.md` and `report.html` (open the HTML in a browser for sorting and filtering); how to re-filter (below); one tip about next steps (e.g. read the top 3's latest papers before emailing). Never paste whole JSON files into the chat.

## Re-filter without re-analysing

```bash
node ${CLAUDE_SKILL_DIR}/scripts/report.mjs --run <run-dir> --country US            # one or more codes, comma-separated
node ${CLAUDE_SKILL_DIR}/scripts/report.mjs --run <run-dir> --stage early,mid --hiring --min-score 60 --out report-hiring
node ${CLAUDE_SKILL_DIR}/scripts/report.mjs --run <run-dir> --search "diffusion" --top 10
```

`--out <basename>` writes separate files so `report.md` stays intact. The HTML report also has live search, country, minimum-score, stage and hiring controls.

## Extend a run (`more`)

Re-run `discover.mjs` on the same run directory with a larger `--max` (or after adding queries to `profile.json`); it overwrites `candidates.json`. Enrich only ids without a file in `enriched/`, then re-run `report.mjs`.

## Rules

- Never fabricate professor facts. Records must cite URLs; unknown stays null; age is never estimated, only career stage.
- Respect the country policy in `${CLAUDE_PLUGIN_ROOT}/lib/countries.json` even if the student asks for mainland China; say so once, kindly.
- Grant APIs for the US (NSF, NIH) are blocked on some networks; the scripts report `unreachable` and subagents fall back to web search. Say "funding unknown", never "no funding", in that case.
- Keep the student informed at each phase boundary with one or two sentences, a time estimate when work is running, and one tip. Do not narrate tool calls.
- If the student is a beginner (no publications, vague interests), spend the extra exchange in Step 2 of the interview; a good `interest_statement` matters more than anything else.

## Files

- `references/interview.md` — step-by-step profile interview with tips
- `references/enrich-prompt.md` — subagent prompt template
- `references/schema.md` — enriched record format (validated by `scripts/validate.mjs`)
- `references/scoring.md` — fit rubric
- `scripts/discover.mjs` — OpenAlex discovery → `candidates.json` (per-country scopes, topic filter, PI gate)
- `scripts/screen.mjs` — hand-screening view and keep/drop filter before enrichment
- `scripts/author.mjs` — OpenAlex + ORCID detail for one professor (`--brief`, `--students`)
- `scripts/funding.mjs` — NSF / NIH / UKRI grants, or suggested searches elsewhere
- `scripts/report.mjs` — ranked Markdown + HTML report with filters
- `scripts/notify.sh` — completion sound and desktop notification
- `${CLAUDE_PLUGIN_ROOT}/lib/countries.json` — selectable regions and the China policy, shared across skills
- `${CLAUDE_PLUGIN_ROOT}/lib/core.mjs` — shared fetch, OpenAlex, paths and JSON helpers
