---
name: cumcm-global
description: Use when a CUMCM project spans multiple specialist stages, needs question-dependency routing, or requires final cross-artifact consistency review; not for a focused modeling, visualization, or paper-writing request.
---

# CUMCM Global Orchestrator

Coordinate specialists. Correct abstraction and traceable evidence outrank algorithm sophistication.

## Start gate

Before formal implementation, read the complete problem statement, attachment instructions, file schemas, units, and every subquestion. Record inaccessible or ambiguous material; never infer it silently. If the user requests a later stage directly, enter that stage but verify its required inputs.

## First output

Create a `PROBLEM BRIEF` and `QUESTION GRAPH` using [contracts](references/contracts.md). Identify inputs, outputs, decision/state variables, parameters, objectives, constraints, data sources, and question dependencies. Classify each question by mathematical structure using [problem taxonomy](references/problem-taxonomy.md), not by matching topic words to historical model names.

Read [question dependencies](references/question-dependency.md) when questions share parameters, data, code, or outputs. Use [competition workflow](references/competition-workflow.md) for a full contest or when sequencing is unclear.

When the graph has a hard model-to-model edge, require a named `UPSTREAM HANDOFF` and route its design to [hybrid model chains](../cumcm-modeling/references/hybrid-model-chains.md). The orchestrator owns routing, while `cumcm-modeling` owns propagation and validation details.

## Routing

- Invoke `cumcm-modeling` for data audit, mathematical formulation, model selection, algorithms, Python implementation, validation, sensitivity, robustness, or uncertainty. Require its `MODEL SUMMARY` and schema-valid `RESULT_MANIFEST` before downstream use.
- Invoke `cumcm-visualization` only with a `FIGURE REQUEST` whose question and main message are known; require a schema-valid `FIGURE_MANIFEST` as its handoff.
- Invoke `cumcm-thesis` only with verified problem, model, `RESULT_MANIFEST`, and `FIGURE_MANIFEST` inputs; it must not recompute or invent them.
- Keep the current stage when the user requests a focused task. Do not restart the entire workflow unnecessarily.

Read the [bidirectional structure-model index](../../cumcm-shared/references/bidirectional-index.md) when candidate routing benefits from distilled use/avoid conditions. Read [excellent-paper patterns](../../cumcm-shared/references/excellent-paper-patterns.md) or [A-problem patterns](../../cumcm-shared/references/a-problem-patterns.md) only when those fixed historical lessons are relevant; do not treat them as a live corpus or retrieve new papers.

## Hard gates

1. No formal code before the problem is mathematically formalized.
2. No complex model without a reasonable baseline or a written reason baseline comparison is impossible.
3. No completion claim without a validation plan and executed checks where data permit.
4. No answer is complete until results are interpreted in the real problem.
5. No key paper number without a traceable program output or cited source.
6. No innovation claim unless the added mechanism fixes a named baseline defect, has a predefined discard rule, and is tested; wording must not exceed its evidence level.
7. No figure without a specific question it answers.

When a gate fails, state the missing evidence and return to the producing stage. Do not paper over the gap with prose.

## Final consistency review

Before final delivery, produce `FINAL CONSISTENCY REVIEW`. Check model vs code, code vs `RESULT_MANIFEST`, result vs `FIGURE_MANIFEST`, figure vs text, units, symbols, parameters, and whether each conclusion has evidence. Use [final checklist](references/final-checklist.md). Report unresolved items as blockers or limitations rather than marking them complete.

## Templates

- Initial analysis: [problem analysis](templates/problem-analysis.md)
- End-to-end execution: [competition plan](templates/competition-plan.md)
