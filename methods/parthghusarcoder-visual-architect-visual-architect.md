---
name: visual-architect
description: Create, validate, review, and evolve professional technical diagrams as self-contained HTML + SVG. Use for software/system architecture, cloud and infrastructure, flowcharts, sequences, ER/data models, database schemas, deployment views, data flows, process/swimlane diagrams, state machines, dependency graphs, user journeys, timelines, and technical explanations. Model semantics before drawing, choose the diagram type automatically, mark assumptions, enforce visual quality, support element-specific review, produce revision diffs, and keep diagrams consistent with source code when requested.
license: MIT
compatibility: Requires an agent capable of writing files. A browser is recommended for reviewing HTML artifacts. Optional external review tools can be used when available.
metadata:
  version: "1.0.0"
  output: "self-contained HTML + inline SVG"
  review: "built-in Review Canvas or compatible annotation tool"
---

# Visual Architect

Build diagrams that help people **understand, decide, review, and maintain** technical systems. Do not produce generic box-and-arrow art. Treat every diagram as a compact visual argument whose structure must be semantically true and visually legible.

## The experience contract

A strong Visual Architect result should feel like a senior architect and an editorial information designer collaborated on it.

The user should receive:

1. the right diagram type without needing to choose it manually;
2. a diagram that communicates its main idea in seconds;
3. explicit assumptions instead of invented facts;
4. a self-contained artifact that opens locally;
5. stable element IDs for precise review;
6. a validation pass before delivery;
7. concise revision diffs after feedback;
8. an editable/source artifact alongside any exports.

## Core workflow

Always use this pipeline:

`UNDERSTAND -> MODEL -> SELECT -> SIMPLIFY -> DESIGN -> GENERATE -> VALIDATE -> REVIEW -> ITERATE -> DIFF -> APPROVE -> EXPORT`

### 1. UNDERSTAND

Determine the audience, purpose, decision to support, system boundary, current/proposed state, important actors/entities/components, relationships, and desired level of detail.

Do not ask the user to choose a diagram type when the request gives enough information to select one.

### 2. MODEL

Build a semantic model before drawing. Identify:

- nodes/entities/components;
- groups/boundaries;
- relationships/edges;
- direction or chronology;
- cardinality where relevant;
- protocols/data carried where relevant;
- trust/environment boundaries where relevant;
- facts versus assumptions.

A diagram is a claim about a system. Never invent APIs, services, databases, queues, security boundaries, tables, or dependencies just to make the canvas look complete.

Mark uncertainty explicitly as `Assumption`, `Proposed`, `Example`, or `TBD`.

### 3. SELECT

Use `references/diagram-types.md`. Prefer:

- **architecture** for systems/components/services and connections;
- **flowchart** for decisions and branching logic;
- **sequence** for interactions over time;
- **ER/data model** for conceptual entities and relationships;
- **database schema** for physical tables, keys, and foreign keys;
- **deployment** for environments/zones/hosts/containers/deployed artifacts;
- **data flow** for how information moves or transforms;
- **process/swimlane** for multi-step or cross-role workflows;
- **state machine** for states and transitions;
- **dependency graph** for prerequisites and fan-in/fan-out;
- **user journey** for stages/actions/touchpoints;
- **timeline/Gantt** for time-oriented plans;
- **tree/layer/nested** for hierarchy.

If one canvas would become overloaded, create an overview first and focused detail diagrams second.

### 4. SIMPLIFY

Every visible element must earn its space.

Default overview target: **5–12 primary nodes**. Above that, group or split unless density is essential to the task. Do not solve crowding by shrinking text.

### 5. DESIGN

Read `references/design-rules.md` before generating a substantial diagram.

Use clear hierarchy, generous spacing, consistent geometry, intentional edge routing, readable labels, and restrained emphasis. Prefer left-to-right for system flows and top-to-bottom for hierarchy unless another direction better matches the semantics.

### 6. GENERATE

Default to a **single self-contained `.html` file with inline SVG, CSS, and JavaScript**. No external assets or runtime should be required unless the user asks for them.

