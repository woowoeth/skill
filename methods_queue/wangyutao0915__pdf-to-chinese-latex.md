---
name: pdf-to-chinese-latex
description: Translate any-language academic PDF papers (English, Japanese, Indonesian, German, French, etc.) into Chinese LaTeX projects that compile in Overleaf with XeLaTeX. Preserves equation numbering, tables, figures, and bibliography one-to-one with the source. Use this skill whenever the user mentions translating / 翻译 / 中文化 / 转中文 a PDF paper, generating a Chinese version of a 文献 / 论文 / paper, producing an Overleaf-compatible 中文版, or building a 中文 LaTeX 工程 from foreign-language academic documents. Also trigger when the user supplies one or more academic .pdf paths and asks for a Chinese translation that keeps equations, tables, figures and reference numbering aligned with the original.
---

# PDF → Chinese LaTeX (Overleaf-ready)

## What this skill does

Given one or more academic PDF papers in any source language, this skill produces, for each paper, a self-contained folder that can be uploaded to Overleaf and compiled to a Chinese version with XeLaTeX. Each output folder contains:

- `main.tex` — full Chinese translation in a `ctex`-based LaTeX template, with all equations, tables, algorithms, and bibliography preserved and renumbered to mirror the original.
- `images/` — figures cropped from the original PDF by caption-anchored rendering (works for both raster *and* vector figures).
- `raw.txt` — page-by-page text dump of the original, kept as the translator's reference.
- `README.md` — Overleaf compile instructions.

The skill keeps source-language paragraphs and Chinese paragraphs in 1:1 correspondence so the user (typically a graduate student doing literature review) can quickly compare and cite. It is *not* a quick OCR-and-MT pipeline — it is a careful translation with structural fidelity.

## Why this skill exists (the why, not just the what)

Naive PDF→LaTeX→translate pipelines break in three ways: (a) vector figures (route diagrams, network diagrams) disappear because they aren't raster images; (b) equation numbering drifts because the translator rewrites equations as plain text; (c) the output is a dead PDF instead of an editable LaTeX project, so the user can't add their own annotations or stitch the paper into their thesis literature review. This skill is built around fixing those three problems.

## When to invoke

Trigger eagerly when the user:
- pastes one or more academic `.pdf` paths and asks for a Chinese version, 中文版, 中文化, 翻译;
- mentions Overleaf / ctex / xelatex along with a paper they want translated;
- asks to build literature-review-ready 中文 LaTeX from a foreign paper.

Skip (or fall back to lighter tooling) when:
- the user just wants the *text* extracted (no translation, no LaTeX);
- the source is already in Chinese;
- the deliverable is a Word doc, a slide deck, or a PDF — use the corresponding skill (`docx`, `pptx`, `pdf`) instead;
- the source PDF is **scanned** (no embedded text layer — pure pixels). This skill needs real text for caption search, equation alignment, and bibliography parsing. Quick check: `pdftotext input.pdf -` (one-liner from the `poppler` toolkit). If the output is empty or near-empty, run OCR first (e.g., `ocrmypdf input.pdf input-ocr.pdf`) and feed the OCR'd file to this skill. `extract_text.py` will refuse loudly if it sees < 50 chars across 5+ pages.

## Operating principles (read before extending this skill)

This skill grew from real translation failures (wrong figure cropped, Wiley watermark baked in, landscape figure rotated, figures floated to end of document, bibliography hand-transcribed by mistake, …). Every fix landed here was meant to be **a universal principle internalized into the skill, not a per-paper workaround**. Anyone (human contributor or AI agent) extending this skill must keep that intent. Three tests for every change:

**1. Universality — generalize the rule, not the symptom.** "Wiley fig9 has a vertical watermark on the right edge" is the symptom; "publisher watermarks sit within Npt of the page edge — search for the string, exclude their bbox" is the universal rule. Encode the rule so the skill handles unseen papers automatically; never hard-code a specific journal name, page number, figure number, or bbox unless it is a user-supplied override.

**2. Internalization — a fresh user benefits without reading the commit history.** After a change lands, a brand-new agent loading this skill (or a new researcher installing it) must benefit automatically, without re-discovering the lesson. Knowledge belongs in:
- **Code defaults** — scripts behave correctly out of the box (e.g., `--auto`, bbox-based clipping, density-based caption picker, watermark detection are all on by default).
- **`SKILL.md` workflow steps** — hard checkpoints with concrete actions, e.g., Step 3.5 *visually verify every extracted figure*.
- **`references/troubleshooting.md`** — concrete `failure → cause → fix` entries for everything the heuristics may still miss.

