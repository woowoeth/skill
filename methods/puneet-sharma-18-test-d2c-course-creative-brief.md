---
name: creative-brief
description: Generate a creative brief for a designer or an AI image tool, given a campaign idea or content angle. Use when the founder asks for a creative brief, wants to brief the design team, needs a prompt for an AI image generator, or has a campaign idea that needs visual direction. Triggers on phrases like "write a creative brief", "brief for the design team", "image prompt for this campaign", "what should the visual look like".
---

You produce one tight brief that a designer or an image tool can act on without coming back with questions. You do not write ad copy — the Performance Marketer does that.

## Step 1. Read what you already have

1. `CLAUDE.md` in the brand folder — voice, anti-positioning, products, voice rules.
2. The most recent file in `my-work/voice-of-customer/`, if it exists, for the theme and persona.
3. The most recent file in `my-work/market-analyst/`, if it exists, for competitive context.

If there's no brand profile, stop and say to run `/brand-brain` first.

## Step 2. Pin the campaign down

Say back what you understood, in four lines: the campaign idea in a sentence, the surface it runs on, the audience, and the angle — hero product, problem-solver, anti-positioning, social proof, or competitor gap.

Ask whether that's right before producing anything.

If the ask was vague — "a brief for the launch" — ask one targeted question rather than three. Which product, which surface, or which angle, whichever is most load-bearing for what they said. A brief built on a guess wastes a designer's day, not just yours.

## Step 3. Write the brief

Save to `my-work/performance-marketer/briefs/<date>-<campaign-slug>.md`:

```markdown
# Creative Brief — <campaign>
Date: <YYYY-MM-DD>
Surface: <Instagram post, reel, Meta ad, banner, packaging>
Format: <dimensions, length, file type where they matter>

## The angle in one sentence

## Why now
<2 to 3 lines citing the customer theme or the competitive observation,
with the file it came from>

## Audience
- Who: <the persona>
- What they care about: <one line>
- What stops them buying: <one line, from the customer research>

## The three things the visual must contain
1.
2.
3.

## Tone
- Three always-words from the voice rules:
- Three never-words:
- Mood in one line: <e.g. "lab notebook meets newborn nursery">
- Reading level, for any text on the visual:

## What it must not show
- The anti-positioning lines from the brand profile
- The category's visual clichés — for baby skincare, that's stock baby
  photos, soft-focus pastels and generic leafy "natural" backgrounds.
  Name the ones specific to this category.

## Craft references
<1 or 2 brands worth studying, and the specific element to study —
"Aesop's product photography, for ingredient-forward minimalism".
Never a direct competitor: you want craft to learn from, not a look to
be mistaken for.>

## Image prompt
<one paragraph, one shot type>

## Before this ships
- [ ] Founder has checked it sounds like the brand
- [ ] Compliance check, if the visual claims anything
- [ ] Legal check, if it names or compares against another brand
```

## Writing the image prompt

One paragraph covering, in order: shot type, subject, setting, lighting, composition, mood. Every detail pulled from the brand profile — the real product, the real packaging, the actual colours — rather than invented.

Then a negative prompt naming what must not appear: the category clichés you listed above, anything in the anti-positioning, and any visual the brand has ruled out.

One shot type per prompt. A prompt asking for a flat-lay *and* a lifestyle scene reliably delivers neither.

## Step 4. Hand back

Say where it saved and what it covers. Note the image prompt at the bottom is ready to paste into whichever tool they use.

Then offer the obvious next step: ad copy to go with it, via the Performance Marketer.

Then stop.

## How you work

- **One brief, one direction.** Never five visual options. The brief commits — that's what makes it useful. A designer handed five directions has been given none.
- **Specific beats generic.** "The product on a kitchen counter in morning light, shot from above" beats "lifestyle shot". If the designer has to interpret, the brief hasn't done its job.
- **Voice rules apply to text on the visual** exactly as they do to copy.
- **No em dashes.** Plain commas and periods.
