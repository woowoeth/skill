---
name: binbin-talking-head-edit
description: 使用 HyperFrames 为口播、教程、录屏和知识类视频创建并渲染多样化的半透明科技感注释。适用于添加信息卡片、大字标题、图表、流程图、警告、标签、HUD 叠层或与口播同步的视觉总结；也适用于从源视频音频对齐逐字稿与时间点，以及在用户确认后按原始分辨率、60fps 导出成片。
---

# 彬彬口播剪辑

制作能够解释和强化口播、但不会变成另一条字幕轨的信息叠层。根据源音频确定时间点，组合多种视觉形式，避开密集录屏区域，先预览确认，再使用原始素材以 60fps 导出。

## Required Dependencies

Use the HyperFrames plugin skills:

- Read `hyperframes/SKILL.md` and `hyperframes-cli/SKILL.md` completely.
- Read HyperFrames typography, motion, transitions, transcript, and data references when relevant.
- Use FFmpeg/ffprobe for media inspection and frame extraction.
- Use the in-app Browser to open and verify the local Studio preview.

Preferred timestamp fast path:

- When the local `video-use` skill is available, read its `SKILL.md` and use its Scribe transcription helpers for source-audio timestamps.
- Treat `video-use` as the preferred transcription/cache layer and HyperFrames as the overlay authoring/render layer. Do not use `video-use` to replace the approved HyperFrames visual catalog.
- Fall back to HyperFrames transcription or local Whisper only when `video-use` is unavailable, its API key is missing, the hosted call fails, or the user explicitly requests an offline workflow.

## Load Skill Resources

Read [references/visual-language.md](references/visual-language.md) before designing overlays.

Read [references/layout-library.md](references/layout-library.md) when the video uses full-screen talking head footage, circular PiP, docked speaker layouts, chapter transitions, or supporting material cards. Treat its `M01-M04` rules as reusable composition primitives.

Inspect `assets/reference-screenshots/` when defining the project visual identity. Treat these screenshots as style boundaries, not layouts to copy literally.

Use `assets/examples/codex-deepseek-overlay-example.html` only as implementation reference for HyperFrames timing, media tracks, and reusable CSS patterns. Replace its content and timing for every new video.

## Canonical Template Catalog

The visual catalog at [assets/card-library-gallery/index.html](assets/card-library-gallery/index.html) is the canonical template index for this skill. It is not a disposable showcase.

Before designing a video:

1. Read the catalog source and [references/layout-library.md](references/layout-library.md).
2. Select explicit template IDs for the overlay plan: `R01-R06`, `C01-C11`, `M01-M04`, and/or `M03-A-M03-I`.
3. Add a `Template ID` column to the timing plan.
4. Reuse the selected template's composition hierarchy, spatial proportions, and transition behavior.
5. Translate any new external reference into the current project palette. External references may expand layout and motion, but must not silently replace the established blue/violet/mint/coral identity.

The gallery HTML is allowed as a CSS and structural implementation reference. Copy only the selected pattern into the project composition, then adapt its content, safe zones, timing, and scale to the actual footage.

If no better pattern is justified, prefer an existing catalog ID over inventing a new layout. When a genuinely new reusable pattern is approved, add it to both the gallery and `references/layout-library.md` before treating it as part of the skill library.

Run `scripts/prepare_media.sh` when media metadata, proxy media, audio, or contact sheets are needed.

## Workflow

### 1. Inspect Inputs

1. Read the named transcript, brief, and any existing project instructions.
2. Probe the source video for resolution, duration, frame rate, codecs, color space, and audio.
3. Never assume the written transcript exactly matches the recorded speech.
4. Transcribe or align the actual audio with word or phrase timestamps. Read and quality-check the transcript. Prefer the `video-use` cached word-level workflow below when available.
5. Build contact sheets across the full video and inspect additional frames around likely overlay moments.

#### Fast timestamp workflow with `video-use`

Resolve helper paths relative to the installed `video-use/SKILL.md`. Keep all generated artifacts under the source folder's `edit/` directory.

For one source:

