---
name: rate-limit-this
description: Audit a JavaScript or TypeScript web app, especially Next.js, for abuse and rate-limit surfaces, ask the human only material policy questions, write a root RATE_LIMITS.md for review, and implement the approved limits in the same context or a fresh agent. Invoke manually to design fair usage policies, choose protections suited to the existing stack, or implement a reviewed rate-limit contract.
---

# Rate Limit This

Three steps: audit the app and agree on what should and should not be rate
limited, get explicit human approval of the policy, then implement and verify
the approved limits. Write the agreed policy as a durable `RATE_LIMITS.md`
before changing code.

Read repository instructions such as `AGENTS.md` or `CLAUDE.md`, then read
the root `RATE_LIMITS.md` when it exists. Its `status` tells you where to resume:

- no spec: start the audit.
- `draft`: present the draft and resolve feedback. Do not implement.
- `approved`: implement and verify only the approved policy.
- `done`: treat a new invocation as a request to audit or revise the limits.

Only explicit human approval of the whole contract changes `status` to
`approved`. Approval of one limiter, silence, or "continue" does not approve the
contract. If repository reality makes an approved decision unsafe or
impossible, stop and reset to `draft` instead of silently substituting a
different identity, limit, backend, or behavior.

## 1. Audit and agree on the limits

Read [references/detection-playbook.md](references/detection-playbook.md).
Inspect the request and work-triggering surface, existing authentication,
external services, costly operations, persistence, deployment runtime, and
current limiters. Start with JavaScript/TypeScript and Next.js conventions, but
follow the repository's actual architecture.

Identify candidate limits and explain each in product language: what resource or
experience it protects, who can trigger it, the likely cost or abuse mode,
existing identity and backend, confidence, and remaining policy questions. Rank
candidates. Do not recommend limits for harmless routes merely because they are
public. Complete the audit only after every public write, expensive external
call, security-sensitive action, upload, generation workflow, and background-job
trigger has been recorded as **limit**, **no limit**, or **defer** with a reason.

Ask one question at a time, only when the answer could materially change
protection, user experience, operational risk, or verification. Give one
recommended default based on repository evidence and explain why in one
sentence. Do not make the human choose an algorithm or provider when the
behavior and existing stack determine it. If no material gaps remain, draft
without inventing questions.

Translate answers into algorithms and infrastructure, resolving: allowance and
window; whether short bursts are acceptable; identity (authenticated user,
account, hashed API identity, IP, or an approved combination); paid, anonymous,
admin, internal, and BYOK exemptions; global cost circuit breakers; the
blocked-user experience; backend outage behavior; and Simple or Thorough
verification. Offer browser fingerprinting only as advanced opt-in after ordinary
server-verified identities are insufficient, explain its privacy and spoofing
tradeoffs, and require explicit approval. Never use it as sole protection and
never store a raw API key as an identifier.

Read [references/spec-template.md](references/spec-template.md). Create or
update one root-level `RATE_LIMITS.md`; do not create a competing JSON or YAML
spec. Give every limiter a stable ID. Set `status: draft`. Present the draft,
call out recommendations and open questions, and stop. Application code,
dependencies, schemas, external resources, credentials, and deployment
configuration must remain unchanged.

## 2. Approve the policy

Only explicit human approval of the whole current contract changes `status` to
`approved`. Before recording approval, require an empty **Open questions**
section and record who approved and when. Increment the revision whenever a
shared draft's policy changes.

## 3. Implement and verify the approved limits

Read [references/provider-routing.md](references/provider-routing.md). Choose
one suitable primary enforcement backend or platform control based on the
existing stack. Verify current official provider documentation before changing
dependencies, schemas, or platform configuration.

By default, implement in the same context after re-reading the approved
`RATE_LIMITS.md`. For sensitive apps, you may instead route implementation to a
fresh subagent whose prompt explicitly identifies it as the implementation agent
for the approved contract, giving it the approved `RATE_LIMITS.md`, repository
instructions, and codebase, not the planning conversation. If the host cannot
create subagents and the human wants the fresh-agent path, stop and ask them to
begin a fresh implementation task with that explicit role and the approved
contract. Creating an account, database, credential, OAuth grant, or deployment
secret requires action-time human confirmation even when the provider is
approved in the spec.

Guardrails while implementing: enforce at the shared boundary so a second route
cannot bypass the policy; keep check-and-consume atomic; hash or map raw API
keys, tokens, and emails, never use them as identifiers or in keys; include a
namespace per application and action; make retries and multi-step workflows
consume exactly what the approved counting point says; and define backend
outage behavior explicitly.

Use the verification depth approved in the spec.

- **Simple**: reuse existing checks and perform a focused smoke check showing
  allowed traffic, the blocked request, and the expected recovery/reset path.
  Add a small test only when the repository already has a suitable seam.
- **Thorough**: extend existing automated tests for identities, exemptions,
  headers, reset behavior, and backend failure modes, plus a safe provider
  smoke test when credentials exist.

When the contract says malformed requests do not consume capacity, validate
required fields and types before admission. Successful JSON parsing alone does
not make a request valid. Test valid JSON with an invalid shape as well as JSON
parse failures. Do not introduce a test framework solely for rate limiting.
Document checks that could not run rather than pretending they passed.

When implementation and verification are complete, set `status: done`, present
the diff, verification evidence, deviations, and remaining operational steps,
and stop before merge, deployment, publication, or announcement unless the
human explicitly asks for that action after reviewing the output.

For the optional strict four-state contract with revision metadata and a
mandatory fresh-agent handoff, see
[references/contract-states.md](references/contract-states.md).
