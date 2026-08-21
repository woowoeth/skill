---
name: chronic-illness-research-partner
description: Scaffolds a long-running research project repo for a chronic-illness patient using AI as a research partner. Run once per project; interviews the user and generates a tailored CLAUDE.md and structure.
---

# Setup: chronic-illness research-partner project

This skill runs ONCE to scaffold a long-running personal research project for someone with a refractory or complex chronic illness. It does not run again per session — the persistent discipline lives in the generated repo's `CLAUDE.md`.

## Activation

Activate when the user invokes this skill by name, OR describes wanting to:
- "set up a long-running research project on my [condition]"
- "use AI as a research partner for my chronic illness"
- "scaffold a research project for [condition]"

Do NOT activate for:
- General medical questions, including one-off questions about a condition (e.g. "what is POTS?").
- Mid-project sessions in an already-generated repo. Look for an existing `CLAUDE.md` referencing this skill — if found, decline and tell the user to work in the generated repo directly.
- Symptom tracking or journaling (existing condition-specific tracker apps already do this).
- Acute medical advice or triage (route to clinician/ER as appropriate).
- Diagnosis-shopping or self-diagnosis. The skill assumes the user has, or is actively pursuing with a clinician, a working diagnosis.
- General medical-literature search (PubMed, Semantic Scholar, Elicit handle one-off questions).
- Re-running on an existing project (this skill is one-shot per project; subsequent work happens inside the scaffolded repo).
- Non-chronic / acute-only conditions with no multi-year arc.
- Caregivers seeking emotional support, care logistics, or insurance navigation rather than literature synthesis. Caregiver-as-researcher is in scope; caregiver-as-general-support is not.
- Clinician workflows (case-series databases, EHR workflow, trial-screening tools need different scaffolding).
- Researching a condition the user does not have or care for.

## Pre-interview preamble

Before Q1, print this paragraph and wait for acknowledgement:

> Three things before we start:
>
> 1. The repo this generates will accumulate personal health information. Do not push it to a public remote without a redaction review.
> 2. You'll be asked about working preferences including whether to drop routine medical disclaimers. That setting relaxes routine hedging only — for any acute red flag (suicidal ideation; signs of stroke, sepsis, anaphylaxis, new neurological deficit; severe medication reactions), I'll always escalate to "call emergency services or your clinician" regardless of disclaimer setting.
> 3. Any answer can be skipped with `skip` or `unknown`. Skipped answers leave the relevant template section as a TODO prompt rather than seeding it. You can fill skipped items later.
>
> Ready to start?

Wait for the user to acknowledge before continuing to Q1.

## Interview

Discipline rules — apply to every question:

- One question per turn. No batching.
- Wait for the user's answer before moving to the next question.
- Do not summarize prior answers conversationally between questions. Just ask the next one.
- For enum questions, list the valid options verbatim. If the user types something that doesn't match an enum, re-prompt once with the valid options. Second invalid response: treat as skip and apply the default.
- `skip` and `unknown` are always accepted (except Q1, which is required for slug derivation).
- Do not use AI-coded vocabulary in the question text (no "surfaced", "leverage", "robust", "comprehensive" as filler, etc.). The questions below are the wording — use them as written.

### Q1: Condition name

Ask: "What's the working diagnostic label, even if contested?"

- Free text. Required (cannot skip — needed to derive the directory slug).
- If user types `skip` or `unknown`, re-prompt: "I need a label to derive the project's directory name. Even a contested or working label is fine."
- Store as `condition_name`.
- Wait for the user's answer before moving to Q2.

### Q2: Whose research

Ask: "Are you researching for yourself, or on behalf of someone else? Options: `self` / `child` / `partner` / `parent` / `other`."

- Enum. Default on skip: `self`.
- Store as `whose_research`.
- Wait for the user's answer before moving to Q3.

### Q3: Project framing

Ask: "In one sentence, what does this project most need to crack? (e.g. a specific subtype hypothesis, a treatment to find, a refractoriness puzzle.)"

