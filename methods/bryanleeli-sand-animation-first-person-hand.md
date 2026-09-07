---
name: sand-animation-first-person-hand
description: Create or adapt high-fidelity first-person sand-animation scenes from reference images or story themes, including story-scene design, sand-style illustration assets, and physically believable hand-driven reveals.
---

# Sand Animation First Person Hand

Use this skill when a video, HTML prototype, HyperFrames composition, or animation scene needs a convincing **first-person sand-table effect**.

The result must look like **real sand animation on a warm light table**:

- a real first-person hand performs the action;
- sand falls, accumulates, wipes, and settles physically;
- complex subjects remain detailed and recognizable;
- the newest visible mark appears only at or just behind the active hand contact / impact point;
- the final image reads as a sand artwork being created, not as a finished image with a hand pasted on top.

Do not optimize only for “it runs.” Optimize for **causality, tactile realism, subject fidelity, and cinematic presentation**.

---

## 0. Input Modes

Choose the route from the user's input.

### Existing reference images

When the user provides images, treat them as the primary source. Use the
image-driven workflow and preserve the recognizable subject details.

### Story theme, moral, concept, or script without images

When the user provides only a story theme, moral, product idea, or short script,
do not ask for images by default. First design a compact story and the sand-style
illustration assets, then animate those assets through the same hand-driven
sand reveal workflow.

Read [references/story-theme-workflow.md](references/story-theme-workflow.md)
for the required story package, illustration prompt contract, semantic-region
planning, narration rules, and QA checklist.

Only ask the user for reference images when the story depends on a specific real
person, product, venue, brand visual, copyrighted scene fidelity, or private
material that should not be invented.

---

## 1. Real Hand Assets Are Mandatory By Default

Always use the bundled real first-person hand assets when they are available.

Preferred assets:

- `assets/hand-skinny-pour-first-person-v2.png`
  - default for additive skinny pouring;
  - preferred hand for drawing dark sand lines and details.

- `assets/hand-wipe-first-person.png`
  - default for wiping, clearing, pushing, or smearing existing sand.

- `assets/hand-draw-first-person.png`
  - use for fingertip carving, negative-space drawing, or direct manipulation.

- `assets/hand-pour-first-person.png`
  - legacy pouring asset;
  - use only after confirming it contains no baked-in falling sand or unwanted background.

### Hard rule

**Do not downgrade to a fake, programmatic, illustrated, vector, silhouette, or symbolic hand if a real hand asset exists.**

A fake hand may be used only when the user explicitly requests a stylized hand or when the real assets are unavailable.

### First-person orientation

For an overhead or near-overhead sand-table shot:

- the forearm must enter from the bottom / near edge of the frame;
- the hand extends toward the upper / far side;
- the arm should remain visually connected to the lower edge;
- avoid a floating hand PNG disconnected from the viewer.

A forearm entering from the top usually reads as another person standing opposite the viewer and is not the default first-person orientation.

---

## 2. Choose the Correct Sand Technique

Sand animation uses different physical techniques. Do not substitute one for another.

### A. Additive / skinny pouring

Use when a clean or lightly textured surface gains new dark sand marks.

Preferred hand:
`hand-skinny-pour-first-person-v2.png`

Pose:
- semi-closed fist or pinched hand;
- held above the light table;
- sand leaks through a narrow gap;
- hand does not touch the forming line.

Required causal chain:

`hand release gap -> falling sand -> impact point -> settled sand mark`

The falling stream must visually connect the hand to the drawing.

Do not use:
- a pointing finger pretending to draw a fresh poured line;
- a hand touching the table while still representing free-falling sand.

### B. Fingertip carving / manipulation

Use when sand already exists and the artist:
- removes sand;
- pushes sand;
- refines details;
- creates negative-space marks;
- carves highlights.

Preferred hand:
`hand-draw-first-person.png`

The contact point must remain physically on the sand surface.

### C. Wiping / clearing

Use when transitioning, clearing, or pushing larger sand areas.

