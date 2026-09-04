---
name: write-iut-thesis
description: Draft, expand, revise, structure, and maintain a full Islamic University of Technology BSc thesis from source documents using the local iutbscthesis LaTeX template. Use when writing or editing thesis metadata, front matter, abstract, chapters, related works, methodology, results, discussion, conclusion, citations, appendices, figures, tables, code listings, or compile guidance for main.tex. Also use when the user expects an AI agent to turn papers, notes, PDFs, LaTeX sources, bib files, data tables, and assets into a substantial thesis manuscript chapter by chapter without requiring repeated babysitting.
---

# Write IUT Thesis

Use this skill to write thesis content that fits an Islamic University of Technology BSc thesis template while also behaving like an agentic thesis-writing workflow. The skill governs both formatting and the practical process of turning source material into a full thesis book.

## Operating Principle

Do not merely make a template-valid short draft. Build the thesis deliberately from the user's source documents. A thesis chapter should normally be more expansive than the corresponding paper section because it must explain motivation, background, definitions, design choices, assumptions, evidence, interpretation, limitations, and links to the overall thesis claim.

When source papers are available, treat them as ground truth. Extract, reorganize, and expand from them; do not compress them into a superficial summary unless the user explicitly asks for brevity.

## First Checks

- Read `main.tex` before editing or drafting so local chapter names, labels, bibliography keys, and project conventions stay intact.
- Read the relevant chapter files before editing so numbering, labels, citations, and narrative continuity are preserved.
- Inspect available source directories such as `Papers/`, `assets/`, `data/`, `figures/`, `chapters/`, and bibliography files before writing substantive content.
- Treat `iutbscthesis.cls`, `frontmatter.sty`, and `personnelhandler.sty` as the source of truth for supported commands.
- Preserve the template structure unless the user explicitly asks for a structural change.
- Do not leave instructional filler, placeholder text, sample chapters, `TBD`, or `TODO` in final thesis-facing content.
- Prefer academic prose with clear claims, evidence, citations, and transitions.

## Agentic Thesis-Building Workflow

For any request to write a chapter, expand a chapter, merge papers into a thesis, or continue the thesis book:

1. **Inventory the evidence first.** Read the source paper sections, appendices, tables, figures, datasets, code, bib entries, and existing chapter material relevant to the requested chapter. Use PDFs only when needed; prefer `.tex`, `.bib`, `.md`, `.csv`, code, and asset filenames when available because they are easier to cite and transcribe accurately.
2. **Make a chapter coverage map.** Identify every source element that belongs in the chapter: claims, definitions, research questions, methods, equations, algorithms, prompts, datasets, models, tables, plots, limitations, and results. Decide what belongs elsewhere so the chapter does not duplicate earlier content.
3. **Write expansively by default.** Expand each source element into thesis prose that explains why it matters, how it was produced, what assumptions it carries, and how it supports the thesis argument. Avoid one-paragraph collapse of multi-page paper sections.
4. **Use figures and tables proactively.** Include relevant source figures, diagrams, heatmaps, charts, algorithms, and result tables when they support the chapter. Refer to each with `\autoref{...}` before or near placement.
5. **Preserve traceability.** Every substantive empirical claim must be tied to a cited source, a local table, a figure, an equation, a dataset description, or a previously reported result. Do not invent numbers, model lists, dataset sizes, prompts, or conclusions.
6. **Build chapter by chapter.** Add or revise one chapter at a time unless asked for a whole-book pass. Include the chapter in `main.tex` only when it is ready to compile.
7. **Verify after editing.** Compile when practical, inspect log errors, and fix LaTeX/reference failures introduced by the edit. If compilation requires missing packages, tell the user the install command instead of working around the template.

## Expansion Norms

When the user says "write", "expand", "make it detailed", "use the papers", or asks for a thesis chapter, assume they want a substantial thesis treatment:

- Introduce the problem and motivation before technical details.
- Define terms before using them as results.
- Explain methodology sequentially enough that another researcher can reproduce the work.
- Include equations, algorithms, prompts, and pipelines when they are part of the source work.
- Report important result tables rather than paraphrasing them away.
- Discuss figures in the text, not just as decorations.
- Connect each subsection back to the chapter's role in the thesis.
- End major result sections with interpretation, not only numbers.
- State limitations and scope boundaries where the evidence requires them.

Do not take the short path just because the user did not specify length. If the source material is large, the thesis chapter should reflect that size.

## No-Hallucination Rules

- Papers, source `.tex`, datasets, code, and user-provided notes beat secondary summaries.
- If a summary file conflicts with the source paper, follow the source paper and mention the conflict only if relevant.
- If a number, prompt, model name, or dataset detail cannot be verified locally, do not fabricate it. Search the repo first; ask the user or mark the gap only if it blocks the chapter.
- Preserve exact model names, metric names, and dataset sizes when the source gives them.
- Do not merge incompatible axes or instruments without explaining the mapping and its limits.
- Do not attribute a result to a study that did not produce it.

## Template Contract

Use `\documentclass{iutbscthesis}` and keep bibliography resources in the preamble when bibliography is required.

Required metadata before `\begin{document}`:

```latex
\title{Title of the Thesis}
\addauthor{Name}{Student ID}
\supervisor{Name}{Designation}{Department}
\department{Department of Computer Science and Engineering}
\program{BACHELOR OF SCIENCE IN COMPUTER SCIENCE AND ENGINEERING}
\defensedate{DD}{Month}{YYYY}
```

Rules:

