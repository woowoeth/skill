---
name: story-to-manga
description: Convert supplied stories, testimony, folklore, primary-source material, or explanatory text into a source-faithful manga, including production script, continuity-anchored art generation, speech balloons, and deterministic lettering. Use when the user asks to manga-ize, comic-adapt, storyboard, panelize, typeset, or visually dramatize supplied prose, or invokes $story-to-manga.
---

# Story to Manga

Turn supplied prose into a source-faithful manga through one continuous workflow: adaptation, production script, manga name, continuity design, pre-lettering art generation, speech-balloon and lettering composition, and visual QA.

## Delivery contract

The default is **staged full production**: complete planning first, then generate bounded visual units sequentially rather than attempting the entire manga in one generation burst.

- When an image-generation tool is available, continue through actual image generation, deterministic balloon and lettering composition, and return the final lettered images.
- Stop at the manga name, continuity sheets, or prompts only when the user explicitly asks for that narrower deliverable.
- If image generation is unavailable or fails, state the concrete blocker and return the completed blueprint plus executable prompt package. Never imply that images were created when they were not.
- Do not require an extra confirmation between stages unless a missing choice would materially change the work or the environment requires authorization.
- Keep only the current page/panel generation package plus compact continuity anchors active during image generation; do not repeatedly carry the full source ledger and all page prompts when they are not needed.
- Generate and QA one page at a time by default. For dense pages, generate one panel at a time and compose deterministically.

For the detailed generation, reference reuse, lettering, file, and QA procedure, read [references/image-production-workflow.md](references/image-production-workflow.md) before generating images.

## Supported modes

Infer the best mode from the source unless the user specifies one.

- **Horror / kaidan** — emphasize silence, negative space, delayed reveals, page turns, sound, and viewpoint.
- **Firsthand account / essay manga** — preserve the narrator's perspective and uncertainty; favor readable chronology and lived detail.
- **Primary-source / documentary** — prioritize factual fidelity, provenance, dates, places, and explicit separation of reconstruction from recorded fact.
- **Explainer / manual** — prioritize sequence, clarity, visual demonstration, labels, and error prevention.
- **Folklore / urban legend** — preserve variants and attribution; do not collapse rumor, tradition, and verified history into one factual layer.
- **General narrative** — adapt supplied prose into a coherent visual sequence without inventing unsupported plot.

## Required input

At minimum:

- Source text, notes, transcript, or a source-grounded summary.

Useful optional inputs:

- Desired page or panel count
- Reading direction
- Target format: vertical scroll, standard manga page, 4-koma, short comic, and so on
- Audience, tone, visual mood, and dialogue density
- Character appearance references
- Historical period, location, prop, or costume constraints
- Desired delivery scope: full production, sample pages, name only, or prompts only
- Source citations, URLs, dates, or document labels when provenance matters

If critical details are absent, choose conservative defaults and label them as adaptation choices rather than facts.

## Core principles

1. **Source fidelity before drama.** Do not alter supplied meaning merely to make it more cinematic.
2. **Separate fact, recollection, inference, and staging.** A reconstructed panel must not imply that every depicted detail is documented.
3. **Visual economy.** Every panel should advance story, atmosphere, continuity, or explanation.
4. **Continuity by reference, not prose alone.** Lock recurring visual anchors and reuse generated master references throughout production.
5. **Page-turn logic.** Place major reveals and reversals where the page turn strengthens them.
6. **Uncertainty preservation.** Retain qualifications such as “I think,” “apparently,” and “it was said.”
7. **Observable completion.** Prompts and pre-lettering art are intermediate artifacts; checked, fully lettered images are the output of full-production mode.

## Workflow

### 1. Classify the source

Identify the source type, adaptation mode, narrator or viewpoint, temporal order, factual anchors, uncertain or disputed elements, and emotional or explanatory spine. Do not silently resolve contradictions.

### 2. Build a source ledger

List the important source-grounded elements. Use these labels when useful:

- **FACT** — explicitly supported by the supplied source
- **RECOLLECTION** — narrator memory or testimony
- **CLAIM** — attributed assertion
- **INFERENCE** — reasonable but not explicit
- **ADAPTATION** — introduced staging or structure
- **UNKNOWN** — unresolved

Keep this lightweight for casual fiction. Make it explicit for primary-source or documentary material.

### 3. Define adaptation and production constraints

Set the target length, format, reading direction, tone, compression, dialogue policy, visual medium, aspect ratio, color treatment, and source-sensitive constraints. Record which choices came from the user and which are adaptations.

### 4. Create the continuity bible

Assign stable IDs such as `CHAR-01`, `LOC-01`, and `PROP-01`.

For recurring people or entities, lock:

- role and age range if known;
- silhouette, proportions, hair, face anchors, clothing, and distinguishing features;
- carried objects and emotional baseline;
- immutable traits versus page-specific variables.

For important locations, lock layout, entrances and exits, fixed objects, lighting logic, spatial relationships, and period details. Mark invented visual details as **ADAPTATION**.

### 5. Compress into beats

For each beat, identify what changes, what the reader learns, the intended effect, and whether it is indispensable. Remove repetition unless repetition itself matters.

### 6. Allocate pages and panels

For every page, define its purpose, panel count, emphasis, viewpoint, action, text, sound effects, continuity IDs, reconstruction status when relevant, and page-turn function.

