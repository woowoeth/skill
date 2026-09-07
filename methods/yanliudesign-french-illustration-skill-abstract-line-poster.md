---
name: abstract-line-poster
description: Generate original abstract hand-drawn line posters from any theme, sentence, event, object, article idea, or supplied image. Always use this skill when the user asks for 抽象线条海报、手绘线稿海报、留白活动海报、wine/coffee/party zine poster, naive editorial line art, or asks to keep this skill's paper palette, conversational typography, sparse layout, and imperfect print character. Preserve the visual system rather than any reference composition. Return both a production-ready image prompt and a generated raster image unless the user explicitly requests prompt-only.
---

# Abstract Line Poster

Turn any subject or supplied image into an original editorial poster built from:

> warm paper + loose single-line drawing + generous silence + conversational type + imperfect ink

Preserve this visual language across topics. Never trace, paraphrase, or reconstruct a reference poster.

## Default Deliverable

Create:

1. one final image-generation prompt;
2. one generated raster image from that prompt;
3. one short recipe note naming palette, layout, line treatment, type pairing, and originality changes.

Save generated files under `/Users/yanliu/Desktop/Claude skills/abstract-line-poster/` when a file path is available. Stop at prompt-only only when the user explicitly asks for it or image generation is unavailable.

## Read The Input

Extract five things before composing:

- **Subject:** the one person, object, gesture, setting, or idea that must remain recognizable.
- **Purpose:** invitation, announcement, cultural notice, menu, personal statement, editorial cover, or poetic observation.
- **Emotional verb:** gather, taste, wait, open, celebrate, wander, listen, rest, or the equivalent implied by the user.
- **Words:** exact supplied title, or one invented phrase of 2-7 words plus optional factual microcopy.
- **Image role:** main subject reference, crop reference, gesture reference, object reference, or no supplied image.

For an abstract or complex topic, translate it into one drawable gesture or object relation. Do not illustrate every point.

When an image is supplied, preserve factual identity: the person, object, pose logic, and defining attributes. Redraw it through loose contours and selective omission. Do not preserve its original crop, background arrangement, lighting, or text placement unless those facts are essential.

### Clarify Poster Copy

When the user provides only a theme or image without poster copy, ask one concise question before composing:

> 这张海报需要主标题和补充内容吗？可以直接提供文字，也可以让我自动拟定。

- If the user supplies copy, preserve the exact main title and verified factual details.
- If the user asks for title only, omit supporting copy except for non-factual visual microtext.
- If the user says no text, create a textless composition and do not invent labels.
- If the user asks the skill to decide, invent one 2-7 word title and at most one short non-factual note.
- Do not ask again when the user has already supplied a title, explicitly requested no text, or told the skill to decide everything.

## Visual Grammar

### 1. Paper And Ink

Use a warm, uncoated paper field rather than digital white.

- **Default paper:** chalk ivory `#F3EEDF`.
- **Alternate paper:** pale oat `#E9E2D1`, blush paper `#F2C7C8`, mist blue `#B9DDF0`, pale lavender `#D8C7E6`, leaf green `#16804A`, or acid chartreuse `#B8CF55`.
- Paper carries subtle fibers, faint scanner dust, and uneven ink absorption. It must remain flat and front-facing with no frame, desk, mockup, or cast shadow.
- Choose exactly one **main ink** from charcoal `#171915`, bottle green `#087243`, cobalt `#1555A5`, aubergine `#56336D`, tomato `#CF4B2F`, or dusty rose `#D66F91`.
- A second ink may appear only as a small communicative accent covering at most 12% of the printed marks. Never use more than two chromatic inks.
- Prefer pale or warm paper with a darker ink. Use saturated paper with reversed ivory ink only when the user explicitly wants a dark poster; reversal too easily becomes polished nightlife branding.

The restricted ink logic makes each poster feel screen-printed or risographed rather than digitally color-coordinated.

### Background Rhythm Across A Series

Treat the flat paper field as a pacing device, not a theme-matching color swatch:

- **quiet base, about three in five posters:** chalk ivory, pale oat, warm gray, or restrained blush; use for intimate, everyday, reflective, or text-led subjects;
- **colored paper, about one in three posters:** mist blue, pale lavender, dusty pink, or softened leaf green; use to vary the sequence and support social, seasonal, or playful subjects;
- **accent sheet, about one in ten posters:** acid chartreuse, saturated green, tomato, or another forceful field; reserve for a visual exclamation point in a series, not as the default response to energetic themes.

