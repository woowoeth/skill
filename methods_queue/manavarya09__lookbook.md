---
name: lookbook
description: >-
  Award-grade design languages for building UI. Use whenever the user wants to build, design,
  create, redesign, restyle, or improve a frontend — a website, landing page, dashboard, app,
  component, page, portfolio, marketing site, or any HTML/React/Vue/Svelte interface — OR asks to
  make something look good / distinctive / less generic / less "AI slop", pick an aesthetic, or
  apply a specific style (Swiss, editorial, neo-brutalism, glassmorphism, Y2K, retro-futurism,
  soft, organic, claymorphism, maximalism, luxury, minimal, cyber, terminal, monospace, Bauhaus,
  geometric). Lookbook gives Claude a real, hand-built reference per design language to adapt,
  instead of generic keyword-driven output.
---

# Lookbook — Award-Grade Design Languages

A curated library of design languages. Each is a **pack**: a philosophy, a full token system,
ruthless anti-slop rules, and — the part that matters — a **real, hand-built reference page** to
study and adapt. You produce craft by adapting a proven exemplar, not by interpreting keywords.

## The one rule

**Never design from scratch when a language fits.** Pick a language, open its pack, study its
`reference/index.html`, then build in the user's stack by adapting that exemplar's tokens,
composition, and details. The reference is the source of truth for *how the style actually looks*.

## Workflow

### 1. Pick a language

- If the user **named a style** (or one clearly maps to their words), use it.
- Otherwise, read their vibe (product, audience, tone) and **recommend 2–3 languages from the index
  below with honest one-line tradeoffs**, then let them choose. Don't silently pick for them on a
  brand-new project unless they've said to just go.

### 2. Load that pack only

Read `languages/<slug>/LANGUAGE.md` in full, then **open and study
`languages/<slug>/reference/index.html`** (and any CSS next to it). This is progressive disclosure —
load one pack, not the whole library.

### 3. Build by adapting the reference

- Lift the **token system** (color, type, spacing, radius, shadow, motion, grid) verbatim unless
  the user's brand overrides it.
- Mirror the reference's **composition and signature moves** (the layout devices, the typographic
  scale, the specific effects). These are what make the style read as *that* style.
- Translate to the user's stack (HTML/Tailwind, React, Vue, Svelte, etc.). The references are static
  HTML/CSS precisely so they translate anywhere.
- Honor the pack's **anti-slop do/don'ts**. They are not optional.

### 4. Verify before delivering

Check your output against the pack's anti-slop checklist. If it could pass for generic AI output,
it's not done.

## Language index

