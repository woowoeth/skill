---
name: moonland-deck
description: >
  Build 16:9 HTML presentation decks (and posters/cards that borrow the same look)
  in the "Dopamine-Swiss" visual language — a Swiss International grid skeleton
  crossed with a dopamine 4-color stage system and hand-painted SVG paint-blob
  highlights. Goes further than styling: it can read a local project, reverse-infer
  what's worth presenting, write a 演讲大纲.md outline, build a single-file deck
  from it, and ship a deck the user edits in the browser and syncs back to the
  outline. Use whenever the user wants a slide deck, talk deck, 演讲 deck, 分享 PPT
  replacement, keynote, HTML slides, pitch, or a poster/social card in the Moonland
  house style — works for any presenter (identity on the deck is always the caller's,
  not the author's), and shines for Chinese-language decks with a strong personal
  voice. Trigger even when the user just says "做个 deck / 做个分享页 / 把这份大纲做成
  幻灯片 / 把我这个项目讲成一场分享 / 用我那套样式" without naming the style.
---

# Moonland Deck — Dopamine-Swiss

A house visual language **and a pipeline** for 16:9 HTML presentation decks. The
look is a Swiss grid skeleton + a dopamine 4-color stage system + hand-painted SVG
paint-blob highlights (得意黑 Smiley Sans). Decks are single HTML files with inline
CSS/JS, keyboard nav, and (on the builder path) an in-browser editing layer. By
default they still load webfonts from Google Fonts + one jsdelivr face, so "single
file" does not mean strictly offline unless those font assets are bundled separately.

## Pick the entry point (auto-judge the mode)

| What the user hands you | Start at |
|---|---|
| A **project folder / a pile of material** ("把这个项目讲成一场分享") | **A — Ingest** → [references/01-ingest-outline.md](references/01-ingest-outline.md) |
| A **finished outline / written content** ("把这份大纲做成幻灯片") | **C — Build** → [references/02-build-and-edit.md](references/02-build-and-edit.md) |
| **Unclear** | Ask one line: "先帮你梳理该讲什么,还是你已经有内容了?" |

## The pipeline

```
A 摄入+反推该讲什么 ─┐  🧠 you (judgment)   ── 01-ingest-outline.md
B 写大纲+定参数     ─┘
     演讲大纲.md   ◄── the contract / single source of truth
C 组装 (build-deck.mjs) ─┐  ⚙️ script + runtime ── 02-build-and-edit.md
D 浏览器内编辑          ─┤
E 大纲 ⇄ deck 往返      ─┘
```

- **A + B** are *your* judgment: read the project, work out what's worth saying to
  whom, propose 3–5 angles, then write **one** `演讲大纲.md` and **stop at the review
  gate** before building. Schema + the "reverse-infer what to talk about" method:
  [references/01-ingest-outline.md](references/01-ingest-outline.md).
- **C** is a deterministic script: `node scripts/build-deck.mjs 演讲大纲.md`. It
  validates layout names, slide ids, `stage`, `style`, `total`, finale params, and
  pipe-field shape before writing HTML.
- **D + E** are runtime JS already inlined into the product — the user edits the deck
  in Chrome/Edge (image/link slots, per-page text) and syncs text back to the
  outline. You don't write this; you point the user at it.
  [references/02-build-and-edit.md](references/02-build-and-edit.md).

## Two paths — know the coverage

- **Builder path (primary, editable):** outline → `build-deck.mjs` → a deck with the
  editing layer + outline round-trip. Supports **7 layouts**: `cover-body`,
  `ly-statement`, `ly-list`, `ly-cards`, `ly-figure`, `ly-gallery`, `ly-finale`.
- **Manual path (fallback, all layouts, not editable):** copy `assets/template.html`
  and hand-edit. Use for one-offs or the 7 layouts the builder doesn't cover yet
  (`ly-split / ly-chain / ly-ladder / ly-code / ly-tpl / ly-compare / stack`). No
  outline, no editing layer.

Don't ask the builder for a non-builder layout — it will error. Either restructure
the beat into a builder layout or use the manual path for that slide.

## Always (non-negotiables — full list in 03-style-dna.md)

- **Identity on the deck is the CALLER's, never the author's.** Fill every presenter
  field (cover photo/name/hats/bio, chrome brand, foot signature) from whoever *this*
  deck is for. **Never** reuse a photo/name/handle from another deck or folder — it's
  a privacy leak. No presenter implied → drop the about-block. In doubt, ask.
- **Type through ramp classes**, never inline `font-size`/`weight`.
- **Color follows the stage:** warm/pink = before/origin, cool/blue = payoff/arrival.
- **≤2 paint-blobs per slide; chrome + foot on every slide; defend Chinese widows.**

## Index

- **[references/01-ingest-outline.md](references/01-ingest-outline.md)** — A+B: scan a
  project, reverse-infer angles, write `演讲大纲.md`; the outline schema + the 7
  builder layouts + variation params.
- **[references/02-build-and-edit.md](references/02-build-and-edit.md)** — C build
  command + layout coverage; D/E in-browser editing + outline round-trip.
- **[references/03-style-dna.md](references/03-style-dna.md)** — the visual language:
  three layers, fixed/floating variation, tokens, emphasis markup, widow defense,
  finale, reuse beyond decks.
- **[references/slot-contract.md](references/slot-contract.md)** — `link:` / `image:` /
  `card:` slot fields → `.linkslot` / `.imgslot` markup + localStorage storage.
- **`assets/outline-template.md`** — a live, buildable sample outline (the contract by example).
- **`assets/template.html`** — the manual-path template + the canonical CSS/markup source of truth.