Preferred hand:
`hand-wipe-first-person.png`

A wipe must leave:
- irregular residue;
- displaced sand;
- a compression ridge;
- small streaks or islands.

Do not use a perfectly clean digital erase.

---

## 3. Non-Negotiable Motion Model

Treat the scene as synchronized systems driven by **one shared trajectory**.

Minimum systems:

1. clean real-hand layer;
2. airborne sand layer;
3. deposited / settled sand layer;
4. reveal state;
5. contact ridge / local shadow;
6. wipe residue if applicable.

All systems must derive from the same sampled path.

Use one normalized trajectory function such as:

```js
const pose = trajectoryAt(progress);

drawSettledSand(pose, progress);
drawAirborneSand(pose, progress);
drawContactPhysics(pose, progress);
drawRealHand(pose);
```

Do not author independent tracks such as:

```js
handX
sandX
revealX
```

Independent tracks drift and create the false impression that the hand is floating over an unrelated completed image.

---

## 4. Direction Lock

The hand path and drawing path must match.

If the hand moves:
- left -> right, the newest mark appears left -> right;
- bottom -> top, the mark grows bottom -> top;
- around a curve, the reveal follows that curve.

The newest visible sand should sit:
- at the impact point;
- directly beneath it;
- or slightly behind it.

Never reveal target detail ahead of the active hand.

If the target appears before the hand reaches it, the shot fails.

---

## 5. Stroke Segmentation

Split the target into physically drawable connected strokes.

A disconnected:
- line;
- eye;
- dot;
- ornament;
- wall segment;
- staff segment;
- crowd cluster;
- enclosed detail

must use a separate gesture when necessary.

Between disconnected strokes:

1. stop sand emission;
2. release the pouring gesture;
3. travel quickly to the next start point;
4. engage again;
5. resume emission.

Never:
- keep pouring while crossing blank space;
- reveal multiple disconnected details from one continuous sweep;
- let a full symbol appear while the hand only travels over part of it.

---

## 6. Gesture Grammar

Every visible hand gesture should follow four phases.

### 1. Approach

- move toward the next start point;
- no emission;
- faster than active drawing motion;
- hand can slightly rotate into position.

### 2. Engage

- short 80–180 ms settling phase;
- hand enters the correct pose;
- sand begins gently.

### 3. Action

- pour, carve, or wipe along the shared path;
- reveal remains locked to the active point;
- hand speed may vary naturally.

### 4. Release

- emission stops before travel;
- add a small follow-through;
- hand either moves to the next stroke or exits.

Do not keep the hand moving at one constant robotic speed.

---

## 7. Sand Must Behave Like Material

Sand is not a mask and not a simple particle overlay.

Every additive stroke should contain three material zones.

### A. Core pile

- darkest part;
- highest density;
- follows the exact stroke centerline;
- narrow and visually heavy.

Typical width at 1080×1920:
- about 6–14 px for detail strokes;
- wider for large mass strokes.

### B. Shoulder scatter

- lower-density grains around the core;
- irregular rather than perfectly Gaussian;
- asymmetric is preferred;
- slightly wider on the trailing side of fast movement.

Typical width:
- about 18–38 px.

### C. Contact ridge / micro-shadow

At or near the current impact point:
- show a subtle local pile;
- small dark crescent, ridge, or compressed grains;
- strongest while emission is active;
- decays quickly after the hand passes.

This creates perceived height and physical contact.

A single uniform cloud of particles reads as digital confetti and should be avoided.

---

## 8. Velocity-Responsive Deposition

Deposited sand must react to hand speed.

Default behavior:

- slow movement -> thicker, darker, denser core;
- medium movement -> normal stroke;
- fast movement -> thinner core, wider trailing scatter;
- brief pause -> small endpoint accumulation;
- restart -> short re-engage buildup.

Example:

```js
const speed = clamp(
  distance(previousContact, contact) / referenceDistance,
  0,
  1
);

const coreWidth = mix(14, 7, speed);
const scatterWidth = mix(20, 38, speed);
const density = mix(1.15, 0.76, speed);
```

