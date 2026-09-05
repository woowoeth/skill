---
name: buena-graphs
description: Insert text-first graphs beside prose. Copy official plain-text twins from the buena-mono catalog for markdown, terminal, or chat output; install the React components from the registry for JSX/MDX hosts. Use when an explanation, report, README, PR body, or doc needs a chart, graph, sparkline, timeline, gantt, status strip, or any data figure - and instead of inventing ASCII art or reaching for Mermaid, SVG, or an image.
license: MIT
metadata:
  version: "1.0.0"
---

# buena-graphs

Thirty graph components with official plain-text twins, drawn on the
Buena Mono grid. The twins are ordinary characters in ordinary fenced
blocks: they read in a terminal, on GitHub, in chat — and renderers
that know [the frame contract](../../CONTRACT.md) upgrade them. The
characters are never invented; they are copied.

## Steps

1. **Pick the host.** Plain markdown, terminal output, chat, or a
   README → use a text twin (steps 2–3). A React/MDX codebase where
   components render → install from the registry (step 4).
2. **Pick the graph.** Open
   [`references/graphs.md`](references/graphs.md) — every component
   with its official twin, grouped by family (density, series,
   magnitude, structure, tabular, clock). Choose the smallest figure
   that makes the point; when nothing fits, compose inside the
   `Frame` contract rather than inventing new characters.
3. **Copy the twin verbatim, then swap only labels and values** —
   with real data, not illustrative numbers. Keep the `[ TITLE ]`
   line (caps), the blank line after it, the legend and axis lines,
   and the trailing summary sentence: renderers rely on that shape
   ([CONTRACT.md](../../CONTRACT.md)). Every character must come from
   the contract's inventory — the height ramp is `▁ ▂ ▃ ▅ ▇ █`, and
   glyphs outside the inventory (`▄`, `▆`, box art) make a figure
   renderers reject. The real numbers must be readable in the figure:
   as labels, an axis, or the summary line — a shape without its
   values is decoration.
4. **JSX/MDX hosts:** install a component into a shadcn-style project
   and render it with props instead of pasting characters:

   ```sh
   npx shadcn@latest add https://graphs.buenalabs.io/r/graph-uptime.json
   ```

   Any component from `r/` works the same way; `r/all.json` installs
   everything. Types, theming variables, and css utilities come with
   the install.
5. **Restraint** (adapted from
   [mdx-graphs](https://mdx-graphs.kshv.me/docs/skill)): at most two
   figures in a section, prose between them, each beside the text it
   supports — never a gallery. A figure earns its place only where
   structure beats sentences.

## Exit criteria

- Every figure is fenced plain text (or an installed component in a
  JSX host) — no Mermaid, SVG, images, or improvised ASCII.
- Data-graph characters match a catalog twin apart from labels and
  values; every character is in CONTRACT.md's inventory; the
  `[ TITLE ]` frame survives.
- The data's actual values are readable in the figure or its summary
  line.
- No section holds more than two figures.

## Troubleshooting

| Issue | Solution |
|---|---|
| Catalog URL returns 403 | Some fetch proxies are bot-blocked. Use the bundled [`references/graphs.md`](references/graphs.md); only `scripts/sync-catalog.sh` (curl) fetches live. |
| No component fits the data | Compose inside the `Frame` contract (first entry in the catalog); never invent a new grammar. |
| Figure wider than 80 columns | Leave it fenced — fences scroll, prose wraps. Do not reflow figure lines. |
| Renderer shows plain text only | Correct and expected: the twin *is* the content. Renderers that know CONTRACT.md (e.g. mrkdwn) upgrade it; nothing requires them to. |
| `shadcn add` fails on the raw URL | The repo may not be public yet, or the URL moved at launch — check the README for the current registry address. |
| Astro app with two JSX renderers | Typed targets put the component in `components/` and the frame in `components/ui/`, splitting one tree across renderer boundaries (symptom: "Unable to render GraphUptime!"). Move the graph component beside `graph-frame` so one renderer owns the whole tree. |
