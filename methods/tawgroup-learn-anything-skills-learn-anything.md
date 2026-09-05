---
name: learn-anything
description: Run an adaptive learning session from the learner's current understanding to a concrete goal. Use when someone asks to learn, deeply understand, or be taught a topic over multiple steps. Do not use for a quick factual lookup or a requested one-shot summary.
---

# Learn Anything

Teach for understanding, not coverage. Spend the learner's effort on the subject rather than on finding resources, sequencing material, or managing the session.

The user's instructions take precedence over this workflow. Shorten, skip, or combine phases when they explicitly ask.

## Workflow

1. **Set the goal.** Turn the topic into an observable outcome: what the learner wants to explain, predict, build, or solve. Ask only when the outcome is genuinely unclear.
2. **Probe.** Use `$probe-knowledge` to locate the learner's relevant knowledge boundary. If that skill is unavailable, ask a few progressively harder questions and record what is solid, shaky, and missing.
3. **Plan.** Use `$plan-learning-path` to connect the learner's solid knowledge to the goal. Show the short plan before teaching unless the user asked for uninterrupted delivery.
4. **Teach.** Use `$teach-adaptively`. Teach one dependency at a time, check it, and adjust before continuing.
5. **Close.** Ask the learner to explain or apply the main idea without hints. Summarize what is now solid, what remains uncertain, and the next useful step.

## Accuracy

Verify claims when the topic is current, high-stakes, disputed, or outside reliable knowledge. Prefer primary and authoritative sources. Separate established facts from simplifying models and open questions.

Do not create learning logs, files, flashcards, or homework unless the user asks for them.
