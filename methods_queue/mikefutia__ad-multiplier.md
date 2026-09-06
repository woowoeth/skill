---
name: ad-multiplier
description: >
  Recast the on-camera talent in a video ad that's already working, and lock everything else.
  Point it at a winning ad (4-30s) plus a reference image of the new person, and it returns the
  same ad with a different presenter: identical shots, cuts, camera moves, product blocking,
  captions, and original audio. Built on Seedance 2.5 via kie.ai, pay-per-render on your own key.
  Trigger on "recast this ad", "swap the creator", "same ad different person", "new talent for
  this video", "multiply this winning ad", or /ad-multiplier.
allowed-tools: Bash(python3 *) Bash(ffmpeg *) Bash(ffprobe *) Read Write AskUserQuestion
---

# Ad Multiplier

**By [Mike Futia | SCALE AI](https://www.skool.com/scale-ai/about)**

One job, done faithfully: take a video ad that already converts and put a different person in it
without disturbing anything that made it work.

**The lock is the default. Every change is an exception you have to argue for, per shot.** That
sentence is the whole skill — the model preserves what it isn't explicitly forced to replace, which
is why the prompt enumerates the keep list and scopes every change to shots and timestamps.

## What it will not do

Read this before promising a client anything.

**Body parts in shots with no face keep the source person.** In a hands-only close-up (pouring,
tearing, applying, unboxing) there is no face to anchor identity, so Seedance preserves the original
person's hands. Tested twice with a dedicated numbered REPLACE op, an explicit pointer to the
reference's own visible hands, and a "must never appear in any frame" negative constraint. It does
not fire. Treat it as a model limitation, not a prompting problem.

This matters because product-handling close-ups are among the most common UGC shot types. **Surface
it at gate 1 and let the user decide** (see below). It also goes wider than skin tone — build, nails
and jewellery persist too.

## 0 — Preflight

```bash
python3 scripts/probe.py <source.mp4>
```

Hard limits (a failure here means the job cannot run at all): duration **4-30s**, **24-60fps**,
≤200MB, 300-6000px per side, aspect ratio 0.4-2.5.

Over 30s is the common failure. Do not silently truncate — say so, and offer to cut a specific
≤30s segment.

## 1 — Analyse the source

Watch the video and extract, at minimum:

- **Shot table** — index, start, end, shot size, camera behaviour (handheld / static / tracking)
- **Cut timestamps** to 0.1s
- **Sub-shot beats** to 0.5s — product entering or leaving frame, hand contacts, named gestures
- **Which shots contain a face**, and which show the person's body with no face ← drives the warning
- **Lighting** per shot and its physical logic
- **On-screen text** — captions, graphics, their styling, placement and timing, or "none detected"
- **Audio** — speech, ambience, music

Beats are what make the lock enforceable. "Keep the timing" is a wish. "Cuts at 7.5 / 9.5 / 10.9;
charm tap at 8.5" is a constraint.

## 2 — Describe the talent reference

Write out the person's externally visible properties: skin tone, hair length/colour/texture, face
shape, brows, makeup level, build, and the exact wardrobe. **Omit anything not visible in the source's
shot types.**

The image supplies the evidence; the text tells the model which evidence matters. Without it the
model may drift the person toward the source's original look, or apply the swap in some shots only.

## 3 — GATE 1: the lock list ← always show this, always stop

```
Source: 8 shots, 26.10s, 720x1280, 30fps, original audio (speech + ambience, no music)

LOCKED
  cuts at 7.5s / 9.5s / 10.9s / 12.9s / 15.2s / 16.5s / 18.5s
  camera: handheld shots 1,2,6,8 - static 3,4,5,7
  beats: pouch enters 7.5 - sachet torn 9.6 - powder hits water 11.0 - straw 13.0 - glass lifts 16.0
  product scale and hand-contact points, per shot
  lighting continuity and direction
  original audio and its sync
  on-screen text: captions bottom-centre throughout + "Melatonin free" graphic 19.3-21.3

CHANGING
  presenter identity + wardrobe   -> @Image1

⚠️ Shots 3-6 (9.5-16.5s, 27% of runtime) show hands with no face in frame.
   Seedance cannot re-identify these; they will keep the source creator's hands.
   -> cast talent with a similar skin tone to the source creator, or
   -> accept the mismatch, or
   -> choose a source ad without face-free body shots.

Approve, or tell me what to move between the lists.
```

## 4 — Compose the prompt

Write it to a file and pass with `--prompt-file`. Structure:

```
@Image1 — PERSON, the person we change to: {full appearance}. Wardrobe: {exact wardrobe}.

Keep this @Video1 clip exactly as it is — the same {N} shots and the same cuts (cuts at {list}),
the same camera moves and handheld/static behaviour per shot, the same framing and composition,
the same product-focused blocking and hand choreography ({named beats}), the same {lighting}
lighting and its direction, the same pacing and timing of every shot, and the same source audio
timing.
Change only: replace the presenter's identity and wardrobe.

Preserve every caption, subtitle, and on-screen text element exactly as it appears — wording,
styling, placement, size, colour, animation and timing{, including the specific graphics}.

1. REPLACE the original presenter — {description of the source person} (all shots, {t0}-{t1}) —
   with PERSON from @Image1, matched beat-for-beat to the original performance: {beat list}.
   Keep the wardrobe exactly: {wardrobe}. {explicit negatives, e.g. "no glasses"}.
2. KEEP the product exactly as it appears, all lettering and colours intact, with identical
   prominence, scale and hand-contact points.
3. KEEP the entire environment unchanged: {furniture, props, depth, perspective}.

Identity lock: the original {source person} must never appear in any frame of the output. Replace
completely, retaining only the original performance, pose, blocking, interactions and timing. Lock
PERSON's exact @Image1 facial identity, hair and proportions across all shots and cuts; do not
duplicate PERSON onto any other figure.

Everything else — camera motion, framing, cut timing, pacing, lighting, environment and all
timing — stays exactly the same.
```

**The opening clause is load-bearing.** Seedance has no mode parameter; it classifies the job from
the prompt. "Keep this clip exactly as it is… change only…" is what selects video-edit mode. Its own
error message says so: *"Seedance identified your task as video editing based on your prompt."*

## 5 — GATE 2 + run

```bash
python3 scripts/run.py --video source.mp4 --talent talent.png \
  --prompt-file prompt.txt --resolution 720p --out recast.mp4
```

It prints a cost estimate and waits for confirmation. **kie.ai has no cost preflight**, so the
estimate is computed from measured $/second — verified against a real charge, and accurate to within
about 20%.

The script uploads both files, submits, polls, downloads, and remuxes the original audio.

## 6 — Report

Close with a diff, not a file path:

```
recast.mp4 · 26.04s · 720p · original audio restored
HELD     cuts 7.5/9.5/10.9/12.9/15.2/16.5/18.5 · camera · lighting · captions · product · environment
CHANGED  presenter identity + wardrobe
KNOWN    hands in shots 3-6 remain the source creator's
COST     ~$X.XX
```

## Non-negotiables baked into the API call

- `aspect_ratio` **must** be `"adaptive"` — any explicit ratio is a hard 400 in edit mode
- `duration: -1` — ratio and duration follow the source; you do not control them
- `generate_audio: false` — always render silent and remux the original, or you get different speech
- Frame rate is **not** preserved (30fps in, 24fps out). Cuts still land correctly.
