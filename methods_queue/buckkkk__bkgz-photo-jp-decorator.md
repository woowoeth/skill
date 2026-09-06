---
name: bkgz-photo-jp-decorator
description: Transform a user-supplied photo into a relaxed summer-inspired instant-film image with a classic white border, carefully placed Japanese Mincho-style vertical text, and delicate handwritten lettering in the border. Use for Polaroid-like, instant-photo, Japanese photo-card, 日系拍立得, or Japanese-captioned photo treatments. Do not use for text-only translation or unrelated image edits.
---

# BKGZ Photo JP Decorator

Create a finished bitmap that keeps the source photograph recognizable while adding an airy summer instant-film look and a two-voice Japanese typography system: prominent Mincho-style vertical text carefully composed in the photo's negative space and delicate handwritten lettering in the white border.

## Required outcome

- Preserve the subject's identity, pose, expression, body proportions, important objects, and overall scene truthfulness.
- Preserve the source orientation. Do not crop important content; extend the canvas for the border when needed.
- Use a classic instant-photo border: narrow white margins at the top and sides and a visibly deeper bottom margin.
- Place exactly two short Japanese Mincho-style vertical columns over a genuinely quiet part of the photo. Preserve visible thick-thin stroke contrast and an editorial travel-postcard feeling. The text may be prominent, but it must not cover or visually cut into the main subject, face, body silhouette, hands, held objects, animals, food, signs, or other focal details.
- Add one separate Japanese handwritten decoration in the white border, normally in the bottom margin. Keep this lettering visibly thinner, lighter, and more understated than the photo-area text so it reads as a finishing note rather than a headline.
- Deliver a high-resolution final image and leave the source untouched.

## Workflow

1. Inspect the source image before editing. Identify the primary subject and its complete silhouette, face, hands, held objects, secondary focal details, quiet negative space, orientation, lighting, season, location cues, and emotional tone. Mentally reserve a clear exclusion zone around the subject before choosing text placement.
2. Choose `warm`, `cool`, or `vivid`. Prefer `vivid` for daylight, greenery, travel, play, movement, or summery scenes; use `warm` for gentle late-afternoon nostalgia and `cool` only for clearly calm or cinematic scenes. If uncertain, use `vivid`.
3. Write concise, natural Japanese based on visible content and mood. Default to breezy, conversational fragments with a summer-day, off-duty, playful, or leisurely feeling rather than formal literary phrasing.
4. Apply only a restrained film treatment: gentle tonal curve, slightly softened highlights, subtle color cast, modest grain, and no conspicuous artificial blur. Do not regenerate or beautify people.
5. Add the border and typography deterministically with `scripts/render_instant_photo.py`. Do not ask an image-generation model to render the final Japanese characters.
6. Inspect the result at full image and close-up scale. If photo text overlaps the subject or important objects, move it to another negative-space region before changing its size. Shorten copy or reduce size only when no clean position exists. Revise any border lettering that feels heavy or headline-like.

## Japanese copy rules

- The two photo-area columns should each be short: approximately 3–8 Japanese characters, excluding punctuation. Shorter copy supports the larger type.
- Prefer relaxed, image-specific wording such as spoken fragments, sensory observations, or light action phrases. Favor kana where natural to soften the voice. Avoid stiff slogans, solemn declarations, four-character idioms, forced quotations, clichés, and machine-like translation.
- Let the pair feel like an easy summer note: sunlight, breeze, shade, fruit, a detour, a break, or unhurried movement when those cues are genuinely visible. Do not force summer references onto winter or indoor scenes.
- Keep grammar, kana, kanji, and punctuation correct. Never invent pseudo-Japanese glyphs.
- Avoid claims about a person's identity, relationship, location, date, or feelings unless the user supplied them or they are unambiguous.
- Keep the border decoration shorter than the combined photo text. A brief phrase or user-provided date is suitable.
- Default to Japanese only. Add English or a date only when requested or clearly appropriate.
- Japanese vertical writing reads in columns from right to left. Pass the first reading column as `--line1`; the renderer places it to the right of `--line2`.

## Placement rules

- Prefer genuine negative space such as open sky, a plain wall, water, pavement, or defocused background. Choose the region that balances the subject and existing visual weight; do not place text mechanically at a fixed edge.
- Select `--side left` or `--side right` only after inspecting the image. Use explicit `--x` and `--y` whenever they produce a more balanced composition. Check the full height and width of both columns against the subject exclusion zone, not just the starting point.
- Maintain breathing room from the crop and border. Photo-area text may interact lightly with background texture but must not cross the main subject silhouette. If both edges are occupied, try upper or lower negative space, shorten the copy, reduce `--font-scale`, or omit a less important phrase rather than covering the subject.
- Use dark ink on light areas and light ink on dark areas. Keep outlines subtle so the Mincho stroke character remains visible; choose a calmer background area instead of using a heavy poster-like outline.
- Do not place the photo-area text inside the border; the border decoration is a separate element.

## Rendering

Run:

```powershell
python scripts/render_instant_photo.py INPUT OUTPUT --mode vivid --line1 "風がきもちいい" --line2 "ちょっと寄り道" --border-text "夏のひと休み" --side right
```

Useful options:

- `--mode auto|warm|cool|vivid`
- `--side left|right`
- `--x` and `--y` for explicit photo-relative placement in the range 0–1
- `--ink auto|dark|light`
- `--font` for a specific Japanese-capable `.ttf`, `.ttc`, or `.otf`
- `--border-font` for a separate Japanese-capable light handwritten or calligraphic font in the white border
- `--border-font-scale` to tune the restrained white-border note independently; `1.0` keeps the deliberately smaller, lighter default
- `--font-scale` to tune the oversized default photo text; `1.0` is the bold high-visibility default

For photo text, prefer a Japanese Mincho or other CJK serif font with clear thick-thin contrast. For border text, prefer a light handwritten, pen, or restrained calligraphic font rather than a heavy brush display face. The renderer selects these two families independently. If better fonts are installed, pass them with `--font` and `--border-font`. Never use a font that renders tofu boxes.

## Quality bar

- Check that all requested Japanese text is present, readable, correctly ordered, and free of substitution glyphs.
- Check that the two treatments remain distinct: refined, visible Mincho columns in the photo and a thinner, quieter handwritten note in the border. The border note must not compete with the image or feel bold.
- Check the complete bounding area of both photo columns. No glyph may cover the main subject, face, hands, held objects, or another important focal element; placement must look compositionally intentional rather than merely technically clear.
- Check that the border is neutral-to-warm white rather than pure digital white.
- Check that grain remains subtle and facial skin is not muddied.
- Check that no source file was overwritten.
- If a safe two-column placement is impossible, prioritize the subject: reduce size, shorten the copy, or choose a safer position rather than forcing the layout.
