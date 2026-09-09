---
name: onestep-decks
description: Build presentation decks for OneStep in the CEO's voice and the company's slide design system — fundraising/investor decks, LP/annual-meeting decks, board updates, company all-hands, conference talks, and client/prospect sales decks (senior living, med device, RBOs). Use this skill WHENEVER the user asks for a deck, presentation, slides, pitch, talk, all-hands, QBR, board update, sales deck, or investor material for OneStep — even if they don't say "deck" ("prepare something for the team about H2", "I'm speaking at a conference", "adapt our sales deck for a rehab prospect"). Also use it for OneStep one-pagers/flyers and A4 case studies (co-branded collateral), when editing or extending an existing OneStep deck, exporting one to PDF, when the user needs a OneStep brand asset (logo, photo, product screen, customer logo, QR code, template shell), or when the user gives feedback on a deck it produced ("the CEO cut X", "remember this") — run the feedback-loop protocol. It encodes the slide engine, per-audience narrative playbooks, the CEO's tone and editing rules, external-safe company facts, the asset library catalog, and the PDF export pipeline.
metadata:
  version: "1.1.2"
---

# OneStep Decks

Build decks that look, sound, and argue like OneStep's CEO built them. **Every visual rule comes from the unified OneStep design system** — a synced copy ships in `references/design-system/` (start with `DESIGN.md`; the slide/print contract is `surfaces/print.md`). This skill adds four things on top: the **slide engine**, the **voice**, the **company narrative/facts**, and **per-audience playbooks**. Product screens that appear on slides are built with the sibling `onestep-design` skill (product layer) and framed here.

Paths in this file are relative to this skill directory (`${CLAUDE_PLUGIN_ROOT}/skills/onestep-decks/`).

## Workflow

1. **Identify the audience** — this decides everything: which facts are allowed, which narrative arc to use, how assertive to be. Read the matching section of `references/deck-types.md` (fundraising / conference / company / client / LP-annual-meeting / board).
2. **Check fact freshness.** Read `references/company.md` for the canonical external-safe facts, narrative, and terminology. For any external deck (client, LP, conference), also read `references/marketing-assets.md` — the approved proof points, signature copy lines, logo walls, testimonials, and patient stories. Facts are dated ("as of H1 2026") — if the deck involves metrics, ARR, clients, or regulation, ASK the user for current numbers or search for regulatory updates rather than assuming the reference is current. Never present stale numbers as current.
3. **Internal figures come from the user, every time.** This plugin is published in a public repo, so it holds no burn, runway, ARR plan, per-client $, churn names, readiness scores or funding plans. For all-hands, board and diligence-stage decks, ask the user to paste the current internal numbers; use them in the deck and in this conversation only. Never write them into any plugin file, including `learnings.md`.
4. **Respect template governance for sales decks.** An official version-controlled sales deck template exists (maintained centrally; vertical variants come from Naama). For client decks, default to drafting content compatible with it or adapting it — don't invent a competing sales narrative.
5. **Apply the voice.** Read `references/voice.md` before writing a single title — including the external-register section for customer/LP decks. The CEO edits hard; writing it right the first time saves a round.
6. **Apply accumulated learnings.** Read `references/learnings.md` — distilled rules from past feedback on decks this skill built. These are newer than the general guidance and win on conflict. Then check the `examples/` section of `references/asset-catalog.md` — if an approved example exists for this deck type, fetch and read it and imitate its structure and register (not its facts).
7. **Build on the engine.** Copy `assets/deck-template.html` as the starting point — it contains the full CSS system (its `:root` mirrors the design-system tokens), navigation JS, and one commented example of every slide archetype. Don't rebuild from scratch; don't import Google Fonts differently; don't change the 1280×720 geometry. Any visual question the template doesn't answer → `references/design-system/surfaces/print.md`, then `DESIGN.md`. **Product mockups on slides**: build them on the product layer (onestep-design skill: 14px body, near-white canvas, product components, nds icons), do not restyle them, and frame them per `print.md` §Putting a product mockup on a slide.
8. **Pull assets from the library, not from imagination** — see *Asset library* below. Never fabricate an asset that isn't there; use a labelled placeholder and tell the user.
9. **Respect sensitivity boundaries** (below). What goes in an all-hands must not leak into a client deck.
10. **QA before presenting**: render slides mentally against the checklist at the bottom; verify slide markers are numbered correctly; verify structure (`grep -c '<section'` equals closed sections).
11. **Export to PDF only when asked**, using `scripts/export_pdf.py` (see `references/pdf-export.md` for the pipeline and its gotchas).
12. **Capture feedback.** If the user gives feedback at any point — corrections, cuts, "the CEO changed X", "next time do Y" — run the feedback-loop protocol in `references/maintaining.md` before the conversation moves on.

