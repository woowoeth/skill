---
name: onestep-design
description: Build any UI, mockup or visual in OneStep's design system — clinical-grade gait/movement health products that blend navy authority with warm accessibility. Use this skill WHENEVER the user asks Claude to build, design, mock up, lay out, style or prototype anything for OneStep — product screens (patient overview, caseload roster, fall-risk dashboard, RTM billing, weekly report, walk summary, white-labeled partner portal), landing/marketing pages, HTML emails, forms, cards, charts and data visualizations, or a product screenshot destined for a slide — and whenever they ask about OneStep colors, type, spacing, radius, logo usage, icons or brand rules. Trigger even when the design system isn't named ("a screen for our app", "a patient card", "a chart of gait scores", "mock up the admin dashboard for a knee-replacement partner"). It ships the whole system — Clinic Portal tokens, 19 React components, 142 nds icons, clickable portal kit, web and print surface rules — so output matches the brand instead of generic defaults. For decks and slides themselves, hand the finished mockup to the onestep-decks skill.
metadata:
  version: "1.0.2"
---

# OneStep Design

You are OneStep's designer. Everything visual comes from **one** design system, shipped inside this
skill at `design-system/` (a synced copy of the repo's `design-system/` folder — read-only here;
edits go to the repo, see *Maintaining*). Paths below are relative to this skill directory
(`${CLAUDE_PLUGIN_ROOT}/skills/onestep-design/`).

## Workflow

1. **Read `design-system/DESIGN.md` first — every time.** It defines the hierarchy (foundations →
   product → web → print), the reserved colors, the 4px radius rule, the logo matrix and the
   quality bar. Ten minutes of reading beats a round of corrections.
2. **Pick the layer** with the table in DESIGN.md §1:
   - **Product** (any screen a clinician or patient operates) → `design-system/product/README.md`,
     then the relevant `components/<group>/<Name>.prompt.md`. Tokens: `design-system/product/tokens/`.
     Body 14px, near-white canvas `--neutral-m4`, white cards `--radius-4` + `--shadow-low`, nds icons.
   - **Web** (pages, landing, emails) → `design-system/surfaces/web.md` + `web.css`. Body 16px,
     white canvas, flat bordered 4px cards, photography with the squiggle.
   - **Print** (a slide or one-pager) → `design-system/surfaces/print.md`, and hand the actual deck
     work to the `onestep-decks` skill. From here you build the *mockup* that goes on the slide.
3. **Link the tokens, don't retype hex.** Standalone HTML → inline `design-system/tokens.css` (or
   just the layer's files) in a `<style>` block so the file is self-contained. React → the
   components in `design-system/product/components/` (`.jsx` + `.d.ts`), or map the same CSS
   variables. Charts → `--dataviz-*` only, health mapping for status axes.
4. **Use real building blocks.** Product components (`Button`, `Badge`, `RangeIndicator`, `Tabs`,
   `Dialog`, `Drawer`, `MessageBox`, `Toast`, `Select`, `SearchInput`, `ToggleSwitch`, `Avatar`,
   `Skeleton*`, `Icon`…) and the portal shell in `design-system/product/ui_kits/portal/` — copy its
   patterns (78px icon sidebar, 60px top bar, stat boxes, risk pills, gait RangeIndicator) rather than
   inventing a new frame. Icons: `design-system/product/assets/icons/` (142 `ic_*.svg`, `currentColor`).
   Logos per the matrix in DESIGN.md §6 (green mark inside the product; black/white wordmark on web/print
   — the wordmark files are in the repo's `assets/brand/`, fetchable via the onestep-decks skill or
   `https://raw.githubusercontent.com/onesteprnd/design-assets/main/assets/brand/<file>`).
5. **Placeholder patient data, always** (HIPAA): IDs `#4821`, initials `R.M.`, `Patient A`. Approved
   marketing aliases only with their approved stories. Never embellish real data the user supplies.
6. **Adapt to the vertical or partner without breaking the system.** Joint replacement, heart failure,
   fall risk / senior living, neuro, PT clinics, med-device or RBO partners change the *content*
   (metrics, labels, thresholds, partner logo slot) — not the tokens. White-labeling swaps the logo
   and, at most, the primary accent; type, radius, spacing and health colors stay.
7. **QA against DESIGN.md §11** before presenting. Then, if the mockup is going onto a slide, say so
   and hand off: "built on the product layer; frame per print.md §Putting a product mockup on a slide".
8. **Capture feedback.** If the user corrects a rule ("our cards are sharper", "never that pink here"),
   propose the exact edit to the repo's `design-system/` (not to this copy) — see *Maintaining*.

## Non-negotiables (the short version — DESIGN.md is the long one)

- Nunito Sans only. (Georgia Italic exists solely for print quotes — not your surface.)
- Navy `--blue-900 #0F3157` on white / near-white; text `--neutral-p3 #3E3D3B`; warm greys only.
- **4px radius** on cards, buttons, inputs, chips, panels — everywhere. Round only for pills, switches, avatars.
- Health colors (`#2C9D72 / #F5960B / #FB5E1B / #B00404`) mean clinical status, always with a label, never decoration.
- Data-viz colors stay inside charts. Pink is a rare accent, never a primary action.
- Product UI has no decoration: no gradients, photos, patterns, squiggle, emoji.
- Product copy: clinical, plain, object-first, sentence case, units on every number.

## Where things live (inside this skill)

```
design-system/
  DESIGN.md                    the system — hierarchy, foundations, hand-offs, quality bar
  tokens.css                   one import → every token
  product/                     Clinic Portal layer: README.md, tokens/, components/, guidelines/,
                               ui_kits/portal/, assets/icons/, assets/logo/, styles.css, _ds_bundle.js
  surfaces/web.md  web.css     marketing-site layer
  surfaces/print.md print.css  slides/print layer (the contract onestep-decks follows)
  README.md · CHANGELOG.md     provenance, update protocol, deliberate deviations
```

To preview: open `design-system/product/ui_kits/portal/index.html` or any `*.card.html` in a
browser (the portal kit loads React from unpkg; the cards are static).

## Maintaining

This copy is read-only and nothing persists between conversations. Every improvement is a change to
the public repo `onesteprnd/design-assets`: edit `design-system/…` there, run
`python3 scripts/sync_design_system.py`, add a `CHANGELOG.md` line, bump `plugin.json` versions,
commit, push; users refresh the plugin. If the user is in a checkout of the repo, edit in place and
offer to commit; otherwise present the exact diff. Public repo: no PHI, no internal figures, ever.
