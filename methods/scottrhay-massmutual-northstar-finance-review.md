---
name: northstar-finance-review
description: Use when reviewing the Northstar Life finance starter workbook or turning its reconciled finance tables into a checkable monthly review.
---

# Northstar finance review

Use the open workbook as the only source of truth. Complete the controls before writing a narrative. Northstar Life is synthetic and contains no MassMutual business data.

## Scope

- Work only with visible tables in the open workbook.
- Preserve `Instructions`, `Dashboard`, `IssueLog`, `PerformanceData`, `PremiumDetail`, `ClaimsDetail`, `ExpenseDetail`, `Reconciliation`, and `DataDictionary`.
- Do not search the web or introduce another source unless the user explicitly supplies and approves it.
- Never infer a business cause from a variance, trend, contributor, or data-quality flag.
- Never change source values merely to make a reconciliation pass.

## Workflow

1. Confirm that `PerformanceData`, `PremiumDetail`, `ClaimsDetail`, `ExpenseDetail`, and `Reconciliation` are present. Stop and name anything missing.
2. Inspect every row in `Reconciliation`. If any status is not `PASS` or any absolute difference is 0.01 or greater, stop the review and list only the failed controls with source references.
3. Rank the five largest unfavorable variances in `PerformanceData` by absolute dollars:
   - Premium Revenue below plan is unfavorable.
   - Paid Claims above plan is unfavorable.
   - Operating Expense above plan is unfavorable.
4. For each finding, show month, category, plan, actual, dollar variance, percentage variance, and exact source row or formula.
5. Use the relevant detail table to identify the largest contributing records. Describe what the records show, not why the result occurred.
6. Label every explanation `Supported`, `Hypothesis`, or `Blocked`. Workbook arithmetic can establish what changed, not an external cause.
7. Independently recalculate the largest finding and show the arithmetic.
8. Record missing ownership or unresolved evidence as an open question rather than inventing an answer.

## Workbook output

Create or refresh a worksheet named `SkillReview` containing:

1. `CONTROL STATUS` with reconciliation result and any failures.
2. `TOP FIVE UNFAVORABLE VARIANCES` with exact source references.
3. `DETAIL CONTRIBUTORS` with the largest relevant records.
4. `CLAIM BOUNDARIES` with claim, status, supporting evidence, missing evidence, and owner needed.
5. `INDEPENDENT CHECK` showing the arithmetic for the largest finding.
6. `OPEN QUESTIONS` identifying evidence or finance-owner decisions still required.

Use editable Excel tables, US dollars with thousand separators and no decimals, percentages with one decimal, banded rows, frozen headers, and clear section labels. Preserve all source sheets and formulas.

## Completion check

Before reporting completion:

- Confirm every reconciliation control passed.
- Confirm the top finding was independently recalculated.
- Confirm no causal explanation is presented as fact.
- Name the created or refreshed `SkillReview` sheet.
- State what still requires a finance owner or additional source.

## Common pitfalls

- Do not rank solely by percentage when the request specifies absolute dollars.
- Do not treat a detail contributor as a proven cause.
- Do not hide data-quality warnings or unresolved ownership.
- Do not modify source data to force a desired result.

After class, retain this skill only if organizational policy permits it; otherwise remove the `northstar-finance-review` folder from the Excel custom-skills folder.
