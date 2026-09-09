---
name: design-proto
description: Track A high-fidelity prototyping — build prototypes directly in the real frontend codebase using the real, shipped design system, so what gets built is accurate to what will ship rather than a visual approximation. Inspects the codebase's components and tokens first, then reuses existing components by default and asks permission before creating new ones. Requires live repo access via Claude Code.
---

# /design-proto — High-Fidelity, In-Repo Prototyping

Designers work directly in the frontend codebase, using the real design system.
Prototypes are accurate to what will ship — not visual approximations of it. This is what
makes dev handoff near-zero-translation (see `/handoff-pr`).

## Hard requirement

**This skill requires live access to the real frontend codebase.** There is no
standalone or offline mode. If Claude Code is not connected to a repo with a frontend
app in it, stop and say so — then point the user to `/quick-proto`, which is designed to
work without a codebase.

Before anything else, confirm there is a frontend app present. If the repo has no
components, no design tokens, and no styling system, this skill has nothing to be
accurate to.

## Step 1 — Inspect the design system first

Before writing a single line, read the codebase and build a picture of what already
exists. Do not skip this — the whole value of Track A is that the prototype uses what's
really there.

Look for, and actually read:

- **Component library** — a `components/`, `ui/`, `design-system/`, or packages
  directory. Note what exists, its props API, and its real usage sites.
- **Design tokens** — Tailwind config, CSS custom properties, a theme file, a tokens
  package. Colors, spacing scale, typography scale, radii, shadows, breakpoints.
- **Patterns in use** — how forms are built and validated, how modals and drawers open,
  how loading and error and empty states are done, how navigation and routing work.
- **Conventions** — file layout, naming, styling approach, state management, data fetching.
- **Storybook / docs / tests** — often the fastest accurate read of the component API.

Prefer reading real usage over reading the component definition alone. How a component is
actually used in three places tells you more than its prop types.

## Step 2 — Confirm readiness

Report back before starting, concretely — naming what you actually found, not a generic
reassurance:

> I've looked at the existing design system in this codebase and I'm ready to prototype
> with you based on it.
>
> **Components available.** <the real ones, named>
> **Tokens.** <color/spacing/type scales as they actually exist>
> **Patterns.** <how forms, modals, errors, empty states are done here>
> **Conventions I'll follow.** <file layout, styling approach, state/data patterns>
>
> I will not invent new components unless it's really needed — I'll ask your permission
> first, unless you specifically tell me we're creating a new component.

If the design system is thin or inconsistent, say so plainly at this point. That's a
finding worth surfacing — and a candidate for `/design-consistency`.

## Step 3 — Component discipline

This is the core rule of Track A.

- **Default: reuse.** Build from components, tokens, and patterns that already exist.
  Never introduce a new component by default.
- **If a new component seems needed: ask first.** Explain specifically why the existing
  components don't fit — what you tried, what broke — and propose the smallest possible
  addition. Wait for permission.
- **Composition before creation.** Most "we need a new component" moments are actually
  composition of two existing ones. Try that first, and show it.
- **Extending an existing component counts as a change.** A new prop or variant on a
  shared component affects every consumer. Ask before adding one, exactly as you would
  for a new component.
- **The user can override any time** by saying explicitly that a new component is being
  created. Then build it, following the codebase's existing component conventions.
- **No off-token values.** No hardcoded hex, no arbitrary spacing, no one-off font sizes.
  If the token doesn't exist, that's a question for the user, not a magic number.

Keeping this discipline is what stops prototypes from quietly expanding the design system
with one-off, un-vetted components.

## Step 4 — Build

- Work on a branch, never directly on the main branch.
- Build real, running screens — routed, navigable, interactive where it matters to the
  question being answered.
- Use realistic data and realistic copy. Lorem ipsum and `Item 1 / Item 2 / Item 3` hide
  exactly the layout problems a high-fidelity prototype exists to expose.
- Include the unglamorous states: loading, empty, error, permission-denied, long content,
  short content. These are where design decisions actually get made.
- Keep prototype code clearly marked as prototype — a dedicated route prefix or directory,
  and a comment at the top of each new file saying what question it exists to answer.
- Follow the codebase's accessibility conventions as a floor: semantic elements, labels,
  focus order, keyboard operability.

Show progress in the running app rather than describing it. Run the dev server and put
the screen in front of the user.

## Step 5 — Wrap up and deliver

State clearly what was built, which existing components it used, anything new that was
added with permission, and what's stubbed or faked.

The prototype code itself lives in the repo on its branch — that isn't negotiable, it's
what makes this Track A. But the **write-up** has a destination, so ask:

- **Markdown file** in the repo — recommend `docs/prototypes/<feature>.md`, next to the code
- **Claude artifact** — a shareable page for stakeholders who won't run the branch
- **Straight into a PR description** via `/handoff-pr`
- **Confluence / Google Drive / Notion** — only if such a connector is actually attached
- **Terminal only**

If the user opts out of choosing, write the markdown file at the recommended default and
say where you put it.

Then offer `/handoff-pr` to package the branch for engineering review.

## Guardrail — prototype is not production

Prototype code is honest about its design and dishonest about everything else. Say so
explicitly on handoff: it typically has stubbed data, missing error handling, no tests,
no analytics, unhandled edge cases, and unconsidered performance. Never let "it's already
in the codebase and it looks right" get read as "it's ready to ship." The value of Track A
is that the *design* needs no translation — the engineering still does.

## Failure modes to avoid

- **Assuming a destination.** Never decide on the user's behalf where output lands. Ask.
- **Skipping the inspection step.** A prototype built on invented components is a
  low-fidelity prototype with high-fidelity costs.
- **Quiet component creation.** The single most damaging failure of this skill.
- **Off-system values.** One hardcoded hex undermines the claim that this is accurate.
- **Happy path only.** Empty, error, and overflow states are where the design breaks.
- **Building on main.** Always a branch.
