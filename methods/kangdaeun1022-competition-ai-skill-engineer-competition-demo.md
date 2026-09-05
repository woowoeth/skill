---
name: engineer-competition-demo
description: Design and rehearse a reliable competition demo around a judge-relevant magic moment, deterministic path, fallback, offline mode, reset plan, and failure recovery. Invoke for “데모설계”, demo script, live presentation reliability, hackathon demo, or prototype rehearsal requests.
metadata:
  short-description: 심사장 데모 설계와 리허설
---

# Engineer the competition demo

## Purpose

Make one important claim observable under real presentation conditions. A demo is evidence of the narrow behavior it shows; it is not proof of production scale, user adoption, model accuracy, or impact beyond the test.

## Start with the magic moment

Define one **magic moment** in this form:

```text
When [specific user] encounters [verified problem moment], they use [implemented capability]
to make or complete [better decision/action], and the audience can observe [artifact/output].
```

Tie the magic moment to one official criterion and one claim in the deck. If it cannot be described without a marketing adjective, narrow it. Prefer one decisive user outcome over a tour of every feature.

## Design a deterministic path

Write a numbered script that a teammate could execute cold:

| Step | Presenter action | Expected system state / visible proof | Claim proved | Time | If it fails |
| --- | --- | --- | --- | --- | --- |

Use known-good fixtures, a fixed account/role, controlled sample inputs, prevalidated permissions, and a versioned build. Specify exactly which data are synthetic, anonymized, historical, live, or unavailable. Do not imply that fixture success proves live performance.

Keep the critical path short. Every step must either advance the magic moment or be removed. Set a presentation time budget with a hard stopping point before Q&A.

Use the official demo duration; when unspecified, target 2–3 minutes and label it a rehearsal default. Policy/idea entries may demonstrate an accountable operating scenario with the same visible decision and recovery logic.

## Engineer recovery before polish

For each dependency—network, API/model, login, device, browser, data, integration, projector—record failure probability, detection point, and recovery owner. Prepare all of the following:

- **Fallback:** a local, prevalidated alternative that demonstrates the same narrowly stated behavior when feasible; label recordings, screenshots, and mock outputs honestly.
- **Offline mode:** a network-independent route or a concise truthful statement of the remaining limitation. Do not silently switch live results for prerecorded ones.
- **Reset plan:** exact instructions to return account, local data, browser, device, and app state to the known-good start state; rehearse it.
- **Recovery script:** one spoken sentence while recovery occurs, the time limit, and the decision to move to fallback.

Never rely on a live external service without a fallback or an explicit decision to omit it from the critical path.

## Rehearsal protocol

Run and log at least these rehearsal modes when the environment permits:

1. normal deterministic run;
2. cold-start run after the reset plan;
3. network or dependency failure → fallback/offline recovery;
4. constrained-time run with the presenter’s actual narration;
5. observer run in which a reviewer states what they believe was proved.

For every failure, classify `demo blocker`, `clarity gap`, `noncritical defect`, or `environment risk`; fix blockers before adding features. A demo is ready only when the observer identifies the intended claim without prompting and the recovery path stays within the time budget.

## Output

Return the magic-moment statement, criterion/claim linkage, deterministic script, dependency and truth-label register, fallback/offline/reset/recovery plans, rehearsal log, remaining risks, and a short presenter cue card. Feed only verified demo claims to the deck and Q&A skills.
