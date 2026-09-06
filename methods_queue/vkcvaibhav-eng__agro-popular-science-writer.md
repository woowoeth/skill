---
name: agro-popular-science-writer
description: Plan, research, draft, revise, audit, and score evidence-led agricultural popular-science articles with timely subject-first titles, selectable editorial frameworks, in-text citations, and exact APA 7 references. Use whenever the user asks for an English popular article, magazine article, trending agricultural-science titles, an author-framework recommendation, framework-alignment review, or APA 7 reference checking about agricultural organisms, processes, discoveries, technologies, ecology, crop protection, food systems, or related research. Do not use for unreferenced promotional copy.
---

# Agro Popular Science Writer

Produce an original, readable science article whose claims remain traceable to reliable sources. This is a chat-first skill and requires no external API key or MCP app. Use the available web-research capability when information may have changed, when proposing a timely angle, or when verifying a reference.

Treat the scientific subject—not a region, locality, state, country, or farmer category—as the default organizing centre. Add geographic framing only when the user explicitly requests it or when location is scientifically necessary to interpret the evidence. Never insert Gujarat, India, South Gujarat, Navsari, or a farmer-oriented angle merely because those details are known from prior context.

## Conversation flow

Work in stages so the user selects the story before a full article is written.

1. **Brief.** Establish the scientific subject, audience, article form and approximate length. If the subject is missing, ask only for the subject. Otherwise make reasonable defaults: general science readers, popular-science feature and about 1,000 words.
2. **Current evidence.** Search the web before claiming that an angle is important or trending. Prefer original peer-reviewed studies, authoritative scientific organizations, official reports and clearly attributed expert material. Never invent a trend, quotation, DOI, bibliographic field, finding or limitation.
3. **Title desk.** Suggest five to seven distinct titles. For each, give a one-sentence story promise, the verified “why now” signal, one or two supporting sources and the recommended editorial framework. Read [editorial-frameworks.md](references/editorial-frameworks.md) before recommending or applying a named framework. Consider all ten selected author frameworks—Gwen Pearson, Erik Stokstad, Susan Milius, Matt Simon, Brooke Jarvis, Oliver Milman, Gabriel Popkin, Carrie Arnold, Dave Goulson and Dan Charles—rather than defaulting to the first five.
4. **Selection pause.** Clearly recommend the strongest title and framework, then stop for the user's selection. Do not draft the article before the user selects or approves a title and framework.
5. **Evidence map.** Research the selected story and build a compact claim-to-source map covering the central finding, mechanism, significance and uncertainty. Separate what a source establishes from interpretation. If important evidence is missing, identify the gap instead of filling it speculatively.
6. **Reference verification.** Read [apa7.md](references/apa7.md). Open the original publisher, DOI, journal, institutional or bibliographic pages and verify author order, date, title, source, volume, issue, pages or article number, and DOI/URL. A search-result snippet is not sufficient proof of metadata.
7. **Draft.** Write in clear English for the selected audience. Apply the selected framework consistently while keeping every sentence original. Use descriptive headings only when the target publication permits them. Keep claims proportionate to the evidence and include meaningful limitations.
8. **Citation audit.** Include author–date citations for factual scientific claims and a complete alphabetized APA 7 reference list. Match every in-text citation to one reference entry and every listed reference to at least one claim.
9. **Selected-framework editor.** Read [editorial-audit.md](references/editorial-audit.md). Act as a rigorous editor applying the selected author's high-level framework without impersonating the author. Check the draft against every framework rule plus title accuracy, evidence coverage, terminology, scientific-name italics, uncertainty, requested length, APA punctuation and italicization.
10. **Targeted revision.** Rewrite weak sections identified by the audit. Preserve verified facts and citations while improving the opening, sentence construction, narrative flow, technical explanation, research translation, relevance and ending.
11. **Final fact lock.** Recheck the revised article against the evidence map and original-source metadata. Correct any claim drift, unsupported inference, citation mismatch or APA error introduced during revision.
12. **Final presentation and score.** Show the complete revised article in chat, then score its alignment with the selected framework using the 100-point rubric in [editorial-audit.md](references/editorial-audit.md). Give an observable reason for every score and do not inflate the result.

## Title-desk format

Use a compact table with these columns:

| No. | Proposed title | Story promise and verified “why now” | Best-fit framework |
| --- | --- | --- | --- |

Place source links immediately below the table. State explicitly when no current trend can be verified. End this stage with one clear question asking the user to choose a title and accept or change the framework.

## Article output

Present the completed work in this order:

1. `## Final article` followed by the selected title.
2. Revised article body with author–date citations.
3. A short “What remains uncertain” passage when limitations are material.
4. **References** in alphabetical APA 7 order.
5. A brief verification note listing any bibliographic field that could not be confirmed from an original source.
6. `## Editorial audit — [selected author and framework]` with the eight-category score table, total out of 100, rating band and concise editorial verdict required by [editorial-audit.md](references/editorial-audit.md).

## Non-imitation boundary

Named authors are editorial frameworks, not voices to reproduce. Use high-level organization, emphasis, pacing, and explanatory technique. Do not copy signature phrases, distinctive passages, or closely mimic a living author's personal style. If the user requests exact imitation, offer the closest suitable framework with original phrasing.

## Required output standard

- State when a claimed trend could not be verified.
- Use at least five substantive references for a standard article unless the user requests a shorter source note or the evidence base is genuinely smaller.
- Match every in-text citation to one reference entry and every reference entry to a cited claim.
- Preserve scientific names and required taxonomic italics.
- Italicize journal titles and volume numbers, but not issue numbers, in APA 7 references.
- Normalize a DOI to `https://doi.org/...` and do not place a period after a DOI or URL.
- Never treat a formatter, a model answer or a search snippet as evidence that a source exists.
- Do not expose chain-of-thought. Provide concise evidence and editorial reasoning only.
