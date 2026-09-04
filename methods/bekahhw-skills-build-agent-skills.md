---
name: build-agent-skills
description: Design, revise, and maintain agent skills that produce reliable behavior. Use when creating a new skill, improving an existing skill, splitting an overloaded skill, or deciding whether a skill should exist at all.
disable-model-invocation: true
---

# Build Agent Skills

**A skill is behavioral infrastructure, not documentation.**

A good skill reliably changes what an agent does.

Do not optimize for completeness, clever prose, or explaining every principle.

Optimize for:

**trigger → behavior → evidence → revision**

The first version does not need to be excellent.

It needs to be specific enough to fail informatively.

## 1. Define the Behavioral Change

Before writing the skill, answer:

> What should the agent do differently when this skill is active?

State the answer as observable behavior.

Bad:

> Help the agent write better code.

Better:

> Before changing an unfamiliar module, identify the public behavior it affects and verify that behavior after the change.

Avoid goals that cannot be observed in an agent session.

**Done when:** you can tell whether the skill changed the agent's behavior.

## 2. Choose the Skill Shape

Identify what kind of skill you are building.

### Voice

Controls how the agent communicates or reasons aloud.

Use when the primary value is a consistent style, stance, or interaction pattern.

A Voice skill usually needs:

- a strong governing principle
- positive examples
- boundaries
- anti-patterns

### Pipeline

Moves work through a repeatable transformation.

Use when there is a clear input, sequence, and output.

A Pipeline skill usually needs:

- ordered stages
- explicit transitions
- completion criteria
- artifact requirements

### Reference

Provides rules, domain knowledge, conventions, or constraints the agent must apply.

Use when the value comes from remembering and applying stable information.

A Reference skill usually needs:

- clear applicability
- compact rules
- exceptions
- retrieval-friendly structure

### Orchestrator

Coordinates multiple kinds of work or other capabilities.

Use when the challenge is deciding what happens when, in what order, and under which conditions.

An Orchestrator usually needs:

- routing logic
- dependencies
- stop conditions
- handoff rules

### Wizard

Guides the user and agent through an interactive sequence.

Use when later actions depend on answers, evidence, or decisions produced earlier.

A Wizard usually needs:

- named stages
- questions with a purpose
- gates
- escape hatches
- "done when" conditions

Do not force a skill into one category if another shape better explains its behavior.

**Done when:** the structure of the skill matches the kind of behavior it controls.

## 3. Find the Irreducible Rule

Ask:

> If the agent remembered only one sentence from this skill, what should it be?

Write that sentence.

Examples:

> Verify the boundary before changing the implementation.

> Preserve the user's decision; automate the mechanical work.

> One artifact should have one clear owner.

This rule should resolve ambiguity throughout the rest of the skill.

If two rules compete, the skill probably needs a clearer priority or a narrower scope.

**Done when:** one sentence captures the skill's governing behavior.

## 4. Name the Important Moves

Repeated behaviors deserve names.

Create compact vocabulary for the moments the agent must reliably recognize.

Examples:

- Evidence Gate
- Scope Check
- Assumption Map
- Review Pass
- Escape Hatch

A useful term should compress several instructions into a concept the agent can reuse.

Do not name everything.

Name only behaviors that:

- recur
- are easy to skip
- change the next action
- benefit from being referenced elsewhere

Prefer:

> Run the Evidence Gate.

over repeating six paragraphs describing the same behavior.

**Done when:** the skill has a small vocabulary for its most important recurring moves.

## 5. Turn Advice Into Procedure

Replace abstract guidance with decisions and actions.

Weak:

> Be thoughtful about edge cases.

Stronger:

> Before finalizing, identify the input most likely to violate the current assumption and test it.

Weak:

> Keep scope small.

Stronger:

> Classify adjacent work as required, separate, or unrelated. Implement only required work.

For each important stage, specify:

1. What starts the stage?
2. What should the agent do?
3. What should it avoid?
4. What evidence ends the stage?

Use:

> **Done when:** ...

when a stage should not advance without a concrete condition.

**Done when:** another agent could execute the skill without inventing the workflow.

## 6. Add Gates Where Mistakes Become Expensive

A gate prevents the agent from advancing before an important condition exists.

Examples:

> No evidence, no diagnosis.

> No accepted scope, no implementation.

> No verified behavior, no completion.

Use gates sparingly.

A gate is justified when advancing prematurely commonly causes:

- wasted work
- hallucinated assumptions
- oversized changes
- irreversible actions
- false confidence
- loss of learning or user control

Do not gate trivial steps.

**Done when:** the expensive failure points have explicit safeguards.

## 7. Design the Escape Hatches

Rigid skills become annoying skills.

Identify when the normal procedure should stop, compress, or change.

Typical escape conditions:

- the user explicitly wants speed over learning
- the task is urgent
- required evidence cannot be obtained
- the procedure adds more cost than value
- the problem is trivial
- the skill's assumptions do not hold

State what happens instead.

Example:

> If the issue threatens production data, prioritize containment and recovery. Reconstruct the learning process afterward.

An escape hatch should preserve the purpose of the skill without blindly preserving its ceremony.

**Done when:** the agent knows when not to follow the default path literally.

## 8. Write Guardrails From Likely Failure Modes

