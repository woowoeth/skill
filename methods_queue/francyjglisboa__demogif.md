---
name: readme-terminal-gif
description: Create a polished terminal/CLI demo GIF for a GitHub README or docs — record or replay a real command and its output as an asciinema cast, render to an animated GIF with agg, and verify the frame. Use when the user wants a demo GIF, terminal recording, asciinema/agg cast, animated CLI demo, or "show the tool running" in a README. Covers both the real-capture path (streaming CLIs) and the readable-replay path (buffered tools that dump output). Enforces an honesty rule — the GIF must show genuine command output, captioned accurately. Not for TUI/browser/GUI screen capture.
---

# README terminal GIF

Make a crisp, honest terminal demo GIF for a README. Pipeline:
**capture real output → build an asciicast (record real, or replay via storyboard) → render to GIF (agg) → verify a frame → embed with an accurate caption.**

Scripts live in `scripts/`. Detailed flags, gotchas, and a worked example are in `references/reference.md` — read it before debugging any rendering oddity.

## 0. Preconditions

- `command -v asciinema agg` — both required. Install: `brew install asciinema agg`. If you cannot install them, tell the user; do not fabricate a GIF.
- Know the exact command to demo and confirm it actually works (run it once for real first).

## 1. Capture the REAL output

Run the actual command and save its genuine output:
```bash
mytool query "how does X work?" > /tmp/answer.txt
```
This text is the source of truth. **Never hand-write or embellish output** — a fake "real" demo on a serious repo is a credibility hit, the exact opposite of the GIF's purpose.

## 2. Choose the path — this is the key decision

**Real-capture path** — when the tool *streams to a TTY in real time* (progress bars, a REPL, a fast CLI). The recording IS the demo:
```bash
scripts/record_real.sh /tmp/demo.cast -- bash -c 'echo "$ mytool sync"; mytool sync'
```
Caption it as a real capture.

**Replay path** — when the tool is *buffered*: it sits idle for seconds then dumps all output at once (LLM print-mode CLIs, slow build tools). A raw capture is then mostly dead air + an unreadable blob. Instead, re-pace the verbatim real text with a JSON storyboard:
```bash
# storyboard.json references /tmp/answer.txt and sets per-line pacing — see references/reference.md
scripts/make_cast.py storyboard.json --out /tmp/demo.cast
```
Caption it as a **replay** (timing illustrative), with the output text noted as verbatim.

When unsure which path: if running the command shows text appearing smoothly as it computes, use real-capture; if it pauses then dumps, use replay.

## 3. Render to GIF

```bash
scripts/render.sh /tmp/demo.cast assets/demo.gif
```
Defaults are tuned for README scale (small font, trimmed idle, asciinema theme). For a long real run add `--speed 2`. Keep it ≤ ~30s and well under ~500 KB.

## 4. Verify — never skip

Rendering succeeds silently even when the result is blank, shows literal `[36m` ANSI codes, or clips. Look at it:
```bash
scripts/check_frame.py assets/demo.gif /tmp/frame.png 0.8
```
Then actually view `/tmp/frame.png` (read it with an image-capable tool). Confirm: real text visible, colors applied (not literal codes), no mid-word clipping. If wrong, see the symptom→cause table in `references/reference.md`.

## 5. Embed with an honest caption

```markdown
![what the tool does](assets/demo.gif)

> A real `mytool query` against … — genuine output, zero setup.            ← real-capture path
> A replay of a real `mytool query` — output verbatim; timing illustrative. ← replay path
```

## The honesty rule (non-negotiable)

The whole value of a demo GIF is that it proves the tool works. So:
- Output text shown is always genuine (captured from a real run).
- "Real capture" caption only for a literal recording; otherwise say "replay … timing illustrative."
- A truncation marker (`… continues`) is fine; fabricated output never is.

Getting caught with a staged "real" GIF destroys the credibility you were buying.
