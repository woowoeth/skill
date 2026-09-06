---
name: sci-ai-skill
description: Build editable, publication-ready scientific figures in Adobe Illustrator 2023 from traceable source panels, using Illustrator COM/MCP or visible Windows Computer Use, staged construction, and evidence-gated visual QA. Use when a user wants a Nature-style figure assembled or revised in Illustrator 2023.
---

# Sci AI Skill

All user-facing conversation must be in Simplified Chinese.

## Scope

- The scientific claim, panel data, statistics, and source panels remain
  traceable to the user's Python/R source workflow. Illustrator is the vector
  assembly, annotation, and finishing surface; it must not invent numerical
  results.
- The primary target is Adobe Illustrator 2023, application version 27.x,
  exposed on Windows as `Illustrator.Application.27` /
  `Illustrator.Application`.
- Keep an editable `.ai` source and export reader-facing PDF/SVG. A flattened
  image is a preview, never the only deliverable.
- Work on a copy or a temporary document until the user approves the result.
  Do not directly edit an exported manuscript PDF to change scientific content.

## Operating modes

Choose the least fragile mode that satisfies the request:

1. **MCP/COM mode**: use a registered Illustrator MCP server for repeatable
   object-level operations, document inspection, and export.
2. **Visible mode**: use Windows Computer Use when the user wants to watch the
   Illustrator canvas. Observe the current window, perform one action, refresh
   the screenshot, and verify the result before the next action. Never automate
   a terminal through the UI.
3. **Hybrid mode**: generate scientific panels from the selected plotting
   backend, then import and assemble them visibly in Illustrator. This is the
   recommended mode for Figure 1 and other Nature-style composites.

Read [references/illustrator-2023-contract.md](references/illustrator-2023-contract.md)
for version, object, coordinate, and export details. Read
[references/visible-operation.md](references/visible-operation.md) before any
visible Windows operation. Read [references/qa-checklist.md](references/qa-checklist.md)
before release.

## User commands

- "开始一个新的 Illustrator 2023 科研图构建项目" creates a fresh project.
- "继续" reads the project state and performs only the next legal action.
- "进入可视化操作" selects the visible Illustrator mode.
- "只修改 ..." changes only the named objects or panels and records a
  checkpoint before mutation.
- "导出并检查" runs the structural and visual QA gates before export.

## Project state and provenance

Use a project-local state directory rather than storing work in the installed
skill:

```text
PROJECT/
├── 00_reference/
├── 01_source_panels/
├── 02_illustrator/
│   ├── source/
│   ├── previews/
│   └── qa/
├── 03_output/
│   ├── ai/
│   ├── pdf/
│   └── svg/
├── 04_logs/
└── .illustrator_recon/
    ├── project_state.json
    ├── panel_registry.json
    └── checkpoints/
```

The panel registry records, for every panel, data origin, source script or
bundle, seed/sample selection, dimensions, imported file hash, and final
Illustrator object or layer name. When a panel depends on a remote result,
record the authoritative remote path and any local mirror path.

## Workflow

### 1. Capability gate

Before building, verify a real Illustrator 2023 path:

- Check the COM registration and version with
  `scripts/check_illustrator_2023.py`.
- Prefer a registered MCP tool inventory and a real status/document-info call.
- Otherwise use visible mode and confirm the unique Illustrator 2023 window.
- In a temporary document, verify at least one rectangle/path, editable text,
  a layer or group, save-as `.ai`, and SVG/PDF export. Record the observed
  result and hashes. A static README or historical PASS is not a capability
  gate.

If the version, connection, or export check fails, stop at the gate and report
the exact blocker. Do not silently fall back to an unverified backend.

### 2. Figure contract

Write the one-sentence conclusion the figure must defend, map each panel to a
unique piece of evidence, classify the composition, and set final dimensions,
fonts, colour mode, editable-text policy, export formats, and source-data
requirements. Drop panels that do not carry a distinct inferential role.

### 3. Source-panel handoff

Import existing SVG/PDF/PNG panels only after checking dimensions, colour mode,
font policy, and hashes. Prefer editable SVG paths or native Illustrator text
for labels, equations, arrows, and simple geometry. Keep raster components at
the required effective resolution and record whether they are linked or
embedded. Never replace a missing font silently.

### 4. Staged Illustrator construction

Create explicit layers such as `REF_OVERLAY`, `PANELS`, `ANNOTATIONS`,
`ARROWS`, and `QA_GUIDES`. Build from back to front. Keep the reference in a
locked, non-printing overlay layer; it must be hidden and excluded from every
final export. Use stable object names and parent paths so later revisions do
not depend on selection order.

After every material mutation, read back the document or refresh the visible
window and verify that a real object, layer, group, transform, or text frame was
added or changed. Save a checkpoint before broad revisions.

### 5. Evidence-gated QA and revision

Run structural checks for artboard size, panel alignment, overflow, layer
visibility, font availability, colour mode, linked files, stroke widths, and
editable text. Run visual checks at full canvas and detail zoom for spacing,
occlusion, arrow endpoints, labels, line weight, contrast, and clipping.

For a mismatch, identify a unique object or panel cause before correcting it.
After two non-improving correction cycles, pause and report
`BLOCKING_OBJECT`, `CAUSE`, `CURRENT_LIMITATION`, and `RECOMMENDED_ROUTE`.

### 6. Delivery

Deliver the editable `.ai`, reader-facing PDF/SVG, panel registry, source-data
references, and QA report. Confirm that the reference overlay is hidden,
temporary guides are excluded, fonts are resolved or explicitly documented,
and the exported files open and have non-zero size. Keep the source registry
with the manuscript figure package; do not place logs or run-level archives in
the clean manuscript `figures/` directory.

## Integrity boundaries

- Do not claim exact reference matching unless the comparison gate passes.
- Do not fabricate a panel, metric, label, or source path.
- Do not convert a user-directed adaptation into a scientific result.
- Do not overwrite the user's existing Illustrator document without an explicit
  request and a recoverable checkpoint.
