---
name: create-landing
description: Create or improve a complete landing page from a plain-language business description. Use when someone asks to make, fix, or improve a landing, sales, or conversion page. Researches the business, asks only essential questions, builds an Astro site, checks it in a real browser, and reports readiness in plain words. Not for a single UI component, an audit-only request, one image, or deployment-only work.
---

# Landing Harness

Outside: one plain dialog. Inside: research, assembly, and verification.

The user explains what they sell, to whom, which problem it solves, why it can
be trusted, what a visitor should do, and which sites they like. Everything
technical the harness chooses, executes, checks, and repairs on its own. The
user sees business decisions, material assumptions, progress in plain words,
and a readiness verdict.

Stage guides live in `references/`; deterministic steps in `scripts/`. Read
the guide for the current state before acting; never improvise a stage from
memory or skip its commands.

## Runs anywhere

Needs only Node 24+ and a shell. Everything else is optional and degrades
silently; never block on it or mention it to the user.

- **Commands.** `<angle brackets>` in a command are placeholders: substitute the
  real value before running it, never the literal text.
- **Working directory.** Resolve `S` once to the absolute path of this skill's
  `scripts/` directory and reuse it for every command below. Run commands from the project root, the folder the
  user opened. The landing is created there as one folder (`landing/` by
  default) that belongs to the user's project, not to the skill. The skill may be installed at
  (`.claude/skills/create-landing/scripts`, `~/.claude/skills/...`,
  `.agents/skills/...`).
- **Companion skills.** Three steps (sharpest-question discovery, frontend
  design, crawler-grade SEO audit) may delegate to other installed skills,
  resolved by capability id in `scripts/adapters/registry.ts`, the only file
  that names one. `node $S/adapters/registry.ts check` reports each as
  installed or not. Not installed is the normal case on most hosts: use the
  built-in section of the stage guide instead.
- **Web research.** Uses whatever browsing or search the host provides. With
  none, say so once in the understanding summary and rely on supplied files,
  links, and the user's answers.
- **Design contracts.** The stage guides name the spec they implement. Those
  specs live only in the skill's source repository and are not shipped; never
  look for them. `references/` is complete on its own.

## The loop

research → ask only what matters → confirm the meaning → synthesize references
→ build → verify → repair → explain the result in plain words.

Three rules decide every unknown:

- **Facts → investigate.** Brand colors, existing site, category language, competitor claims.
- **Decisions → ask.** Primary conversion (demo or signup), what may be published, what the user likes.
- **Defaults → choose.** Title format, section presence, form fields, event names, whether pricing is shown (off unless the user says it is public). Record each as an assumption.

Never invent proof: no customers, numbers, certificates, testimonials,
integrations, results, or guarantees the claim register does not hold as a
confirmed fact.

## Modes

Pick the mode from the message; no command syntax is required.

| The user | Mode | Entry state |
|---|---|---|
| Invokes the skill with no text | Ask one opening question, then Make: "What do you sell, to whom, and what should a visitor do on the page? Add your site and any pages you like." | `Intake` |
| Describes a business, pastes links, attaches files | Make: intake, research, questions, direction, build, verify, readiness | `Intake` |
| Says "improve" and names a finished run | Improve: snapshot the brief, one focused change, re-verify, before → after | `Improve` (from `Ready`) |
| Names an unfinished landing folder (`landing`, or a name they chose) | Resume at the recorded state (`run.ts resume <landing>`) | recorded state |

## Prerequisites

Once per machine. Skip when `scripts/node_modules/` exists.

```bash
node -v                                   # 24 or newer
cd "$S" && npm ci && npx playwright install chromium && npm run check
```

If install fails (no Node, no network, no permission), tell the user in one
plain sentence what is missing and stop. Optional: `POSTHOG_KEY` (and
`POSTHOG_HOST`) in the environment connect analytics; without a key the page
runs a no-op provider and the summary says so.

## Stages

