---
name: design-child-reading-adventures
description: Verify supplied books and editions, then turn grounded contents into age-appropriate, child-led reading-play ideas, structured plans, or complete reading-adventure handbooks at the depth requested. Use when a user asks for children's reading methods, book-based projects, activity cards, reading challenges, journals, passports, structured reading plans, or printable/digital reading handbooks, especially when accuracy, fun, independent completion, and recordable outputs matter.
---

# Design Child Reading Adventures

Protect reading pleasure and the child's ownership. Treat adult participation as optional scaffolding, not the engine of the experience.

## Resolve constraints in priority order

Apply constraints in this order when they conflict:

1. physical safety, privacy, lawful access, and copyright;
2. content grounding and no invented book details;
3. explicit user constraints and the selected output mode;
4. child agency and independent completion;
5. protected reading time and text-connected activity design;
6. layout, variety, ratio, and visual enhancements.

Never override a child's stated preference solely to satisfy a lower-priority quota. Explain any justified exception in the adult-facing audit.

## Select the smallest sufficient output mode

Choose one mode from the request; do not ask a question only to choose a mode.

- `ideas`: Use for a few methods, activities, prompts, or cards. Return a bounded set of ideas, not a complete route or handbook.
- `plan`: Use for a reading route, cadence, list diagnosis, or structured program. Return the adult-facing reading adventure plan.
- `full`: Use for a complete handbook, passport, challenge map, printable/digital artifact, or an explicit request for both deliverables. Return the adult-facing plan and child-facing handbook.

When the request is ambiguous, choose the smaller mode that satisfies it and mention that it can be expanded.

## Scale the parent-set intake to the mode

Use supplied context first.

For `ideas`, collect only missing information that would materially change the ideas:

- age or grade;
- current independent-reading level and preferred format;
- one or two expected effects.

For an individualized `plan` or `full` result, also require:

- exact title, author/translator, edition, abridged/full status, and identifying material such as ISBN, contents, copyright page, or relevant text;
- available weeks and session length;
- requested inline, Markdown, DOCX, printable, or digital format.

Invite, but do not require, the child's interests, dislikes, preferred creation methods, accessibility needs, and topics to avoid.

When a compact intake question includes expected effects, preferred activities, or boundaries to avoid, add a few neutral example directions plus an explicit `不确定／暂无限制` option. Present examples as non-exhaustive prompts, not recommendations or a checklist. Distinguish useful design directions:

- effects: reading interest/autonomy, story understanding/reasoning, sustained reading, language, knowledge connections, or expression/creation;
- activities: arranging/building, choosing/deduction, drawing/mapping, movement/role-play, sound/telling, hands-on trials, or thinking without leaving a trace;
- avoid: story themes, long writing/performance/recording/competition, or material/sensory/accessibility boundaries.

Ask only for boundaries relevant to the reading experience. Do not infer a preference from age, grade, gender, or the adult's goal.

If age/grade, independent-reading level, or expected effects are critically missing, ask one compact intake question using `assets/parent-intake-card.md`. Offer a clearly labeled provisional framework when useful, but do not call it individualized. Never require adult grading or continuous performance reports.

Translate expected effects into observable opportunities, not promises or quotas. Let the adult set destination and safety boundaries; let the child choose route, task, medium, pace, stopping point, and whether to share.

## Pass the content-grounding gate

Read `references/content-grounding.md` before designing book-specific activities. Verify the exact work and edition whenever the user has not supplied sufficient text or excerpts. Use lawful, reliable access routes and disclose the evidence level.

Do not treat a sales page or general synopsis as knowledge of detailed contents. Generate chapter-, character-, plot-, quotation-, or page-specific activities only from accessible text or reliable edition-specific evidence.

- Level A/B evidence: stay within the inspected text or sections.
- Level C evidence: provide only a clearly labeled provisional genre-level route, activity set, or handbook shell.
- Level D evidence: stop book-specific design, ask for identifying material, and optionally provide a generic shell.

