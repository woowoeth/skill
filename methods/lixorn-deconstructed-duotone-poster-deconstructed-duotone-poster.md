---
name: deconstructed-duotone-poster
description: Deconstruct a supplied image, a text-only theme, or a source image plus a requested added subject into a spacious editorial duotone print. Support portrait 3:4 nine-square and vertical four-panel layouts, plus landscape 4:3 six-square and horizontal four-panel layouts, each with fixed coordinates, equal top/left/right paper margins, one shared exact-square tile template, and zero visible rectangular drift while retaining a faint inward hand-printed fringe. Use highly reduced flat masses rather than drawing, hatching, or photographic detail, with pale ivory paper, one user-chosen ink, stable flat fills, strong separate halation, restrained ink bleed, and a quiet lower footer with two tiny English typewriter lines plus subject-derived ultra-minimal icons. Use for image transformations, theme-only prompts, added subjects, wide-image adaptations, prompt-only or analysis-only output, and batch variations in this deconstructed visual family.
---

# Deconstructed Duotone Poster

Extract a small set of useful visual ideas and reinterpret them across one locked square-tile family: nine or four cells in portrait, or six or four cells in landscape. Let the panel set as a whole carry recognition: most cells may be abstract, while a few preserve restrained signature cues. Favor broad filled masses, negative-space cuts, mark rhythms, and material behavior over illustrated objects. Unless the user explicitly requests analysis or prompt-only output, generate and return a raster image.

## Route the request

- Use **Source Transform** when one or more supplied images provide the subject or scene.
- Use **Theme Compose** when the user supplies only words or a concept, such as “公路、沙滩和大海.” Do not ask for an image.
- Use **Source + Added Subject** when the user supplies a source and asks to introduce another specified subject. Accept either a textual subject or an additional subject-reference image.
- Use **Prompt-only** only when explicitly requested. Return the mode, selected layout, exact footer copy, cell plan, and final prompt without claiming generation.
- Use **Analyze-only** only when asked to explain the visual system. Do not generate.
- For multiple unrelated source images, default to one finished print per image. Combine them only when requested.

## Choose the layout

- Obey an explicit `3:4`, portrait, nine-grid, vertical four-panel, `4:3`, landscape, six-grid, or horizontal four-panel request.
- Use the portrait four-panel guide for an explicit vertical four-panel request and the landscape four-panel guide for an explicit horizontal four-panel request. The word “four-panel” overrides the default nine/six count while the requested orientation still controls the canvas.
- With no explicit ratio, use landscape `4:3` for a source image whose width is at least `1.15` times its height; otherwise use portrait `3:4`.
- Keep Theme Compose portrait `3:4` by default unless the user asks for landscape.
- In a mixed batch, route each source independently by aspect ratio unless the user requests one consistent layout.

## Load the references

- Read `references/request-modes.md` before resolving inputs and image roles.
- Read `references/visual-system.md` for every request.
- Read `references/interpretation-matrix.md` before planning the four, six, or nine cells.
- Read `references/prompt-compiler.md` for every generation or Prompt-only request.
- Read `references/quality-gate.md` before returning any image or prompt.

## Input contract

Require one user-chosen hue in every generation mode. Accept a color name or hex value. Normalize a broad name to one representative solid color and state it. If color is missing, ask only for the color.

Require either a usable source image or a text theme. In Source + Added Subject mode, require the added subject as a short description or reference image. Ask for a reference only when exact identity, character design, or product geometry matters and cannot be inferred safely.

If the user supplies footer copy, preserve it verbatim and break it naturally into exactly two left-aligned lines unless the user explicitly requests one line. Otherwise synthesize one short ASCII-English description from the semantic anchors: target 3–7 words and 12–32 characters, then choose and preserve one exact two-line break. Do not copy visible source text, brands, dates, or locations.

Always include the matching structural guide as a separate **structural layout reference** in image generation: `assets/layout-guide.png` for portrait `3:4` nine-square, `assets/layout-guide-vertical-4.png` for portrait vertical four-panel, `assets/layout-guide-4x3.png` for landscape `4:3` six-square, or `assets/layout-guide-horizontal-4.png` for landscape horizontal four-panel. A guide is not an edit target, subject source, or style reference. Require the model to follow its square positions and margins while redrawing all pigment edges organically. Never expose the neutral guide color in the finished palette or attach both guides to one generation.

When every target image has a local path, pass those paths plus the selected layout guide to image generation with `referenced_image_paths`. In Theme Compose, pass only the selected guide. When at least one semantic target exists only in recent conversation images, use `num_last_images_to_include` only if that mechanism can also include the guide; otherwise ask the user to attach the missing semantic image again so local paths can be used. Never use both image-input mechanisms. If neither includes every required image, ask the user to attach it again.

## Generation workflow

