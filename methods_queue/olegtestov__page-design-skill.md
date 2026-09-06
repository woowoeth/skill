---
name: page-design
description: >-
  Design and build a single-file HTML page that looks deliberately designed —
  landing page, report, dashboard, explainer, prototype, poster, one-pager.
  Load it BEFORE writing the first line of markup or CSS, and before choosing
  fonts, colours or chart styling. Covers the light/dark token pattern that
  breaks most generated pages, typography, layout rhythm, chart legibility,
  the AI-generated looks to avoid, and the self-check discipline that stops
  you from burning a session re-screenshotting your own file.
---

# Page design

You are the design lead on a page that has to look chosen, not generated.
Everything here is the default; the user's own words outrank it.

## 1. Read the request first

| Question | What it decides |
|---|---|
| What kind of page? | document, dashboard, tool, marketing, teaching — different centres of gravity |
| Who reads it, on what? | type size, column count, tap targets |
| Read once or daily? | a one-time page can be bold; a daily one must be quiet |

## 2. Honour what already exists

Look for a design system before inventing one: `CLAUDE.md` / `AGENTS.md`, a
tokens or theme file, a Tailwind config, existing component CSS.

Precedence: **the user's words → the project's system → this file.** This file
fills gaps and never overrides the other two.

## 3. Ground the page in its subject

One concrete subject, one audience, one job.

Carry at least one detail only this subject would have — its real units, its
document conventions, its terms of art — as content, not decoration. Freight
pages use tonnes and lane codes; trial pages use arms and endpoints. That is
the difference between "a page" and "this page".

Real content throughout. Never lorem ipsum.

## 4. Typography

- **Name two faces in the plan**, one display and one text, paired deliberately.
  The display face is most of what makes a page look authored. System-only is
  legitimate for a dense internal tool — but then say so and say why, rather
  than arriving there by omission.
- **Declare a real fallback stack.** A `<link>` to Google Fonts or an inlined
  `@font-face` data URI; a silent fallback is a redesign you did not approve.
- Running text 60–75 characters per line. One type scale, held throughout.
- `text-wrap: balance` on headings, letter-spacing on uppercase labels,
  `font-variant-numeric: tabular-nums` wherever digits line up in a column.

## 5. Colour

- **Choose the neutral.** A pure mid-grey reads as unconsidered; bias it toward
  the accent hue. White and near-black are fine when the subject wants them.
- **One accent, spent in one place.** If it fights the ground, shift it toward
  an analogous hue or drop saturation — don't swap in another colour.
- Contrast floors: 4.5:1 body text, 3:1 large text and UI edges.

## 6. Both themes

The viewer has **three** states: explicit dark, explicit light, and the default
"system" setting, which stamps *no attribute at all*. Most viewers are in that
third state, where only `prefers-color-scheme` separates the themes.

**All three blocks below are required.** Bare `:root` plus the media query is
the common shortcut, and it looks right until someone flips a toggle the media
query cannot see.

```css
/* 1. Bare :root defines the COMPLETE palette. EVERY token starts here,
      including ones the dark block will redefine below. */
:root {
  --bg:      #fcfcfa;
  --surface: #ffffff;
  --fg:      #1a1a17;
  --muted:   #6b6b63;
  --line:    #e4e4dd;
  --accent:  #9a4a2f;
}

/* 2. System dark: tokens only, guarded so explicit light beats a dark OS. */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg:      #16161a;
    --surface: #1e1e23;
    --fg:      #ecece6;
    --muted:   #9b9b93;
    --line:    #2e2e35;
    --accent:  #e08a63;
  }
}

/* 3. Explicit dark: same tokens, so a toggle wins in both directions. */
:root[data-theme="dark"] {
  --bg:      #16161a;
  --surface: #1e1e23;
  --fg:      #ecece6;
  --muted:   #9b9b93;
  --line:    #2e2e35;
  --accent:  #e08a63;
}

/* 4. body paints its own ground; a transparent body borrows the host's. */
body { background: var(--bg); color: var(--fg); }
```

- **Define every token in the bare `:root` block before any media or
  `[data-theme]` block redefines it.** A colour defined only inside a theme
  block does not apply in the un-stamped state — the single most common broken
  page, one theme's text on the other's ground.
- Components read tokens, never literals, and take their colour from the same
  token set as the surface behind them.
- **A single-theme page is allowed** — a neon arcade screen, a letterpress
  invitation. Skip the media query and attribute blocks entirely, but still
  paint background and every colour explicitly. Make it a decision, not an
  omission.

Give the second theme the same care as the first; don't invert mechanically.

## 7. Layout

- **Layout does the spacing.** Sibling groups get flex or grid plus `gap`, not
  per-element margins that collapse or double.
- **Wide content gets its own scroller.** Tables, code, charts:
  `overflow-x: auto` on their container. The body never scrolls sideways.
- **Compose repeated things as one object.** Cards, label/value pairs, badges:
  identical padding and edges, aligned baselines, recurring elements in the
  same slot on every item.
- **Let content set the height**, and pick a column count the items fill —
  nothing stretched over dead space, nothing alone in a final row.
- Text that can outgrow its box wraps or scrolls. Clipped text is a bug.
- **A column header shares its cells' alignment.** A left header over
  right-aligned numbers leaves a dead gap and reads as a layout error. The
  cheap fix is one rule — `th { text-align: inherit }` plus alignment set on
  the column, or a `.num { text-align: right }` class put on both the `th` and
  its `td`s.

## 8. Not everything is a card

Border, fill, radius and shadow each announce "separate object". Spend them by
role, lifting the one element that needs it, instead of stamping one radius and
one shadow on every block until the hierarchy is wallpaper.

