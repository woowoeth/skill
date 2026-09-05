---
name: make-maths-pdf
description: Build and revise self-contained, cited LaTeX mathematics projects from complete ChatGPT transcript corpora in PDF, Markdown, or other readable formats. Use explicitly to synthesize overlapping or branched chats at full informational depth, integrate new chats into existing material with targeted rewriting, or make small reader-driven refinements; compile with pdflatex and keep project files together inside the working root.
---

# Make Maths PDF

Turn a corpus of mathematical chat transcripts into a persistent, coherent document for the person who asked the original questions. Treat the chats as research notes about the intended subject, audience, notation, and depth—not as a sequence to reproduce.

## Establish the assignment

1. Resolve the working root and the selected transcript folder. Transcript folders are named `chats` or `chats_<topic>`. If more than one could apply and the invocation does not select one, ask which to use.
2. Resolve a dedicated LaTeX project folder inside the working root. Use the folder supplied at invocation. If creating a document and no folder is supplied, create `latex_<topic>` from the selected `chats_<topic>` name; when the topic or a safe folder name is unclear, ask first.
3. Keep every document-owned file inside that LaTeX project folder: `.tex` sources, the compiled PDF, `.bib` files, figures, local styles, generated tables, included sections, and compilation artifacts. Never scatter these files across the working root, the transcript folder, or source-reference folders.
4. Identify whether the user wants a new document or an edit to an existing project inside that folder. If several possible project folders or main `.tex` files exist, or the requested insertion point is unclear, ask before editing.
5. Inventory user-supplied source folders, existing `.bib` files, figures, and the LaTeX project's structure. External books and articles may remain in their own source folders inside the root. Keep the working `.bib` database in the LaTeX project folder; when a bibliography is supplied elsewhere, copy or merge the needed entries into that project database without modifying the original. Do not treat supporting mathematical files as chat transcripts merely because they share a transcript file format.
6. Inventory and read every transcript in the selected transcript folder, recursively, before outlining or writing. Do not assume one file format: transcripts may be PDF, Markdown, plain text, HTML, or another readable format. Use the appropriate parser for each file, preserve mathematical notation during extraction, and use visual inspection or OCR when a PDF's text layer is incomplete. If any transcript format cannot be read reliably, identify the file and ask for a usable export or conversion before writing.
7. Record the invocation's requirements about topics, exclusions, notation, organization, rigor, citations, and the target section. These instructions take priority over defaults inferred from the corpus.

Do not begin drafting while some transcripts remain unread. Reading the corpus is a global analysis phase, not an incremental write-as-you-read process.

## Synthesize the whole corpus

Build an internal concept map and a coverage ledger across all chats before deciding on the document structure. The ledger should record every distinct piece of substantive mathematical content, including definitions, claims, intuitions, examples, derivations, caveats, comparisons, notation choices, references, and unresolved qualifications.

- Use the user's questions to infer their background, motivations, points of confusion, preferred explanations, and desired level of detail.
- Do not treat conversational attention as a direct measure of mathematical importance. A topic may dominate the transcripts because the user repeatedly struggled with one point or deliberately followed a temporary rabbit hole. Judge its emphasis in the document by the current invocation, its role in the overall mathematical program, its dependencies, and the explanation the intended reader actually needs—not by the number or length of exchanges devoted to it. Preserve its distinct substantive content, but consolidate clarification loops and give digressions a proportionate place and length.
- Detect common trunks, repeated questions, clarification loops, and overlapping passages in branched chats. Merge repeated material semantically; do not repeat a definition, explanation, or example merely because it occurs in several files.
- Remove redundancy of expression without removing information. When several explanations overlap, combine them into one treatment that retains every unique mathematical point, nuance, example, qualification, and useful formulation contributed by any version.
- Do not target compression or a shorter document. Unless the invocation requests omissions, preserve every distinct item in the coverage ledger except errors corrected under the policy below.
- Let later follow-up questions improve earlier material. They may require a clearer explanation, a deeper treatment, a new topic, a correction, a notation change, or a different ordering.
- Prefer the clearest, most complete, and mathematically correct version when chats contain competing explanations. Reconcile compatible versions into one exposition.
- Organize by mathematical dependencies and pedagogical coherence, not transcript order, file order, or frequency of repetition.
- Identify mathematical errors, contradictory claims, conflicting notation, genuine gaps, and requests that cannot all be satisfied.

