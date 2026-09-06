---
name: paper-video
description: Use when a user wants to turn a viewpoint, theme, emotional idea, story premise, or animation description into a complete adult-healing paper-sculpture video production package.
---

# Paper Sculpture Story Video

Create a production-ready Chinese Markdown package. By default, do not generate images, video, voice, or music.

## Workflow

1. Inspect the idea and project files. Ask only when an unanswered choice would materially change the core message; otherwise make a reasonable assumption.
2. Classify the input as factual explanation, viewpoint, emotional story, or animation description. Browse primary sources when factual claims are current, niche, or consequential.
3. Read `references/story-design.md`, `references/paper-sculpture-style.md`, `references/h3-ref2va.md`, and `references/output-contract.md` completely.
4. Use `assets/制作包模板.md` as the skeleton and replace every placeholder.
5. Save to `<主题>/纸雕故事版/制作包.md`. If it exists, use `纸雕故事版-v2/制作包.md`. If both exist, ask before overwriting.
6. Run `python3 scripts/validate_package.py <制作包.md>` and fix every error.

## Content Rules

- Build one causal story whose scenes advance through cause, goal, emotion, or theme rather than disconnected cards. Do not require a character, object, or visual symbol to persist from the first scene to the last.
- Default to 16:9, 1920×1080, 30–60 seconds, 4–6 scenes, 4–10 seconds each.
- Each scene starts from its own clean background. Effects happen inside the scene.
- Prefer tearing, folding, flipping, pressing, rails, gates, and magnetic attraction to PPT-like pop-ins.
- Put every visible information-bearing word in the image prompt using large, bold, high-contrast Chinese text.
- Generate a subject once when it is actually reused, and identify every reuse. Do not invent reuse merely to connect scenes.
- Every required element needs an element-board prompt and an entry in the coverage checklist.

## Boundaries

- Use `industrial-vox-video` for explicit industrial/archive Vox aesthetics.
- Use `h3-prompt-writing` when only an H3 prompt is requested.
- Use `imagegen` when actual images are explicitly requested.
- Actual media generation is a separate explicit request after package delivery.
