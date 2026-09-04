---
name: clip-video
description: Use when asked to clip a YouTube or local video into a short vertical video for TikTok, Instagram Reels, or YouTube Shorts — e.g. "clip this video", "make a short from this URL", "add captions/subtitles and effects", "make a reaction clip / top-5 countdown / POV / music edit", "turn this into a 30-40 second vertical clip with a hook".
---

# Clip Video — vertical shorts with burned-in captions

## Overview
Turn a long YouTube video into a 25–45s 1080×1920 clip with word-accurate animated captions, chapter badges, zooms, and flash transitions. Works with ANY ffmpeg build (no libass needed): captions are Pillow-rendered PNGs composited with the core `overlay` filter.

Scripts live in `scripts/` next to this file. Requires: `yt-dlp`, `ffmpeg`, and Pillow (`python3 -m venv .venv && .venv/bin/pip install Pillow` in the work dir).

## Pick a format first

Platforms rank shorts on WATCH TIME — choose the structure that holds viewers longest. The same source can be rendered in 2–3 formats to A/B test; all reuse this pipeline, varying caption style and structure.

| Format | Use when | Recipe |
|--------|----------|--------|
| Hook trailer (default) | narrative long-form (vlogs, challenges, docs) | cold-open hook → chapter badges → cliffhanger/payoff + CTA |
| Reaction | a creator's reaction IS the moment | 1 segment, minimal fx; one `pill` caption giving context ("Kai reacts to X 👀", y≈950); best on trendy moments |
| Top-N countdown | several comparable moments | `pill` title at top + the `countdown` rail (below): ALL rank markers (🥇🥈🥉 then "4." "5."…) stacked on the LEFT for the WHOLE clip; the current rank's colored label pops in beside its marker. ORDER: open mid-list (#4 of 6, #3 of 5 — never at the bottom), escalate upward; you MAY withhold #1 entirely — the ever-visible 🥇 marker is the bait that holds viewers to the end |
| POV / text-on-screen | one self-explanatory viral moment | raw clip + a single `pov` caption (y≈700); no transcript captions |
| Gaming split-screen | talking-only source (podcast/interview) | talk on top (~55%), looping gameplay below; strong on Reels/Shorts, weaker on TikTok. Per segment: `[0:v]scale=1080:1060:force_original_aspect_ratio=increase,crop=1080:1060[a]; [1:v]scale=1080:860:force_original_aspect_ratio=increase,crop=1080:860[b]; [a][b]vstack,setsar=1` |
| Music edit | footage niches (sports, cars, movie/show edits) | beat-cut montage, NO captions; trending audio dominates the mix (`volume=0.8` on music, duck or drop source audio); money & anime themes overperform |

## Workflow

1. **Transcript:** `python3 scripts/transcript.py <URL> <workdir>` → writes `words.json` (word-level timestamps) + `transcript.txt` (15s blocks). Read transcript.txt and pick moments.
2. **Editorial cut (the part that matters):** duration is a HARD rule — minimum 25s, maximum 45s. Under 25s? Extend with build-up before the peak or aftermath/reaction after it, or add a second moment; never ship short. Hook = the video's most quotable absurd/specific claim (a price, superlative, or contradiction — usually in the cold open); end on a cliffhanger right before a reveal, or the payoff + CTA. Structure: 1–3 segments for a single-scene clip; 8–13 short segments for a whole-video trailer (one moment per chapter, with a badge each). Cut mechanics from words.json: start ~0.05s before the first word's `t`, end 0.3–0.5s after the last word's `t` but before the next word starts. Trimming a mid-sentence digression is fine — jump cuts are the genre.
3. **Stream URLs:** `yt-dlp -g -f 401 URL > vurl.txt` (4K AV1; fall back `-f 313`) and `yt-dlp -g -f "bestaudio[ext=m4a]" URL > aurl.txt`. Cropping 9:16 from 4K then downscaling to 1080×1920 beats a 1080p source.
4. **Segments:** for each cut, `scripts/grab_segment.sh vurl.txt aurl.txt <start> <dur> seg_NN.mp4` — frame-accurate network seek, downloads only what's needed, normalizes to 1080×1920/30fps/SAR 1.
5. **Edit spec:** write `spec.json` (format below), then `.venv/bin/python scripts/build_clip.py spec.json` → renders caption/badge PNGs, writes `filters.txt` + `render.sh`, prints the timeline.
6. **Render:** `zsh render.sh`, then **verify**: extract frames at each chapter (`ffmpeg -ss T -i out.mp4 -frames:v 1 f.jpg`) and view them; check audio with `volumedetect` (expect peak ≈ −0.3 dB, mean ≈ −19 dB).

## spec.json

