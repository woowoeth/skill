---
name: dr-mona-posts
description: Design and export on-brand Instagram content for Dr. Mona Ali (psychiatrist, addiction & rehabilitation clinic) — static square/portrait posts, multi-slide carousels, and 1080×1920 reel covers, built as plain HTML/CSS and rendered to PNG with headless Chrome. Use whenever the user asks for an Instagram post, carousel, slide, reel cover, awareness-day graphic, CTA slide, or a re-render/recolour of one, or when they invoke /post, /carousel, /reel-cover, /recolour or /export. Also use it when the user attaches a reference image as design inspiration for a post.
---

# Dr. Mona — Instagram content

You are building publish-ready Instagram artwork for **@dr.monaalisardar** — Dr. Mona Ali,
psychiatrist, psychiatric & drug rehabilitation clinic. Plain HTML + CSS, no frameworks,
exported to PNG with headless Chrome.

The client reviews closely and is strict about fidelity. Everything below is either a
fixed rule or a documented judgement call that has already been litigated once.

---

## 1. Intake — what varies, what never does

**The background colour ("the ground") is the one required input. The user supplies it.**
Everything else — element placement, sizes, spacing, the type system — is fixed by this
skill. If no ground is named and no preset applies, **ask; never guess.**

Read a request into this contract. Ask only about fields marked *required*; infer or
default the rest and say what you assumed.

| Field | Required | Default |
|---|---|---|
| `format` | yes | — `static` · `carousel` · `reel-cover` |
| `topic` | yes | — the occasion, awareness day or subject |
| `ground` | yes | — a hex, or a preset name (§2). Ask if absent. |
| `size` | no | `1080×1080` static/carousel · `1080×1920` reel cover. `1080×1350` portrait allowed. |
| `slides` | no | 2 for a carousel (message + CTA). More only if the content genuinely needs it. |
| `headline` | no | you write it from `topic` — copy is in scope, not just layout |
| `row` | no | three glass cards; you propose the three beats |
| `mantra` / `closing` | no | one Caveat line, you propose it |
| `extra assets` | no | none — see §6 when the user supplies one |
| `reference` | no | none — an attached image or a named past post. Read `references/reference-images.md` when there is one. |
| `layout` | no | **you design it** — see §3. Only pinned if the user describes one. |
| `notes` | no | free text from the user; treat as additive constraints on top of the spec |

Anything the user adds beyond these fields is an **addition, not a replacement**. Fold it
in; never let it silently override a non-negotiable in §4 — if it collides, say so and
propose the nearest on-brand alternative.

**Copy is in scope.** The client expects headlines and card copy reconsidered and
improved, not poured into boxes verbatim.

---

## 2. The colour contract

The user gives one value: the **ground**. Two supporting tones are derived from it; the
rest of the palette is fixed and never varies.

```css
:root{
  /* ---- per-post input ---- */
  --ground:      #B8A9C9;  /* the canvas background                       */
  --ground-deep: #9B87B2;  /* same hue, lightness × 0.85 — background linework */
  --accent:      #4B3A61;  /* same hue, lightness ≈ .25, sat ≈ .25 — icons, rules, keylines */
  /* ---- fixed, every post ---- */
  --cream:    #FDFCF5;     /* logo, handle, type sitting on the ground     */
  --ink:      #2A2530;     /* headlines and card headings                  */
  --ink-soft: #514A5C;     /* body copy                                    */
  --panel: linear-gradient(152deg, rgba(253,252,245,.60) 0%,
                                   rgba(253,252,245,.32) 54%,
                                   rgba(253,252,245,.46) 100%);
  --pad-edge: 46px;
}
```

Derive the two tones with the bundled script rather than eyeballing them:

```bash
python3 scripts/derive_colors.py "#B8A9C9"
```

It prints a ready `:root` block and a contrast check. Named presets (`sage`, `cream`,
`lavender`, `clay`, `night`, `sky`) are built in — `python3 scripts/derive_colors.py sage`.

**Sage `#799D84` + cream `#F0EAE1` + ink is the core brand.** Gold, lavender and
terracotta accents were each proposed and rejected. Another hue is fine **only when the
user names it for that post** — and even then it is a *ground*, never a text colour.

Full rules, presets and dark-ground handling: `references/colour.md`.

---

## 3. The layout is yours to design — every time