Apply this priority order when resolving choices:

1. The current invocation's explicit instructions.
2. Conventions and constraints in the supplied LaTeX project.
3. Mathematical correctness and internal consistency.
4. Preferences and explanations inferred from the transcripts.

## Correct routine errors autonomously

Do not interrupt the user over minute or mechanically resolvable issues. Correct an error autonomously when the intended form is mathematically unambiguous from the surrounding argument, the preferred sources, or direct verification, and the correction is local rather than structural. This includes:

- spelling, grammar, punctuation, formatting, and export or transcription errors;
- obvious notation slips or inconsistent symbol formatting;
- clear local sign errors, missing constants, malformed formulas, or factual mislabels whose correction does not change the intended mathematical program.

Use the corrected form in the document without discussing the source typo there. After delivery, mention a nontrivial mathematical correction briefly when useful, but do not produce an inventory of cosmetic fixes.

## Pause when clarification would improve the result

After reading the whole corpus, ask focused questions without hesitation whenever the answer would materially change the document. In particular, pause before writing when:

- a mathematical error has more than one plausible correction, changes a definition or conclusion, affects substantial downstream content, or exposes a genuine disagreement between reliable sources; explain the issue concisely and propose the available resolution;
- scope, notation, audience, structure, or the target section remains consequentially ambiguous;
- sources or transcript folders have conflicting roles;
- a requested choice conflicts with the supplied document;
- a transcript is unreadable or incomplete;
- producing a self-contained account appears to require a substantive mathematical topic, theorem, example, or proof outside the program established by the chats.

Wait for the user's response in these cases. Do not ask perfunctory questions when the corpus and invocation already determine a sound answer. Editorial connective material does not require approval.

## Write an organic mathematical document

The result must read as an independently conceived mathematical text.

- Do not include the original questions, a Q&A structure, dialogue, transcript chronology, references to chats, or phrases such as “as discussed.”
- Do not preserve distinctive conversational sequencing or repetition from which the source questions or branching history could be reconstructed.
- Make the document self-contained at the level appropriate to the inferred reader.
- Aim for complete informational coverage of the selected chats, not brevity. The finished document may be as detailed as, or more detailed than, the nonredundant mathematical content of the corpus.
- Use smooth transitions, consolidated definitions, short reminders, and connective explanations freely. Reorder material as needed.
- Match the rigor of the transcripts. For a survey-style corpus, emphasize definitions, intuition, notation, relationships, and informative examples rather than adding many proofs.
- Include proofs that appear in the transcripts unless the user excludes them or a correction makes them unusable. Do not add substantial proofs merely for formality.
- Normalize notation throughout. Follow invocation-specific notation first, then the supplied project's notation; otherwise select one coherent convention informed by the chats.
- Do not broaden the mathematical program merely because external references contain related material.

For an existing project folder, edit the supplied `.tex` source directly, preserve unrelated material, match its macros and style, and integrate the new prose into the requested section. For a new project folder, default to a clean `article`-class main file using pdflatex-compatible mathematics packages, omit the author unless supplied, and choose a structure suited to the topic. Keep the main source, included sources, bibliography, and PDF together within that folder hierarchy.

## Integrate overlapping new transcripts into existing material

Use this mode when the user explicitly says that one or more transcripts overlap significantly with material already written in LaTeX, or that the new material needs careful integration rather than being added on top.

1. Read the complete selected transcript corpus and the existing LaTeX project before editing. If the user identifies a subset as newly added, distinguish it while retaining the whole-corpus context.
2. Build a correspondence map between the new material and the existing exposition. Classify each distinct contribution as already covered equivalently, complementary, a clearer or more complete replacement, a correction or conflict, or genuinely new.
3. Choose the best location and treatment for every contribution. Retain equivalent existing material without duplicating it; merge complementary details; replace weaker or inaccurate passages; distribute material across existing sections when mathematical dependencies require it; create a new subsection only when the content is genuinely new and does not fit organically elsewhere.
4. Rewrite affected paragraphs, subsections, or sections as needed so the result reads as a single planned exposition. The user's explicit integration request authorizes these targeted rewrites; do not seek approval merely because careful integration requires replacing existing prose.
5. Preserve every distinct mathematical contribution from both the existing document and the new transcripts unless the user explicitly requests an omission or the correction policy applies. Preserve unrelated sections and the project's overall voice.
6. Reconcile notation, citations, labels, theorem numbering, definitions, and cross-references across the affected material. Review the complete affected narrative arc for duplicated explanations, seams, broken dependencies, and contradictions.