Do not use fixed particle count and fixed stroke thickness for all motions.

---

## 9. Falling Sand Physics

For skinny pouring:

- emitter starts at the real hand’s release gap;
- falling sand travels mostly downward;
- stream is short and visually connected;
- particles accelerate slightly toward the table;
- horizontal drift remains small;
- scatter happens mainly near impact.

Avoid:
- long curved particle strings;
- sideways sand lines parallel to the hand;
- particles appearing from empty space;
- a stream that begins from the center of the hand image rather than the calibrated release gap.

Calibrate emitter coordinates per hand asset.

---

## 10. Wipe Physics

A wipe should produce three zones.

### Clean zone
Behind the hand:
- most sand removed;
- not necessarily perfectly clean.

### Compression ridge
At the leading edge:
- displaced sand gathers;
- thicker / darker than surrounding residue.

### Residue zone
Around the wipe boundary:
- isolated grains;
- thin streaks;
- broken fragments;
- deterministic irregularity.

Avoid a single linear `destination-out` gradient as the whole effect.

For scene-clearing transitions, prefer a repeated palm-wipe model over a single
front mask:

- use several fast diagonal passes that start outside the lower-left side of the
  artwork and exit outside the upper-right side, alternating direction on
  adjacent passes;
- offset those passes across the normal direction so the hand covers the top,
  middle, bottom, left, and right artwork areas instead of a narrow center band;
- derive the hand pose, erasure footprint, disturbed grains, and residual ridges
  from the same `wipeCenter(passIndex, passLocal)` or equivalent sampled
  trajectory;
- anchor the wipe hand PNG by a calibrated palm contact point inside the image,
  not by adding an unrotated screen-space y-offset after the pose is sampled;
- inside the palm contact footprint, destroy the original coherent linework
  completely with a rough hard mask; do not leave the original drawing visible
  as a lighter transparent copy;
- after each contact sample, draw back only unstructured disturbed material:
  short streaks, loose grains, broken islands, and a small compression ridge;
- the first pass may make the artwork messy and displaced, but later passes
  should remove the recognizable image, not merely fade it.

Avoid:
- one large full-frame polygon or linear gradient that erases areas the hand did
  not physically pass over;
- a left-to-right wipe that never reaches the upper and lower artwork areas;
- synchronized-looking hand motion with a separate independent erase front;
- repeated regular residue shapes that read as a stamped pattern.

A possible retention model:

```js
retention =
  smoothstep(front - feather, front + feather, projectedDistance);

retention *=
  0.92 + seededNoise(x, y) * 0.08;
```

Then render displaced grains separately at the wipe front.

---

## 11. Complex Reference Images Must Stay Complex

When the source image is complex, do **not** simplify it into:
- a symbolic outline;
- a few primitive shapes;
- a cartoon icon;
- a stick figure;
- a minimal silhouette.

The final sand artwork must preserve the image’s **recognizable structure and local detail density**.

For a complex mythic / cinematic reference, preserve:
- facial identity anchors;
- costume and armor structure;
- hair / fur texture;
- major props;
- architecture;
- secondary figures;
- environmental atmosphere.

The skill should favor **high-fidelity sand interpretation**, not aggressive simplification.

---

## 12. Semantic Decomposition for Complex Images

Do not reveal a complex image uniformly.

Break it into semantic regions.

Default hierarchy:

### Layer 1 — Identity anchor
Reveal first:
- face;
- eyes;
- brows;
- iconic headgear;
- emblem;
- key silhouette;
- most recognizable object.

Goal:
the subject becomes recognizable within the first 1–2 seconds.

### Layer 2 — Structural mass
Then reveal:
- body;
- torso;
- main garment;
- architecture;
- large props;
- major foreground shapes.

### Layer 3 — Secondary detail
Then add:
- hair;
- armor;
- folds;
- ornaments;
- wall texture;
- crowd detail;
- surface decoration.