Gate source-book page references separately from content claims:

- Write an exact source-book page number or range only after inspecting pagination from the matching edition. Never transfer pagination from another edition, translation, abridgment, format, preview, or work-level text.
- When the content is verified but matching-edition pagination is not, omit page numbers, page ranges, blank page fields, and “fill in the page” instructions. Use only a verified chapter, section, or event cue.
- When accurate content is unavailable, omit book-specific “read here” and lookup cues. Use a generic child-controlled entry such as choosing today’s section and reading until a self-chosen stopping point, or stop and request better material.
- Apply the same rule to maps, story doors, next-door navigation, adult plans, and child pages. Do not make the child resolve an edition mismatch.

Never fill gaps from model memory.

## Build the reading experience

### 1. Diagnose the reading list when the mode requires it

For `plan` and `full`, identify each title's genre/structure, likely entry points and friction, most valuable reading capability, and suitable reading mode: full, selective, cyclical, or long-form. Record its evidence level.

Sequence books by accessibility, emotional load, and cognitive demand. Add optional bridge texts only when a jump is likely to frustrate the child. Do not force every book into the same cadence.

### 2. Choose a child-owned adventure frame

Use a coherent, non-school-like identity such as explorer, detective, curator, inventor, reporter, cartographer, naturalist, or time traveler. Give each book a distinct role. Avoid reward systems based on pages, speed, perfect answers, streaks, or adult approval.

### 3. Design activities from the text outward

Read `references/activity-library.md`. Label every activity `core` or `optional`, then include:

1. a child-facing title and invitation;
2. one grounded textual anchor or reading move;
3. steps understandable without adult explanation;
4. estimated time and safe materials, plus a no-material or low-risk option when useful;
5. one optional trace: mark, card, map, audio, object, note, photo, model, or decision;
6. an optional extension;
7. a stop rule.

Prefer 5-20 minute activities. Allow `just read today` as a complete choice. Make adult discussion optional.

Pass a text-dependence gate for every core activity:

- Name one input the child notices or chooses from the inspected text after a protected reading chunk: a detail, obstacle, decision, relationship, rule, or causal pattern.
- State how that input materially changes the play's route, rule, available choice, or consequence. A title, character name, illustration theme, or genre decoration does not count.
- Apply the book-removal test: if the book were removed or replaced by an unrelated story and the activity could continue essentially unchanged, reject or rebuild it.
- Treat mazes, coloring, matching, building, movement, collecting, and similar mechanics as wrappers. Their playable obstacles, choices, rules, or consequences must depend on verified story content, not merely use story labels.
- Keep this non-graded and open-ended. Ask the child to carry something they noticed into play, not to supply an adult's one correct answer.

When only Level C evidence is available, do not invent the input. Let the child choose something from the section they just read and make that chosen element alter the play; when accurate content is unavailable, keep the activity generic and child-controlled.

Default to one open-play invitation rather than several tightly specified school tasks. Use a charged situation, one or two text-grounded constraints, at least three child-controlled dimensions, optional idea sparks, and a clear stop condition. Keep only the textual anchor and safety/stop condition mandatory.

Count an activity as open only when the child controls at least three meaningful dimensions whose alternatives would change the process or outcome. Color, name, decoration, or the wording of an otherwise fixed answer is cosmetic and does not count. At least one consequential dimension—goal, rule, or outcome—must be changeable, abandonable, or allowed to remain unresolved.

Use an open-play control budget:

- Do not make goal, materials, method, order, rules, and end state mandatory together. Beyond the text anchor and necessary safety／stop boundary, present everything as a possibility the child may replace, reorder, combine, or ignore.
- Write starting moves as invitations, not a required sequence or hidden success path. A late “change one rule” does not make an otherwise predetermined recipe open.
- Show explicit permission to remix, switch medium, stop, refuse an extension, and leave no trace. `Just read` remains a complete outcome.
- In the adult audit, name the open dimensions and identify which goal, rule, or outcome remains under child control; do not infer openness from playful wording.

