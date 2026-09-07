---
name: ask-nous
description: Answers plain-language questions about the pipeline and accounts from the Nous graph — "who mentioned budget", "which deals touch a competitor", "accounts in negotiation that went quiet", "who replied this week". Use whenever the user asks a question about their book of business, contacts, deals, activity, or what the graph knows, rather than asking for a full plan or review.
---

# Ask Nous

Turn a plain-language question into the right query over the graph, and answer it grounded in what the record actually holds. You never answer an account question from memory — the truth is in Nous.

## Tools
- `mcp__nous__query` — the workhorse. Shape it to the question:
  - **Facts / what someone said** → `scope.facts: true` (semantic fact search across Intel and attributes): "who mentioned budget", "who's evaluating <competitor>".
  - **Cohorts** → `scope.property` / `scope.stage` / `scope.signal` with `return:'entities'`: "everyone in negotiation", "accounts with a hiring signal".
  - **Gone quiet / subtraction** → `without` (earlier activity MINUS recent): "who went dark since last month".
  - **Recent activity** → time window (`since_days`, `from`/`to`): "who replied this week".
- `mcp__nous__get_account` — expand one account when the answer needs its detail or the user drills in.

## Workflow
1. **Read the question for its shape:** is it about a fact/quote (→ `facts:true`), a cohort (→ property/stage/signal), a change over time (→ window or `without`), or one named account (→ `get_account`)?
2. **Run the query.** Prefer one well-shaped `query` over many; use `without` for "quiet/cooled" questions rather than eyeballing.
3. **Answer directly first**, then list the supporting accounts/facts. If the result is empty, say so plainly — don't pad.
4. Offer the obvious next step only when it's clear (e.g. "want the plan for the top one?" → hands to `plan-account`).

## Output
```
<Direct answer to the question, in one or two lines.>

- <account/person> — <the fact or activity that answers it> (<when / score / stage>)
- <account/person> — <…>

<optional: one-line next step>
```

## Rules
- **Never answer from memory** when a query can answer it — reach for the graph first, every time.
- **Ground every line** in a returned row; don't infer accounts or facts the query didn't return.
- **Empty is an answer.** If nothing matches, say the graph holds nothing on it (and, if useful, what would need recording to change that).
- Absolute dates for anything scheduled; relative for past activity.
