---
name: x-article-thumbnails
description: "Design article thumbnail concepts, generation prompts, and precise image revisions. Use for reference selection, readable workflow diagrams, visual style extraction, or coordinated title and thumbnail packaging."
---

# X Article Thumbnails

Read the article or brief. Identify the one relationship, workflow, or transformation the image should explain. The visual should give a small amount of value before the click and make deeper material approachable.

## Set the visual direction

Pinterest is an optional reference source, not a required tool. Search directions can include technical editorial diagrams, serif poster typography, or minimal workflow infographics. Use references for named properties: typography from one, palette from another, composition from another. Build an original visual for the current article; do not copy another creator's claims or identity.

A useful default is a few dominant elements, strong contrast, consistent typography, and one large diagram with short labels of roughly four or five words. The creator calls this the “Cocomelon effect”: immediate recognition through simple packaging. This is a design heuristic, not a measured claim about a platform or a rigid limit on diagram nodes.

Use the user's ratio and dimensions. A 5:2 canvas is an example preference for wide article covers, not a universal platform requirement. A request for more resolution must preserve the existing ratio and composition unless instructed otherwise.

## Generate or edit

Use the available image-generation tool for visual generation or edits. When the user requests editable SVG, author a self-contained SVG with a viewBox, readable text, accessible title/description, and no external assets or scripts. If generation is unavailable, return a complete image brief and label it as a brief.

For edits, identify both what changes and what stays. An approved diagram is an anchor, not an invitation to redesign everything. Match exact title line breaks, connector geometry, labels, and regional changes when requested. Do not silently replace a finished asset with a new concept.

If extracting a style as JSON, use [the visual brief](references/visual-brief.md). Label estimated font matches or sampled colors honestly.

## Verify

Inspect the final visual at its intended display size. Check text, labels, contrast, crop, arrows, and whether the image conveys the correct mechanism. Check actual exported dimensions separately from visual acceptance. A generated preview or export is not proof the user approved it. Fix concrete issues and deliver the full requested asset.

See [the prompt pack](references/prompts.md) for generation, style extraction, and narrowly scoped revisions.
