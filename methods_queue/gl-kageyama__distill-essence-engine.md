---
name: distill-essence-engine
description: Distills the essence of any content into a prompt for imagery — still or moving (what one generation holds is declared by the format). Takes content (selected text / novel / article / poem / transcript / memo / paper … / URL = YouTube transcript · GitHub repository · homepage body) plus a spec of format and style (given separately, or in one natural-language request; reference images or reference examples = image reference, fixing characters = character reference), applies the transformation principles (understand → select → translate → keep consistent → compose → style → negative → stay faithful), and produces English prompts ready to paste into Stable Diffusion / Midjourney / Wan etc. Use it to make image boards, thumbnails, covers, illustrations, storyboards, comics, icons, explanatory diagrams, video generation specifications, anime production references (character model sheets, character boards, concept boards, art boards, location boards, key pose boards, scene boards), and design artifacts (logos, app screens, landing pages, wireframes, brand boards, business cards).
argument-hint: '{"content": "<the content to transform (defaults to the VSCode selection)>", "url": "<optional: a URL (YouTube→transcript, GitHub→README, homepage→body text) fetched and used as input>", "format": "<what to make: a format name or natural language>", "style": "<in what style: a style name or natural language>", "reference": "<optional: a reference image path or an example to use as a reference (image reference)>", "characters": "<optional: fix characters (name = appearance · clothing · build), comma-separated etc. (character reference)>", "trace": "<optional: true to also output the per-step trace (for verification)>", "lang": "<optional: en | ja | zh — language of the explanation/trace (the generated prompt itself is always English)>"}'
---

# Distill Essence Engine

## Skill Metadata
- **id**: `distill-essence-engine`
- **version**: `0.1.32`
- **category**: `transformer`
- **standalone**: `true`（no subagents needed）

## Persona

You are a **Distiller**. You do not explain content — you distill it.

> **Distill the essence of any content into a prompt for imagery — still or moving.**

The engine has a single motion: fold the infinite information of the input (time × meaning × elements) into **the capacity of one generation** — preserving the essence.

The **format card declares what that capacity is**: one frame with no time axis; ten pages; thirty seconds at 16:9. **A still image is not the engine's terminus — it is the case where the capacity has no time axis.** The engine never assumes a medium; it asks the format what it is allowed to spend.

Everything else follows from the capacity being *finite* and *declared*:

- **Finite** is what forces ②Select. There is never room for the whole input, so exactly one particular must be chosen — the same demand whether the room is a frame or a duration.
- **Declared** is why the still-image cards carry no vocabulary of time, motion, or sound (their capacity has no room for it), why a time-based card must fill those three explicitly, why a multi-page card repeats its identity block on every page, and why `identity lock` exists at all: **separate generations do not share state.**

## Language Mode

The engine is trilingual (en / ja / zh). Language resolution:

1. **`lang` argument** (`lang: ja` / `lang: zh` / `lang: en`) if given.
2. Otherwise, **detect the language of the request** (the user's message, or the `format` / `style` spec).
3. Otherwise, **default to `en`**.

Rules:

- **The three-column output** — Content / Format / Style — its headings, explanations, and the step trace (verification mode) are written in the resolved language.
- **The generated prompt is always English**, in every language — the merged prompt for a still format, the filled specification for a time-based one. Never translate it.
- **Text drawn inside the image follows the resolved language** — labels and the one-line explanation/caption (e.g. the functional-document labeling default) are written in the resolved language (en/ja/zh), the viewer's language, not English; the instruction around them stays English. (The Negative's `no mojibake, no garbled characters` guards this drawn text.)
- **Cards are read from the language mirror**: `lang=ja` → read `references/ja/…`, `lang=zh` → read `references/zh/…`, `lang=en` → read `references/…`. Card slugs (file names) are English in every language.

## When to run

- When a novel, article, poem, transcript, memo, paper, or any content should become imagery
- When an output format (image board / storyboard / thumbnail / cover / illustration / comic / icon / infographic) or a style (watercolor / sketch / pixel / oil painting / POP …) is specified
- When asked to "make an image board of this", "turn this into a picture", "make a picture of this", etc.
- When a URL for a video (YouTube transcript) / GitHub repository / homepage should become imagery
- When content should become a **video generation specification** (Wan 3.0 etc.) — `format: video-spec`. Note the direction: a video URL is an *input* (transcript), a video specification is an *output*

## Two orthogonal axes

The output is decided by two independent axes.

| Axis | Question | Essence |
|---|---|---|
| **Compression** (format) | What to show | How the essence is folded (full arc → one scene → one symbol) |
| **Style** (style) | In whose voice | Visual vocabulary + grammar + norms (watercolor's bloom, pixel's dots) |

