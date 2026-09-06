---
name: image-loop
description: Turn a still image or photograph into a seamless hypnotic loop by warping its own pixels with a periodic displacement field, then compositing rhythmic falling particles on top. Use this skill whenever someone supplies, uploads, attaches, or points at an image and wants it animated, looping, breathing, moving, alive, or turned into a living wallpaper, a looping video, an animated background or an ambient GIF — including "animate this photo", "make this picture loop", "add falling particles to this image", "can you make this move", "anima esta foto", "faz essa imagem se mexer". Also use it when someone shows a looping video they want reproduced from a frame of it. Do NOT use it to generate a scene from scratch with no source image — that is the sibling `hypnotic-loop` skill — and do not use it for cross-fades, Ken Burns pans, or slideshow transitions, none of which are this genre.
---

# Image-driven hypnotic loop

The scene is not rebuilt from the image; the image itself is deformed. Every output
pixel reads from the source at an offset that is a periodic function of loop phase, so
the pixels stay photographic while the mass appears to breathe. Then the particle
layers go on top, because a warp alone never carries enough rhythm.

This is the Tier 2 approach: it gets most of the reference's effect from any suitable
still, at the cost of one real limitation — **a warp cannot reveal what is behind
anything**. There is no per-flower rotation about a stem base, only coherent local
drift. At 3–8 px of displacement in a dense mass that difference is very hard to see;
push the amplitude higher and it becomes obvious stretching.

Loop safety is inherited from the sibling skill's contract, which applies here
unchanged. Read `../hypnotic-loop/references/loop-math.md` before modifying any
formula, and `../hypnotic-loop/references/export-and-verify.md` for encoding.

## Workflow

1. **Check the input is suitable** before promising anything. A good source has a
   large contiguous dark or low-detail region, a dense mass of saturated texture, and
   no baked-in particles. Tell the person if it does not — a bright evenly-lit photo
   will produce a weak result no matter how well the warp is tuned.
2. **Crop UI chrome and watermarks.** Screenshots of videos carry play buttons, GIF
   badges and timestamps. They warp along with everything else and look broken.
3. **Analyse**: `python3 scripts/analyze_image.py photo.jpg --out work/`
   Read the printed numbers and check `work/diagnostic.png`, which puts the source,
   the amplitude mask, the phase field and the masked source side by side. The mask is
   the thing to judge: the dark region must be black in it.
4. **Respect the amplitude ceiling** the analysis prints. It is derived from how
   steeply the mask changes, because local stretch is `amp × |∇mask|`. If the ceiling
   is lower than you want, re-run with a larger `--mask-blur` — a smoother mask buys
   more amplitude. That is the main tuning lever and it is not obvious.
5. **Tune** in `assets/warp-bench.html` (drop in the image plus `mask.png`,
   `phase.png`, `phase2.png`). It runs the identical formula in a shader and prints the
   `warp_loop.py` command for the settings you land on. No particles there by design.
6. **Render**: `python3 scripts/warp_loop.py photo.jpg --work work/ --out frames/
   --frames 360 --amp <ceiling from step 2>` — never above the printed ceiling.
   The renderer probes two frames first and warns if predicted motion is below
   the audit floor, before spending the full render.
7. **Audit**: `python3 ../hypnotic-loop/scripts/loop_check.py frames/`
   Seam ratio must be at or near 1.0. Image loops usually land at the low end of the
   motion budget (0.004–0.010) — that is expected and fine; the floor exists to catch
   a loop that is effectively frozen.
8. **Encode** with the ffmpeg recipes in the sibling reference, and report the audit
   numbers with the file.

## What the analysis derives

| Output | How | Used for |
|---|---|---|
| amplitude mask | product of saturation, local detail energy, an adaptive luminance gate and a depth ramp, then blurred hard | what moves and how much |
| phase fields | travelling wave across x plus a smooth seeded random field | when each region moves |
| accent colour | k-means over bright saturated pixels, most luminous cluster | particle colour, so it matches a hue already in the image |
| mass top edge | per-column sustained-brightness threshold, smoothed across x | the depth ramp |
| amplitude ceiling | `0.06 / p99.9(|∇mask|)` | the honest limit on `--amp` |

The luminance gate is adaptive rather than a constant: it uses a percentile of *this*
image, so a bright photo and a dark one both get a sensible sky threshold. The depth
ramp exists because uniform breathing reads flat; motion has to grow toward the
foreground exactly as it does in the synthetic scene.

## Tuning

| Symptom | Change |
|---|---|
| Dark region visibly wobbles | raise `--dark-pct`; check the mask is black there in `diagnostic.png` |
| Visible stretching or jelly at the sky boundary | lower `--amp`, or raise `--mask-blur` and re-render |
| Whole image breathes as one | raise `--wave-travel` (1.0–2.0 is the useful band) |
| A visible stripe sweeps across | lower `--wave-travel` below ~2.5 |
| Motion below the audit floor | raise `--mask-blur` first (it lifts the ceiling), then `--amp`, then `--rain` |
| Reads as sliding, not breathing | raise `--vertical` toward 0.4 |
| Particles look pasted on | let the accent come from the image; do not override `--accent` unless the k-means picked a colour that is not in the mass |
| Source already has rain streaks | `--rain 0`, or they double up and the baked ones will not fall |

`--rain 0` is the right default for frames taken from videos in this genre, since they
almost always already have streaks. Motes composite fine on top either way.

## Files

    scripts/analyze_image.py   mask, phase fields, accent, diagnostics, amplitude ceiling
    scripts/warp_loop.py       the renderer: periodic warp plus particle layers
    scripts/imagelib.py        shared numpy helpers (blur, smoothstep, fields, resampling)
    assets/warp-bench.html     WebGL tuning bench, identical formula, no particles
    references/warp-fields.md  the displacement field, mask construction, the stretch limit

Dependencies: numpy and Pillow only. No scipy, no node, no browser required for the
render path. ffmpeg for encoding.

## Honest limits

- No parallax and no occlusion recovery. Foreground objects cannot slide across
  background objects.
- Large single objects deform rather than move. The genre's density is what hides this;
  a photo of three big flowers on a plain background will look like jelly.
- Baked motion blur in the source stays baked, and it will wobble.
- The vertical component is a shallow figure-of-eight, not a pendulum arc. True arc
  coupling was tried and removed: at 4–6 px displacement the dip term contributes
  under 0.2 px, so it cost complexity and bought nothing measurable.
