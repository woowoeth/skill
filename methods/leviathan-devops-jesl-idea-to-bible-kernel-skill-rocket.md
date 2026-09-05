# Idea-to-Bible Kernel — Skill Rocket

## Fuse
Fire when a raw natural-language idea arrives and a structured bible is needed before MPSE. This is kernel 1 of 6 in the lifecycle chain; its output feeds `bible-to-spec`.

## When to Fire
- Input is a plain idea string (1–2000 chars), no prior bible exists
- The pipeline needs parallel exploration (domain / constraints / value) merged into a schema-gated bible
- The journal chain must start — this kernel seeds the lifecycle's sha256 evidence spine

## Payload
- `workflow.json` — JESL graph: `validate-idea -> parallel(explore-a,b,c via Llm) -> merge-bible -> schema-gate -> journal-sink`. Tier 2 (generation bracketed `contract: json`), 7 nodes, 8 edges, fan-out at validate via `idea` channel.
- `activities.ts` — Effect Activities journaling every step (pre+post per Law 6):
  - `validate-idea`: blank → `[JESL CHANNEL-UNSET]` structured error, never a partial bible
  - `exploreOne(angle)` via `Llm` cap — stub-mode returns scripted `ExploreResult` per angle; live mode calls `Llm.callModel`
  - `mergeToBible(idea, results)` → `BibleDoc` (`$schema: trident-workflow-v1`, 4 nodes, 3 edges)
  - `schemaGateBible(bible)` → `decodeDoc + validateDoc` (Law 7: gate failure = structured error, never a partial dressed as bible)
  - `runIdeaToBible(idea, {runId})` — the single-entry kernel: validate → Effect.forEach(angles, exploreOne, concurrency 15) → merge → schema-gate → journal-sink. Every step writes invoke+verdict rows with `source: workflow/idea-to-bible/<node>`, sha256-chained via Journal service.
  - `makeStubLlmLayer(scripted?)` + `StubLlmLive` — test/live Llm stub; `buildNodeHandles(idea, runId)` — executor wiring for `runProgram(doc, ctx)`.
- `fixtures/sample-idea.txt` — real idea fixture
- `fixtures/expected-bible.json` — bible-shaped WorkflowDoc fixture (valid trident-workflow-v1, 4 nodes, 3 edges)

## Launch
```ts
import { runIdeaToBible, makeStubLlmLayer } from "./kernels/idea-to-bible/activities"
import { makeJournal, Journal } from "./core/journal"
import { Effect, Layer } from "effect"
const idea = "Build a mechanically intelligent code review tool..."
const journal = yield* makeJournal
const bible = await Effect.runPromise(
  runIdeaToBible(idea, { runId: "idea-to-bible-demo-1" }).pipe(
    Effect.provide(Layer.merge(Layer.succeed(Journal, journal), makeStubLlmLayer()))
  )
)
// bible.$schema === "trident-workflow-v1", bible.meta.name starts with "bible-"
// journal.verify(runId) === true, rows.length >= 14 (2 per step × 7 steps)

// Via executor:
import { runProgram } from "./core/executor"
import raw from "./kernels/idea-to-bible/workflow.json" with { type: "json" }
import { decodeDoc } from "./core/schema"
const doc = await Effect.runPromise(decodeDoc(raw))
const summary = await Effect.runPromise(runProgram(doc, { runId, doc, vars: { idea }, nodeHandles: buildNodeHandles(idea, runId), caps: Context.empty(), clock, budget, ... }))

// CLI
// bunx jesl run jesl/kernels/idea-to-bible/workflow.json --in '{"idea":"..."}'
```

## Laws
- Law 3/4: Effect only, zero host imports (`effect`, `../../core/*` only)
- Law 5: 8 tokens only — blank idea → `[JESL CHANNEL-UNSET]` (not a 9th invented token)
- Law 6: journal pre+post per step, sha256 chain via Journal service
- Law 7: schema-gate MUST pass before bible is returned — gate failure = structured error
- Law 8: each step single-duty
- D11: kernel runs as Effect Workflow / JeslRun pattern (Workflow.make JeslRun, node:<id> Activities — see workflow/jesl-run.ts)

## Workflow
`bunx jesl run jesl/kernels/idea-to-bible/workflow.json --in jesl/kernels/idea-to-bible/fixtures/sample-idea.txt` → bible JSON + journal at `.trident/rockets/<run-id>.jsonl`

## Verification
- `bunx tsc --noEmit` 0
- `npx vitest run` — idea-to-bible suite: happy-path → bible schema-gate pass, blank → structured error, journal chain intact, parallel fan-out via stub Llm (Effect.forEach concurrency 15)