These ratios guide a sequence, not an individual request. For three or more related posters, include at least one quiet base and no more than one accent sheet unless the user specifies a palette.

A pure-color background must still feel like physical paper. Add only two or three restrained variations: faint edge fading, a subtle sun-bleached patch, uneven fiber density, scanner dust, or slightly inconsistent ink absorption. Keep the field visually single-color; do not introduce gradients, watercolor clouds, decorative stains, vignette lighting, or digital noise. Background variation should be noticed after the composition, never before it.

### 2. Negative Space And Grid

- Default to a vertical 3:4 canvas. Respect a user-specified ratio.
- Keep 25%-45% of the page visibly empty. Empty paper must form one or two large connected zones, not many accidental gaps.
- Use outer margins of 5%-8% of page width.
- Align most content to one loose vertical axis or a simple 2-column editorial grid.
- Keep the composition asymmetric. Place the visual center slightly above or below the geometric center.
- Build one dense cluster and one quiet counterweight. Do not distribute objects evenly.
- Let one element break the grid through a tilted baseline, drifting caption, cropped line, or oversized word.

Negative space controls pacing. It should make the drawing and title feel spoken into a quiet room, not lost on an unfinished page.

### Romantic Looseness

When the user asks for French-romantic, playful, or relaxed energy, compose by relationships rather than measurements:

- let objects orbit, interrupt, lean toward, or nearly miss one another as if they were fragments of a conversation;
- use one intimate trace of human presence such as a lipstick ring, bent cocktail pick, half-peeled citrus curl, fingertip, folded napkin edge, or unfinished handwritten aside;
- vary baselines, scale, rotation, and spacing by eye; do not specify equal columns, exact object counts, or a mechanically balanced cluster;
- allow one purposeful near-collision and one element to drift toward or beyond an edge;
- keep the mood sensual through touch, appetite, pause, and after-hours warmth, never through luxury styling or Paris clichés.

In this mode, avoid excessive percentages and numeric placement instructions in the final prompt. Relational language produces more human rhythm than diagram-like coordinates.

### 3. Line Drawing

Draw with one continuous-feeling ink voice:

- loose monoline or lightly varied pen pressure;
- simplified contour, selective internal detail, and 2-5 small hatching zones;
- imperfect joins, occasional doubled contours, and slight registration wobble;
- visible hesitation: 3-8 broken strokes, overshot corners, blunt line endings, and unequal curves; never let every path look equally smooth;
- recognizable silhouette at thumbnail size without realistic rendering;
- no polished vector geometry, smooth icon set, anime treatment, cute mascot language, or decorative watercolor fill.

Use omission as the abstraction method. Keep the gesture, silhouette, and one characteristic detail; remove incidental texture. Lines should look observed by hand, not auto-traced from a photograph.

Do not draw a complete explanatory scene when a few displaced objects can imply it. Unequal object scale, awkward gaps, and partial crops create the naive editorial energy; polished spatial consistency destroys it.

Choose one primary composition skeleton. A small secondary device may support it, but never combine several skeletons into a sampler:

- **single emblem:** one object or gesture occupies 24%-44% of the page;
- **social vignette:** 2-5 loosely connected objects or hands imply an event without drawing a full scene;
- **floating inventory:** 3-7 small objects drift along one axis with unequal gaps;
- **contour crop:** one enlarged fragment enters from one edge and stops before dominating the page;
- **type-and-line knot:** lettering and drawing share one compact central cluster;
- **near-empty specimen:** one small drawing occupies 10%-22% with unusually large silence.
- **notice spine:** one cropped person or object anchors a side while title, note, and utility copy stack along a loose vertical spine; useful when the poster must communicate several information levels;
- **object shelf:** 2-4 unrelated-scale objects sit on an implied horizontal band, each with a different amount of air and one displaced caption; useful for markets, menus, and small collections;
- **monument and side notes:** one simplified symbol rises vertically while two or three short text blocks counterweight it from different sides; useful for a single iconic object without defaulting to a centered logo;
- **perimeter orbit:** a loose scene or object family occupies the middle while words, fragments, or annotations travel around only two or three edges, leaving one edge open; useful for gatherings and celebratory abundance;
- **tabletop island:** a small oblique arrangement sits low or off-center like a remembered table, surrounded by disproportionate empty paper and distant copy; useful for intimate meals, books, or quiet events;
- **radial gathering:** hands, tools, glasses, or small objects enter from uneven edges toward an intentionally incomplete center; useful only when the theme genuinely involves shared action;
- **annotated constellation:** objects of unequal scale form 2-4 loose clusters joined by captions, punctuation, or a wandering line rather than a central hero; useful for menus, itineraries, and mixed activities;
- **diagonal action:** one pour, reach, ride, throw, or unfolding gesture crosses the page and carries the reading order; useful when motion is more important than object inventory;
- **corner-framed specimen:** two or three incomplete corner marks or cropped contours loosely hold a small subject and scattered information without forming a complete border; useful for personal notices and restrained invitations.

