---
name: youpu-reckoner
description: Forecast uncertain macro, geopolitical, economic, industry, market, and global events from natural-language questions using operational definitions, historical reference classes, official and physical data, cross-asset signals, optional prediction-market quotes, auditable analyst ranges, scenario pathways, monitoring indicators, revision logs, and self-contained HTML/SVG risk reports without assuming market efficiency. Use by default for questions such as war risk, recession risk, energy crises, sanctions, supply-chain disruption, policy outcomes, or asset outlooks even when no prediction contract exists. When the user explicitly asks whether a prediction-market contract is mispriced, tradable, reliable, or an arbitrage, route to the separate contract-audit workflow.
---

# 有谱 Reckoner：question-first forecasting

Match the product lockup to the report language:

- Chinese: **有谱 Reckoner** — **有依据的判断，白纸黑字的验证（Forecast on the record）**.
- English: **Youpu Reckoner** — **Evidence-backed judgments, forecasts on the record**.

Mirror the user's language by default. Build target definitions, evidence explanations, and
monitoring text in that language as well; do not merely translate the renderer chrome. An English
question must produce an English Markdown report and use the automatic English HTML/SVG rendering
path unless the user explicitly requests another language. A direct language request overrides
question-language detection.

Use lifecycle language precisely:

- **开始研判** for a new question or an unrecorded working draft;
- **落子并记录** only after the user authorizes personal audit logging and the append succeeds;
- **等待应验** for a recorded forecast that remains pending or disputed;
- **应验复盘** for outcome resolution, scoring, calibration, and postmortem review.

For English output, use the fixed equivalents **Begin the assessment → Commit it to the record →
Await resolution → Review the outcome**. Do not insert the Chinese lifecycle labels into an
otherwise English report.

Never call an unpersisted report “落子”, and never call an unresolved forecast “应验”.

Treat the user's question about the world as the primary object. A prediction-market contract is
an optional observation, never a required input or the system's ontology. Produce a transparent,
revisable range rather than claiming privileged foresight or market efficiency.

## Route before loading details

- Use the **macro forecast workflow by default** for event risk, probability, outlook, scenario,
  policy, geopolitical, economic, industry, or asset questions. It must run without a contract.
- Only when the user explicitly asks about a contract, quote reliability, trade, payoff, or
  arbitrage, read [references/contract-audit.md](references/contract-audit.md) and use the contract
  audit workflow.
- In macro mode, do not import `youpu_reckoner.costs` or `youpu_reckoner.decision`. Do not report
  order books, depth, fees, funding costs, payoff calculations, or a no-trade zone.

## Non-negotiable epistemic rules

1. Keep reference-class rates, market observations, analyst ranges, and calibrated model outputs
   visibly separate.
2. Do not call a market quote a physical probability without a relevant passing out-of-sample
   `CalibrationArtifact`.
3. Define the event, horizon, resolution basis, and near misses before estimating it.
4. Never publish a naked analyst point. Give a plausible range, assumptions, sensitivities,
   provenance, rival explanations, and falsifiers. A center is optional.
5. Use scenario pathways as qualitative scaffolding, not as a probability calculator. Never
   multiply, aggregate, propagate, or otherwise synthesize pathway intervals into a target range.
6. Express evidence strength only as `weak`, `moderate`, or `strong`, always with a written reason.
   Never assign numeric evidence weights.
7. Deduplicate observations by labeled `shared_factor`; feeds and tickers are not independent votes.
8. Do not assume pathways are mutually exclusive or collectively exhaustive. State coverage and
   use partition arithmetic only after proving a true partition.
9. Permit `abstain` when the event cannot be made resolvable. Permit a clearly labeled
   `permitted_unvalidated` analyst range when structured judgment is useful but uncalibrated.
10. Do not enable personal audit logging without explicit user authorization. Research-panel
    logging remains separate.