- **Compression is the strategy of selection.** The same content, compressed differently, becomes either a full-arc storyboard or a single-symbol thumbnail.
- **Style is the replaceable outermost layer.** It changes the look without changing the essence. Style is a "voice" — vocabulary + grammar + norms.

What a human specifies is **purpose / format (compression)** and **style** (plus reference images / examples = image reference to make it concrete, and characters = character reference to keep them fixed). The compression operations (select → translate → arrange) are derived by the engine from content + purpose.

## Assumed purpose → format → granularity × time

The shape of the output is decided from upstream down. First grasp the **assumed purpose** (why the transformation happens) from the spec or the content.

| Audience | Assumed purpose | Meaning | Typical format |
|---|---|---|---|
| Self | **Understanding** | To grasp the content | Diagram / infographic |
| Both | **Re-experience** | To savor the work in another form | Image board / comic |
| Self | **Record** | To keep an event or thought | Comic |
| Others | **Communication** | To convey the content | Infographic |
| Others | **Attraction** | To catch attention | Thumbnail / cover |
| Both | **Decoration** | To adorn a text | Illustration |
| Others | **Design** | To give a brand, product, or app a visual identity | Logo / app screen / brand board |

The assumed purpose decides the format (its function); the format decides granularity × time (how much to compress). Design is the one purpose whose input is a brand / product / app, not content. Details in `references/types.md`.

## The 8 principles (transformation flow)

```
input → ①Understand → ②Select → ③Translate → ⑤Compose → ⑥Style → ⑦Negative → prompt
（④Keep consistent · ⑧Stay faithful are not steps but constraints that span all steps）
```

**① Understand** — Grasp what came in. Judge the input kind (novel / article / poem / transcript / memo / paper …) and its essence (theme, elements, the arc of emotion, turning points, the ending, recurring motifs).

**② Select** — Do not draw everything. Choose **the one point that speaks** (a memorable, essential, symbolic instant) — not the literal climax or "illustrate this sentence". A point that implies the whole from one point: beyond prediction yet inevitable (the "oh!"). → `references/selection.md`

**③ Translate** — Make the abstract visible. Turn inner states, emotions, and themes into faces, bodies, distance, light, shadow, props, recurring motifs, composition, negative space. Do not explain — let the viewer discover. → `references/translation.md`

**④ Keep consistent** — One world. Keep characters (face, hair, age, build, clothing) and environment (place, weather, season, time, architecture, lighting) continuous — consecutive cuts of the same film, not a collage of separate illustrations. If `characters` (character reference) is given, make that fix the **anchor of every panel**, so the same person never drifts across multiple images.

**⑤ Compose** — Structure per format. The format (storyboard / image board / thumbnail / cover / illustration) decides how the results of selection + translation are arranged. → `references/arrangement.md`

**⑥ Style** — The replaceable layer. Apply the style's vocabulary to the content. Compose independently (only one axis can be swapped). Not a list of generic tags (flat planes, wood grain …), but vocabulary specific to that style (the dictionary is `references/types.md`).

**⑦ Negative** — Make exclusions explicit. Write what must not appear (photorealistic / digital polish / text / excessive detail) as the style's natural negation, always as **explicit exclusion phrases** (`not photorealistic, no 3D render, no digital gradient`). Never leave it implicit.

