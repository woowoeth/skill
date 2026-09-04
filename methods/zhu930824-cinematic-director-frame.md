---
name: cinematic-director-frame
description: Generate a single exact 2.35:1 cinematic film frame with strongly expressed auteur visual grammar, director-specific lens and focus behavior, immediately recognizable color signatures, precise production design, and rich composition geometry. Supports 24 director grammars and scene-conditioned focal lengths from 18mm to 180mm. Use when the user asks for a movie still, film frame, cinematic keyframe, director-inspired shot, storyboard-quality image, or wants distinctive camera, optics, lighting, palette, blocking, texture, material detail, symmetry, golden-ratio, layered depth, frame-within-frame, or other director-compatible visual choices.
---

# Cinematic Director Frame

Turn the user's idea into:

1. one generated cinematic frame;
2. the final generation prompt;
3. a concise shot card with director translation, lens, camera, light, palette, and framing.

## Mode Policy

Use **Frame Mode + Strong Translation** by default. Set director-language strength to **85/100** unless the user asks for subtle, stronger, or maximal treatment. Generate one image unless the user requests variants or prompt-only output. Always design for a native 2.35:1 composition, never a generic landscape with decorative black bars.

Use the built-in image generation capability by default. When the generated file is not exactly 2.35:1 and a local file is available, run `scripts/crop_to_scope.py` to create the final exact-ratio image. Preserve the subject with the script's focal anchor options.

## Director Translation Policy

Treat a named director as a request for cinematic grammar, not literal imitation.

- Read `references/director-grammars.md` when the user names a director or asks for auteur selection.
- Translate the director into observable traits: framing, camera height, lens range, movement, blocking, light, palette, texture, pacing, and production design.
- Do not put the name of a living director in the final image-generation prompt. Use the translated traits only. This keeps the result original and gives the model clearer visual instructions.
- Prefer translation for all directors, including deceased filmmakers, because concrete visual language is more controllable than a name.
- Never recreate a recognizable frame, character, actor likeness, costume, or set from an existing film unless the user supplies it and explicitly requests an edit or transformation.
- If the user combines directors, assign one primary grammar and at most one secondary influence. State what each controls.
- If the director is absent from the reference, infer a compact grammar from reliable knowledge. If uncertain or if the user asks for research-backed accuracy, browse authoritative interviews, cinematographer notes, camera/lens documentation, or primary production sources before generating.

## Director Signature Amplifier

Prevent the result from collapsing into generic “cinematic” imagery. Before writing the prompt, extract a **Director DNA bundle** containing exactly one dominant choice from each axis:

1. composition and blocking;
2. camera position, focal length, and movement;
3. motivated lighting structure;
4. palette and capture texture;
5. production design, material, and wardrobe;
6. temporal behavior, shutter character, and movement rhythm;
7. emotional distance and performance behavior.

Treat all seven as non-negotiable visual invariants. In Strong Translation:

- Make at least five axes immediately visible in the raster, not merely mentioned in the prompt.
- Let the director grammar control the entire frame geometry, not just grading or grain.
- Use the director profile's **Strong signature lock** as the default bundle when it fits the scene.
- Repeat the most important composition/camera trait in paragraph 2 or 3 and the light/texture trait in paragraph 4. Do not repeat the director's name.
- Prefer a bold, coherent interpretation over mixing safe conventions from unrelated cinema.
- Keep originality boundaries intact at every strength. Stronger means clearer formal decisions, not copying a known frame.

Map user language to strength as follows:

- subtle / lightly inspired: 40/100, three visible axes;
- default: 85/100, at least five visible axes;
- strong / unmistakable: 90/100, all seven axes visible with four dominant;
- maximal: 100/100, all seven axes visible plus one controlled exaggeration selected from lens proximity, negative-space scale, color-field dominance, camera rigidity, temporal smear, or production-design repetition. Exaggerate only one lever and remain original.

At 90 or 100, read `references/style-amplification.md`. Do not make every lever louder. Preserve the director's own restraint: stronger minimalism means stricter subtraction, not more decoration.

## Composition Geometry Engine

Make every frame intentionally composed, not merely well lit. Read `references/composition-geometry.md` for every generation, then choose exactly one **primary geometry** and optionally one **supporting geometry**.