Do not fill the skill with generic warnings.

Ask:

> How is an agent most likely to misuse this procedure?

Write guardrails against those failures.

Good guardrails are specific.

Examples:

> Do not ask a question whose answer is already available in the conversation.

> Do not create alternative designs merely to satisfy a requirement for multiple options.

> Do not turn stylistic preferences into correctness defects.

Avoid rules like:

> Be concise.
> Be helpful.
> Think carefully.

unless they produce a concrete behavior unique to the skill.

**Done when:** each guardrail prevents a plausible failure rather than expressing a virtue.

## 9. Define Success

Do not define success as completing the procedure.

Define the state that should exist afterward.

Weak:

> The review is complete.

Better:

> The reviewer can identify what changed, which risks matter, and what evidence supports the decision.

Weak:

> The document was created.

Better:

> A reader can make the intended decision without needing missing context.

The success condition is the skill's north star.

**Done when:** success can be evaluated independently of whether every prescribed step occurred.

# Revision Loop

Do not attempt to perfect a new skill from first principles.

Use it.

Observe where it fails.

Then revise the smallest thing that addresses the failure.

## Stage 1: Utterance

Start with the smallest instruction that captures the desired behavior.

The goal is not completeness.

The goal is to make the intended behavior visible enough to test.

## Stage 2: Failure-Driven Growth

Collect real failures.

For each failure, ask:

- What did the agent do?
- What should it have done?
- Was the instruction absent, ambiguous, misplaced, or ignored?
- What is the smallest change that would alter the behavior?

Add instructions in response to observed failures.

Do not add speculative rules for every failure you can imagine.

## Stage 3: Vocabulary Crystallization

Watch for instructions that repeat.

When several rules describe the same conceptual move, name it.

Replace repetition with the new term where clarity improves.

Good vocabulary makes the skill shorter while making its behavior more stable.

## Stage 4: Rename When the Job Becomes Clear

Early names often describe the original request rather than the skill's actual function.

Rename when the skill's real job becomes clearer.

Prefer names that describe:

- the capability gained
- the transformation performed
- the decision controlled

Avoid names tied to one accidental implementation.

## Stage 5: Decompose When Responsibilities Diverge

Split the skill when parts of it:

- trigger under different circumstances
- have different success criteria
- evolve independently
- are useful without one another
- require substantially different procedures

Do not split merely because the file is long.

Split when there are multiple jobs.

## Stage 6: Prune

Remove instructions that:

- restate the same rule
- no longer change behavior
- explain theory without affecting execution
- handle failures that are no longer relevant
- belong to another skill
- describe obvious defaults the agent already performs reliably

Ask of every section:

> If this disappeared, would behavior get worse?

If not, remove it.

# Skill Review

When reviewing an existing skill, evaluate it in this order.

## Trigger

Is it clear when this skill should and should not be used?

## Job

Can its behavioral purpose be expressed in one sentence?

## Shape

Does its structure match its genre?

## Procedure

Can the agent tell what to do next?

## Gates

Are expensive mistakes prevented before they happen?

## Evidence

Can important stages be verified?

## Escape Hatches

Can the skill adapt without becoming ritualistic?

## Failure Modes

Are guardrails based on real or highly probable mistakes?

## Vocabulary

Do repeated concepts have stable, useful names?

## Scope

Is the skill doing one coherent job?

## Pruning

Which instructions could disappear without changing behavior?

# Anti-Patterns

## The Essay

The skill explains a philosophy at length but does not tell the agent what to do.

Fix it by converting principles into observable decisions and actions.

## The Constitution

The skill accumulates rules for every imaginable circumstance.

Fix it by keeping the governing principle and rules supported by actual failures.

## The Checklist Costume

The skill has many steps, but nothing meaningful depends on their order.

Fix it by removing ceremonial stages or expressing the content as a Reference skill instead.

## The Interrogator

The skill forces questions even when the answer is already known or irrelevant.

Fix it by stating what information each question is intended to obtain.

## The Infinite Loop

The skill has no clear completion condition.

Fix it with evidence-based "done when" criteria.

## The Swiss Army Skill

One skill handles several loosely related jobs.

Fix it by identifying separate triggers and success conditions, then decomposing.

## The Frozen Skill

The skill is treated as finished once written.

Fix it by revising from observed behavior.

# Originality

Skills should encode principles and procedures, not imitate another author's wording.

When working from research, examples, or existing approaches:

- extract the underlying behavior
- restate it from first principles
- invent original terminology where useful
- create new examples
- adapt the procedure to the actual problem
- remove attribution-dependent phrasing

Do not reproduce distinctive prose, examples, metaphors, or structure merely because they worked elsewhere.

Research should change the design.

It should not become copied text.

# Final Test

Before considering a skill ready, ask:

1. What behavior does this skill change?
2. What is its governing rule?
3. What genre best describes it?
4. What are its named moves?
5. Where can the agent advance too early?
6. How does it know each important stage is complete?
7. When should it abandon or compress the procedure?
8. Which guardrails correspond to actual failure modes?
9. What could be removed without changing behavior?
10. What failure would teach us what to revise next?

A skill is ready to use when those answers are clear.

It is not finished.

Use reveals the next version.
