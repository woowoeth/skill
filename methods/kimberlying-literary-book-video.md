---
name: literary-book-video
description: "Create a Chinese vertical literary book-review short video in the established quiet Siddhartha style: slow cloned narration, restrained emotional copy, dark painterly backgrounds, book-cover overlay, Songti subtitles, forced subtitle alignment, ambient noise bed, FFmpeg rendering, and contact-sheet QA. Use when the user asks to make another book video, imitate the existing Siddhartha/One Hundred Years of Solitude workflow, preserve the same voice/tone/rhythm, or package a repeatable book-account video process. Full Chinese workflow guidance is in README.zh-CN.md."
---

# Literary Book Video

## Purpose

Produce a 9:16 Chinese literary book short video modeled on the local `siddhartha/` workflow: one emotional narration drives the whole piece, visuals stay quiet and literary, subtitles are large and aligned to the final voice, and every render is checked with contact-sheet frames.

The `scripts/` directory contains working templates. Copy them into a new project folder, then customize `project.json` and `narration.txt`.

For the same workflow written in Chinese, see [README.zh-CN.md](README.zh-CN.md).

## Default Route

1. Inspect the reference project before changing anything:
   - `siddhartha/narration.txt`
   - `siddhartha/build_assets.py`
   - `siddhartha/generate_cloned_voice.py`
   - `siddhartha/render_final.py`
   - `siddhartha/verify_contact.jpg`
2. Create a new folder named after the book, for example `one_hundred_years_solitude/`.
3. Copy the template scripts from this skill into that folder.
4. Create `project.json` from `references/project-config-example.json`.
5. Write `narration.txt` first. Keep it short enough for a 45-75 second final video.
6. Generate cloned narration using the local `.voiceclone` environment when available.
7. Slow the narration only after measuring actual duration. Use a subtle `atempo=0.88-0.94` range.
8. Run forced alignment against the slowed final voice.
9. Build visual assets and subtitles.
10. Render the final MP4.
11. Generate and inspect a contact sheet before reporting done.

## Writing The Narration

Write like a literary account, not a plot explainer. The target shape is:

1. Start with the feeling after rereading the book.
2. State what the book seems to be about on the surface.
3. Pivot to the deeper human theme.
4. Name a few symbolic story elements without summarizing the whole plot.
5. End with one quiet, memorable interpretation.

Keep the tone slow, restrained, and reflective. Avoid dense facts, author biography, chapter-by-chapter summary, internet-style punchlines, and motivational slogans.

Recommended length: 10-14 Chinese lines, 250-360 visible Chinese characters. If TTS overshoots, shorten the script rather than accepting a multi-minute result.

## Visual Contract

Read `references/style-contract.md` when changing the look, subtitle rules, voice pacing, or QA criteria. Do not replace the style with a generic explainer template.

Core defaults:

- Canvas: `1080x1920`, `30fps`.
- Background: four slow-moving painterly segments.
- Overlay: dark top/lower gradients, tilted book cover at upper-left, big centered title, small author line, decorative English keyword near the lower third.
- Subtitle: white Songti, black stroke, centered around the lower-middle safe area.
- Audio: cloned voice plus very low brown-noise ambience; no loud music by default.

## Script Workflow

In the new project folder:

```bash
cp /path/to/skill/scripts/*.py .
cp /path/to/skill/references/project-config-example.json project.json
```

Edit:

- `project.json`: book title, author, cover lines, palettes, output file name, reference voice settings.
- `narration.txt`: final Chinese voiceover text.

Generate voice:

```bash
/Users/qianmeng/Documents/剪视频/.voiceclone/bin/python generate_cloned_voice.py
```

If the process fails with `No Metal device available`, rerun it outside the sandbox with approval. The MLX TTS and forced-aligner models need local Metal/GPU access.

After voice generation:

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 voiceclone_output/*.wav
ffmpeg -hide_banner -y -i voiceclone_output/<generated>.wav -filter:a atempo=0.9,aresample=44100 narration_voice.wav
/Users/qianmeng/Documents/剪视频/.voiceclone/bin/python align_voice.py
python3 build_assets.py
python3 render_final.py
python3 make_contact_sheet.py
```

Use the bundled Codex runtime Python if system Python lacks Pillow:

```bash
/Users/qianmeng/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 build_assets.py
```

## Verification

Always verify:

- `ffprobe` reports expected final duration.
- `verify_contact.jpg` shows readable title and subtitles.
- Subtitles sit in the same lower-middle band as the reference and do not cover the cover/title.
- Decorative words are legible; use uppercase English if lowercase script looks muddy.
- Final file exists and plays as `output_file` from `project.json`.

Report the final MP4 path, contact-sheet path, duration, and any caveat such as "voice generation required unsandboxed Metal access."
