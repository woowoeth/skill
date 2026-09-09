---
name: docs-lookup
description: Fetch focused, current library documentation through the context7 REST API from the terminal, no key or MCP needed. Use when an API surface is uncertain, a call fails against the installed version, or a library is unfamiliar. Not for general questions the model already answers.
---

# Docs lookup

Current docs for a library, on demand, two commands. Read the error first; fetch docs second.

## Commands

```bash
bash .agent/skills/docs-lookup/scripts/docs.sh search <library>                      # library ids, e.g. /pallets/flask, /expressjs/express
bash .agent/skills/docs-lookup/scripts/docs.sh get <library-id> <topic> [tokens]     # focused snippets for that topic, default 2500 tokens
```

Example: `docs.sh search flask` → `/pallets/flask`; then `docs.sh get /pallets/flask "error handling" 1500`.

## Rules

- One docs call per problem. If the answer is not in the first fetch, narrow the topic once, then stop and ask.
- Prefer the official repo id (`/owner/repo`) over `/websites/...` mirrors.
- Quote the snippet you relied on in one line when you use it, so the reasoning is visible.
- Verify against the installed version (`pip show`, `npm ls`) when the docs and the code disagree; the installed version wins.
- Never fetch docs for things the installed code already shows: read the existing code first.
