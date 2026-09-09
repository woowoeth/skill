---
name: cumcm-modeling
description: Use when a mathematical modeling competition task needs data analysis, mathematical formulation, model selection, algorithm design, numerical solution, Python implementation, validation, sensitivity, or robustness analysis.
---

# CUMCM Modeling

Build the simplest model that adequately answers the formalized problem. Priority is: correct interpretation, formulation, model choice, reliable solution, validation, explanation, then improvement and computational sophistication.

## Required input

Consume a `PROBLEM BRIEF` and, for multi-question tasks, a `QUESTION GRAPH`. If objectives, variables, units, constraints, or data provenance are missing, return the gap instead of choosing an algorithm.

When the graph contains a hard cross-model edge, read [hybrid model chains](references/hybrid-model-chains.md). Freeze each `UPSTREAM HANDOFF`, retrieve evidence by stage and whole chain when useful, and validate both stages and the end-to-end decision.

## Workflow

1. Audit the data: shape, fields, types, units, sampling unit, missing values, duplicates, outliers, distribution, imbalance, temporal/spatial dependence, and leakage risk. Use `scripts/data_profile.py` for a first pass; it does not infer semantics or units.
2. Formalize decision/state variables, parameters, equations, objectives, constraints, and initial/boundary conditions.
3. Read [model selection](references/model-selection.md). Compare candidates by mathematical structure, data conditions, objective, interpretability, scale, and uncertainty. For a full comparison, layer them as robust baseline, competition-strength improvement, and falsifiable innovation. When asked to create or judge innovations, read [innovation design](references/innovation-design.md); for a portfolio, use [model comparison](templates/model-comparison.md) and preserve every screening column plus the finalist record.
4. Establish a transparent baseline. A complex model must demonstrate useful gain under the same data split, metric, constraints, and compute budget.
5. Specify the algorithm, parameter estimation, seed, tolerances, stopping conditions, output artifacts, and failure handling. Read [Python implementation](references/python-implementation.md) when coding.
6. Validate against the model's actual failure modes. Read [baseline and validation](references/baseline-and-validation.md); for uncertainty or parameter claims, also read [uncertainty, sensitivity, robustness](references/uncertainty-sensitivity-robustness.md).
7. Interpret the result in the real system and state the validity domain.

For physical, engineering, geometric, or differential-equation tasks, read [mechanism modeling](references/a-mechanism-modeling.md). For family-specific prerequisites and exclusions, read [model families](references/model-families.md). Check [common errors](references/common-errors.md) before finalizing.

## Non-negotiable decisions

- Do not equate an advanced algorithm with a better paper.
- Do not randomly split time series or leak preprocessing across validation folds.
- Do not default evaluation tasks to entropy-weight TOPSIS.
- Try deterministic or exact solvers before metaheuristics when structure permits.
- For stochastic heuristics, report repeated seeded runs, feasibility rate, dispersion, convergence and a fair baseline.
- Training fit, including high R-squared, is not generalization evidence.
- A+B is not innovation. Name the baseline defect, isolate the added mechanism, and run an ablation under identical conditions.

## Output contract

Return a `MODEL SUMMARY` with: problem/objective; variables/units; assumptions; baseline; main model/equations; algorithm/parameters; upstream handoffs consumed; uncertainty output; validation performed, including end-to-end evidence when applicable; saved result artifacts; key results; limitations. Also produce a `RESULT_MANIFEST` conforming to the [JSON Schema](../../cumcm-shared/schemas/result-manifest.schema.json); every reported metric and validation claim must resolve to a versioned, hashed artifact or remain explicitly unverified. Use [modeling plan](templates/modeling-plan.md), [model comparison](templates/model-comparison.md), or [experiment plan](templates/experiment-plan.md) as needed.

Do not select manuscript wording or publication styling. Send the verified `RESULT_MANIFEST` and units to `cumcm-visualization`; send it with the completed `MODEL SUMMARY` to `cumcm-thesis`.