Lead with big-number tiles only when those numbers are the point of the page.

## 9. Charts

- **One scale** places marks, ticks and labels. Every axis label names a value
  the data reaches.
- Chart text reads from the theme tokens, so it works in both themes.
- Marks, labels and edges stay clear of each other and inside the drawing. In
  SVG: room in the `viewBox` for the outermost labels, explicit `fill` on every
  shape.
- **Title the finding, not the axes.** "Revenue doubled after the March launch"
  beats "Revenue by month".
- No truncated bar baselines, no dual axes chosen to make two lines cross.
- **Confirm the marks actually differ in the render.** `height: 67%` on a bar
  whose parent is auto-height never resolves: every bar collapses to the same
  stub with the correct number printed beside it, and the source looks right.
  Give the track an explicit height, use flex-grow, or draw in SVG.

## 10. Show the page at rest

The first still frame — what a thumbnail, a shared link and a skimming reader
get — already contains everything meant to be read.

- Nothing parked at `opacity: 0` waiting on an `IntersectionObserver`. Animate
  *from* a visible resting state, if at all.
- Size a hero to what it holds; a `100vh` opener pushes the page out of its own
  first frame.
- A tool opens in a plausible working state: real data where it exists,
  otherwise example rows plainly marked as examples, never passed off as the
  user's figures. An empty shell shows nothing.

## 11. Avoid the AI-generated look

| The cluster | The tell |
|---|---|
| Warm cream `#F4F1EA` + serif display + terracotta accent | "tasteful default" |
| Near-black with one acid-green or vermilion pop | "dark mode = edgy" |
| Purple-to-blue gradient hero on white | 2021 SaaS landing page |
| Inter or Space Grotesk as the safe face | no typographic decision made |
| Emoji as section markers | headings that couldn't carry themselves |
| Everything centred, one radius, one shadow, accent rail on every card | no hierarchy |
| Hairline rules and dense columns imitating a broadsheet | costume, not structure |

If the user asks for one of these, give it to them exactly — their words win.
When nothing is specified, don't spend that freedom on a default.

## 12. Build cleanly

- Close every non-void element; double-quote attributes.
- Visible keyboard focus. Respect `prefers-reduced-motion`.
- Watch selector specificity: two generated classes easily cancel each other's
  padding.
- Generative or decorative graphics → canvas or WebGL, not hand-authored SVG
  path data.
- External code: pin an exact CDN version, and put `<script src>` **before** the
  inline script using it.
- Assume the host may sandbox the page. Blocked resources fail *silently*, so
  inline CSS and embed small assets as data URIs.

## 13. Copy

- The title is a **name**, not a summary: two to four words, distinctive enough
  to pick out of a list of twenty.
- Every heading earns its line. If a section reads fine without it, cut it.
- Numbers carry units and a basis: "+12% (vs. Q2, same cohort)".

## 14. Process

1. **Plan in five lines**: subject, audience, the page's one job, the two
   typefaces, the palette, the one risk you are taking.
2. **Build from the plan**, deriving every colour and type decision from it.
3. **Write, look once, ship.** One look at the rendered page — one screenshot
   or preview — then one pass of edits for what it showed. On a page that
   charts real numbers, spend that look on the chart.

   No test loop around your own file: no repeated screenshots, no running the
   script through node, no DOM probes. That loop re-checks what a careful write
   already settled while the reader waits.

4. **No way to render?** Say so, then re-read for the four bugs that are
   invisible in source: chart marks that do not reach different sizes, colour
   tokens defined only inside a theme block, wide blocks without their own
   scroller, elements that start hidden.

5. **If a `check-page.py` ships beside this skill**, run it — it settles the
   rules a regex can decide and exits 1 on failure:

   ```
   python3 <this skill's dir>/../../tools/check-page.py page.html
   ```

   **Best-effort, never fatal.** Missing file, a sandbox that will not read
   outside the project, no python: skip it and say so. Do not glob the
   filesystem for it, and never let a refused permission end the task. It reads
   source, not layout, so a chart of identical marks passes clean — that is
   what the look is for. Fix every FAIL; answer every WARN.

6. **Publishing is not yours to decide.** The deliverable is the file. Do not
   push it to a host, enable GitHub Pages, or put it on a public URL unless the
   user asked in this conversation. Say where the file is and let them choose.

7. **Then stop.** The live page is the review surface. If the user reports
   something visibly broken, fix that one thing and ship again.

## 15. When the request is editorial

The client has already rejected everything that felt templated and is paying
for a point of view.

- **The hero is a thesis.** Open with the most characteristic thing in the
  subject's world.
- **Typography carries the personality**, not a neutral delivery vehicle.
- **Motion is deliberate or absent.** One orchestrated moment beats scattered
  effects; extra animation is itself a tell.
- **Match complexity to the vision.** Maximalist needs elaborate execution,
  minimal needs precision. Elegance is executing the chosen vision well.
- **Take one real risk**, in one place, and keep everything around it quiet.

## Final check

- [ ] Every token defined in bare `:root`; no colour lives only in a theme block
- [ ] `body` sets its own `background` and `color` from tokens
- [ ] Both themes legible; accent works on both grounds
- [ ] Nothing readable behind a scroll trigger; no `opacity: 0` at rest
- [ ] Wide content scrolls in its own container
- [ ] Repeated items share padding, edges, baselines
- [ ] Chart marks differ in the render; labels name values the data reaches
- [ ] Fonts have a fallback stack; external scripts pinned and ordered
- [ ] Focus visible; `prefers-reduced-motion` respected
- [ ] Real content, real units, no lorem
- [ ] Title is a short distinctive name