Composition richness comes from role changes, not object count. Give elements distinct jobs: one anchor, one counterweight, one path, one interruption, and one quiet zone. Do not make every object the same size, give every object a label, or fill every open area.

### 4. Typography

Use two voices, with an optional third only for tiny metadata.

- **Human voice:** dry-brush, felt-tip, wax-pencil, or naive handwritten lettering. Use for one short emotional phrase, annotation, or irregular display title.
- **Editorial voice:** narrow grotesk, sturdy condensed sans, or high-contrast serif. Use for the main title when clarity matters.
- **Utility voice:** optional tiny monospaced or typewriter text for date, place, ingredients, credits, or one factual line.

Choose lettering by stroke behavior rather than by naming or imitating a reference font. Select one display behavior, one contrasting support behavior, and optionally one utility behavior:

- **swollen marker block:** heavy uppercase forms with pinched counters, unequal widths, soft corners, and abrupt blunt terminals; useful for urgent or declarative titles;
- **soft blob display:** rounded, inflated letters with melting joins, irregular bowls, and a friendly low center of gravity; useful for playful social titles;
- **tall pinched condensed:** narrow uppercase letters with uneven height, slightly crooked verticals, and compressed spacing; useful for names, lists, or an editorial-led title;
- **naive separated capitals:** simple felt-tip uppercase letters that do not share a baseline, with awkward gaps and inconsistent crossbars; useful for informal event titles;
- **fast slanted brush:** connected or nearly connected words with changing pressure, dry skips, long entry strokes, and overshooting exits; useful for appetite, motion, and celebratory phrases;
- **rounded casual lowercase:** thick, childlike lowercase forms with bouncing x-height, open counters, and deliberately uncertain spacing; useful for menus and object labels;
- **thin private handwriting:** fine monoline writing with stretched ascenders, loose loops, drifting baselines, and unfinished terminals; useful for intimate notes or one conversational sentence;
- **scratched utility note:** small compressed capitals or mixed-case pen writing with hurried corrections, crowded lines, and uneven word spacing; useful for factual microcopy and marginal annotations.

Do not use this as a catalog to display every behavior. One poster normally uses two strongly contrasting behaviors; a third appears only in small metadata. Contrast should come from weight, width, rhythm, and scale, not from adding more colors.

Choose one hierarchy:

- **hand-led:** large irregular hand title + tiny editorial details;
- **editorial-led:** strong serif/condensed title + one hand note;
- **split voice:** two phrases of clearly different scale balance the drawing;
- **quiet notice:** medium title + compact factual block + almost no extra text.

Rules:

- Keep the main display wording to 2-7 words.
- Make the largest type 4-9 times the microcopy size.
- Use natural or zero letter spacing; never use extreme luxury tracking.
- Break typographic regularity intentionally: vary at least three of baseline, character scale, width, rotation, spacing, pressure, or stroke completion across the display phrase. Do not place every letter or character inside an equal invisible box.
- Let one display word compress while another breathes; allow one near-collision and one conspicuous gap. Do not distribute irregularity evenly, because uniform wobble looks synthetic.
- Allow one title to stack irregularly, follow a contour, or overlap a line drawing by no more than 8% of its area.
- Make the title participate in the drawing: one letter or word must touch, interrupt, frame, or visually replace part of an illustrated contour. A detached headline above a separate illustration fails the style.
- For English display type, exploit unequal letter width, mixed scale, open spacing, wandering baselines, elongated strokes, and letters that frame or merge with drawn contours. Preserve word recognition rather than font consistency.
- For Chinese display type, preserve the recognition skeleton of each character but break the square-box rhythm: use mixed character scale, staggered baselines, selective compression or stretching, dry gaps, shared strokes, and character-to-object contact. Let one character dominate and let others orbit, stack, or travel along a contour. Do not distort every character equally.
- When exact Chinese wording and extreme freedom conflict, keep one or two key display characters expressive and move the remaining copy into a clearer editorial or utility voice.
- Keep all critical words readable. Treat secondary microtext as texture only when exact wording is unimportant.
- Never invent logos, sponsors, URLs, QR codes, addresses, prices, or event facts.