- Use one and only one `\supervisor{...}{...}{...}`.
- Use one `\addauthor{...}{...}` per student.
- Use `\addcosupervisor{...}{...}{...}` only when co-supervisors exist.
- Do not put commas inside author, supervisor, or co-supervisor name/designation/department arguments because `personnelhandler.sty` uses comma-separated internal lists.
- Keep `\defensedate` as three arguments: day, month name, year.

## Front Matter Order

Keep front matter in this order unless the local template or user explicitly requires a change:

```latex
\coverpage
\pagenumbering{roman}
\titlepage
\declarationofcandidate
\dedicatedto{...}
\tableofcontents
\listoffigures
\listoftables
\clearpage
\begin{abbreviations}
  \abbr{ABC}{Expanded Term}
\end{abbreviations}
\begin{acknowledgement}
...
\end{acknowledgement}
\begin{abstract}
...
\end{abstract}
\pagenumbering{arabic}
```

Front matter norms:

- Write acknowledgements formally and specifically. Include supervisors, co-supervisors, collaborators, family, tools, funding, lab support, department, and institution when verified or requested.
- Write the abstract as one compact summary covering context, problem, method, results, and conclusion.
- Keep abbreviations alphabetized when practical and define only terms used in the thesis.

## Chapter Norms

A normal thesis body often includes:

1. `Introduction`
2. `Related Works`
3. `Data and Models` or `Background`
4. `Methodology` / study chapters
5. `Results`
6. `Discussion`
7. `Conclusion`

Adapt chapter names to the repository's existing structure. Do not force a five-chapter generic outline onto a thesis whose evidence requires more chapters.

### Introduction

Introduce the topic for readers outside the immediate research area. Define key terms early. Explain motivation, practical relevance, research gap, problem statement, objectives, contributions, scope, and thesis organization. Use teaser figures when the source work has strong visual anchors.

### Related Works

Make this a large synthesis chapter when the source bibliography is large. Group prior work by theme, method, dataset, limitation, or debate. Compare studies, show disagreements, connect them to the thesis gap, and end by motivating the methodology. Do not produce an annotated list.

### Data And Models / Background

Document datasets, instruments, statement lists, model cohorts, coordinate systems, preprocessing, projection models, and implementation assumptions. Include source statement lists, diagrams, and algorithms when they are necessary for reproducibility.

### Methodology

Explain the complete approach sequentially. For each component, state role, input, output, method, theoretical basis, implementation choices, alternatives considered, and justification. Include equations, algorithms, prompts, and pipeline diagrams when used by the research.

### Results

Report raw and summarized results clearly in tables and figures. Interpret how each result answers the research questions. Include major appendix results from papers when those results are necessary for the thesis argument.

### Discussion

Synthesize across chapters. Explicitly state each thesis-level claim and support it with earlier experiments, data, tables, figures, equations, or cited literature. Discuss implications, limitations, threats to validity, and what the thesis proposes.

### Conclusion

Restate objectives and research questions, summarize key findings, explain contributions, acknowledge limitations, suggest future work, and end with a clear final statement. Do not overclaim beyond the evidence.

## Figures, Tables, Algorithms, Listings

- Refer to every figure and table in the text before or near its placement, using `\autoref{...}` where possible.
- Use descriptive labels such as `fig:architecture`, `tab:metrics`, `alg:projection`, and `lst:preprocessing`.
- Use `[H]` only when fixed placement is genuinely needed; otherwise use standard float placement.
- Tables use `booktabs` style when possible: `\toprule`, `\midrule`, `\bottomrule`.
- The template configures table captions on top and figure captions below; follow that convention.
- Use `subfigure` for grouped images and label both the group and meaningful subfigures.
- Use `algorithm`/`algpseudocode` for important algorithms when the template loads them.
- Use `lstlisting` for short code excerpts only when code itself is part of the argument.

## Citations

- Use `biblatex` commands already supported by the template: `\cite`, `\textcite`, `\parencite`, `\footcite`, and `\textcites`.
- Keep bibliography entries in `.bib` resources already used by `main.tex`.
- Cite claims about prior work, datasets, algorithms, external facts, and source-paper methods.
- Use multi-citations for grouped related evidence, e.g. `\cite{key1,key2,key3}`.
- If adding a citation key, verify it exists in an active `.bib` file or add a complete entry from a reliable source.
- Print references with `\printbib` in the back matter unless the template uses a different command.

## Language Rules

- Use precise academic language, active voice where natural, and concrete claims.
- Prefer "we" when the existing thesis uses it.
- Avoid generic filler such as "this is very important" unless the sentence states why.
- Avoid starting every related-work paragraph with author names; begin from the concept, gap, method, or finding.
- Use transition phrases to connect chapters and studies.
- Use `\emph{...}` for emphasis sparingly.
- Use `\verb|...|` or `\texttt{...}` only for packages, commands, filenames, code identifiers, or literal technical tokens.
- Use correct punctuation for hyphen, en dash, and em dash in prose.

## Compile Guidance

The class commonly loads `stix2`, `biblatex` with `backend=biber`, and other CTAN packages. On Debian/Ubuntu, missing dependencies commonly require:

```bash
sudo apt install texlive-fonts-extra texlive-bibtex-extra biber texlive-xetex
```

Compile a bibliography-aware build with:

```bash
pdflatex -halt-on-error main.tex
biber main
pdflatex -halt-on-error main.tex
pdflatex -halt-on-error main.tex
```

If LaTeX prompts `Enter file name:`, stop and install the missing package. Do not type `main.tex` at that prompt.