**This skill does not ship a layout. It ships a frame and a set of invariants.** The
arrangement — the grid, the alignment, what the content row even is, where the eye lands,
how the air is distributed — is a fresh design decision for each post.

The failure this rule exists to prevent: every post coming out as a centred title over
three glass cards. That is one archetype among fourteen in `references/composition.md`,
and using it twice running is a defect, not a house style.

So, before writing any HTML:

1. **Read `references/composition.md`.** It carries the archetype catalogue, the eight
   variation axes, what makes a slide beautiful, and the critique pass.
2. **Look at the last two posts** of this format in `ready-posts/` — open the PNGs, not
   just the HTML. The new post must differ from them on **at least four** of the eight
   axes.
3. **If the user attached a reference image**, read `references/reference-images.md` and
   work from its structure. Take the composition; leave their colours, fonts, marks and
   wording.
4. **Write the composition down in about four lines before you code it** — anchor, focal
   point, support, field, air. That paragraph is the design; the CSS is transcription.

Then build it into `templates/frame-square.html` (or `frame-reel.html`), which carries the
invariants and a kit of primitives — glass, the four type voices, the illustration disc —
so the brand material is one line away and your effort goes into the arrangement.

`examples/` holds four finished slides. They are there to show what "done" looks like —
**read them for craft, never copy their layout.**

---

## 4. Non-negotiables

These have all been enforced in review. Do not trade any of them away for fit.

- **Handle `@dr.monaalisardar` sits bottom-left on every slide.** Never top, never
  centred, never moving between slides of one carousel.
- **Swipe cue is a bare 200px arrow**, bottom-right, on carousel slides `1 … N-1` only.
  No "SWIPE NEXT" text, no pagination dots, no `DM` monogram.
- **The occasion outranks the slogan.** The topic or awareness day is the largest thing
  on the slide; a mantra is support.
- **One idea per canvas.** A slide carries a title and *one* body of content — one row,
  one list, one panel, one statistic. A CTA does not fit alongside that; a post needing
  both is a two-slide carousel. ("Too much bloated" was the verdict on the dense version.)
  **Split rather than compress** — this is a density rule, not a layout: how that one body
  of content is arranged is yours to design.
- **Use the client's CTA artwork** (`assets/cta/`), never a typeset substitute. Never
  overwrite `cta.png`; recolouring writes a new sibling file.
- **Never use a placeholder for contact data.** Always
  `MON-SAT | 6:00 – 9:00 PM`, `0315-7090609`, `MBBS, MD, MRCPsych(UK)`.
  Briefs that supply `dr-mona.com` or `1-800-…` are ignored in favour of these.
- **Glass panels, not opaque ones** — and never both on the same slide.
- **Type is never set in the accent hue on the ground.** Headlines `--ink`, light type
  `--cream`; the accent is for icons, rules, keylines and script accents.
- **Fonts:** Playfair Display (display, roman + italic) · Caveat (script accent, used
  sparingly) · Poppins (everything else).
- **Larger type is almost always the right call** — this has been asked for repeatedly.
  When something does not fit, buy space from spacing and layout, never from font sizes.
- **Her photo is never the centrepiece.** A big centred portrait cutout reads as cheap —
  she belongs in a small medallion or inside the CTA artwork.
- **Never delete or overwrite a file the user supplied.** Derive a new sibling file.

Note what is *not* on this list: the grid, the alignment, the arrangement of the content,
the background artwork, the ornament, the density. Those are design decisions (§3) and
they should be different on every post.

---

## 5. Build sequence

1. **Resolve intake** (§1). Ask only for the ground if it is missing.
2. **Derive the palette** — `python3 scripts/derive_colors.py <ground>`.
3. **Read the format recipe** — it carries what that format constrains, not a layout:
   - static post → `references/static-post.md`
   - carousel → `references/carousel.md` (+ `references/cta-slide.md` for the last slide)
   - reel cover → `references/reel-cover.md`
   - the invariant furniture and the type scale → `references/layout-map.md`
4. **Design the composition** (§3) — `references/composition.md`, plus
   `references/reference-images.md` if the user attached one. Look at the last two posts,
   choose an archetype that differs from them on four axes, and **write the four-line
   composition note before you code.**
5. **Write the copy** — `references/copy-voice.md` (tone, and the safe-messaging rules
   that are requirements, not taste, on suicide/self-harm/addiction topics).
