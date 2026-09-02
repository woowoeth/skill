---
name: analyze-song
description: Use when the user wants to recreate a song's guitar tone on a Quad Cortex and needs the song analyzed first — researches the gear/rig (web + Cortex Cloud), optionally separates and analyzes the audio (guitar stem, tempo, key), and produces a structured, source-tagged song tone profile. Run before build-signal-chain.
---

# Analyze Song — Tone Profile

## Overview

Produce a **song tone profile**: the song's parts, the guitar tone of each, the real gear
behind them (with sources), tempo/key, and how that gear maps to **documented QC modules**.
This profile is the input to quad-cortex:build-signal-chain.

**REQUIRED BACKGROUND:** quad-cortex:qc-guitar-rig (strat/pickup context + how parts become
scenes).

**Core honesty rule:** every gear/tone claim carries a confidence tag
(**[verified] / [likely] / [speculative] / [unknown]**); audio-derived numbers are
**[estimate]**. Never invent gear, settings, or module names. An unknown stays unknown.

## Workflow

1. **Identify** artist, song, and a source. **No source provided ≠ skip audio.** Before ever
   falling back to research-only, *get* a source: search the web for the official track audio
   and pass a **YouTube URL straight to `qc-analyze-song analyze`** (it downloads via yt-dlp), or
   ask the user for a URL/file. "Research the song online" includes finding the audio to analyse.
2. **Audio — the default path, not optional.** ALWAYS run `qc-analyze-song check` first (never
   assume the toolchain's state) — don't trust a remembered/earlier "research-only"; re-run it.
   The commands run via `uv` from the cortexrig checkout, which resolves the project venv, so
   tools installed there are used. Run the pipeline whenever `check` reports `audio-pipeline-ready`:
   ```bash
   uv run qc-analyze-song check
   # ALWAYS use a per-song output dir — never a shared one. Pass tmp/<song-slug> explicitly,
   # or omit it and the command derives tmp/<title-slug> from the source title.
   uv run qc-analyze-song analyze "<url-or-file>" "tmp/<song-slug>"
   ```
   **Never reuse one output dir across songs** (e.g. the old `tmp/analysis`): yt-dlp skips the
   download when `source.wav` already exists, so the pipeline would silently separate and analyse
   the *previous* song. The command now derives a per-song dir and clears a dir whose `.source-id`
   differs — but still give each song its own dir. Sanity-check `duration_sec`/tempo against the
   real track to catch a wrong-source run.
   Use the guitar stem, `features.json` (tempo/key), `features_guitar.json` **and
   `features_other.json`** (per-stem tempo/key **+ modulation + drive** — the pipeline now writes
   a features file for the `other` stem too), and MIDI. See
   [references/audio-pipeline.md](references/audio-pipeline.md). **A crunchy electric often hides
   in the `guitar` stem (blended with acoustic) or leaks into the `other` stem — analyse both,
   don't assume the electric is cleanly isolated.**
   - **Demucs cannot separate two guitars.** When a song has **both an acoustic and an electric**,
     they land in the *same* `guitar` stem. If the acoustic is louder/brighter it **dominates the
     stem's crest factor and HF read**, so a *driven* electric sitting behind it reads as "clean /
     edge-of-breakup" — the classic trap. Do **not** characterise the electric from the blended
     stem's drive number. Instead: (a) find a passage where one guitar drops out (e.g. an
     electric-only outro/solo) and read the drive *there*; (b) lean on gear research (a maxed
     boost into a cranked amp is *always* grinding, verses included); (c) ask the player. State
     explicitly that the blended-stem read is acoustic-led, not the electric in isolation.
     (This exact miss happened once: "The Chain" verses were called a clean electric when the
     electric was a crunch buried under the bright acoustic — corrected only after the player
     pushed back.)
   **Only go research-only if `qc-analyze-song check` *itself* reports `research-only`** (tools
   genuinely absent) **or** no source can be obtained — and then say which of the two it is and
   how to fix it (install the ✗ items via `task setup` / `task setup-audio`, or provide a source).
   Don't conflate "no source handed to me" with "audio impossible."
   - **LISTEN to the guitar stem before characterising tone.** The pipeline renders
     `guitar.mp3` (and `other.mp3`) automatically — play them, and **send them to the user too**
     (SendUserFile) so they can hear the part. Spectral averages (centroid/flatness) describe
     *timbre* only — they are **blind to modulation** (tremolo, auto-pan, vibrato, rotary), which
     a multi-second average erases. Check `features_guitar.json → modulation` for a flagged
     tremolo rate, and confirm by ear.
   - **If you cannot actually hear the audio (headless/agent run), do not assert clean-vs-crunch
     or modulation from the numbers as if you'd listened.** Send the stem with `SendUserFile`,
     state the measured estimate, and **ask the player to confirm** — the drive/modulation figures
     are inputs to a human ear, not a verdict on their own.
   - **Clean vs. breakup/crunch: use the `drive` block (crest factor + sustained >2 kHz energy),
     NEVER spectral flatness.** Clean and distorted guitar are both harmonic → flatness is low for
     both, so it can't tell them apart. Low crest (~4–7) + sustained HF = broken-up/crunch; high
     crest (~10+) + low HF = clean. Check `drive → by_quartile` for a clean-verse-vs-driven-solo
     split, and confirm by ear. **Caveat:** crest factor is a *whole-stem* statistic — a loud
     bright acoustic in the same stem inflates it and hides a driven electric underneath (see the
     "Demucs cannot separate two guitars" note above). Compare the `guitar` and `other` stems, and
     trust a quartile only where one instrument clearly dominates.
   - **Actively rule each effect family in or out** — don't just report brightness/gain. Run
     through: tremolo/auto-pan (envelope pulse), vibrato/chorus/phaser/rotary (pitch/comb
     movement), wah (fixed or swept formant), delay (repeats), reverb (tail). Name each as
     present/absent rather than leaving it unmentioned.