Give non-obvious play a teaser, curiosity hook, optional noticing secret, safe materials or no-material version, two to four starting moves, a tiny non-prescriptive example, and a visible handoff of control. A child should make the first physical or imaginative move within 90 seconds.

### 3a. Protect varied play rhythm in a full handbook

For a child-facing handbook with four or more core activities, make a parent-only play-rhythm audit before laying out the child pages. For every core activity, name its **primary interaction grammar**: the child’s central decision loop, such as allocating under scarcity, inferring from clues, choosing a route with consequences, building and testing, performing a role response, revising a world rule, encoding with sound, comparing evidence, or transforming a constraint.

Do not count a changed title, story detail, prop, visual layout, output medium, trace, or decorative theme as a new grammar unless it changes what the child actually decides, tests, or does. A sequence of renamed “notice something, then make or arrange an object” activities is one repeated grammar.

- With `n >= 4`, do not place the same primary grammar in adjacent core activities; use each grammar at most twice and include at least four primary grammars.
- With `n >= 8`, include at least six primary grammars.
- If a child explicitly prefers a recurring medium or mechanic, preserve that preference but vary the underlying decision loop where possible; record the justified exception in the adult audit rather than pretending it is diverse.

Keep every grammar text-dependent, non-graded, and compatible with child control. Do not expose this audit arithmetic on child pages.

### 4. Calculate quantitative gates consistently

Let `n` be the number of activities labeled `core`; exclude optional activities from every denominator.

- For `at least p%`, require `ceil(p × n)` qualifying activities.
- For `no more than p%`, allow `floor(p × n)`.
- For `fewer than half`, allow `ceil(n / 2) - 1`.
- Require at least `ceil(0.5 × n)` core activities with genuinely unpredictable process and outcome.
- Require at least `ceil(0.7 × n)` core activities labeled `🟢 自主完成`.
- For ages 6-9 or an explicitly playful handbook, require at least `ceil(0.6 × n)` toy-like core activities and allow at most `floor(0.25 × n)` fixed-organizer core activities.
- Require four mechanics only when `n >= 4`; when `n < 4`, give every core activity a distinct mechanic.
- Do not report a percentage when `n = 0`; mark it not applicable.

For a playful handbook, keep writing, drawing, reporting, summarizing, and fixed organizers combined below half of core activities. Preserve the child's preferred medium when it conflicts with this lower-priority ratio and disclose the exception rather than misreporting compliance.

Show counts only in the adult-facing audit, never as compliance arithmetic on child pages.

### 5. Turn each full-handbook unit into one playable packet

Use the choose-read-play-trace-bridge-next loop:

1. **Choose** a text, stopping point, or story door.
2. **Read** from an exact grounded entry and protect uninterrupted reading.
3. **Play** with immediately adjacent text-connected actions.
4. **Leave a trace** only if the child wants one.
5. **Use a bridge** to reread, check one word, skip, switch, pause, or request help.
6. **Choose next** by named story doors, page doors only when matching-edition pagination is verified, an any-story door, or stopping.

Use a standard two-page packet:

- Page A: invitation, reading entry, play start, bridge, and named next doors.
- Page B: creation/play surface and a small next-door reminder.

Add an optional Page C only when extended creation genuinely needs more space. Keep the full loop and navigation complete on Pages A-B; Page C must never be required to continue.

Place a grounded `Start now` adventure immediately after the cover. Make it playable within three minutes and dependent on no prerequisite rules page or distant card deck.

When using a map, make it the contents, navigation, and progress surface. Repeat the same location name, number, icon, and color on each packet. Prefer story doors and picture-book scenes over taxonomies, dashboards, card grids, and adult-looking tables.

### 6. Enforce independence, safety, and light learning support

Label every activity:

