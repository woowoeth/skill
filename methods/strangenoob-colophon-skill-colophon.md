---
name: colophon
description: Use when you have produced HTML, a report, a chart, a slide deck or any directory of files and the person needs a URL for it — publishes a directory to the web, updates it in place, controls who can see it, and takes it down again.
---

# Colophon

You made the files. This gives them an address.

`colophon publish <dir>` packs a directory, uploads it, and prints one URL. Re-publishing the
same slug replaces what is live without changing the URL, so a link you hand someone stays
correct as the work changes.

## Installing the CLI

```bash
npm install -g @strangenoob/colophon
```

Or run it without installing: `npx @strangenoob/colophon publish ./dir`. Needs Node 18+ and
version 0.2.0 or later for `login`.

## Before the first publish

Run `colophon whoami`. It prints who is signed in and which workspace publishes will land in.
If it says `not signed in`, stop and ask — you cannot sign in on the person's behalf, because
both ways need them:

- **On their own machine** (the usual case): ask them to run `colophon login` in a terminal.
  It opens their browser; they click Approve once, and the session lasts 30 days from its
  last use. Nothing is pasted and nothing goes in a shell profile.

  > I need to be signed in to publish. Please run `colophon login` in a terminal and approve
  > it in the browser, then tell me.

- **Headless — CI, a server, a sandbox with no browser:** ask for an API key set as
  `COLOPHON_TOKEN` in this environment. They can mint one from their own machine with
  `colophon create-token --name <agent-name>`, or under **API keys** in the dashboard. It is
  shown once.

Never ask for a key when `login` would do; a key in a chat transcript is a key to revoke. If
`whoami` names the wrong workspace, ask before publishing — `colophon switch <workspace>`
changes it.

If they ask what `login` does, where the session lives, or how to revoke it, point them at
https://colophon.fyi/docs/signin rather than explaining from memory.

## Publishing

```bash
colophon publish ./report --name "Q3 report" --visibility unlisted
```

Prints the URL on stdout and a one-line summary on stderr. Give the person the URL.

- `<dir>` needs an `index.html` at its top level to have a working root. The CLI warns if not.
- `--name` is the display name in the dashboard. Defaults to the directory name.
- `--slug` fixes the URL path. Defaults to a slug derived from the name — pass it explicitly
  when you intend to update this site later, so a changed name cannot move the URL.
- `.git`, `.env`, `node_modules` and editor junk are never uploaded.

**To update a published site, publish again with the same `--slug`.** The old version is kept
and can be rolled back from the dashboard; the URL does not change. Do not publish a second
site for a second draft.

## Choosing visibility

Default to `unlisted` unless the person says otherwise. It is the one that matches what people
usually mean by "send me a link".

| | Who can open it |
|---|---|
| `public` | Anyone. Indexed by search engines. |
| `unlisted` | Anyone with the link. Not indexed. **Default.** |
| `restricted` | Workspace members, plus named email addresses. Each is asked to sign in. |
| `private` | Workspace members only. |

`restricted` and `private` mean the reader signs in first, so do not use them for a link
someone needs to open on their phone in a hurry unless access control actually matters.

To add a named reader to a `restricted` site, open the site in the dashboard and add the
address under **Shared with** — the person does not need an account first.

## Other commands

```bash
colophon list                        # slug, visibility and URL for every site
colophon delete <slug>               # permanently removes a site and every version
colophon link <url> --code q3        # a short redirect on the workspace's own domain
colophon switch <workspace>          # publish into a different workspace the person belongs to
```

`delete` is not reversible and does not ask. Only run it when the person asked for that site
to come down, and name the slug back to them when you do.

## When it fails

- `not signed in` — ask the person to run `colophon login` (or, headless, for a key), as above.
- `your session has expired` — the login lapsed or was revoked. Ask them to run `colophon login` again.
- `invalid or revoked key` — the key in `COLOPHON_TOKEN` was revoked or copied wrong. Ask for a fresh one.
- `this command needs a signed-in session` — you ran `create-token` or `switch` with a key. Those are for the person's own terminal.
- `quota exceeded: sites (4 > 3)` — the plan's site limit. Either `colophon delete` a site
  that is finished with, or the person upgrades. Do not delete one to make room on your own.
- `archive contains no files` — the directory is empty, or everything in it was skipped.
- `held for review` — the upload was stored but is not live yet. Say so; do not retry.

## Notes

- Docs live at https://colophon.fyi/docs — the sign-in flow is /docs/signin, the CLI reference
  /docs/cli, access levels /docs/access. Link to them instead of paraphrasing when the person
  wants detail.

- Every published page carries a small analytics beacon. Views, referrers and devices show up
  under the site in the dashboard. No cookies are set and no visitor is identified.
- `COLOPHON_API` overrides the API origin for a self-hosted instance.