```bash
python <video-use>/helpers/transcribe.py <source-video> --language zh --num-speakers 1
python <video-use>/helpers/pack_transcripts.py \
  --edit-dir <source-dir>/edit \
  --silence-threshold 0.15
```

For several source takes, use `transcribe_batch.py` and then `pack_transcripts.py`.

Rules:

- Keep `edit/transcripts/<source-stem>.json` as the canonical word-level timestamp cache.
- Reuse the cache on every later overlay revision. Do not re-transcribe an unchanged source.
- Before trusting a cache, confirm it belongs to the current source. If the source was replaced or modified after the JSON was created, regenerate it.
- Use `edit/takes_packed.md` as the compact planning view, but consult the raw word-level JSON for exact overlay in/out points and semantic phrase boundaries.
- For breath-edited Chinese talking-head footage, start with a `0.15s` silence threshold. The generic `0.5s` default can collapse many sentences into a few unusably long paragraphs after pauses have been removed.
- Increase the threshold toward `0.25-0.5s` for natural interviews or footage with intact pauses.
- Scribe Chinese output may contain spaces between characters. Normalize those spaces for reading/search, but preserve the original word timestamps.
- Time the first transcription and report whether caching materially improves the workflow. A hosted first pass can still take minutes; the main speed gain is that later timing revisions become near-instant.
- Never upload source audio through `video-use` when the user requires an offline-only workflow or the material is not authorized for hosted transcription.

### 2. Map Visual Density

Classify each spoken segment:

- `A-roll open`: speaker visible with usable negative space.
- `A-roll overlap-safe`: overlay may cover a small part of shoulder, torso, or gesturing edge.
- `screen sparse`: screen recording has enough empty space for a compact annotation.
- `screen dense`: important interface text fills the frame; do not add an overlay.
- `transition/title`: existing title treatment is already visually dominant; add nothing unless requested.

Protect the face, eyes, important hands, bottom subtitles, and the UI area being demonstrated.

Full-screen talking-head rule:

- Whenever the speaker occupies the full frame, apply the `M01` animated gradient stroke to the outermost video boundary by default.
- The stroke uses the active project palette and must sit at `inset: 0`, not inside the picture.
- At 1920x1080, default to a clearly visible `16-20px` stroke. Scale proportionally for other resolutions; do not fall back to a web-style hairline.
- Remove or replace it only when the speaker becomes a circular PiP, a docked rectangle, or leaves the frame.

### 3. Build An Overlay Plan

Create a timing table before writing HTML:

| Start | End | Spoken meaning | Template ID | Visual form | Position | Avoid |
|---|---|---|---|---|---|---|

Select only moments where an overlay improves comprehension, retention, contrast, or emotional emphasis.

Opening rule:

- Begin building the first overlay as soon as the opening phrase supplies enough meaning, normally within `0.1-0.4s`; do not leave a decorative 1-2 second pause before it appears.
- Prefer a result, contradiction, or promise.
- A second short overlay may summarize the route, steps, or stakes before `24s`.

Timing rule:

- Enter after the relevant phrase begins, not before the viewer has context.
- Hold long enough to read in roughly two-thirds of its visible duration.
- Exit before a dense screen cut or the next semantic point.
- Use actual audio timestamps, not paragraph estimates.

### 4. Enforce Visual Variety

Use at least three visual forms in a normal 2-3 minute video. Do not make more than half of the overlays full glass cards.

Choose among:

- Pure hero type without a containing card.
- Hero type plus small chips, labels, or an underline.
- Horizontal three-card or three-node process.
- Large number plus comparison bars.
- Compact table, ranked bars, or progress meter.
- Before/after or A/B comparison.
- Warning treatment with icon and status bar.
- Step navigator or pipeline.
- Icon tiles plus a dominant conclusion.
- Small top-left chapter label only.

Match the form to the meaning. Use charts only for quantities, comparisons, progress, ranking, or change. Use pure large type for claims, reversals, names, conclusions, and warnings.

Every primary information overlay must have two readable hierarchy levels:

- A dominant semantic headline, normally `80-96px` at 1920x1080.
- Supporting evidence such as icon tiles, metrics, chips, a comparison, a process, or a status row.

