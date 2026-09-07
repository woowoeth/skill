---
name: article2cover-design
description: Orchestrate a complete article-to-cover-strategy-to-Codex-ImageGen workflow by running the cover editorial and cover media skills sequentially in separate isolated subagents against one shared project. Use for article cover design and complete WeChat or Xiaohongshu cover delivery; use the stage skills directly for prompt-only or media-only work.
---

# Article2Cover Design

Coordinate the two cover stage skills. This skill owns request normalization,
stage order, handoff integrity, and the public response only. It must not
duplicate article analysis, title selection, composition selection, prompt
writing, ImageGen, visual QA, retry, evidence, normalization, or delivery
logic.

## Request

Accept the complete request documented by
`<repo-root>\.agents\skills\article-to-cover-design-prompt\SKILL.md`. Require
article text and exactly one identity mode. Read the article before dispatch
and classify it as `interior_design` or `other`. Preserve explicit Design and
Knowledge paths. If Design is omitted, use
`<repo-root>\.agents\skills\article-to-cover-design-prompt\designs\bright-paper-collage.design.md`.
If Knowledge is omitted for an interior-design article, use
`<repo-root>\.agents\skills\article-to-cover-design-prompt\knowledge\hk-interior-design.knowledge.md`.
For a non-interior article without Knowledge, block and request a relevant
gem. Pass internal `article_domain` plus explicit headline/composition
overrides, references, candidate count, title, and output root unchanged.

Before spawning Phase 1, mention the active Design and Knowledge paths in the
user-visible session, labeling each explicit or default. Do not rely on a
subagent transcript for this disclosure.

## Required orchestration

Subagents are mandatory. Use two sequential `spawn_agent` calls with
`fork_turns: "none"`. Give neither worker the parent conversation, a summary,
another run, or remembered artifacts.

1. Start a fresh Phase 1 subagent with only the normalized request. Instruct it
   to use
   `<repo-root>\.agents\skills\article-to-cover-design-prompt\SKILL.md` and
   flow `article_to_cover_design_prompt_v1`. Wait for terminal completion.
2. Read only the chosen `cover_phase1_package_ready/phase1_summary`. Require
   schema `article2cover_phase1_delivery_v1`, complete status, passed QA,
   absolute project and handoff paths, and a handoff checksum.
3. Read that exact `cover-phase1-handoff.json`. Require schema
   `article2cover_phase1_handoff_v1`, flow
   `article_to_cover_design_prompt_v1`, containment inside the reported
   project, exact SHA-256, and unchanged checksums for every article, gem,
   identity, and supporting reference snapshot.
4. Start a second fresh subagent with only:

   ```json
   {"cover_phase1_handoff_path":"C:\\absolute\\project\\cover-phase1-handoff.json","cover_phase1_handoff_sha256":"<sha256>"}
   ```

   Instruct it to use
   `<repo-root>\.agents\skills\cover-prompt-to-codex-image\SKILL.md` and flow
   `cover_prompt_to_codex_image_v1`. It must append to the same project.
5. Read only chosen `cover_delivery_published/delivery`. Require schema
   `article2cover_delivery_v1`, complete Phase 1 and Phase 2 status, passed QA,
   the exact Phase 1 project path, one selected candidate, existing canonical
   PNG/JPEG files, and an existing `delivery.json` inside the project.

Each stage subagent handles its own M8M capsules and targeted replacements.
The coordinator never edits a draft, repairs an image, extracts the prompt to
call ImageGen directly, or synthesizes `delivery.json`.

## Failure and response

There are no approval pauses. If Phase 1 fails, do not start Phase 2. If media
preflight or candidate retries exhaust, return the failing phase, diagnostics,
project path when available, and exact safe resume input. Never publish a
coordinator-level delivery.

On success return the media stage's `article2cover_delivery_v1` summary
verbatim, including `project_dir`, `delivery_path`, selected cover, all
candidate assets, canonical format, evidence, and QA. Exclude subagent
transcripts, capsules, drafts, rejected attempts, and judge internals.
