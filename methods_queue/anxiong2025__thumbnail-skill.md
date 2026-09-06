---
name: create-social-thumbnails
description: Create, adapt, or review high-CTR creator thumbnails and social-media covers for Xiaohongshu, WeChat Channels, YouTube, YouTube Shorts, and Douyin. Use for requests such as 自媒体封面, 爆款封面, high-CTR thumbnail, or click-driving cover from real photos, screenshots, products, or style references; preserve real assets exactly, avoid AI-generated lookalikes, and never promise virality or performance.
---

# Create High-CTR Creator Thumbnails

Produce a platform-ready creator thumbnail that communicates the topic in roughly one second, remains legible at feed size, uses the user's real assets faithfully, and has a clear click-driving visual hierarchy. Treat “viral” or “爆款” as a creative objective, never as a guaranteed outcome.

## Route the request

1. Identify the target platform and content type. Treat the requested ratio as a separate choice: it may use a platform preset or a generic `1:1`, `4:3`, `3:4`, `4:5`, `6:7`, `16:9`, or `9:16` canvas.
2. Read [references/platform-specs.md](references/platform-specs.md) for the matching platform or ratio-only canvas and export preset.
3. If the user names a style ID, uses a natural-language style phrase, supplies a style reference, asks what styles are available, or needs a reusable prompt, read [references/style-catalog.md](references/style-catalog.md). A supplied style reference is the primary art-direction input: match its general title scale, density, subject ratio, background category, card rhythm, outline weight, and decoration language while using the user's own content.
4. Read [references/composition-patterns.md](references/composition-patterns.md) when adapting the selected style to supplied assets, creating variants, or reproducing the title-to-image gradient treatment.
5. Read [references/asset-integrity.md](references/asset-integrity.md) whenever the request includes user photos, product screenshots, brands, public figures, or a commercial-use claim.
6. Before delivery, follow [references/qa-checklist.md](references/qa-checklist.md).

## Intake

Collect or infer these inputs:

- target platform, content type, and requested ratio;
- a style name, style reference, or free-form visual description; a catalog ID `S01` through `S11` is optional;
- primary title and optional supporting text; when the user supplies only a topic, write three concise candidate hooks internally and select the strongest one instead of asking the user to fill every label;
- exact-use assets such as the user's portrait, real screenshots, products, or logos;
- style-only references;
- desired tone, brand colors, and output format;
- whether the user is requesting commercial-use clearance.

Do not block on non-critical omissions. Choose a sensible default and state it. Ask only when a missing title, required real asset, or rights-sensitive choice would materially change the result.

## Protect source fidelity

Classify every input before editing:

- **Exact-use asset:** preserve its actual content. Crop, mask, scale, color-correct, and composite it deterministically.
- **Style reference:** borrow only general layout, rhythm, contrast, or color direction. Do not copy protected artwork or treat the reference as a source asset.
- **Generatable support:** scene extension, generic shapes, arrows, highlights, and non-branded decoration may be generated when useful. If a real interface, room, product screen, or evidence image can establish the topic, reuse and extend it instead of inventing an unrelated abstract background.

Never redraw a real interface screenshot, product, document, data visualization, logo, or person when the user expects the original. Never create an AI lookalike as a substitute for the supplied portrait. If a cutout tool may alter the subject, compare the result with the source at face, hands, clothing, logos, and edges before using it.

## Build the composition

1. Create the exact target canvas before laying out content. Never stretch an existing cover to change ratios; recompose it.
2. Establish one dominant promise, one dominant subject, and one supporting proof area.
3. Keep the main title short enough to understand in roughly one second. For high-density creator covers, use two or three compact lines occupying roughly 35–45% of the canvas height, with alternating pale-yellow and white fill plus a very thick dark keyline. A chunky hand-painted/marker rhythm may be used for the main hook and large count; keep subtitles, labels, scores, and check items in a clean heavy sans/黑体.
4. Reserve UI-safe margins and avoid placing essential text or faces near edges.
5. For a collage beneath the title, place the real collage unchanged, then add a separate background-colored-to-transparent overlay above it. Do not bake fake screenshots into the gradient.
6. For a portrait-led cover, cut out the supplied person, keep recognizable features unchanged, and scale the half-body subject to 35–55% of the canvas. Place it in the lower half, let it bleed off an edge when appropriate, and add a pale-yellow or white contour plus shadow. Never put a usable cutout back inside a photo frame.
7. When exploration is requested, create up to three meaningfully different variants: text-led, face-led, and proof-led. Do not create superficial color-only variants.
8. Treat `S11 Creator Impact / 真人高密度大字` as the current flagship system. When it is selected or the user requests a dense bold-title portrait cover, read [references/signal-impact-system.md](references/signal-impact-system.md). Its default structure is huge outlined hook + expressive cutout person + real topic background + one proof card + short check items/arrows.

## Generate and edit

When the user asks to create the cover, use the built-in image-generation workflow for the finished visual by default; do not stop at a prompt or substitute a code-drawn poster unless the user explicitly requests deterministic/source-editable construction. Pass the supplied style reference, person, screenshots, and logo as separately labeled inputs. In the prompt, lock the person's identity, exact title, reference background category, subject ratio, title scale, palette, cards, arrows, and check items. Use deterministic compositing or a final overlay pass for exact logos, numbers, tables, and text when generation changes them materially.

For one requested cover, generate one strong master first. Inspect it at full size and feed size. Retry only for a concrete failure such as wrong ratio, unreadable title, altered identity, malformed hands, invented data, unrelated background, or weak visual density.

Keep source files separate where possible:

- background and texture;
- title and annotations;
- real collage or product screenshots;
- subject cutout;
- gradient, outline, and shadow effects.

## Verify

Run the bundled helpers when Python is available. The prompt builder is optional; natural-language style direction is the primary interface:

```bash
python3 scripts/platform_presets.py --list
python3 scripts/platform_presets.py --list-ratios
python3 scripts/prompt_builder.py --list-styles
python3 scripts/prompt_builder.py --style S01 --ratio 16:9 --title "400+ Figma Templates"  # optional catalog helper
python3 scripts/verify_thumbnail.py output.png --platform wechat-channels
python3 scripts/verify_thumbnail.py output.png --ratio 4:3
```

Use `--aspect-only` only when the user intentionally requests a non-canonical resolution. The verifier checks technical conformance; still perform visual QA at full size and at a small feed preview.

## Deliver

Report:

- the final file path and pixel dimensions;
- the platform preset or generic ratio used;
- the interpreted style description and, if useful, an optional catalog tag;
- which supplied real assets were preserved;
- any assumptions or unsupported native-file claims;
- a rights caveat when commercial use is requested but third-party rights are not documented.

Do not label an output “commercially cleared” merely because this skill's code is open source. Commercial clearance depends on every included photo, person, brand, font, screenshot, template, and generated asset.