6. **Build** — copy `templates/frame-square.html` (or `frame-reel.html`) into the output
   folder and write your composition into the COMPOSE regions. The frame carries the
   invariants and the primitives; the arrangement is yours.
7. **Render and look at it.** `python3 scripts/render.py <file.html>`, then **Read the PNG**
   and crop in at full resolution to check type and edges.
8. **Critique and revise.** Run the five questions in `references/composition.md` §7, fix
   the weakest thing, and re-render. **At least one revision pass, always** — the first
   render is a draft. Never report done on an unrevised first render.
9. **Check against §4 and `references/gotchas.md`** before handing over.

### Output folder — no exceptions

```
ready-posts/YYYY-MM-DD/post-NN-topic/     # static posts and carousels
  slide-01.html  slide-02.html
  output/slide-01.png  slide-02.png       # 2160 × 2160

reels/YYYY-MM-DD/reel-NN-topic/           # reel covers
  cover.html
  output/cover.png                        # 2160 × 3840
```

`NN` is zero-padded and counts within that date folder. The frames in `templates/` and the
finished slides in `examples/` are references — never publish either directly.

---

## 6. Assets

Everything ships with this skill under `assets/`. Reference them with a relative path from
the slide file (`../../../` from `ready-posts/YYYY-MM-DD/post-NN/`) or copy the ones you
need into the post folder.

| Need | File |
|---|---|
| Logo mark on a coloured ground | `assets/logo/logo-cream-mark.png` |
| Logo mark on glass / light | `assets/logo/logo-plum-mark.png` — **plum/lavender grounds only**; otherwise `python3 scripts/tint_logo.py "<accent>"` |
| CTA artwork (client's own) | `assets/cta/cta-plum-trimmed.png` — 1820×440, aspect 4.136 |
| CTA artwork, sage variant | `assets/cta/cta-trimmed.png` |
| Portrait medallion | `assets/photos/dr-mona-avatar.png` (640px circular) |
| Line icons · decorative shapes | `assets/icons/*.svg` · `assets/graphics/*.svg` |

**When the user supplies an extra asset** (a photo, an illustration, a new logo lockup):
put it in the post's own `assets/` folder, reference it relatively, and grade it to the
ground — a raw full-colour photo on a tinted field breaks the palette. The duotone recipe
is in `references/reel-cover.md`. Never modify the original in place.

To re-tint the CTA strip: `python3 scripts/retint_cta.py <hex>` — it writes a **new**
sibling file. **Tint the strip and the logo mark to the post's `--accent`, not to the
ground** — the glass panel is a pale version of the ground, so a ground-tinted strip
washes out on it. Full pipeline and the traps in `references/assets.md`.

---

## 7. Export

```bash
python3 scripts/render.py path/to/slide-01.html          # → output/slide-01.png at 2×
python3 scripts/render.py path/to/*.html                 # a whole carousel
python3 scripts/render.py cover.html --height 1920       # reel cover
```

2× device scale — square lands at **2160 × 2160**, portrait 2160 × 2700, reel 2160 × 3840.
The script finds Chrome on macOS, Windows and Linux and needs nothing but Python 3.

The templates keep their preview padding behind a `@media (min-width:1200px)` guard, so a
headless window sized exactly to the canvas produces an exact screenshot with no crop
step. **Hand-built older files with unconditional `body{padding:40px}` must use the
inflate-and-crop route instead** — `scripts/render.py --legacy-crop` does it. The reason:
with `--window-size` equal to the canvas, an overflowing centred canvas makes Chrome
silently clip ~40px off every edge.

---

## 8. References

| File | Read it when |
|---|---|
| `references/composition.md` | **always, before writing any HTML** — archetypes, variation axes, what makes it beautiful, the critique pass |
| `references/reference-images.md` | the user attached a design reference |
| `references/layout-map.md` | always — the invariant furniture, the type scale, the glass recipe |
| `references/static-post.md` | building a single post |
| `references/carousel.md` | building a carousel |
| `references/cta-slide.md` | building the closing slide |
| `references/reel-cover.md` | building a reel cover |
| `references/colour.md` | choosing/deriving a ground, dark grounds, presets |
| `references/assets.md` | logos, CTA re-tinting, cut-outs, adding new assets |
| `references/copy-voice.md` | writing the words; safe-messaging requirements |
| `references/gotchas.md` | before reporting anything done |
