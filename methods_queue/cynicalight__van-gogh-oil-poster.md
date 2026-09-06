---
name: van-gogh-oil-poster
description: Generate or analyze vertical art posters built from a visibly unpainted canvas or art-paper support and one coherent Van Gogh-inspired oil-painted event occupying about one third or two thirds of the surface according to the user's theme and input. Use when the user supplies a theme, sentence, article, mood, subject, photograph, artwork reference, or image folder and wants final poster images saved under the current working directory's art folder, an evidence-derived selection from six defined Van Gogh color palettes, reusable style rules, or a varied poster series with materially visible negative space.
---

# Van Gogh Oil Poster

Turn content into a new poster composition rather than a reproduction of an existing painting. Keep the production prompt internal. Save every generated raster under the invocation working directory's `art/` folder and return the image plus its saved path without exposing the prompt.

## Route the request

Choose the smallest mode that fulfills the request.

- **Generate — default:** theme, phrase, article, subject, or mood → input evidence → substrate → metaphor and anchor → spatial and color candidates → joint selection → prompt → image → inspection.
- **Photo Input — Generate subflow:** a supplied photograph must affect the poster → classify its role and preservation level → include the actual image in generation → inspect both recognition and poster quality.
- **Reference Analysis:** inspect supplied art or posters → separate observed traits, reusable rules, variables, and source residue → return a source-safe style system without exposing an image-generation prompt. Generate only when requested.
- **Analyze + Generate:** analyze references first, then build a new composition through Generate without copying the reference subject, wording, signature, or exact layout.
- **Batch:** generate several posters in one family while varying substrate, footprint, anchor, directional field, and typography according to `references/variation-engine.md`.

Treat a request to “做一张” as Generate. Make safe visual choices instead of asking the user to select among options already covered by this skill.

## Load the relevant references

- Read `references/style-system.md`, `references/substrate-system.md`, and `references/palette-system.md` for every mode.
- Read `references/prompt-compiler.md` for every generation request. Treat its compiled prompt as private working material.
- Read `references/variation-engine.md` before selecting a single recipe or planning a batch.
- Read `references/reference-analysis.md` whenever images or folders are supplied for analysis.
- Read `references/quality-gate.md` before returning a generated image or analysis.

## Bind the output directory

- At the start of the request, resolve and record the absolute invocation working directory before reading Skill files or using a different tool workdir. Call it `invocation_root`.
- Set `art_dir` to the absolute path `<invocation_root>/art` and create it before generation. The Skill installation directory is never the output directory unless the user invoked the Skill from there.
- If `art` already exists as a non-directory, or resolves through a symlink outside `invocation_root`, stop and report the unsafe output-path conflict instead of writing elsewhere.
- Use a filesystem-safe descriptive filename such as `van-gogh-<theme-slug>-<timestamp>.png`. Preserve the actual raster extension when the generator returns another format.
- Never overwrite an existing image. Add a timestamp or numeric suffix when necessary.
- After generation and inspection, save or copy the final selected raster into `art_dir`. Resolve its absolute path and verify that it exists and is a regular non-empty file.
- For a batch, save every accepted image separately in the same `art_dir` and verify the complete expected file count.
- Treat generation as incomplete when the raster exists only in a temporary location, remote result, or conversation preview. Persist it into `art_dir` before returning.
- If the image tool does not expose a persistable raster, report that limitation. Never claim the image was saved without verifying the local file.

## Respect source and artwork boundaries

- Inspect actual supplied images before making claims about dimensions, ratios, color, layout, texture, identity, or visible text.
- Separate observation from interpretation. Use file metadata for exact dimensions and call visual percentages estimates unless measured.
- Learn visual grammar from existing artworks. Do not reproduce an exact Van Gogh composition, named painting, signature, museum label, crack pattern, frame, watermark, or provenance cue unless the user is explicitly asking to edit a supplied image and the request is otherwise permitted.
- Keep the new scene, subject arrangement, paint boundary, and typography original even when a named work supplies the palette or motion vocabulary.
- Use user-supplied poster text when requested. Keep image-model text short. Never invent a Van Gogh signature.
- State limitations rather than inventing details when files are missing, unreadable, or unavailable to the generation tool.

## Classify supplied images

Assign one role to every supplied image before compiling the prompt.

- **Edit target:** the photograph or recognizable subject must appear in the new poster.
- **Reference image:** use only its palette, composition grammar, substrate, brush behavior, or mood.
- **Supporting insert:** preserve one specified person, object, texture, or fragment inside a new painted event.

Infer the role from wording. “把这张照片做成海报” means edit target. “参考配色、笔触或构图” means reference image. “把照片里的这个人或物放进去” means supporting insert. A photograph supplied with only “做一张” defaults to edit target.

Record a preservation level.

