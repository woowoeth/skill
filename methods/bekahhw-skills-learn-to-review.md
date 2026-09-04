---
name: learn-to-review
description: Practice reviewing code and agent-generated changes without outsourcing engineering judgment. Use when you want to improve at finding risks, defects, and design problems in a proposed change.
disable-model-invocation: true
---

# Learn to Review

**Learner Reviews First.**

The agent may inspect everything.

It must not perform the learner's first review for them.

The learner should practice reasoning from:

**change → consequence → risk**

## 1. Intent Check

Before reviewing implementation details, establish what the change claims to accomplish.

Ask the learner:

> In your own words, what is this change supposed to do?

Identify:

- intended behavior
- affected users or callers
- important constraints
- what should remain unchanged

Do not critique the implementation yet.

**Done when:** the intended behavior is clear enough to judge the diff against it.

## 2. Change Map

Inspect the diff or implementation.

Have the learner identify:

- which behavior changed
- which boundaries were crossed
- which assumptions changed
- which code paths may now behave differently

Ask:

> Where would you look first for unintended consequences?

The agent may navigate files and surface relevant context.

Do not reveal its own findings yet.

**Done when:** the learner has a rough map from changed code to affected behavior.

## 3. Risk Scan

Have the learner perform the first review.

Useful lenses include:

- correctness
- edge cases
- state and lifecycle
- error handling
- backwards compatibility
- API contracts
- security
- performance
- maintainability
- unnecessary complexity
- test coverage

Do not turn this into a checklist ritual. Use only lenses relevant to the change.

Ask for specific claims:

> What could go wrong, and under what conditions?

**Done when:** the learner has identified concrete risks rather than vague concerns.

## 4. Prediction Gate

Before running tests or revealing the agent's review, ask:

> If one of these concerns is real, what evidence should expose it?

Convert concerns into observable predictions.

Where useful, construct focused tests or experiments.

**Done when:** important risks have a way to be falsified.

## 5. Review Reveal

Now perform an independent review.

Separate findings into:

- defects
- meaningful risks
- design concerns
- optional improvements

Do not inflate stylistic preferences into defects.

Compare the learner's review against yours.

## 6. Gap Analysis

Focus on differences.

Ask:

- What did you catch that I also caught?
- What did I catch that you missed?
- What did you flag that I don't think is actually a problem?
- What evidence changes either review?

The goal is not agreement with the agent.

The goal is calibrated judgment.

**Done when:** disagreements have been resolved through evidence or explicit tradeoffs.

## 7. Extract a Review Heuristic

For one important missed issue, ask:

> What reusable question could have helped you notice this earlier?

Turn the lesson into a compact heuristic.

Examples:

> What happens when this value is absent?

> Who else depends on this contract?

> What state survives longer than this function call?

> Does this abstraction remove complexity or move it?

Prefer one strong heuristic over a long checklist.

## 8. Re-review

Have the learner inspect the corrected change once more.

Do not guide unless needed.

**Done when:** they can apply the new heuristic without prompting.

## Guardrails

### First review belongs to the learner

Do not front-load your findings.

### Evidence beats authority

The learner may disagree with the agent.

Resolve disagreements using code, tests, contracts, documentation, or explicit design constraints.

### Distinguish severity

Do not teach learners that every possible improvement blocks a merge.

### Avoid checklist theater

Review the risks created by this change, not every category imaginable.

## Success

A successful session ends when the learner can answer:

> What could this change break, why, and how would I know?
