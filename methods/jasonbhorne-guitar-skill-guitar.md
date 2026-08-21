---
name: guitar
argument-hint: "<song title> [artist] [options]"
description: >-
  Build an advanced, playable guitar chart for any song the user names, and add
  it to a personal repertoire library. Produces one .md per song with chord
  diagrams, arrangement map, strum/picking pattern, riffs and solos in tab, and
  the chord progression. Activate when the user says "/guitar", "how do I play
  <song>", "how to play <song> on guitar", "guitar chart for <song>", "tab out
  <song>", or "add <song> to my guitar library".
---

# guitar -- song-to-chart breakdowns

The user names a song (or a list of songs); this skill produces an advanced,
fully playable chart and files it in a personal guitar library. Each chart is
self-contained: someone could sit down with it and play the song.

Charts give chord progressions, structure, and technique. They do not reproduce
copyrighted song lyrics -- chart the progression and let the user add lyrics
from a licensed source. Keep song charts personal; do not republish them.

## Inputs

- Required: song title.
- Recommended: artist (disambiguates covers and same-named songs).
- Optional overrides, stated inline: `easy version` (simplify to open chords and
  capo around barre chords), a preferred capo or tuning, or "just the solo" /
  "just the intro" to chart one section only.
- If a title is ambiguous and no artist is given, default to the best-known
  recording and say which one you chose in the Sources section.
- If the user lists several songs, loop the pipeline once per song -- one file
  and one index update each.

Default detail level is advanced: exact voicings, real riffs and solos in tab,
fingerstyle where the song calls for it, and alternate tunings.

## Pipeline

### Step 1 -- Identify the song and set a confidence flag

Work from your own knowledge first. If the song is obscure, or you are unsure of
the exact progression, sections, tuning, or capo, run a `WebSearch` and, if
useful, a `WebFetch` to verify before writing. Then assign a confidence flag:

- HIGH -- a well-known song you can chart reliably and cross-check.
- MEDIUM -- knowledge-based and plausible, but not independently verified.
- LOW -- still uncertain after a lookup. Say so plainly in the chart and tell
  the user which parts to treat as a best guess.

Never present a guessed progression as fact. Flag uncertainty in the chart.

### Step 2 -- Work out the arrangement

Determine and write down: key, capo position, tuning, tempo (BPM), time
signature, overall difficulty, the full list of chords used (with exact
voicings as low-E-to-high-e fret strings), the strum or picking pattern, the
section map (intro / verse / chorus / bridge / outro with bar counts), and the
tab for any intro riff, signature lick, and solo.

For a capo'd song, state both the shape key (chords as fingered) and the
sounding key (actual pitch). For an alternate tuning, name it explicitly.

### Step 3 -- Render the chord diagrams

Build a JSON list of every chord in the song and render all diagrams in one
call. Each item is `{"name": ..., "frets": ..., "fingers": ..., "tuning": ...}`
(`fingers` and `tuning` optional; `frets` is a 6-position low-E-to-high-e string
like `x32010` or `6-8-8-7-6-6`).

```
python3 ~/.claude/skills/guitar/guitar_tools.py diagram --batch chords.json
```

Always pass explicit `frets` -- you know the voicings, and explicit is
unambiguous. The script also has a small `--chord "<name>"` library for quick
single lookups; if a name is not in it, use `--frets`. Paste the rendered
diagrams into the Chord Vocabulary section verbatim.

### Step 4 -- Assemble the chart

Fill in the template below. Tab uses standard ASCII tab (six lines, low E at
bottom, e at top, numbers = frets). The Full Chart section gives the chord
progression by section with bar counts; it does not reproduce lyrics.

### Step 5 -- Save and index

Save to `~/Documents/Guitar/Songs/<Artist> - <Song Title>.md`. Create the
folder first with `mkdir -p ~/Documents/Guitar/Songs`. If a file for this song
already exists, copy it to `<name>.bak` before overwriting.

Then upsert the repertoire index:

```
python3 ~/.claude/skills/guitar/guitar_tools.py index \
  --meta '{"title":"...","artist":"...","key":"...","capo":0,"tuning":"Standard","tempo":120,"difficulty":"Advanced","confidence":"HIGH"}'
```

The script writes `~/Documents/Guitar/Songs/_Index.md` (and a `_index.json`
source file). Re-running a song updates its row in place; it does not duplicate.

### Step 6 -- Report

Tell the user the saved path, the confidence flag, and a one-line difficulty
note (what makes the song easy or hard). If confidence is MEDIUM or LOW, say
which parts to double-check against a recording.

## Song-chart template

```markdown
---
type: guitar-song
title: <Song Title>
artist: <Artist>
key: <sounding key>
capo: <fret number, or none>
tuning: <Standard, or e.g. DADGAD>
tempo: <BPM>
time-signature: <e.g. 4/4>
difficulty: <Beginner | Intermediate | Advanced>
confidence: <HIGH | MEDIUM | LOW>
date-added: <YYYY-MM-DD>
---

# <Song Title> -- <Artist>

## Quick Reference

- Key: <sounding key>   Capo: <fret or none>   Tuning: <tuning>
- Tempo: <BPM>   Time: <signature>   Difficulty: <level>
- Confidence: <flag> -- <one line on what is solid vs. a best guess>

## Chord Vocabulary

<ASCII diagrams from guitar_tools.py, one per chord used>

## Arrangement Map

<Section order with bar counts, e.g.:
Intro 4 bars | Verse 1 (8) | Chorus (8) | Verse 2 (8) | Chorus (8) |
Solo (16) | Chorus x2 | Outro (4)>

## Strumming / Picking

<The rhythm pattern, notated. For strumming use D/U arrows over a count
(1 & 2 & 3 & 4 &). For fingerstyle, give the picking-hand pattern (p-i-m-a).>

## Riffs & Solos

<ASCII tab for the intro riff, signature licks, and the solo. Label each.
Note bends, slides, hammer-ons, pull-offs with standard tab symbols.>

## Full Chart

<The chord progression for every section, with bar counts, labelled by
section. Do not reproduce copyrighted lyrics -- note that the user should
line up lyrics from a licensed source under these progressions.>

## Performance Notes

<Technique tips, tricky transitions, where to breathe, tone and gear notes,
how the recording differs from a solo acoustic rendition.>

## Sources & Confidence

<What the chart is based on (knowledge, specific lookups), which recording was
charted, and exactly which parts are verified vs. a best guess.>
```

## Notes

- No per-song log -- the chart files and `_Index.md` are the running record.
- For an `easy version` request, drop difficulty to Beginner, prefer open
  chords, and use a capo to avoid barre chords; note the trade-off in Quick
  Reference.
- ASCII tab convention: top line is high e, bottom line is low E; read left to
  right; numbers are fret positions; `h` hammer-on, `p` pull-off, `/` slide up,
  `\` slide down, `b` bend, `~` vibrato, `x` muted.
