---
name: project-interview-review
description: "基于简历项目与实现仓库核验项目主张，生成项目化面试追问、基础知识地图、0/1/2/3 评分模拟和可续练复盘包。适用于用户提供仓库与简历、希望核对项目描述或继续项目面试训练的场景；不用于泛化题库、普通代码审查、故障调试或缺少仓库证据的简历润色。"
---

# Project Interview Review

Build and maintain an evidence-grounded interview review pack for one resume project.

Treat this as one repeatable job:

> Convert resume claims plus the current implementation repository into a versioned project interview review pack whose statements, questions, and scores remain traceable to evidence.

## Required inputs

Require both:

1. A project implementation repository or accessible checkout.
2. The resume project section to audit.

Accept optionally:

- target job description;
- prior `.interview-review/<project-slug>/` state;
- external evidence for business/performance metrics, such as benchmark output, logs, acceptance reports, screenshots, or analytics exports.

Do not block if optional inputs are absent. Record them as unavailable.

## Output root and persistence mode

Use the logical review root:

`.interview-review/<project-slug>/`

For interactive review, default to **local checkpoint mode**: stage this logical tree outside the production repository and package/version it as a downloadable checkpoint. Do not write review artifacts into the project repository or GitHub unless the user explicitly asks for repo-local persistence.

Do not modify production source code merely to make a resume claim easier to prove.

The authoritative metadata file is `manifest.json`. Follow `references/output-contract.md`.

## Interactive staged mode

When the user is learning or reviewing interactively, default to processing **one resume line per round**. Read `references/resume-line-workflow.md`.

Use the resume line as the outer organization, code traces as the verification mechanism, and technology as a cross-line learning index.

Do not advance to the next resume line until the current round has an auditable artifact and mock checkpoint, unless the user explicitly requests batch mode.

## Workflow

### 1. Snapshot sources

Record:

- repository root and remote when available;
- current commit SHA;
- resume source and a stable hash of the audited project text;
- optional JD source/hash;
- run timestamp;
- skill schema version.

If a prior manifest exists, compare source fingerprints first. Reuse unchanged evidence and re-audit changed or stale claims.

### 2. Atomize resume claims

Split the project section into atomic claims before reading implementation details.

Preserve exact:

- numbers;
- technologies;
- ownership statements;
- security claims;
- performance claims;
- architecture claims;
- operational claims.

Assign stable IDs such as `C1`, `C2.1`, `C2.2`.

Do not silently rewrite or soften the resume wording during verification.

### 3. Acquire codebase knowledge for the claims

Read repository guidance first when present: `AGENTS.md`, `README`, architecture docs, package/module manifests, deployment files, and migration entrypoints.

Then trace each claim through implementation paths. Prefer targeted tracing over exhaustive summarization.

For each claim:

1. locate entrypoints;
2. trace the main call/data path;
3. inspect relevant schemas/migrations/configuration;
4. inspect tests or runtime/benchmark evidence;
5. record file paths and symbols;
6. record negative searches when expected evidence is missing.

Use the strategy in `references/codebase-audit.md`.

### 4. Verify every claim

Apply `references/evidence-policy.md`.

Never infer measured outcomes from implementation alone.

Examples:

- code may verify that a materialized view and advisory lock exist;
- code does not by itself verify "stable under 50 ms";
- migrations may verify a row-visibility model exists;
- code does not by itself verify "rework rate dropped 96%".

Each atomic claim must receive:

- verification status;
- confidence;
- evidence strength;
- interview risk;
- evidence references;
- missing evidence;
- drift notes.

### 5. Reconstruct the interviewable architecture

Build only the architecture needed to explain verified/high-risk resume claims.

For each important flow, capture:

- entrypoint;
- trust boundary;
- state/data owner;
- main call path;
- concurrency/consistency boundary;
- failure behavior;
- observability/audit points;
- explicit design tradeoffs visible in code;
- unresolved assumptions.

Do not invent historical design rationale. When rationale is not documented, phrase it as an interview question for the user.

### 6. Generate the question ladder

Generate questions from evidence, not from the technology list alone.

For each high-priority claim, create a ladder:

- L1 — explain what the feature does;
- L2 — explain the concrete implementation path;
- L3 — explain why this design was chosen;
- L4 — explain the underlying mechanism/fundamental;
- L5 — identify failure modes and weaknesses;
- L6 — propose scaling, migration, or redesign under changed constraints.

Every project-specific question must reference at least one claim ID.
Whenever possible, attach evidence paths/symbols that the reviewer should revisit before answering.

Follow `references/interview-questioning.md`.

### 7. Build the fundamentals map

Derive fundamentals from exposed implementation decisions.

Prioritize a topic using:

`priority = resume_exposure × implementation_centrality × followup_likelihood × weakness_multiplier`

Use qualitative values `P0`, `P1`, `P2`.

Do not turn every dependency into a study topic.
Prefer fundamentals that an interviewer can naturally reach from a resume bullet.

### 8. Run or continue mock interview when requested