- Let the director grammar choose the geometry. Do not force rule-of-thirds or a golden spiral onto directors whose signature depends on symmetry, frontal balance, rigid architecture, or deliberate imbalance.
- Assign a primary focal anchor, a secondary narrative anchor, an eye path, and a controlled negative-space region before writing the prompt.
- Place faces, hands, decisive objects, horizon lines, doorframes, vanishing points, and practical lights on meaningful nodes or paths from the selected geometry.
- Make the geometry visible through blocking, architecture, light, and depth. Never draw or mention visible grids, guide lines, or spirals in the image.
- Compose for the final 2.35:1 crop. Keep critical anchors inside the crop-safe region and re-check the geometry after cropping.
- Reject technically correct but visually accidental arrangements: centered subjects without purpose, arbitrary headroom, tangencies through faces, clipped hands, competing focal points, dead empty space, and foreground objects that do not guide the eye.
- Prefer one strong organizing principle over combining multiple formulas.

## Precision Shot Blueprint

Before prompting, create an internal blueprint with measurable choices. Read `references/production-design-and-texture.md` for material and detail control.

- Declare subject coordinates using normalized x/y positions, subject scale as a percentage of frame height, horizon height, vanishing-point position, and crop-safe margins.
- Assign foreground, midground, and background a distinct job: guide, action, consequence, concealment, scale, or atmosphere.
- Limit story-bearing detail to one hero action, one secondary clue, and up to three supporting material details.
- Specify architecture, surface finish, wardrobe fabric, hero prop, atmospheric medium, and age/wear. Make every detail belong to the same place, era, climate, and social reality.
- Distinguish clean, worn, damp, dusty, lacquered, oxidized, sun-bleached, smoke-stained, or hand-painted surfaces. Avoid the generic phrase “detailed environment.”
- State what must remain visually quiet. Precision requires controlled absence as well as added detail.

## Director Color Signature Engine

Make the director's color language recognizable at thumbnail size. Always read `references/director-color-signatures.md` when a director is named or selected.

- Set color-signature strength to **85/100** by default. Use 90/100 for strong director translation and 100/100 for maximal translation. Reduce it only when the user explicitly asks for muted, neutral, documentary, or monochrome output.
- Choose one dominant color family, one supporting family, one small accent, a neutral base, and an exposure/contrast behavior from the selected profile.
- Carry the palette through set surfaces, wardrobe, motivated light, practical fixtures, props, shadows, and capture response. Do not rely on a global color filter alone.
- Make the palette visible across meaningful frame areas. Do not reduce the signature hue to a tiny prop unless the director profile specifically depends on restrained accents.
- Preserve believable skin and motivated sources. Strong color means coherent hue relationships and distribution, not indiscriminate saturation.
- Let the director decide whether recognizability comes from saturation, pastel color blocks, near-monochrome fields, mixed color temperatures, or controlled primary accents.
- Use color to reinforce composition: place the highest chroma or strongest warm/cool contrast at the primary anchor, then echo a weaker related hue at the secondary anchor.
- Avoid generic orange-and-teal grading unless it is explicitly part of the selected profile and scene.
- Regenerate once if the image looks generically cinematic, washed out, colorless, dominated by an unrelated palette, or if the signature exists only as post-production tint.

## Reference Frame Gallery

Read `references/reference-gallery.md` when the user asks to compare directors, inspect available visual languages, or diagnose a weak translation. The matching images live in `assets/reference-frames/`.

- Treat each frame as an original visual benchmark for geometry, palette distribution, lighting, and focal hierarchy—not as a composition to copy.
- Never pass a gallery image into image generation by default. Use the written grammar and color recipe first.
- If the user explicitly asks to use a gallery image as a reference, preserve the new scene and characters while varying blocking, architecture, props, and narrative instant.
- Keep new results original and reject outputs that reproduce the gallery frame too closely.

## Frame Prompt Compiler

Compile only details that become pixels. Answer these questions in order.

1. **Narrative instant** — What irreversible or emotionally charged instant is visible? Choose one action, glance, pause, or spatial relation; do not summarize a whole plot.
2. **Frame geometry** — Declare a native 2.35:1 cinematic frame, the selected composition geometry, subject scale, horizon, foreground/midground/background, primary and secondary focal anchors, negative space, and the visual path through the frame.
3. **Blocking** — Place each person or object precisely. Limit the frame to one primary subject relationship and a few story-bearing details.
4. **Camera position** — Specify camera height, distance, angle, symmetry/asymmetry, and static/handheld/dolly/locked-off behavior.
5. **Lens and focus** — Use one full-frame-equivalent focal length informed by the selected grammar. State deep, moderate, or shallow focus and why it serves the moment. Do not list multiple focal lengths in one frame.
6. **Lighting** — Identify motivated sources, direction, softness, contrast ratio, exposure bias, practical lights, weather, and time of day.
7. **Color and material** — Choose the director profile's dominant family, supporting family, accent, neutral base, approximate distribution, skin-tone behavior, exposure logic, surface texture, wardrobe, and production-design carriers.
8. **Capture character** — Specify photochemical or digital behavior: grain, halation, highlight roll-off, diffusion, shutter character, gate weave, or clean restraint. Use only effects that match the grammar.
9. **Originality boundary** — Keep the scene original. Exclude film titles, director names, actor likenesses, franchise imagery, logos, subtitles, letterbox bars, watermarks, and promotional-poster typography.

