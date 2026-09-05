# Kernels-to-Code Kernel — Stub Inventory → Bracketed Subagent Dispatch → Per-Stub Oracle-Gate → Journal

## Fuse
Run `kernels-to-code` after `spec-to-kernels`. It takes the kernel prototypes + stubs (from spec-to-kernels's output: `stub-emit + kernel-emit`) and turns each stub into verified code via bracketed subagent dispatch with per-stub oracle discharge.

## Payload
- `workflow.json` — JESL graph: `k2c-inventory(pipeline) -> k2c-dispatch(subagent-dispatch, bracketed) -> k2c-oracle-gate(oracle-gate) -> k2c-journal(journal-sink)`. The dispatch node is bracketed: `contract:"code-spec", repair:{target:"k2c-oracle-gate",max:2}, confidenceFloor:0.55` — the W4 prompt.ts pattern (max 2 repairs, 0.55 → UNCLEAR).
- `activities.ts` — Effect Activities: `inventoryStubs(raw, registry)` → `processStub(stub, registry, runId)` via `SubagentCap.dispatch(promptFile)` stub-mode (returns code snippet) → per-stub `oracle-gate` via `mpse/oracle.ts discharge` (integer-equality, float+epsilon, NaN→CONTRADICTED) → bracket repair loop (max 2, confidence 0.55 floor) → `runKernelsToCode(input, opts)` journals every step (invoke/verdict rows, sha256 chain via Journal service).
- `fixtures/sample-stubs.json` — minimal stub inventory from spec-to-kernels output (stub-a int 42 + stub-b float 0.6±0.05).

## Launch
```ts
import { runKernelsToCode, makeStubFixture } from "./kernels/kernels-to-code/activities"
import { makeJournal, Journal } from "./core/journal"
import { Subagent } from "./core/caps"
import { Effect, Layer } from "effect"

const stubs = [makeStubFixture("stub-a", 42), makeStubFixture("stub-b", 0.6, 0.05)]
const fakeSubagent = Layer.succeed(Subagent, { dispatch: (promptFile: string) => Effect.succeed({ text: "42", confidence: 0.9 }) })

const report = await Effect.runPromise(
  runKernelsToCode(stubs, { runId: "k2c-demo" }).pipe(
    Effect.provide(Layer.merge(Layer.effect(Journal)(makeJournal), fakeSubagent))
  )
)
// report: { pass, fail, inconclusive, rows: [{ stubId, code, verdict, attempts, discharges, evidence }], runId, inventory, chainValid }
```

## Laws
- Law 12 LOWEST-COMPOSITION — bracket repair ≤2, confidence 0.55 → UNCLEAR (W4 prompt.ts pattern). 3 violations → FAIL.
- Law 7 — per-stub oracle-gate MUST pass — 3-strike violation → FAIL loud, never INCONCLUSIVE masquerading as PASS.
- D15 — bracketed dispatch: unbracketed generation is refused at schema (tier-2 requires bracket).
- Law 6 — every step journals (invoke/verdict rows, sha256 chain). Verdict FROM rows.
- K2 — core purity: Subagent cap via Context, never raw Promise.

## Workflow
`bunx jesl run jesl/kernels/kernels-to-code/workflow.json --in jesl/kernels/kernels-to-code/fixtures/sample-stubs.json`

## Dispatch contract (stub-mode)
`SubagentCap.dispatch(promptFile)` where `promptFile = kernels-to-code/stub-<id>.prompt` and the cap returns `{ text: code, confidence, model? }` or string code. The prompt file is spec-file ONLY — the WAVE VERBATIM law (D15).