For reviewable artifacts:

- give important SVG groups `data-va-id="..."` and `data-va-label="..."` attributes;
- use deterministic, meaningful IDs such as `service-fees`, `db-primary`, `edge-api-db`;
- set the SVG `role="img"`;
- include `<title>` and `<desc>`;
- never encode meaning using color alone.

When a highly interactive review experience is useful, start from `assets/review-canvas.html` and replace the demo SVG/content while preserving its review hooks.

### 7. VALIDATE

Read `references/validation.md`. Check both semantics and rendering before delivery.

At minimum verify:

- diagram type fits the information;
- title and direction are immediately understandable;
- important relationships are present;
- assumptions/current/proposed states are distinguishable;
- labels are readable;
- obvious overlaps are absent;
- connectors do not pass through unrelated nodes/labels;
- crossings are minimized;
- important elements have stable review IDs;
- the artifact can be understood without the surrounding chat.

Never claim pixel-perfect validation when you have not actually rendered/inspected the artifact.

### 8. REVIEW

Preferred review order:

1. use the built-in Review Canvas when producing HTML;
2. if a compatible annotation tool such as Lavish is already available, it may be used instead;
3. otherwise deliver the artifact and invite element-specific feedback.

Treat feedback as targeted change requests, not a generic rewrite.

Recommended states:

`Requested -> Working -> Ready for Review -> Approved`

### 9. ITERATE

Preserve approved regions unless a dependency forces a change. Re-run validation after every meaningful revision.

### 10. DIFF

After revision, summarize only meaningful changes using applicable categories:

- **Added**
- **Removed**
- **Renamed**
- **Moved**
- **Relationship changed**
- **Visual-only change**
- **Assumption resolved**

Do not describe a layout move as an architecture change.

### 11. APPROVE

Continue until the user approves or asks to stop. Do not endlessly redesign already-approved areas.

### 12. EXPORT

Keep the editable/source HTML. Produce SVG/PNG/PDF/Mermaid/draw.io only when requested and supported by available tools. Never discard the source artifact merely because an export was requested.

## Current state vs proposed state

Never silently mix them. If both are useful, prefer either:

- two clearly titled diagrams (`Current State`, `Proposed State`), or
- one diagram with unmistakable visual and textual state labeling.

## Code-to-diagram consistency

When repository/source/configuration is available and the user asks for an as-is or implementation-derived view, inspect evidence before drawing.

Map important nodes and edges to repository evidence when practical. Distinguish directly observed relationships from inference. For mismatches, report:

`Diagram says -> Implementation shows -> Recommended resolution`

Do not mutate code to match a diagram, or a diagram to match code, unless the user asks.

## Review Canvas behavior

`assets/review-canvas.html` provides a dependency-free review experience. Preserve these hooks when adapting it:

- `data-va-id` identifies the selected diagram element;
- `data-va-label` provides a human-readable label;
- clicking an element selects and highlights it;
- comments are recorded against that stable ID;
- feedback can be copied/downloaded as structured JSON;
- zoom, fit/reset, and keyboard navigation must continue to work.

For regenerated diagrams, keep stable IDs for unchanged semantic elements so feedback remains traceable across revisions.

## Output language

Use concise labels. Prefer nouns for components and short verb phrases for flows. Avoid paragraph-sized node text. Put explanations in a legend, callout, or accompanying notes rather than inside every box.

## Failure modes to avoid

Never:

- invent architecture to fill gaps;
- make every node the same visual priority;
- use tiny typography to fit too much content;
- allow connectors to run through nodes;
- create decorative gradients/shadows that reduce information clarity;
- rely on color alone;
- output a giant diagram when overview + drill-down would be clearer;
- regenerate approved areas gratuitously;
- hide assumptions inside polished-looking visuals.

## Quality bar

A diagram is finished only when a reader can answer, without the chat:

1. **What am I looking at?**
2. **What is the main flow/structure?**
3. **What matters most?**
4. **What is fact versus assumption/proposal?**
5. **Where should I look for detail?**

If any answer is unclear, improve the diagram before presenting it.