### Layer 4 — Atmosphere
Finally add:
- sky;
- dust;
- clouds;
- smoke;
- background edges;
- loose foreground sand;
- subtle environment texture.

---

## 13. Example: Complex Warrior + Ancient City Scene

For a reference image containing:
- a monkey-king / mythic warrior;
- detailed face;
- ornate headband;
- hair / fur;
- armor;
- staff;
- ancient wall;
- gate;
- pavilion;
- crowd;
- dust atmosphere;

do not treat it as one image region.

Recommended decomposition:

1. `warrior_face`
2. `brow_eyes_nose_mouth`
3. `headband`
4. `hair_fur`
5. `staff`
6. `armor_upper`
7. `scarf_cloak`
8. `torso_lower`
9. `pavilion`
10. `wall_stones`
11. `gate_arch`
12. `crowd`
13. `foreground_terrain`
14. `sky_dust`

Each region may contain several connected strokes.

Use more strokes for high-detail identity areas than for atmosphere.

---

## 14. Source Image Use

For image-driven stories, source images are primarily **analysis and target-generation inputs**.

When the user prioritizes complex image fidelity over pure particle reconstruction, use the source-preserving grain-mask technique:

1. load the sand-styled source image at full frame;
2. cover-crop it to 1080x1920;
3. apply a mild-to-medium blur so it no longer reads as a crisp photo;
4. add deterministic fine sand grain, edge-darkening, light-table warmth, and vignette;
5. reveal this sand-textured material only through the local hand-driven mask.

This is acceptable only when the source image is already sand-styled or has been converted to sand-art texture first. It must not look like an untouched photograph appearing under a brush.

Preferred workflow:

1. load the source image;
2. analyze luminance, edges, and semantic regions;
3. choose either a source-preserving grain-mask material or deterministic sand target points;
4. reveal the material locally through physical gestures;
5. render the final frame as sand artwork.

Avoid showing the untouched source image directly under a reveal mask as the primary final visual.

If the current template uses the source image as a texture reference, ensure:
- the reveal stays local;
- the image is blurred/softened enough to avoid crisp-photo clarity;
- the image is heavily sand-textured with deterministic grains;
- the hand remains causally linked;
- no untouched photographic region appears ahead of the hand.

---

## 15. Target Point Data

For source-preserving grain-mask rendering, dense target points are optional. The template can run with semantic `regions` only, because the material detail comes from the sand-textured source image and deterministic grain overlay.

For direct particle reconstruction, each sampled target point should ideally contain:

```text
x
y
alpha
radius
random
revealOrder
regionIndex
localOrder
tone
edge
```

Recommended meaning:

- `x`, `y` — final location;
- `alpha` — base sand opacity;
- `radius` — grain size;
- `random` — deterministic per-point variation;
- `revealOrder` — global reveal order;
- `regionIndex` — semantic region;
- `localOrder` — reveal order inside region;
- `tone` — normalized local darkness;
- `edge` — normalized edge strength.

Use:
- higher `tone` for darker / denser sand;
- higher `edge` for stronger contour definition;
- lighter sparse sand for atmosphere and highlights.

---

## 16. Avoid Large Automatic Final Fill

Do not use a large late-stage `finalFill` that makes an entire region appear independently from the hand.

Bad pattern:

```js
const finalFill = smooth((local - 0.76) / 0.24);
return Math.max(coverage, finalFill);
```

This can reveal target details the hand never physically reached.

If a gap-filling stabilization pass is needed, keep it tiny:

```js
const finalFill =
  smooth((local - 0.94) / 0.06) * 0.10;
```

Use it only to close small visual holes.

It must not visibly complete a region on its own.

---

## 17. Real Hand Compositing

Real hand assets should be rendered above sand.

Recommended order:

1. light-table background;
2. fixed base dust;
3. old settled sand;
4. current deposited sand;
5. airborne falling sand;
6. contact ridge / local shadow;
7. hand cast shadow;
8. clean real hand;
9. subtle vignette.