Ask before proceeding when integration would materially change the document's global scope or architecture, require a global notation change, discard nonredundant existing content, or present several genuinely different structural choices with important consequences. Otherwise make the best editorial integration autonomously.

## Use citations and BibTeX by default

Create a properly cited document unless the user explicitly asks for a citation-free treatment.

1. Give first precedence to sources the user identifies or supplies inside the working root.
2. Next, use sources already cited in the transcripts when they can be identified and verified.
3. Consult and cite a different source only when the needed material cannot reasonably be found in the preferred sources. Do not use this permission to expand the document's scope.

Inspect a source before relying on it. Never invent bibliographic metadata, page numbers, theorem numbers, quotations, or support that the source does not provide. Use pinpoint citations when they materially help the reader.

Maintain references in a BibTeX `.bib` file and cite them with ordinary LaTeX citation commands. Preserve an existing bibliography system when it already uses BibTeX. For a new document, default to a conventional BibTeX setup such as `\bibliographystyle{plain}` and `\bibliography{references}`. Do not switch the project to biblatex/Biber unless the user requests it.

External sources may also be consulted for verification. If they reveal a material error, use the clarification gate before drafting. Prefer supplied sources for the final citations whenever they support the relevant claim.

## Compile and verify

Compile with `pdflatex` and BibTeX from the LaTeX project folder so that the PDF and all compilation artifacts remain there. The bundled `scripts/build_pdf.sh` performs the normal compilation sequence and fails on unresolved references or citations:

```bash
scripts/build_pdf.sh project-root/latex_topic/main.tex
```

Before finishing:

- confirm the PDF was produced from the current sources;
- resolve compilation errors, undefined citations, undefined references, and materially bad layout warnings;
- inspect the rendered PDF for clipped equations, broken tables, poor page breaks, malformed bibliography entries, and inconsistent section styling;
- spot-check mathematical notation and cross-references against the source;
- compare the finished source against the coverage ledger and account for every distinct substantive item not explicitly excluded or corrected;
- ensure the document contains no conversational residue or duplicated branch material.

## Refine the document after reader questions

Treat questions asked after delivery as a normal iterative mode. The user may ask about the PDF, then ask for the answer to be added or for a small passage to be replaced.

- Answer a question in the conversation without changing files unless the user asks for a document edit.
- When an edit is requested, make the smallest coherent change that incorporates the answer. Read the surrounding source and relevant mathematical context before editing.
- Integrate new material as organic exposition, not as a pasted answer, Q&A, addendum, or record of the follow-up conversation.
- Preserve the document's transcript-derived architecture: its principal scope, section hierarchy, ordering, narrative progression, and notation should remain stable.
- Do not re-outline the document, rename or reorder unrelated sections, change global notation, or broadly rewrite prose merely because a local improvement is possible.
- Adjust nearby transitions, definitions, citations, labels, and cross-references when needed to make the local edit read naturally and remain correct.
- If the requested “small” change would actually require a major restructuring or conflict with the transcript-derived program, explain this and ask whether the user wants a constrained local treatment or an explicit larger revision.

On a later invocation, recover the document's original basis from the complete transcript corpus before editing unless that full-corpus analysis has already been completed in the active context and the inputs have not changed. After every document edit, recompile and verify the PDF. Briefly identify which passage changed without turning the report into a new transcript history.

These constraints apply to ordinary reader-question refinements. They do not prohibit the broader targeted rewriting described in the integration mode above when the user explicitly identifies new overlapping transcripts.

## Report the result

Give the user the LaTeX project folder and the paths to its main `.tex`, `.bib`, and PDF outputs. Briefly report:

- the resulting organization and any significant overlap that was consolidated;
- for an integration pass, the principal regions merged, replaced, or redistributed;
- material corrections agreed with the user and any nontrivial routine corrections made autonomously;
- meaningful omissions or scope decisions;
- any outside sources used because the preferred sources were insufficient;
- unresolved issues or compilation warnings.

Keep this provenance report in the conversation, not in the mathematical document.
