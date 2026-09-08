---
name: mastergo-ui-fidelity
description: Reconstruct and polish production frontend pages from MasterGo designs. Use when reading MasterGo MCP data or `.mastergo/design` snapshots, recovering assets and exact geometry, implementing a page or section without copying broken D2C layout, comparing browser screenshots, fixing visual differences, or advancing an approved page into real routes, data, responsive layouts, and motion.
---

# MasterGo UI Fidelity

Build from design evidence, validate in a real browser, and advance through explicit quality gates.

## Read project rules first

Before changing code:

1. Inspect `git status --short --branch`.
2. Read repository `AGENTS.md`.
3. Read `$nice-cloud-v2-ui` only for a Nice Cloud V2 project that uses it; do not make an unrelated greenfield project depend on that skill.
4. Inspect the target route, global layout, navigation, backgrounds, overlays, and nearby approved code.
5. Preserve unrelated changes and approved sections.

Project rules and the user's current scope override this Skill. When repository rules require a pull, attempt it before project inspection; if the checkout has no remote/upstream, report that fact without inventing one.

## Keep acceptance separate from execution

- Resolve short replies and numbered choices against the actual question or option they answer. Visual acceptance such as “可以” or “还原得可以” closes the current visual review; it does not by itself authorize the next delivery stage, copy changes, status hints, new languages, or interactions.
- When the user has approved a concrete implementation step, complete that step without asking again. Do not turn this boundary into a confirmation requirement for every reversible edit.
- A selected “inspect only” option authorizes inspection and review artifacts. A selected subset of fixes authorizes that subset; keep uncertain or excluded items out of the patch.
- Plan documents and prior proposals are evidence of intent, not a substitute for the latest execution boundary. Preserve a requested independent-project boundary and honor explicit exclusions of another frontend's code, even if reusing it would be faster.

Read [scope-and-baselines.md](references/scope-and-baselines.md) when reviewing an accepted page, changing stages, applying a selected subset, or recovering from an overbroad change.

## Choose the MasterGo surface

When both surfaces are available, use **web MasterGo in the connected browser as the primary evidence surface**. It is the repeatable path for opening a file/page/layer, reading read-only native annotations, recording node IDs and geometry, and pairing design evidence with the local browser render. Use the documented browser surface and keep each successfully inspected node's evidence.

Use the **MasterGo desktop app as a secondary visual review surface**. It is useful for judging the official rendering of blur, masks, clipping, gradients, and overall visual impression after a browser-based correction. App-only visual inspection does not replace recorded node properties or a reproducible browser comparison; do not infer a CSS value from an app screenshot alone.

Keep the roles distinct: web MasterGo acquires and records design evidence, the local browser measures the implementation, and the app performs an optional final visual sanity check. If only the app is available, state the evidence limitation and avoid claiming repeatable node-level verification. If only web MasterGo is available, proceed with the web evidence and report that the app review was not performed.

## Select the active stage

Use the smallest authorized stage:

1. **Design acquisition** — obtain structure, screenshots, dimensions, text, and assets.
2. **Static reconstruction** — implement geometry and complete screenshot calibration.
3. **Production integration** — migrate to the original route and connect real actions or data.
4. **Responsive adaptation** — implement mobile and intermediate breakpoints from evidence.
5. **Motion** — add interaction and entrance animation after static geometry is stable.

Read [delivery-stages.md](references/delivery-stages.md) before advancing beyond static reconstruction.

## Execute static reconstruction

Read [static-reconstruction.md](references/static-reconstruction.md) before implementing or polishing a static MasterGo page.

- For font, weight, or text-style differences, read [typography-fidelity.md](references/typography-fidelity.md).
- Before relying on browser captures or refreshing a built preview, read [capture-and-preview.md](references/capture-and-preview.md).

Core sequence:

1. Establish route, target viewport, content width, and preserved global components.
2. Collect a full-page screenshot, node structure, isolated section previews, and important background ancestors.
3. Map design nodes into full-width backgrounds and centered content layers.
4. Reuse original SVG, PNG, image, font, logo, and certificate assets.
5. Build semantic page sections. Use absolute coordinates only inside a section.
6. Render at the exact target viewport and measure DOM rectangles.
7. Compare reference/current screenshots, blend, and amplified differences.
8. Correct section geometry before typography, effects, and decoration.
9. Run `git diff --check`, `pnpm test`, and `pnpm build`.

## Treat D2C as evidence

Use D2C for:

- text;
- hierarchy clues;
- dimensions and coordinates;
- colors, typography, effects, and asset paths.

Do not copy its root layout, generated component tree, or ordinary document flow. Generated exports may contain invalid nesting, duplicated layers, broken SVG filters, or design-canvas coordinates.

## Preserve invariants

- Separate full-width backgrounds from fixed-width content.
- Preserve the design-specified fixed desktop shell as an exact coordinate system (`1200px` when specified), not a proportional scene that may be scaled to fit.
- On Nice Cloud V2 pages, read and enforce `$nice-cloud-v2-ui`'s `references/fixed-desktop-layout.md`. Desktop scene scale must remain `1`.
- Preserve approved global navigation.
- Isolate legacy backgrounds and overlays on new routes.
- Do not modify old routes during V2 construction without authorization.
- Do not invent business behavior for static controls.
- Do not bake live text, buttons, or media into recovered background images.

## Apply quality gates

Apply these gates to the authorized changed surface; an inspection-only task finishes with evidence and an unchanged-source check, without requiring a build or implementation. For an implemented change, do not call work complete until:

- bounding boxes, spacing, typography, radii, effects, and asset choices match;
- every required desktop viewport passes the fixed-shell width, X, ancestor-scale, and relative-child-coordinate assertions;
- the correct route is used and old routes do not regress;
- legacy overlays do not cover the page;
- exact-viewport screenshots have been reviewed;
- nested scroll containers and clipped artwork have been checked;
- `git diff --check` passes;
- production build succeeds or remaining failures are proven pre-existing.

For section-by-section work, stop after the requested section. For whole-page authorization, finish all visible sections and request one consolidated review.

## Capture confirmed lessons

When the user requests or has authorized skill maintenance, record the reusable cause, prevention rule, and verification method in the relevant reference. Visual acceptance alone is not authorization to edit global skills.

Keep page-specific values, screenshots, and execution history in project evidence. Do not turn one machine's font weights, browser failure, or project convention into a universal rule. Preserve unrelated skill resources, keep a recoverable old copy, and validate the installed skill.

## Compare screenshots quantitatively

Use `scripts/compare_screenshots.py` when Pillow is available:

```bash
python .agents/skills/mastergo-ui-fidelity/scripts/compare_screenshots.py \
  reference.png current.png \
  --height 760 \
  --match-size crop-min \
  --region left-bg:0,60,640,499 \
  --out-dir /tmp/mastergo-compare
```

Use strict size matching for geometry. Use `crop-min` only for a known scrollbar or capture-edge difference and report it.

MAE is diagnostic, not a universal pass score. Always inspect the rendered images and important edges.

## Report evidence

Report:

- route or URL;
- completed sections;
- target viewport and key measurements;
- screenshot and build validation;
- known warnings;
- changed files;
- commit, push, and deployment status.

Never claim pixel-perfect fidelity without screenshot evidence.
