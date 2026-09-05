---
name: lecture-notes-to-outline
description: >-
  Use when asked to take, write, or publish notes from a lecture, course slide
  deck, seminar, or PDF/PPTX into Outline -- including phrasings like "take
  notes of TopicN.pdf on outline", "put this lecture in the right
  page/collection", "note this course in outline", or any request to turn
  university/course material into an Outline document. Also use when notes must
  be "complete but synthetic", or when an existing dated lecture document in
  Outline needs to be filled in or refreshed.
---

# Lecture notes to Outline

## Overview

Turn a lecture deck into one Outline document organized **by concept, not by
slide**. Three things go wrong without this skill: agents publish with
`editMode: "replace"` onto documents that already hold notes (destroying them),
the scope of "complete but synthetic" drifts 30% in length between runs
because each agent re-decides what counts as lecture substance, and each run
invents its own prose texture, so pages in one collection do not read as
siblings.

## Placement: find the document, do not create one

`../_shared/outline-conventions.md` carries the lookup, the title convention, the
no-H1 rule, the `editMode` safety table and the sibling read. Read it first.

What is specific here: the destination almost always **already exists as an empty
dated stub**. Match on date and topic -- a child doc named `DD-MM-YY - <Topic>`
whose date equals the deck's cover-slide date is the target. Create a new document
only when no dated stub matches.

The sibling you read for prose texture is a lecture document **that already holds
notes** -- in this collection, or the nearest course collection if this one is all
stubs. An older sibling whose title lacks a topic, or whose first line repeats one,
is showing you texture to copy and a title convention to ignore. Skipping that read
is what makes two runs produce pages that do not look related.

**One document per dated session, not per topic covered.** A deck that runs a
course intro and a lecture back to back is one session and gets one page; two
pages sharing a date prefix imply two sessions that never happened. Split only
when the material was actually delivered on different dates.

## Never replace a non-empty document

The `editMode` safety table is in `../_shared/outline-conventions.md`. This skill
takes **no exception** to it: lecture notes get edited by hand as often as by an
agent, so nothing here is a disposable derived artifact.

## Red flags -- stop

- About to pass `editMode: "replace"` without having read the current body
- "My synthesis restructures the whole document, so replace is the right shape"
- "The existing content looks like the same thing, so overwriting is fine"

All three mean: fetch, read, and `append` or `patch` instead. If content genuinely
must go, say so to the user and let them decide.

## The title carries the topic, so the body does not

The title is `DD-MM-YY - Lecture N - <the deck's own topic>`, for example
`01-09-26 - Lecture 3 - Socio-technical aspects of cybersecurity`. A stub named
`01-09-26 - Lecture 3` is an unfinished title: when you fill the document in, set
the title to include the deck's topic, keeping the existing date and lecture
number exactly as they are. Rename via the same `update_document` call that
writes the body.

Because the title carries the topic, the **body's first line never repeats it**.
That line is the lecturer and date, then the pointer to the parent course page:
`Joakim Kävrestad, 2026-09-01. Course admin lives in the parent page, [Course](url).`

## Attach the source deck

The notes are one reading of a file; keep the file with them, so the source
survives the local copy being renamed, moved or deleted.

1. `mcp__outline__create_attachment` with the deck's `contentType`, its `name`,
   and its exact `size` in bytes (`stat -c%s`). It returns a pre-signed
   `uploadUrl`, the `form` fields to send with it, and the final `attachment.url`.
2. POST the file to `uploadUrl` as multipart form data -- every `form` field
   verbatim, then `file=@<path>`. **Step 1 only reserves the attachment: it hands
   back a real-looking id and url while no bytes exist yet, so stopping there
   leaves a link that resolves to nothing.** The signed upload URL expires an hour
   after it is issued -- create and upload in the same pass.
3. Link it from the body, on the line directly under the provenance line:
   `Source deck: [<filename>](<attachment.url>)`

Confirm it round-trips: `fetch` with `resource: "attachment"`, download the
`signedUrl` it returns, and check the byte count equals the local file's.

## The document contract

Markdown starts with a one-line provenance sentence, **never an H1** -- Outline
stores the title separately. Course admin is not a section -- it lives on the
parent page, reached from that first line. Under it sits the `Source deck:` line
from the section above. Then `## N. Section` headings, numbered
consecutively from 1, in the deck's own conceptual order. Typically:

1. The lecture's first core concept
2. ...through the lecture's argument...
N-1. Seminar / discussion questions
N. Method or reading checklists

Group scattered slides on one concept into one section. Drop pure discussion
prompts that carry no content ("What's your take?").

## Scope: what "complete but synthetic" means

**In** -- everything that could be examined: every definition with its citation,
every taxonomy and enumeration, worked examples, seminar questions and checklists
near-verbatim.

**Out** -- slide titles as structure, content-free prompt slides, the full
end-of-deck reference list (cite inline where used instead).

**Course admin is never dropped, but it is not lecture content.** People, topic
list, learning outcomes, credits/grading table and thresholds, assignment
rationale, seminar mechanics and the reading list with chapter mapping do not
change from one lecture to the next, and the next deck will repeat those slides.
They belong in the **parent course page**, not the dated lecture page.

* Parent page empty and the deck carries admin slides → `append` them there,
  and open the lecture page with one line pointing to it.
* Parent page already has them → leave it alone; do not restate them.

Do not drop admin as "scaffolding" -- grading thresholds and the chapter mapping
are the most reused part of the notes. Put them where they stay findable.

## Fidelity

- A formal definition is an **inline italic quote carrying its citation in the same
  sentence**, sitting in the paragraph or bullet that uses it -- the shape is
  `Information security = *"preservation of confidentiality, integrity and
  availability of information"* (ISO/IEC 27000, 2018, p. 4).` A `>` blockquote
  makes the definition a standalone block and breaks the sibling pages' texture.
- Preserve enumerations completely -- a taxonomy with one branch missing is wrong,
  not synthetic.
- Reproduce figures as inline arrow chains: `Identify → Protect → Detect`.
- A number read off a **figure** rather than slide text must say so
  ("the timeline shows a Year 0-Year 5 plan"). Never present it as slide text.

## Verify

Verify from the write response, per `../_shared/outline-conventions.md` -- do not
re-fetch. Confirm the table rendered, nested bullets survived, and arrows/`→`/em
dashes are intact. Report the URL, the sections covered, and any judgment call you
made.

## Common mistakes

| Mistake | Fix |
|---|---|
| Creating a second doc for a lecture that has a stub | List the collection first; match on date |
| `replace` on a doc with notes in it | `append` / `patch`, or ask |
| Opening the body with `# Title` | Outline's title is a separate field |
| Dropping the grading/ILO/reading info | It is examinable; keep it, on the parent page |
| Repeating course admin in every lecture page | It belongs once, on the parent course page |
| Transcribing slide by slide | Regroup by concept; merge repeated slide titles |
| Section numbers starting at 2, or unnumbered first section | Number consecutively from 1 |
| Writing the body without reading a sibling document | Fetch one; it is the style spec, not just the naming convention |
| Definitions pulled out into `>` blockquotes | Inline italic quote + citation, in the sentence that uses it |
| Leaving the stub title as `DD-MM-YY - Lecture N` | Extend it with the deck's topic in the same update call |
| Repeating the lecture title on the body's first line | The title carries it; the first line is lecturer, date and the parent-page pointer |
| Attachment created but never POSTed to `uploadUrl` | The link 404s; upload the bytes in the same pass, then verify the size |
| Notes published with no link to the deck they came from | Attach the source; the local file will not stay where it is |