```json
{
  "output_file": "clip.mp4",
  "segments": [
    {"file": "seg_00.mp4", "src_in": 0.16, "fx": ["push:1.10"]},
    {"file": "seg_01.mp4", "src_in": 106.0, "fx": ["flash_in", "shake", "flash_out"]}
  ],
  "captions": [{"seg": 0, "t": 1.20, "text": "WHERE A [$24,000] MEMBERSHIP 🚿"}],
  "badges": [{"text": "LEVEL 1|THE $0 GYM", "from_seg": 1, "to_seg": 1}],
  "headline": {"text": "[$0] vs [$10,000] GYMS", "until_seg": 0},
  "cta": {"text": "WATCH THE [FULL VIDEO] 👀", "last_seconds": 2.6}
}
```

- Caption `t` is SOURCE time (from words.json); the script maps it to clip time and ends each caption at the next one. One caption per spoken phrase of 2–5 words — a new caption roughly every 0.7–1.5s, anchored to its first word's `t`. Caption every spoken word in the clip (no gaps).
- `[brackets]` = gold highlight, multi-word OK (`[GOLDEN SHOWER]`); use on prices, numbers, punchline nouns. Emoji render via Apple Color Emoji.
- Caption `"style"`: default = bold white stroke (word-by-word transcript captions); `"pill"` = white rounded box, black text (TikTok-native — reaction context lines, countdown titles); `"pov"` = italic serif white (text-on-screen format). Optional `"y"` sets any caption's center-y.
- `badges`/`headline`/`cta` are optional — badges only make sense for multi-chapter montages. `headline` accepts `"style": "pill"` and omitting `until_seg` makes it persist the whole clip — use that for countdown titles (a `caption` can't span segments).
- `countdown` (Top-N rail): `{"x": 55, "top_y": 280, "spacing": 150, "items": [{"rank": 1}, {"rank": 2}, {"rank": 3, "label": "Ion know 😭", "color": "#FF5555", "from_seg": 0, "to_seg": 1}, {"rank": 4, "label": "Valid crashout 🤣", "color": "#55BBFF", "from_seg": 2}]}`. EVERY item's marker (medal emoji for ranks 1–3, "N." beyond) stays on screen the whole clip — including ranks you never play; that's the anticipation bait. A `label` pops in (slide-up) when its `from_seg` is reached and then STAYS pinned to its marker through the end — labels ACCUMULATE (after #1 reveals, the #3/#2/#1 labels are all on the rail at once), they never disappear when the next rank starts. (`to_seg` is unused for label timing now; keep it for badge-style fallbacks.) **Face-aware placement:** when `top_y` is omitted, the build scans the composed segments with OpenCV (needs `opencv-python-headless` in the venv; ~1s, deterministic) and slides the rail up/down to the y that least covers faces — eye bands weighted 3× over the rest of the face. Explicit `top_y` overrides; `"face_avoid": false` disables; x/alignment never changes. Labels ≤4 words; keep `top_y` ≥ 280 so the rail clears a title pill at y≈130.
- `fx`: `push:Z` (slow zoom-in), `punch:Z` (static punch-in), `shake`, `flash_in[:d]` / `flash_out[:d]` (white flash). Convention: flashes between chapters, hard cuts within.
- Badge text: `"GOLD PART|WHITE PART"`.

## Gotchas (each one cost a debug cycle)

| Trap | Fix |
|------|-----|
| ffmpeg build lacks `ass`/`drawtext` (Homebrew slim builds) | Don't replace user's ffmpeg — PNG overlays (this pipeline) work on any build |
| zsh does NOT word-split unquoted `$VAR` in `for` loops | Loop runs ONCE silently; use literal args or arrays (grab_segment.sh avoids this) |
| `zoompan` outputs SAR like 7712:7713 → concat dies "Failed to configure output pad" | `setsar=1` after every per-segment chain (build_clip.py does this) |
| AAC segment audio ≠ video duration → lip-sync drift across concat | `atrim` + `apad=whole_dur=` per segment (handled) |
| `yt-dlp --download-sections` cuts at keyframes → sloppy/unknown offsets | Seek the direct stream URL instead: `-ss` before `-i` while transcoding is frame-accurate |
| yt-dlp format `"401/313+bestaudio"` picks 401 alone → silent video | First alternative must include audio: `"401+bestaudio[ext=m4a]/..."` or grab audio separately |
| Overlay input indexes shift when segment count changes | render.sh/filters.txt are generated together — never hand-edit indexes |
| Caption wider than 1080 | Auto-wraps at 950px to 2 balanced lines (don't exceed ~6 words) |

## Layout constants (TikTok/Reels-safe)
Captions centered y≈1330, headline/badges y≈170–185, CTA y≈1560; keep text inside x 60–1020. Font: Arial Black (`/System/Library/Fonts/Supplemental/Arial Black.ttf`).
