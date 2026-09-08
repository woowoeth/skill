---
name: content-cannibalization-finder
description: Detect and assess possible search-intent competition among existing site pages using supplied URL, title, content, and query-by-page performance data, then recommend KEEP, DIFFERENTIATE, MERGE, REDIRECT, INTERNAL-LINK, or HUMAN actions with evidence and uncertainty. Use for SEO cannibalization audits, query-ownership analysis, overlapping-content reviews, and consolidation triage; not for declaring cannibalization from keyword or title similarity alone.
---

# Content Cannibalization Finder

Find page pairs or clusters that may compete for the same search intent, distinguish harmful overlap from useful coexistence, and recommend the smallest justified action. Treat cannibalization as a diagnosis requiring multiple signals, not as a synonym for similar pages or ranking volatility.

## Inputs

Accept any combination of:

- A URL inventory with stable page identifiers
- Page titles, headings, article text, extracts, or summaries
- Google Search Console or equivalent query-by-URL data, including date range and available clicks, impressions, CTR, and average position
- Comparable historical periods or time-series exports
- Optional canonical, redirect, indexation, internal-link, conversion, backlink, content-role, and business-priority data

Use only supplied data and information retrieved through authorized tools. Query-by-URL performance data is optional, but without it the result is a content-overlap screening: label findings `competition candidate`, do not state that performance cannibalization is established, and explain which performance evidence would test the hypothesis.

## Candidate efficiency

Do not compare every page pair at full depth by default.

Use a staged funnel:
1. Generate candidates cheaply from shared query exposure, supplied clusters, titles/headings, or precomputed similarity; for large inventories, default to the top 20 candidate pairs/clusters by explicit signals.
2. Remove pairs with clearly different roles/intents when evidence is sufficient.
3. Deep-read full content and time-series evidence only for the remaining plausible competition candidates; default to the top 5 deep comparisons per pass unless the user asks for a broader batch.
4. Rank and report only material candidates plus a concise count of screened-out groups.

For large sites, prefer deterministic/precomputed candidate generation before model-heavy pair analysis. Never treat the cheap screening signal as proof of cannibalization. Before a materially larger batch, warn that the run is high-load and propose chunking.

## Reference routing

- For normalization, candidate generation, evidence signals, counterevidence, query ownership, time-series analysis, and confidence, read [references/detection-framework.md](references/detection-framework.md).
- For action definitions and selection criteria, read [references/action-framework.md](references/action-framework.md).
- For the required report structure and handoff record, read [references/output-template.md](references/output-template.md).
- Before delivery, run [references/quality-checklist.md](references/quality-checklist.md) and fix any failure.

## Workflow

1. Inventory the evidence. Record source, coverage, field definitions, date ranges, filters, aggregation level, row limits, missing values, and whether comparison periods are equivalent.
2. Normalize identifiers conservatively. Join pages and metrics only by a supplied stable ID, exact URL, or defensible canonical mapping. Preserve original URLs and report duplicates, unmatched records, and uncertain mappings.
3. Describe each examined page's primary intent, audience, funnel role, and content role from available evidence. Distinguish hubs, detail pages, episode/chapter pages, people/entity profiles, reviews, comparisons, analyses, FAQs, and other legitimate roles rather than assuming pages on one topic should be merged.
4. Generate page-pair or cluster candidates from shared query clusters and, when content is available, overlapping intent and subject matter. Similar titles, slugs, entities, or keywords may prioritize review but cannot establish cannibalization.
5. Evaluate each candidate across independent dimensions: intent equivalence, same-query exposure, query ownership and switching, click/impression distribution, position context, time-series behavior, content duplication, distinctive value, site role, and alternative explanations.
6. Classify the finding and confidence using the detection framework. Keep observed values, transparent calculations, interpretations, counterevidence, and unknowns visibly separate.
7. Choose one primary action from `KEEP`, `DIFFERENTIATE`, `MERGE`, `INTERNAL-LINK`, or `HUMAN`. Use `REDIRECT` only as a separately approved implementation step after a merge, retirement, or URL migration decision; never infer its target.
8. State scope, pages affected, evidence for and against, risks, preserved value, missing evidence, concrete next step, and success or reassessment signals. Do not change, merge, redirect, publish, or delete pages unless the user separately authorizes execution.
9. Return the report using the output template. Rank candidates by likely impact, evidence strength, and decision urgency, not by superficial similarity.

## Non-negotiable guardrails

- Never invent URLs, queries, page contents, page roles, metrics, time-series changes, canonical relationships, conversions, backlinks, causes, or search intent.
- Do not declare cannibalization from title, slug, keyword, entity, or text similarity alone.
- Do not treat one ranking decline, a low average position, an aggregate CTR change, or normal URL fluctuation as proof of cannibalization.
- Do not assume two URLs appearing for the same query is harmful. Check intent, SERP role, stability, click distribution, and whether the pages serve a useful multi-page journey.
- Treat Search Console average position and CTR as aggregated diagnostic clues. Do not add row CTRs or average row-level CTRs without appropriate weighting; derive cluster CTR as total clicks divided by total impressions when raw values exist.
- Do not compare partial, differently filtered, differently aggregated, migrated, seasonal, or otherwise non-equivalent periods without an explicit limitation.
- Do not use missing Search Console data as evidence that competition does not exist. Do not use content-only evidence to claim measured search-performance harm.
- Preserve unique facts, first-hand experience, author analysis, conversions, backlinks, and purposeful page roles in any consolidation plan. When those values are unknown, flag them for review.
- A `MERGE` recommendation does not authorize deletion, canonical changes, or redirects. `REDIRECT` requires a verified source, approved destination, internal-link review, and human approval.
- Surface conflicts between sources instead of selecting the version that best supports a recommendation.

## Related skills and handoffs

- Use `$content-refresh-auditor` when the goal is broader lifecycle prioritization across freshness, quality, demand, and strategic value. Pass confirmed overlap candidates, query ownership, evidence limits, and proposed action as one diagnostic dimension.
- After `DIFFERENTIATE` or `MERGE` is approved and the content is revised, use `$article-quality-editor` to review intent clarity, factual integrity, structure, and preserved unique value.
- Use `$internal-link-architect` after page roles and stable destinations are decided. Pass the approved primary/secondary page relationship and verified inventory; do not present an overlap hypothesis as a settled link architecture.
- Use `$skill-router` when the request combines cannibalization diagnosis with refresh, editing, or link implementation. A typical sequence is detect → human decision → revise/merge → editorial review → internal-link design → measure.
