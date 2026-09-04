---
name: accessible-pdf
description: Make a single course file (Keynote deck, Word document, or bare PDF) into a WCAG 2.1 AA / ADA Title II–ready PDF for posting to students on bCourses, following UC Berkeley RTL guidance. Use when the user asks to make a file accessible, remediate a PDF, add alt text, check a PDF for Ally, or prepare slides/readings for posting. Works file-by-file.
---

# accessible-pdf

Turn one source file into a PDF that a screen reader can actually use, and verify it before it goes to students. Three lanes, chosen by input type; every lane ends with the same automated verification. Reference material distilled from Berkeley RTL is in `reference/berkeley-rtl-guidance.md` — read it once per session, don't re-fetch the web pages.

**Fix at the source whenever a source exists.** Alt text and structure that live in the `.key`/`.docx` survive every future re-export; anything injected into a PDF is lost the next time the deck is edited. PDF injection is the fallback, not the default.

## Scripts (all `python3`, all in `scripts/`)

| script | does |
|---|---|
| `verify_pdf.py FILE.pdf` | audit: tagged, title, language, text layer, figure alt text, headings, links, fonts → verdict READY / NOT READY. `--json` for machine output. `--extract-images DIR` pulls images in page order for drafting alt text. `--fix [--title T] [--lang en-US] [--alt alt.json]` sets title/lang/MarkInfo/DisplayDocTitle and injects `/Alt` on Figure tags by index; writes `*_a11y.pdf`. |
| `audit_docx.py FILE.docx` | source-side Word audit: real headings, fake headings, manual lists, image alt text, vague/bare-URL links, table header rows and merged cells, fonts, language. |
| `keynote_tools.py open\|images\|export` | open a deck in Keynote; pull original images from the `.key` bundle; AppleScript export to PDF (uses Keynote's *last* PDF export settings — do one manual export with Accessibility: On first). |

## Lane 1 — Keynote deck (the common case)

1. **Get a PDF to inspect.** Keynote 12.0 on this machine already exports tagged PDFs via AppleScript (verified 2026-08-18: structure tree, H1 tags, live text), so run `keynote_tools.py export DECK.key /tmp/DECK.pdf` first and check the `tagged` line of `verify_pdf.py`. Only if it comes back untagged: have the user do one manual export (File › Export To › PDF › *Accessibility: On*, never Print) and, if that option is absent, update Keynote from the App Store.
2. **Audit**: `verify_pdf.py /tmp/DECK.pdf`. The Figures table now shows each Figure tag's *content*: `IMAGE …`, `vector(...)`, or `empty`. Keynote emits several **empty** Figure tags per slide for theme placeholders — those are decorative by construction; `--fix --decorative-nonimage` handles them all at once. Only `IMAGE` figures need a human decision.
3. **Extract images in slide order**: `verify_pdf.py /tmp/DECK.pdf --extract-images /tmp/imgs`. A theme image (e.g. the Berkeley seal) repeats on every slide with the same byte size — classify it once as decorative. Read each remaining image with the Read tool. For every image decide:
   - *decorative* (logo, banner, stock art, visual that only repeats slide text) → give it a two-word label ("Cal logo", "decorative banner"). **Ally scores an empty description as missing**, so never leave a real image's description blank; only non-image placeholder tags get empty alt (`--decorative-nonimage`);
   - *meaningful* → draft alt text: 1–2 sentences, ≤ ~125 characters, lead with the content, convey the point the slide is making with it, don't repeat the caption;
   - *contains text* (screenshot of a statute, contract clause, case excerpt, table) → **transcribe the passage in full** as the description, and if it is short (a sentence or two) recommend replacing the screenshot with live text on the slide instead. Legal decks are full of these; they are the highest-value fix.
   Also note any image whose fine print is illegible at PDF resolution — offer `keynote_tools.py images DECK.key DIR` to read the originals.
4. **Present a review table** — slide | figure index | content | classification | proposed description. If the user asked for the PDF *now*, don't block on approval: produce it via step 6 immediately, show the table, and offer to re-run with edits (a re-run takes seconds).
5. **Make it permanent in Keynote** (user does this; give exact clicks): open the deck (`keynote_tools.py open`), select each image › Format sidebar › *Image* › *Accessibility Description* › paste. Text-screenshots the user chose to replace become a text box. Save. This step is what survives future edits of the deck; the injection in step 6 has to be redone after every re-export.
6. **Produce the PDF**: write the approved descriptions to `alt.json` keyed by figure index (short label like `"Cal logo"` for decorative images — never `""` on an image, Ally counts that as missing), then
   `verify_pdf.py /tmp/DECK.pdf --fix --title "<Course — Class N: Topic>" --lang en-US --alt alt.json --decorative-nonimage --out "<PDF_Slides>/<Course>_ClassNN_<Topic>.pdf"`.
   Title is what a student would recognize, not the filename.
7. **Verify** (below) — the `--fix` run re-audits its own output; the last line must be READY TO POST.

## Lane 2 — Word document

1. `audit_docx.py FILE.docx`. Walk the user through fixing the issues in Word: apply Heading styles (no skipped levels), convert typed bullets to real lists, right-click images › *View Alt Text* (mark decorative where appropriate), rewrite bare-URL/"click here" links, mark table header rows (Table Layout › Repeat Header Rows), un-merge cells. Run Word's own checker (Review › Check Accessibility) as a last pass.
2. Export: File › Save As › PDF › **"Best for electronic distribution and accessibility"** on Mac (Options › "Document structure tags" on Windows). Never Print to PDF.
3. **Verify** (below).

For a Word file that is a *reading* (an excerpt, a case), first ask whether a licensed Library copy or a bCourses Page would serve — RTL ranks both above any PDF.

## Lane 3 — bare PDF, no source

1. `verify_pdf.py FILE.pdf`. Read the verdict:
   - **image-only pages** → it needs OCR + tagging that this machine can't do locally. Give the user the SensusAccess recipe (upload › Accessibility Conversion › *PDF – tagged PDF (image over text)* › email) and ask them to bring the result back for verification. If they'd rather, Acrobat's *Scan & OCR › Recognize Text* then *Prepare for Accessibility › Autotag* does the same locally.
   - **untagged but real text** → Acrobat: All Tools › Prepare for Accessibility › *Automatically tag PDF*, then *Check for Accessibility*. Bring it back.
   - **tagged** → proceed to fixes.
2. Draft alt text for figures exactly as in Lane 1 step 3–4 (extract images, review table).
3. `verify_pdf.py FILE.pdf --fix --title "<descriptive title>" --lang en-US --alt alt.json` — writes `FILE_a11y.pdf`. Title should be what a student would recognize ("Contracts — Class 3: Consideration"), not the filename.
4. Anything the script reports it can't fix (reading order, missing headings, untagged links) → point to the specific Acrobat tool, then re-verify.

## Verify (every lane ends here)

Run `verify_pdf.py OUT.pdf`. Report to the user in plain language:
- the verdict line (READY TO POST / NOT READY),
- each failed check and the one action that fixes it,
- advisories separately (they don't block posting).

If READY, close with the posting hygiene from the reference: upload, check the Ally meter, and if any file in the module is still unremediated, restrict access to it and keep the syllabus note inviting students to report barriers. Suggest a descriptive filename (`Contracts_Class03_Consideration.pdf`) if the current one is cryptic.

## Guardrails

- Never claim a file is accessible on the basis of appearance; only the verify step decides.
- Don't generate alt text without looking at the image; don't invent content in a text-screenshot transcription — if a word is illegible, say `[illegible]` and flag it.
- If drafting alt text would require sending student data or exam content to an external service, keep it local (Read the image directly); the RTL guide's Gemini path is optional and requires the CalNet account, not a personal one.
- Only run the AppleScript export after the user has done one manual export with Accessibility: On this session; otherwise the setting state is unknown.
- One file per run. If handed a folder, list it and ask which file to start with; RTL's triage order is: essential readings first, first-few-weeks first.