| State | What happens | Guide |
|---|---|---|
| Intake | Accept description, links, files. No questions yet. Show the understanding summary. | `references/discovery.md` |
| Research | Study the site, documents, category, competitors, proof, brand. Capture references, assess coverage. | `references/discovery.md`, `references/reference.md` |
| Clarification | Batches of at most 3 questions, business language, each with a suggested answer. | `references/discovery.md` |
| DirectionReview | Direction summary with every assumption and excluded claim; "Is this right?". Build only on confirmation. | `references/discovery.md` |
| Build | Page strategy with the section order from the examples, copy from confirmed facts only, the user's images and fonts, a design plan before any style, the static site, build, local preview. | `references/build.md` |
| Verify | Open the built page in a real browser; eleven check layers including a design review against the plan; the gate as hard blockers. | `references/verify.md` |
| Repair | Fix the highest-priority failure only; re-verify. Stop after two cycles with no gain. | `references/verify.md` |
| Ready | Readiness summary in plain language. Publishing only on explicit request. | `references/verify.md` |
| Blocked | One question: a decision, an asset, or a credential. | `references/discovery.md` |
| Improve | Snapshot the brief, one focused change, re-verify, before → after. | `references/verify.md` |

## Scripts

All state goes through `run.ts`. Never edit `state.json`,
`validation-report.json`, or `gate.yaml` thresholds by hand. Per-stage
commands are in the stage guides.

```text
run.ts init [<landing>]
run.ts status <landing>
run.ts resume <landing>
run.ts transition <landing> <state>
run.ts artifact <landing> <key> <path-relative-to-.harness>
run.ts readiness <landing> <score> <ready|not-ready>
run.ts confirm <landing> <kind>
run.ts fallback <landing> <capability>
run.ts validation <landing> <report-path> <passed|failed>
run.ts bump-brief <landing>
```

Invoke each as `node $S/state/run.ts <subcommand> …`.

One landing is one folder in the user's project: the site at the top level
(`src/`, `public/`, `package.json`, `dist/` after build; host it or commit it
as is) and everything else hidden in `<landing>/.harness/`: brief, research
notes, reference synthesis, page strategy, `page.json`, `design-plan.md`,
`assets-manifest.json`, claim register, `gate.yaml`, validation report,
`readiness-summary.md`, `assets/` (user files, never overwritten),
`references/`, `evidence/`, `state.json`. The folder name is the run id;
`run.ts init` takes `landing` unless another name is given. Never say
`.harness` to the user; say "the landing folder".

## Talking to the user

Progress lines, in this order and these words only:

1. Positioning formed
2. Design direction from examples ready
3. Structure and texts ready
4. Design plan ready
5. Design assembled
6. Phone version checked
7. Search readiness set up
8. Analytics added
9. Forms and buttons checked
10. Design reviewed
11. Found problems fixed

Never show internal terms outside the technical appendix; the blocklist and
replacements are in `references/vocabulary.md`. Read it before writing any
user-visible line. Show the body of `readiness-summary.md` verbatim: it opens
with the score and verdict, lists limitations and assumptions, and ends with
"tell me to publish, or ask for an improvement".

## Escalation

| Situation | Behavior | Message |
|---|---|---|
| A business decision is missing | Ask one focused question | "Before continuing I need one decision…" |
| A reference is unreachable | Continue with the others | "One example could not be studied; I used the others." |
| Proof is unconfirmed | Exclude the claim | "The unconfirmed number was not used." |
| A code or visual issue is fixable | Fix and re-check | (do not interrupt the user) |
| A technical blocker persists | Save the work, explain the step | "The page is built, but the form needs…" |
| The gate narrowly fails | Show the limitation honestly | "Almost ready; one problem remains…" |

The user is involved only when their knowledge, decision, approval, asset, or
credential is needed. Publishing never happens without an explicit request.

## Calibration

Gate thresholds (`templates/gate.yaml`), the brief readiness minimum (80), the
question-batch limit (5), and the repair budget (5 cycles, stop after 2 without
gain) are starting values. After five real runs, compare `readiness_history`
and `adapter_fallbacks` across `*/.harness/state.json` and adjust the template.