## Lens, Optics, and Focus Engine

Always read `references/lens-optics-and-focus.md` for a named or selected director. Express focal lengths as **full-frame equivalents**. Select one exact lens, then commit.

- Use the director's lens ladder: spatial wide, human normal, or compression/detail. Choose by narrative need and shot scale rather than always selecting the profile default.
- Available anchors include 18, 21, 24, 27, 28, 32, 35, 40, 45, 50, 58, 65, 75, 85, 100, 135, and 180mm.
- Describe perspective behavior: stretched foreground, natural human scale, flattened planes, distant surveillance, macro-like detail, or architectural compression.
- Specify spherical or restrained anamorphic behavior only when it materially matches the grammar. A 2.35:1 frame does not automatically imply anamorphic flares or oval bokeh.
- Lock focus strategy: deep staging, moderate relational focus, selective plane, close-focus falloff, rack-focus endpoint, or split-plane clarity.
- Lock aperture behavior qualitatively and name the focus subject. Never use shallow depth of field as a generic cinema shortcut.

Match focus depth to blocking: deep focus for spatial relationships, moderate focus for observation, shallow focus only for deliberate isolation.

## Variation Engine

Choose one item from each axis before prompting. Change visual grammar, not only color.

### Shot Scale

- extreme wide environment
- wide ensemble
- medium two-shot
- medium close observation
- close portrait
- insert/detail

### Composition

- layered-depth tableau
- off-center negative space
- doorway or window frame-within-frame
- one-point symmetry
- lateral profile staging
- foreground occlusion
- reflection or glass separation
- compressed planes
- axial offset symmetry
- nested rectangles
- lateral compartment staging
- S-curve eye path
- extreme foreground scale
- strong horizon and vanishing wedge

### Camera Behavior

- locked-off witness
- low, still observation
- precise slow dolly
- shoulder-level handheld drift
- lateral tracking implication
- subjective close proximity

### Light Logic

- soft overcast daylight
- window-motivated interior
- mixed practical night light
- fluorescent institutional light
- sodium-vapor street night
- hard directional sun
- dusk ambient with practicals

### Capture Texture

- fine 35mm grain
- pushed high-speed film grain
- subtle halation and bloom
- clean large-format digital restraint
- mild underexposure and crushed shadows
- gentle highlight roll-off and lifted blacks

## Standard Prompt Shape

Write the final prompt as five compact paragraphs:

1. native 2.35:1 frame + narrative instant + original setting;
2. blocking + frame geometry + production-design details;
3. camera position + one exact lens + focus + camera behavior;
4. motivated light + palette + capture texture;
5. emotional temperature + originality and avoid-list.

Do not use generic filler such as “cinematic masterpiece,” “award-winning,” or “beautiful cinematography.” Prefer measurable, imageable instructions.

## Workflow

1. Parse the request.
   - Extract story beat, subjects, location, era, time, weather, director, emotional temperature, and any exact invariants.
   - If details are missing, invent only what is needed to make one coherent frame.

2. Select the grammar.
   - Load `references/director-grammars.md` for named or suggested directors.
   - Always load `references/composition-geometry.md` and choose a director-compatible primary geometry.
   - Load `references/director-color-signatures.md` and lock a director-compatible palette recipe.
   - Load `references/lens-optics-and-focus.md` and select one exact lens from the director's scene-conditioned ladder.
   - Load `references/production-design-and-texture.md` and lock a coherent material world.
   - Choose a primary grammar, a strength level, and a seven-axis Director DNA bundle.
   - If no director is supplied, select a grammar that fits the story and disclose the choice.

3. Choose a variation recipe.
   - Pick shot scale, primary composition geometry, optional supporting geometry, camera behavior, light logic, and capture texture.
   - Assign the primary focal anchor, secondary narrative anchor, eye path, and negative-space region.
   - Choose the dominant color family, support family, accent, neutral base, exposure behavior, and the physical carriers of each color.
   - Choose one optical behavior, one focus strategy, one material family, one atmospheric medium, and one controlled imperfection.
   - Avoid repeating the last visible recipe.

4. Compile the prompt.
   - Use the five-paragraph Standard Prompt Shape.
   - Remove director names from the generation prompt and retain only translated characteristics.
   - State the seven signature invariants concretely and make the strongest traits visually dominant.
   - Describe the composition geometry through concrete placement, perspective, blocking, and light; never ask the model to display a grid or spiral.
   - In paragraph 4, state exact color families, their visual distribution, which surfaces/lights/wardrobe carry them, and how the primary and secondary anchors use color contrast.
   - State “native 2.35:1 composition, no letterbox bars.”