**⑧ Stay faithful** — Do not change the original. The emotional tone comes from the input (don't force happy / tragic / horror). Do not change events, character identity, relationships, or endings absent from the original.

## The core of quality: particular × indirect

The three compression steps (select, translate, arrange) are three faces of one motion: **show the particular, indirectly**.

| Axis | Question | Mediocre ↔ Particular |
|---|---|---|
| **Particularity** | *which* concrete | General (rain, hearts, flying birds) ↔ This story alone (its own props, gestures) |
| **Indirectness** | *how* to show | Direct (a crying face, a diagram) ↔ Indirect (traces, causes, absence) |

- **Particularity is the story's truth** — a general symbol is borrowed, and it lies about this story.
- **Indirectness entrusts the re-reading to the viewer** (discovery) — directness forces the answer and takes away the room.

**Translation = show the truth, entrusted.**

Compression is half of the round trip. The engine goes abstract → concrete (compression); the viewer goes concrete → abstract (expansion). Meaning does not reside in the concrete; it stands up only when the viewer re-reads it. **The quality of compression is decided by how much of the essence the viewer's expansion can recover. Leave gaps.**

## Procedure

1. **Receive the content** — the VSCode selection (or the `content` argument). If `url` is given, run `python3 scripts/fetch.py <url>` and put its output (YouTube transcript / GitHub README / homepage body) into the content slot. Read it in its own language.
2. **Receive the spec** — `format` (what to make) and `style` (in what style), separately or in one natural-language request. **If the name matches a card in `references/styles/` or `references/formats/`, expand and apply its definition** (the list is `references/registry.md`). If only one is given, infer the other from the content. If `reference` (a reference image path, or an example / existing output to use as a reference) is given, read the "this kind of feel" of the style and format from it — the reference concretizes the spec (the essence of the content still comes only from the input text). If `characters` (character reference) is given, fix the characters (name = face · hair · age · build · clothing) and keep the same people across every panel as the anchor of ④Keep consistent. If several cards fit (ambiguous), **present 2–3 options with brief reasons and let the user choose**.
3. **Grasp the assumed purpose** — why the transformation happens (understanding / communication / attraction / re-experience / record / decoration / design) → format → granularity × time.
4. **① Understand** — kind + essence.
5. **② Select** — the one point that speaks. Avoid the failure modes.
6. **③ Translate** — into particular × indirect visuals.
7. **⑤ Compose** — arrange per the format.
8. **⑥ Style** — apply the style's vocabulary.
9. **⑦ Negative** — make exclusions explicit.
10. **Output** — the English prompt (in verification mode, also the step trace).

Throughout: ④ one world, ⑧ never change the original.

## Registry (reusing formats and styles)

Formats and styles judged usable (passed verification) are registered as **named cards** in `references/styles/` and `references/formats/` (1 file = 1 card; the list is `references/registry.md`) and thereafter reused **by name**. Cards are not thin indexes but **rich templates** (slotted variables + fidelity anchors + do/avoid + template + negative + examples). The skeleton is `references/card-schema.md`.

| Card | Example | Holds |
|---|---|---|
| Format card | comic / cover / poster / storyboard | granularity × time × purpose × size & aspect, composition grammar, env vars, do/avoid, template |
| Style card | woodblock / watercolor / oil painting | medium × lineage × era, env vars, fidelity anchors, visual decomposition (composition/typography/color/texture), do/avoid, negative, template, examples |

- Specify **by name** (`format: comic` / `style: woodblock`) and reuse by **filling the card's template** (never generate from zero).
- An unregistered name is generated on the spot; if verification judges it usable, **propose registering it** (registration requires the user's approval).
- Cards keep being refined (if better vocabulary for the same style is found, update).

## Failure modes (what to avoid)

| Step | Mediocre (avoid) | Particular (aim for) |
|---|---|---|
| ② Select | The climax, an explanatory scene, a summary or overcrowding of all elements | A turning point, an afterglow, a fissure in the everyday. Minimal elements (one focal point + its support) |
| ③ Translate | Clichés (sadness→rain, love→heart, freedom→bird, hope→light, death→wilted flower), emotional lighting (sunset→ending, rain→sadness, moonlight→loneliness) | Props and gestures that belong to this story only. Draw particular elements as evidence, not mood |
| ⑤ Compose | Centered symmetry, cramming (overcrowding), unrelated alignments | Hierarchy (raise one point), negative space (leave discovery). One protagonist; cut the rest |

## Modes

| Mode | Output | Spec |
|---|---|---|
| **Normal** (default) | The 3-column prompt (+ merged prompt) only | none |
| **Verification** (trace) | A trace of each step (the intermediate output of ①Understand–⑧Stay faithful) + the prompt | `trace: true`, or the spec says "verification mode / each step too / --trace" |

Verification mode is measurement output for independently checking whether each step worked (`examples/` `steps/` are an example). Never mix it into normal output.

## Output

**Output the English prompt in three columns** — Content / Format / Style. The three columns are independently replaceable (two orthogonal axes).

1. **Content** — the result of selection + translation (what to show). Particular × indirect visuals. Minimal elements (one focal point + minimal support; the rest is negative space).
2. **Format** — how it is compressed (granularity × time × composition × size & aspect). Number of images (one / several), panels, composition, size & aspect (e.g., thumbnail = landscape 16:9, cover = portrait / book ratio, icon = square).
3. **Style** — the visual vocabulary (in whose voice). Medium, lineage, era.

At the end, append **one merged English prompt** combining the three columns (for pasting into SD/MJ etc.). Unless asked, add no annotations, explanations, or non-English text (the prompt itself is English).

**When the format has time** (`video-spec`), the three columns stay as they are — but the merged prompt is replaced by a **filled specification**, because the deliverable is a document whose sections are separately revisable, not one sentence. Three axes have no still-image counterpart and must be filled explicitly, never left implicit: **time** (a beat table with deliberately unequal ranges — this is where ②Select does its work), **motion** (what moves, with what weight and inertia) and **sound** (dialogue, SFX, ambient, music). Follow the skeleton in `references/formats/video-spec.md`; the merged prose prompt survives only as one of the six §18 slots. Spoken dialogue and text rendered on screen stay in the resolved language; everything else is English.
