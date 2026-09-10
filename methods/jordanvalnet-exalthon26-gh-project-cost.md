---
name: gh-project-cost
description: Writes the COST rows of a non-technical GitHub onboarding report: price for users, running/infrastructure cost, funding and sponsors, documented development effort — strictly from what the documentation says (facts.cost via the GitHub MCP); writes 'Not documented' otherwise. Used by /onboard-project.
allowed-tools: Bash(bun run:*), Bash(~/.bun/bin/bun run:*), Read
---

# gh-project-cost — What does it cost?

Single responsibility: write **only** this section of the onboarding report, for a reader with **no
technical background**. Input: `facts.json` from `onboarding-facts` (key `cost`), or run
`bun run onboarding/src/cli.ts cost <owner>/<repo>` to get the same JSON standalone (use `~/.bun/bin/bun` if `bun` is not on PATH).

Rules: every sentence traces to a fact in the JSON (`facts`), sources are listed in `sources`,
anything missing is in `gaps` and stays a gap ("The documentation does not say." / "Not reachable
through the GitHub MCP tools" + URL). No code, no file paths in prose, gloss any technical word,
short sentences. Label interpretation as "our reading". Never fetch outside the GitHub MCP (see
`github-mcp-access`).

## What to write
- Fill the four rows of the skeleton table: **Price for users** (`pricingSections`, `priceExcerpts`, license → 'free to use, open source' only if the license says so), **Running / infrastructure cost** (`runningCostExcerpts`), **Funding & sponsors** (`fundingFile`, `fundingExcerpts`), **Development effort** (`effortExcerpts`, documented only).
- Each excerpt carries `matched` (the word that triggered it): if the match is irrelevant (e.g. "hackathon" in a title), ignore the excerpt and say "Not documented".
- Each row: one or two sentences + the source file. Quote numbers exactly as written in the docs.
- Empty evidence → **'Not documented.'** No estimates, no market knowledge, no guesses about cloud bills or salaries. `codeSearchHits` only tells you which files to read further with `mcp__github__get_file_contents` if a hit looks relevant.

## Output
The Markdown of this section only (heading included), replacing the matching ✍️ placeholder of
`skeleton.md`. Keep the factual tables the skeleton already contains.
