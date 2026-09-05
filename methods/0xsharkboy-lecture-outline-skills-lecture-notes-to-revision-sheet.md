---
name: lecture-notes-to-revision-sheet
description: >-
  Use when asked for a revision sheet, study sheet, exam sheet, cram sheet or
  "fiche de révision" built from lecture notes that already live in Outline --
  including phrasings like "fais une fiche de révision de la Lecture 3", "make a
  revision sheet for this lecture on outline", "fiches pour réviser le cours X",
  "add a study sheet under that note", "régénère la fiche", or "the note changed,
  update its revision sheet". Also use when an existing revision sheet must be
  refreshed after its parent lecture note was edited, or when asked to make a
  lecture note revisable without rewriting the note itself.
---

# Lecture notes to revision sheet

## Overview

Turn one Outline lecture note into a **revision sheet nested under it**: a single
screen you reread the night before an exam, ending in a self-test whose answers are
hidden until you open them.

Follow `../_shared/outline-conventions.md` for the collection lookup, the title
convention, the no-H1 rule and the `editMode` safety table. This file covers what is
specific to revision sheets.

Without this skill, agents reliably produce a **reformatted copy of the note**: the
note's own section numbering, 550+ words, the definition dropped into a blockquote,
and answers printed in the open under an "Answers" heading — a document that is not
faster to revise from than the note it came from.

## The source is the Outline note, never the deck