If a lesson lives only in a commit message, conversation transcript, or someone's head, it is **not** internalized — finish the work.

**3. Low friction, high quality — keep the install-to-result path short.** The skill is meant to be loaded by an agent that has no prior context with this user, and produce a publishable Chinese translation on the first try. Optimize for:
- **Sane defaults** so the agent doesn't ask the user to configure things that have an obvious correct answer (the `_figure_includes.tex` sidecar already picks `width=` from PNG aspect — the agent doesn't re-derive it).
- **Loud failure** — when a heuristic doesn't apply, surface a visible signal (warning line, sidecar artifact, fallback log). Never silently ship broken output.
- **Verification loops that close inside the tool, not in the user's head** — e.g., `_inspection.html` makes "did I crop the right region?" answerable in 30 seconds without opening the source PDF.
- **Token-conscious docs** — SKILL.md describes what the agent must do, not the history of how we got here. War stories belong in commit messages and `troubleshooting.md`, not in the main workflow.

When proposing a change, run the three tests:

> 1. Would this same fix help **every** future paper of this kind, or only the one paper that surfaced it?
> 2. After it lands, can a fresh agent / fresh user benefit **without reading this conversation**?
> 3. Does it **reduce** friction (fewer steps, fewer questions, fewer tokens, fewer surprises) for the next user?

If all three answers are *yes*, land it. If not, reshape it until they are.

## Verify the install (do this once)

After installing the skill, run:

```bash
python scripts/self_check.py
```

This generates a tiny synthetic PDF in a temp dir, runs the full pipeline (`extract_text` → `render_figures --auto` → minimal `main.tex` → `check_tex` → `xelatex`), and prints PASS / FAIL per stage. Exits 0 if everything works. `xelatex compile` shows SKIP if no TeX install is on PATH — that's only a problem if the user wants local PDF output (Overleaf doesn't need it). Anything FAIL means the skill won't produce correct output on a real paper either — fix the broken dep before triggering the workflow.

## Workflow (7 steps + optional local compile)

Follow these in order. Each step has a clear stop/check; report progress to the user but don't ask permission between steps unless something genuinely ambiguous comes up.

### Step 1 — Ask two scoping questions (don't skip)

Before extracting anything, call `AskUserQuestion` with two questions:

1. **图表处理** (figure/table handling):
   - ① 从原 PDF 抽图嵌入 + 中文标题（推荐）
   - ② 占位框 + 中文标题
   - ③ 跳过图表
2. **翻译颗粒度** (translation depth):
   - ① 全文逐段（推荐）
   - ② 仅核心章节（摘要 / 引言 / 模型 / 算法）
   - ③ 全文 + 中英术语对照表

These two choices determine whether to run `render_figures.py` (step 3), and how aggressively to compress sections 5--7 (experiments, results) during translation. Without them you risk doing 4× the work the user wants — or 1/4×.

### Step 2 — Extract text per page

For each input PDF, run:

```bash
python scripts/extract_text.py "<pdf_path>" --out "<output_dir>/raw.txt"
```

This writes one page per delimiter (`========== PAGE N ==========`). The model then *reads* `raw.txt` and uses it as the translation source. Don't try to translate directly from the PDF binary — the per-page text is much easier to align with figure pages, table positions, and reference numbering.

Watch for:
- Wiley/Elsevier journals embed a full download header on every page (~30 short lines like "Downloaded from ... Online Library ..."). Mentally skip these when translating.
- Subscripts and superscripts often land on the next line in extracted text — interpret based on context.
- Landscape (rotated) tables come out as reversed character strings; **don't** try to translate these line by line — summarize their key findings in prose instead, with a pointer to the original page numbers in the README.

### Step 3 — Render figures (skip if user chose ② or ③ in step 1)

**Fastest path: `--auto`.** The script scans every page, picks the real caption per figure (density-based disambiguation), detects the actual image / drawing bbox (Voronoi-assigned per caption), auto-rotates landscape figures back to upright, and excludes publisher watermarks — all in one command:

```bash
python scripts/render_figures.py "<pdf>" --out "<output_dir>/images" --auto
# Wiley / Elsevier: add `--side-margin 30 --top-margin 100`
```

Per-figure manual overrides via suffixes after the keyword in `--figs`. Overrides layer on top of `--auto` — only the listed figures get replaced:

| suffix | use when |
|---|---|
| `\|bbox=x0,y0,x1,y1` | inspection HTML shows the red box at the wrong region (single-column override, subfigure split, etc.). Coordinates in PDF points. |
| `\|rotate=N` (0 / 90 / 180 / 270 CW) | auto-rotation went the wrong way or didn't fire when it should |

```bash
python scripts/render_figures.py "<pdf>" --out images --auto \
    --figs "5:11:Figure 5.|bbox=50,200,540,560,9:24:Fig. 9.|rotate=90"
```

**Two sidecars are written next to `images/`:**

- `_figure_includes.tex` — paste-ready `\begin{figure}[!htbp]` blocks with aspect-aware `width=` (see Step 5 table). Closes the "huge figure floats to end of document" trap by default.
- `_inspection.html` — see Step 3.5 for the visual checkpoint.

**Algorithm details, failure modes, watermark-string list, and deeper troubleshooting** live in [`references/figure_extraction.md`](references/figure_extraction.md). Read it only when `_inspection.html` shows a figure was cropped wrong. For paper-version edge cases (two-column papers, subfigure caption splitting, scanned PDFs, GB/T 7714 Chinese refs), see [`references/troubleshooting.md`](references/troubleshooting.md).

### Step 3.5 — Visually verify every extracted figure (do not skip)

The script also writes `_inspection.html` next to `images/` — open it in any browser. Each row shows the extracted `figN.png` on the left and the **source PDF page with a red rectangle over the exact crop region** on the right.

**Scan every row in under a minute** and check:

1. Does the red box contain the entire figure, including all sub-panels, axis labels, legend, and figure caption?
2. Is the extracted PNG oriented upright (not sideways or upside-down)?
3. For multi-figure pages, does each `figN` red box cover only its own figure and not bleed into neighbours?
4. For Wiley / Elsevier papers, is the right-edge "Downloaded from..." watermark and the top page-header band excluded?

`0 fallback to full page` in the script's exit summary does NOT guarantee correctness — the bbox / Voronoi / rotation heuristics can silently pick the wrong region on layouts they haven't seen before. This visual check is the hard checkpoint.

If something is wrong, fix it by passing `|bbox=x0,y0,x1,y1` (manual crop in PDF points) or `|rotate=N` (0/90/180/270 CW) as a suffix on that figure's `--figs` entry, re-run, and verify again. Coordinates can be read off the red rectangle's clip values shown in the inspection HTML, or by inspecting the source PDF page in a viewer that shows PDF points.

### Step 4 — Build the project skeleton

Create, for each PDF, a folder named `{FirstAuthor}{Year}_{ShortTopic}_中文版/` (e.g., `Tan2025_MDEVRPSTW_中文版/`). Inside:

- `main.tex` — start from `references/latex_template.tex` (a `ctex` skeleton with all the packages already loaded).
- `images/` — figures from step 3.
- `README.md` — see `references/readme_template.md` for the user-facing compile instructions.
- `raw.txt` — already from step 2.

### Step 5 — Translate section by section into `main.tex`

Replace the placeholders in `latex_template.tex` and fill in the body. Rules of thumb:

