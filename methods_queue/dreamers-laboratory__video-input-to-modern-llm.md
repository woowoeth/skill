---
name: video-input-to-modern-llm
description: Give an agent eyes on a video without blowing the context window. Use when the user shares a video file (screen recording, demo, meeting, dashcam, security clip, lecture) and wants it described, checked, summarized, timestamped, or searched. Samples frames with ffmpeg at a user-chosen resolution and cadence, estimates the token cost per model family before anything is attached, and fits a token budget by trading frame count against resolution. Two-pass by default: cheap contact sheets to find where to look, then full frames only where it matters.
---

# Video Input to Modern LLM

A model cannot watch a video. It can look at frames. The whole game is choosing which frames and at what size, because every frame is paid for in tokens whether or not it mattered. This skill makes that choice explicit and measured.

All commands run from this skill's folder and need `ffmpeg` and `ffprobe` on PATH. No other dependencies.

## Decide before sampling

Answer three questions, out loud, in the transcript:

1. **What is the question about the video?** "What happens" wants scene changes. "Is the button ever red" wants a steady cadence. "Read the error text at 3:41" wants one high-resolution frame at 3:41. "Summarize the lecture" may want the audio track more than the frames.
2. **What resolution does the question need?** `low` (512 px long side) reads layout and color. `medium` (768) reads large UI text. `high` (1024) reads body text and small labels. `full` keeps native size and is rarely justified. The user may name a level; if they don't, start low and go up only where the first pass says to.
3. **What is the token budget?** Frames compete with everything else in context. Pick a number before sampling, pass it as `--token-budget`, and state it.

## Pass one: cheap overview

```bash
python3 scripts/sample_video.py VIDEO --out /tmp/frames \
  --mode scene --resolution low --sheet 4 --token-budget 3000 --model-family claude
```

Or for a steady cadence, `--mode interval --every 10`. The script writes `frame_NNNN.jpg` with the timestamp burned into the corner, `sheet_NN.jpg` contact sheets, and `manifest.json` with every frame's timestamp, dimensions, and estimated tokens for Claude, OpenAI tile-based, and OpenAI patch-based models.

Look at the sheets, not the frames. A 4x4 sheet of low-resolution frames is one image of about 1,850 Claude tokens; the same sixteen frames attached separately are about 3,150, and the model sees them side by side on the sheet, which is better for spotting change. Sheets are capped at 1568 px wide because that is where the provider downscales anyway.

## Pass two: look closer where it matters

From the sheets, pick the timestamps that answer the question. Sample only those, at the resolution the question needs:

```bash
python3 scripts/sample_video.py VIDEO --out /tmp/frames/detail \
  --mode interval --every 1 --start 221 --end 224 --resolution high
```

Then attach those frames. Cite timestamps in the answer (`at 03:41`), never frame numbers.

## Measure before attaching

Always run the meter on what you are about to attach and report the number:

```bash
python3 scripts/measure_tokens.py /tmp/frames/detail
```

`--exact` (with `ANTHROPIC_API_KEY`) returns the real token count from the provider's counting endpoint instead of the estimate. Use it when the budget is tight or the answer is expensive to get wrong. Report tokens spent on frames as a line in the final answer.

## Modes

| mode | picks | good for |
|---|---|---|
| `interval --every S` | one frame every S seconds | steady coverage, "did X ever happen" |
| `fps N` | N frames per second | short clips, motion |
| `scene --scene-threshold T` | frames where the picture changes (0.3 default; lower finds more cuts) | edited video, slides, screen recordings with navigation |
| `keyframes` | the encoder's I-frames | fast rough pass on long files |

`--max-frames N` caps any mode by thinning evenly. `--start/--end` window the video. `--audio` also writes a mono 16 kHz WAV for a transcription step.

## Budget behavior

With `--token-budget`, the script computes the per-frame cost at the chosen resolution, caps the frame count to fit, and, if even one frame does not fit, steps the resolution down and says so in `notes`. It never silently exceeds the budget. It also never upscales: a 640-wide source stays 640 wide under `medium`.

## Rules

- State mode, resolution, frame count, and estimated tokens before attaching anything.
- Prefer sheets for discovery and single frames for reading. Do not attach both a sheet and all of its frames.
- Timestamps in answers come from `manifest.json`, not from guessing by frame order.
- If the question is really about what was said, extract audio and transcribe; frames are the wrong tool for speech.
- Token figures are estimates from published sizing rules unless `--exact` was used; say which.
- Do not sample videos the user did not provide or point at.
