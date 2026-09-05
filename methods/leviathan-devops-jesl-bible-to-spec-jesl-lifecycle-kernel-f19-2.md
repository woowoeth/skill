# bible-to-spec — JESL Lifecycle Kernel (F19 #2)

## Purpose

Consumes a bible-shaped `WorkflowDoc` (`$schema: trident-workflow-v1`) and emits a DPL1 spec `WorkflowDoc` via the Effect kernel pipeline:

```
bible → digest (hash + structural inventory) → FR extraction → math-contract lint → DPL1 template gate → journal
```

## Pipeline

1. **digest** — `digestBible(bible)` — canonical hash (`canonicalSerialize` + `simpleHash`) + inventory `{nodeCount, edgeCount, nodeIds, tier, name, via}`. Journals `bible.digest` pre/post.
2. **FR extraction** — `extractFRs(bible, digest)` — deterministic stub from `node.config.{title,description}` → `FR[]`; if `Llm` cap is bound, attempts `Llm.callModel` for structured FR JSON, falls back to deterministic. Journals `bible.fr-extract`.
3. **math-contract lint** — `lintMathContracts(bible)` — any node `config.{math,expression,expr,formula,contract}` string is parse-checked via `mpse/parser.ts:parseMathExpr`. First bad expression fails with `[JESL UNKNOWN-NODE]` structured error (field `config.math`). Journals `bible.math-lint`.
4. **DPL1 template gate** — `gateDPL1Spec(candidate)` — `core/schema.ts:decodeDoc` + `validateDoc` against `WorkflowDoc` schema. Candidate is built from FRs (`buildSpecCandidate`). Journals `bible.template-gate`.
5. **journal** — every step journals `invoke`/`verdict` via `core/journal.ts` sha256 chain (`prev`/`self`). The run journals `__run` open/close. Verify with `journal.verify()`.

## Activities

`activities.ts` exports Effect primitives, zero host imports:

- `digestBible(bible, runId?) : Effect<DigestResult, JeslError, Journal>`
- `extractFRs(bible, digest, runId?) : Effect<FR[], JeslError, Journal | Llm>`
- `lintMathContracts(bible, runId?) : Effect<void, JeslError, Journal>`
- `gateDPL1Spec(candidate, runId?) : Effect<WorkflowDoc, JeslError, Journal>`
- `runBibleToSpecSimple(bible) : Effect<WorkflowDoc, JeslError, Journal>` — full pipeline (digest → decode → FR → lint → candidate → gate) with `__run` journal bookends. Use this in tests.
- `runBibleToSpec(bible, runIdSeed?) : Effect<WorkflowDoc, JeslError, Journal | Llm>` — variant with optional Llm-driven FR path.

All steps are single-duty, `Clock.currentTimeMillis` for timing, `Effect.gen` + typed `Schema.TaggedError` JeslError codes (`[JESL ...]`), and structured `{code, node, field, expected, actual, remedy}`.

## Workflow

`workflow.json` is the JESL document for this kernel: `meta.name=bible-to-spec/tier=1`, nodes `digest → fr-extract → math-lint → template-gate → sink`, edges via `digest/frs/lint/spec`. Executable via `runJeslWorkflow` or `runProgram` with handles mapping each node id to the corresponding activity.

## Fixtures

- `fixtures/bible-valid.json` — 3-node bible with `math: "x + y * 2"` (happy path).
- `fixtures/bible-math-bad.json` — 2-node bible with `math: "@@@invalid math (("` (lint must refuse).
- `fixtures/bible-minimal.json` — 1-node minimal bible (edge case).

## Testing

```ts
import { runBibleToSpecSimple } from "../kernels/bible-to-spec/activities"
import { makeJournal, Journal } from "../core/journal"
import { Layer } from "effect"
// happy
const journal = yield* makeJournal
yield* runBibleToSpecSimple(bibleValid).pipe(Effect.provide(Layer.succeed(Journal, journal)))
// missing bible → [JESL CHANNEL-UNSET]
// bad math → [JESL UNKNOWN-NODE] with field config.math
// journal chain → yield* journal.verify()
```

## Caps

- Requires `Journal` (always). `Llm` is optional for FR extraction enrichment; stub-mode without it is the default tested path.
- Zero `node:fs` / `fetch` / `Date.now` in kernel code — pure Effect + `Clock`.

## Schema Gate

Output spec validates via `decodeDoc` + `validateDoc(isKnownKind)` where `isKnownKind` is the `ALL_KINDS` registry set. Invalid candidate never ships — loud `JeslUnknownNode` / `JeslCycle` / decode error.

## Journal Invariants

- `row[0].prev === "genesis"`, `row[n].prev === row[n-1].self`, `self = hash(canonical(row minus self) + NUL + prev)`.
- `source` always `workflow/bible-to-spec/<node>`.
- Every `invoke` has a matching `verdict`.

## Known Gaps

- Llm FR path is best-effort JSON parse; malformed Llm JSON falls back deterministically rather than failing — keeps pipeline deterministic for tests.
- Math lint scans keys `math|expression|expr|formula|contract`; other config shapes are not linted.

## References

- L2 §4.15 KERN-6 (2) bible-to-spec — digest → FR extraction (lexicon) → math-contract lint → DPL1 template gate
- `core/journal.ts` — sha256 chain, `covers()`, `verify()`
- `core/schema.ts` — `decodeDoc`/`validateDoc`
- `mpse/parser.ts:parseMathExpr` — MPSE lint

— END SKILL —
