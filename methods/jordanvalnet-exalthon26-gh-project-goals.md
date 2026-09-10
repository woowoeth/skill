---
name: gh-project-goals
description: Writes the OPTIMIZATION paragraph of a non-technical GitHub onboarding report: what the project seeks to optimize (time, money, speed, quality, reliability…) and for whom, separating stated goals from interpretation, from facts.goals collected through the GitHub MCP. Used by /onboard-project.
allowed-tools: Bash(bun run:*), Bash(~/.bun/bin/bun run:*), Read
---

# gh-project-goals — What does it seek to optimize?

Single responsibility: write **only** this section of the onboarding report, for a reader with **no
technical background**. Input: `facts.json` from `onboarding-facts` (key `goals`), or run
`bun run onboarding/src/cli.ts goals <owner>/<repo>` to get the same JSON standalone (use `~/.bun/bin/bun` if `bun` is not on PATH).

Rules: every sentence traces to a fact in the JSON (`facts`), sources are listed in `sources`,
anything missing is in `gaps` and stays a gap ("The documentation does not say." / "Not reachable
through the GitHub MCP tools" + URL). No code, no file paths in prose, gloss any technical word,
short sentences. Label interpretation as "our reading". Never fetch outside the GitHub MCP (see
`github-mcp-access`).

## What to write
- From `goalSections` and `optimizationExcerpts`: what is optimized, for whom, quoted when possible → label **stated**.
- From `vocabulary` (word counts): a cautious one-line reading of the emphasis → label **our reading**.
- If both are empty: **'The documentation does not state what the project optimizes.'**

## Output
The Markdown of this section only (heading included), replacing the matching ✍️ placeholder of
`skeleton.md`. Keep the factual tables the skeleton already contains.