Typography should feel like a person communicating, not a brand launching a campaign.

### 5. Communication Tone

Write like an independent cafe notice, neighborhood wine night, small cultural gathering, or personal zine:

- direct, warm, lightly witty, and socially inviting;
- concrete nouns and active verbs;
- one human observation is better than an inspirational claim;
- factual microcopy stays plain and compact;
- no sales pressure, brand manifesto, productivity slogan, luxury language, or generic motivational quote.

Use the user's language. Do not add random French, Italian, Japanese, or Korean words merely to signal taste.

## Composition Decision Flow

Choose the layout from the content:

1. Is there one strong supplied person, hand gesture, or object?
   - Use **single emblem**, **contour crop**, **notice spine**, or **monument and side notes**.
2. Is it an event involving food, drink, music, or gathering?
   - Use **perimeter orbit**, **object shelf**, **annotated constellation**, or **type-and-line knot**. Use **social vignette** or **radial gathering** only when a specific shared action is central; generic symmetrical hands holding objects look like stock event graphics.
3. Is the phrase itself the main idea?
   - Use **type-and-line knot** with an editorial-led or hand-led hierarchy.
4. Is the mood intimate, reflective, or poetic?
   - Use **near-empty specimen**, **tabletop island**, or **corner-framed specimen**.
5. Is the emotional verb physically directional, such as pour, ride, reach, unwrap, or dance?
   - Use **diagonal action** and let the gesture determine the reading order.
6. Does the content contain several categories, menu items, stops, or activities?
   - Use **annotated constellation** or **object shelf**, with one category noticeably quieter than the others.
7. Otherwise use **single emblem** or **floating inventory** and let one hand annotation provide the emotional cue.

For repeated requests, rotate the primary skeleton, title path, empty-space location, crop direction, and information topology. Changing only color, object substitutions, or ink texture does not count as a new composition. Do not use **floating inventory** or a centered hero for more than one of three consecutive posters unless the user explicitly asks for continuity.

## Palette Decision Flow

Choose one recipe, then adapt only when the subject requires it:

- **Everyday warmth:** ivory paper + bottle green ink + tiny tomato accent.
- **Night gathering:** blush paper + charcoal ink + tiny cobalt accent.
- **Fresh market:** leaf green paper + ivory ink + tiny charcoal metadata.
- **Playful notice:** mist blue paper + cobalt ink + tiny dusty rose accent.
- **Urgent cultural poster:** acid chartreuse paper + charcoal ink, no secondary ink.
- **Quiet editorial:** pale oat paper + dusty rose or cobalt ink, no secondary ink.
- **Purple gathering:** pale lavender paper + aubergine ink + tiny tomato accent. Keep purple in the paper-and-ink relationship rather than using a dark purple flood with white outlines.
- **Romantic violet:** faded lilac paper + aubergine ink + lipstick vermilion, with optional warm ivory showing only through unprinted paper. Use for playful, intimate, French-romantic gatherings.

Do not map mood to stereotypical color automatically. A wine theme does not require burgundy; a botanical theme does not require green.

## Reference Image Firewall

Treat references as evidence for a visual grammar, never as a composition to trace.

Before generation, change at least five of these from every style reference:

- subject or gesture;
- crop and viewpoint;
- drawing structure;
- object count;
- title wording and line breaks;
- title location;
- empty-space location;
- grid axis;
- paper/ink pairing;
- type hierarchy;
- metadata treatment;
- aspect ratio;
- grid-breaking device.

Never reproduce visible slogans, logos, signatures, illustrations, borders, exact object arrangements, distinctive hand-letter shapes, or publication marks. Never mention a living artist, studio, or source poster in the final generation prompt. Describe the independent visual properties instead.

When the user supplies their own photograph as content, preserve the subject's identity but reconstruct the poster around it from a different crop, abstraction level, layout family, and text path.

## Prompt Compiler

Write the final image prompt as five compact paragraphs in this order:

