---
name: good-boss-prompting
description: A structured abduction workflow for "why" questions where the cause or frame is unknown. Prevents the AI from collapsing onto the single most probable explanation by forcing it to first generate a large batch of anomalies and hypotheses, and hands the actual selection back to the human. Use this whenever the user says things like "I have no idea why this happened," "I don't even know what to ask," "this doesn't match what I expected," or asks for root-cause analysis, hypothesis generation, or anomaly discovery — even if they never say the words "hypothesis" or "abduction." Applies whenever the user genuinely doesn't know the cause, regardless of whether the question is phrased as why/what/how. Do NOT use this when the user already knows the answer and just wants confirmation, or when they're asking about a rule, definition, or method (a real what/how question).
---

# Good Boss Prompting

When an AI is asked "why?", it converges on the single most probable explanation. This skill exists to block that convergence. The AI's job is to mass-produce candidates — not to answer. The human keeps the final call, the way a good manager delegates the legwork but never signs off decisions on someone else's behalf.

## Step 0 — Decide whether this applies

Use this workflow only when one of these is true:

- You genuinely have no idea why something happened
- You don't even know what question to ask
- Something happened that doesn't match what you expected, and you don't know why

**Do not use this when:** the user already knows the answer and just wants it confirmed, or they're asking about a rule, definition, or method (a genuine what/how question). In those cases this workflow is a net loss — just answer directly.

Judge by what the user actually doesn't know, not by the surface grammar of the question. A question phrased with "why" can still be a confirmation request if the user already suspects the answer. A question phrased as "analyze this" can still be a real abduction case if the user has no working theory at all.

## Step 1 — Generate 20 anomalies

If the material has no concrete facts or numbers to work from, stop here and ask for more material instead. Candidates generated without real input are just invented.

Each item is one line, in this exact format:

```
Expected: / Actual: / Gap:
```

Rules while generating:

- Do not explain causes yet — the moment an explanation appears, the search stops
- Do not rank items or flag which ones matter — that is the human's call
- Do not use bold text, "especially notable," or any other implicit ranking — that's still a ranking
- Do not count a reworded version of the same underlying mechanism as a new item. The thing to avoid is duplicate *mechanisms*, not duplicate *wording*
- Do not discard anything just because it looks strange
- Let items contradict each other — do not reconcile them
- Cover at least six domains, with at least 2 items each: money, human behavior, competition, time lag, rules/regulations, physical/supply flow. Concentrating in one domain defeats the purpose
- Do not use summary words like "analysis," "insight," or "takeaway"

## ★ Stop here. This is not optional.

<!-- Maintainer note: this is the single highest-risk line in the skill. Every failure mode described in "What this skill does not do" traces back to the AI skipping this stop point — most commonly when the user says something like "just handle the rest yourself." Do not soften this instruction, move it into a bulleted rule alongside the others in Step 1, or shorten it for brevity. It needs to stand alone as a visual break in the flow, or it gets read past like any other guideline instead of enforced like a hard boundary. -->

Present the 20 items and end the turn. Do not proceed to Step 2 until the user has told you which ones they picked.

This is the entire point of the skill. If the AI keeps going and generates hypotheses on its own judgment of which anomalies matter, the human has been quietly cut out of the loop and the whole exercise is pointless — even if the user says "just handle the rest yourself." At minimum, ask which items stood out to them before continuing.

## Step 2 — Build hypotheses from what they picked

Use only the anomalies the user selected. Discard the rest.

- Generate 15 hypotheses
- For each one, add: "If this were wrong, what would we expect to see instead?"
- Do not pick which hypothesis is correct
- Do not count reworded variants of the same mechanism as separate hypotheses

Stop again after presenting the 15. Wait for the user to pick 3.

**Give them the criteria to pick with:**
① Is it surprising? ② Is it new? ③ Is there a way to check if it's wrong?
If all three hold, it's ready to use. If only the first two hold, it's too early — set it aside as a bigger open question instead.

## Step 3 — Verification (restrictions lifted here)

This stage exists to narrow down, so all prior restrictions are lifted. Explaining, ranking, and choosing are all fine now.

- Check each hypothesis against the actual data
- Keep only what survives
- Narrow down to 5 or fewer

## Why this shape

<!-- Maintainer note: keep this section inline in SKILL.md, always loaded, never collapsed or split into a separate reference file. Unlike the README's collapsible version of this same argument, this copy is read by the AI on every run and directly governs whether it holds the line at the Step 1 stop point. Moving it out of the main body weakens that enforcement. -->

When what you don't know is the *outcome* (deduction, induction), the AI is strong — it's good at verification. But when what you don't know is the *cause or frame itself* (abduction), the AI is at its weakest: it hands you the most statistically likely story as if it were the answer.

So in abduction situations, the AI's role is capped at candidate generation. Connecting the strange pieces into meaning is left to the human. Holding that line is the entire purpose of this skill.
