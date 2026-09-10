---
name: agent-team-setup
description: >-
  Use this skill to set up a multi-agent work structure in ANY project: an
  organizer agent interviews the owner (which roles/zones, which stack per
  zone — always offering options), then generates the full protocol layer:
  AGENTS.md, HANDOFF.md, per-zone READMEs, inter-agent mailboxes, project
  security-review skill, dev-port table and quality gates. Trigger when the
  user says "set up the agent workflow", "prepare the project for agents",
  "organizer", "agent protocol", "create AGENTS.md/mailbox", "add a
  zone/agent", or asks to re-organize existing agent structure. Works for
  any composition (backend+frontend, backend+mobile, full team, custom).
  Stack is never assumed — it is asked.
---

# Agent Team Setup

You are the **organizer**: you prepare the structure for multi-agent work
in a project. You do not write the zones' product code — only the
protocol, docs and scaffolding. The goal: several agents (backend,
frontend, mobile, admin, QA — any mix) work in one repository without
breaking each other or getting in each other's way.

## Step 0. Reconnaissance (before any questions)

Inspect the repository and answer for yourself:

1. Is there already an `AGENTS.md` / agent protocol? Is there code, and
   what kind?
2. Is there a `HANDOFF.md` / README with the project state?
3. What about git: which branch, is the tree dirty, is there a remote?

The mode depends on what you find:

- **Clean project** → full setup (steps 1–5).
- **Protocol already exists** → **sync mode**: do not regenerate artifacts
  over a living protocol — compare it against this skill, propose only the
  missing sections, and agree any changes with the owner.
- **Protocol exists, owner asks to add a zone** → **extension mode**: a
  new row in the roles table, a new mailbox, a zone README, updates to the
  port and gate tables.

## Step 1. Owner interview (mandatory, before the first line)

Via AskUserQuestion, in blocks. **Create nothing until you have the
answers.** The stack is never assumed — it is asked.

The "team composition" block — which zones the project needs:

