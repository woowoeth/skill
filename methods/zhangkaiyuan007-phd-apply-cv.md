---
name: cv
description: This skill should be used when a student asks to "write my academic CV", "make a CV for PhD applications", "update my CV", "which order should my CV sections be in", "what do I send my recommender", "recommendation letter packet", "track my recommendation letters", or runs /cv. It extends the shared phd-apply profile with the fields a PhD-application CV needs, renders one version per target region (Markdown, print-ready HTML, PDF) in the section order real admitted applicants used, writes a checklist of what was left off and why, and builds recommender briefing packets and a letter tracker. It never invents experience and never drafts a recommendation letter.
argument-hint: "[new | update | <cv.pdf> | render --region us | packet [name] | letters init|status|set ...]"
allowed-tools:
  - Bash(node ${CLAUDE_SKILL_DIR}/scripts/*)
  - Bash(mkdir *)
  - Bash(ls *)
  - Bash(cp *)
---

# /cv — academic CV and recommender packet

Build the CV the way the research says real admitted applicants built theirs: Education first, then whichever of Publications or Research Experience is the stronger asset, two to three pages, GPA only if it helps, competitions under Awards, categorised skills, links to code in the header, nothing the student cannot document. Then give recommenders what faculty say they need, without ever writing a word of the letter.

Part of the `phd-apply` plugin. Skill directory: `${CLAUDE_SKILL_DIR}`; shared helpers in `${CLAUDE_PLUGIN_ROOT}/lib/`. Data home `~/.phd-apply/` (override with `PHD_APPLY_HOME`):

```
~/.phd-apply/profile.json                 the shared profile; this skill adds the CV fields (references/profile-fields.md)
~/.phd-apply/documents/cv/                cv-<region>.md / .html / .pdf and checklist-<region>.md
~/.phd-apply/letters/<recommender>/       packet.md per recommender
~/.phd-apply/letters/tracker.json|.md     letter tracker
~/.phd-apply/schools/<program_id>.json    target programs, when /schools has run (else profile.targets[])
```

Arguments: `$ARGUMENTS`

- nothing, `new` or `update` → gap interview, then render.
- a file path (PDF/DOCX/MD) → read the student's existing CV with the Read tool, pre-fill the gaps, confirm, then render.
- `render ...` → re-render only, passing the flags through to `render.mjs`.
- `packet [name]` → recommender packet(s).
- `letters init|status|set ...` → letter tracker.

Speak the student's language. Tone: a senior labmate who has read a lot of CVs, short and concrete, one `💡 Tip:` line per step.

## Phase 1 — Fill the gaps

Follow `${CLAUDE_SKILL_DIR}/references/interview.md`. Start with what `profile.json` already holds (findaphd writes name, education, experience, projects, publications, awards, skills, countries) and ask only about the gaps. Write the bullets from the student's answers, read them back, and change them until the student says they are true. Never ask for date of birth, nationality, marital status, sex, religion or a photo.

Save with the Edit or Write tool into `~/.phd-apply/profile.json`, keeping every field findaphd wrote. The extended schema is in `references/profile-fields.md`; legacy shapes (string awards, flat skills, `what`/`where`/`duration` experience) still render, and `lint.mjs` says what to upgrade.

Quick check at any point:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/lint.mjs --region us
```

## Phase 2 — Decide the order, then render

Ask the ordering question explicitly (AskUserQuestion): which is the strongest asset, published or accepted papers, research experience, or awards? Explain the observed rule in one line each (`references/ordering-and-regions.md`). `--order auto` applies it: a published, accepted or in-press paper puts Publications second; otherwise Research Experience is second and in-progress papers move after Skills. Then ask which regions to render (one per target country) and, for US versions, whether to list referees.

```bash
node ${CLAUDE_SKILL_DIR}/scripts/render.mjs --all-regions --pdf
node ${CLAUDE_SKILL_DIR}/scripts/render.mjs --region uk --order research --in-progress separate --gpa yes --referees --pdf
```

Flags: `--region us|uk|hk|sg|other` (or a country code), `--order auto|publications|research|awards`, `--gpa yes|no`, `--referees`, `--coursework`, `--test-scores`, `--in-progress labels|separate`, `--pdf`, `--out <dir>`. The PDF uses headless Chrome or Chromium if one is installed (`CHROME_PATH` to point at one); otherwise the HTML prints to PDF from any browser at the right page size.

Walk the student through `checklist-<region>.md`: the order used and why, the page count (2–3 is the norm; nobody strong was at one page), each omitted item with its reason, and the lint findings, decisions first. Fix the profile and re-render until the checklist has no errors and every decision is made. Show the Markdown of the final version in the chat only if the student asks; otherwise give the paths.

## Phase 3 — Recommender packets and letter tracking

Only when the student asks, or once the CV is done and they have named recommenders. Collect per recommender (in the student's words): relationship, what to emphasise, the "things I shouldn't forget about you" list, courses and projects together (`references/recommender-packet.md`). Targets come from `/schools` records or `profile.targets[]`; any letter fact without a source is printed as unverified.

```bash
node ${CLAUDE_SKILL_DIR}/scripts/packet.mjs                    # one packet per recommender
node ${CLAUDE_SKILL_DIR}/scripts/packet.mjs --recommender Hopper --cv-region uk
node ${CLAUDE_SKILL_DIR}/scripts/letters.mjs init                # program × recommender rows with ask-by, soft and reminder dates
node ${CLAUDE_SKILL_DIR}/scripts/letters.mjs status
node ${CLAUDE_SKILL_DIR}/scripts/letters.mjs set --program mit --recommender hopper --status invited
```

Tell the student: ask in person where possible, two months before the earliest deadline and never under a month; send the packet with the CV, statement draft and transcript; one brief reminder; confirm receipt in each portal; waive the right to view every time.

## Rules

- **Never invent.** No project, paper, award, skill or bullet the student did not state. Bullets are read back and confirmed.
- **Never list what cannot be documented.** Competitions need a results URL or "certificate on file". MOOC certificates are left off, with the reason in the checklist.
- **Never render personal details** (birth date, nationality, marital status, photo) on any version; say why in the checklist. Regions other than the US and UK render the UK form and are marked unverified.
- **Never draft, edit, translate or submit a recommendation letter**, even if a recommender asks the student to (Stanford calls it a violation of application terms). Offer the packet instead. Never enter the student's own email as a recommender's; `packet.mjs` and `letters.mjs` refuse. Never suggest un-waiving the right to view, nagging beyond one brief reminder, or gifts.
- **One profile, many renders.** Do not hand-edit the outputs; change the profile and re-render.
- Keep the student informed at each phase boundary with one or two sentences and one tip. Do not narrate tool calls.

## Files

- `references/profile-fields.md` — the CV fields added to the shared profile, with rules
- `references/ordering-and-regions.md` — observed section order, in-progress vocabulary, length, regional form, the never list
- `references/interview.md` — gap interview with tips
- `references/recommender-packet.md` — packet contents, refusals, tracker date rules
- `scripts/lint.mjs` — convention checks on the profile
- `scripts/render.mjs` — Markdown, HTML, PDF and checklist per region
- `scripts/packet.mjs` — recommender briefing packet
- `scripts/letters.mjs` — letter tracker (init, status, set)
- `${CLAUDE_PLUGIN_ROOT}/lib/core.mjs` — shared paths, profile and program loaders, date helpers
