---
name: minimax-h3-single-dancer-prompt
description: After a dancer image is attached, present all dance, duration, performance, camera, audio, and ending options in one Chinese selection message, then convert one comma-separated reply into a complete English MiniMax H3 single-dancer prompt. Use for one visible dancer; do not use for group choreography or generating the video itself.
---

# MiniMax H3 Single-Dancer Prompt

Create one production-ready H3 prompt for exactly one visible dancer through a single Chinese selection form. Preserve the user's requested duration, dance genre, appearance, setting, camera style, audio behavior, dialogue or lyrics, and reference relationships. Do not invent details that conflict with supplied media.

Before composing, read [references/guided-selection-options.md](references/guided-selection-options.md) in full. Its image gate, six-field order, complete option lists, comma-separated reply grammar, validation, and repair behavior are mandatory.

## Workflow

1. Require and inspect an accessible reference image before beginning the wizard. If it is missing, ask the user to upload it and stop. Treat any additionally attached audio, keyframe, or reference dance video as another reference input.
2. Confirm that the target contains one visible dancer. A singer or off-screen voice may exist, but do not introduce backup dancers, crowds performing choreography, reflections that act independently, clones, or duplicated bodies.
3. Show all six complete option groups from [references/guided-selection-options.md](references/guided-selection-options.md) in one message and ask for one comma-separated reply in the exact order `dance, duration, tone, camera, audio, ending`. Do not generate a provisional prompt while any required value remains unresolved.
4. Parse and validate all six values. If one or more are missing or invalid, retain valid values and request only the missing or invalid fields in one compact repair message. After all six are resolved, proceed immediately without an extra confirmation turn or parameter recap.
5. Select the H3 mode and exact output structure using [references/output-contract.md](references/output-contract.md).
6. Read [references/choreography.md](references/choreography.md) and apply the selected dance direction as the primary movement language.
7. Read [references/cinematography-and-music.md](references/cinematography-and-music.md) and translate the selected camera and audio choices into the prompt.
8. Write the full prompt in English. Keep dialogue, lyrics, and visible text verbatim in their original language. Match every timestamp and final hold to the selected duration.
9. Validate against the output-contract checklist, then return only the prompt as plain text: no greeting, explanation, selection recap, self-check, or Markdown fence.

## Interaction Boundary

- The single complete selection message is the normal pre-generation interaction unless an attachment is missing or a submitted value is invalid.
- Present all six option groups together in the defined order. Do not spread them across multiple turns.
- Accept a key, its Chinese label, an option number, or a user-written custom value. `auto` means infer only that dimension from the actual image and supplied brief.
- If the user supplied valid choices with the image, do not show redundant option groups; request only unresolved fields or generate immediately when all six are present.
- Never make the user repeat valid values. If the user changes an answer, replace only that field.

## Creative Invariants

- Keep the dancer's identity, anatomy, clothing, and accessories stable unless the user explicitly requests a change. Maintain one coherent body with natural limbs and no identity drift.
- Build a readable routine with roughly 5–10 core movements when duration allows. Fully articulate extensions, levels, weight shifts, landings, and poses; graceful does not mean timid.
- Write transitions as `previous landing -> momentum-bearing transition -> next initiation`. Do not reset the body between moves.
- Limit spins to 1–2 purposeful rotations unless the dance genre or user explicitly requires more. Do not default every climax to a split or every ending to a pull-out.
- Camera motion supports action readability. Favor close and medium framings for expression and detail, but use full-body framing whenever complete lines, jumps, floorwork, kicks, backbends, or wide travel must remain visible.
- Never claim exact BPM, beat, drop, chorus, instrumentation, melody, or lyric timing unless it was supplied or can actually be inspected. With unreadable audio, use relative anchors such as `when the next phrase begins`.
- Supplied performance audio is copied 1:1 unless the user explicitly requests editing. Visual synchronization must never alter melody, rhythm, lyrics, instrumentation, timing, or audio layers.
- Outside the wizard, ask only when a missing attachment or invalid answer prevents progress. Never silently substitute a different option.