Use existing question ladders, `interviewer-context.json`, learner state, and prior weaknesses.

Read `references/interviewer-perspective.md` and `references/teaching-response-contract.md`.

Ask one question at a time. Do not reveal the full model answer before the user responds.

After the user answers, the visible response order is mandatory:

1. **标准回答** — candidate speech only, grounded in resume + verified implementation;
2. **答案结构** — explain the answer shape;
3. **用户回答分析与 0/1/2/3 评分**;
4. **教学** — fix the largest conceptual/evidence gap;
5. ** exactly one next question**.

Keep evaluator knowledge and interviewer knowledge separate. The interviewer is assumed to know only the resume/JD and what the candidate has already said aloud. Hidden repository details may guide verification and question selection but must not leak into interviewer-facing phrasing.

After each turn update:

- `mock-state.json`;
- `learner-profile.json`;
- `interviewer-context.json`;
- `weaknesses.md`;
- the current round artifact;
- manifest checkpoint metadata.

A fluent answer that contradicts repository evidence must score poorly on credibility.

### 9. Persist the review pack

Write/update:

- `manifest.json`
- `claim-evidence.md`
- `architecture.md`
- `question-bank.md`
- `knowledge-map.md`
- `mock-state.json`
- `weaknesses.md`

Keep raw secrets, tokens, credentials, production data, and private customer data out of the review pack.

### 10. Report completion

Summarize:

- verified claims;
- risky/unverified claims;
- highest-priority interview topics;
- top questions to practice next;
- source changes detected since the previous run.

## Evidence discipline

Use these rules everywhere:

- Prefer code + tests over descriptive docs.
- Prefer runtime/benchmark evidence over performance assertions.
- Treat README/spec claims as supporting evidence, not implementation proof.
- Treat missing evidence as missing evidence, not proof of falsehood.
- Separate "mechanism verified" from "business outcome verified".
- Preserve uncertainty explicitly.
- Never fabricate a metric, rationale, incident, scale, user count, QPS, latency, or production outcome.

## Progressive disclosure

Read only the references needed for the current phase:

- verification: `references/evidence-policy.md`
- repository tracing: `references/codebase-audit.md`
- question generation: `references/interview-questioning.md`
- mock scoring: `references/scoring-rubric.md`
- interviewer knowledge boundary: `references/interviewer-perspective.md`
- interactive feedback ordering: `references/teaching-response-contract.md`
- persistence/schema: `references/output-contract.md`
- trigger QA: `references/trigger-tests.md`
- staged resume review: `references/resume-line-workflow.md`

Do not load every reference by default.

## Boundaries

Do not use this skill when:

- no project repository is available and the request is generic interview prep;
- the user only wants a resume rewritten;
- the task is ordinary debugging or code review;
- the user only wants a codebase map without interview preparation.

For those tasks, use a more specific workflow.


## Resume Relevance and Depth Budget

Treat the repository as evaluator-only evidence, not as information automatically available to the simulated interviewer.

- The simulated interviewer may use only:
  1. the visible resume;
  2. facts the candidate has already said aloud during this mock interview.
- Repository-only details may verify or correct the candidate internally, but MUST NOT be injected into an interviewer question until the candidate has disclosed that concept or the resume itself makes it reasonably inferable.
- Keep the question graph resume-centered. Every question must be classified as one of:
  - `resume_direct`: directly tests the current resume claim;
  - `resume_adjacent`: one technical hop needed to defend that claim;
  - `off_resume_extension`: useful pressure/advanced knowledge beyond what the resume requires.
- Default depth budget:
  - unlimited `resume_direct` while the claim is unresolved;
  - at most 1 consecutive `resume_adjacent` deepening after the candidate demonstrates the core claim;
  - at most 1 `off_resume_extension` question unless the user explicitly asks to continue deeper.
- After an `off_resume_extension`, return to a `resume_direct` claim. Do not let an interesting distributed-systems or infrastructure tangent replace the staged resume workflow.
- Scores on `off_resume_extension` questions MUST NOT lower the assessment of the underlying resume claim unless the resume explicitly claims that technology.
- When the user signals pressure, fatigue, or topic drift, immediately reduce depth and return to resume-direct questions.

### Required feedback order after each user answer

1. `标准回答`: natural candidate speech, grounded by resume + verified implementation, with no repository/meta language.
2. `答案结构`: concise structure of the good answer.
3. `你的回答分析`: evaluate the user's actual answer.
4. `评分`: only 0/1/2/3 and low/medium/high.
5. `教学补充`: evaluator-side source verification, missing fundamentals, and implementation boundaries.
6. Ask exactly ONE next question.

### Local checkpoint requirements

Maintain local artifacts for:
- `interviewer-context.json`: what the interviewer is allowed to know from resume + candidate disclosures;
- `learner-profile.json`: observed understanding and weaknesses;
- `mock-state.json`: question IDs, scores, scope classification, next question;
- per-round notes/artifacts and evidence boundary;
- do not write these review artifacts into the user's production repository unless explicitly requested.
