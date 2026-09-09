---
name: agent-prose
description: "Write or audit agent-facing instructions: skills, context files like AGENTS.md, and what they point to. Use when creating or changing one, when the user names one to review, or to record their standing conventions. Not for end-user prose, code design, or running a skill."
disable-model-invocation: false
---

Write or audit documents that direct an agent, so that every run follows the same decision procedure; outputs may still differ.

## Classify the request

- **Record or update personal conventions.** Take the personal-conventions path.
- **Review or audit.** Take the audit path, whether the target is named by a path or established in the conversation.
- **Create or revise.** For other agent-facing documents, take the drafting steps.
- **The target is a skill.** Read [PACKAGING.md](PACKAGING.md) before deciding or judging its frontmatter, listed or manual mode, description, split, shared files, or menu behavior.
- **A distinction matters.** Read [GLOSSARY.md](GLOSSARY.md) for every audit, and during drafting whenever a decision turns on the difference between two of its terms (pointer against link) or a term used below is one you could not define.
- **Reading cannot settle whether a sentence or structure changes what the model does.** Run [BLIND-COMPARISON.md](BLIND-COMPARISON.md); assumed defaults are not evidence.

Done when the request has one path and the siblings that path needs are open.

## Drafting

Read up to two relevant neighbouring documents in the repo before writing. Existing local conventions, not this file, decide headings and list forms. With one neighbour, use it and proceed; with none, proceed using any supplied local conventions, or simple headings and lists suited to the task if none are available. Reuse context files already supplied instead of searching for them. Do not invent neighbours or search unrelated files to reach a count.

1. **Fix the remit and the paths.** State what the document covers and where adjacent work goes. List its paths, one per substantively different case. Done when every case the document handles is on the list and every adjacent case has a named destination.

2. **Place every block on the ladder.** Steps first. Support every path needs goes after the steps in the same file. Support only some paths need goes in a sibling behind a pointer, however inconvenient the move. A flat rule set with no steps is a legitimate shape; do not force it into a sequence. A concept's definition, its rules, and its exceptions sit under one heading. Done when every block has a rung and nothing every path needs sits behind a pointer.

3. **Write the pointers.** A pointer names its destination and every condition that must send the agent there. When a needed file is under-reached, sharpen its condition before inlining anything. Always-visible text (a description line, a context file) is paid on every turn: keep it terse, put the most discriminating words first, and carry nothing the destination already supplies. Done when every disclosed file has a pointer whose condition covers each path that needs it.

4. **Bound every step.** End each step with a done condition an agent can recognize, that demands real work, and that is exhaustive where the task allows. A flat rule set gets a coverage bar instead ("every X has a verdict"). When agents stop early, sharpen the bound first; split the sequence only when a bound cannot be made definite and early exit has been observed, then hide the later steps behind a real boundary, a handoff or an isolated subagent, since an in-context call hides nothing. Done when every step has a done condition you could check against the artifact.

5. **Keep only what changes behavior.** Test each sentence against what the model does without it and delete the inert ones instead of rewriting them. Say the wanted behavior; a prohibition survives only as a hard safeguard, paired with the wanted behavior. Anchor behavior with established compact terms the model already knows, coin a term only when it is fully defined and worth its cost, and put such a term in a description only when user requests, prompts, project documentation, or code already name the work by it. Facts the agent can inspect cheaply (a CLI's `--help`) are looked up, not cached in prose. Give each meaning one home and delete anything stale. Done when every remaining sentence changes a decision.

6. **Close the silent defaults.** Find decisions the document leaves to model defaults: what is in scope, what authority the agent has to edit, write, or delete, when it hands off and to whom. State each; leave one open only when it is a genuine conditional path, never merely on purpose. Done when every consequential decision is stated or is a conditional path.

## Personal conventions

1. **Find what exists.** Read the convention documents already in force for the user and the project: user-level and project `AGENTS.md`, `RULES.md`, and any file they point to. Done when you can list what each already decides.
2. **Preserve by default.** Keep every existing rule the request does not contradict; replacing the set outright needs the user's approval first. Done when every dropped rule has a contradicting request or that approval.
3. **Gather evidence.** A preference the user states is evidence. A habit you observe becomes a rule only with repeated corroboration. Use only this conversation and transcripts the user handed you. Ask only short questions whose answers change a trigger, an authority, an output, or a workflow and that this record does not already answer. Done when every candidate rule has its evidence listed beside it.
4. **Write decision rules.** Each rule says when it applies and what to do, not what the user is like. Do not repeat the skill list, which is already in context. Then run drafting steps 2 to 6 on the set. Done when every rule is a condition and an action with one home.
5. **Validate.** Compare each rule with its evidence; when its effect on behavior is uncertain, run [BLIND-COMPARISON.md](BLIND-COMPARISON.md) before adopting it. Done when no uncertain rule was adopted untested.

## Audit

Read the target in full and every file it points to, directly or through another file, before judging any passage; dispatch read-only `scout` subagents in one batch when the tree is large. Then run the passes in order.

1. **Reachability and remit.** List every path, every pointer and load mechanism that leads to material, and every scope boundary. For a skill, inspect the frontmatter and the description; for a linked file, inspect the exact loaded text that points to it. Name promises the body does not keep, needed paths no trigger reaches, overreach, and consequential decisions left unstated. Done when every path, pointer, and boundary has a verdict, reachable or not.
2. **Behavior change.** Judge every sentence on its own against the model's ordinary behavior and mark it changing or inert; an inert sentence gets removal, not polish. When the default is uncertain, defer that sentence to a blind comparison. Done when every sentence has a verdict.
3. **Placement and maintenance.** Assign each surviving block a rung: step, local support, or a named disclosed destination. Check each pointer's wording, each concept's co-location, overlength, stale buildup, duplicate homes, and prose that caches inspectable facts. Done when every block and pointer has a verdict and every problem is pinned to a passage.
4. **Done conditions.** For each step, rate the bound on recognizability and on demanded work; for a flat rule set, rate the coverage bar. Pair each weak bound with a concrete replacement that is observable and demanding. Done when each step or rule body has a verdict.
5. **Packaging.** Skills only. Done when the bar in PACKAGING.md is met.

Report one list in descending behavioral risk: failures that keep needed material from loading or cause major scope drift first, weak local wording last. Each finding gives the location and excerpt, the failure mechanism, the behavioral consequence, and exactly one repair: removal, relocation to a named file, sharper pointer wording, compression through an anchor, positive restatement, or an explicit boundary. Edit nothing unless the request included implementation. Done when every finding has all four parts.

## Adjacent work

`shape` for an idea too unformed to instruct. `shakedown` for pressure-testing a draft's assumptions. `intent`, then `spec`, then `plan` for capturing a need, slicing it, and sequencing implementation. `software-design` for code structure and interfaces. `pr` for pull requests, `linear` for tracking. `natural-english` for prose that reads as machine-written; it does not replace the behavioral analysis here. `handoff` is the user's to invoke when live work passes to a successor, never yours to load; suggest it by name.
