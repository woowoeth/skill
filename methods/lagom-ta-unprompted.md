---
name: unprompted
description: Analyze the user's own local Claude Code / Codex session history and show who they are on different projects — two contrasting modes, what they never say, the moments that contradict each other, and a playful MBTI-style AI-use persona with a bespoke card. Use when the user asks about their own AI-use patterns, prompting habits, "what do my sessions say about me", their AI-use personality or MBTI, or asks for an Unprompted report. Analysis runs entirely on their machine; no network calls unless they explicitly ask for LLM naming.
---

# Unprompted

Reads `~/.claude/projects` and `~/.codex/sessions`, runs a purely statistical
analysis, and writes a self-contained HTML report to the user's machine.

The insight is comparative, not a score: the same person is measurably a
different collaborator on different projects. The report contrasts two poles
(project × day), names what is conspicuously absent, and points at moments that
contradict each other.

On top of the report sits one playful layer: `persona` compresses the same
measured rates into a four-letter MBTI-style AI-use type — a parody that says
so — and you turn it into a write-up and a bespoke HTML card.

## Run it

```bash
node bin/unprompted.mjs scan      # pass 1: what's there. No analysis.
node bin/unprompted.mjs report    # pass 2: analyze + write HTML
node bin/unprompted.mjs persona   # same corpus, one four-letter parody type
```

`bin/unprompted.mjs` sits next to this file. Node ≥ 20.19, zero dependencies —
nothing to install. If a relative path fails, use the absolute skill directory
(commonly `~/.claude/skills/unprompted/bin/unprompted.mjs`, or
`~/.agents/skills/unprompted/bin/unprompted.mjs` under Codex).

## Workflow

1. **Scan first.** Run `scan` and show the user the project list and counts.
   They should recognize themselves in the numbers before anything is analyzed —
   if the row for their main project says 12 utterances, something is wrong with
   the read, not with them.
2. **Settle the scope before analyzing.** If the user already named a project —
   or clearly asked for everything — respect that and don't re-ask. Otherwise
   ask exactly one question: analyze **all projects**, or **one specific
   project**? Offer the scanned project names (top few by utterance count) as
   the choices. Project names are last path segments like `TextBook`; match
   what the user says against the scan list case-insensitively and by
   substring, and if it's ambiguous, show the candidates instead of guessing.
   Whatever they pick, carry the same `--project` / `--from` / `--to` flags
   through every command that follows.
3. **Report.** Run `report --open` to write the HTML and open it in their
   browser. Relay the digest that the command prints.
4. **Persona.** Run `persona` with the same scope flags. Then retell it in the
   conversation's language (see Language below): keep the four-letter code as
   printed, translate the type name and essence faithfully, and make the
   write-up genuinely fun — but every claim must point at a number from the
   command's output. The letters are nicknames for measured rates; say so in
   the write-up. A flat axis is told as "no signal", never as a trait.
   `insufficient` gets the same honesty as an `empty` report: not enough to
   type, full stop — don't pad it.
5. **The persona card.** When the user wants the persona (they asked for it, or
   said yes to the offer), hand-write a bespoke self-contained HTML card and
   save it to `~/.unprompted/persona-<YYYY-MM-DD-HHMMSS>.html`, then offer to
   open it. Design it fresh every run — palette, motif and layout keyed to the
   type and its numbers, so no two people (and no two scopes) get the same
   card. Hard constraints, restated in `references/persona.md`:
   - Self-contained like the report: everything inline, no CDN, no web fonts,
     no remote images, no `<script>`. It must render complete offline.
   - Contents are the persona only: the code, translated name and essence, the
     four axes with their real percentages and rates, your narrative lines.
     Nothing else from the sessions — no verbatim quotes, no timestamps, no
     file paths, no session IDs.
   - Written in the conversation's language.
6. **Read the tier honestly.** `full` / `noPoles` / `sparse` / `empty` are all
   valid outcomes. `empty` is not an error — say plainly that there wasn't
   enough to work with and stop. Do not pad a thin report into a thick one.
7. **Naming is opt-in.** Only if the user asks for LLM-generated names: run
   `naming-payload`, show them the exact JSON, and send it only after they say
   yes. Details in `references/naming.md`.

## Language

Adapt to the conversation, not to the tool. The CLI prints English labels and
numbers; everything **you** produce on top of it — the digest retelling, the
persona write-up, the persona card — is written in the language the user is
speaking with you. English question → English write-up and English card;
Chinese question → Chinese write-up and Chinese card; any other language →
translate the type name and essence faithfully instead of inventing a new
archetype. The four-letter code, dimension ids and numbers stay exactly as
printed.

## Rules you must honor

- **Quotes stay in the file.** `report` deliberately prints no verbatim
  utterances. The HTML is local; your context is not. Pass `--quotes N` only
  when the user asks you to discuss specific things they said. `persona`
  prints no quotes at all, by construction.
- **Never put an API key in a flag or in a file.** `name` reads
  `UNPROMPTED_API_KEY` or `OPENAI_API_KEY` from the environment and refuses
  without `--confirm`. Do not work around either guard.
- **Don't copy session data anywhere.** No summaries into repo files, no
  pasting `~/.claude` contents into the conversation. The user's history stays
  where it is. The persona card carries only what `persona` printed.
- **Report what the analysis found, not what would be flattering.** The tone is
  observational and specific. The core report is not a personality test, not a
  diagnosis, and not therapy language. If the user asks "is this bad", the
  honest answer is that it's a description of behavior, not a verdict on them.
- **The persona is a parody and says so.** It compresses real measured rates
  into four letters for fun. Present it with its numbers, never as psychology,
  never as an assessment of ability or character. If the user asks whether to
  take it seriously: the numbers are real, the letters are a costume.
- Some content is filtered out before analysis and its removal is never
  quantified in the report. That is intentional. Don't reconstruct or report on
  what was filtered.

## Command reference

| Command | What it does |
| --- | --- |
| `scan` | Project list, utterance counts, date ranges, dropped-by-rule counts. |
| `report` | Analyze and write the HTML. `--open`, `--out <path>`, `--no-html`, `--quiet`, `--json`, `--quotes N`. |
| `persona` | Four measured axes → one four-letter parody type. Numbers only, no quotes. `--json`. |
| `naming-payload` | Print the exact bytes naming would send. Sends nothing. |
| `name` | Send one naming request. Needs `--confirm` and an env key. |

Scope flags for `report` / `persona` / `naming-payload`: `--project <name>`
(repeatable), `--from <YYYY-MM-DD>`, `--to <YYYY-MM-DD>`, `--exclude-recent-days`.
Source overrides: `--claude-dir`, `--codex-dir`, `--tz-offset <minutes>`.

`node bin/unprompted.mjs --help` prints all of it.

## Reference

- `references/report-tiers.md` — what each of the four tiers contains, and how
  to talk about a degraded one.
- `references/dimensions.md` — what the measured dimensions mean, so you can
  explain a gap without inventing a mechanism for it.
- `references/persona.md` — the persona axes, the sixteen types, the card
  constraints, and the tone rules for the parody layer.
- `references/naming.md` — the opt-in LLM naming flow and its guarantees.
- `references/privacy.md` — what is read, what leaves the machine, what never does.
