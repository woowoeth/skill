---
name: cumcm-thesis
description: Use when writing, revising, structuring, checking, or polishing a CUMCM or similar mathematical modeling paper, including abstracts, mathematical exposition, results, model evaluation, LaTeX, or final review.
---

# CUMCM Thesis（论文写作）

Write so a judge can quickly see why the model fits, what the verified result is, and why the conclusion is credible. Logic outranks rhetoric; this Skill expresses completed modeling and never recomputes it.

## Input gate

Require the relevant `PROBLEM BRIEF`, verified `MODEL SUMMARY`, schema-valid [RESULT_MANIFEST](../../cumcm-shared/schemas/result-manifest.schema.json), and schema-valid [FIGURE_MANIFEST](../../cumcm-shared/schemas/figure-manifest.schema.json). Preserve their definitions, units, assumptions and limitations. If evidence is missing, use an explicit traceability placeholder such as `[由 results.json 的 q2.rmse 写入]`; never invent a number, method, validation result or figure message.

## Workflow

1. Build a claim-evidence map: each method claim points to formulation/code, each number to a saved result, each visual statement to the current figure.
2. Choose the paper structure from the actual question dependency graph using [论文结构](references/paper-structure.md). Do not narrate the chronological work log.
3. For the abstract and problem analysis, read [摘要与问题分析](references/abstract-and-analysis.md). Follow the reasoning chain: problem nature -> evidence/research basis -> candidate method -> justified simplification -> targeted improvement -> verified result. Vary prose naturally; do not force a generic data-cleaning/prediction/optimization/robustness sequence.
4. For assumptions, notation and equations, read [模型假设、符号与模型表述](references/assumptions-notation-model.md).
5. Explain results rather than reciting tables. Read [结果分析与模型评价](references/results-and-evaluation.md) for scope-specific strengths, limitations and improvements.
6. Use [LaTeX 排版规范](references/latex-style.md) for directly insertable mathematics and [学术表达](references/academic-style.md) for concise prose.
7. Run [论文审查清单](templates/review-checklist.md) and record failed/unverified items. Check [常见写作错误](references/common-errors.md).

## Boundaries

- Do not choose or refit a model; return modeling gaps to `cumcm-modeling`.
- Do not redesign figures; send a `FIGURE REQUEST` to `cumcm-visualization`.
- Do not copy the problem statement or an excellent paper's distinctive wording.
- Do not call a model accurate, robust or innovative without named executed evidence.
- A model-specific weakness must state its consequence and validity boundary; avoid “科学合理、精度较高、适用性强.”

## Output

Produce the requested section plus a compact review ledger: claim, source artifact/key, evidence state, unit/symbol check, and unresolved action. Use [论文提纲](templates/paper-outline.md), [摘要模板](templates/abstract-template.md), or [章节模板](templates/section-template.md) only as shape guides; adapt them to the actual question graph.