- Free text, one sentence.
- Skip behavior: emit a TODO sentence in the seed file rather than seeding it.
- Store as `project_framing`.
- Wait for the user's answer before moving to Q4.

### Q4: History years

Ask: "How many years has this been going on? (integer, 0–100)"

- Integer 0–100.
- Skip behavior: omit the history-length sentence from the context block.
- Store as `history_years`.
- Wait for the user's answer before moving to Q5.

### Q5: Refractory status

Ask: "Where are you on the treatment arc? Options: `never-treated` / `partial` / `refractory-multi` / `dx-ongoing`."

Brief gloss if helpful:
- `never-treated`: newly diagnosed, no trials yet.
- `partial`: some response to standard care; still seeking better.
- `refractory-multi`: failed multiple classes (the typical case for this skill).
- `dx-ongoing`: working label contested or diagnostic workup ongoing. The project organizes evidence and questions for clinicians who are still working a diagnostic case; it does not do diagnostic work itself.

- Enum. Default on skip: `refractory-multi`.
- Store as `refractory_status`.
- Wait for the user's answer before moving to Q6.

### Q6: Specialist status

Ask: "Are you working with a specialist clinician for this? Options: `yes` / `no` / `seeking`."

- Enum. Default on skip: `yes`.
- Store as `specialist_status`.
- Wait for the user's answer before moving to Q7.

### Q7: Tracker data

Ask: "Any existing tracker data we should know about? (e.g. `tracker app X, 5y`, `tracker app Y, 18mo`, `none`.)"

- Free text.
- Skip behavior: omit the `{{tracker_data_note}}` placeholder.
- Store as `tracker_data`.
- Wait for the user's answer before moving to Q8.

### Q8: Terseness preference

Ask: "How terse do you want responses? Options: `terse` / `balanced` / `fuller`."

Brief gloss if helpful:
- `terse`: effect sizes, citations, no filler.
- `balanced`: concrete and specific where it matters; readable everywhere else.
- `fuller`: narrative explanation welcome.

- Enum. Default on skip: `balanced`.
- Store as `terseness_pref`.
- Wait for the user's answer before moving to Q9.

### Q9: Disclaimer preference

Ask: "How should I handle medical disclaimers? Options: `off` / `soft` / `standard`."

Brief gloss if helpful:
- `off`: no routine "ask your doctor" reflexes (the safety floor still applies — see preamble).
- `soft`: include only when safety-relevant.
- `standard`: include routinely.

- Enum. Default on skip: `off`.
- Store as `disclaimer_pref`.
- Wait for the user's answer before moving to Q10.

### Q10: Pushback preference

Ask: "How hard should I push back on weak hypotheses? Options: `hard` / `gentle` / `defer`."

Brief gloss if helpful:
- `hard`: challenge directly; argue both sides; surface confounders.
- `gentle`: surface concerns diplomatically.
- `defer`: state once and move on.

- Enum. Default on skip: `hard`.
- Store as `pushback_pref`.
- Wait for the user's answer before moving to Q11.

### Q11: Primary literature comfort

Ask: "How deep do you read primary literature? Options: `abstracts-and-methods` / `abstracts` / `summaries`."

- Enum. Default on skip: `abstracts`.
- Store as `primary_lit_comfort`.
- Wait for the user's answer before moving to Q12.

### Q12: Evidence rigor

Ask: "How strict should evidence-tagging be? Options: `full` / `tags-only` / `informal`."

Brief gloss if helpful:
- `full`: evidence tags + PMID/DOI round-trip required for every medical claim.
- `tags-only`: tags required; round-trip when the claim is load-bearing for a candidate.
- `informal`: surface the strongest evidence with citations where available.

- Enum. Default on skip: `full`.
- Store as `evidence_rigor`.
- Wait for the user's answer before moving to Q13.

### Q13: Open questions

Ask: "Up to three open questions you most want this project to crack. One per line, or skip."

- List of up to 3 free-text strings.
- Skip behavior: empty list emits a TODO prompt in the seed file.
- Store as `open_questions`.
- Wait for the user's answer before moving to path confirmation.

