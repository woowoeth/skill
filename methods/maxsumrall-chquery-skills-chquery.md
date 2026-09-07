---
name: chquery
description: Uses chquery.com to explain or visualize a ClickHouse query and return a redacted query plan link. Use when the user mentions chquery, says "explain/visualize this ClickHouse query", or asks for a ClickHouse query plan.
license: MIT
compatibility: Requires Node.js 20 or newer. Analysis runs locally without network access.
---

# CH Query

Turn ClickHouse query evidence into a CH Query report and redacted link for the user.

1. Fetch and follow `https://chquery.com/llms-full.txt` for the current collection SQL, bundle schema, privacy rules, and fallbacks.
2. Run the collection SQL only through the ClickHouse connection the user has already provided. CH Query itself never connects to the database.
3. Build a version 1 bundle locally. Do not collect row data, users, hostnames, or credentials.
4. From this skill directory, run `node scripts/chquery.mjs analyze bundle.json --link`. The bundled CLI and settings catalog are self-contained, use no dependencies, and make no network requests during analysis. After npm publication, `npx chquery analyze bundle.json --link` will be equivalent.
5. Show the redaction summary, then include the complete markdown report and link in your reply. If the link is about 16 KB or larger, warn that it may be truncated and return the redacted bundle as a file instead.

Never create or send an unredacted link without asking the user first. Database, table, and column identifiers are not pseudonymized by the bundled redactor; review that with the user when identifiers may be sensitive.
