---
name: muge-photo-line-art
description: Transform one user-provided portrait photo into a square minimalist continuous-line decorative poster with one visually unbroken matte-black line, source-aware muted Morandi color blobs, a micro palette, a derived corner motif, and restrained cursive text. Use for photo-to-one-line-art portraits, minimalist line posters, gentle wall-art graphics, wallpaper or stationery visuals, and requests mentioning 一笔画, one-line art, continuous-line portrait, or 极简线稿海报.
---

# Muge Photo Line Art

Turn one portrait photograph into a clean 1:1 decorative poster while preserving the subject's recognizable silhouette, hair flow, pose, and one distinctive anchor.

## Required resources

- Read [references/visual-spec.md](references/visual-spec.md) before composing the generation prompt.
- Use [references/prompt-template.md](references/prompt-template.md) as the canonical prompt structure.
- Inspect the actual source image before generation.
- Use the environment's image-generation or image-editing tool with the source photo attached. Do not return only a prompt unless the user explicitly requests one.

## Handle the input

1. Require one readable reference photo containing one clearly visible person or one coherent interacting group.
2. Use the most recently attached photo unless the user identifies another one.
3. Accept optional choices for the mood phrase, background color, accent colors, recognition anchor, or corner motif.
4. Infer unspecified choices from the source instead of making the user complete a form.
5. Preserve an obvious couple, family pair, or compact interacting group as one composite subject. Keep the person count, poses, spacing, gaze, and contact relationships.
6. If several unrelated people compete for attention or the intended group is unclear, ask which person or group should anchor the composition.
7. If the subject contour is too obscured to recognize reliably, ask for a clearer image rather than inventing a new pose.

## Analyze the reference

Record these variables internally:

- `subject_description`: person count, poses, orientation, spacing, contact relationships, crop, head silhouettes, hair flow, and clothing outlines.
- `recognition_anchors`: one simple distinctive feature for each key person or for the relationship, such as a collar, bandana knot, hairpin group, hat brim, glasses outline, sleeve shape, joined hands, forehead touch, or leaning gesture.
- `open_line_exits`: cropped or incomplete body regions where the continuous line must trail into negative space.
- `background_color`: one flat pale low-saturation cream, grey-blue, or similarly quiet source-derived tone.
- `source_palette`: 3–4 muted colors that correspond to visible source colors and locations.
- `blob_plan`: one medium-large blob, one or two medium blobs, and one small finishing dab.
- `corner_motif`: one small motif extracted from the photo, such as a flower, sparkle, curl, ribbon, or textile geometry.
- `mood_phrase`: 2–3 original English mood words supplied by the user or derived from the image.

Do not expose the inventory unless it helps explain a design decision.

## Simplify the figure

- Preserve the subject count, head silhouettes, hair direction, poses, spacing, contact relationships, crop, and recognition anchors.
- Draw the entire figure as one visually traceable, unbroken, non-branching, thin matte-black line.
- Keep line weight even and the stroke smooth. Avoid sketch buildup, duplicated contours, burrs, hesitation marks, or rough pencil texture.
- Allow an occasional self-crossing only when the single path remains visually understandable; never create a fork or detached secondary stroke.
- Omit eyebrows, pupils, nostrils, eyelashes, individual hair strands, fabric texture, and other small facial or clothing details.
- Keep cropped body contours open. Extend their line exits naturally into the surrounding whitespace; never seal an incomplete torso or limb into a closed cut-off loop.

## Compose the supporting system

- Use a square 1:1 canvas.
- Center the figure and let it occupy approximately 65%–70% of the canvas height, with generous whitespace around it.
- Place 3–4 separated, semi-transparent, soft-edged irregular blobs beneath the black line. Do not overlap the blobs or cover the face.
- Match each blob's color and approximate location to a source-photo color cue. Use only restrained Morandi colors; reject fluorescent or highly saturated accents.
- Add a micro palette in the bottom-left corner, occupying only about 3%–4% of the canvas: four tiny watercolor dabs in a compact vertical rhythm, connected by one hairline and labeled with very small lowercase color abbreviations.
- Add one small source-derived line motif in the top-right corner using a muted palette color.
- Add a small 2–3-word connected cursive phrase at the bottom center. Keep it visually subordinate to the portrait.
- Keep the background flat and clean. Do not add gradients, shadows, grain, paper distress, or decorative texture clutter.

## Generate and inspect

1. Fill the variables in the canonical template without changing its priority order.
2. Attach the original photo as the image reference.
3. Generate one square result.
4. Inspect the result against the validation checklist.
5. Retry once with a targeted correction when a hard constraint fails.
6. If the single-line structure still fails after one retry, explain the limitation and offer a cleaner second attempt with fewer subject details.

## Priority order

Resolve conflicts in this order:

1. Preserve the subject's recognizable silhouette, pose, crop, and recognition anchor.
2. Maintain one visibly continuous, unbroken, non-branching black line.
3. Keep cropped body regions open and extended into whitespace.
4. Preserve the square layout, figure scale, and generous negative space.
5. Derive the muted blobs and their positions from the source photo.
6. Keep the face unobstructed and all blobs separated.
7. Apply the micro palette, corner motif, and cursive phrase.

## Validate the result

Reject and regenerate when any hard constraint fails:

- The canvas is not square.
- The subject count, silhouettes, poses, spacing, contact relationships, crop, or recognition anchors no longer match the source.
- The black line is visibly broken, branched, doubled, heavily varied in thickness, or assembled from sketchy fragments.
- A cropped body region closes into a sealed loop.
- The work contains realistic facial details or many individual hair strands.
- Color blobs overlap each other, cover the face, sit above the black line, or use bright saturated colors.
- The composition contains shadows, gradients, grain, heavy paper texture, borders, logos, or watermarks.

Treat these as soft-quality checks and retry when practical:

- The figure occupies roughly 65%–70% of the height.
- Whitespace feels generous and balanced.
- Blob sizes follow one medium-large, one or two medium, and one small accent.
- The bottom-left palette stays tiny and the top-right motif remains subordinate.
- The cursive phrase is small, legible, original, and correctly spelled.

## Handle typography failures

Image models may distort tiny labels and cursive wording.

1. Preserve exact user-supplied wording and retry once when misspelled.
2. Prefer removing micro labels before enlarging them enough to disturb the hierarchy.
3. If exact wording still fails, disclose the limitation and offer a two-pass version: generate clean artwork without text, then typeset the palette labels and mood phrase separately.

## Deliver the result

Show the generated image. Briefly state the chosen recognition anchor, palette source, open-line treatment, and any typography limitation. Do not expose the full internal prompt unless requested.

## License notice

This skill is licensed under CC BY-NC 4.0. Noncommercial public sharing and adaptation are allowed when attribution, license-linking, and change-marking requirements are followed. Commercial use requires separate prior written permission from the copyright holder. Keep the bundled `LICENSE` file with every copy or redistribution.

若公开分享，欢迎标注：Photo Line Art Skill by @Yeshmuge
