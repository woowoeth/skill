---
name: practitioner-bio
description: >-
  Interview a practitioner and save their English and German bio, portrait and profile links to
  the practitioners collection, shown at / and rendered on hackersandwizards.dev. Use for "create
  my bio", "practitioner bio", "my bio", "Biografie erstellen", "hilf mir eine Biografie zu
  erstellen", "add my profile links", "update my bio".
---

# Practitioner Bio

You interview a practitioner and save their introduction to `src/content/practitioners/<slug>/`:
`bio.md` (the frontmatter and the English text), `bio.de.md` (the German text, no frontmatter)
and `photo.webp`. The website renders the English page from the first file and the German page
from the second, so what you save is what a client reads.

## Mandatory and optional

Mandatory: **name, bio in English and German, LinkedIn URL, portrait**. Without all of them the
entry stays `status: draft` and you say what is missing.

Optional, asked once each, recorded only where the practitioner maintains it (a dead link is worse
than none): **Bluesky, X, Threads, Mastodon, GitHub, own website or blog, a public booking link**
(cal.com, Calendly; `bookme` in the schema).

Not here at all: role and group. Who appears on the website, in which section and with which
title is the website's roster, kept by Stefan and Bina. A wish to change it is flagged to Stefan,
never written into a file in this repo.

## Procedure

1. **Ask for the name**, then look for an existing directory under `src/content/practitioners/`.
   What is already there is not asked again; an existing entry is updated, not recreated. Keep
   frontmatter you did not collect.
2. **Collect the links**, mandatory and optional as above.
3. **Ask for the portrait**: a file path to a photo they like, roughly square, at least 480x480.
   Convert it to a 480x480 `photo.webp` in their directory.
4. **Interview for substance**, a few questions rather than a form: what they work on right now,
   the two or three stations or projects that shaped them, what they deliver with h&w, and one
   concrete thing that makes them memorable (a niche, a stack, a first).
5. **Draft the English bio**: 3 to 5 sentences, 100 to 2000 characters, third person. Short
   sentences, concrete nouns, real experience over adjectives. No buzzwords ("passionate",
   "expert", "seasoned", "transform"), no technology lists for their own sake, no dash used as
   punctuation. It should read like a colleague describing them, not like a CV.
6. **Show the draft and iterate.** Their reaction is the test; expect a round or two.
7. **Draft the German bio** from the approved English one: the same content in their own German,
   not a word-by-word translation. Show it; most practitioners will edit a phrase.
8. **Save** both files in the format below, then run `bun run dev` and show the result at
   http://localhost:4321 so they see what a client sees. Confirm the new sentences are on the
   page, not that the page loaded.
9. **Commit only after they say yes** to exactly what the commit contains. Name the three files
   on `git commit` itself; never `git add -A`. Then push to main: it is their own entry. Without
   write access, they ask Stefan or Bene for it.

## File format

`practitionerSchema` in `src/lib/schema.ts` is the authority; the shape today:

```markdown
---
name: <Full Name>
photo: ./photo.webp
linkedin: <url>
bluesky: <url> # optional fields only where a living profile exists
x: <url>
threads: <url>
mastodon: <url>
github: <url>
website: <url>
bookme: <url>
status: active # draft until name, both bios, LinkedIn and portrait are all real
owner: <Full Name>
updated: "2026-09-06" # quoted, or YAML makes it a Date and the schema rejects it
---

<The English bio.>
```

`bio.de.md` holds the German text and nothing else.

## Boundaries

- Name no client without public coverage of the work; describe the work instead.
- Role and group are the website's roster. Flag a wish, do not write it here.
