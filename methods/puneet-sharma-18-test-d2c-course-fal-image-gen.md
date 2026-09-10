---
name: fal-image-gen
description: Generate real images and short videos via fal.ai. Use when the founder needs a shippable asset (ad creative, PDP hero, reel, packaging mockup, festive poster) rather than a described one. Triggers on phrases like "generate an image", "make me a creative", "draw a hero shot", "render the ad", "generate a video", "animate this", "make a reel". Optional add-on: needs a fal.ai key. Without one it hands back a finished prompt to paste into any image tool. This is a thin caller — the agent invoking it composes the brand-aware prompt.
---

You wrap a Python script that calls fal.ai and puts a real file on disk. You do not compose prompts and you do not apply brand voice — the caller does that. You take a prompt, an output path and a few flags, and you produce an asset.

**This skill is optional.** It needs an API key and one system tool. If either is missing, you still finish the job — see step 1.

## Step 1. Check you can actually run, before promising anything

Two things have to be in place:

1. **`FAL_KEY`**, either exported in the shell or in a `.env` file in the brand folder. Keys come from the fal.ai dashboard. The script auto-loads `.env` from the working directory; a shell export wins over the file.
2. **`uv`** installed. macOS `brew install uv`, Windows `winget install --id=astral-sh.uv -e`, otherwise the installer at docs.astral.sh/uv. The Python dependency is declared inline in the script, so `uv run` builds its own environment on first call. There is no `pip install` step.

**If either is missing, do not fail and do not stall.** Say plainly what's absent, then deliver the prompt anyway:

> "I don't have a fal.ai key set up, so I can't render this here. The prompt below is finished and ready — paste it into Midjourney, ChatGPT, Gemini, or whichever tool you already use. If you'd rather render from here, set `FAL_KEY` in a `.env` file in this folder and ask again."

Then give them the complete prompt, formatted to paste. A founder who never sets up a key still walks away with the thing that took the thinking. The key only changes *where* the pixels get made.

**Never install `uv` silently.** If `uv run` fails with "command not found", surface it, quote the install command, and ask before running it — even when the session would otherwise let you act without asking. Installing a system tool is the founder's call, not yours.

## Picking a mode

| Mode | Model | For |
|---|---|---|
| `t2i` | Flux dev | Photography-style lifestyle, hero shots, product-in-scene. **Cannot render legible text.** |
| `poster` | GPT Image 2 | Festive creatives, sale cards, anything where a headline is part of the artwork. English and Devanagari render cleanly. |
| `i2i` | Flux dev i2i | A new image anchored to a reference's style, palette and composition. Fanning an approved hero out across other products. |
| `t2v` | Kling 3.0 Standard | Short ad video, reel hero, B-roll. Native audio. |
| `i2v` | Kling 3.0 Standard | Animating an approved still into 6 to 8 seconds of motion. |

Do not use video modes for diagrams, flowcharts or anything typographic. Video models are good at organic motion — steam, drift, parallax, fabric, light shifts — and unreliable at rendered text. For a typography-first creative, make the still in `poster` mode and animate it after if you need to.

## Running it

The script sits at `.claude/skills/fal-image-gen/fal_run.py`.

**Image:**
```bash
uv run .claude/skills/fal-image-gen/fal_run.py \
  --prompt "<the full brand-aware prompt>" \
  --output "<path/to/output.png>" \
  --aspect <1:1|4:5|9:16|16:9|3:4>
```
Defaults: `--mode t2i`, `--aspect 1:1`.

**Poster with legible text:**
```bash
uv run .claude/skills/fal-image-gen/fal_run.py \
  --mode poster \
  --prompt "<headline in quotes, layout, palette, exclusions>" \
  --output "<path/to/output.png>" \
  --aspect 4:5 --quality high
```
Put the headline in quotes so it renders verbatim. Describe the typographic mood — "block sans-serif, centred, lower third", "ornate Devanagari title at top, ingredients bottom-left". Use `low` or `medium` quality while burning through variants, `high` on the winner. For Tamil, Telugu, Bengali, Punjabi, Gujarati, Odia, Malayalam or Kannada, generate the background here and overlay the script in a real design tool — those don't render reliably.

**Variation from a reference:**
```bash
uv run .claude/skills/fal-image-gen/fal_run.py \
  --mode i2i \
  --reference "<path or URL>" \
  --prompt "<what changes: new product, same plate, same light, same composition>" \
  --output "<path/to/variant.png>" \
  --strength 0.75
```
Aspect inherits from the reference. `--strength` is the only knob: 0 returns the reference untouched, 1 ignores it entirely. A local file gets uploaded automatically; a public URL is fetched directly.