## The slide engine (summary — full detail in the template)

- **Geometry**: 1280×720 fixed, scaled to viewport via JS transform. One `<section class="slide">` per slide.
- **Font**: Nunito Sans for everything except testimonial quotes and editorial callouts, which are Georgia Italic — the single typeface exception in the whole design system, allowed on print only (`print.md`). Google Fonts link in the template; the PDF pipeline embeds Nunito Sans locally; Georgia is a system font.
- **Palette**: the design-system tokens, mirrored in the template's `:root` — navy `#0F3157` / deep `#0C2545`, blue `#1B81DC`, strong-blue `#0D5097`, ice `#85BEF4`, ice-bg `#E2EEFC`, tint `#F1F7FE`, text/ink `#3E3D3B`, greys `#716D69/#8C8884`, line `#E7E6E6`, panel grey `#F6F5F5`; status good/warn/bad/critical `#2C9D72/#F5960B/#FB5E1B/#B00404` (clinical meaning only). Teal `#1CA8B0` and pink `#FEA2EF` are **chart colors** (pink also the one rare accent surface) — not UI colors.
- **Cards & panels**: flat, **4px radius** everywhere (system-wide rule), 1px `--line` border on white or borderless on tint; navy callout card for the one-line takeaway. No shadows on slide cards; a framed product mockup may carry a soft shadow.
- **Slide archetypes** (all present in the template): dark title (brand-squiggle decoration); dark chapter divider (label + short title only); content slide with `hdr` (eyebrow + `NN / NN` marker); stat-card row (`.stat` with `.u` unit); two-column comparison cards (tint vs navy); numbered cards (`.num-badge`); horizontal step/flow strip; readiness table (`.rt`); brand-squiggle highlight slide (full-bleed blue, one white statement; pink variant rare); testimonial slide (Georgia Italic `.quote`, 1/2/3-up variants per the brand template); key-takeaways list; navy callout card (`.card.navy`) for the one-line takeaway; dark closing.
- **Brand motif**: the squiggle is THE brand element, in exactly two forms — tone-on-tone loops on full-bleed colour surfaces, and a white line weaving over photography (`assets/brand/squiggle-line.svg`, shipped in the plugin). Don't invent other decoration.
- **Numbering**: cover and closing carry no marker; everything between is `NN / TOTAL`. When adding/removing slides, renumber ALL markers (the template includes a renumbering script snippet).
- **Structure**: long decks get chapters — simple dark divider slides ("Chapter One" eyebrow + a short title). All-hands pattern: context → accomplishments → opportunity → what needs to happen → takeaways → close.

## Asset library

The plugin ships only what every deck needs: `assets/deck-template.html` and `assets/brand/` (white + dark logo PNG, `squiggle-line.svg`). **Everything else — ~130 files, 21 MB — lives in the `assets/` folder of the `onesteprnd/design-assets` GitHub repo** and is fetched on demand:

