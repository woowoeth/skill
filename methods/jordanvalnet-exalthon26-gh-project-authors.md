---
name: gh-project-authors
description: Writes the WHO section of a non-technical GitHub onboarding report: owner, original author, current maintainers, number of contributors, license explained in plain words, from facts.authors collected through the GitHub MCP. Used by /onboard-project.
allowed-tools: Bash(bun run:*), Bash(~/.bun/bin/bun run:*), Read
---

# gh-project-authors — Who is behind it?

Single responsibility: write **only** this section of the onboarding report, for a reader with **no
technical background**. Input: `facts.json` from `onboarding-facts` (key `authors`), or run
`bun run onboarding/src/cli.ts authors <owner>/<repo>` to get the same JSON standalone (use `~/.bun/bin/bun` if `bun` is not on PATH).

Rules: every sentence traces to a fact in the JSON (`facts`), sources are listed in `sources`,
anything missing is in `gaps` and stays a gap ("The documentation does not say." / "Not reachable
through the GitHub MCP tools" + URL). No code, no file paths in prose, gloss any technical word,
short sentences. Label interpretation as "our reading". Never fetch outside the GitHub MCP (see
`github-mcp-access`).

## What to write
- Distinguish **owner** (`owner.login`, person vs organization), **earliest author seen** (`firstCommit`, say 'approximately' if `commitsSeen` hit the cap), **most active contributors** (`topCommitters`), **people with access** (`collaborators`, or 'not visible to this token').
- Use `authorshipFiles` and `licenseCopyright` when present; quote them.
- Explain the license in one everyday sentence (from facts.repository.license): 'free to reuse with attribution', 'open source, changes must be shared', 'no license file = all rights reserved by default'.
- Never print e-mail addresses.
- If `firstCommit.date` is earlier than the repository creation date (facts.repository.createdAt), say the history was imported from an earlier project — label it "our reading".
- **Also own §7.6 People**: who commits (`topCommitters`), who proposes changes (facts.pullRequests.authors), who opens tickets (facts.issues rows) — approximate, one short paragraph.

## Output
The Markdown of this section only (heading included), replacing the matching ✍️ placeholder of
`skeleton.md`. Keep the factual tables the skeleton already contains.
