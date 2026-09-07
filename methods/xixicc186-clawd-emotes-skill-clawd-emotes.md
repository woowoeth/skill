---
name: clawd-emotes
description: >-
  Create original pixel-art "Clawd" crab emotes as pure SVG + CSS keyframe
  animations (no frame-by-frame GIFs, no raster sprites), and optionally export
  them to looping GIFs. Each emote is a tiny pixel crab doing an activity —
  holding a prop, wearing a hat, reacting — built from <rect>/<polygon>/<circle>
  and animated with @keyframes. Use this skill whenever the user wants to make,
  add, fix, or extend Clawd / pixel-crab / desk-pet emotes, mascot animations,
  "表情/图鉴" cards of an animated character, festival or daily-life crab
  stickers, or asks to turn such SVG animations into GIFs — even if they don't
  say the word "SVG". Also use it when fixing visual bugs in these emotes
  ("帽子悬空/hat floating", "脚断开/feet detached", a prop that looks
  disconnected from the hand), since the fixes follow specific structural rules
  documented here.
---

# Clawd pixel-crab emotes

Build a cast of tiny animated pixel crabs, each doing something (eating, gaming,
celebrating a holiday, playing guitar…). Every emote is **one inline `<svg>`
animated entirely with CSS `@keyframes`** — no GIF frames, no external images.
Many emotes live together as cards in one HTML "图鉴" (catalog) page.

This approach is loved because it's tiny, crisp at any zoom (`image-rendering`
stays sharp), trivially themeable, and editable as plain text. The cost is that
the crab's body is a fixed pixel grid, so **placement is everything** — most
"bugs" are an element drawn at the wrong coordinate or in the wrong group.

## The workflow

1. **Pick the activities.** One emote = one clear action. Decide the prop, the
   hat (if any), and the one "hero motion" that sells it (a sip, a strum, a
   blink-and-bob). Keep it readable at 150×150 px.
2. **Copy the scaffold.** Start each page from `assets/card-template.html` — it
   has the shared `<style>` block, the grid, and one fully-built example card.
   Each new emote is one `<div class="card">`.
3. **Build the crab, then layer.** Drop in the base anatomy (see
   `references/anatomy.md`), give it a unique prefix, then add eyes/arms,
   the prop, the hat, and particles — in that draw order.
4. **Animate the hero motion** plus idle life (blink, bob, shadow). Use the
   transform-origins from the anatomy reference; a wrong pivot is the #1 cause
   of parts flying off.
5. **Verify visually — always.** Render with headless Chrome and actually look
   at every emote (`scripts/check.py`). This is non-negotiable: pixel art lies
   in the source and only the render tells the truth. Fix floating hats,
   detached feet, and disconnected props.
6. **Export to GIF only if asked** (`scripts/export_gif.js`).

## The five rules that prevent every common bug

These come from real bugs hit while building the existing sets. Internalize them
and you avoid almost all rework.

1. **Feet live *inside* the animated body group.** The shadow is separate and
   stays on the ground; everything that is part of the crab — feet included —
   goes inside `<g class="XX-body">`. Feet drawn outside the group don't share
   the body's transform, so the body bobs/tilts away and the feet "detach." This
   is structural: feet inside the group *cannot* detach.

2. **A hat's brim must sit on the torso top (y≈6), not float above it.** After
   drawing a hat, compute the y of its lowest edge and confirm it reaches ~6. If
   there's a gap, the hat floats. Lower the whole hat and set its
   `transform-origin` near the contact point (e.g. `7.5px 6px`) so any wobble
   pivots from the head, not from empty space.

3. **A prop held by a moving arm goes *inside that arm's group*** and pivots at
   the shoulder. If the prop is in a different group than the hand, the hand
   moves and the prop stays — it looks disconnected. Chopsticks, brushes, mics,
   watering cans: all nested in the arm `<g>`.

4. **Long props need gentle rotation.** Rotation moves a point by roughly
   `radius × angle`. A long prop far from its pivot sweeps a huge arc, so a big
   keyframe angle flings it off-crab. Either keep the swing small (±10–15°) or
   move the pivot closer to the prop. (The original eating-crab bug: chopsticks
   far from the shoulder on a −52°→24° swing — they detached visually. Fixed by
   anchoring them to the hand and softening to −13°→3°.)

5. **Every inline SVG needs a unique class/keyframe prefix.** All the cards share
   one document, so global CSS names collide. Prefix everything per emote
   (`bd-` birthday, `cf-` coffee, `gm-` gaming…): `.cf-body`, `@keyframes
   cf-sip`. Reusing `body`/`blink` across cards makes animations bleed between
   crabs.

## Draw order (z-order) matters

SVG paints in document order. Within the body group, the reliable layering is:

```
shadow (separate, on the ground)
└ body group:
    feet → torso → screen-glow/face-tint → arms → eyes → mouth
    → hat (on top of head)
    → particles that belong behind the prop
    → foreground prop (mug, bowl, laptop, camera…)  ← drawn last so it overlays
```

Foreground props (a mug, a laptop, a bowl) are drawn *after* the face so they
sit in front of the body — but keep the eyes above the prop's top edge so the
crab can still "look." When a prop must cover the face (a camera up to the eye),
that's intentional; add a hint of expression elsewhere (a little smile below).

## Reference files — read these when you need them

- **`references/anatomy.md`** — the base crab geometry (every coordinate),
  transform-origins for each part, the standard idle animations, the per-card
  theming variables, and ready-to-paste snippets. **Read this before building
  your first crab**; it's the source of truth for placement.
- **`references/prop-recipes.md`** — a catalog of props and hats already built
  (24 emotes: festivals, daily life, hobbies) with the technique each one uses
  (held prop, rotating tool, floating screen, particles, headwear). Skim it for
  patterns and to avoid re-deriving solutions.

## Verifying

Run `python3 scripts/check.py <file.html>`. It:
- validates each SVG is well-formed (catches missing spaces between attributes
  like `style="..."x="..."`, unescaped `&`/`<`, etc.),
- renders the page with the locally cached/headless Chrome,
- saves a full screenshot and one crop per card under `/tmp/clawd-check/`.

Then **read the crops** and check each crab against the five rules: hat on the
head? feet attached? prop connected to the hand? face readable? If a browser
extension or live server is flaky, this headless path is the dependable way to
see the result — never report an emote "done" without looking at a render.

## Exporting to GIF (only when the user asks)

`node scripts/export_gif.js <file.html> <out-dir>` produces one looping GIF per
card. It drives Chrome over CDP and steps each CSS animation deterministically
via `document.getAnimations()` (pause, set `currentTime` per frame) rather than
capturing in real time — this guarantees a clean, seamless loop. Frames are
piped through `ffmpeg` palettegen/paletteuse for crisp pixel colors. See the
header comment in the script for the per-card loop-period list and tunables
(fps, size, deviceScaleFactor). Requirements: Node, `puppeteer-core` (or a
Chrome path), and `ffmpeg` on PATH.

### Transparent GIFs

`node scripts/export_transparent.js <file.html> <out-dir>` exports each card to a
GIF with a **transparent background** (named `clawd-<tag>.gif`). The key steps:
strip the cards' CSS backgrounds in-page, screenshot each `<svg>` with
`omitBackground:true` so the empty area is truly transparent, then encode with
`ffmpeg palettegen=reserve_transparent=1` + `paletteuse=alpha_threshold`. Do NOT
color-key the background away — the crab's eyes and shadow are also black and
would be deleted; re-rendering from the source keeps them while clearing only
the empty background. The loop period per card is auto-detected from its longest
CSS animation.