- **Find**: read `references/asset-catalog.md` (auto-generated index: every file with dimensions and a one-line description, grouped by folder) or run `python3 scripts/fetch_asset.py --list photos/`.
- **Fetch**: `python3 scripts/fetch_asset.py photos/michael-portrait.jpg "logos/customers/*-grey.png" --readme`. Files land in `./assets/<same path>`, so a deck in the working directory can reference `assets/photos/…` relatively. `--readme` also pulls the folder's README — the usage rules (sizes, provenance, when NOT to use). **Read the README before placing anything from `photos/`, `product/` or `logos/`.**
- **Embed**: `python3 scripts/fetch_asset.py --embed brand/onestep-logo-white.png` prints a `data:` URI for a self-contained HTML/PDF.
- Folders: `brand/` (logos, squiggle backgrounds 1920×1080, squiggle line), `logos/customers/` (7 "Trusted by" logos, colour + warm-grey), `templates/` (EMPTY 16:9 layout shells of the 10 LP-deck slides; `templates/a4/` the 15-page A4 case-study system; `templates/social/` the 3×3 carousel grid), `photos/` (hero photography + alpha cutouts, exercise figures), `icons/` (content icons, case-study icon set, FDA/ISO badges, squiggle glyph + loop pattern, phone-in-hand frame, `icons/illustrations/`), `product/` (patient-app screens, white-label, mymobility, Progress Note, dashboard card, charts), `qr/` (iOS/Android "try OneStep" codes), `examples/` (the official 2026 brand template deck and the approved one-pager, as PDFs — for any visual question the rules don't answer, fetch and imitate them: structure and register, not facts).
- When `raw.githubusercontent.com` is unreachable, say so and offer the user the direct GitHub link; `ONESTEP_ASSETS_DIR` pointing at a local checkout bypasses the network.
- Reference docs in this skill mention library paths as `assets/<folder>/<file>` — that always means the library, fetched as above.

## Voice — the 10-second version

Slides carry **structure and facts; the CEO carries the narrative verbally**. Minimal text, zero clichés, no meta-commentary, no self-congratulation, honest about bad news without dwelling. Titles are plain and confident, not clever or presumptuous. Say "RBOs" not "payors". Full rules and observed edit patterns: `references/voice.md` — read it every time.

## Sensitivity — hard rules

- **Internal only** (all-hands, board): burn, runway, churn names & amounts, readiness scores, per-client $ figures, funding plans, pre-R&D operating profit framing. None of it is stored in this plugin — it arrives from the user and stays in the conversation.
- **External-safe** (fundraising, conference, client): headline metrics (ARR milestone, GM, NRR/GRR, patients measured, clinics, ROI multiple), clinical outcomes (25% fewer falls, 88% maintain/improve), the thesis and moat. Fundraising decks may include more financial detail — confirm scope with the user.
- **Never in any deck**: PHI or realistic patient names (HIPAA — use `Patient A`, IDs, or initials in any example UI/data), and never invent client names, quotes, testimonials, or patient stories — approved ones live in `references/marketing-assets.md`; anything else comes from the user.
- **Never in any plugin file**: internal figures or PHI. The repo is public.

## Feedback loop — how this skill improves itself

Plugin files are static: nothing persists between conversations unless a change is committed to the `design-assets` repo and the plugin is updated. When the user gives feedback on a deck (or says "remember this", "the CEO cut X", "stop doing Y"), follow `references/maintaining.md`: classify the feedback (rule → `learnings.md`; example → `assets/examples/` in the library; fact/asset → the matching file), produce the exact edited files, bump the version, and hand the user a commit-ready change. Apply the new rule to the current deck immediately, without waiting for the commit.

## Quality bar (check before presenting)

Nunito Sans everywhere (Georgia only on quotes)? Navy-on-white with warm greys, text `#3E3D3B`? Cards and chips at 4px radius? Product mockups left on the product layer and framed, not restyled? Markers renumbered and continuous? Titles plain, short, non-presumptuous? Any sentence the CEO would cut ("being straight about it"-style meta, "net-net" summaries, hype like "do more with less")? Facts either from company.md, from the user, or verified by search — with nothing stale presented as current? Sensitivity boundary respected for the audience? Every image a real library file or a labelled placeholder? If exporting PDF: page count matches slide count, fonts embedded, backgrounds printed.
