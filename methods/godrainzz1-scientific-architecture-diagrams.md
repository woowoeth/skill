---
name: scientific-architecture-diagrams
description: "Rebuild research system or neural-network architecture diagrams from a paper and source code using grounded ImageGen composition plus editable Mermaid reconstruction; not for generic decorative illustrations or unsupported claims."
---

# Scientific Architecture Diagrams

Use this skill when a scientific diagram must be visually polished, faithful to a manuscript/codebase, and easy to correct later. The deliverable has two explicit layers: an illustrated visual composition that establishes the scientific visual hierarchy, and a deterministic Mermaid reconstruction that preserves editable structure and wording.

## Core Workflow

1. **Ground the diagram before drawing.** Locate the authoritative manuscript, protocol/configuration, implementation files, and result/evidence records. Extract only facts that can appear in the figure. Treat training, offline validation, experiment-time deployment, simulation/replay, and hardware evidence as separate statuses.
2. **Build a claim ledger.** For every node and arrow record its label, input, output, source location, status, and whether it is measured, inferred, or merely planned. Resolve contradictions in favor of the locked protocol and current manuscript.
3. **Write a visual brief.** Define the figure's narrative, zones, main direction, node hierarchy, color roles, label budget, and an explicit avoid list. Prefer one clear story over exhaustive implementation detail.
4. **Generate and save the visual composition.** Use the built-in ImageGen path by default and treat it as a hard visual-layer requirement for polished scientific figures. ImageGen must establish the hierarchy, visual motifs, zone balance, and overall reading order before Mermaid reconstruction begins. Request a scientific educational infographic: white or very light background, restrained multi-hue accents, thin arrows, compact modules, stable spacing, domain-relevant motifs (for example sensor/brain/device/waveform/tensor elements), and short labels. Ask the model to preserve layout even when exact text is difficult; never let it invent modules, metrics, participants, or deployment claims. Save the selected ImageGen result as a versioned raster asset such as `imagegen_draft.png` when the tool exposes a local artifact. If the tool only returns an inline preview, record that limitation and create a reviewed illustrated local asset with the same hierarchy and motifs; do not silently substitute a Mermaid wireframe.
5. **Audit and iterate once per defect.** Inspect the ImageGen asset for semantic errors, text corruption, overlap, unreadable density, missing scientific motifs, and misleading arrows. Make targeted revisions rather than regenerating an unconstrained variant. If the ImageGen result cannot be saved locally, do not present a Mermaid render as the visual replacement without explicitly labelling it as a schematic fallback.
6. **Rebuild deterministically in Mermaid.** Re-express the same structure with named subgraphs, short labels, explicit parallel paths, and a small number of cross-zone edges. Use a central "synchronized data/runtime streams" node when direct cross-links would destroy layout. The Mermaid source is authoritative for wording and claim boundaries.
7. **Render and verify.** Render the `.mmd` to SVG and a high-resolution PNG with Mermaid CLI when available. For any SVG-to-PNG conversion, verify that the PNG was actually rewritten after the SVG (output modification time newer than input), has the expected dimensions, and is visually inspected at full resolution. If a CLI invocation produces no output or leaves an older file, treat the export as failed and rerun with a deterministic local renderer (for example the bundled `scripts/render_svg_png.mjs` helper when `sharp` is available). Check the rendered output visually and run the final claim ledger against the source. A vector preview may look wide at page scale; verify at zoom and keep the SVG for publication editing.
8. **Deliver the complete set.** Save the selected ImageGen raster (`imagegen_draft.png` or a more descriptive versioned name) when available, or a clearly labelled reviewed illustrated fallback when only an inline preview was returned; also save the `.mmd`, the rendered SVG, the Mermaid PNG preview, and a short README describing which asset is the visual composition and which is the editable source. The README showcase must embed the visual composition asset by default; the Mermaid preview is secondary and must never be presented as the visual replacement for a requested infographic. Do not overwrite prior assets without an explicit replacement request.

## Hard visual-layer contract

- **ImageGen owns visual hierarchy.** For a polished research infographic, use ImageGen (or a reviewed illustrated local fallback when the result is inline-only) to define the composition, domain motifs, emphasis, and reading order. This is not optional decoration.
- **Mermaid owns editability.** Mermaid is the semantic reconstruction for deterministic wording, arrows, and later correction. It is not the primary visual-design method and cannot be the only delivered layer when the request calls for a rich scientific figure.
- **No silent downgrade.** If ImageGen is unavailable, say so in provenance and create a local illustrated fallback with explicit scientific motifs; label it as a fallback. Never call a Mermaid-only wireframe a completed visual architecture figure.
- **Renderer parity is part of correctness.** SVG and PNG must depict the same layout. A stale raster, changed font metrics, clipped labels, or a PNG that was not actually rewritten is a delivery defect, not a cosmetic issue.

## Non-Negotiable Boundaries

- Never draw independent algorithms as a validated cascade unless the source explicitly measures that cascade.
- Never place a training-only teacher, oracle, or ablation branch inside the deployed runtime chain unless it is actually deployed.
- Do not turn software-in-the-loop replay, simulation, screenshots, or session feasibility evidence into a new online algorithm result.
- Keep recorded channels distinct from fields parsed only in a runtime feedback thread.
- Do not invent latency, confirmation rate, participant count, physical actuator levels, or statistical claims to make the diagram look complete.
- For AI-generated text, treat OCR-like labels as provisional. Correct them in Mermaid or another editable source before publication.
- A Mermaid-only diagram is a structural fallback, not a completed visual architecture figure, when the request calls for a polished research infographic with icons, waveforms, brain/device motifs, or other generated artwork.
- Prefer short, literal labels. Put explanatory detail in the caption or accompanying notes, not inside every box.
- Apply data minimization to generation prompts: never paste a full manuscript, source file, raw dataset, subject identifier, local path, email, unpublished table, or private device log into ImageGen. Send only the smallest set of abstract labels and relationships needed to compose the figure.
- If a figure requires sensitive content that cannot be abstracted, keep the workflow local and deterministic (for example Mermaid/SVG) or obtain explicit approval before transmitting it to an external generation service.
- If the user forbids cloning a reference repository, read only the necessary public guidance in a browser and do not pull the repository locally.

## References

- Read [references/workflow.md](references/workflow.md) when creating a new figure or when the visual brief, prompt, Mermaid structure, or audit needs a reusable template.
- Read [references/claim-audit.md](references/claim-audit.md) when the figure mixes offline methods, online deployment, replay/simulation, and hardware evidence, or when the source contains known legacy/locked-result conflicts.
