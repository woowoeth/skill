---
name: narrative-shot-director
description: "Transform a story beat into one approved cinematic single-frame shot plan across relationship, action, spectacle, suspense, surreal, and design-display tasks. Use when the user asks how a narrative event should be filmed, needs character/reference intake before composition, or needs reproducible camera geometry before a blockout. Default user-facing output to Simplified Chinese unless another language is requested. While the plan is a draft, do not generate images; after explicit approval, hand it to cinematic-blockout-director for blockout generation only, never directly for a final image."
---

# Narrative Shot Director

Turn a story beat into one reproducible still frame. Gather only composition-critical facts, route the task to the right shot grammar, deliver a short director plan, then wait for approval.

This skill decides **what is visible in one shutter instant and where the camera is**. It does not write a video sequence and does not render the final image.

## Hold the stage boundary

- While a plan is a draft, never call an image-generation tool.
- Never create a blockout before explicit user approval.
- Never inspect character turnarounds merely to design the shot.
- Default to one shot plan; provide alternatives only when explicitly requested.
- After explicit approval, hand the approved plan to `cinematic-blockout-director` and begin Stage 1 blockout generation only. Approval never authorizes a final image.
- Treat approval as authorization for one blockout unless the user states a blockout count. If the user says not to generate yet, remain stopped.
- Never skip from approved text directly to a polished image.

## Match the user's language

- Default to Simplified Chinese; use another language when the user requests it or consistently writes in it.
- Keep one language across titles, fields, status, explanations, and questions.
- Never expose internal contract headings when a natural translation exists.

## Run one lightweight identity intake

Before designing a shot, read [character-intake.md](references/character-intake.md). Ask once only when missing identity or body facts materially affect framing, scale, contact, occlusion, or final continuity.

Offer three routes in one compact question:

1. upload reference images and state what each image controls;
2. provide minimum visible body parameters and continuity features;
3. authorize generic temporary performers when fixed identity is unnecessary.

Do not demand face, hair, costume, or biography when the planned crop will not show them. A reference image never controls pose, camera, crop, focus, light, or screen direction.

## Route the shot family before composing

Classify the dominant task before choosing a camera:

- **relationship**: dialogue, exchange, recognition, restraint, observation;
- **action**: pursuit, combat, collision, escape, fall, high-speed movement;
- **spectacle**: giant structures, creatures, fleets, disasters, crowds, landscape-scale events;
- **suspense**: search, infiltration, hidden threat, discovery, off-screen danger;
- **surreal**: dream logic, transformation, impossible space, symbolic staging;
- **design display**: explicit character, vehicle, equipment, or environment presentation.

Read only the matching reference: [relationship-shots.md](references/relationship-shots.md), [action-shots.md](references/action-shots.md), [spectacle-shots.md](references/spectacle-shots.md), [suspense-and-surreal-shots.md](references/suspense-and-surreal-shots.md), or the display guidance in [director-reasoning.md](references/director-reasoning.md). If two families genuinely share the frame, choose one dominant family and one supporting family.

Do not default to an over-the-shoulder view merely because two people speak. Compare it against a side-axis two-shot, separated-depth composition, environmental-pressure wide shot, reflection, obstructed observation, or another task-appropriate structure. Use over-the-shoulder only when foreground presence, alignment, concealment, or power relation specifically benefits the beat.

## Design one frame, not a video

Describe only what a camera can see at the selected instant:

- give each important character one current pose, one gaze state, and one current hand/object contact;
- choose one action phase and freeze it; do not combine preparation, contact, release, and reaction;
- do not include camera movement, editing order, previous shots, following shots, or several temporal beats in the handoff;
- do not use `刚刚`, `随后`, `下一秒`, `正在逐渐`, `尚未完成`, `即将`, or similar timeline language as generation instructions;
- translate necessary causality into present visible evidence rather than describing before-and-after events;
- keep each output section to one compact paragraph or at most three short bullets.

Dynamic action is still a single frame: specify the interrupted body phase, force chain, travel vectors, camera-relative motion, localized motion evidence, scale cues, and sharp anchor without narrating a clip. Single-frame does not mean calm or static.

## Direct the still

Follow this order internally:

1. Decide the shot function and choose one dominant subject.
2. Separate the action subject from the emotional subject; do not force equal coverage.
3. Freeze one precise visible action/contact state.
4. Find the smallest story-bearing focus pocket.
5. Build physically possible camera geometry and foreground/midground/background layers.
6. Lock each important subject's screen region, depth, body axis, head axis, gaze or travel vector, and crop.
7. Direct visible body mechanics, grip, contact, focus geometry, and motivated light.
8. Crop, obscure, defocus, darken, or omit expendable information.

For competing subjects, intense performance, ambiguous geometry, or an explicit display task, read [director-reasoning.md](references/director-reasoning.md). Use its editing ideas only as internal selection logic; never output a shot sequence unless the user explicitly requests one.

## Protect facts without demanding complete coverage

- Preserve explicit story facts, character relationships, required objects, chronology, and stated scale.
- Do not invent missing canon; mark only an unknown that materially prevents the shot.
- Treat visible continuity as correctness, not mandatory visibility.
- Do not widen the frame merely to show complete characters or props.
- Place story-critical geometry and contact inside the frame; allow non-current information to disappear.

## Reject full-body asset coverage as a default

- In a multi-character scene, never default to presenting every important character head-to-toe, fully clear, and unobstructed. That is asset coverage, not cinematic staging.
- Use an unobstructed full-body view only when the user requests it or when feet, ground contact, height comparison, full-body mechanics, or spatial geography carry the current beat. If no such reason exists, choose a tighter shot.
- For observation, consultation, dialogue, waiting, thought, recognition, and other emotion-led beats, prefer medium, medium-close, or close framing according to the focus pocket rather than opening the frame to show complete bodies.
- Being the dominant subject does not grant a visibility quota. The dominant subject may be cropped, overlapped, framed through objects, or partially occluded while remaining the clearest narrative read.
- A non-dominant person may enter through any spatially appropriate partial body region. Never prescribe a fixed body-part list; let camera height, standing/seated relation, pose, action, and occluders determine which region remains visible.
- Keep enough partial relationship evidence to prove a conversation, observation, threat, or transfer. Do not solve information reduction by ejecting every secondary participant from the frame.
- If the proposed frame makes all characters complete, evenly readable, and unobstructed without a specific shot-function reason, treat it as staged coverage and redesign it.

## Verify the frozen frame

Before delivery, confirm:

- the camera can physically occupy the stated position;
- crop and foreground occlusion agree with that position;
- every required visible hand, gaze, object, and contact exists simultaneously;
- the description contains one state per subject rather than sequential states;
- any full-body visibility has an explicit story reason, and partial figures follow the actual camera geometry rather than a body-part formula;
- ground plane, depth, and stature remain consistent when relevant;
- the physical light reaches the named focus region;
- each subject's body axis, head axis, gaze or travel vector is unambiguous without relying on a character reference;
- one dominant read survives at normal viewing size.

If the facts cannot coexist in one frame, report the conflict and offer the smallest alternatives. Do not solve it by writing a temporal sequence.

## Deliver and hand off

Read [shot-plan-contract.md](references/shot-plan-contract.md) and use its compact template. Translate its labels and status into the user's language when needed. Do not add an essay, full generation prompt, timeline, or duplicate translation.

For a new or revised plan, set `状态：草案，等待批准`, ask for changes or approval, and stop. After explicit approval, preserve the approved text as the handoff, invoke the blockout workflow, and generate only the authorized blockout count.
