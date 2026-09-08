---
name: travel-memory-sticker-pack
description: "Turn one or multiple travel, street, landscape, lifestyle, portrait, or pet photos into one portrait 3:4 packaged printable PNG with a sealed header and exactly twelve source-derived die-cut stickers: three simplified scenic stickers and nine true irregular silhouette stickers, rendered in low-saturation deliberately clumsy flat gouache/cut-paper style."
---

# Travel Memory Sticker Pack

Create one portrait packaged sticker sheet from one photo or a shared pool of multiple related photos. Default to a sealed header plus exactly twelve illustrated stickers on a pale warm-ivory printable background.

The default visual language is the same selective-memory language as `travel-memory-sticker-card`: blunt matte color masses, awkward hand-cut silhouettes, quiet negative space, and deliberately non-realistic simplification. Do not make miniature paintings or photo-like sticker panels.

## Workflow

1. Inspect every source photo. Inventory its emotional center, main subject, actions, relationships, place cues, useful objects, compact silhouettes, and source-native colors.
2. Build one cross-photo motif pool and remove near-duplicates before choosing exactly twelve motifs.
3. Allocate the twelve slots using the fixed shape mix below: exactly three simplified scenic stickers and exactly nine true irregular silhouette stickers.
4. Read [references/style-guide.md](references/style-guide.md), then generate one upright portrait `3:4` sheet with a sealed header occupying roughly `13–15%` of the height.
5. Inspect the generated PNG. Count the stickers, verify the canvas ratio, check the `3 + 9` shape mix, and reject photographic or painterly rendering. Regenerate once when any invariant fails.
6. Save the final project-bound PNG in the workspace. Use transparency only when the user explicitly requests it.

## Source selection and de-duplication

- Treat all uploaded photos as one source collection. Select exactly twelve motifs total, never twelve per photo.
- Represent each materially distinct source photo where possible, but do not allocate equally when one photo has stronger motifs.
- Prefer different narrative roles: main subject, action, relationship, pet, functional object, environmental form, structural fragment, atmospheric cue, and one place anchor.
- One visible pair or group is one sticker when the relationship is the motif.
- Reject near-duplicates even when they come from different photos. Similar portraits, repeated viewpoints, repeated held objects, or the same landmark at a different scale do not earn separate slots.
- If a main subject already contains an object, do not automatically repeat that object as a standalone sticker. Repeat only when its silhouette or narrative role changes materially.
- Use only visible or strongly implied source content. Never invent filler, souvenirs, food, animals, vehicles, or decorative wedding/travel icons.
- Preserve people through silhouette, hair, eyewear, clothing blocks, pose, and relationship. Keep faces absent or extremely minimal.
- Preserve pets through species, coat-color blocks, pose, and proportions, not fur realism.
- Retain at most one truly central venue or place name, exactly once, only when it materially identifies the memory. Remove all other incidental text, labels, prices, signs, signatures, and watermarks.

## Fixed sticker shape mix

The sheet must contain exactly twelve stickers below the header:

- **Exactly three simplified scenic stickers.** Use only the three strongest spatial memories. Their outer edges must be loose hand-torn or source-shaped contours, never rectangles, rounded rectangles, cards, frames, windows, or miniature postcards.
- **Exactly nine true irregular silhouette stickers.** The warm-white border must closely follow the subject or grouped motif: person, animal, bird group, vehicle-plus-signal, lamp, tree pair, rock cluster, building row, bouquet, or another source-native form.

Do not solve a landscape-heavy source set by turning every photograph into a rounded-square scene. If a motif can be separated from its background, make it an irregular silhouette sticker.

## Packaged printable composition

- Default canvas: exact upright portrait `3:4`, width:height = `3:4`, visibly taller than wide.
- Default header: one inset horizontal sealed retail head card near the top, targeting `14%` of total canvas height and allowing only `13–15%` generation tolerance. Preserve a narrow, deliberate warm-ivory paper edge matching the `JEJU DAYS` reference proportions: top margin about `1%` of canvas height and left/right margins each about `1.7%` of canvas width. The three outer margins must look thin, uniform, and intentional; do not make them wider, unequal, absent, or convert them into a full surrounding frame. Keep square, softly hand-cut outer corners rather than rounded retail-card corners, and add no shadow. Include exactly one centered horizontal hang slot and exactly two small horizontal metallic staple marks: one in the left outer quarter and one in the right outer quarter, aligned on the same baseline. Never omit, multiply, center, stack, or replace the two staples with dots, folds, holes, or decoration. The main ivory sticker area begins directly below the header.
- Derive the header fill from one quiet, identity-bearing dark or mid-dark source color. Prefer the deepest recurring environmental color, such as mineral blue, smoky indigo, forest green, brown-black, brick, or another subdued place-native hue. Do not use the brightest accent, pale background color, arbitrary black, unrelated brand color, gradient, pattern, or multicolor header. Keep it visually subordinate to the stickers but dark enough for warm-ivory title text to remain clearly legible. For ambiguous source sets, choose the darkest calm color from the dominant scene rather than from a small object or outfit. Use one short source-derived title and tiny `12 PIECES`. The header is packaging, not a sticker, and does not count toward twelve.
- Arrange the twelve stickers below in an airy three-column/four-row rhythm with uneven scale hierarchy. Do not use a rigid equal-cell catalog grid.
- Keep every sticker fully visible, separated, uncropped, and individually contour-cuttable.
- Give every sticker a thick, slightly irregular warm-white die-cut border. Do not add external cast shadows.
- Default background: uniform opaque pale warm ivory near `#F5F1E8`, distinct from the warm-white cut borders. Deliver RGB PNG.
- Transparent mode is allowed only when explicitly requested; preserve opaque warm-white borders and Alpha 0 outside them.
- Do not add labels, captions, keywords, legends, numbers, dates, decorative confetti, signatures, or watermarks below the header.
- Override the ratio, packaging, title, background, count, or style only when the user explicitly requests a different output.

## Non-negotiable quality checks

- PNG is an upright `3:4` image unless explicitly overridden.
- One sealed header is at the top and is clearly separate from the sticker area.
- The header preserves the fixed narrow paper edge: approximately `1%` top margin and `1.7%` left/right margins, all in the same warm ivory as the sticker area. No additional outer frame or enlarged gutter appears.
- The header contains exactly one centered hang slot and exactly two symmetrically balanced staple marks, one left and one right.
- Exactly twelve sticker objects appear below the header.
- Exactly three are simplified scenic stickers and exactly nine are true irregular silhouette stickers.
- No sticker is a rectangular or rounded-rectangular miniature photograph/postcard.
- First read is broad flat shapes and quiet space, not detail, realistic lighting, or photographic texture.
- Motifs are distinct in silhouette and narrative role; no repeated portrait or repeated landscape filler remains.
- Every motif is traceable to the source collection.
- No sticker is cropped, touching, accidentally merged, or duplicated.
- No unintended readable text, watermark, signature, or decorative filler remains.

## Delivery

Show the finished image and provide one file link labeled `十二枚旅行贴纸 PNG`. Briefly name the three scenic stickers and nine irregular stickers, and report the saved path. If transparency was explicitly requested, state that Alpha was validated.