3. **Gear research (exacli):** rig rundowns, interviews, tab/gear sites — escalation ladder in
   [references/research-playbook.md](references/research-playbook.md). Tag every fact + source.
   - **Always research tuning + capo** (search `"<song>" tuning capo`, lesson/tab sites) — never
     default to "standard tuning." Altered tunings and a capo are common and they change how the
     part is played and reasoned about. **Reconcile the finding with the audio key estimate**: a
     capo or a drop tuning explains an unexpected key (e.g. Double Drop D + capo 2 sounds in E —
     so the analysis reading "E" is consistent, not contradictory). Tag tuning [verified] only
     with a source; otherwise [likely]/[unknown], not a silent "standard."
4. **Cortex Cloud (if a browser MCP is connected):** look for existing song presets —
   [references/cortex-cloud.md](references/cortex-cloud.md). Skip gracefully if no MCP.
5. **Map gear → documented QC modules** using the category skills (qc-amps-cabs,
   qc-drives-fuzz, qc-modulation, qc-time-based, qc-utility, qc-bass-amps-cabs). Verify every
   name against their `references/modules.md`; flag substitutions and gaps.
6. **Write the profile** from [assets/song-profile-template.md](assets/song-profile-template.md):
   overview, musical facts, guitar/pickups, **section→part map**, per-part gear evidence,
   mapping notes, open questions. Write **render-safe markdown** (match the template): no `>`
   blockquotes, `[label](url)` links not bare URLs, and keep each `**bold**` span on one line.

## The part map (most important section)

Distill the song into **distinct guitar tones** — each becomes a **scene** later
(max 8 per preset). Merge sections that share a tone. For each part capture: tone-in-a-line,
gain level, and notable FX, with the closest pickup choice (5-way) and VCC switch setting for
the Blade California Custom (see quad-cortex:qc-guitar-rig → blade-california-custom.md).

## Output

A completed song tone profile (Markdown). Offer to pass it to quad-cortex:build-signal-chain.

## Common mistakes

- **Skipping audio because no source was attached** → wrong. Search for the track (YouTube URL →
  `qc-analyze-song analyze`) or ask. "No source given" is not "audio impossible."
- **Declaring research-only without running `qc-analyze-song check`** → never assume the toolchain
  is missing. Run it; `uv` resolves the project venv where the tools live, so a stale earlier
  result (or a bare-`PATH` guess) gives a false negative.
- **Saying "no audio because no file/URL supplied" when the real blocker is tools** → name the
  actual reason (missing tools vs missing source) and the remedy. They're different fixes.
- Presenting tempo/key or MIDI as fact → they're **[estimate]**; verify if it matters.
- Filling an unknown amp/pedal with a guess → leave it **[unknown]**.
- Naming a QC module from memory → only names in the category `references/modules.md` are real.
- Over-claiming from a stem with bleed → describe only what you actually hear.
- **Characterising tone from spectral stats alone** → centroid/flatness/RMS capture timbre and
  level but are **blind to modulation**. A steady ~6 Hz tremolo averages out to a flat number.
  Always render + listen, and check `features_guitar.json → modulation`. (This exact miss
  happened once: a deep verse tremolo was reported as a plain "dark clean.")
- **Calling clean vs. distorted from spectral flatness** → flatness is low for clean AND for
  crunch (both are harmonic), so it can't discriminate them. Use the `drive` block (crest factor
  + sustained >2 kHz energy) instead. (This exact miss happened once: a broken-up crunch rhythm
  was reported as a "warm clean" off low flatness — corrected only after the player pushed back.)
- **Assuming the electric is cleanly isolated in the `guitar` stem** → a clean acoustic and a
  crunchy electric can share the `guitar` stem, and a distorted electric often leaks into `other`.
  Analyse both stems (`features_guitar.json` + `features_other.json`) when the electric tone is
  what matters. A loud acoustic in the blend inflates the crest factor and **hides a driven
  electric** — read drive where one instrument dominates (e.g. the electric-only outro), and never
  call the verses "clean" off a blended stem alone.
- **Defaulting to "standard tuning" without researching it** → altered tunings + capo are common
  and change everything downstream. Search `"<song>" tuning capo` and reconcile with the audio key
  (a capo/drop tuning explains an "unexpected" key). (This exact miss happened once: "The Chain" is
  Double Drop D + capo 2, reported as standard tuning until the player corrected it.)
- **Reusing one output dir across songs** → yt-dlp skips the download when `source.wav` already
  exists, so the whole pipeline silently analyses the PREVIOUS song. (This happened once: a run
  for "The Chain" actually analysed a leftover "You Oughta Know" — caught only when the user
  recognised the stem.) Use a per-song dir, and sanity-check `duration_sec`/tempo vs. the real track.
- Mistaking "slight movement" in research notes for chorus → it may be **tremolo/auto-pan**;
  measure the envelope rate before naming the effect.