- **High:** preserve identity, facial structure, body proportions, pose when relevant, defining markings, product geometry, silhouette, and object count. Translate large color fields into the required selected A-F palette; preserve recognition-critical colors only as restrained off-palette accents inside the 10% cap.
- **Medium:** preserve the main subject and defining characteristics while allowing crop, pose simplification, required A-F palette translation, brush abstraction, scale, and surroundings to change.
- **Low:** preserve only requested visual traits; do not preserve the source subject or composition.

Use High for identifiable people, pets, products, characters, and artworks unless the user explicitly permits reinterpretation. When oil-paint abstraction conflicts with recognition, preserve the subject first and report any remaining limitation.

Include every image meant to affect the output in the image-generation call. Use local referenced paths when every target has a local file path. Otherwise include the smallest number of recent conversation images that contains every target, up to five. Never mix both inclusion mechanisms. Ask for reattachment only when no available mechanism can include all required targets.

## Generate workflow

1. **Parse the content.** Identify the core subject, emotional temperature, exact supplied text, intended audience, requested ratio, and every input-image role. Reduce an article or abstract idea to one central imageable relation.
2. **Build the input evidence sheet.** Before choosing substrate, composition, color, or support annotations, record explicit constraints, image roles, required invariants, subject silhouette, pose, gaze or facing, implied motion, spatial verbs, emotional verb and intensity, time, season, light, source color relationships, supplied or inferred short title, and any source composition that must not be copied. Mark each item as explicit, observed, or inferred. Do not invent image evidence when no image was supplied.
3. **Choose the substrate.** Select one support from `references/substrate-system.md` using the input evidence. Record its base tone, weave or fiber, absorbency, ground, wear, and interaction with paint. Treat blank support as a visible material, never as digital white.
4. **Choose the visual metaphor and anchor.** Translate the content into one subject, relation, or compact scene. Derive one stable dominant form from the content rather than defaulting to a recurring object menu. Record the anchor's geometry, orientation, and required breathing room.
5. **Choose the attention geometry.** Follow `references/variation-engine.md`. Treat sparse-event and expanded-event as equally valid: about one-third paint with two-thirds exposed support, or about two-thirds paint with one-third exposed support. Honor an explicit painted or blank share first. Otherwise compare both modes using subject scale, recognition needs, narrative density, emotional pressure, environmental importance, and the need for material silence. Record the selected mode and evidence; never use a fixed coverage default.
6. **Derive spatial candidates.** Keep coverage mode, footprint family, placement, advance vector, and anchor position as separate decisions. Create two or three viable internal candidates from the input evidence, compare their semantic fit, subject geometry, continuous negative space, source preservation, and visual tension, then select the strongest. Never use lower-right or any other quadrant as an unstated default. Use recent-output diversity only as a tiebreaker.
7. **Select one primary palette.** Follow `references/palette-system.md`. Every poster must use exactly one of the six defined palettes A-F as at least 90% of the finished oil-painted chromatic area. Honor an explicitly named A-F palette first; otherwise select from input evidence, theme, emotion, season, and light. Map large source-image color fields into that palette. Allow at most 10% total off-palette accents for explicit thematic or identity-critical details, list every accent and role, and never hybridize two palettes.
8. **Build the required working layer.** Follow `references/style-system.md` and `references/variation-engine.md`. Every generated poster must include both one short charcoal-handwritten English theme phrase and a visible set of graphite layout lines on the exposed support. Treat both as active oil-painting drafts rather than finished typography or decorative marks. Use the user's exact English wording when supplied; otherwise infer 1–5 natural English words and record them as inferred. Make the handwriting visibly irregular and provisional. Map the pencil centerline, horizon, directional diagonals, perspective rays, proportion ticks, enclosing shapes, or value divisions to the actual composition. Optionally add umber or ultramarine underdrawing and one or two artist masking-tape fragments. Keep the working layer subordinate while making it clearly present; do not reduce it to token lines or fill space with unrelated doodles.
9. **Resolve attention, composition, palette, and annotations together.** Check that the selected coverage gives the subject enough scale while preserving one meaningful continuous support field, that the selected A-F palette remains at least 90% dominant, and that the anchor, highest contrast, thickest focal impasto, focal color, construction lines, and title placement support the same visual hierarchy. Adjust coverage, location, palette emphasis, accent use, or annotation density when they compete. Do not bind a palette to a habitual coverage mode, footprint, or quadrant.
10. **Map directional energy.** Give every painted zone one or two dominant stroke directions. Use structural strokes for the subject, flow strokes for atmosphere, particle strokes for rough matter, wrapping strokes at active contours, and rhythmic strokes for repeated elements.
11. **Compile the prompt.** Follow the ordered six-paragraph contract in `references/prompt-compiler.md`. Include the evidence-derived coverage mode, placement, advance vector, selected A-F palette, locked color roles and ratios, off-palette accents, exact substrate behavior, attention geometry, original motif, anchor, stroke map, impasto topology, painted-edge anatomy, the required charcoal draft phrase, graphite layout, optional secondary typography, reproduction, and a short relevant avoid list.
12. **Generate the raster.** Use built-in image generation. Pass the actual source image for Photo Input. Keep the compiled generation prompt internal and never include it in the final response.
13. **Inspect the result twice.** Inspect the whole poster at thumbnail scale for the selected 1:2 or 2:1 paint-to-support relationship, evidence-derived placement, anchor, palette, support annotations, and composition. Inspect at full size for support texture, plausible construction media, tape fibers and adhesion, directional strokes, broken-color adjacency, impasto ridges, and edge behavior. Also compare source invariants for Photo Input.
14. **Regenerate once when central constraints fail.** Tighten the failed measurable constraint instead of adding vague adjectives. Prioritize source preservation when applicable, then selected attention geometry, substrate legibility, evidence-derived placement and palette, anchor, support-annotation restraint, directional strokes, and impasto.
15. **Persist and return the artifact.** Save the accepted raster in the previously bound `art_dir`, verify the file, then provide the image, absolute saved path, recipe, selected substrate, attention geometry and reason, selected A-F palette, palette share, off-palette accents and shares, one-sentence color reason, selected support annotations, one short interpretation, and any preservation limitation. Do not quote, summarize, reveal, or paste the internal generation prompt.

