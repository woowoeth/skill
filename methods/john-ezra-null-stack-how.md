---
name: how
description: Explain how existing code works by tracing a path from trigger to effect, with owners and boundary crossings. Use when the user asks how something works, how a flow or subsystem runs, who owns what, where code or a layer belongs, or wants a tour of unfamiliar code. Rationale and history are `why`; design verdicts are `software-design`.
disable-model-invocation: false
---

Trace the code as it stands and explain it, from the event that starts a path to the effect it leaves. Read-only: a how question never becomes a fix, a feature, or a redesign. History and motive go to `why`. Critique ("is this well designed", "how would you restructure this") runs this skill first, then hands the modules on the path to the review branch of `software-design`; do not score the design or invent your own architecture rubric here.

## 1. Fix the scope

Take the narrowest reading the conversation and repository support; never ask the user to choose. When two readings would send you to different code or answers, say in one sentence which you took and keep going. Done when you can name the entry point and the effect.

## 2. Narrow or wide

- **Narrow.** One module, helper, or short call chain: trace it yourself.
- **Wide.** Several modules, packages, or processes, or a user action through to durable state: cut two to four slices by the kind of knowledge each needs (control from trigger to effect; domain state and its transformations; what persists; process or service boundaries; configuration on the path; what the caller observes), never by file count or file ranges. Dispatch one read-only `scout` per slice in a single batch, each with the whole question, its slice's explicit edges, and the evidence rules below; you synthesize. Done when every part of the path belongs to exactly one slice.

## 3. Trace each slice

1. **Find the trigger.** What actually starts the path (a handler, CLI command, inbound request or message, framework hook, scheduled job), named by file and symbol.
2. **Navigate by the language server.** Focused `grep` only when it is absent or returns nothing useful.
3. **Read bodies.** Names, filenames, and signatures are not evidence.
4. **Record each hop.** What arrives, what it becomes, which branch is taken, what state mutates, which errors are caught or propagated, what leaves.
5. **Name owners and boundaries.** Per module, the one responsibility it owns, in the repository's domain terms; per crossing into a database, another service, a process, an external API, or another area of the codebase, what crosses.
6. **Read around the path only when it changes the answer.** Tests, configuration, and callers when they set observable behavior (a default that picks the branch) or a constraint the code alone does not show (a lock order); skip them when they would only confirm the implementation.
7. **Record gaps.** A hop you could not read, reach, or follow (generated code, dynamic dispatch, a dependency without source) is written down as a gap, never bridged with a plausible story.

A slice is done when you can state its trigger, path, owner of each step, boundary crossings, and gaps, with no step resting on an unread hop; exploration is done when every slice is.

## 4. Write the explanation

Lead with an answer the reader could stop at, then five layers, each assuming only what came before; skip an empty layer rather than pad it.

1. **Overall behavior.** What it does, what starts it, and the main route, in a few sentences.
2. **Concepts.** Only the types, states, and modules the walk uses, each defined in one sentence at first use, in the repository's vocabulary.
3. **Walk.** Trigger to effect; every step names path and symbol and what happens there: transformation, decision, state change, error path, boundary crossing.
4. **Source map.** Where each responsibility lives, as a compact table or list.
5. **Caveats and gaps.** Surprising behavior, edges that will trip the reader, and every gap from the trace, each marked unverified or inaccessible.

Wide work delivers one integrated account, never scout reports. Done when every slice is represented and every repository claim passes the evidence rules.

## Evidence rules

- **Cite.** Every repository claim carries `path:line`; without one it is an opinion.
- **Separate seen from inferred.** An observation is what the cited line says; an inference is a conclusion from several observations, labeled as one and naming the observations it rests on.
- **No motive from shape.** Current structure does not reveal intent, history, or evolution; older versions, other branches, and commit history are out of scope.

## Diagrams

Draw one only when prose would leave the reader reconstructing a relationship in their head, such as three services passing messages in a fixed order. Build any diagram of three or more parts in stages: two parts and their edge first, then one more part with its edges per stage, keeping everything already drawn.
