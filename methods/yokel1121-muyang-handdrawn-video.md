---
name: 沐阳手绘视频
description: Use when a user asks for 沐阳手绘视频, create-handdrawn-explainer, a complete hand-drawn explainer, whiteboard animation, illustrated lesson, narrated short video, Remotion MP4, automatic Chinese voiceover, subtitles, or a topic-to-video workflow.
---

# 沐阳手绘视频

Turn a topic into a finished, editable Remotion video. Support two modes:

- **Automatic:** the user says “default”, “automatic”, or supplies only a topic. Make every choice and deliver the MP4.
- **Guided:** the user asks to choose or customize. Guide style, typography, narration language, voice, duration, and aspect ratio without turning the session into a questionnaire.

## Required sub-skills

- **REQUIRED SUB-SKILL:** Use `imagegen` for every focal scene illustration.
- **REQUIRED SUB-SKILL:** Use `remotion-best-practices` before editing or rendering Remotion.
- Use `elevenlabs-tts` when it is installed; otherwise use the bundled `scripts/elevenlabs_project.py`.
- Use bundled `scripts/fish_audio_project.py` when the user selects Fish Audio or ElevenLabs has no usable Chinese/Mandarin voice.
- Use `control-chrome` only when the user asks Codex to configure ElevenLabs from an already signed-in Chrome session.

## Start here

1. Read `references/plan-schema.md` before authoring a plan.
2. Read `references/style-catalog.md` when selecting or implementing a visual style.
3. Read `references/guided-flow.md` only for guided mode.
4. Read `references/elevenlabs-setup.md` when credentials or voice selection are involved.
5. Run `python scripts/preflight.py --project <project-dir>` before generation.

## Automatic defaults

Do not ask questions when the user supplies only a topic or requests defaults.

| Setting | Default |
|---|---|
| Language | Chinese narration and Chinese captions |
| Duration | 60–90 seconds, 7–9 scenes |
| Frame | 1080×1440, 30fps |
| Style | `warm-editorial` |
| Motion | Style-matched motion preset |
| Images | One coherent image-generated illustration per scene |
| TTS | Fish Audio or ElevenLabs Chinese/Mandarin voice |
| Voice | Best usable Chinese/Mandarin narrator voice |
| Music | None unless requested |

Never fall back to SAPI or another mechanical voice after natural TTS is requested. For Chinese narration, never fall back to an English/foreign-character voice. If credentials or usable Chinese voices are missing, preserve the image-complete project and guide configuration. Prefer Fish Audio as the cloud fallback when the user has configured it.

Default to **continuous narration**: synthesize the whole voiceover as one audio file with one selected voice/reference, then allocate scene timing from that single file. Use segmented per-scene TTS only when the provider cannot synthesize the full script or the user explicitly asks for separate clips. Captions are mandatory by default.

## Production workflow

1. Write a factual conversational script with one spoken idea and one visual metaphor per scene. Verify time-sensitive or high-stakes claims.
2. Save UTF-8 `plan.json`. Keep headlines shorter than narration, set `style.id` from the catalog, and set `motion.id` only when overriding the style-matched default.
3. Create the project:

   ```powershell
   python scripts/create_project.py --plan plan.json --output video
   ```

4. Generate one 1080×1440 text-free illustration per scene with `imagegen`. Keep the same protagonist, palette, paper, line quality, and camera language. Save as `public/images/<scene-id>.png`.
5. Configure Fish Audio or ElevenLabs if needed. Never print, paste into chat, or commit an API key.
6. Generate narration with the selected provider. For Fish Audio, the default is one continuous `public/audio/narration.mp3` so the voice stays coherent:

   ```powershell
   python scripts/fish_audio_project.py --project video
   ```

   Use `--mode segmented` only for debugging or provider limits.

   For ElevenLabs, list or select voices when guided; otherwise let the bundled script rank available Chinese/Mandarin voices and handle paid-library fallback inside that language pool:

   ```powershell
   python scripts/elevenlabs_project.py --project video --auto-voice
   ```

7. Run `npm install`, preview representative frames, then `npm run render`.
8. Run `scripts/verify_output.py` and inspect 15%, 50%, 90% of every scene plus both sides of every cut. Fix clipped text, weak focal hierarchy, subtitle overlap, flashes, truncated narration, or blank endings.
9. Return clickable links to the MP4, project, and a preview/contact sheet.

## Guided mode rules

- Ask at most three short decisions at once.
- Show a visual style gallery when the user wants to choose a style.
- Offer 3 voice samples made from the same sentence; never ask the user to judge names alone.
- Make a recommendation first and always include “use defaults”.
- Once the user says “default the rest”, stop asking.

## Quality gates

- Use generated images, not generic SVG primitives, as focal visuals.
- Use deterministic Remotion frame math; no CSS animations or runtime randomness.
- Use the bundled motion presets for title, image, subtitle, texture, and accent movement. The motion must be visibly present: title entrance, image reveal/drift, subtitle entrance, and an accent/texture motion are required in every scene. Keep motion secondary to readability.
- Measure actual audio duration; never estimate from character count when audio exists.
- Prefer one continuous narration file for the finished video; do not create a final video whose voice identity changes between scenes.
- Keep readable text at least 80px from the sides and 96px from top/bottom.
- Use a heading font plus a highly legible caption font; never use calligraphy for subtitles.
- Keep generated-image text empty; render all text in Remotion.
- Render synchronized subtitles/captions in Remotion for every scene unless the user explicitly requests no subtitles.
- Avoid left-right split layouts in default style presets. Keep title, focal image, and subtitle in a top-center-bottom reading flow unless the user explicitly requests a split-screen composition.
- Match narration language to voice identity. Chinese videos require a Chinese/Mandarin voice unless the user explicitly overrides cross-language casting.
- Require H.264 video, AAC audio, planned dimensions/FPS, audible narration, and no blank final frame.

## Security and licensing

- Keep `.env`, local voice profiles, reference voices, and account data outside the skill and gitignored.
- Create restricted ElevenLabs keys with only Text-to-Speech and Voices Read permissions when possible.
- Clone a real person’s voice only with explicit authorization.
- Do not bundle proprietary fonts. Use installed fonts or openly licensed fonts described in the style catalog.

## Common mistakes

- Asking a full questionnaire after the user requested automatic mode.
- Using the first ElevenLabs library voice and failing on free-plan restrictions; use ranked same-language fallback.
- Falling back from Chinese narration to an English role voice; stop and ask for a usable Chinese voice instead.
- Printing Fish Audio, ElevenLabs, or OpenAI keys in chat or logs.
- Rendering before images or voice are complete.
- Reusing one generic illustration for multiple scenes.
- Applying decorative handwriting to long captions.
- Claiming completion when only a silent preview or stale MP4 exists.
