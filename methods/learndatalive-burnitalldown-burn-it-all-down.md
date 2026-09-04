---
name: burn-it-all-down
description: Run the Burn It All Down adversarial review on a plan, design, or architecture. Use when the user wants their plan pressure-tested, red-teamed, or wants a second opinion that doesn't just agree with them.
argument-hint: [path-or-description]
context: fork
agent: burn-it-all-down
---

Run an adversarial "anarchist" review of $ARGUMENTS.

If $ARGUMENTS is a file or directory path, read it (and any directly related files in the same directory) before reviewing. Do not review from the path name alone. If $ARGUMENTS is pasted text or a plain-language description, treat that text itself as the plan under review.

Follow the five-stage process defined in your own instructions, front to back: enumerate constraints, classify each one, propose asymmetric shortcuts, red-team the plan, then close with ranked leverage points, a steelman, and an anti-sycophancy check. Produce the full structured output. Do not summarize stages away or shortcut the process itself.
