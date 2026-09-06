---
name: applying-to-jobs
description: Use when applying to a job or internship, tailoring an application to a specific posting or job description, researching a company before applying, drafting answers to an application form, or writing a cover note, referral message, outreach comment or application video script.
---

# Applying to Jobs

Turn a posting into a researched brief and drafted answers. Facts come from
`profile.yml`. Nothing else goes in.

## The Iron Rule

**Every claim in every drafted answer must trace to `profile.yml`.** Not in the
profile, not in the application. A missing fact becomes a visible marker:

    [ASK: which of your projects had real users I can name here?]

An application is a promise you have to defend in an interview, to someone who
will check.

### Rationalizations: every one of these means STOP

| Excuse | Reality |
|---|---|
| "The JD wants 5 years, write equivalent experience" | You will be asked about years. Say what is true. |
| "Mirror their keywords into my history" | That is the JD writing your resume. Interviewers can tell. |
| "Everyone stretches in a cover letter" | Not the ones who get hired. |
| "The posting is enough, skip the product research" | The wedge is almost never in the posting. |
| "The gap is small, leave it out" | Naming a gap and saying what you would do about it reads stronger. |
| "They will not check the GitHub link" | Founders at small companies always check. |
| "Make it sound impressive" | Impressive comes from the real work. Ask for the missing fact. |

## Workflow

1. **Find `profile.yml`.** Look in the working directory, then ask. Without one,
   run the `writing-resumes` skill first: this skill has no facts of its own.
2. **Capture the posting.** From a URL, try firecrawl, then WebFetch, then ask
   the person to paste it. A screenshot works. Save a dated snapshot to
   `jd.md` so a reposted or edited JD can be diffed later.
3. **Research the product, not just the posting.** Read the company's own site,
   docs, pricing and changelog, and find the founders. See
   `references/research-playbook.md`. The posting says what they want. The
   product shows what they care about, and most useful matches come from
   there.
4. **Extract** into `insights.md`: apply mechanics (see below), what the company
   actually builds, hard requirements separated from boilerplate, the match
   against `profile.yml`, and the honest gaps.
5. **Draft only what the posting demands.** Form answers, a video script, an
   outreach comment, a tailored resume. Rules in `references/answer-craft.md`.
   For the resume, hand off to `writing-resumes` with the JD as the input.
6. **Update the board.** `python3 apply.py board`

## Apply mechanics come first

Every brief opens with how to apply, what is mandatory, what triggers automatic
rejection, and the deadline.

Postings bury disqualifiers in prose: "no video means automatic rejection", "put
the link in the box below the question about why you want to work here", "apply
by commenting on this post". Missing one of these loses the application no
matter how good the answers are, and it is the cheapest thing to get right.

## Name the gaps

State which requirements the person does not meet, in the brief and often in
the application itself. "I have not built real-time voice, and it is the part
of this role I would want to own" reads better to a small team than silence,
and far better than a bluff that collapses in the first interview.

## Red flags: stop and re-read the Iron Rule

- Writing an answer you could not source from `profile.yml`
- Rewording a requirement into an accomplishment
- Researching only the posting because the company site looked slow
- Deleting an `[ASK:]` marker without an answer to put there
- The draft would embarrass the person if the interviewer had the repo open