## Path confirmation

After Q13, derive the slug from `condition_name`:

1. Lowercase and strip the input. Replace any non-alphanumeric run with `-`. Strip leading/trailing `-`. Then PascalCase by splitting on `-` and capitalizing each segment.
2. Apply special cases (case-insensitive match on the lowercased, stripped input, before applying the general rule):
   - `me/cfs` → `MECFS`
   - `pots` → `POTS`
   - `eds` → `EDS`
   - `long covid` → `LongCovid`
   - `ms` → `MS`
   - `als` → `ALS`
   - `ibd` → `IBD`
3. Cap at 64 characters.
4. If the algorithm produces an empty slug, re-prompt the user for `condition_name`.

Default target path: `~/{condition_slug}Research/`. Example: condition `Long COVID` → slug `LongCovid` → path `~/LongCovidResearch/`.

Print the absolute path and ask: "I'll generate the project at this absolute path. The interview produced N answers; I'll create approximately 25 files and 10 directories. Proceed? (`yes` / `different path` / `cancel`)"

If the user picks `different path`, accept any filesystem-safe absolute path. Reject paths whose final segment contains `/`, `\`, `..`, leading `.`, NUL, or characters disallowed on the user's platform. On rejection, re-prompt once.

Filesystem state handling for the chosen target path:

- Does not exist: create it.
- Exists, is a directory, empty: proceed.
- Exists, is a directory, non-empty: print its contents (`ls`, max 50 entries shown, one per line). Ask the user to type the absolute path back verbatim to confirm overwrite, OR pick a new path. Partial paths, relative paths, and `y`/`yes` do not count as confirmation. Mismatch: refuse and exit. Do NOT proceed without an explicit type-back confirmation.
- Exists, is a regular file (not a directory): refuse; do not overwrite. Ask the user to pick a different target.
- Exists, is a symlink: resolve the symlink and apply the rules above to the resolved target. If the symlink is broken, refuse with a clear error.
- Exists, contains a `.git` directory: refuse; do not run `git init` on top of an existing repo. This rule fires even if the directory would otherwise count as empty save for `.git/`.
- Exists, on a read-only filesystem: refuse with a clear error (e.g. surface `EROFS` verbatim); do not attempt any writes.

No partial writes on refusal: if the script refuses for any reason above, exit before creating any files in the target.

## Generation

For each template under `templates/`, do the following:

1. Read the template file.
2. Compute the precomputed blocks from the interview answers (formulas below).
3. Substitute every `{{name}}` token with its value.
4. Write the result to the target path under the corresponding non-`.tmpl` filename (e.g., `templates/CLAUDE.md.tmpl` → `<target>/CLAUDE.md`; `templates/intake/journey.md.tmpl` → `<target>/intake/journey.md`).

Use the Write tool. Do NOT use a templating library. Create parent directories as needed.

Every render must produce byte-identical output for identical interview answers. Do not paraphrase or "improve" the sentence templates below at generation time.

### Precomputed block formulas

#### `{{condition_name}}`

Q1 answer verbatim.

#### `{{condition_slug}}`

Derived per "Path confirmation" rules.

#### `{{generated_date}}`

Today's date in `YYYY-MM-DD` format.

#### `{{role_block}}`

2–3 sentence research-partner paragraph. Vary by `whose_research`:

- `self`: "Claude is the user's research partner — postdoc to PI. Specifically: interview the user to extract context that's in their head and in any data on hand; synthesize that with peer-reviewed literature; propose candidate causes and treatments (especially ones not yet tried); stress-test working hypotheses; prepare materials for clinician visits."
- `child`: "Claude is the user's research partner — postdoc to PI. The user is researching on behalf of their child. Specifically: interview the user to extract context that's in their head and in any data on hand; synthesize that with peer-reviewed literature; propose candidate causes and treatments (especially ones not yet tried); stress-test working hypotheses; prepare materials for clinician visits."
- `partner`: "Claude is the user's research partner — postdoc to PI. The user is researching on behalf of their partner. Specifically: interview the user to extract context that's in their head and in any data on hand; synthesize that with peer-reviewed literature; propose candidate causes and treatments (especially ones not yet tried); stress-test working hypotheses; prepare materials for clinician visits."
- `parent`: "Claude is the user's research partner — postdoc to PI. The user is researching on behalf of their parent. Specifically: interview the user to extract context that's in their head and in any data on hand; synthesize that with peer-reviewed literature; propose candidate causes and treatments (especially ones not yet tried); stress-test working hypotheses; prepare materials for clinician visits."
- `other`: "Claude is the user's research partner — postdoc to PI. The user is researching on behalf of someone else. Specifically: interview the user to extract context that's in their head and in any data on hand; synthesize that with peer-reviewed literature; propose candidate causes and treatments (especially ones not yet tried); stress-test working hypotheses; prepare materials for clinician visits."

#### `{{context_block}}`

2–4 sentences derived from `history_years`, `refractory_status`, `specialist_status`, `tracker_data`. Each sentence is built from one answer; skip whichever is `skip` or `unknown` per the rules below. Concatenate with single spaces into one paragraph.

Sentence templates:

- `history_years`: "{N}-year history of {condition_name}." — omit if skipped.
- `refractory_status`:
  - `never-treated`: "No adequate treatment trials yet."
  - `partial`: "Partial control on current regimen; still seeking better."
  - `refractory-multi`: "Refractory to multiple lines of treatment."
  - `dx-ongoing`: "Diagnostic workup ongoing — working label may be revised."
- `specialist_status`:
  - `yes`: "Working with at least one specialist clinician."
  - `no`: "Not currently working with a specialist."
  - `seeking`: "Seeking a specialist."
- `tracker_data`: "Existing tracker data: {tracker_data}." — omit if skipped or the value is "none".

Trim priority if over 600 chars or 6 lines: drop tracker_data sentence first, then specialist_status, then history_years. Always keep the refractory_status sentence.

#### `{{working_style_block}}`

3–5 sentences combining `terseness_pref`, `disclaimer_pref`, `pushback_pref`, ending with the safety-floor sentence verbatim. Concatenate with single spaces into one paragraph.

Sentence templates:

- `terseness_pref`:
  - `terse`: "Direct, terse, quantitative. Effect sizes and citations beat hedged prose."
  - `balanced`: "Balanced — concrete and specific where it matters; readable everywhere else."
  - `fuller`: "Fuller explanations are welcome when they aid the user's mental model."
- `disclaimer_pref`:
  - `off`: "Skip routine medical disclaimers — the user has a clinician and is making decisions with one."
  - `soft`: "Light disclaimers where genuinely useful; not as filler."
  - `standard`: "Standard medical disclaimers are appropriate here."
- `pushback_pref`:
  - `hard`: "Push back hard on weak hypotheses. Argue both sides; surface confounders."
  - `gentle`: "Push back when warranted, but with care."
  - `defer`: "Mostly defer; the user wants to drive."
- Always-included safety floor (verbatim): "Even with disclaimers off, urgent red flags (suicidal ideation; signs of stroke, sepsis, anaphylaxis, new neurological deficit; severe medication reactions) get an unconditional 'call emergency services or your clinician' — disclaimers-off relaxes routine hedging, never emergency triage."

Trim priority if over 600 chars or 6 lines: never drop the safety-floor sentence; drop fuller-mode elaboration first, then disclaimer detail, then pushback elaboration.

#### `{{evidence_rigor_block}}`

2–3 sentences combining `primary_lit_comfort` and `evidence_rigor`. Concatenate with single spaces.

- `primary_lit_comfort`:
  - `abstracts-and-methods`: "The user reads abstracts and methods regularly; minimal explanatory scaffolding around literature."
  - `abstracts`: "The user reads abstracts; some scaffolding around methods is helpful."
  - `summaries`: "The user prefers summaries; provide explanatory scaffolding around primary literature."
- `evidence_rigor`:
  - `full`: "Every medical claim carries an evidence tag (RCT/META/OBS/CASE/REV/CONS/MECH/SPEC) with applicability annotation; PMID/DOI round-trip is required before assertion. See `meta/standards.md` and `meta/research-methodology.md`."
  - `tags-only`: "Every medical claim carries an evidence tag. Round-trip when the claim is load-bearing for a candidate. See `meta/standards.md`."
  - `informal`: "Surface the strongest evidence, with citations where available. Be honest about uncertainty."

Trim priority if over limit: drop the methods-comfort sentence before the evidence-tag sentence.

#### `{{population_block}}`

1–2 sentence population-applicability note keyed off `whose_research`:

- `self`: "Population: adult self-research. Evidence applicability is read against this population."
- `child`: "Population: pediatric — research on behalf of a child. Adult RCT findings often do not transfer; evidence applicability must be checked against pediatric populations specifically. See `meta/standards.md` for the population/applicability TODO."
- `partner`: "Population: research on behalf of a partner. Evidence applicability must be checked against the relevant adult population (the user records age range and other population specifics in `meta/standards.md` during the frontier scan)."
- `parent`: "Population: research on behalf of a parent. Evidence applicability must be checked against the relevant older-adult population (the user records age range and other population specifics in `meta/standards.md` during the frontier scan)."
- `other`: "Population: research on behalf of another person. Evidence applicability must be checked against the relevant population (the user records age range and other population specifics in `meta/standards.md` during the frontier scan)."

#### `{{open_questions_md}}`

Markdown numbered list of `open_questions` array entries (one per line, `1.`, `2.`, `3.`). Empty list (skipped Q13) → `<!-- TODO: fill in next session -->`.

#### `{{project_framing}}`

Q3 answer verbatim. If skipped, fall back to `<!-- TODO: what does this project need to crack? -->`.

#### `{{tracker_data_note}}`

`Existing tracker data: {tracker_data}.` — omit (collapse to empty string) if `tracker_data` is `skip`, `unknown`, or "none".

## Empty directories

After file generation, create these empty directories with a `.gitkeep` file in each:

- `causes/`
- `mechanisms/`
- `literature/papers/`
- `literature/topics/`
- `literature/searches/`
- `data/raw/`
- `clinician/visits/`
- `clinician/pre-visit/`
- `notes/`

## Git initialization

Run from the target directory:

1. Check `git config --global user.email` and `user.name`. If either is missing AND the local repo's `git config` is also missing, ask the user once: "Git identity is not set. Provide name and email so I can create the initial commit, OR I can leave the repo without an initial commit." Accept their choice. If they decline or provide empty values, skip the initial commit but still run `git init` so the working tree is in a repo.
2. `git init` in the target directory.
3. `git add .` and `git commit -m "initial scaffold via chronic-illness-research-partner skill"`.

If `git init` or the initial commit fails for any reason — missing binary, permission denied, signing failure, pre-commit hook failure, anything else — print the error verbatim, leave all generated files in place, and tell the user: "You can `git init` this directory yourself when ready." Do NOT delete files or roll back. Do NOT bypass commit signing or pre-commit hooks: no `--no-gpg-sign`, no `-c commit.gpgsign=false`, no `--no-verify`, no equivalent flag. Whether to skip a hook or signing is the user's decision after they see the error; the skill never decides this for them.

## Closing message

After successful generation, print:

> The {{condition_name}} research project is ready at {target_path}.
>
> Your first working session is the **frontier scan**. Read in this order:
>
> 1. `CLAUDE.md` — the operating contract for every future session
> 2. `meta/research-methodology.md` — the research-discipline doc; protocols for search, round-trip, quote bank
> 3. `meta/frontier-scan-status.md` — the gate file; this is the checklist for the frontier scan
> 4. `meta/standards.md` — see the eight TODO sections that the frontier scan fills in
>
> Treatment-candidate work is gated on completion of the frontier scan. The Claude instance you work with in this repo will refuse to generate `treatments/candidates/` files until the scan is marked complete in `meta/frontier-scan-status.md`.
>
> Privacy: this repo will accumulate personal health information. Do not push it to a public remote without a redaction review.
