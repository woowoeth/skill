---
name: style-skill-from-refs
description: Turn a folder of reference images into a complete, self-contained image-generation style skill with machine-readable design-system catalogs, a prompt compiler, a validator and evals. Use when the user says 从参考图生成 skill, 把这些图做成风格 skill, 用这些参考图提取设计系统, 做一个风格 skill, build a style skill from these references, extract a design system from images, make a skill out of these reference images, turn this moodboard into a generation grammar.
---

# Build a style skill from reference images

Input: a folder of images, or image paths in the user message. Output: a new skill
directory whose catalogs are the only source of truth for a prompt compiler.

Two finished runs of this procedure, read either one when a decision is unclear:
`examples/wpa-poster-skill` (12 public-domain posters, lettering present) and
`examples/user-refs-skill` (7 user images, unknown provenance, no lettering).

Templates live in `templates/` next to this file.

## Phase 0. Intake

1. Collect image paths from the user message, or list the folder they named.
2. Pick an output directory. Default `./<skill-name>-skill` (or `~/.claude/skills/<skill-name>-skill` if installing globally), ask if unsure.
3. Copy each image to `<out>/references/ref-NN.<ext>`, numbered from 01, extension
   unchanged. Never edit, crop or recompress.
4. Record provenance per batch: public domain with a source URL, user-owned, or
   unknown. Ask once if the user did not say.
5. Public domain: write `references/SOURCES.md` plus `references/sources.json` with
   title, creator, date, item URL and the per-item rights statement.
6. Unknown or user-owned: no SOURCES.md. The generated skill must say `references/`
   is not redistributable and that the user has to confirm rights before sharing.
   Do not guess an origin, do not name a probable artist.

## Phase 1. Look

Read every image with the Read tool. No skimming, no sampling.

1. Name the shared visual language in one paragraph: what every image does the same.
2. Choose a kebab-case skill name from the mechanism, not from a movement label.
   `ultramarine-dither-engraving` works. `retro-vibes` does not.
3. Flag outliers, the images that break the shared language. Record which and why.
   They stay in the catalogs, they just never become defaults.
4. Record `protected_elements` per image: identifiable faces, logos, watermarks,
   traced existing artwork, photographed sculpture, legible brand text. Anything
   listed here becomes a hard avoid in the generated skill.

## Phase 2. Annotate

Write `<out>/design-system/reference-analysis.json`, one object per image.
Shape: `templates/reference-analysis.schema.json`.

Each object carries five arrays of 3 to 5 phrases: `typography`, `colors`, `layout`,
`style`, `signature_moves`. Plus approximate hex per ink, ink or hue count, visible
text language, `protected_elements`.

Quality bar. Every phrase has to be executable by an image model that never saw the
picture. Concrete geometry, percents, counts, hex.

Good:
- "headline occupies the top 9 percent of the sheet, letters touch both side margins"
- "long straight rays escape the disc and bleed off all four edges"
- "skin built from two warm inks only, one hard edge between lit and shadow planes"

Bad:
- "bold retro typography" (adjective, not observation)
- "striking composition" (says nothing about geometry)
- "nostalgic warm palette" (no hex, no count)

Mark every hex `approximate: true`. Scans and screenshots carry colour shift, so the
hex is a target zone, not a measured ink.

## Phase 3. Merge

Build the catalogs. Shapes and one filled example each in `templates/catalog-shapes.md`.

Always: `colors.json`, `typography.json`, `compositions.json`.
Plus one material catalog named for the medium: `imperfections.json` for print,
`texture.json` for surface or raster work, `lighting.json` for rendered work.

Rules:

1. Every entry carries a non-empty `refs` array of reference ids.
2. Merge near-duplicates. Two layouts differing only in headline position become one
   pattern with `variants: [A, B]`, refs unioned. Two inks within perceptual spitting
   distance become one ink whose refs list both.
3. A role the references never show still goes in the catalog if the layouts leave
   room for it, marked `observed_in_refs: false`. The user-refs example does this for
   all typography: zero of its 7 images contain lettering.
4. Caps: 6 to 9 composition patterns, 4 to 7 type roles. Over the cap means merge
   harder. Under it means the reference set is thin, say so in the report.
5. Numeric ranges as `[low, high]` arrays, both bounds observed, never invented.
6. Each catalog gets a `defaults` block so the compiler can run with no user input.

## Phase 4. Write the generated SKILL.md

Fill `templates/SKILL.template.md`. Placeholder list sits at the top of that file.
Fixed sections, in order:

1. Frontmatter: name, description with both Chinese and English trigger phrases.
2. When to trigger, plus what not to trigger for.
3. The catalogs-are-truth rule: read all catalogs, pick exactly one id per dimension,
   never invent an id, never blend two, name any substitution.
4. The recipe block, yaml, one line per dimension.
5. Prompt compiler, five paragraphs in fixed order: canvas and inks; composition;
   subject; typography and exact wording; material and hard avoids.
6. Hard avoids, derived from what the references never do, plus one clause forbidding
   every recorded `protected_elements`.
7. Originality firewall: change at least four dimensions against any single reference.
8. Attribution, matching the Phase 0 provenance verdict.
9. Output format: image if the host can generate one, compiled prompt in a fenced
   block, recipe block, one line naming the four changed dimensions.
10. Five example triggers with resolved recipes, at least two in Chinese.

Writing constraints for everything you generate:

- No "in the style of" any named designer, studio, brand or living artist.
- Fonts by category and mechanics (heavy geometric sans, flat terminals, squeezed
  counters), never by commercial name.
- No invented history, no invented provenance, no invented movement names.
- Model-agnostic prompt wording. No tool-specific flags or weights.

## Phase 5. Validate

1. Copy `templates/validate_design_system.py` to `<out>/scripts/`. It discovers
   catalog names itself, so adapt only the closing summary lines if you renamed
   anything.
2. Run `python scripts/validate_design_system.py`. Exit 0 is required. Fix the
   catalogs, never the validator, unless the validator is wrong about the shape.
3. Write `<out>/evals/evals.json`, 6 prompts spanning: a Chinese request, an English
   request, a text-free request, a request naming something the catalogs do not cover
   (tests substitution), an outlier-adjacent request, a request that asks to copy a
   reference (must be refused by the firewall).
4. Write `<out>/README.md` from `templates/README.template.md`, Chinese first, then
   English, with the provenance and license note.

## Phase 6. Report

Report to the user, in this order:

1. Theme in one sentence and why that grouping.
2. Outliers, with the reason.
3. Protected elements found, and how the generated skill blocks them.
4. File table with line or entry counts.
5. Validator output, verbatim.
6. One compiled prompt, in a fenced block, pasteable into an image model right now.

## Delegation

Model routing guidelines:

1. Phase 2 annotation: one capable vision subagent (e.g. Claude 3.7 Sonnet / Opus) per 4 to 6 images, run in parallel. Each gets the image paths, `templates/reference-analysis.schema.json`, and the concrete geometric quality bar above.
2. Phase 3 merge: high-reasoning model (Opus / Sonnet / Pro). It needs all annotations in one context to deduplicate and establish global design system ranges.
3. Quality check: Never let the agent that wrote the catalogs judge them. A second model re-reads 3 randomly chosen reference images against their annotation objects and reports each phrase as matching, wrong or unverifiable.
4. Phase 5 validation is mechanical. Exit code decides, not an opinion.
5. Every subagent call should specify the model explicitly.
