---
name: publish-to-wiki
description: Publish a markdown research or analysis file to the home Wiki.js (homelab/wiki-content) under research/, where it renders at wiki.home for review. Use when a research report, analysis, or long-form markdown file has been written on the homelab and should go to the wiki. Also follow the proactive-offer behavior below after writing any such file.
user-invocable: true
argument-hint: <path-to-markdown-file> [slug] [--draft]
---

# Publish to Home Wiki

Pushes a markdown file to the home **Wiki.js** so the user can read and review it
at `http://wiki.home/research/<slug>`. The wiki's content lives in the Git repo
**`homelab/wiki-content`**; Wiki.js pulls that repo on a **~5-minute Git sync
interval** and renders any new page. This skill writes the file (with Wiki.js
front-matter) into `research/<slug>.md`, pushes to `main`, and waits for it to render.

See `~/containers/wiki/README.md` for the full wiki architecture.

## When to use it

- The user asks to put a research file / report / analysis on the wiki.
- **Proactively:** right after writing a substantive research or analysis markdown
  file anywhere on the homelab (e.g. a `/deep-research` report, an investigation
  write-up), offer to publish it: *"Want me to push this to the wiki for review?"*
  Don't auto-push without asking, and don't offer for code, configs, READMEs, or
  scratch notes — only reader-facing research/analysis prose.

## How to run it

```bash
bash ~/.claude/skills/publish-to-wiki/publish.sh <file.md> [slug] [--draft]
WIKI_SECTION=household bash ~/.claude/skills/publish-to-wiki/publish.sh <file.md> [slug]
```

The script:
1. Derives a URL **slug** from the filename (or uses the one you pass).
2. Ensures the file has **Wiki.js front-matter**. If the file already begins with a
   `---` block, it is trusted as-is. Otherwise a minimal block is generated (title
   from the first `# H1`, `published: true`, `tags: research`).
3. **Validates** the front-matter YAML parses (catches the classic unquoted-colon-in-title bug).
4. **Copies local images** into `research/<slug>/` and rewrites the markdown links to
   absolute wiki paths (`![x](charts/a.png)` → `![x](/research/<slug>/a.png)`). This is
   automatic — do not move images yourself. Absolute URLs, `/`-rooted paths and `data:`
   URIs are left alone; a missing image logs a warning and its link is left untouched.
5. Clones/refreshes `homelab/wiki-content`, writes `research/<slug>.md` plus any images,
   commits, and pushes to `main` (the branch Wiki.js syncs bidirectionally — not protected).
6. Polls `http://wiki.home/research/<slug>` for up to ~6 min **waiting for HTTP 200**, then
   checks each image also returns 200. Exits non-zero if the page never renders.

It is **idempotent** — re-running on an unchanged file reports "already up to date".

**Never report a page as published without a 200.** The poll checks the HTTP status code
for exactly this reason: a Wiki.js 404 still returns a full HTML page, so a body-content
heuristic (e.g. grepping for "does not exist") will happily declare a 404'd page LIVE —
which is how this script once reported success on a page that wasn't there. If you verify
by hand, use `curl -s -o /dev/null -w '%{http_code}' -L <url>`; if it 404s, check a
known-good page (e.g. `/research/dc-2022-precinct-map`) to tell a slow git sync (yours
404s, theirs 200s) apart from an access problem (both 404).

## Preferred workflow (best results)

For a polished page, write the front-matter yourself before calling the script, so
the title, description, and tags are good — the script will trust and validate it:

```markdown
---
title: "A Clear, Specific Title"          # QUOTE the title if it contains a colon
description: One-sentence summary for the wiki list and search.
published: true
date: 2026-06-25T00:00:00.000Z
tags: research, dc-policy, topic-here
editor: markdown
dateCreated: 2026-06-25T00:00:00.000Z
---

# A Clear, Specific Title
...body...
```

Conventions:
- **Section:** defaults to `research/`. Override with the `WIKI_SECTION` env var when the
  page clearly belongs elsewhere: `WIKI_SECTION=household bash publish.sh <file.md> <slug>`.
  Existing sections: `research/` (reports and analysis), `guides/` (how-tos),
  `household/` (house systems and chores). Pick the one a reader would browse to;
  when in doubt use `research/`. Add a link from that section's index page so the
  new page is reachable.
- **State:** `published: true` (live) by default. Use `--draft` (or `published: false`)
  only when the user wants a hidden draft they'll flip live in the UI.
- **Title with a colon** must be quoted, or Wiki.js's YAML parser breaks. The script
  quotes auto-generated titles; quote your own when you hand-write the block.
- Do **not** write under `synced/` — that tree is a read-only mirror of repo docs.

## Troubleshooting

- **"This page does not exist yet" right after pushing** — normal. Wiki.js only pulls
  every ~5 min. Wait for the next cycle, or have the user click **Administration →
  Storage → Git → Force Sync** in the wiki admin UI (that button is behind admin auth;
  the model cannot trigger it). A `docker compose restart wiki` also forces a sync on
  boot but briefly takes the wiki offline — ask first, it's shared infra.
- **Push rejected** — check the Gitea token at `/home/homelab/.gitea-token`. Unlike
  project repos, `wiki-content`'s `main` is *not* branch-protected (Wiki.js pushes
  browser edits straight to it), so direct pushes are expected here.
