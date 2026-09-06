---
name: logo-material-explorer
description: Use when a user wants to turn a flat logo, wordmark, monogram, or brand mark into a dimensional 3D material study, compare extrusion geometry, or apply a supplied or built-in surface reference while preserving brand identity.
---

# Logo Material Explorer

Transform one clear flat logo into a controlled C4D-style material study. Protect identity by separating geometry approval from material rendering.

Precedence: original logo identity is highest; explicit user text decides material tradeoffs; a supplied reference contributes observable surface traits. A built-in asset never overrides either.

## Required Flow

1. Inspect the logo. If it is blurred, obscured, strongly distorted, or contains multiple unidentified marks, request a clearer single target. Do not infer hidden geometry.
2. Ask the user to choose `Free material exploration` or `Use uploaded material references`. When the user names a specific material, proceed directly to the clay comparison sheet; defer the exploration-mode choice until after geometry approval.
3. Read [prompt-recipes.md](references/prompt-recipes.md) and generate one A/B/C clay comparison sheet.
4. Before presenting it, validate the clay sheet. If it alters the logo identity, its A/B/C labels are missing, duplicated, unreadable, or incorrect, or it contains any extra added text, regenerate it instead of presenting it.
5. Show the valid clay sheet and ask the user to choose A, B, C, or request an adjustment. If the user requests an adjustment, regenerate the clay sheet and repeat the same validation and A/B/C selection gate.
6. Stop at this gate. **Do not generate the final material render before the user selects A, B, or C.**
7. After geometry approval:
   - For free exploration, read [material-library.md](references/material-library.md), offer at most four suitable directions, and wait for a selection. When offering four options, choose from at least three material families when the logo and user intent allow; prioritize identity-safe materials for thin strokes, small counters, and tight gaps.
   - For uploaded references, analyze visible surface scale, roughness, reflectivity, softness, seams, texture, colors, and highlight shape. A user-supplied reference takes priority over the built-in library.
   - If the user named a specific material before the clay stage, treat it as already selected after A/B/C approval: use an uploaded reference if supplied; otherwise map it to a clearly matching built-in asset (for example, metallic inflated nylon maps to Metal and fabric). If no close built-in match exists, retain the exact description and ask whether to proceed text-only or upload a reference. Never ask the free-vs-uploaded entry choice again for an already named material.
8. Generate the final image from the original logo, approved geometry, and chosen material reference. Show the image, then state the selected geometry, material name, and two or three visible material traits.

## Identity Rules

- Preserve the outer contour, internal letterforms or symbols, negative space, spacing, and proportions.
- Do not redesign, stretch, twist, melt, or reinterpret the logo.
- Texture may add fine relief, folds, fibers, seams, or crystals, but may not close counters, cut through key strokes, or change the silhouette.
- When material detail conflicts with recognition, simplify the material detail and disclose that choice.

## Image Input Rules

- If every source image has a local path, pass the original logo, approved clay sheet, and material reference through `referenced_image_paths`.
- If any required target exists only in recent conversation images, first expose every local-only target via `view_image`, then use `num_last_images_to_include` with the smallest value that includes every required source, up to five.
- Never use both image-input mechanisms in one generation call.
- If every required source cannot be included within that five-image limit, ask the user to reattach missing sources before generation.
- For the clay sheet, include only the original logo. For the final render, include all three source roles when available.

## Output Rules

- Clay sheet: one image with three clearly separated candidates on a pure black background, using controlled C4D studio treatment (upper-left/front key, right rim, bevel highlights, and ambient occlusion). The only permitted added text outside the source logo is a small readable A, B, or C beside its candidate. Source logo lettering must remain unchanged.
- Final render: one logo centered slightly high, about 55–65% of the image width, pure black background, generous negative space.
- Use controlled studio lighting, visible sidewalls, clean bevel highlights, and ambient occlusion.
- Exclude floors, grids, captions, labels, explanatory text, watermarks, and extra objects from the final render.
