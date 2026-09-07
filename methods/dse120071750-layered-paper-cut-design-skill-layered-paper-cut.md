---
name: layered-paper-cut
description: Compile exactly the requested poster, cover, still, keyframe, infographic, B-roll, image-to-video, layout/code, or custom asset-generation prompt in an adaptive exhibition layered paper-cut design language. Use when the user names layered-paper-cut, asks for handmade paper-cut or paper-sculpture collage, or a workflow needs a prompt in this design system. The skill returns prompts only and never generates media or an unused companion prompt.
---

# Layered Paper Cut Design Skill

Turn each information item into exactly one generation prompt for the asset the caller actually requested. Apply the same recognizable handmade paper-cut language across still images, video, code-authored layouts, and custom media without forcing one ratio, palette, subject type, or motion pattern.

## Non-negotiable output rule

- Return one `generation_prompt` per ordered item.
- Compile only for the resolved `generation_mode`.
- Never add a still prompt to a video request, a motion prompt to an image request, or any other companion prompt.
- Never invoke ImageGen, Grok, FFmpeg, a renderer, or another asset generator.
- Do not expose the internal recipe unless `include_recipe: true`.

## Accepted request

Accept natural language or an ordered object containing `items`. Each item may contain:

- `id`: optional stable identifier.
- `information`: required source information and the only authority for factual claims.
- `asset_spec`: optional `asset_type`, `generation_mode`, `aspect_ratio`, `duration_seconds`, `delivery_context`, generator, medium, dimensions, timing, and delivery constraints.
- `exact_text`: optional display copy to preserve verbatim.
- `text_policy`: `auto`, `none`, `preserve-reference`, or an explicit caller-defined policy such as `timed-preserve-reference`.
- `reference_paths`: local references whose factual and visual identity must be preserved.
- `must_include`, `must_avoid`, and `design_overrides`.

The supported generation modes are `text-to-image`, `image-to-image`, `text-to-video`, `image-to-video`, `layout-or-code`, and `custom`. `asset_type` is descriptive, not a closed enum.

Resolve the request in this order:

1. Explicit `asset_spec` values.
2. The caller's wording and delivery context.
3. Built-in defaults from [formats.json](design-system/formats.json).
4. If the target still cannot be inferred, use a `3:4` editorial poster and disclose that default.

Preserve item order. Never silently discard an item.

## Design process

For each item:

1. Identify the message, factual anchors, audience, requested asset, and generation mode.
2. Derive one legible visual metaphor. Symbolic imagery may interpret the source but must not imply unsupported facts.
3. Resolve an internal recipe using explicit overrides, semantic routing, and a stable seed. Use [resolve_recipe.py](scripts/resolve_recipe.py) for structured workflows.
4. Generate or preserve display copy under the text rules below.
5. Compile only the prompt contract for the resolved mode.
6. Run the quality gate before returning or writing the package.

For direct natural-language work, read only the catalogs needed for the request. The structured resolver loads and cross-validates the full catalog set so mixed-mode arrays share one consistent version. Core routing uses:

- [formats.json](design-system/formats.json) for target defaults.
- [colors.json](design-system/colors.json), [materials.json](design-system/materials.json), and [imperfections.json](design-system/imperfections.json) for the physical paper language.
- [compositions.json](design-system/compositions.json), [subjects.json](design-system/subjects.json), [typography.json](design-system/typography.json), and [rhythm.json](design-system/rhythm.json) for spatial decisions.
- [motion.json](design-system/motion.json) only for video-generation requests.
- [routing.json](design-system/routing.json) and [prompt-contract.json](design-system/prompt-contract.json) for deterministic selection and compilation order.

## Visual identity

Every prompt must preserve these invariants:

- Premium exhibition, art-magazine, and independent-publication layered paper-cut collage.
- Handmade paper sculpture built by folding, cutting, stacking, and masking, not a glossy volumetric 3D scene.
- One core motif as the visual anchor. Reinterpret the source's most identifiable contour, pose, and narrative relation; do not photocopy photographic detail.
- Warm ivory or light paper ground. A limited paper set extracted from the source's most recognizable vivid colors: one primary, one dark structural tone, one light overlay, and one restrained accent.
- Full-color photographic print fragments are allowed only when the source justifies them. They keep natural light, subtle magazine grading, and uncoated fiber, and they sit inside the collage rather than filling a mandatory half of the canvas.
- Matte cardstock, visible paper fiber, clean cut edges, soft contact shadows, natural diffuse light, and readable fold thickness.
- One clear visual metaphor and one focal event.
- Generous negative space, readable hierarchy, and modern editorial restraint.
- No Klein Blue full-canvas field, black-and-white-halftone-as-signature, mandatory 50/50 split, plastic 3D, cheap cardboard, neon, complex gradients, cinematic CGI, scrapbook clutter, unsupported facts, fake branding, unsolicited UI, or watermark.

