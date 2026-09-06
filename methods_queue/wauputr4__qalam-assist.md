---
name: qalam-assist-write-ebook
description: Plan, draft, revise, cite, and compile source-grounded books or journal articles in LaTeX using NotebookLM. Use when an author wants to turn the configured NotebookLM notebook into an outline, section draft, literature synthesis, cited manuscript, BibTeX references, or compiled LaTeX document without inventing sources.
---

# Qalam Assist

Build a LaTeX manuscript from NotebookLM evidence. Orchestrate the installed `$notebooklm` and `$latex-document` skills; do not duplicate their full instructions.

## Notebook roles

Use this fixed methodology notebook for writing guidance:

```text
14f5746f-276f-4c3a-a056-cce106fa57bd
```

Use a separate evidence notebook for the manuscript's subject matter. Ask for its full ID when the user has not supplied it. The methodology and evidence IDs may be the same only when that notebook genuinely covers both roles.

Always pass full notebook IDs. Do not rely on `notebooklm use` or shared context.

Before planning or drafting, read:

- [references/writing-guide.md](references/writing-guide.md) for the grounded writing workflow.
- [references/prompt-library.md](references/prompt-library.md) when planning, drafting, researching, revising, or preparing submission.
- [references/source-catalog.md](references/source-catalog.md) when identifying provenance or bibliography metadata.

## Prerequisites

Require the NotebookLM runtime and the two supporting skills:

```bash
notebooklm auth check --test --json
notebooklm list --json
```

Accept auth only when `status` is `ok` and `checks.token_fetch` is `true`. If auth fails, follow `$notebooklm`; never request cookies in chat or commit credential files.

Require `$latex-document` from:

```text
https://github.com/ndpvt-web/latex-document-skill
```

If unavailable, tell the user to install it with:

```bash
npx skills add https://github.com/ndpvt-web/latex-document-skill --skill latex-document
```

## Workflow

## Author approval gates

These gates control every workflow step below. Do not silently make manuscript choices or begin content production merely because the user named a topic.

### 1. Brief before research or drafting

Ask one compact set of questions for all missing manuscript decisions:

- document type and working title;
- purpose and intended reader outcome;
- target reader and current knowledge;
- language, voice, and style references;
- target length in pages or words;
- publication format: trim size, margins, body font, and target compiler;
- included topics, exclusions, and required examples;
- citation style, publisher or journal template, and disclosure requirements;
- evidence notebook ID and output directory.

Return a short manuscript contract: promise, scope, exclusions, tone, length, publication format, evidence notebook, and unresolved choices. State every assumption plainly. Treat page targets as meaningful only after trim size, margins, font, and compiler are fixed.

End by asking the author to approve or revise the contract. Do not query NotebookLM for content, create an outline, write prose, create files, or compile a document at this stage.

### 2. Require explicit approval

Proceed only after the author explicitly approves the contract, for example with setujui, approve, or lanjutkan. If the author changes title, reader, scope, length, tone, or evidence, update the contract and request approval again.

### 3. Draft-review loop

After approval, create the smallest outline that satisfies the contract, then work on exactly one outline unit at a time:

1. Query ready NotebookLM sources for that unit and retain returned source IDs.
2. Return a review draft with claim-to-source ledger, facts and interpretations clearly separated, and unresolved items.
3. Ask the author whether to accept, revise, or reject the unit.
4. Only after acceptance, write the approved unit into the LaTeX manuscript and move to the next unit.

Do not generate a whole book or article in one pass. Do not present a review draft as inserted manuscript text. Do not compile a final document until the author has accepted the intended units or explicitly asks for an interim build.

Apply steps 4-10 to the current unit. Step 10 applies only to an accepted unit or a requested interim build.

Interpret short author replies consistently:

- `lanjut`, `continue`, or `gas`: accept the current unit and start the next unit;
- `revisi` plus instructions: keep the unit in review and revise only what was requested;
- `setuju` or `oke`: approve the current contract or unit in context;
- `compile`, `buat PDF`, or `gabungkan`: build only accepted units unless the author explicitly includes review drafts.

When intent is ambiguous or acceptance would make a material manuscript change, ask one short question instead of guessing.

Keep review and accepted files separate:

```text
manuscript.tex
chapters/bab-01.tex
review/bab-02.tex
references.bib
source-ledger.md
```