1. **Canvas:** aspect ratio, exact paper color, exact ink recipe, flat physical paper, and empty-space percentage.
2. **Original composition:** name one primary skeleton and describe the anchor, counterweight, reading path, interruption, quiet zone, crop direction, and one grid break. Describe relationships rather than a list of evenly placed objects.
3. **Subject drawing:** recognizable subject, preserved facts from a supplied image, omitted details, contour behavior, and hatching zones.
4. **Typography and words:** hierarchy, exact short title, one named display stroke behavior, one contrasting support behavior, at least three axes of irregularity, placement, overlap behavior, and any verified microcopy. Describe visible letter behavior rather than a font name.
5. **Material and anti-style:** ink wobble, fibers, scan character, emotional temperature, originality changes, and hard avoids.

Describe only details that become pixels. Do not include analysis, hex alternatives, style-reference names, or this skill's name in the final prompt.

## Generation Workflow

1. Parse the subject, purpose, emotional verb, words, and image role.
2. Choose one drawing structure, one type hierarchy, and one palette recipe through the decision flows.
3. Draft the exact 2-7 word display phrase. Reuse user wording when supplied.
4. Compile the five-paragraph image prompt.
5. Generate a raster image with the available image-generation tool. Use a supplied image as a content reference, not a layout reference.
6. Inspect once at full size and once at thumbnail size.
7. Regenerate once when a quality gate fails. Tighten only the failed constraint.
8. Return the image, final prompt, and recipe note.

If exact title text renders incorrectly after one retry, generate a text-light base poster and report the intended copy separately for later typesetting. Do not claim distorted text is correct.

## Hard Avoids

Always exclude:

- copied composition, copied wording, recognizable branding, or artist signatures;
- full illustrated scenes, realistic rendering, auto-traced photographic contours, or polished vectors;
- glossy mockups, 3D depth, cinematic lighting, hard shadows, lens blur, or gradients;
- centered template symmetry, card grids, UI panels, stickers, tape, or decorative blobs;
- dense collage, grunge overload, scrapbook styling, or more than two active inks;
- corporate event graphics, luxury editorial styling, commercial CTA language, or social-media template aesthetics;
- long paragraphs, decorative gibberish headlines, fake dates, fake venues, fake prices, QR codes, or URLs.

## Quality Gate

Before returning, verify:

- Does the page use one paper field, one main ink, and at most one small accent ink?
- Is 25%-45% of the page a connected empty zone?
- Does the composition have one dense cluster, one quiet counterweight, and one deliberate grid break?
- Does the composition commit to one primary skeleton, with clear roles for anchor, counterweight, path, interruption, and quiet zone?
- If this follows earlier posters, did the skeleton, title path, empty-space location, crop direction, and information topology materially change rather than merely swapping objects?
- Is the subject recognizable through simplified hand-drawn contours rather than realism or vector polish?
- Do contours include broken strokes, overshoots, blunt endings, and visibly unequal curves rather than uniformly smooth SVG-like paths?
- Are there only 2-5 hatching zones and a consistent ink voice?
- Does typography use two clear voices, a 4x-9x scale jump, and no more than 7 display words?
- Does the display lettering vary on at least three axes without turning every glyph into the same kind of wobble?
- Are the selected lettering behaviors limited to one display voice, one contrasting support voice, and at most one tiny utility voice?
- For Chinese, is the square-box rhythm broken while every critical character keeps a recognizable skeleton?
- Does one part of the title physically interact with the drawing rather than sitting in a separate header zone?
- Is the language human, specific, non-commercial, and in the user's language?
- When an image is supplied, is identity preserved while crop, layout, and text path are newly constructed?
- Do at least five structural variables differ from every supplied style reference?
- Was a raster image generated unless the user requested prompt-only or generation was unavailable?

## Output Format

````markdown
**生成图**

![Abstract line poster](absolute-image-path-or-rendered-image)

**最终 Prompt**

```text
[the exact five-paragraph prompt used]
```

**本次配方**

- 配色: [paper + main ink + optional accent]
- 构图: [drawing structure + negative-space location]
- 线条: [contour and hatching treatment]
- 字体: [hierarchy + voices]
- 原创性: [major structural departures from references]
````

## Example Requests

- “用 abstract-line-poster 做一张关于周五下班喝一杯的海报。”
- “把这张人物照片画成留白很多的线稿活动 poster，标题是：慢慢来。”
- “做一个咖啡和旧书交换会的手绘海报，3:4 竖版。”
- “沿用那套暖纸、单线、手写沟通感，但这次主题是远程工作。”
- “Make this dinner photo into a sparse two-ink line-art zine poster.”
