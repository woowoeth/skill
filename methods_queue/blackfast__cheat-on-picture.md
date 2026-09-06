---
name: cheat-on-picture
description: Turn articles, posts, explainers, methods, workflows, and conceptual text into Ian/Xiaohei-style article illustrations, optionally replacing Xiaohei with a user-provided character card, then rebuild the chosen still image as motion-ready SVG and deliver a Pixel2Motion-style animated HTML showcase. Use when asked for animated article illustrations, custom-avatar article illustrations, Xiaohei replacement, image-to-motion from article art, GIF/MP4-ready illustration motion, article visual shot lists with motion ideas, or HTML motion output for a hand-drawn explainer image.
---

# Cheat On Picture

## Core Position

Create animated article illustrations, not logo reveals and not full short-film storyboards. The default flow is:

```text
article -> cognitive-anchor shot list -> character-resolved still draft -> simplified motion SVG -> standalone animated HTML
```

Default to Xiaohei when no custom character is provided. When a user provides their own image or character description, turn it into a reusable text character card instead of storing raw reference images by default.

## Read As Needed

- `references/character-card-template.md`: read when the user provides a custom avatar, persona, reference image, mascot, or asks to replace Xiaohei.
- `references/illustration-to-motion-bridge.md`: read before converting a still illustration or visual idea into SVG actors and motion.
- `references/output-contract.md`: read before saving or reporting deliverables.
- `/Users/xiaoheipro/.codex/skills/ian-xiaohei-illustrations/SKILL.md`: read for the current Ian/Xiaohei article-illustration workflow, then load its referenced style files only when needed.
- `/Users/xiaoheipro/.codex/skills/pixel2motion/SKILL.md`: read for HTML motion, QA hooks, timeline discipline, and final-frame checks. Do not force article art through logo vectorization.

## Workflow

### 1. Determine Intent

First classify the request:

- **Strategy only**: user asks how to illustrate, where to add images, or wants a shot list. Produce a shot list and stop.
- **Static illustration**: user asks to generate article images but not motion. Generate stills and save them under the static output path.
- **Motion deliverable**: user asks for animation, GIF, MP4, HTML, moving illustration, Pixel2Motion, or "make it move". Build HTML first; export GIF/MP4 only after HTML QA if requested.

If intent is ambiguous, default to a short shot list plus one recommended motion direction. Do not invent a full production request.

### 2. Build The Shot List

Do not average every paragraph. Select cognitive anchors: core judgment, turning point, before/after split, input-output loop, bottleneck, route, failure mode, role-state change, or system handoff.

For each proposed image include:

- Placement after which paragraph or section.
- Theme.
- Core meaning.
- Structure type.
- Character action.
- Suggested visual elements.
- Suggested short Chinese labels if the article is Chinese.
- Motion idea.
- Animatable parts.

Default quantity: 1-3 for short posts, 4-8 for normal articles, never more than 9 unless the user explicitly asks.

### 3. Resolve Character

- If the user gives no character, use Xiaohei: small solid-black deadpan worker, white dot eyes, tiny legs, serious absurd action.
- If the user provides a character image or description, create or update a character card under `assets/character-cards/<character-slug>.md`.
- If the user names an existing character card, read and reuse it.
- Preserve the source character's recognizable silhouette and markers, but keep the article-illustration grammar: black linework, sparse accent colors, white background, and the character doing the core conceptual action.

The character must not become decoration. If removing the character leaves the concept fully intact, redesign the image around a character action.

### 4. Create The Still Draft

Use the Ian article-illustration style:

- 16:9 horizontal article image.
- Pure white background.
- Minimal black hand-drawn linework.
- Sparse red, orange, and blue handwritten annotations.
- Lots of whitespace.
- One image explains one conceptual structure.
- No PPT look, commercial vector polish, dense infographic, cute mascot poster, complex UI mockup, or top-left title label.

When using a custom character, replace Xiaohei in the prompt with the character card's visual traits and action constraints.

### 5. Rebuild For Motion

Treat the generated still as a visual reference, not as a strict tracing target. Reconstruct a simplified SVG with only the meaningful actors:

- Character.
- Main path or arrow.
- 3-6 core objects.
- Warning/result labels.
- Optional secondary notes.

Use stable semantic ids such as `#character`, `#main-path`, `#object-a`, `#warning-label`, and `#result-note`. Do not animate by `nth-child` selectors. Add `pathLength="1"` to stroke paths that will draw on.

Do not chase every hand-drawn wobble. A clean SVG actor set that preserves meaning is better than a noisy trace that cannot animate well.

### 6. Animate And Package

Default motion when the user gives no choreography:

- Character: subtle preparation, action, and settle.
- Main path: draw-on or directional reveal.
- Objects: staggered pop/slide/settle.
- Labels: short fade/pop, never all at once.

For user-specified motion, follow the user's direction unless it breaks legibility or the final-frame contract. Keep article motion light by default; full storyboard animation is only in scope when the user explicitly asks for it.

Build a standalone HTML deliverable with Pixel2Motion-style behavior:

- Main animation in `#logo-root` or an equivalent stable root.
- Replay control, speed control, and reduced-motion behavior.
- `?t=<ms>` deterministic seeking.
- `?static=1` final static state.
- `window.__p2mReady`.
- Final frame must match the verified static SVG state.

Use Pixel2Motion scripts and references when available, especially `animate_svg_showcase.py`, `capture_motion_frames.py`, `probe_motion_continuity.py`, and `references/html-delivery-template.md`.

## QA Gates

Before delivery, verify:

- Shot list focuses on cognitive anchors, not paragraph-by-paragraph decoration.
- Character is the action subject.
- Still image stays sparse, white, hand-drawn, and not PPT-like.
- SVG contains a small semantic actor set with stable ids.
- Motion uses staggered timing; parts do not move in lockstep unless intentional.
- Reduced motion shows the final state immediately.
- Captured final frame equals the static SVG state.
- GIF/MP4 exports, if requested, are generated from the verified HTML timeline.

## Response Style

Keep strategy output short and usable. After creating artifacts, report:

- What was created.
- Which article anchor each item serves.
- Where files were saved.
- Any QA caveats, especially if a GIF/MP4 export was requested but only HTML has passed verification.