| Slug | Language | The feeling | Best for | Avoid for |
|------|----------|-------------|----------|-----------|
| `swiss` | Swiss / International | Grid, precision, restraint | SaaS, docs, fintech, B2B, dev tools | Playful consumer, maximal brands |
| `editorial` | Editorial / Magazine | Typographic, asymmetric, print-inspired | Long-form, media, culture, agencies, blogs | Dense app UIs, dashboards |
| `neo-brutalism` | Neo-Brutalism | Raw and bold — the refined kind | Creator tools, startups, portfolios, bold brands | Conservative/enterprise, accessibility-critical |
| `glassmorphism` | Glassmorphism | Frosted depth, Apple-grade | Modern SaaS, dashboards, fintech, premium product | Content-heavy reading, low-power, flat brands |
| `y2k` | Y2K / Retro-futurism | Chrome, gloss, nostalgia | Music, fashion, gaming, Gen-Z, culture drops | Enterprise, trust-critical, accessibility-critical |
| `soft-organic` | Soft / Organic | Warm, rounded, tactile | Wellness, consumer apps, kids/education, friendly brands | Data-dense, austere/luxury, technical |
| `maximalism` | Maximalism | Controlled chaos, layered density | Fashion, culture, events, portfolios, statement sites | Utility UIs, accessibility-critical, dashboards |
| `luxury-minimal` | Luxury Minimal | Fashion-house restraint, vast space | Luxury, fashion, beauty, architecture, hospitality | Dense functional apps, playful consumer |
| `cyber-terminal` | Cyber / Terminal | Monospace, dark, technical | Dev tools, infra, crypto/web3, security, AI products | Warm consumer, luxury, mainstream non-tech |
| `bauhaus` | Bauhaus / Geometric | Primary colors, shapes, modernist | Culture, museums, education, design-forward brands | Conservative corporate, soft/luxury |
| `art-deco` | Art Deco / Gatsby | Gilded geometry, symmetric grandeur | Luxury hospitality, spirits, finance, theatre, fashion, events | Dev tools, minimal SaaS, playful consumer |
| `claymorphism` | Claymorphism | Soft inflated 3D, pillowy and friendly | Playful apps, kids/education, fintech onboarding, mobile, games | Dense data UIs, austere luxury, editorial |
| `vaporwave` | Vaporwave / Synthwave | Neon sunset, retro-future haze | Music, gaming, nightlife, creative tools, Gen-Z drops | Enterprise, trust-critical, accessibility-first |
| `neumorphism` | Neumorphism / Soft UI | Soft monochrome, pressable, tactile | Smart-home/IoT, calm apps, finance dashboards, audio/player UIs | Data-dense tables, content-heavy reading, text-everywhere |
| `frutiger-aero` | Frutiger Aero | Glossy aqua optimism, nature-meets-tech | Eco/clean-tech, wellness, consumer cloud, family tech | Enterprise, luxury restraint, dark/edgy, austere |
| `memphis` | Memphis / Postmodern | Clashing pastels, playful confetti geometry | Design festivals, creative studios, food/kids, culture | Enterprise, luxury, finance trust, dense dashboards |
| `skeuomorphism` | Skeuomorphism | Real materials — leather, metal, paper, glass | Heritage/nostalgic apps, audio tools, journaling, hobby | Data-dense SaaS, ultra-modern minimal, fast utility |
| `brutalist` | Brutalist / Raw Web | Exposed structure, default type, harsh honesty | Experimental studios, portfolios, zines, art/culture, dev | Trust-critical mainstream, e-commerce, enterprise calm |
| `constructivism` | Constructivism | Diagonal red-and-black agitprop energy | Arts/film/theatre festivals, type studios, exhibitions | Corporate calm, luxury, soft consumer, dense data |
| `japandi` | Scandinavian / Japandi | Warm muted calm, craft, vast space | Ceramics/homeware, tea/coffee, wellness, furniture, slow-living | Data UIs, dev tools, loud consumer, high-energy events |
| `pixel` | Pixel / Retro-Gaming | 8-bit pixels, CRT, arcade HUD | Indie games & studios, game jams, arcades, retro products | Enterprise, luxury, finance trust, dense reading |

## Global anti-slop guardrails (apply to every language)

These override default habits regardless of style:

- **No default fonts** (Inter, Roboto, Arial, system-ui) unless a pack explicitly calls for them.
  Each pack names its real typefaces.
- **No purple-on-white gradient cliché**, no timid evenly-distributed palettes. Commit to the pack's
  palette with dominant colors and sharp accents.
- **No predictable centered single-column** unless the pack's composition calls for it.
- **No emojis — ever.** Not as icons, bullets, badges, or decoration. Emoji instantly cheapen a
  layout and read as AI-generated. Use a real word or a custom SVG glyph instead.
- **No icon libraries.** Never pull Lucide, Feather, Font Awesome, Heroicons, Material Icons,
  Bootstrap Icons, Tabler, or any icon font/package — and never substitute an emoji for an icon.
  Draw **custom inline `<svg>` icons** tuned to the pack: its stroke weight, corner radius, optical
  size, and grid. Premium products draw their own marks; a borrowed icon set is a slop tell. Keep
  the set small and internally consistent (one stroke width, one corner treatment, one optical
  size), mark each `aria-hidden`, and pair it with a real text label.
- **No status / indicator dots.** The little ● "Live" / "Online" / pulsing-green availability dot
  (and the red notification dot) is a generic AI-UI cliché. Signal status with a word, a colored
  label or pill, a custom glyph, or type weight — never a bare dot.
- Match implementation effort to the aesthetic: maximalist/Y2K need elaborate detail; Swiss/luxury
  need precision and restraint. Execute the vision fully.
