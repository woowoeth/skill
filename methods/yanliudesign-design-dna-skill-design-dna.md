---
name: design-dna
description: "Translate a vague visual direction, reference website URL, named product, or optional screenshot into an original, executable design language and apply it to a new web interface. Use whenever the user says make it feel like, inspired by, reference this site, match this vibe, translate this aesthetic, or wants a web UI based on a visual reference without copying its brand identity."
---

# Design DNA

Turn a lightweight reference into transferable design decisions, then implement and visually verify them. Do not require a mood board or multiple screenshots.

## Input Priority

Accept the lightest input the user already supplied:

1. A natural-language feeling or analogy
2. A named product, publication, place, or visual genre
3. A public URL
4. One or more optional screenshots

Do not ask for images when the first three inputs provide enough direction. Ask one focused question only when the target surface or primary user task is genuinely unknown and cannot be inferred.

## Translation Workflow

### 1. Separate Source From Target

Identify:

- **Source signal:** the feeling or reference being translated
- **Target job:** what the new interface must help its user do
- **Transfer boundary:** what may carry over and what must remain original

Preserve the target's usability before preserving the source's appearance. A financial dashboard inspired by an editorial magazine must still scan like a financial dashboard.

### 2. Inspect Available Evidence

For a URL, inspect the live page at desktop and mobile sizes when browser tools are available. For an image, inspect only visible evidence. For a named reference without accessible evidence, use established high-level characteristics and explicitly label uncertain inferences.

Never invent exact measurements, fonts, interaction behavior, or hidden states that cannot be observed. Express uncertain values as ranges or design intent.

### 3. Extract Design DNA

Translate evidence into 5-8 rules across the dimensions that materially affect this target:

- hierarchy and information density
- grid, alignment, and composition
- typography roles and scale relationships
- color roles and contrast strategy
- surfaces, borders, radius, and depth
- imagery and icon treatment
- interaction and motion rhythm
- responsive transformation

Every rule must be operational. Include a decision, its reason, and its implementation consequence.

Bad: "Use a clean, premium aesthetic."

Good: "Build hierarchy with type scale and whitespace rather than nested cards, because the reference feels editorial; keep major sections unframed and reserve bordered containers for interactive tools."

### 4. Remove Brand Fingerprints

Do not copy logos, proprietary illustrations, trademarked shapes, signature layouts, exact copy, or distinctive asset combinations. Do not reproduce the reference pixel-for-pixel.

Translate concrete attributes into roles:

- exact brand blue -> one restrained action accent
- proprietary typeface -> a font with the same functional contrast
- signature hero composition -> the underlying hierarchy principle
- recognizable illustration -> a new subject using a compatible visual treatment

The result should feel related in design logic but clearly belong to the target product.

### 5. Resolve Conflicts

When source and target conflict, decide in this order:

1. task completion and content legibility
2. accessibility and responsive behavior
3. target brand and domain conventions
4. transferred visual character

State only consequential compromises. Do not burden the user with routine implementation narration.

### 6. Implement

Before coding, map each Design DNA rule to a visible implementation location. Reuse the project's framework, components, tokens, and icon library. Create new abstractions only when the design language repeats enough to justify them.

Use real or representative content. Implement expected interaction states and responsive behavior, not only a static hero.

### 7. Verify Visually

When browser tools are available:

1. render the result at desktop and mobile sizes
2. capture screenshots
3. check hierarchy, overflow, text wrapping, interaction states, and brand independence
4. repair visible failures

Do not claim visual verification if screenshots were not inspected.

## Output Contract

Keep analysis concise and action-oriented.

### Design DNA

Provide 5-8 numbered rules. Each rule contains:

- **Decision**
- **Why it transfers**
- **Implementation**

### Translation Map

Use a compact table:

| Source signal | Translated rule | Applied location |
|---|---|---|

### Deliverable

Create or modify the requested web interface. If no codebase exists and the user asked only to explore a direction, create the smallest runnable artifact that demonstrates the language.

### Verification

Report:

- desktop and mobile status
- major issues repaired
- any unverified assumptions

## Quality Gate

Before finishing, confirm all five statements are true:

- The user was not forced to provide more reference material than necessary.
- The Design DNA contains observable decisions, not aesthetic adjectives.
- The target workflow remains appropriate for its domain.
- No recognizable brand fingerprint was copied.
- The implementation was visually checked when tools allowed it.