## Keep the style identity stable

- Choose one evidence-derived attention geometry: sparse-event uses 62%–72% exposed support and 28%–38% paint, targeting 66% support and 34% paint; expanded-event reverses those ranges, targeting 34% support and 66% paint.
- Keep one continuous, materially legible support field in either mode. The connected painted event must dominate its allocated share, and any detached flecks stay inside that total and use at most about 2% of the canvas.
- The exposed-support share measures surface without finished oil-paint coverage. Restrained pencil, charcoal, monochrome underdrawing, handwritten title, or masking tape may appear within it without reclassifying it as painted coverage, provided the support remains visually dominant there.
- Keep one stable anchor inside the painted event and let the remaining strokes carry motion.
- Build color by adjacent strokes and broken color rather than smooth digital gradients.
- Make bright ridges and selected focal strokes thicker than shadows. Preserve low valleys where support tooth can breathe through.
- Make the boundary read as a finished painting erupting across blank support, with dense interior paint, dragged bristle transition, and sparse terminal flecks. Do not depict a bucket spill, liquid puddle, or random action-painting splatter.
- Include exactly one short charcoal-handwritten English theme phrase and a visible graphite composition draft as required working layers. Keep all additional typography optional, sparse, and subordinate.
- Preserve a flat art-object view with diffuse raking light. Avoid a framed-wall mockup, desk scene, gallery interior, or glossy product render.

## Variation discipline

- Change visual grammar across adjacent outputs, not only coordinates. Vary at least paint footprint, placement or advance vector, anchor structure, and directional field when the input permits it.
- Preserve family resemblance through visible support, a deliberate 1:2 or 2:1 paint-to-support relationship, exactly one dominant A-F palette, directed impasto, irregular painted boundary, and one strong anchor.
- For a batch of four or more, use at least three footprint families and at least two substrates. Do not repeat the same substrate + footprint + anchor combination on adjacent posters.
- Use exactly one defined A-F palette per poster. Across a batch, select palettes from each poster's evidence; repeat one only when the themes support it. Keep all off-palette accents within the per-poster 10% cap.
- Remove secondary text and decorative flecks before weakening the anchor, paint geometry, or directional brush system.

## Output formats

### Generate

````markdown
**生成图**

![Van Gogh Oil Poster](absolute-path-inside-current-directory-art-folder)

**配方**

- Mode: Generate
- Saved to: [absolute path inside invocation_root/art]
- Substrate: [support / tone / tooth]
- Color: [origin / selected A-F palette / palette share / off-palette accents and shares / why]
- Recipe: [coverage mode and reason / footprint / placement / advance vector / anchor position and breathing room / metaphor / direction field / support annotations / typography / finish]
- Photo role and preservation: [omit when no image was supplied]
- Note: [one short interpretation and any regeneration or limitation]
````

### Reference Analysis

Return the structure defined in `references/reference-analysis.md`: style name, concise summary, inspected evidence, fixed system, variable system, source residue, A-F palette mapping, evidence-derived variation block, avoid list, confidence, and limitations. Never expose the internal generation prompt.

## Non-negotiable outcome

A successful result keeps the tactile unpainted art support materially legible while one coherent Van Gogh-inspired oil-painted event occupies the evidence-derived one-third or two-thirds share. It must feel deliberately composed, materially convincing, emotionally colored, and newly authored rather than filtered, unintentionally full-bleed, randomly splattered, or copied from a known painting.

## Example requests

- “用 $van-gogh-oil-poster 做一张关于失眠海岸的海报，文字尽量少。”
- “把这篇关于告别的文章提炼成一个意象，自动选最合适的纸张和六套配色之一，然后出图。”
- “用 Palette C，把麦田式焦虑改写成城市通勤主题，保留约三分之二空白画布。”
- “参考这组画的笔触和色彩关系，先分析，再做一张全新构图，不复制任何原作。”
- “把这张人物照片做成局部厚涂海报，脸仍然要一眼认得出来。”