The sheet derives from the parent note and nothing else. If something examinable is
missing, fix the **note** first (that is the `lecture-notes-to-outline` skill's job),
then regenerate. Reaching for the source PDF produces a sheet that disagrees with the
note sitting directly above it.

**One sheet per topic, not per note.** Most notes carry one topic and get one sheet.
A note that covers several — a session that ran an intro and a lecture back to back, or
a deck spanning distinct areas — gets **one sheet per topic**, each nested under the same
note, each at the cap, each with its own self-test.

Split when compressing to a single sheet would drop whole examinable areas rather than
detail. Cut along the note's own `## N.` section boundaries, group adjacent sections into
topics, and never split one section across two sheets. Use the **fewest sheets that hold
the examinable core** — splitting a note that fits in one sheet just scatters it.

**The split plan is a hypothesis; `wc -w` is the test.** You decide the grouping by
eyeballing density, and that estimate is regularly wrong on quote-heavy sections. If a
planned sheet busts the cap at write time, **split it again** — do not drop examinable
areas to make the original plan hold. Announce the revised count rather than quietly
compressing.

Content-free discussion prompts are not a topic. A section of open seminar questions
carrying no content of its own earns no sheet and no place on another one.

When a note is split, the `<topic>` slot in each title carries that sheet's **sub-topic**
instead of the lecture's overall topic; the rest of the title rule is unchanged. A
definition needed by two sheets is repeated in both: each sheet answers its own quiz.

A course-level request ("les fiches du cours X") iterates over the course page's children
that have content and skips empty stubs. There is no course-wide synthesis sheet.

## Placement and title

`mcp__outline__create_document` with `parentDocumentId` = the lecture note's id, so the
sheet is a real sub-page. **Before creating anything**, look at that note's `children[]`
in the collection tree for titles starting `DD-MM-YY - Revision sheet -`. If any exist,
this is a regeneration of **all** of them, not a creation — a split note's sheets are
regenerated as a set, because a change in the note can move content between them.

The title is the parent's title with `Revision sheet` inserted after the date:

```
01-09-26 - Revision sheet - Lecture 3 - Socio-technical aspects of cybersecurity
```

**Outline rejects a title over 100 characters.** When the mirrored title would exceed
that, shorten the *topic* and keep the date, `Revision sheet` and the lecture number
intact: `01-09-26 - Intro/Lecture 1 - Course introduction plus fundamental concepts and
terms` becomes `01-09-26 - Revision sheet - Intro/Lecture 1 - Fundamental concepts and
terms`.

English, like the sheet itself — the exam is in English, so the terms must be recalled
in English. Never invent a shorter scheme; the date prefix is what keeps the sidebar
sorted with its siblings.

## First line: provenance and the freshness check

The body opens with one line, **never an H1**:

```
Revision sheet for [01-09-26 - Lecture 3 - Socio-technical aspects of cybersecurity](url) — parent revision 12.
```

`parent revision N` is the parent's `revision` field from `mcp__outline__fetch`. On a
later run, an unchanged parent revision means the sheet is current — say so and write
nothing.

## The five blocks

`## Definitions`, `## Structures to reproduce`, `## Key claims`, `## Exam traps`,
`## Self-test` — in that order, every time. **Not the note's section numbering**: the
blocks are revision functions, and reusing the note's structure is what turns the sheet
back into a copy of the note.

| Block | What goes in it |
|---|---|
| `Definitions` | every formal definition, one bullet each, shaped `- **Term** — *"verbatim quote"* (citation)` |
| `Structures to reproduce` | complete enumerations, taxonomies, arrow chains (`A → B → C`), checklists |
| `Key claims` | central theses, "from X to Y" shifts, worked contrasts |
| `Exam traps` | 2-4 bullets: likely confusions, where a definition stops, fine distinctions |
| `Self-test` | 5-7 questions |

Where the note defines a term without quoting a source — a method checklist naming
*validity*, *reflexivity* and the like — keep the term-first shape and drop the quote
marks; do not invent a citation. A topic that genuinely defines nothing keeps the
heading and says so rather than padding it.

A definition bullet names the term **before** the quote. A bare quote makes the reader
work out what is being defined, which is the opposite of a revision sheet. The quote
itself stays verbatim and keeps its citation, and it is never a `>` blockquote.

**Cap: 500 words**, whatever the note's length, measured with `wc -w` on the body —
measure it, do not estimate. `wc` counts markdown syntax and the provenance URL too, so
the prose lands near 450. Over the cap, **delete a bullet or a question**; do not reword
to claw back three words. A dense lecture is a reason to cut harder, not to exceed the
cap: the compression is the product. If the cutting would cost whole examinable areas
rather than detail, the note covers more than one topic — split it into several sheets
instead of stretching one.

## The self-test only tests the sheet

Every question and every answer must be answerable from the four blocks above it. A
question reaching back into the note, or an answer adding reasoning the sheet never
states, breaks the sheet's one guarantee: **you can revise from it without reopening
the note.**

## Answers go in `+++` toggles

Outline's ToggleBlock serializes as `+++` fences and round-trips through the API. The
first child block is the visible head; everything after it is hidden until opened.

```markdown
**1.** Name the five elements of an STS in the course definition.

+++
Answer

People, technologies, organizations, rules, practices.
+++
```

**Write `+++`; expect `+++++` back.** Outline's serializer emits `3 + nesting height`
plus signs, so a stored toggle reads back with more `+` than you wrote. That is proof it
parsed as a node rather than literal text — it is not corruption, and it is not a reason
to rewrite the sheet.

**The blank line after `Answer` is load-bearing.** Without it, head and answer parse as
one paragraph, the whole answer becomes the visible head, and the toggle hides nothing.
Verified: the API stores the two-paragraph form intact and collapses the one-paragraph
form.

Outline's collapsible *headings* are not an alternative — the `collapsed` attribute is
neither serialized to nor parsed from markdown.

Toggles rendering as literal `+++` in the write response is the only reason to fall
back to a single `## Answers` block at the end. "I can't guarantee spoilers render" is
not a reason — read the response and find out.

## Regeneration: the one place `replace` is allowed

The sheet is a derived artifact this skill owns, so it may be regenerated. The
permission is gated on what the document says, not on what you expect it to say:

1. `fetch` **every** existing sheet under the note, not just the first.
2. First line starts with `Revision sheet for ` → generated here, expendable →
   `replace` allowed.
3. Anything else — annotated, hand-written, restructured → **stop and ask.** One
   hand-edited sheet blocks that sheet; say which, and leave the rest alone unless the
   regeneration would move content into it.
4. Parent revision unchanged since the recorded one → nothing to do; say so.
5. A split that now needs fewer sheets than exist leaves the extra ones in place —
   deleting a page is the user's call, so report it instead.

`replace` is **never** allowed on the parent note. This skill writes only inside its
own sub-page.

## Red flags — stop

- About to open the body with `# ...`
- About to write `> ` in front of a definition
- The sheet's headings match the note's headings
- Stretching one sheet past the cap for a note that actually holds two topics
- Writing answers in the open because spoilers "might not render"
- A definition bullet that opens with the quote instead of the term it defines
- A `wc -w` over 500, or a word count you estimated instead of measuring
- Rewording sentence by sentence to squeeze under the cap instead of cutting a bullet
- A self-test answer containing something the sheet does not state
- A title over 100 characters — `create_document` rejects it outright
- `create_document` without having checked the parent's `children[]`
- `replace` without having read the existing first line

## Verify

Read the body returned by the `create_document` / `update_document` response — that
response **is** the stored content, so do not re-fetch. Confirm: toggles came back as
`+` fences and not literal text, each toggle's head and answer are still separate
paragraphs, `→` and em dashes survived, and the word count is under the cap. Report the
URL, the blocks written, and any judgment call.

## Common mistakes

| Mistake | Fix |
|---|---|
| Reformatting the note under new headings | Regroup by revision function, not by lecture section |
| Body opens with an H1 | Outline stores the title separately |
| Definition in a `>` blockquote | Inline italic quote with its citation |
| Definition quoted with no term in front of it | `- **Term** — *"quote"* (citation)` |
| Answers printed under an "Answers" heading by default | `+++` toggles; the fallback needs evidence |
| Toggle written without the blank line after its head | The answer becomes the visible head |
| Title in another language, or without the date prefix | `DD-MM-YY - Revision sheet - Lecture N - <topic>` |
| Split sheets all carrying the lecture's overall topic | Each title's `<topic>` slot carries that sheet's sub-topic |
| A second sheet for a topic that already has one | Check the parent's `children[]` first |
| One note split into sheets that each fit easily | Split only when one sheet would drop examinable areas |
| Questions written from the note | The sheet must answer its own quiz |
| Sheet generated from the PDF | Fix the note, then regenerate from the note |