- `🟢 自主完成`: child-readable and independently completable;
- `🔵 工具可选`: audiobook, dictionary, map, timer, camera, or AI is optional;
- `🟡 同伴可选`: solo completion remains possible;
- `🟠 求助卡`: adult help is limited to difficult context, accessibility, physical safety, or material preparation.

Do not count an activity as autonomous when it depends on adult preparation or safety intervention. Convert adult questioning, checking, praise, printing, or scheduling into optional help, a child-readable prompt, or a self-check.

Read `references/safety-and-tools.md` whenever an activity uses loose parts, string, movement, camera/audio, online sharing, or AI. Keep public sharing and child identifying data out of core activities.

Use `references/design-principles.md` for prediction, retrieval, spacing, connection-making, multimodal representation, chunking, metacognition, and appropriate challenge. Preserve uninterrupted reading and rereading. Never promise guaranteed comprehension, intelligence, or retention, and never grade emotional reactions.

## Deliver the selected mode

### `ideas`

Return:

1. the assumed/provided age, level, effect, and content evidence level;
2. the bounded number of requested activities;
3. a short evidence or safety limitation;
4. what additional material would unlock more specific design, if relevant.

Do not add a full diagnosis, route, handbook, or compliance table unless requested.

### `plan`

Return:

1. design brief;
2. content basis and evidence limitations;
3. compact reading-list diagnosis;
4. route and cadence;
5. purposeful core and optional activities;
6. independence and ratio audit with counts;
7. adjustment rules for difficulty, emotional load, and lost interest.

### `full`

Return two coordinated but separate deliverables:

1. an adult-facing plan adapted from `assets/parent-reading-plan-template.md`;
2. a child-only handbook adapted from `assets/reading-adventure-handbook-template.md`.

When the user requests files, create two separately named editable artifacts by default; combine them only when the user explicitly asks. If the response must remain inline, use two clearly separated top-level sections and never interleave adult notes with child pages.

Keep evidence levels, diagnosis, cadence, safety rationale, adjustment rules, and audit counts in the adult plan. Keep all adult implementation notes and compliance arithmetic out of the child handbook.

Design the child handbook as a playable picturebook world, not an adult plan restyled with brighter colors. Use one coherent illustrated setting, a recurring guide or motif when appropriate, scene-based spreads, speech bubbles or short character lines, large child-readable type, generous interaction space, and story-world navigation such as maps, doors, stamps, collections, or constellations. Make every illustration serve story, choice, play, or navigation; decoration alone does not satisfy the visual goal. “Cute” and “fun” must remain age-respectful, grounded, editable, accessible, and collision-free.

Write to the child in short, warm, non-patronizing language. Include a cover/mission, immediate `Start now`, integrated map, self-contained picturebook spreads, optional traces, artifact gallery/index, preference-based reflection, and reusable blank pages/tool cards only at the end.

Do not include parent signatures, grades, rankings, compulsory summaries, streak pressure, or speed targets.

When the user requests files, create editable artifacts. For DOCX/PDF, use the applicable document skill and visually verify every rendered page. Confirm readable contrast, non-color navigation cues, live/editable text where possible, clear text-safe zones, and no overlap among illustrations, instructions, stamps, and navigation.

## Run the delivery gate

Before delivery, reject or repair the output if it:

- exceeds the selected output mode;
- invents book or edition details;
- lets making/writing outweigh planned reading;
- disguises ordinary homework with a playful title;
- hides adult grading, scheduling, printing, or public sharing inside a core activity;
- contains a core game that would remain essentially unchanged if the book were removed or swapped for an unrelated story;
- counts cosmetic choices or a final token choice as open while goal, method, rules, and result remain predetermined;
- violates the two-page packet base rule or makes optional Page C necessary for navigation;
- miscalculates core-activity ratios;
- omits a safe/private alternative where the safety reference requires one.

Confirm that the child can begin, choose, stop, switch, and understand the next move without adult performance management.