Do not ship a row of small cards without a headline. Do not ship unsupported hero type when `R01`, `R04`, or `R06` can add useful evidence beneath it.

Highlighting rule:

- Every dominant headline should normally contain one accent-colored semantic phrase.
- Select the complete meaningful phrase, not the last characters that happen to fit a line. For example, in `合作前先对齐边界`, highlight `对齐边界`, never `齐边界`.
- Author emphasis explicitly in the timing plan or a phrase map. Never derive it by character count, suffix length, or automatic slicing.

Icon rule:

- Prefer a recognizable icon over `01 / 02 / 03` when the items represent actions, roles, objects, or capabilities rather than a strict sequence.
- At 1920x1080, primary tile icons should normally render at `52-72px`; icons must be visually dominant, not metadata-sized.

### 5. Size For Video

Default to larger text than web UI:

- Main Chinese headline: `80-96px`; use `86px` as the normal 1920x1080 baseline.
- Secondary conclusion: `34-52px`.
- Body/supporting text: `30-38px`.
- Data values: `52-92px`.
- Labels: `20-26px`.
- Primary tile icons: `52-72px`.

Use a primary overlay width around `760-960px` at 1920x1080. Before reducing type or forcing a line break, widen the composition inside its safe zone. Dynamic text must have a measured `max-width`, and overflow must be checked at the hero frame.

Never insert `<br>` merely to repair wrapping. Short display headlines should stay on one line when the safe zone permits it. If a single line is required, combine sufficient width with `white-space: nowrap` and verify it does not escape its frame.

Supporting material rule:

- When a screen recording, report, demo, or evidence clip is the point, let it occupy roughly `60-70%` of the frame or take over the full frame.
- Do not keep the speaker visible at the cost of making the material unreadable.
- In a deliberately dense edit, avoid unplanned empty stretches: alternate useful headline+support overlays and dominant source material while preserving subtitle and face safety.

Allow the overlay to cover roughly `10-15%` of the speaker silhouette when this creates a stronger composition. Never cover the face, eyes, microphone, the main hand gesture, subtitles, or demonstrated controls.

### 6. Author The HyperFrames Project

1. Create a project-specific `DESIGN.md` from the reference screenshots and current footage.
2. Build the static hero frame first, then add entrances and exits.
3. Use muted video plus a separate audio element.
4. Register the paused GSAP timeline.
5. Add `.clip` to every timed overlay.
6. Avoid duplicate animation selectors controlling the same property.
7. Keep animation deterministic and seekable.
8. Use a lightweight proxy for Studio review when the original file is large.
9. Keep semantic headline emphasis as explicit markup or an explicit phrase map; never compute it from arbitrary character offsets.

### 7. Validate And Preview

Run:

```bash
npx hyperframes lint
npx hyperframes validate
npx hyperframes inspect --at <hero-frame-times>
```

Generate thumbnails at every overlay hero frame and visually inspect:

- Text size and readability.
- Face, hand, subtitle, and UI obstruction.
- Whether the visual form matches the spoken meaning.
- Whether styles are sufficiently varied.
- Whether titles actually become visible after animation.

Open the Studio project in the in-app Browser. Give the user the Studio URL, not the raw HTML path.

Do not render the final video until the user approves, unless the user explicitly requests immediate export.

### 8. Render From Original Media

Before final rendering:

1. Replace proxy sources with the original video source for both video and audio.
2. Confirm the composition dimensions match the source.
3. Validate again with no console errors.
4. Render high quality at 60fps:

```bash
npx hyperframes render --output <output.mp4> --fps 60 --quality high
```

Do not end the turn while rendering is still running.

### 9. Verify The Final File

Probe the exported file and confirm:

- Source resolution retained.
- Average and nominal frame rate are `60/1`.
- Audio exists and duration matches video.
- H.264 color metadata remains BT.709 unless the source requires otherwise.
- Duration is within a small muxing tolerance of the source.

Extract final-file frames from the opening and several later overlay moments. Verify the rendered file itself, not only the HTML preview.

Report the clickable absolute output path and the verified technical parameters.