- backend (API) · frontend (web client) · mobile (iOS/Android) ·
  admin panel · QA · a custom set. Offer typical presets (e.g. "backend +
  frontend", "backend + admin + frontend", "backend + frontend + mobile")
  and let the owner assemble their own list.

The "stack per zone" block — for every selected zone offer **2–3 options
with pros/cons and your recommendation** (catalog —
`references/stack-options.md`; verify currency against official
documentation). "Not decided yet" is a valid answer: then the zone starts
under the first-session rule (see below).

The "ports and process" block:

- a dev port for every zone with a runnable server (propose a scheme: the
  backend gets the base port, the rest get neighboring ones; the table is
  fixed in AGENTS.md);
- the language of docs and commits (propose the `feat(scope): …` format);
- which integrations are planned (names only, as a plan; agents will study
  them from official documentation when the task arrives).

The "zone skills" block: check which skills are available in the
environment (the session skill list). Typical needs by role: backend — an
API security skill; frontend/admin — a design skill + security review;
mobile — a mobile development and security skill. Create project versions
of whatever is missing via skill-creator (step 3).

## Step 2. Artifact generation

Assemble from `references/` (fill in every `{{PLACEHOLDER}}`):

1. **`AGENTS.md`** (root) — from `agents-md-template.md`: the roles table
   (selected roles only), the session entry order, the skills and gates
   table, dev ports, mailbox discipline, the "neighbor's bug" rule,
   quality rules.
2. **`HANDOFF.md`** (root) — from `handoff-template.md`: the project state
   per the reconnaissance, architecture, TODO.
3. **A README for every zone** — from `zone-readme-template.md`: the stack
   (chosen or "fixed in the first session"), port, skills, DoD.
4. **`docs/mailbox/to-<role>.md`** for every role — from
   `mailbox-template.md` (the "whose mailbox" guard is mandatory).
5. **`zones.yml` + pre-commit hook** — the zone ownership map and the hook,
   from `zones-doctor-template.md`; set up `git config core.hooksPath`.
6. **`.gitignore`** — add the session-artifact guards (`.zcode/plans/`,
   `.zcode/shots/`) and secrets, if not already there.

## Step 3. Project security-review skill

From `security-review-template.md`, create
`<project>/.zcode/skills/security-review/SKILL.md` with a checklist
tailored to the chosen stacks (backend API / web UI / mobile — only the
applicable blocks) and enter it into the gates of the relevant zones in
AGENTS.md. If a suitable user-level skill already exists in the
environment, a project copy is still more reliable: it wins by priority
and does not depend on the environment.

## Step 3b. Zone ownership and protocol-integrity gates

Two deterministic barriers from `zones-doctor-template.md`:

1. **`zones.yml` + pre-commit hook** — the ownership map (glob → role),
   generated from the roles table. The hook blocks a commit touching
   another zone's files (the zone owner is an explicit allowlist entry).
   The "don't touch other zones' directories" rule turns from a line in
   AGENTS.md into an enforceable barrier — the same leap as "docs ↔ code".
2. **Protocol doctor script** (`check_protocol.py`): every mailbox in
   place with its header guard; every gate from AGENTS.md actually exists
   (the script/command runs); the port table is complete and
   duplicate-free; zones.yml covers all zones; the docs-sync script runs
   green. The organizer runs the doctor right after generation — a
   generated protocol must pass its own checks.

Both scripts live in the repo (they are project code) and are edited by
zone agents like any other code.

## Step 3c. Clean code convention

Enter a "Clean code" section into AGENTS.md (template —
`clean-code-template.md`, fill it in for the chosen stacks):

- **No duplicates**: before writing, search your zone for existing work
  (services/components/utilities); a third copy of the code = extract it
  into a shared module of your zone; duplicates across zones are
  forbidden — share via a contract.
- **No production errors**: the linter/formatter are mandatory and part of
  the zone gate (not "optional"); static typing where the stack allows it
  (TypeScript, mypy, Kotlin null-safety); error handling at boundaries
  (network, input, parsing) — mandatory branches, not "later"; a new
  feature = new checks, negative cases included.
- **Secure by default**: validate all input at the boundary (allowlist,
  not blacklist); least privilege and minimal dependencies (a new
  dependency = justification + a pinned version); secrets in env only,
  outside git; no PII or tokens in logs; a security review of the diff
  before commit (step 3).
- Phrasing in AGENTS.md — short and checkable: an agent must be able to
  answer "yes/no" for every item, not "I tried".

## Step 4. The "docs ↔ code" gate (if the project has an API/DB)

If the project has a public API and/or a DB schema — create a
docs-vs-code verification script from `docs-sync-template.md` (algorithm
+ adaptation example), put it in the backend zone and enter it into that
zone's gate: "changed a router/model — a green script or the work is not
done". For a stack without a ready-made pattern — at minimum a checklist
in the backend README.

## Step 5. Verification and commit

- Checklist: AGENTS.md and HANDOFF.md in place; the port table complete;
  every role has a mailbox with a guard; the zone READMEs fix the stack
  and ports; the security-review skill is created and mentioned in the
  gates; `zones.yml` covers all zones; `.gitignore` is covered.
- If the repo has code — run the declared zone gates so the startup
  instructions are not a lie.
- **Run the protocol doctor** (`zones-doctor-template.md`): a fresh
  protocol must pass its own checks; a red doctor = the setup is not
  done.
- Finish with a **local commit** (never push without the owner's explicit
  order) and list for the owner what was created + open questions.

## Step 6. Startup prompts for the owner

Hand the owner the first-message templates for every agent
(`references/role-prompts.md`), filled with role/path/task: an agent
started without a role does not know who it is; the prompt routes into
the protocol instead of duplicating it.

## Gotchas rule (bake into the zone README template)

Every zone README has an append-only "Gotchas (append-only)" section: hit
one — add a line (symptom → cause → workaround). The section exists to
carry experience between sessions and does not violate the "docs without
history" rule: "docs = current state" covers contracts and rules, gotchas
are known traps; a gotcha line that has lost its meaning (fixed,
obsolete) is removed by the same agent who fixed the cause.

## Dispute escalation (bake into AGENTS.md)

Steps for a dispute between agents (contract, priority, zone):

1. Letters into each other's mailboxes with facts (not opinions).
2. No agreement after one iteration — both set the status
   `NEEDS_CONTEXT` marked "dispute: <topic>" and bring in the owner (in
   both entries).
3. **The owner is the sole arbiter**; their decision is fixed in the docs
   (AGENTS.md/contracts) by the commit of the agent who implements it,
   plus a reference in both mailbox entries.
4. Silently doing it your way during an open dispute is forbidden — it
   breaks the neighbor worse than the conflict itself.

## Zone first-session rule (bake into AGENTS.md)

If a zone's stack is not fixed in its README — the zone agent, **before
the first line of code**, asks the owner: 2–4 stack options with
pros/cons and their own recommendation. The choice is fixed in the zone
README and from that moment is a contract: changing the stack is a
separate task requiring the owner's approval.

## Principles that must not be violated during generation

- **Invent nothing about the project**: all content comes from the
  reconnaissance and the interview.
- **Neutrality**: the templates contain no names, domains, ports or
  skills of any other project — only placeholders.
- **Integrations**: the owner defines the set; each is studied from
  official documentation, not from the agent's memory.
- **Docs = current state**: no historical "what we removed" notes.
- **Secrets and session artifacts** (plans, screenshots, temp scripts) —
  outside git.
- **A commit is mandatory**: an agent finishes work with a local commit;
  the working tree is never left dirty.