Keep sand out of the hand PNG itself.

Do not bake:
- falling grains;
- dust trails;
- contact ridge;
- sand pile

into the hand asset.

Those belong to Canvas.

---

## 18. Hand Shadow

A subtle hand shadow improves realism.

Guidelines:
- soft;
- low opacity;
- close to the hand;
- stronger near the wrist / lower hand;
- not a large dramatic drop shadow.

Do not let the shadow obscure detailed artwork.

---

## 19. Light-Table Look

Default style:

- warm amber / golden-brown illumination;
- brighter center;
- darker outer edges;
- dark brown sand;
- fine high-density grains;
- slight surface imperfections;
- natural scattered residue;
- strong but not crushed contrast.

The background should feel luminous rather than like a flat brown fill.

Avoid:
- pure black background;
- plain beige background;
- clean digital gradients with no material texture.

---

## 20. Camera and Composition

Default:
- overhead or near-overhead;
- 9:16 vertical;
- active hand + active drawing kept inside the central safe area;
- no excessive camera motion during precise drawing.

Optional:
- 1–2% slow push-in over an entire scene;
- very subtle camera breathing;
- minimal handheld drift.

Do not use camera movement that breaks emitter / contact calibration.

---

## 21. Opening Rhythm

Within the first 1–2 seconds:

- show a real hand;
- show visible sand emission or manipulation;
- reveal a recognizable identity anchor.

Avoid spending the opening on:
- empty brown table;
- random sand particles;
- an unrecognizable abstract line;
- slow hand entrance with no result.

For short-form social video, prioritize immediate visual payoff.

---

## 22. Quality Presets

### Preview

Use only for fast iteration.

- lower target point count;
- fewer airborne grains;
- reduced trail density;
- simplified ridge / shadow;
- no expensive blur.

Do not use Preview for a user-provided complex artwork unless explicitly requested.

### Production — Default

Use by default.

- dense target points;
- real hand assets;
- velocity-responsive deposition;
- contact ridge;
- wipe residue;
- detailed semantic decomposition;
- deterministic rendering.

### Hero

Use for:
- important shots;
- complex character close-ups;
- cinematic sand art;
- thumbnails;
- short premium sequences.

Hero should add:
- highest target density;
- more micro-detail;
- stronger tone / edge fidelity;
- richer endpoint accumulation;
- hand shadow;
- wipe residue;
- more atmospheric sand.

For a complex reference image, choose **Production or Hero**, never automatically simplify to Preview quality.

---

## 23. Bundled Assets

Reusable assets in `assets/` include:

- `seed-to-birds-sand-animation.html`
  - standalone 9:16 starter;
  - suitable for simple procedural stories.

- `three-scene-region-sand-animation.html`
  - image-driven multi-scene template;
  - suitable for dense still-image sand stories.

- `hand-draw-first-person.png`
  - real first-person manipulation / drawing hand.

- `hand-pour-first-person.png`
  - legacy real pouring hand.

- `hand-skinny-pour-first-person-v2.png`
  - preferred real first-person additive pouring hand.

- `hand-wipe-first-person.png`
  - preferred real first-person wipe hand.

- `gsap.min.js`

Image-driven templates may also use:
- `scene-*.png`
- generated `sand-target-points.js`

Generate target points with:
`scripts/generate_sand_points.py`

---

## 24. Template Selection

Choose the template according to content complexity.

### Simple symbolic transformation

Examples:
- seed -> sprout -> tree -> birds;
- heart -> flower;
- moon -> bird.

Use:
`seed-to-birds-sand-animation.html`

### Complex user-provided image

Examples:
- detailed character;
- movie-like composition;
- architecture + people;
- portrait + environment;
- mythological scene.

Use:
`three-scene-region-sand-animation.html`

or a derived image-driven template.

Do **not** reduce a complex image to the procedural starter simply because it is easier.

### Story-theme generated illustration

