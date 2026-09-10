---
name: video-editing
description: >-
  Edit video from the command line with ffmpeg and whisper. Use whenever the
  user wants to cut/trim/join clips, turn a horizontal video into a vertical
  Reel/Short (9:16), generate or burn-in subtitles/auto-captions, add music,
  speed up, or extract audio. Triggers on "смонтируй", "нарежь", "reels",
  "shorts", "субтитры", "автотитры", "вертикальное видео", "склей", "обрежь",
  "монтаж", edit video, trim, crop to 9:16, burn captions.
---

# Video editing with ffmpeg + whisper

You edit video by running command-line tools on the user's machine. There is no
timeline UI — every edit is a reproducible `ffmpeg` (or `whisper`) command. This
is exactly how the "Claude edits my videos" setups online work: Claude picks the
right command, runs it, and inspects the result.

## Before you start

1. Check the tools exist. Run `scripts/check_deps.sh`. If something is missing,
   tell the user the one install command they need (see that script's output)
   and stop — do not try to work around a missing `ffmpeg`.
2. Find the input file. Ask for the path if the user hasn't given one. Never
   guess a filename. Always work on a copy — never overwrite the source; write
   to a new file (e.g. `input.mp4` -> `input_reel.mp4`).
3. Inspect before editing. Run
   `ffprobe -v error -show_entries stream=width,height,codec_type,duration -of default=noprint_wrappers=1 INPUT`
   so you know the resolution, orientation and length before choosing a command.

## The helper scripts

Prefer these over hand-writing long ffmpeg filtergraphs — they encode the
fiddly, easy-to-get-wrong parts (subtitle styling, vertical framing, safe
concat). Each one prints usage when run with no arguments. All paths can be
absolute or relative.

| Task | Script |
|------|--------|
| Check ffmpeg/whisper are installed | `scripts/check_deps.sh` |
| Trim / cut a section by time | `scripts/trim.sh` |
| Join several clips into one | `scripts/join.sh` |
| Make a vertical 9:16 Reel/Short | `scripts/make_reel.sh` |
| Transcribe speech to an .srt file | `scripts/transcribe.sh` |
| Burn subtitles into the video | `scripts/add_subtitles.sh` |
| Auto-remove silent pauses (jump cuts) | `scripts/remove_silence.py` |
| Karaoke captions (words light up) | `scripts/karaoke_subs.py` |
| Background music with ducking | `scripts/add_music.sh` |
| Colour-grading presets (looks) | `scripts/color_grade.sh` |
| Title-card intro / outro | `scripts/intro_outro.sh` |
| Auto-insert B-roll from a folder | `scripts/auto_broll.py` |

Read `reference.md` for the raw ffmpeg recipes behind these (speed change,
music bed, fades, GIF, thumbnails, format conversion) when a request falls
outside the scripts.

## Workflow guidance

- **Reels / Shorts.** Most source footage is horizontal (16:9). Use
  `make_reel.sh` to produce a 1080x1920 vertical clip. Default framing is a
  blurred background with the video centered (`--fit blur`) — it looks the most
  "reel-like" and never crops faces. Offer `--fit crop` (fill, center-crop) if
  the subject is safely centered. Keep Shorts/Reels ≤ 60s; if the source is
  longer, trim first with `trim.sh`, then reel it.
  Pass `--platform tiktok|shorts|reels|square|feed` to target a specific site:
  the 9:16 platforms share 1080x1920 but nudge the subject up out of each site's
  bottom UI (blur/pad modes), while `square` (1080x1080) and `feed` (1080x1350,
  4:5) change the aspect for Instagram feed posts. The script prints a
  recommended caption bottom-margin for the chosen platform.
- **Subtitles / auto-captions.** Two steps. First `transcribe.sh` produces an
  `.srt` from the audio using whisper. **Always tell the user to open the `.srt`
  and correct any misheard words before burning** — auto-transcription is never
  perfect, especially with names and Russian. Then `add_subtitles.sh` burns the
  (corrected) `.srt` into the video with large, readable, centered captions.
- **Cut & join.** `trim.sh` for a single section; run it several times and then
  `join.sh` to assemble the pieces, or to remove a dead segment in the middle
  (cut around it, then join). `join.sh` re-encodes so clips with different
  codecs/resolutions still concatenate cleanly.
- **Auto-remove pauses (jump cuts).** `remove_silence.py` detects silent
  stretches and keeps only the spoken parts (audio+video stay in sync). Do this
  *early*, on the raw clip, before reeling/captioning. Start with defaults; if it
  clips words, raise `--pad` or `--min-silence`; if it leaves long dead air,
  lower `--threshold` (e.g. `-35`) or `--min-silence`. Needs an audio track.
- **Karaoke captions.** `karaoke_subs.py` makes captions where each word turns
  colour exactly as it's spoken (the punchy Reels look). It uses whisper *word*
  timestamps, writes a `.karaoke.ass`, and burns it. Same caveat as subtitles:
  auto-transcription errs — offer to let the user fix the text (edit the `.ass`
  Dialogue lines, or re-run) before finalizing. `--highlight green|cyan|yellow`
  picks the active-word colour. Two looks via `--style`: `karaoke` (default) —
  spoken words stay coloured and fill up cumulatively; `word` — ONLY the current
  word is coloured and earlier words revert to white (the bouncing single-word
  look). This is an alternative to `add_subtitles.sh`, not an addition — use one
  or the other.
- **Background music with ducking.** `add_music.sh` lays a music track under the
  video and, by default, *ducks* it (drops its volume) whenever there's speech,
  raising it again in the gaps — via sidechain compression. Music is auto-looped
  to the video length. Tune with `--music-vol` and `--duck low|medium|high`; use
  `--no-duck` for a flat music bed. If the video has no voice track it just adds
  music. Add music *last*, after captions.
- **Colour grading.** `color_grade.sh --preset NAME` applies a look (warm, cool,
  cinematic teal-orange, vivid, matte, vintage, bw, noir). `--list` shows them.
  Grade *before* captions/intro so the look is consistent, and keep it subtle —
  offer `cinematic` or `warm` as safe defaults. It re-grades the whole clip.
- **Intro / outro.** `intro_outro.sh --intro "Title|Subtitle" --outro "..."`
  generates title cards matching the video's size and fps and splices them on.
  Split title and subtitle with `|`; tune with `--seconds`, `--bg`, `--fg`. Needs
  a Cyrillic-capable font (DejaVu/Arial — found automatically). Add these last,
  after the main edit, so card size matches the final frame.
- **Auto B-roll.** `auto_broll.py INPUT BROLL_DIR OUTPUT` cuts the picture away
  to clips/images from a folder the user provides (it does NOT fetch stock), on
  a regular cadence, while the main audio keeps running — the talking-head +
  B-roll look. Tune `--every` (cadence) and `--clip` (insert length; must be <
  every); `--order shuffle` to randomise. Ask the user for the B-roll folder;
  never invent one. Do this on the trimmed, paused-removed cut, before captions.
- **Order of operations.** Remove pauses → trim → auto B-roll → colour grade →
  reel → captions → intro/outro → music. Burn captions on the already-vertical
  clip so size and position match the final frame; add music last so ducking
  reacts to the final voice track; add intro/outro title cards last so they
  match the final frame.

## Rules

- Never overwrite or delete the user's original files. Always output a new file
  and tell the user the exact output path.
- Long encodes can take minutes. Run them in the background and report when done
  rather than blocking; for a first pass on a long video, offer to test the
  command on a short trimmed sample first.
- After producing a file, verify it with `ffprobe` (duration/resolution look
  right) and tell the user what you made and its path. Don't claim success on an
  encode you didn't check.
- If the user is on their own machine and asks to *see* the result, you can open
  it with the OS default player (`xdg-open` / `open` / `start`) — ask first.