Write a unit to `review/` first. Move or rewrite it into `chapters/` only after acceptance. Use one shared manuscript wrapper for page geometry and compilation; do not maintain a separate preamble per chapter.

### 4. Prepare the current unit

Use the approved manuscript contract. Write a one-sentence purpose and explicit scope boundary for the current unit before generating prose.

### 5. Inspect evidence for the current unit

Run:

```bash
notebooklm source list --notebook <evidence-notebook-id> --json
```

Use only sources with `status: ready`. If the requested topic is not covered, say so and ask the user to add a source; do not fill the gap from memory.

### 6. Choose the current-unit writing path

For a book:

1. Define purpose, reader, tone, and exclusions.
2. Use a linear outline with non-overlapping chapters.
3. Draft one chapter or subsection at a time.
4. Review coherence across chapters after each completed unit.

For a journal article:

1. Start from supplied data, results, and methods.
2. Establish supported conclusions and measurable novelty.
3. Draft results and methods before conclusion, abstract, introduction, and title.
4. Never manufacture data, uncertainty, ethics approval, or novelty.

Select the smallest matching template from `references/prompt-library.md`. Fill known placeholders, ask only for missing required values, and use one prompt per task. Do not send the entire prompt library to a model.

### 7. Query NotebookLM before writing

Ask a focused question for the current section and require JSON:

```bash
notebooklm ask "<focused question>" \
  --notebook <evidence-notebook-id> \
  --json
```

Use `-s <source_id>` for a selected subset. Keep the returned `references[].source_id` with every claim carried into the draft.

If `cited_text` is missing, generic, or only a section heading, inspect source full text or ask a narrower question. Mark unresolved claims `[perlu verifikasi]`.

If `notebooklm ask --json` returns only a session or incomplete evidence, retry once with a narrower question and selected source IDs. If it still lacks usable citations, inspect ready source full text. Stop and report the evidence gap when neither path supports the claim.

### 8. Draft and cite

Use `$latex-document` to choose the smallest appropriate template and write valid LaTeX.

- Preview generated prose before inserting it.
- Separate fact, inference, opinion, and illustration.
- Convert NotebookLM citation numbers deterministically: citation number → source ID → verified local BibTeX key → `\cite{key}`.
- Never guess author, year, DOI, page, publisher, or citation key metadata.
- Preserve an audit trail from each substantive claim to its NotebookLM source ID.
- Keep the internal source ledger separate from the reader-facing bibliography. The ledger may contain NotebookLM source IDs and verification notes; the bibliography contains only verified publication metadata.
- Classify sources before relying on them: primary or official, scholarly secondary, reputable explanatory, or weak/background. A NotebookLM source being `ready` means it is queryable, not authoritative. Use weak sources only for bounded context and disclose their limitation when material.

### 9. Revise

Perform three passes:

1. **Evidence:** verify claims, numbers, quotations, and source mappings.
2. **Structure:** remove repetition and ensure each section serves the manuscript purpose.
3. **Language:** remove chatbot residue, simplify unclear sentences, and keep terminology consistent.

Disclose AI assistance when required by the institution, publisher, or user.

### 10. Compile and inspect

Follow `$latex-document` for compilation and preview. Fix the root cause of compilation errors, then inspect the rendered PDF for broken references, overflow, unreadable tables, missing glyphs, and inconsistent headings.

Do not call the work complete until the `.tex` source compiles and the PDF has been visually checked.

### 11. Finalize

Before calling a manuscript final, confirm:

- author name, final title and subtitle;
- license or publication rights;
- AI-assistance disclosure requirements;
- PDF metadata and removal of draft labels such as `Naskah kerja`;
- accepted-unit completeness and absence of review-only text;
- resolved citations, verified bibliography metadata, and recorded evidence gaps;
- final page count under the approved publication format.

If any item is unresolved, label the build as an interim manuscript rather than final.

## Deliverables

Return only the artifacts needed for the request:

- `.tex` source and supporting files;
- `.bib` entries containing verified metadata only;
- compiled PDF and preview when requested;
- a short source ledger mapping claims or sections to NotebookLM source IDs;
- a list of unresolved `[perlu verifikasi]` items.

Do not generate podcasts, slides, quizzes, or other NotebookLM artifacts unless the user asks.
Do not promise DOCX layout parity with LaTeX. Keep `.tex` as the canonical editable source and PDF as the canonical rendered output.