Examples:
- a moral fable with 2-3 scenes;
- a product metaphor told through one protagonist;
- a philosophical short story;
- a poem-like transformation sequence;
- a tutorial intro that needs a cinematic sand-art demo.

Use:
1. [references/story-theme-workflow.md](references/story-theme-workflow.md)
2. generated transparent sand-style illustration assets with the subject preserved;
3. `three-scene-region-sand-animation.html` or a derived image-driven template.

The generated illustration is the source artwork. The final video still needs
real-hand causal reveal, semantic region order, sand material treatment, and
frame QA.

For story-theme generation, default the source illustrations to **transparent
RGBA sand layers**: keep the subject, props, and necessary environment marks as
sand; leave empty background transparent. Let the animation template provide the
light-table background, so the final composition has no generated rectangular
image boundary.

---

## 25. Image-Driven Workflow

For a complex reference image:

1. keep the source image at useful resolution;
2. preserve important subject details;
3. define semantic regions;
4. prioritize identity anchors;
5. run `generate_sand_points.py`;
6. use the real pouring hand;
7. reveal local regions through physically drawable strokes;
8. use non-emitting travel between disconnected strokes;
9. add wipe only when there is a narrative reason;
10. verify no detail appears ahead of the hand.

---

## 26. HyperFrames / Seekable Rendering

If used inside HyperFrames or another frame-seekable renderer:

- all randomness must be deterministic;
- do not use unseeded `Math.random()`;
- do not depend only on wall-clock time;
- derive state from absolute timeline time;
- repeated rendering of the same frame must produce identical grains and reveal state.

Keep `mulberry32()` or an equivalent seeded PRNG.

Backward scrubbing must reproduce:
- the same particles;
- the same hand pose;
- the same deposited state;
- the same wipe residue.

---

## 27. Frame QA

Check at least:
- start;
- 20%;
- 40%;
- 60%;
- 80%;
- end

of every major gesture.

A production shot passes only if:

1. the hand is a real bundled hand asset unless the user requested stylization;
2. hand orientation reads as first-person;
3. hand pose matches the physical technique;
4. falling sand begins at the calibrated release gap;
5. stream reaches the current impact point;
6. newest mark is at or just behind the impact point;
7. no target detail appears ahead of the hand;
8. disconnected strokes contain non-emitting travel;
9. slow vs fast motion changes deposited sand behavior;
10. wipes leave residue and displaced sand;
11. complex subjects remain recognizably detailed;
12. no large region suddenly auto-fills;
13. scrubbing reproduces the exact same result.

If any item fails, fix trajectory, emitter calibration, semantic decomposition, or deposition physics before polishing color or camera movement.

---

## 28. Default Execution Preference

When uncertain, prefer:

- real hand;
- high-fidelity complex sand image;
- semantic decomposition;
- local progressive drawing;
- dense sand texture;
- physical deposition;
- velocity response;
- residue;
- causal motion;
- cinematic composition;
- Production or Hero quality.

Do not prefer:

- fake hand;
- programmatic hand;
- generic pointer;
- simple icon;
- stick figure;
- line-art simplification;
- whole-image fade;
- whole-region automatic reveal;
- clean Photoshop-like wipe;
- floating particles unrelated to the hand.

---

## 29. User Reference Image Priority

When the user provides a reference image:

- treat it as the primary subject and composition reference;
- preserve its recognizable major structure;
- preserve high-value local details;
- do not replace it with a simpler invented subject;
- do not downgrade the visual complexity without explicit user permission.

If the reference is highly detailed, automatically select:
- image-driven workflow;
- Production or Hero quality;
- semantic region decomposition;
- real-hand assets.

The output should feel like the user’s image is being recreated through sand, not loosely reinterpreted as a simple drawing.

---

## 30. Final Standard

The skill succeeds only when the viewer can believe:

> A real person is physically creating this detailed image with sand on a light table.

If it instead looks like:
- a finished picture with a hand on top;
- an image reveal effect;
- a particle overlay;
- a fake hand;
- a simplified sketch;

the result should be treated as unfinished and revised.
