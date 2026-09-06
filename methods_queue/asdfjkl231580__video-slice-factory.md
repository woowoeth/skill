---
name: video-slice-factory
description: Turn long Chinese talking-head or meeting videos into topic-complete publishable clips with source-grounded transcripts, optional TikHub market evidence, deterministic edit plans, per-video cover frames, captions, HyperFrames and Remotion motion packaging, speech-first music, formatted manuscripts, independent per-video audits, and four-file delivery. Use for 视频切片、长视频拆条、口播剪辑、批量成片、字幕动画、封面、背景音乐 or an auditable reusable video workflow.
---

# Video Slice Factory

## Purpose

Produce one defensible video at a time. The output count comes from the source, never from a quota. Preserve meaning, make every edit traceable, and stop when required evidence is missing.

## First use

1. Run `python3 scripts/setup.py --check --human`. Treat `assets/dependencies.json` as the dependency truth; do not infer readiness from prose or from one command succeeding.
2. If anything is missing, run `python3 scripts/setup.py --plan --human`. Show the user three groups: already installed, installable after confirmation, and guided/manual actions.
3. After explicit approval, run `python3 scripts/setup.py --install --yes` for system and locked local packages. Include `--with-codex-plugins` only when the user also approved installing the available HyperFrames and Remotion plugins. Never install a plugin, submit credentials, accept a license or authorize a paid request silently.
4. Re-run `python3 scripts/setup.py --check --human`. If a plugin was installed, say that Codex may need the next turn or a restart before the new Skill is available. Do not continue while a required environment dependency remains missing.
5. Run `python3 scripts/doctor.py`. Do not call the machine production-ready if any runtime or project check remains open.
6. Run `python3 scripts/init_project.py --root "/absolute/project" --brand-name "brand" --speaker "speaker" --source "/absolute/video.mp4"`.
7. Put optional user-owned portraits in `品牌资料/我的照片/`, optional licensed music in `品牌资料/音乐/`, and edit `品牌资料/brand-profile.json`.
8. Rerun `python3 scripts/doctor.py --project "/absolute/project"` to validate font, music authorization and disk space.
9. If no portrait is provided, run `extract_cover_candidates.py` and select a frame from each video's own rough cut. Never reuse one pose across all covers by default.
10. Read [references/01-production-sop.md](references/01-production-sop.md), then only the reference for the current gate.

Do not copy HyperFrames, Remotion, transcription or DOCX Skill source code into this Skill. Detect installed Skills/plugins, use an available Codex plugin installer only after confirmation, and preserve a guided fallback when the current Codex environment cannot install a dependency automatically.

## Non-negotiable rules

1. Keep `raw_transcript`, `corrected_transcript`, and `editorial_script` separate.
2. `edit_plan.json` is the sole timeline truth; video, captions and animation are derivatives.
3. Freeze a source content map before market search. Market evidence may rank or phrase a topic, never invent a claim absent from the source.
4. Topic completeness determines duration. `short` means at most 120 seconds; `long` means above 120 seconds only for folder organization.
5. Choose the least invasive mode: continuous clip, same-source montage, then cross-source montage.
6. Keep subtitles independent from the moving talking-head layer. A content panel may reflow the video upward but may not cover the speaker's face or leave the panel permanently visible.
7. HyperFrames owns the stable visual shell; Remotion owns time-based relayout, semantic motion and the independent caption layer.
8. Music is optional, licensed by the user, and speech-first. Measure loudness; do not cover speech.
9. Cover, subtitle, motion and outro behavior come from `brand-profile.json`; do not silently fall back to a different font or visual preset.
10. A producer cannot approve the same output. Every video gets an independent read-only audit and a complete watch record.
11. Batch mode may parallelize transcription, hashing and frame extraction only. Editorial selection, picture lock, render authorization and final watch advance one video at a time.
12. Deliver one cover PNG, one standalone motion MP4, one packaged MP4 and one formatted DOCX manuscript per approved video folder.
13. Never bundle user photos, credentials, paid API responses, unlicensed fonts, music or source videos into the Skill or repository.

## Ordered gates

### Gate 0 — environment and source identity

Run `doctor.py`, hash and `ffprobe` every source, identify the target speaker, and record missing dependencies truthfully.

### Gate 1 — transcript truth

Create immutable raw ASR, corrected text with a correction ledger, and an editorial layer citing source sentence or word IDs. Homophones and product names require glossary review.

### Gate 2 — source-first content map

Inventory every defensible claim, example, method, context and risk. Each usable block becomes used, reserved, duplicate or rejected with a reason.

### Gate 3 — optional market evidence

Prepare a free query plan first. `collect_market_signals.py` is TikHub-only, makes no paid call without `--allow-paid`, and never treats an empty response as zero demand. See [references/03-market-evidence.md](references/03-market-evidence.md).

### Gate 4 — topic intersection

Classify source/market intersections as `priority`, `brand_reserve`, `future_recording` or `discard`. Only source-supported `priority` topics proceed.

### Gate 5 — paper edit and timeline

Write the complete topic manuscript, choose edit mode, audition every seam, then validate:

```bash
python3 scripts/validate_edit_plan.py /absolute/edit_plan.json
```

### Gate 6 — clean rough cut and picture lock

Render without cover, captions, music or decorative graphics. Review start, end, every seam, context, sync and a complete watch before picture lock.

### Gate 7 — packaging

Create one exact cover file from the current video's reviewed frame; embed that same file. Generate captions from the corrected transcript mapped through `edit_plan.json`. Use semantic yellow emphasis only where reviewed. Add content-adaptive motion only when it explains a real relationship.

### Gate 8 — per-video audit

Complete every blocker in [references/04-audit-and-delivery.md](references/04-audit-and-delivery.md). A playable MP4 is not a pass. A failed video stops independently and cannot inherit a batch pass.

## Files to preserve

- Project identity: `job.json`
- Timeline truth: `edit_plan.json`
- Brand truth: `品牌资料/brand-profile.json`
- Market evidence: raw response plus normalized evidence state
- Render input hashes and tool versions
- Per-video audit result and independent auditor run ID
- Four-file delivery manifest with hashes

## Safe-stop conditions

Stop before rendering if source identity, transcript fidelity, topic support, speaker identity, context, seam review, brand assets, font resolution, cover identity, motion timing, music authorization or audit independence cannot be verified. Report `not_collected`, `insufficient_sample`, `provider_failure` and `true_zero` separately.
