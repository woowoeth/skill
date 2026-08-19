---
name: moonlit-book-workflow
description: Build or resume a reusable 12-page personalized English picture book in the Moonlit watercolor house style, using Codex built-in image generation for a per-book character sheet plus illustrations and local authorized-adult voice cloning for narration. Use when the user asks to create, regenerate, resume, validate, or publish a custom Moonlit children's book from child profile data.
---

# Moonlit Book Workflow

## Purpose

Produce one personalized English picture book as a resumable local job. Keep story content variable while locking the illustration style with the approved neutral style key and one per-book character sheet. Render narration locally only from an authorized adult voice profile.

This skill orchestrates Codex tools and the project CLI. The browser application does not call Codex image generation directly.

## Locate The Project

Use the current workspace when it contains `scripts/book-workflow.mjs` and `workflow/styles/moonlit-watercolor-v1/style.json`. Otherwise ask the user to open or provide the Moonlit Stories repository; never guess a user-specific absolute path. Refer to the repository root as `PROJECT_ROOT` in commands.

Do not put jobs, voice references, model weights, or generated private assets in source control. Use `PROJECT_ROOT/.moonlit/jobs` and `PROJECT_ROOT/.local-models`. A form-created job may keep its normalized narrator profile under that job's `private/voice/` directory; never move it into public assets.

## Required Workflow

1. Read [workflow-contract.md](references/workflow-contract.md), [image-generation.md](references/image-generation.md), and [tts-and-release.md](references/tts-and-release.md) before acting.
2. Run `node scripts/book-workflow.mjs list` first. If the user supplied the job ID returned by the browser form, inspect it with `node scripts/book-workflow.mjs status --job-id JOB_ID` and read its `manifest.json`. Resume that exact job; do not recreate it. For a new job without an ID, derive a filesystem-safe ID such as `20260803-luna-lantern`, report it, and use it consistently.
3. Ensure the profile has a separate Latin-script `english_name`. If the form supplied only a Chinese name, propose an English name or pinyin and get guardian confirmation before creating the job; never insert Han characters into English narration.
4. Create a job from a validated child profile when no job exists.
5. Draft exactly 12 pages. Each page has one English sentence, one faithful Chinese translation, and one scene prompt. English narration must use the child's chosen English name and contain no Han characters.
6. Commit the story and run `plan`. Review the resulting prompt/task manifest before image generation.
7. Generate the character sheet first with built-in image generation. Inspect it visually. Record the exact returned file path, then approve it.
8. Generate the cover and pages 1–12 with both the neutral style key and the approved character sheet as references. Inspect every candidate before approval.
9. Inspect `manifest.narration`. When it is `parent-clone/ready`, reuse the normalized profile at `private_profile_path` inside the job; do not ask the user to upload it again and do not expose its transcript or consent file. When it is `standard/pending`, finish story and illustrations, then stop at the TTS gate and ask for an authorized adult recording. Run local TTS only from an explicitly authorized adult profile. Never clone a child or an unconsenting person.
10. Record and approve all 12 narration files, assemble `book.json`, validate the job, and build a self-contained reader HTML.
11. Before making a shareable HTML, obtain guardian confirmation for the chosen child display name and generated likeness. Keep full profile details in the private manifest and publish only reader-required fields.
12. Open the result in the in-app browser and verify desktop and mobile rendering, page navigation, Chinese toggle, and audio playback. Close temporary servers and browser sessions started for testing.

## Resume Discipline

- Treat `manifest.json` as the source of truth.
- Never infer image output by modification time. Pass the exact path returned by built-in image generation to `record-image`.
- Keep approved tasks. Retry only pending or failed tasks.
- If the story changes, re-run `commit-story` and `plan`; accept the CLI's selective invalidation instead of deleting the job.
- If the style key, character identity, narration text, voice sample, model revision, or TTS parameters change, regenerate affected artifacts.
- Never invent an image seed or stable model version. The built-in generator does not expose either.

## Completion Gate

Do not report completion until all of the following are true:

- one approved character sheet, one approved cover, and 12 approved page illustrations exist;
- each page illustration used the same neutral style key and per-book character sheet;
- exactly 12 English sentences contain no Han characters and their Chinese translations are faithful;
- exactly 12 local narration files correspond to the English text;
- `assemble` and `validate` succeed;
- the custom single-file reader opens without console errors and the assets are embedded;
- no private voice reference or consent file is embedded in the reader.

If no authorized voice reference is available, stop at the TTS preflight gate and state that illustration/story production can continue but voice cloning is not complete.
