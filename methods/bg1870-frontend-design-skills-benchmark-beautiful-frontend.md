---
name: beautiful-frontend
description: This skill should be loaded whenever the agent is about to write browser-rendered visual output — landing/marketing/pricing pages, dashboards, product UI, clickable prototypes, or visual additions to an existing site — and the bar is work that looks art-directed rather than AI-generated. It forces a committed art direction before any code and replaces autopilot patterns with concrete typographic, color, layout, and motion decisions. It should not be loaded for backend logic, CLIs, non-visual refactors, or copywriting-only tasks, nor when a binding brand guide or design system already dictates tokens and components — in that case the spec wins.
---

# Beautiful Frontend

## 1. Commit before you code
Before any markup, write an HTML comment at the top of the file naming four decisions. If you cannot name them, you have not decided.

- **Register** — the aesthetic world, derived from the brief's subject and audience: editorial, technical, brutalist, warm-consumer, or luxe-dark. Choose what the brief implies. Dark-mode-with-glow is your habit, not a decision; treat it as last resort.
- **Palette** — one surface, one ink, one accent, as hex values.
- **Type pairing** — display face + text face, each with an explicit job.
- **Signature move** — the single element a viewer would screenshot (see §6).

## 2. Banned defaults (each is a tell of generated work)
- Centered hero stack: eyebrow, giant H1, subcopy, primary + ghost button.
- Three-up icon feature grid; icon-in-a-colored-circle.
- Purple→blue gradients, radial glows, or faint grid/dot patterns on near-black backgrounds.
- Glassmorphism: blurred panels with 1px white borders.
- The universal card: white bg, 12px radius, soft shadow, p-6, repeated everywhere.
- Gradient text on headlines. Emoji or generic line-icon grids as visual content. Grey boxes labeled "image".
- system-ui / Inter / Roboto as the entire design — load at least one real typeface (font CDN is fine).
- Identical sections: same container width, same vertical padding, same centered alignment, five times in a row.
- Fade-up-on-scroll applied to every block as the page's only motion.
- Placeholder copy: "Lorem", "Feature title", "Welcome to X, the best way to…".

## 3. Type
- Largest display size ≥ 4× body size: `clamp(3rem, 7vw, 7.5rem)`, line-height 0.95–1.05, letter-spacing −0.02 to −0.04em.
- Body 16–18px, line-height 1.5–1.65, measure ≤ 68ch. Kickers/labels 11–12px, uppercase, letter-spacing 0.14em+.
- Two faces max. The display face must have character (high-contrast serif, wide grotesk, mono); the text face stays quiet.
- `font-feature-settings: "tnum"` and right-aligned figures anywhere numbers appear.

## 4. Color
- Three-color discipline: surface, ink, accent, plus tints of those. Accent covers <10% of pixels — CTAs, one word in a headline, key figures.
- Never pure #000 on pure #fff. Paper ≈ #f6f3ec–#faf8f2; ink ≈ #12110e–#1a1a1e; dark surfaces ≈ #0d0d0f, never navy-purple.
- Starting points, chosen per register, not a fixed palette: editorial (paper #f6f3ec, ink #1b1815, oxblood #7c2d2d) · technical (ink #101014, paper #f4f4f2, ultramarine #2b3bff) · brutal (#ffffff, #000000 2px rules, acid #d9ff00) · warm (cream #fbf1e3, espresso #241a10, cherry #e0342f) · luxe-dark (#0e0e10, bone #ece7dd, gold #c9a227).

## 5. Layout
- Required per page: at least one full-bleed band, one element that overlaps a boundary or breaks the grid, one asymmetric split (e.g. 5/7 columns). All-centered alignment is a failure.
- Alternate section surfaces for rhythm (light → dark → light, or paper → tint). Five identical white sections is a failure.
- Vary container widths (mix full-bleed, ~1280px, ~640px measures) and vertical padding (96–160px, different per section). Let one section be mostly whitespace.
- Separate with 1px hairlines at 10–15% ink opacity, not shadows. Shadows only on genuinely floating elements, large and soft: `0 24px 48px -12px rgb(0 0 0 / .18)`.
- Build "imagery" in code — SVG diagrams, generative canvas, charts, rendered mini-UI of the product — never empty placeholder boxes.

## 6. Signature move
One per artifact, tied to the product's core metaphor: kinetic or marquee type, an oversized stat/numeral, a canvas or WebGL hero, sticky-stacking panels, a horizontal-scroll chapter, hover-reveal imagery. Execute it fully and keep everything around it quiet. It usually lives in the hero; if not, the hero must be oversized typography doing the talking or the product itself rendered live — never a text stack.

## 7. Motion
- Entrances 600–900ms, `cubic-bezier(0.22, 1, 0.36, 1)`, stagger children 50–90ms, animate transform/opacity only. Micro-interactions 150–250ms.
- Every interactive element gets a hover state that moves something — translate, underline draw, arrow nudge, color invert — not a bare opacity dip. Style `:focus-visible` in the accent.
- Choreograph the hero on load; do not make scroll-reveal the only trick. Honor `prefers-reduced-motion`.

## 8. Copy and details
- Invent a plausible brand name. Headlines carry concrete nouns, numbers, or an opinion. CTAs are verb phrases ("Get the report"), never "Learn more". Testimonials get names, roles, specifics.
- Set `::selection` to the accent. Ship an inline SVG favicon. For paper and luxe registers, lay 3–5% opacity SVG-noise grain over the surface.
- The footer is a canvas — oversized wordmark or wordmark-as-graphic — not a four-column link farm.
- Dashboards: density is the aesthetic. Hairline grid, tabular right-aligned figures, one excellent chart beats five placeholder cards.

## 9. Pre-ship check — fix every "no" before delivering
- Display type ≥ 4× body? Exactly one accent color? At least one broken-grid or overlap moment?
- Every clickable thing has a hover and focus state? Zero banned patterns from §2? All copy real?
- No horizontal scroll at 375px and at 1440px? Does the §1 comment exist and does the page actually look like it?