Use fewer panels for dread, shock, emotional weight, and complex visual explanation. Use more panels for procedures, fast action, incremental realization, and comic timing.

### 7. Write the production script and lettering plan

Keep text concise and drawable. Never invent quotations and present them as source text, turn paraphrase into quotation, or give historical figures undocumented exact dialogue as fact. Use narration, indirect speech, or an explicit dramatization label when exact wording is unavailable.

Create a production script keyed by page and panel. For every entry, specify scene, action, expression, dialogue, narration, SFX, transition, source status, and continuity IDs.

Create a machine-readable lettering plan with exact text, speaker, panel, reading order, orientation, normalized placement box, balloon shape, and optional tail coordinates. Treat text and balloons as a separate deterministic production layer.

### 8. Build the generation package

Create:

- a global art-direction block;
- compact immutable continuity blocks keyed by ID;
- a character reference-sheet prompt;
- location or prop reference prompts when needed;
- one page prompt per page, or one panel prompt per panel when page-level generation would be too dense;
- negative constraints and reserved lettering zones;
- a generation manifest mapping every output to source beats and continuity IDs.

Do not overload each prompt with the entire source. Put stable information in references and page-specific differences in the individual prompt.

### 9. Stage the production run

Freeze the approved source ledger, continuity bible, beat sheet, and name as the production state. Do not regenerate them for each page. Build a compact per-page handoff containing only the relevant beat, continuity IDs, art direction, reserved lettering zones, and prior-page continuity cues.

### 10. Generate master references

Use the available image-generation tool to create the character sheet first, followed by essential location or prop sheets. Inspect them before page generation. Correct material identity, costume, era, or layout errors now so they do not propagate.

If the user supplied appearance references, use them as references rather than silently redesigning the subject.

### 11. Generate pre-lettering pages or panels

Generate one distinct asset per tool call. Reuse the approved master references on every call; do not use the previous generated page as the sole identity anchor. Generate in story order so the preceding page can be an additional continuity reference when useful.

Generate artwork without dialogue text, captions, SFX, speech balloons, or watermark. Preserve the low-detail zones reserved by the lettering plan. Use page-level generation for simple layouts. Use panel-level generation followed by available deterministic composition when a crowded page or exact panel geometry makes a single generated page unreliable.

### 12. Insert speech balloons and lettering

Read [references/lettering-workflow.md](references/lettering-workflow.md). Use `scripts/letter_manga.py` with the validated lettering plan to place bubbles, captions, and exact vertical or horizontal text over the approved art. Keep the pre-lettering art unchanged and write a separate final file. Do not ask the image model to render exact final dialogue when deterministic composition is available.

### 13. Inspect and repair

Check every output against the production script, name, source ledger, continuity bible, reading order, anatomy, props, environment, balloon ownership, text accuracy, text fit, and safety constraints. Correct the lettering plan for copy or placement errors; regenerate art only for art defects. Do not silently accept a visually polished image that changes a source fact or recurring design.

Finish by returning the fully lettered images in reading order, the production script, and a concise manifest of any unresolved limitations.

## Mode-specific rules

### Horror / kaidan

Prefer anticipatory panels, empty space, off-panel sound, repeated framing with one changed detail, partial forms, and page-turn reveals. Do not insert a visible monster merely because the source is frightening. Preserve ambiguity when the source does.

### Firsthand account

Keep the narrator's knowledge limited to what they could reasonably know at that point. Avoid omniscient panels that convert later inference into contemporaneous fact.

### Primary-source / documentary

Begin with a brief **Adaptation fidelity note**. Mark reconstructed visuals **RECONSTRUCTION** or **ADAPTATION** in planning notes; distinguish documented details from generic period-appropriate fill; preserve dates, named entities, sequence, and attributed claims; never fabricate archival-looking evidence. Show disagreements between sources instead of silently choosing one.

### Explainer / manual

Optimize for successful completion. Show the starting state, action, result, and relevant warning for each step. Dramatic composition must not obscure the procedure.

## Copyright-aware handling

When the source may be copyrighted, adapt through summary, structure, and transformation; avoid reproducing long passages or distinctive dialogue unnecessarily; and do not imitate a living artist's exact style. User-supplied original text may be transformed directly while still avoiding needless verbatim duplication in the planning output.

## Default output

Use this order unless the user asks for something narrower:

1. Adaptation summary and fidelity risks
2. Source ledger
3. Character, location, and prop continuity bible
4. Beat sheet
5. Production script and page-by-page manga name
6. Generation package, lettering plan, and manifest
7. Generated reference sheets
8. Generated pre-lettering pages or panels
9. Fully lettered final pages in reading order
10. QA notes and human-check items

For a quick or blueprint-only request, return only the requested subset and clearly state that image generation was intentionally not run.

## Guardrails

- Do not invent source facts or erase uncertainty for dramatic convenience.
- Do not add supernatural explanations, gore, sexualization, or shock elements not supported by the source or requested treatment.
- Do not change identities, dates, places, causal relationships, or historically meaningful objects without labeling the change.
- Do not generate filler panels.
- Do not claim continuity merely because prompts repeat the same adjectives; use stable IDs and visual references.
- Do not ask the image model to improvise final copy or bubble placement when the lettering script can compose them exactly.
- Do not overwrite pre-lettering art during balloon and text insertion.
- Do not claim a page is final before checking it.
- When factual fidelity and cinematic effect conflict, preserve fidelity and explain the compromise.
