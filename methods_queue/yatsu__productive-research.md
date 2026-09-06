---
name: writing-up-findings
description: Use when writing up the results of research, an investigation, a comparison, or a verification as a document — a report file, "write this up for the team", or the write-up step of a research skill. Not for co-authoring a spec, PRD, or proposal section by section with the requester, chat answers, commit messages, code comments, or changelogs
---

# Writing Up Findings

## Overview

A write-up is read by someone who was not in the investigation — usually the requester, later. Its job is to let that reader decide, without reading everything, what was found, what it means, and whether the work needs redoing. Facts and opinions are kept apart so the reader can check the facts and argue with the opinions.

**Core principle:** Reader first, most important first, facts apart from opinions.

## When to Use

- "Write up what you found" / "put this in a report" / "document the investigation"
- The write-up step of productive-research:understanding-on-their-terms and other research skills
- Any document whose content is the result of looking things up, measuring, or comparing

Not for: co-authoring a spec, PRD, or proposal with the requester — that is interactive drafting, so ask them for the context you need and draft section by section instead. Also not for chat answers, commit messages, code comments, or changelogs.

## Before Writing: Reader Profile and Thesis

Once the write-up begins, emit these four lines as a message of their own — a text block sent before any tool call the write-up makes: no search, no fetch, no file read or write other than reading this skill. When an investigation skill ran first, its tool calls are already behind you; the write-up still opens with this message:

- **Reader:** who will read this.
- **Already knows:** what they can be assumed to know, and what they cannot.
- **Wants:** what they need from the document, and what they want to know first.
- **Thesis:** one sentence stating what the document establishes or answers.

Then proceed without waiting for approval; if the requester corrects any of the four, restart from the corrected version. Repeating the profile in the handover message afterwards does not stand in for sending it first — by then the reader it describes has already been guessed at.

## The Document Contract

Write the document in the requester's language. It has these parts, in this order.

**1. Thesis and overview.** The document's first line is its `#` heading, and that heading is the thesis sentence, not a topic title: "WAL mode ends the reader stalls on the audit database, and the open question is the NFS-mounted volume", not "SQLite journaling modes". Directly under it, a few paragraphs giving the main findings and what they imply. Nothing goes between the heading and those paragraphs — no reading legend, no status note, no background section. A reader who stops here knows the result and whether the work needs redoing. There is no separate summary section; these paragraphs are the summary.

**2. Body: fact sections and opinion sections.** Each section is one kind, and its heading says which — facts under Findings, What X does, Results; opinions under Assessment, Discussion, Conclusions. Order the sections for the reader (by category, by importance, by time), not in the order the sources were read. A subject chapter produced by another skill's contract keeps its own inner order and still obeys one kind per section.

- Fact sections carry what was observed, measured, or quoted: numbers, quotes, observations. Evaluative adjectives ("amazing", "promising", "dead") and sentences about what should be done next belong in an opinion section instead.
- A claim from a secondary source that a primary source would settle is checked against the primary source before it is written as fact; if it stays unresolved, it is written as unresolved and attributed to the source that made it.
- Opinion sections carry interpretation, judgment, hypothesis, and recommendation. Each one names whose opinion it is — ours, the maintainer's, a named colleague's — and what it rests on. Someone else's opinion is reported in their terms and labeled with their name, never with ours. It also says what kind of opinion it is (inference, judgment, hypothesis), states any assumption the argument needs before the conclusion that rests on it, and lays out the steps from findings to conclusion so a reader can find a missing one.

**3. Method and detail.** How the data was gathered: exact commands, raw output, and other detail most readers skip. A finding states the number and what was measured; the conditions behind it — hardware, cache state, how many runs, what was not compared — are named here and only here, after the findings and the assessment.

**4. Where I looked.** Sources searched, and sources deliberately not searched ("searched the docs and the GitHub issues; did not search Hacker News, Reddit, or conference talks").

**5. Terms.** A list of the names the body relies on in more than one place, each with a one-sentence definition. Project-specific names taken from the requester's own wording — an internal artifact, a codename, a package with a special role — are on it by definition: the writer does not decide that the reader already holds them. Terms of art join it when the reader profile says the reader does not hold them. It sits here, after the parts a first-time reader goes through in order, because it is consulted when needed, not read through. A name the body uses only once gets its definition in a parenthesis at that mention instead:

> the audit database (the read-only replica the nightly compliance export runs against)

**6. References.** Every statement taken from a source carries its citation in the body, where the statement is made. A source's first mention in the body is written out in full — the titled link followed by its number, so the reader sees what is being cited without scrolling:

> In WAL mode one writer and many readers proceed concurrently ([Write-Ahead Logging — SQLite](https://sqlite.org/wal.html) [3]), and the WAL file persists between connections [3].

Later mentions of that same source are the bare number, as in the second half of that line. This part is the numbered list those numbers point to, one entry per source, `[n] [Title](url)`. Files and artifacts from the conversation are named in the text and need no number. The document ends here.

## The Chat Reply

The document is handed over in a chat message, and that message — not the document — carries what could not be investigated, the limitations of the work, and suggested next steps. Write them out in the message itself: the document has no "open questions", "limitations", or "next steps" section to point back at.

## After Writing

- Sweep the finished document for every name the reader has not met in the conversation — internal artifacts, packages, codenames, people, team-specific nicknames. A name that appears only inside a quoted opinion, a method aside, or a heading still counts. A name the body uses in more than one place gets a Terms entry; a name used once gets a parenthesis at that mention. Add the missing ones before anything else, and remove any Terms entry the body does not rely on.
- Re-read against the reader profile: the first screen answers what the reader wants to know first, and nothing assumes what they don't know.
- Headings: reader order, consistent granularity. Merge or split.
- Terminology: one term per concept throughout. If the project keeps a glossary, propose entries for new terms.
- If a subagent is available, give it only the document and the reader's first question. If it cannot answer from the document, fix the document.

## Common Mistakes

- Opening with background because the sources did ("SQLite was first released in 2000 by...") — the reader wants the result first
- A heading that names the topic instead of stating what was established
- An adjective smuggled into a finding ("its excellent resolver") — move the judgment to an opinion section or drop it
- A colleague's opinion written in the document's own voice, or labeled with the wrong owner — name whose it is
- Analyzing the causes of an opinion as if it were a fact — an opinion needs a basis, not a root-cause analysis
- An "open questions", "limitations", or "next steps" section at the end of the document — that content goes in the chat reply
- A reference list at the end that nothing in the body cites, bare URLs, or "[1]" without a title at first mention — cite in the body, in the title-link-number form
- Sending the reader profile with the finished document instead of before starting it
