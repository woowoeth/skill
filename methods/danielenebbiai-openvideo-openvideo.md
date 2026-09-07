---
name: openvideo
description: Orchestrate AI video editing across local media analysis, narrative cuts, silence removal, multivideo, authored Remotion visuals, preview, and rendering.
metadata:
  requires: remotion-best-practices
---

# OpenVideo

Orchestrate existing tools and skills. Do not duplicate Remotion guidance or invent substitute skills.
## Runtime

Do not require the user to clone this repository. Before the first OpenVideo command, run this skill's bundled `scripts/bootstrap.mjs`. Use the `runtime` path from its JSON output as the working directory for all OpenVideo commands. The bootstrap reuses its persistent installation on later runs and keeps project media outside the agent plugin directory.

## Required dependency

Before any Remotion composition, visual, animation, caption, media integration, Studio, or render task, load the installed `remotion-best-practices` skill and follow the official reference it routes to. If unavailable, stop and install it with:

```bash
npx skills add remotion-dev/skills --skill remotion-best-practices --yes
```

## Route the request

- Import, metadata, transcript, silence and frame analysis: [Import and analysis](references/import-analysis.md)
- Narrative trimming and silence removal: [Cuts and silences](references/cuts-and-silences.md)
- Multiple cameras, source video and B-roll: [Multivideo](references/multivideo.md)
- Diagrams, explainers and motion graphics: [Authored visuals](references/visual-generation.md)
- Validation, Remotion Studio and export: [Preview and render](references/preview-render.md)

Load only the references needed for the request.

## End-to-end workflow

1. Import every source without modifying originals.
2. Analyze every imported video.
3. Build the narrative cut from exact transcript timestamps.
4. Use secondary media intentionally as camera cuts or B-roll.
5. Unless the user requests cuts only, select up to three ideas that benefit from authored visual explanation.
6. Author every visual from the scene's meaning with `remotion-best-practices` and OpenVideo's primitive grammar. Never reuse preset geometry, exemplar structure, or another scene's choreography; integrate through the existing scene commands.
7. Validate and inspect the actual result in the synchronized Remotion Studio preview.
8. Stop for user review. Apply requested revisions in the same preview; do not render during iteration.
9. Render only after the user explicitly approves the video and asks for export.

Never describe imported footage, captions, or stock overlays as generated Remotion visuals.
