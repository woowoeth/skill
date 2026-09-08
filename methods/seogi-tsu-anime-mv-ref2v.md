---
name: anime-mv-ref2v
description: Specialized prompt engineering and storyboard orchestration skill for creating anime Music Videos (MV) and Promotional Videos (PV) using MiniMax H3 Reference-to-Video (ref2va / r2v). Generates professional, audio-synced video prompts combining character image references ([Picture 1]), reference audio tracks ([Audio 1]), kinetic typography, motion graphics, UI/HUD overlays, and anime visual language without requiring specific LoRA trigger words.
---

# Anime MV Ref2V Prompt Engineering (MiniMax H3)

This skill designs high-impact, audio-synchronized prompt sequences for MiniMax H3's Reference-to-Video (`ref2va` / `r2v`) generation pipeline. It translates character reference images and soundtrack audio into dynamic anime music videos using professional motion graphics and storyboard grammar.

## Core Capabilities
1. **Reference Asset Binding**: Seamlessly binds character references (`<Picture 1>`, `<Picture 2>`) and soundtrack references (`<Audio 1>`) following H3 official specifications.
2. **Layered Motion Graphics**: Infuses anime MV visual language—kinetic typography, HUD telemetry, split-screen panels, halftone screentones, and geometric color blocks.
3. **Beat-Accurate Audio Synchronization**: Align camera velocity and action beats with audio energy curves (Intro -> Build-up -> Drop/Climax -> Poster Freeze).
4. **Universal Compatibility**: Operates independently of specific trigger words (such as `lumimv`), producing native prompts compatible with base H3 as well as custom MV LoRAs.

## Prompt Architecture Standard

Every generated prompt must follow this standard 4-block schema:

```text
[Global Style, Color Palette & Reference Asset Binding]
Use <Picture 1> as reference character, and <Audio 1> as reference audio track.

[CUT 1: Intro / Establishing | 00:00 - 00:03]
[Camera movement] — [Character micro-action & eye contact] — [Ambient graphic HUD / typography layers]

[TRANSITION | 00:03]
[Dynamic camera whip pan / glitch smear / geometric split cut]

[CUT 2: Dynamic Action & Rhythm Escalation | 00:03 - 00:06]
[Accelerated camera orbit / tracking] — [Full-body dance or jump-spin motion] — [Bursting color blocks, speed lines]

[TRANSITION / DROP IMPACT | 00:06 - 00:07]
[Audio drop impact sync] — [Shattering particles / radial shockwave]

[CUT 3: Climax & Poster Layout Freeze | 00:07 - 00:10]
[Low-angle hero snap zoom] — [Signature pose & expression] — [Bold 3D title typography lock, halftone dot frame]
```

## Graphic Design Layers (Synthesized from MV Dataset)
Refer to [visual_design_vocab.md](references/visual_design_vocab.md) for full vocabulary:
- **UI & HUD**: Concentric orbital rings, technical telemetry crosshairs, sound visualizer waves, battery/REC status indicators.
- **Typography**: Kinetic Japanese Kanji lyrics, stylized Katakana logos, bold English sans-serif headers, italic speed text.
- **Layouts**: Asymmetric poster cards, vertical triple-split screens, retro OS popups, polaroid scrapbook collages.
- **Medium & Texture**: Crisp cel shading, halftone comic screentones, chromatic aberration glitches, high-contrast duotone.

## Audio-Sync Protocol
When reference audio is provided:
1. Identify the tempo (BPM) and peak drop timestamp (typically between 5.5s - 6.5s in 10s clips).
2. Use `scripts/audio_beat_analyzer.py` on WAV clips to determine exact RMS peaks.
3. Lock the visual transition or whip pan precisely to the drop timestamp.
