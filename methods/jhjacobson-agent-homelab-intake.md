---
name: intake
description: Turn a rough idea for a new AWS site into an approved, written project brief (~/aws/<name>/BRIEF.md) that /scaffold-aws can provision from with no conversation context.
user-invocable: true
argument-hint: <rough description of the site>
---

# Intake

`$ARGUMENTS` is the user's rough description of a new site. Produce an approved brief at
`~/aws/<name>/BRIEF.md`. This skill writes **only that file** — no repo, no todolist, no
AWS. The scaffold reads the brief; the sprint reads the todolist and the code. Nothing in
this conversation survives, so everything the later steps need goes in the brief.

## Defaults (apply unless the description says otherwise)

| Setting | Default |
|---|---|
| Prod URL | `https://<name>.districtjosh.com` |
| Test URL | `https://<name>-test.districtjosh.com` |
| Dev URL | `http://dev.<name>.home` |
| Buckets | `<name>-test-site`, `<name>-site` |
| RUM | shared districtjosh app (`rum: "shared"`) — because it is a hub subdomain |
| Shape | static site, Vite + TypeScript + vitest, S3 + CloudFront, no API, no auth |
| Environments brought up by the scaffold | test and prod |
| Gitea | `aws/<name>`, private |

A site on its own registrable domain sets `fqdn_*` accordingly and `rum: "own"` (needs a
`homelab/<name>-rum` 1Password item — say so in the brief). Ask about hosting only when
the description mentions another domain or is ambiguous about it.

## Step 1: Ground yourself

Read `~/CLAUDE.md` and `~/aws/CLAUDE.md` (project structure, infra pattern, RUM rule,
cost guardrails, anti-fabrication). Skim one recent brief under `~/aws/*/BRIEF.md` if any
exist, for tone and size.

## Step 2: Pick a name and check collisions

Kebab-case, short, no underscores. Check all three namespaces before proposing it:

```bash
ls ~/aws/ | grep -i "<candidate>"
curl -s -o /dev/null -w '%{http_code}\n' "http://git.home/api/v1/repos/aws/<candidate>" -H "Authorization: token $(cat ~/.gitea-token)"   # want 404
curl -s "http://todolist.home/api/v1/projects?include_archived=true" -H "X-API-Key: $(cat ~/.todolist-key)" | jq -r '.data[].name' | grep -i "<candidate>"
```

## Step 3: Ask only what changes the scaffold

One `AskUserQuestion` round, at most 5 questions, each with a recommended default first.
Candidates — drop any the description already answers:

1. **Name** — your proposal plus one or two alternatives.
2. **Data sources** — what the site shows and where it comes from (URL, API, dataset,
   PDF, hand-maintained JSON). Needed for the anti-fabrication rule.
