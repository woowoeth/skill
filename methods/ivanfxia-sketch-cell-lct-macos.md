---
name: cell-lct-macos
description: Create or import editable scientific SVG figures into the user's currently open Adobe Illustrator document on macOS. Use for scientific diagrams, graphical abstracts, mechanism figures, reference-image vectorization, and appending vector artwork without replacing existing content. Requires macOS and Adobe Illustrator; do not use on Windows.
---

# Cell LCT macOS

Produce a true-vector SVG, validate it, then append it to the document the user already has open in Adobe Illustrator. Preserve existing artwork.

## Route the request

- For an existing SVG, validate and import it directly.
- For a raster reference, preserve the original, record visible text, remove text semantically, vectorize the cleaned image, then restore live SVG `<text>` before import.
- For a text-only request, first create a flat scientific illustration reference, then use the same vector workflow.

Read [references/workflow.md](references/workflow.md) for raster reconstruction. Read [references/macos-illustrator.md](references/macos-illustrator.md) before controlling Illustrator.

## Safety and credentials

- Never launch, quit, focus, resize, or rearrange Illustrator. Ask the user to open Illustrator and the target document.
- Never delete, hide, rename, move, or replace existing Illustrator objects.
- Store the Xiaomiao API key only in macOS Keychain via `scripts/keychain_api_key.py`; never put it in a command, file, log, screenshot, or chat.
- Before any image upload, determine the expected credit cost. If it exceeds 1 credit, ask the user and wait for explicit approval.
- Treat network upload and Illustrator mutation as separate authorization boundaries.

## Execution

1. Allocate a fresh job directory and retain the untouched input.
2. Build one final SVG containing true vector geometry and live text.
3. Run `python3 scripts/validate_svg.py FINAL.svg`.
4. Run `python3 scripts/import_to_illustrator.py FINAL.svg --dry-run`.
5. After the user has Illustrator and the target document open, run `python3 scripts/import_to_illustrator.py FINAL.svg --output-ai OUTPUT.ai --output-png OUTPUT.png`.
6. Visually inspect the result in Illustrator before reporting success.

The importer adds one named group above existing artwork, fits it within the active artboard, saves an AI copy, and exports one PNG. On failure it removes only the newly created group.

## Completion gate

Do not report completion until the SVG has no raster image nodes or unsafe external references, visible text remains editable, Illustrator imported the group successfully, existing content remains unchanged, and the requested outputs exist.

Report concise output paths and any compatibility limitation. Do not claim raster-to-vector conversion succeeded when only a raster wrapper was produced.
