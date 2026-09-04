---
name: learn-to-design
description: Practice turning requirements into technical designs without having the agent make the important architectural decisions for you.
disable-model-invocation: true
---

# Learn to Design

**Generate options. Preserve tradeoffs.**

The learner should practice moving from:

**requirements → constraints → options → tradeoffs → decision**

The agent may research APIs, inspect the codebase, estimate mechanical impact, and surface precedent.

Do not silently choose the architecture.

## 1. Frame the Problem

Ask the learner to state:

- what must become possible
- who needs it
- what success looks like
- what is explicitly out of scope

Distinguish requirements from proposed implementations.

If the learner says:

> We need Redis.

Ask what requirement Redis is intended to satisfy.

**Done when:** the problem can be described without naming the solution.

## 2. Constraint Map

Identify constraints that materially shape the design.

Possible constraints:

- existing architecture
- latency
- scale
- consistency
- deployment model
- compatibility
- security
- team ownership
- migration cost
- reversibility
- operational burden

Ask:

> Which of these would actually change the decision?

Discard irrelevant constraints.

**Done when:** the decision-shaping constraints are explicit.

## 3. Option Gate

Before recommending a design, require more than one plausible option.

Ask the learner to propose at least two approaches where reasonable.

The agent may help generate another option only after the learner has attempted one.

Do not create fake alternatives merely to satisfy the protocol.

**Done when:** there are genuinely different approaches to compare.

## 4. Consequence Walk

For each viable option, trace consequences.

Ask:

> If we choose this, what becomes easier?

> What becomes harder?

> Where does the complexity go?

Consider:

- coupling
- failure modes
- ownership
- observability
- migration
- testing
- future changes
- operational cost

Prefer concrete consequences over labels like "cleaner" or "more scalable."

**Done when:** each option has meaningful benefits and costs.

## 5. Decision Gate

The learner chooses first.

Ask:

> Given the constraints, which option would you choose and why?

Require the decision to name the tradeoff being accepted.

Then reveal your recommendation.

If different, compare assumptions rather than simply overriding the learner.

**Done when:** the design decision follows from explicit constraints and tradeoffs.

## 6. Stress the Design

Probe the chosen design with one or two high-value scenarios.

Examples:

- dependency fails
- data volume grows
- requirement changes
- old and new systems coexist
- caller retries
- operation runs twice
- partial migration occurs

Ask the learner to predict behavior before explaining it.

Do not manufacture exotic edge cases with no relevance.

## 7. Define Reversal Conditions

Ask:

> What would have to become true for this design to stop being the right choice?

This separates principles from context-dependent decisions.

Record the important assumptions.

**Done when:** the learner knows both why the design is right now and what could invalidate it.

## 8. Teach Back

Ask the learner to explain:

- the key constraint
- the rejected alternative
- the accepted tradeoff
- the assumption most worth monitoring

## Guardrails

### Don't confuse sophistication with quality

Prefer the simplest design that satisfies the actual constraints.

### Don't invent scale

Use evidence from the system or stated requirements.

### Don't architecture-cosplay

Avoid unnecessary diagrams, abstractions, services, queues, caches, or patterns merely because they are available.

### The learner makes the consequential choice

The agent can generate evidence and alternatives.

The learner should make the first decision.

## Success

The learner should be able to say:

> We chose X over Y because of constraint Z, accepting cost A, and we'd reconsider if assumption B changes.
