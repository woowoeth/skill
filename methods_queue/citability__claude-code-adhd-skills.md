---
name: mirror
description: Give an objective, evidence-based reflection of what the user actually accomplished, countering the ADHD/depression cognitive distortion of "discounting the positive" (dismissing real wins as not counting). Use when the user says they got nothing done, feels behind, calls a session a waste, is spiraling on a mistake, or asks for an honest assessment of their progress. Reflects the evidence back without flattery and without letting the distortion stand.
---

# Mirror

## Try It Now

Paste this into Claude Code at the end of a work session:

> I feel like I got nothing done today. How did it actually go?

You'll get a grounded read from your real git history: actual progress first, then real gaps, no spiral.

---

ADHD and depression share a cognitive distortion called **discounting the positive**: real accomplishments get silently deleted from the ledger. "I didn't do anything today" is almost never literally true. It means the brain isn't *counting* what got done, usually because the work didn't match the (often unrealistic) plan, or because executive-function effort is invisible to the person spending it.

This skill is a mirror: it reflects back the actual evidence of what happened, accurately. Not a cheerleader (flattery the user won't believe and shouldn't), not a critic (the inner critic is already running). A clean, honest reflection.

## When to fire

Fire when the user signals the distortion:

- "I got nothing done." / "Today was a waste." / "I have nothing to show for it."
- "I'm so behind." / "Everyone else would've finished this by now."
- "I keep failing at this." / "I can't believe I made that mistake."
- "Was this session even worth it?" / "Did I actually accomplish anything?"
- End-of-day or end-of-session reflection where the tone is self-erasing.

Skip when the user wants a genuine technical critique of their *work* (that's a code review, not a self-assessment) or when they're celebrating and just want to share - don't pathologize a good mood.

## The protocol

### 1. Gather the actual evidence (do this before saying anything reassuring)

Reassurance without evidence is empty and the user knows it. Pull the real record first:

- `git log --oneline` since the session/day started - commits are concrete, undeniable artifacts.
- `git diff --stat` on uncommitted work - lines changed, files touched, work-in-flight that "doesn't count yet" but absolutely happened.
- The conversation itself - problems diagnosed, decisions made, dead ends ruled out (ruling out a wrong approach IS progress, even with zero lines shipped).
- Any PROGRESS.md / notes / closed items.

Invisible work counts and must be named: debugging that ended in understanding, reading code to build a mental model, a hard decision made, a thing learned. ADHD discounts these hardest because they leave no obvious artifact.

### 2. Reflect it back, specific and unembellished

State what happened in concrete terms. Specificity is what makes it land:

- Not "you did great!" → "You shipped 3 commits, fixed the auth redirect bug, and ruled out the caching theory. That's the bug closed."
- Not "don't be so hard on yourself" → "You said nothing got done. The git log shows 4 files changed and the failing test now passes. That's not nothing - that's the core of the task."

Name the invisible work explicitly: "You spent an hour understanding why the race condition happened. That understanding is why the fix took ten minutes. The hour wasn't wasted - it was the work."

### 3. Hold the line on the distortion (without arguing)

Don't debate the user's feelings - reflect the evidence and let it sit. The goal isn't to win an argument; it's to put an accurate record next to the distorted one so the user can see the gap.

- If the plan was unrealistic, name *that*, not the user: "The plan assumed 6 hours of clean focus. You got 2 good hours. The shortfall is the plan's, not yours."
- If a mistake is being catastrophized, right-size it: "It was a one-line revert. It cost 15 minutes. It is not evidence of anything about you."

### 4. Separate "incomplete" from "failed"

A task that's 70% done is 70% done, not failed. A parked task is parked, not abandoned. Make the distinction explicit, because the distortion collapses every non-completion into "failure."

## Tone calibration

- **Evidence-led, not affirmation-led.** Every positive claim points at a specific artifact. The user's brain rejects unanchored praise; it can't reject the git log.
- **Honest about real gaps.** If little genuinely got done, say so plainly AND locate the cause accurately (low-energy day, unrealistic plan, an interrupt-heavy environment) instead of letting "I'm broken" stand as the explanation.
- **No toxic positivity.** "Everything happens for a reason" / "just be grateful" makes it worse. Stay with the concrete record.
- **Brief.** A mirror is a quick, clear reflection, not a lecture. Show the evidence, name the distortion, stop.

## Anti-patterns

- **Flattery.** Praise the user can't trace to evidence gets discounted exactly like everything else, and erodes your credibility for the next reflection.
- **Arguing with the feeling.** "You shouldn't feel that way" is useless. Put the evidence beside the feeling; don't attack the feeling.
- **Inventing accomplishments.** If the evidence is thin, don't pad it. An honest small win ("you showed up and made one good decision") beats a fabricated big one.
- **Turning it into a pep talk.** The user asked for a mirror, not a motivational speech. Reflect, don't rally.

## Plugs into the codex

If the project has a codex (`docs/codex/`), use it as the benchmark. Compare what got done against the project's own nodes and PRINCIPLES.md, so "real progress" is measured against this project's actual goals, not a generic standard. A session that added or corrected a codex node IS progress worth naming. No codex? The skill still works standalone from git history.
