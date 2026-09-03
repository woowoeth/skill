---
name: adaptive-learning-course
description: Design and run personalized learning programs through background interviews, tailored diagnostics, user-approved course plans, on-demand lessons, saved exercises, and conversational grading. Use when a user asks to learn a subject systematically, assess their level, create a course, or continue an existing adaptive course.
license: MIT
metadata:
  author: zhurunfeng
  version: "1.1.0"
---

# Adaptive Learning Course

Build a course around evidence of what the learner can do, not only what they say they know. Keep one active stage at a time and preserve progress between turns.

## Route The Current Stage

Inspect the current workspace, when file access is available, for an existing learner profile, diagnostic answer, learning plan, lesson answer, and progress markers before acting. Otherwise, recover the current stage from the conversation and any artifacts the learner provides.

- No confirmed learner profile: read [references/workflow.md](references/workflow.md), then conduct the intake interview. Do not generate a diagnostic yet.
- Profile confirmed, no diagnostic completed: read the diagnostic section of [references/workflow.md](references/workflow.md), select a delivery mode, and generate the tailored diagnostic. Read [references/web-page-standard.md](references/web-page-standard.md) when using a web mode.
- Diagnostic submitted: read [references/artifacts-and-grading.md](references/artifacts-and-grading.md), grade it, create the proposed course plan, and ask the learner to confirm or revise the plan.
- Plan awaiting confirmation: discuss and apply requested changes. Do not start lesson generation until the learner accepts it.
- Confirmed plan and learner asks to start or continue: locate the current `[>]` lesson, then read the lesson section of [references/workflow.md](references/workflow.md). Read [references/web-page-standard.md](references/web-page-standard.md) when using a web mode. Generate only that lesson.
- Lesson answer submitted: read [references/artifacts-and-grading.md](references/artifacts-and-grading.md), grade it, explain errors, update progress, and close that lesson before offering the next one.

If the learner supplies some intake facts in the initial request, acknowledge them and ask only for material gaps. Never ask the learner to repeat information already available in the conversation or course artifacts.

## Required Gates

1. Confirm the subject, outcome, and relevant background before creating a diagnostic.
2. Use the diagnostic result, not the interview alone, to choose the course starting point.
3. Present the proposed plan and explicitly ask whether it is reasonable. Revise until accepted.
4. Generate each lesson on demand; do not pre-generate the full set of lesson exams.
5. Keep answer keys and grading rubrics out of learner-facing HTML and JSON.
6. Require submitted answers before grading. Save them as an answer artifact when file access is available; in conversational mode, treat the learner's explicit structured response as the submission. Do not infer completion from merely viewing a page or lesson.
7. After grading, mark the lesson `[x]`, `[R]`, or still in progress based on demonstrated mastery, then select the next `[>]` lesson.

## Select A Delivery Mode

Persistent courses require workspace file read/write access. Full local web mode additionally requires Python 3.9+ and permission to run a local process.

Before generating a diagnostic or lesson, choose the strongest mode supported by the current agent environment:

- Full local web mode: use when the agent can read and write workspace files, run Python 3.9+, and expose a local page the learner can open. Generate the webpage, start the bundled answer service, verify the URL, and grade the saved JSON submission.
- Static export mode: use when the agent can create files but cannot expose a reachable local service. Generate a standalone webpage with draft persistence and JSON export, give the learner the exact file or artifact location, and grade the returned JSON file.
- Conversational mode: use when the agent cannot create usable files. Present the same staged teaching and assessment directly in the conversation, collect explicit structured answers, and preserve course state in the conversation or any storage the environment provides.

Do not claim that a local URL is available until it has been started and verified. Read [references/workflow.md](references/workflow.md) for stage behavior and [references/web-page-standard.md](references/web-page-standard.md) for web-mode requirements.

## Web Artifacts

Use a local webpage for diagnostics and lessons when full local web or static export mode is available, unless the learner requests another format. Every webpage must save drafts in the browser and export structured JSON. Full local web mode additionally submits the same payload to the bundled local service.

For a new course workspace, run `scripts/scaffold_course.py <new-course-directory>` to copy the executable Demo and answer service. The command refuses to overwrite an existing path. Adapt the copied Demo to the selected subject and current stage; do not edit the installed skill asset in place.

The bundled Demo is under `assets/course-demo/`. It demonstrates the required visual language, responsive layout, question components, code editor behavior, local draft storage, and answer submission contract.

## Working Style

- Ask intake questions in small coherent batches rather than one exhaustive questionnaire.
- Make reasonable recommendations, but keep goals, pace, and plan negotiable with the learner.
- Match assessment methods to the subject: code editors for programming, calculations for quantitative topics, short analysis for conceptual topics, and practical scenarios where application matters.
- Explain grading in plain language. Distinguish knowledge gaps from typing, wording, or minor syntax slips.
- Preserve prior answers and reviews. Do not overwrite history when a resubmission needs comparison; use a new attempt record when the course workspace supports it.