5. Generate.
   - Use built-in image generation unless the user explicitly requests prompt-only or a supported alternate path.
   - Inspect composition, focal hierarchy, eye path, subject count, color distribution, skin, motivated light, optical behavior, material coherence, anatomy, unwanted text, and whether at least five signature axes survived.
   - Inspect at thumbnail size. Confirm that the director-compatible palette remains immediately legible without reading the prompt.

6. Enforce ratio.
   - If the saved raster is not exact 2.35:1, run:
     `python scripts/crop_to_scope.py INPUT OUTPUT --anchor-x 0.5 --anchor-y 0.5`
   - Adjust anchors from 0 to 1 to protect an off-center subject. Never stretch the image.
   - Inspect the cropped result once. Confirm that the primary and secondary anchors still sit on the intended geometry and no crop-created tangency appears.

7. Iterate once when necessary.
   - Regenerate once if the result reads as generic cinema, has a weak or incorrect color signature, has accidental or weak composition, loses its focal hierarchy after cropping, shows fewer than five signature axes, has generic materials, copies recognizable IP, loses the narrative instant, contradicts the selected lens/composition, or cannot survive the 2.35:1 crop.

8. Return the final frame, prompt, and shot card.

## Negative Constraints

Always avoid:

- letterbox bars baked into the image, borders, poster layouts, title cards, subtitles, credits, logos, and watermarks
- generic orange-and-teal blockbuster grading unless specifically motivated
- random anamorphic flares, extreme bokeh, or shallow focus used as shortcuts for cinema
- overdesigned sets, excessive props, multiple unrelated actions, and fashion-editorial posing
- plastic skin, glamour retouching, game-engine 3D, concept-art brushwork, and HDR harshness unless requested
- direct copies of famous frames, recognizable actors, protected characters, signature costumes, or franchise locations
- director names in the final generation prompt when the director is living

## Output Format

```markdown
**生成画面**

![2.35:1 cinematic frame](absolute-image-path-or-rendered-image)

**镜头卡**

- Mode: Frame
- Strength: [40 / 85 / 90 / 100]
- Director translation: [name supplied by user] → [3–6 concrete traits]
- Director DNA: [seven axes; mark the dominant axes]
- Composition: [primary geometry; optional supporting geometry] → [primary anchor / secondary anchor / eye path]
- Color signature: [strength] → [dominant / support / accent / neutral / exposure]
- Recipe: [shot scale / composition / camera / light / material / texture]
- Lens: [one exact full-frame-equivalent focal length], [perspective / optical family / focus]
- Art direction: [architecture / surfaces / wardrobe / hero prop / atmosphere / controlled wear]
- Ratio: 2.35:1 [native or cropped]

**最终 Prompt**

```text
[five compact paragraphs used for generation]
```

**解读**

[one short sentence explaining the visible dramatic instant]
```

## Quality Gate

Before finalizing, verify:

- Is the delivered raster exactly or natively 2.35:1?
- Does the frame show one clear narrative instant rather than a poster or plot summary?
- Did the prompt translate the director into concrete visual traits?
- Is the director-compatible color signature recognizable at thumbnail size?
- Do set, wardrobe, motivated light, props, shadows, and capture response carry the palette rather than a single global tint?
- Is the strongest chroma or warm/cool contrast supporting the primary anchor?
- Are skin tones believable within the chosen color logic?
- Does the image avoid unrelated palettes and generic orange-teal grading?
- Are at least five of the seven Director DNA axes visible, with the intended dominant axes unmistakable?
- Would the formal family remain distinctive if color grading and grain were removed?
- Is one primary composition geometry clearly organizing the frame?
- Are the primary and secondary anchors placed deliberately, with a readable eye path?
- Does the chosen geometry fit the director rather than impose generic beauty rules?
- Is negative space active and balanced rather than dead or accidental?
- Did the exact 2.35:1 crop preserve the intended geometry without harmful tangencies?
- Is there exactly one committed focal length and a plausible focus strategy?
- Does perspective compression or distortion visibly agree with the chosen focal length and camera distance?
- Do architecture, surfaces, wardrobe, prop, atmosphere, and wear belong to one coherent material world?
- Are camera height, distance, blocking, and motivated light specified?
- Does the composition use foreground, midground, and background deliberately?
- Is the result original rather than a recognizable frame or actor recreation?
- Are letterbox bars, typography, logos, subtitles, and watermarks absent?
- Did the run actually generate the image unless prompt-only was requested?
