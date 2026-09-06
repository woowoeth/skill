---
name: yarn-rug-reference
description: Create strict reference-based 1080x1620 comparison images that transform a user image into a low-color handmade yarn, rug, blanket, or tufted textile artwork. Use when the user provides an original image and optionally a reference image, and wants faithful composition preservation, 6-8 total colors, unified color blocks, realistic soft fiber texture, natural fuzzy edges, and a clean 2:3 vertical before-after layout.
---

# Yarn Rug Reference

## Goal

Use this skill to strictly reference the provided guide image and transform the user image into a low-color yarn / rug / blanket / tufted handmade artwork. Preserve the original subject and composition. Do not add content.

## Workflow

1. If a reference image is provided, inspect it first. Treat it as the primary visual standard over text.
2. Learn only the reference image's material, fuzzy edge, color unification, and overall presentation. Do not copy its content.
3. Simplify the user image into 6-8 total colors before applying textile texture.
4. Render the bottom image as handmade yarn / rug / tufted textile with clear real fiber flow, unified color blocks, and a natural soft fuzzy edge.
5. Compose a final 1080x1620 vertical comparison: original image on top, finished artwork on bottom.

## Effect

The bottom artwork is not a photo filter or a photo pasted onto fabric. It should look like a simplified handmade textile design: reduce photographic detail, keep only the main color blocks and silhouette, and render the surface with soft, loose, naturally flowing yarn fibers. The fiber texture should feel plush and handmade, with mostly short interwoven fibers and a few longer natural strands, not obvious knitted lines or regular woven patterns.

## Color Rules

- The bottom artwork must use no more than 6-8 total main colors, including sky, ground, objects, shadows, and highlights.
- Large regions must be unified: sky = 1 main blue; grass / ground = 1 main green or brown; mountains / buildings = 1 main neutral gray, brown, or warm gray; water = 1 main blue-green.
- Texture must not add extra color levels.
- Color mixing must stay within the same color family only.
- Do not use cross-family color mixing, colorful noise, random speckles, photographic gradients, or multi-tone fragmentation.
- Sky must be a single main color, with at most one slight value variation.
- Each large region should use unified color blocks. For example, sky, grass, and buildings should each use only 1-2 main colors. Avoid heavy gradients, fragmented tones, and noisy color variation inside the same region.

## Edge

Keep the overall artwork outline stable and close to rectangular. Do not create a regular fuzzy border or decorative frame. Only allow subtle natural fiber scatter and small loose strands around the edge, so the result feels like a real handmade textile edge without becoming messy or ornamental.

## Composition

Do not add elements that are absent from the original. Do not add rocks, trees, people, shadows, roads, or new background details. Do not redesign the scene. Preserve the original subject relationships and main layout.

## Output Layout

- Canvas: 1080x1620, vertical 2:3.
- Background: warm white / off-white only.
- Top panel: original image, 920x690, 4:3, x=80, y=70, no shadow, no border.
- Bottom panel: finished artwork, 920x690, 4:3, x=80, y=815.
- Gap between panels: 55 px.
- Bottom margin: 70 px.
- Bottom artwork body: about 84%-88% of panel width, recommended 780-810 px.
- Use comfortable whitespace. Do not add text, decoration, extra background, shadow, or border.

## Forbidden

- Do not create bead or plastic texture.
- Do not add new elements.
- Do not redesign the composition.
- Do not use more than 8 total colors.
- Do not mix unrelated colors in the same region.
- Do not make the result look cramped.
- Do not preserve photographic-level details or copy every object detail from the source image. The result should look like a handmade rug / yarn artwork design, not a photograph covered with textile texture.

## Reference Images

The `references/` folder contains example before-after images that show the intended layout, color simplification, plush yarn texture, and soft natural edge treatment. Use them as visual guidance for style and material only. Do not copy their content into a user's image.

## Core Prompt

Use the provided reference image as the primary visual standard. Transform the user image into a simplified low-color artwork first, strictly limited to 6-8 total colors, then render it as a handmade yarn / rug / tufted textile artwork with soft fiber texture, unified color blocks, and a natural soft fuzzy edge. Keep the composition faithful to the original image, do not add new elements, keep the overall shape stable and near-rectangular, and do not introduce color noise or multi-tone gradients. Use a 1080x1620 vertical canvas with two centered 4:3 panels, each 920x690 px, with fixed margins and spacing. Place the original image on top and the finished artwork on the bottom. The bottom artwork should occupy about 84%-88% of the panel width, with comfortable white space, no shadow, no extra background, and a clean warm-white presentation. Create a soft textile surface with natural flowing fibers and uneven loose strands, while keeping the artwork edge stable with only subtle natural fiber outgrowth, not a regular fuzzy border.