3. **API needed?** — does anything require a Lambda (form submission, auth, live
   fetch that can't be done at build time)? Default no.
4. **Auth?** — default none.
5. **First milestone** — what has to be true for the first deploy to be worth showing
   someone.

Do not ask about hosting, buckets, RUM, environments, or stack unless a default is in
doubt. Do not ask more than one round unless an answer contradicts another.

## Step 4: Write the brief

Create `~/aws/<name>/` and write `BRIEF.md` in exactly this shape. The two fenced JSON
blocks are machine-read by the scaffold (`json scaffold-config`, `json scaffold-tasks`);
keep the info strings verbatim.

````markdown
# <Title> (`<name>`) — project brief

Status: DRAFT

## Goal
One paragraph: what the site is, for whom, and the one thing a visitor should be able to do.

## Audience
Who uses it and how they arrive (link from the hub, search, shared URL).

## Hosting and domains
| Env | URL | Storage |
|---|---|---|
| dev | http://dev.<name>.home | Docker, live reload |
| test | https://<name>-test.districtjosh.com | S3 `<name>-test-site` + CloudFront |
| prod | https://<name>.districtjosh.com | S3 `<name>-site` + CloudFront |

RUM: shared districtjosh application, service `<name>`.

## Shape and stack
Static Vite + TypeScript multi-page site (one HTML entry per real page), vitest, S3 +
CloudFront, deployed by Gitea Actions on merge. <Add Lambda/API/auth here only if needed,
and say what the scaffold should NOT build so the sprint does it.>

## Data sources
For each source: what it is, the exact URL or path, how it is fetched (build-time script,
committed JSON, runtime fetch), update cadence, license/attribution. **If a source cannot
be obtained deterministically, the task that needs it must stop and report — never
synthesize it.**

## Non-goals
What this site deliberately does not do (keeps the sprint from expanding scope).

## Milestone 1
The smallest version worth deploying. Everything P1 below adds up to exactly this.

## Approval
Approving this brief authorizes `/scaffold-aws` to run unattended: create the Gitea repo
and todolist project, add and reload the dev nginx server block, and create the AWS
resources for every environment listed below (S3 buckets, CloudFront distributions, ACM
certificate use, Route 53 records) via the Gitea runner. No further confirmation is asked.

## Scaffold config
```json scaffold-config
{
  "name": "<name>",
  "title": "<Title>",
  "goal": "<one sentence, used in README>",
  "fqdn_test": "<name>-test.districtjosh.com",
  "fqdn_prod": "<name>.districtjosh.com",
  "bucket_test": "<name>-test-site",
  "bucket_prod": "<name>-site",
  "rum": "shared",
  "environments": ["test", "prod"],
  "api": false
}
```

## Tasks
```json scaffold-tasks
[
  {
    "title": "<imperative, specific>",
    "priority": 1,
    "description": "<what and why, 1-3 sentences>\n\nAcceptance criteria:\n- <observable, testable>\n- <...>\n\nSource/inputs: <exact source or 'none'>"
  }
]
```
````

Task-writing rules:
- **P1** = required for Milestone 1. **P2** = next. **P3** = nice to have. `/sprint`
  pulls P1 and P2 automatically.
- Each task is one developer-agent unit of work: one feature, 2–5 acceptance criteria a
  tester can check without asking anyone, and the named input it depends on.
- Do **not** list what the scaffold already delivers (repo, CI, deploy pipeline, RUM,
  infra, placeholder home page, nginx). The first P1 task is usually "Replace the
  placeholder home page with <the real thing>".
- Include a P1 task for each data source's fetch/ingest step when one exists, with the
  deterministic way to obtain the data spelled out.
- Aim for 5–12 tasks. More than that means the milestone is too big.

## Step 5: Review loop

Show the user the brief (the file contents, not a summary) and ask for approval or
edits. Apply edits and show it again. Loop until they approve. Do not create anything
outside `BRIEF.md`.

## Step 6: Approve and hand off

When asking for approval, say in one sentence what it authorizes (the brief's Approval
section): the scaffold will run unattended, create the Gitea repo and todolist project,
add and reload the dev nginx block, and create the AWS resources for every listed
environment via the Gitea runner. No further confirmation is asked after this.

On approval, replace `Status: DRAFT` with `Approved: YYYY-MM-DD` (today's date), say
"Brief approved — scaffolding now", and **immediately invoke the `scaffold-aws` skill
with `<name>` as its argument in this same session** (Skill tool). Do not print a
command for the user to run and do not wait for another message: the approval was the
go-ahead for the whole flow. The scaffold's own handoff (`Run /clear, then: ...`) is the
only thing the user needs to act on, because clearing context is the one step Claude
cannot do itself.

## Common mistakes to avoid

- Asking for approval without saying what it authorizes. The scaffold never asks again.
- Stopping after approval and telling the user to run `/scaffold-aws`. Invoke it
  yourself; the user should only ever type `/intake` and, at the end, `/clear` + `/sprint`.
- Asking about things the defaults already settle. The user set the districtjosh
  default on purpose; one round of questions, then write.
- Tasks that describe implementation ("add a React component") instead of outcome
  ("visitor sees X"). Agents pick the implementation.
- Putting facts in the chat but not the brief. The scaffold and the sprint never see
  this conversation.
- Editing the JSON blocks' info strings. `json scaffold-config` and `json scaffold-tasks`
  are what the scaffold's awk looks for.