11. Enforce scope monotonicity on every displayed range: broad bounds must be at least base bounds,
    and base bounds must be at least narrow bounds. Put supplementary numeric ranges in
    `ScopeJudgment`; never carry a scope range only in prose.

## Default macro forecast workflow

### 1. Build a question-first target

Create a `ForecastTarget` from `youpu_reckoner.targets` with broad, base, and narrow
`TargetDefinition` variants when they are meaningfully distinct. Every target must include:

- the user's original question and a versioned target ID;
- timezone-aware horizon start and end;
- at least a base operational definition;
- structured `geography`, `event_type`, measurable `threshold`, and `occurrence_rule` fields for
  every definition;
- a resolution basis for each definition;
- explicit near misses.

Present the three definitions compactly. Continue with `BASE` unless the ambiguity would
materially change the task; let the user override it. For labels such as “world war”, “collapse”,
“energy crisis”, or “extreme weather”, narrow them into observable criteria or abstain. A
probability must always travel with its exact observation dates and complete base criterion. If
the estimate covers “at least once during the horizon” but does not identify a sub-period, say so;
do not invent a likely month or date.

### 2. Build a historical reference class

Create a `ReferenceClass` with numerator, denominator, inclusion rule, period, applicability, and
uncertainty. Use a Wilson interval when the unit and sampling interpretation support one, but do
not mechanically convert annual frequencies into a six-month forecast or treat dependent years
as independent trials. Label weak analogies as descriptive near-references.

### 3. Collect evidence across relevant channels

Read [references/data-sources.md](references/data-sources.md) to choose providers and
[references/providers.md](references/providers.md) for source-specific limits. Core analysis must
work without API keys. Use a prediction market only if a meaningfully mapped contract happens to
exist; do not search for a contract before deciding which evidence channels the question needs.

Represent each observation as `EvidenceSignal` from `youpu_reckoner.signals`:

- channel and source;
- source observation time;
- affected pathway IDs, or empty for global evidence;
- direction: raises, lowers, ambiguous, or context-only;
- ordinal strength plus a written rationale;
- `shared_factor` for dependence control;
- rival explanation and falsifier;
- immutable snapshot IDs when raw data was captured.

Use channels by role rather than by prestige:

- reference class for historical anchoring;
- official assessment for declared intent, capability, policy, or measurement;
- physical activity for observable real-world state;
- financial market for risk pricing, funding, stress, and transmission;
- prediction market for a fallible crowd quote;
- news event for discovery and chronology, not automatic probability;
- structural for trade, energy, fiscal, alliance, or supply-chain exposure;
- expert judgment for attributed interpretation with explicit uncertainty.

### 4. Deduplicate factor families

Pass `EvidenceSignal` objects or their `shared_factor` labels to
`count_independent_factors()`. Explain correlated signals and contradictions. VIX, falling equity
prices, credit spreads, and risk-sentiment indices may all load on one global-risk factor.

### 5. Build qualitative scenario pathways

Create several `ScenarioPathway` objects. Each requires at least one observable `Indicator` and
one falsifier. Declare whether the set is partial, overlapping, or proven MECE; partial and
overlapping is the default.

A pathway may disclose its own analyst interval only when assumptions are stated. Never expose or
invent a function that combines pathway intervals. The target range is a separate structured
analyst judgment; pathways disclose why that judgment could move.

### 6. Create and permit the target range

Create `AnalystEstimate` with the `ForecastTarget`, a mandatory range, optional center,
assumptions, sensitivities, reference class, evidence dependencies, provenance, and
`AuditableRationale`. New macro estimates must place all used `signal_id` and `pathway_id` values
in the rationale. Run `assess_analyst_estimate()`.

- `permitted_unvalidated`: structured and auditable, but predictive validity is not demonstrated;
- `permitted_calibrated`: relevant provenance matches a passing out-of-sample artifact;
- `denied`: the target or provenance fails a hard gate.

The analyst range must be stated directly and signed through `EstimateProvenance`; do not claim it
was calculated from pathway intervals or quote aggregation.