- **Title / authors / affiliations**: translate the title, romanize author names (don't translate them), translate affiliations.
- **Abstract + keywords**: translate as a single paragraph with a `\textbf{关键词：}...` line at the end.
- **Body sections**: paragraph-by-paragraph translation. Keep the original section/subsection numbering (`\section`, `\subsection`). If the source uses (1), (2), ... for itemized lists, mirror with `enumerate[label=(\arabic*)]`.
- **Equations**: every numbered equation in the source becomes a numbered equation in the translation, labeled `\label{eq:cN}` where N matches the source equation number. Use `\eqref{eq:cN}` in prose so the cross-references re-render correctly. Inline math stays in `$...$`.
- **Tables**: don't hand-transcribe — let `extract_tables.py` build the skeleton for you:

  ```bash
  python scripts/extract_tables.py "<pdf_path>" --out "<output_dir>/_tables.tex"
  ```

  Each table in the PDF is emitted as a paste-ready `\begin{table}[!htbp]` block with `tabularx + booktabs`, column types inferred from cell content (`l` for label cols, `r` for numeric). Paste blocks into `main.tex` where needed, fill in `\caption{...}` and translate header cells. Two real-world rough edges to fix manually: (a) text-strategy may over-extract (pulls an itemized paragraph as a "table") — just delete those blocks; (b) cells containing `[1.516, 2.775]` may split at the comma — merge the affected columns. Still ~30× faster than rebuilding by hand. For very large landscape tables (5+ columns × 20+ rows), prefer prose summary + page-number pointer to the source — don't burn a day on a table no one will read.
- **Figures**: paste from `<output_dir>/_figure_includes.tex` (auto-generated in step 3) into `main.tex` where the figure should appear, then fill in `\caption{...}` and `\label{fig:...}`. The sidecar already picked `\includegraphics` widths from each PNG's aspect ratio:

  | aspect (W/H) | width                | typical figure              |
  |---|---|---|
  | ≥ 2.5        | `0.85\textwidth`     | very wide banner            |
  | 1.5–2.5      | `0.75\textwidth`     | standard landscape          |
  | 0.9–1.5      | `0.65\textwidth`     | square-ish (single panel)   |
  | < 0.9        | `0.55\textwidth`     | portrait (often rotated)    |

  Default placement is `[!htbp]`, which lets LaTeX try here / top / bottom / float page — far less likely to defer a figure to the end of the document than `[ht]`. If a figure still defers, escalate to `[H]` (the `float` package is preloaded in `latex_template.tex`) — only as a last resort, since `[H]` can leave blank space on the page.
- **Algorithms / pseudocode**: use `algorithm + algpseudocode`. Translate comments; keep variable names exactly as in the source.
- **References**: list every entry in `\begin{thebibliography}{99}`. Keep author/journal/title in **English** (translators searching for the original will need this); only translate fields like "Accessed: ..." or "访问于 ...". **Don't hand-transcribe** — let `extract_bibliography.py` build the skeleton for you:

  ```bash
  python scripts/extract_bibliography.py "<output_dir>/raw.txt" \
      --out "<output_dir>/_bib.tex"
  ```

  Locates the References / Bibliography section, parses each entry by its `[N]` prefix (IEEE/Wiley style) or by `Surname, X.,` author-year start (Elsevier/OR style), and emits a ready-to-paste `\begin{thebibliography}` block. Paste it into `main.tex` and adjust line wrapping if pdfplumber lost any whitespace. Tested on 20-entry numbered (Tan2025) and 42-entry author-year (Liu2025) bibliographies.
- **Citations**: every `\cite{key}` in the prose must have a matching `\bibitem{key}` — see step 6 for the static check.

The CTeX setup automatically handles Chinese fonts; you don't need to specify `\setCJKmainfont` manually.

### Step 6 — Static validation

Before declaring done, run:

```bash
python scripts/check_tex.py "<output_dir>/main.tex"
```

The script reports:
- `\begin{...}` / `\end{...}` balance per environment;
- `\cite` ↔ `\bibitem` correspondence (missing bibitems, unused bibitems);
- `\ref` / `\eqref` ↔ `\label` correspondence;
- per-line `$...$` count parity (catches stray dollar signs that escape into prose);
- every `\includegraphics{X}` resolves to a **real image file** (PNG / JPEG / PDF / TIFF / EPS magic-byte check, honors `\graphicspath`). This catches the failure mode where an upstream step wrote 12-byte placeholder PNGs or left a path pointing at a missing file — both of which xelatex would silently skip, leaving blank space where a figure should be.

Fix everything the script flags. If `\cite` keys are missing bibitems, either add the missing bibitem or remove the orphan citation. If equation labels referenced in prose don't exist, add them. If an image is reported as missing or as having unrecognized header bytes, re-run `render_figures.py` for that figure number.

Don't claim "compiles cleanly" without running this step — the user may not have a local LaTeX install (Overleaf-only is common), and untested broken `.tex` files cost them a round-trip to Overleaf to discover.

### Step 7 — Package and hand off

For each output folder, create a same-named `.zip` next to it so the user can drag-drop into Overleaf:

```powershell
Compress-Archive -Path <folder>/main.tex,<folder>/images,<folder>/README.md `
                 -DestinationPath <folder>.zip -Force
```

(On bash: `cd parent && zip -r <folder>.zip <folder>`.)

End with a summary message that lists, per paper: the folder path, zip path, page count of source, number of equations/tables/figures preserved, and the **Overleaf upload steps**:

1. Overleaf → New Project → Upload Project → drag `.zip`.
2. Menu → Compiler → **XeLaTeX** (must be XeLaTeX; pdfLaTeX won't render ctex Chinese).
3. Recompile.

### Step 8 (optional) — Compile to PDF locally

If the user has a local TeX distribution with XeLaTeX (MikTeX / TeX Live / MacTeX), you can skip the Overleaf round-trip entirely and compile in place:

```bash
python scripts/compile_pdf.py "<output_folder>"
```

The script:
- Probes `xelatex` on PATH (and on Windows also checks the default MikTeX install path);
- Runs `xelatex -interaction=nonstopmode -halt-on-error` twice (the second pass resolves cross-references — `\ref`, `\eqref`, `\cite` all need it);
- Reports the resulting PDF path, size, and page count;
- Cleans up `.aux`/`.log`/`.out`/`.toc`/`.synctex.gz` so the output folder stays tidy (pass `--keep-aux` to preserve them when debugging).

If `xelatex` is not found, the script prints install commands (MikTeX / MacTeX / texlive-xetex) and the Overleaf fallback steps. The skill should *not* hard-require local TeX — but when it is available, running compile gives you a real end-to-end check that the `.tex` actually produces a clean PDF before declaring the task done. Static validation (step 6) is fast but doesn't catch issues like missing `\usepackage{multirow}` or font fallback warnings; only a full compile does.

When to run step 8:
- The user has MikTeX/TeX Live installed (check by running `where xelatex` / `which xelatex`).
- You want to verify ctex Chinese rendering — visually inspect the first page after compile.
- The user explicitly asks for a PDF (not just a `.tex`) as the deliverable.

When to skip step 8:
- No local TeX install — recommend Overleaf as default.
- The user is on a system where installing TeX would be intrusive (CI containers, shared machines).

## Output format invariants

These hold regardless of source language or paper length:

- One output folder per input PDF.
- `main.tex` always has `% !TEX program = xelatex` as the first line.
- Equation labels follow `eq:cN` where N is the source equation number.
- Figures are `fig1.png`, `fig2.png`, ... matching `\label{fig:...}` in the body.
- The README's "How to compile" section is identical across all output folders (use the template in `references/readme_template.md`).

## Common pitfalls and how to handle them

- **Pypdf images come out as decorations**: publisher logos, ORCID icons, journal banners get extracted as p01_0.jpg / p01_1.png etc. Don't bother filtering them — the figure rendering pipeline (step 3) doesn't use them. They're harmless leftovers.
- **PyMuPDF caption search fails**: the script tries `Fig. N.` / `Figure N.` / `FIGURE N` / `Abb. N.` automatically, so capitalization is usually a non-issue. If it still falls back to full page, the figure caption is probably wrapped weirdly (line-break mid-keyword) — hand-specify with `|bbox=x0,y0,x1,y1` after the keyword in `--figs`.
- **Cropped image is the WRONG region (got body text instead of figure)**: an in-text reference like "see Figure 5" appeared higher on the page than the actual caption, and an older version of the script picked it. The current version picks the lowest hit, but verify by opening the rendered PNG. If wrong, pass `|bbox=...` to lock the rect.
- **Figure has a Wiley/Elsevier download stamp baked in**: auto-watermark detection only fires when the watermark string sits within 80pt of a page edge. If it slipped through, add `--side-margin 30 --top-margin 100` to the command line.
- **Bibliography keys collide across translated batches**: each paper gets its own `\begin{thebibliography}`, so keys are scoped to the file. Don't bother prefixing keys with paper IDs unless the user explicitly asks for a merged bibliography.
- **Source uses non-standard equation numbering like (3.1)**: mirror with `eq:c3-1` or `eq:3-1`. The static check only cares about cite/label consistency, not the naming convention.
- **User asks for the translation in a Word doc instead**: that's a different skill (`docx`). This skill emits `.tex` only — don't try to render to `.docx` from here.

## Files in this skill

- `SKILL.md` — this file.
- `scripts/extract_text.py` — pdfplumber-based per-page text dump.
- `scripts/render_figures.py` — PyMuPDF caption-anchored figure renderer (with `--auto` discovery + watermark exclusion).
- `scripts/extract_bibliography.py` — turns the References section of `raw.txt` into a `\begin{thebibliography}` skeleton (handles numbered `[N]` and author-year `Surname, X.,` styles).
- `scripts/check_tex.py` — static validator for `main.tex` (envs, cite/bibitem, ref/label, `$` parity, image-file existence + magic-byte check).
- `scripts/compile_pdf.py` — optional local XeLaTeX compile (skips Overleaf).
- `references/latex_template.tex` — `ctex` skeleton with all packages preloaded.
- `references/readme_template.md` — the per-paper README contents.
- `references/troubleshooting.md` — extended FAQ for tricky cases (multi-column papers, rotated tables, etc.).
- `examples/` — sample input/output pairs (see README).