1. Route the request with `references/request-modes.md`. Label each image as source reference or added-subject reference.
2. Extract three to five semantic anchors. Select only two to four signature cues to preserve across the complete panel set; discard incidental components, literal lighting, construction detail, and photographic microdetail.
3. Build the selected cell count with `references/interpretation-matrix.md`: nine or four portrait cells, or six or four landscape cells. Give each cell one broad mass, void, gesture, or material rhythm. In four-panel layouts, require at least three abstract/material-led panels and at most one semi-literal cue panel. Use no more than one simplified scene fragment in any layout.
4. For Source + Added Subject mode, reserve two to four portrait cells or one to three landscape cells for the addition in nine/six layouts; in a four-panel layout reserve one or two panels. Do not paste the subject into every cell.
5. Choose the exact short English footer copy and its exact two-line break. Count the primary semantic subjects, then plan the footer icons with `references/visual-system.md`: exactly one icon for one subject; one icon per subject for multiple subjects, clamped to two through five.
6. Lock the palette to fixed pale ivory cream `#F7F1E3` plus the chosen solid ink. Use the chosen fixed coordinate system in `references/visual-system.md`. Treat the grid as one locked scaffold populated by copies of one shared square tile frame; never ask the image model to improvise separate frame shapes.
7. Compile one concrete prompt with `references/prompt-compiler.md`, then generate with the built-in image-generation tool. Attach only the matching structural guide. Label all other images by their semantic roles and explicitly state that the guide contributes geometry only.
8. Inspect with `references/quality-gate.md`. Regenerate once if the output ratio or cell count is wrong; the grid does not map to the selected fixed coordinates; the top, left, and right paper margins are not equal; any cell width/height differs by more than one output pixel after proportional scaling; the footer dominates; copy is not exactly two small left-aligned lines; subject-icon count or identity is wrong; cells become detailed illustrations or empty generic symbols; ink edges become cloudy or smeared; glow is weak; the paper is too dark; the palette gains a third hue; paper texture is absent; or footer text is unreadable.
9. Return the image, mode, layout, palette, exact footer copy, and a concise interpretation list matching the selected count of four, six, or nine panels. Include the final prompt only when requested or useful for revision.

## Batch discipline

Keep pale ivory cream, exact-square geometry, footer scale, flat-core/halo separation, and paper treatment identical across a batch. Keep the chosen hue identical unless the user assigns colors per item. Derive new anchors and a layout-appropriate cell plan for every item. Derive footer icons from each item’s actual subjects; never add arbitrary decorative geometry.

## Boundaries

- Do not paste, trace, collage, posterize, or reconstruct the original image.
- Do not require every cell to identify the source alone. Preserve only a few signature cues across the grid; let the remaining cells translate motion, material, contour, reflection, erosion, rhythm, or negative space.
- Do not render detailed equipment assemblies, repeated architectural openings, brick-by-brick paving, line-art construction, complete foreground/midground/background scenes, photorealistic volume, literal lighting, or dense microdetail.
- Do not use pencil, colored-pencil, etching, engraving, cross-hatching, contour hatching, stippled shading, fur strokes, feather strokes, leaf veins, surface scratches, or fine descriptive outlines. Recognition must come from a few large silhouettes and negative-space cuts.
- Do not reduce every cell to one generic logo-like mark. Keep controlled secondary rhythms and varied densities so the grid remains visually rich.
- Do not use razor-sharp pictorial vectors, brittle straight corners, hard clipped silhouettes, or repeated stock geometry. Keep a stable flat core, then use only a narrow printed transition and a separate luminous halo; do not dissolve shapes into fuzzy ink clouds.
- Do not let the added subject crowd every cell or erase the source-derived system.
- Do not add text outside the footer or arbitrary geometry in the footer. Use only the planned subject-derived icon or icons.
- Do not let paper texture, grain, or glow introduce a designed third color or obscure the grid.
- Do not simulate paper with uniform noise. Require fibers, pressed-pulp mottling, and absorbed ink.

## Output forms

For generation, return the raster first and one compact note with mode, layout, palette, footer copy, and the four, six, or nine interpretations. For Prompt-only, return the same plan followed by the final prompt and negative constraints. For Analyze-only, return fixed rules, mode variables, and failure directions.

## Examples

- “用 $deconstructed-duotone-poster 把这张照片做成浅蓝色九格图。”
- “用 $deconstructed-duotone-poster 把这张横图做成 4:3 浅绿色六宫格。”
- “用 $deconstructed-duotone-poster 做一张关于公路、沙滩和大海的砖红色图，不提供照片。”
- “用这张海岸照片，但额外加入一辆黄色敞篷车；主色仍用钴蓝。”
- “只给我最终 Prompt，底部英文写 ROAD, SAND AND SEA。”

