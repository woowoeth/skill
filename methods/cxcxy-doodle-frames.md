---
name: make-progressive-doodle-illustrations
description: "Turn one user-provided copy block into original white-paper black-bean doodle illustration sets at the requested or context-appropriate aspect ratio with built-in $imagegen: automatically split the copy into scenes and generate exactly three cumulative full-canvas PNG states per scene, where each later image adds one knowledge module without moving or repainting earlier ink. Use for 白底手绘、小黑插画、三帧累加架构图、清单/工具/步骤配图、参考图风格迁移，or whenever the user invokes $make-progressive-doodle-illustrations. If the user supplies only copy, treat that as complete input and infer the aspect ratio from the destination, project, reference, or copy structure rather than fixing one ratio. This skill produces illustration assets only, not video, animation, audio, captions, or publishing copy."
---

# Make Progressive Doodle Illustrations

Create project-ready illustration sets that look like one white sheet being completed in three steps. Use built-in `$imagegen` for generation and editing; keep all earlier ink fixed.

## Minimal input contract

The only required user input is the source copy.

When the user invokes this Skill with copy and no other production details:

- treat the request as complete and begin work;
- split the copy into coherent scenes in its original semantic order;
- use a pure-white full canvas at the selected aspect ratio and the fixed black-bean doodle style;
- generate exactly three complete white-paper cumulative images for every scene;
- keep every earlier pixel fixed; stage 2 and stage 3 each add exactly one knowledge module;
- infer the scene count from the copy instead of asking the user;
- do not ask for a separate topic, style, character design, image count, or cumulative-frame rule.

Select the aspect ratio in this order: explicit current-turn request, target project or platform, supplied reference, then the copy's visual structure. Use a wide canvas for horizontal processes or side-by-side comparisons, a portrait canvas for stacked steps or list narratives, and a square canvas for one centered concept. Do not pause for confirmation when a reasonable semantic split and aspect-ratio inference are possible. Ask only when the supplied copy itself is missing, contradictory, factually unsafe to visualize, or multiple known destinations require incompatible canvases. An explicit current-turn user override takes precedence; silence never changes the other defaults.

## Read before generation

1. Read `references/state-and-style.md` for the visual and cumulative-pixel contract.
2. Read `references/prompt-recipes.md` before the first `$imagegen` call.
3. Read `references/qa-checklist.md` before selecting or delivering assets.
4. Load the installed `imagegen` Skill and follow its built-in-first save-path rules.

## Scope

Produce only:

- one `character-anchor.png`;
- exactly three full-canvas cumulative PNGs per scene;
- an illustration plan;
- a prompt ledger;
- optional contact sheets and validation output.

Do not create HyperFrames, GSAP, video, audio, captions, voice, publishing copy, or MP4.

## Defaults

- Canvas: pure white; aspect ratio and dimensions follow the explicit request, target project/platform, supplied reference, or the copy's visual structure.
- Ink: imperfect rounded near-black marker line.
- Accents: pale blue `#B2DFF1` and orange `#F4951B`, used sparingly.
- Mascot: original black bean-shaped body, round white glasses/eyes, small friendly mouth, two arms, two legs.
- Composition: 75–90% white space; reserve the bottom 17% when the images may later be used with captions.
- Character treatment: free-standing and acting on the diagram; do not put it in a decorative circle, badge, sticker, or frame unless containment has meaning.

## Workflow

### 1. Convert content into an illustration plan

- Preserve supplied wording and facts.
- Treat one pasted copy block as the complete brief.
- Resolve one canvas aspect ratio and pixel size before generation; keep them identical across all three states in the same deliverable set.
- Split at semantic turns: one scene per independent claim, step, comparison, or result; keep short dependent clauses together.
- Preserve source order and do not invent bridge claims.
- Split each scene into exactly three drawable beats:
  1. `hero`: person, subject, or problem;
  2. `mechanism`: add one process, evidence, path, or comparison;
  3. `result`: add one output, decision, or synthesis.
- Assign one dominant metaphor to each beat.
- Reject filler decoration. Every new object must explain a clause.
- Record scene IDs, three visual additions, filenames, and prompt IDs in `illustration-plan.json` or the user's requested format.
- Proceed directly from the plan to generation unless the user explicitly requests a plan-only gate.

### 2. Generate the character anchor

- Call built-in `$imagegen` once for a neutral full-body anchor.
- Keep one character, both arms, both legs, clear glasses/eyes, generous padding, no text, logo, watermark, scenery, shadow, or gradient.
- Save the selected anchor into the project before referencing it.
- Inspect it with `view_image`.

### 3. Generate each three-state scene

- Use one built-in image-generation call per state or variant.
- Label image roles explicitly:
  - Image 1: character identity reference;
  - Image 2: previous cumulative state, when editing;
  - optional Image 3: composition or prop reference.
- Create full white-background images at the selected canvas dimensions, never cropped fragments.
- Stage 1 introduces only the hero.
- Stage 2 keeps stage 1 unchanged and adds exactly one module.
- Stage 3 keeps stage 2 unchanged and adds exactly one result/synthesis module.
- Render exact Chinese text, product names, numbers, and factual labels outside raster generation whenever possible. If the user only wants illustrations, leave clean space for later editable text.

### 4. Handle identity or layout drift

- Inspect every generated state before continuing.
- If an edit repaints earlier lines, changes the character, or shifts the layout, reject it.
- Retry once with a single-change invariant from `references/prompt-recipes.md`.
- If drift persists, generate one approved complete master and derive earlier states locally by extracting whole semantic clusters. Offline masks may build assets, but each delivered state must still be a complete white canvas.
- Never accept “close enough” character or coordinate drift across cumulative states.

### 5. Validate

Store scene images with this naming scheme:

```text
media/generated/three-stage/
  hook-stage-01.png
  hook-stage-02.png
  hook-stage-03.png
  item-01-stage-01.png
  item-01-stage-02.png
  item-01-stage-03.png
```

Run:

```bash
python3 <SKILL_DIR>/scripts/validate_cumulative_frames.py \
  <PROJECT_DIR>/media/generated/three-stage
```

Require zero changed existing-ink pixels unless the user explicitly accepts and documents a tolerance. Fix missing stages, size mismatch, or insufficient new ink.

### 6. Deliver

- Save all selected assets inside the project; never leave project-referenced files only under `$CODEX_HOME/generated_images`.
- Save final prompts and image roles in `imagegen-prompts.md`.
- Report rejected variants and remaining uncertainty.
- Provide absolute paths to the anchor, all three-state scene sets, plan, prompt ledger, contact sheet if created, and validator result.

## Originality and safety

- Transfer only abstract line quality, palette, white space, and cumulative storytelling from references.
- Do not copy an artist's exact frame, mascot, logo, signature, or creator identity.
- Do not invent product interfaces, reviews, claims, data, endorsements, or outcomes.
- Preserve user-provided evidence without redrawing it into misleading proof.