### 7. Record revisions only in an authorized ledger

If the user has explicitly enabled personal audit logging, append `forecast_created` for the first
estimate. On a revision, call `append_revision()` with changed signal IDs, reason, old range, and
new range. Verify the ledger hash chain. Without authorization, do not persist personal analysis;
still state “first forecast” or summarize the comparison in the report.

### 8. Render the default report

Use `MacroForecastReport` and `render_macro_report()` or follow its exact section order:

1. Target definitions: broad/base/narrow and the adopted scope.
2. Baseline range: optional center and analyst permit label.
3. Scenario pathways and their indicators, with the non-MECE coverage statement.
4. Evidence list: channel, direction, ordinal strength, rationale, and deduplicated factors.
5. Change from the previous forecast and the signal IDs responsible; say “first forecast” if so.
6. Revision triggers: the most important observable indicators.
7. Main uncertainty sources.
8. Only if a mapped contract exists, one line comparing its raw quote with the analyst range.

In section 8, do not expand the order book or calculate a trade. Direct the user to contract audit
mode if they want execution analysis.

After writing the Markdown report, call `write_html_report(report, markdown_path)`. Its default
`locale="auto"` detects Chinese script in `report.target.question`; Chinese questions render in
Chinese and other questions render in English. Use `locale="en"` or `locale="zh-CN"` only to
override that result. The selected locale must govern the product lockup, deterministic risk
phrase, share card, dossier headings, and image-export status copy. This writes a same-name,
self-contained HTML sibling and opens it only when a graphical
environment is available. On desktop, the first screen must place the conclusion and reading
guide on the left and the exportable share card on the right; below 920px, stack the card
immediately after the conclusion and before the dossier. Keep the checked-in 10×10 (100-world)
array from `make_share_card()`. Never invent a risk phrase: use `risk_phrase()` and the checked-in locale
dictionaries `RISK_PHRASE_BANDS` / `RISK_PHRASE_BANDS_EN`.

The share card must retain the exact observation period, geography, event type, measurable
threshold, occurrence rule, interval, 100-world array, permit/calibration label, report hash, and
a concise disclaimer that travels with the image. Criterion text must wrap completely; never
replace it with an ellipsis. Do not put revision indicators, a “该盯什么” block, or truncated
monitoring prose on the card; keep those details in the HTML dossier.
The PNG button uses only native SVG, canvas, and Blob APIs. Do not add a CDN, web font, frontend
framework, `foreignObject`, or a center-only hero number. For an optional read-only index, run
`python3 scripts/serve_reports.py OUTPUT_DIR`; it must remain bound to `127.0.0.1`.

## Claim discipline and calibration

Use `calibrated_probability` only for a matched, versioned model with a passing out-of-sample
artifact. An unvalidated macro range is still useful when its judgment calls and limits are
visible, but must never be called calibrated or objective.

Use fixed-date or rolling-origin evaluation. Score resolved observations while retaining
cancelled, invalid, disputed, and unresolved coverage. Cluster repeated forecasts by event family
or forecast ID. Never reuse sports or election calibration for geopolitical tail events. Read
[references/evaluation.md](references/evaluation.md) before making calibration claims.

## Source and wording safeguards

- Public Form 4 filings are reported transactions, not private insider information.
- CFTC categories are positioning categories, not “smart money”.
- GDELT and similar feeds measure reported-event intensity, not event probability.
- A financial price can reflect hedging demand, risk premia, access, liquidity, regulation, and
  capital constraints as well as beliefs.
- Write “not available” for missing fields. Do not improvise.

## Validation after changes

Run the complete test suite and the skill validator. Preserve the existing behavioral contract
and add question-first regressions for Taiwan risk, recession, Hormuz disruption, and energy
crisis. The Taiwan macro prompt must omit execution sections; the Taiwan contract prompt must
load [references/contract-audit.md](references/contract-audit.md) and retain v0.2.1 behavior.