**Video:**
```bash
uv run .claude/skills/fal-image-gen/fal_run.py \
  --mode t2v \
  --prompt "<subject, motion, light, mood, exclusions>" \
  --output "<path/to/output.mp4>" \
  --aspect 9:16 --duration 6s
```
Durations 4s, 6s or 8s. `--no-audio` to mute. `--negative-prompt` for explicit exclusions. For `i2v`, add `--reference` and keep the motion prompt small and physical. Kling rejects `auto` for aspect, so pass `16:9` or `9:16` explicitly.

Start video tests at `--duration 4s` and scale up only on the winner. Video is meaningfully more expensive than image, and a bad six-second clip costs the same as a good one.

## The strength knob and rendered text

This is the non-obvious one, and it has caught people out.

Flux cannot render legible copy at any strength. But at *low* strengths it tries to preserve the letter shapes in your reference, which produces something worse than dropping them:

| `--strength` | What happens to text in the reference |
|---|---|
| 0.85 to 0.95 | Reference text and graphic overlays are cleanly **dropped**. You get a photo in the reference's brand world, no inherited copy. Composite real text afterwards. |
| 0.50 to 0.80 | The model **tries to keep** the letter shapes. Output looks right from across the room and reads as gibberish up close. |
| Below 0.50 | Worse gibberish, and the image content mostly echoes the source. |

Tested case: an ad with a rendered headline, a brand mark and a labelled arrow, run three ways. At 0.85 the copy dropped cleanly and the output was usable. At 0.65 the brand world came through beautifully — right palette, right composition, right shapes — and the headline rendered as plausible-looking nonsense. The same headline through `poster` mode, prompt-only with no reference, rendered perfectly.

**The rule.** If you need the reference's copy preserved, use `poster` mode with the headline written verbatim into the prompt, and accept that you lose the reference channel. If you want a clean photo and will add text in a design tool later, use `i2i` at 0.85 or above. Never sit in the middle — that band produces the one output that looks fine in a thumbnail and falls apart when anyone looks at it.

## Where reference images live

Anywhere works. The useful convention: persistent brand anchors — approved hero shots, mood boards, winning ad screenshots — in a `brand-brain/visual-refs/` folder; a previously-winning ad in whatever folder the Performance Marketer already reads; anything generated earlier in the same session in that run's own output folder, passed by path. A hosted URL works too and skips the upload.

If none of those folders exist, ask the founder to drop the reference into the conversation and use it from there. Don't make them build a folder structure to render one image.

## Output

One JSON line to stdout on success, carrying the output path, mode, model, format flags and the fal-hosted URL. PNG for images, MP4 for video. On failure, JSON to stderr and a non-zero exit — read the error rather than retrying blindly.

## Swapping models

Two ways: `--model <slug>` for one call, or edit the `MODEL_DEFAULTS` dict near the top of the script to change a mode's default permanently.

The durable reasoning, which outlasts any specific model: **the cheap video model is roughly five times cheaper than the premium one.** That maths only flips for the one hero asset a quarter where quality is the entire point. Weekly ad variants run on the cheap model, the annual brand film does not. The same logic applies to image models — the upgrade targets earn their cost on a hero PDP shot, not on the twentieth A/B variant.

Common upgrades: a stronger Flux or Gemini image model for a quarterly hero shot; Gemini for Devanagari festive work where typography *is* the creative; GPT Image 2 with edit arguments when the job is "change this poster's price" rather than "make a new variant"; Veo for a hero video.

**Model names and prices in this file are a snapshot and they move fast.** Check current pricing on the fal.ai dashboard before committing to a run of any size, and re-check which model wins each job before assuming these defaults are still right.

## The prompt is the caller's job

This skill is deliberately dumb. Whatever prompt arrives is what fal receives, unmodified.

A good prompt names the specific product and its real ingredients, the brand's mood and palette, the format it's for, and the banned imagery as plain exclusions inside the prompt itself. "A paan product photo" is a bad prompt. "Hand-rolled meetha paan on a brass plate, warm afternoon kitchen light, shallow depth of field, rose petals and slivered almonds visible, no tobacco, no spitting, no stained surfaces" is a good one.

The Creative Brief skill and the Performance Marketer both produce prompts in exactly this shape. Prefer taking one of theirs over composing from scratch — they have already read the brand profile and the anti-positioning.

## How you work

- **One asset per call.** No batching. The caller loops.
- **No prompt rewriting.** What arrives is what gets sent.
- **No retries.** Failures surface to the caller, who decides.
- **No silent installs.** Ever. Quote the command and ask.
- **Cheap first.** Small, fast, low quality while exploring. Spend on the winner.
- **A missing key is not a dead end.** Hand over the prompt.
