---
name: timepress-video
description: Use when the user asks for 时间压机, 动态视频, 动态正文配图, motion explainer, HTML/SVG/GSAP video, or wants to turn Chinese articles, scripts, product ideas, workflows, static visual briefs, or single viewpoints into a short playable browser-based timeline video with a chosen visual preset.
---

# Timepress Video

Create short dynamic explainer videos from Chinese content. The distinctive concept is the "Timepress": a timeline machine that presses a static idea, article, workflow, or visual brief into a playable motion composition. The output is a timed HTML/SVG/GSAP project that can be opened directly in a browser.

This skill is not tied to one character. Choose a visual preset per task. `xiaohei-sketch` is only one bundled preset for pure-white hand-drawn character metaphors.

## Resource Map

Load only what the task needs:

- `references/style-dna.md`: visual presets, color/typography guardrails, and style drift rules.
- `references/motion-patterns.md`: motion shot-list schema, scene archetypes, timing, main-mover actions, and animation operators.
- `references/html-motion-workflow.md`: HTML/SVG/GSAP output contract, preview path, and file layout.
- `references/qa-checklist.md`: pre-delivery checks for style, motion, readability, and renderability.
- `assets/templates/timepress-demo/`: copyable starter template using the optional `xiaohei-sketch` preset.
- `assets/examples/timepress-demo.gif`: optional sketch-preset visual calibration only; do not copy its composition blindly.
- `scripts/validate_motion_project.py`: local validator for generated motion projects.

## Core Workflow

1. **Digest the source**
   - Read the article, outline, topic, or single viewpoint.
   - Extract 1-5 cognitive anchors: core judgment, workflow, before/after change, bottleneck, status shift, or metaphor.
   - Prefer one anchor for a short demo; use 3-5 anchors for a multi-scene explainer.

2. **Choose a visual preset**
   - Default to `editorial-sketch` for articles, ideas, and conceptual explainers.
   - Use `clean-product` for product or SaaS workflows.
   - Use `data-flow` for systems, processes, metrics, and automation.
   - Use `xiaohei-sketch` only when the user asks for Xiaohei, 小黑, or a deadpan black hand-drawn character.

3. **Write a motion shot list first**
   - For planning requests, stop at the shot list.
   - For production requests, still draft the shot list internally before coding.
   - Each shot must include: anchor, 3-second read, structure type, main mover, objects, labels, motion beats, duration, and transition.
   - Use `references/motion-patterns.md` for the schema.

4. **Lock visual identity**
   - Read `references/style-dna.md`.
   - Create or update `DESIGN.md` in the output project before writing HTML.
   - Record the chosen preset, palette, typography, actor/object rules, and anti-patterns.
   - Do not drift into generic slideshow, stock animation, or image-to-video aesthetics.

5. **Build the motion composition**
   - Default output is a self-contained project folder with `index.html` and `DESIGN.md`.
   - Use the template in `assets/templates/timepress-demo/` only when the selected preset matches or can be adapted cleanly.
   - Draw the final hero frame first with SVG: actor/object, flow arrows, short labels, and output artifact.
   - Add GSAP timeline after layout is stable: draw-in lines, object movement, main-mover action, label writing, film/timeline output.
   - Keep text labels short. Prefer 2-6 Chinese characters per label; never use long explanatory sentences inside the frame.

6. **Preview and verify**
   - Run `python scripts/validate_motion_project.py <project-dir>`.
   - Follow `references/html-motion-workflow.md` for the local browser preview path.
   - Do not block on video encoders or external render tooling; validated playable HTML is the default deliverable.
   - Use `references/qa-checklist.md` before final delivery.

## Output Contract

For a finished production task, deliver:

- `index.html`: playable HTML/SVG/GSAP composition.
- `DESIGN.md`: chosen visual preset, style prompt, colors, typography, and anti-patterns.
- Optional `frames/`: browser screenshots for visual proof when useful.
- A directly openable preview link, such as `http://127.0.0.1:<port>/index.html` or a published preview URL. Start or publish the preview yourself; do not ask the user to run command-line steps.
- A short final note with paths and validation performed.

## Boundaries

- Do not use image-to-video as the default route; it is unstable for Chinese text and benchmark verification.
- Do not require Xiaohei unless the user selected the `xiaohei-sketch` preset.
- Do not make a PPT-like flowchart, dense course slide, commercial vector animation, generic tech UI, or cute mascot short.
- Do not copy bundled examples or upstream examples as a layout swap. Reuse style rules, not exact compositions.
- Do not promise file export from this skill. Treat export as a separate downstream task.