Ivory `#F4EDE0` with cinnabar `#C23A2B` and ink `#2B2420` is the signature default only when the request gives no palette direction. Other catalog palettes remain equally valid when routed or explicitly selected.

Humans are optional. Choose a human, object, spatial, symbolic, data, mixed-media, or abstract subject mode according to the source and target. Never add a person merely to satisfy a style habit.

## Text rules

- Preserve `exact_text` verbatim when supplied.
- For a text-bearing asset without supplied copy, write one concise Taiwan Traditional Chinese headline grounded in `information`.
- Permit at most one `／` as a non-rendering line-break marker; instruct the generator to render the two lines without the slash.
- With `text_policy: none`, forbid readable text.
- With `text_policy: preserve-reference`, keep all accepted reference text unchanged in content, placement, spelling, and legibility.
- With `text_policy: timed-preserve-reference`, preserve accepted text exactly and describe only the caller-specified timing.
- When extra readable copy is not forbidden, unconstrained stills may add 2 to 4 very small auxiliary groups drawn from object name, place, number, chapter mark, serial, coordinate, direction, status, material term, category label, or one short poetic note. Never invent a year. The main title carries identity and feeling; small type carries order and rhythm. The title may become paper-cut or origami lettering. Small type stays thin, modern, and editorial, and it may lock to paper edges, contours, axes, or negative space.
- If `must_avoid` or the asset specification forbids extra readable copy, render only the accepted headline and add no auxiliary type.
- Never introduce additional readable copy unless the selected text regime allows it.

## Mode compilers

### `text-to-image`

Describe the complete canvas in this order: asset and ratio, source-grounded visual metaphor, composition and focal event, subjects and material treatment, exact typography behavior, palette and lighting, then shared and caller negatives. Do not describe motion or seconds.

### `image-to-image`

Treat supplied references as factual and identity authority. State exactly what must remain unchanged, then transform only the paper-cut treatment, hierarchy, crop, and composition requested by the caller. Do not invent details hidden by or absent from the source.

### `text-to-video`

Describe duration, ratio, initial state, object-specific temporal action, typography timing, locked or explicitly requested camera behavior, final state, and hold. Use the motion catalog. Do not create a separate keyframe prompt.

### `image-to-video`

Treat the supplied image as visual authority. Preserve design, layout, identity, crop, color, material, and accepted text. Describe only the permitted movement of existing non-text groups, camera behavior, duration, and final hold. Do not redesign the frame.

### `layout-or-code`

Write deterministic implementation instructions rather than image-model prose: exact canvas geometry, safe zones, grid, CSS-ready spacing, layer order, typography metrics, colors, paper textures, and any requested animation states or timings.

### `custom`

Honor the caller's generator, medium, dimensions, timing, and delivery constraints. Retain the visual identity and one-prompt-only rule unless a constraint is technically incompatible; disclose any incompatibility rather than silently changing it.

## Internal recipe

The internal recipe records the stable seed, resolved asset specification, selected palette, composition, subject mode, typography, rhythm, imperfections, optional motion profile, factual anchors, visual metaphor, copy policy, extra-copy allowance, and defaults used. Keep it private by default. Include it in structured output only when explicitly requested.

Stable tie-breaking uses the SHA-256 of normalized item information plus the resolved asset specification. Explicit valid overrides always win.

## Quality gate

Before returning a prompt, verify:

1. The asset, generation mode, ratio, duration, and delivery context match the request.
2. There is exactly one prompt and no unused companion prompt.
3. The visual metaphor is understandable and grounded in supplied information.
4. The composition is physically plausible as handmade layered paper-cut and compatible with the target.
5. Text obeys the selected policy, invents no year, and contains no extra readable copy when extra copy is forbidden.
6. Motion language occurs only in video modes; image-to-video preserves the supplied frame.
7. Layout/code prompts use deterministic geometry instead of vague image-model prose.
8. No unresolved placeholders, fake facts, branding, UI, watermark, plastic 3D, neon, cheap cardboard, Klein Blue field, or scrapbook clutter remain.

## Response contract

For one interactive item, return only:

```markdown
**Asset:** Poster · 3:4 · text-to-image

**Generation Prompt**

```text
[the single required asset-generation prompt]
```
```

For structured workflows, return `layered_paper_cut_prompt_package_v1` with ordered items containing `id`, `index`, resolved `asset_spec`, one `generation_prompt`, and QA status. Include `recipe` only when requested.

When an absolute `output_dir` is supplied, create a collision-safe package directory and write:

- `prompt-package.json`
- `prompt-package.md`
- `<index>-<id>/generation-prompt.txt` for every item

Never overwrite an existing package.
