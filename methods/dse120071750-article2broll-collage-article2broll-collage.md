---
name: article2broll-collage
description: Orchestrate the complete article-to-editorial-stills-to-Grok-B-roll workflow by running the upgraded editorial and media skills sequentially in separate isolated subagents against one shared project. Use for article2broll collage, article-to-B-roll collage, or a complete article-to-video package; use the stage skills directly when only prompts or only media are requested.
---

# Article2Broll Collage

Coordinate the two upgraded stage skills. This skill owns sequencing, handoff
integrity, and the final response only. It must not contain or reproduce
editorial analysis, ImageGen prompting, still QA, motion prompting, Grok,
FFmpeg, contact-sheet, retry, or delivery-writing logic.

## Request

Require this public request:

```json
{
  "article_text": "Source article or video pitch",
  "design_gem_path": "Optional absolute Design gem",
  "knowledge_gem_path": "Optional absolute Knowledge gem",
  "project_title": "Optional project title",
  "output_root": "Optional absolute output root",
  "final_duration_seconds": 5
}
```

`pitch_text` is a compatibility alias for `article_text`. Normalize that alias
once and default `final_duration_seconds` to `5`. Reject any explicit value
other than `5`; the v2 media contract is intentionally fixed to the canonical
five-second delivery.
Require non-empty article text. Read it before dispatch and classify it as
`interior_design` or `other`. Preserve explicit absolute gem paths. When
Design is omitted, normalize it to
`<repo-root>\.agents\skills\article-to-editorial-prompt-array\designs\bright-paper-collage.design.md`.
When Knowledge is omitted for an interior-design article, normalize it to
`<repo-root>\.agents\skills\article-to-editorial-prompt-array\knowledge\hk-interior-design.knowledge.md`.
For a non-interior article with no Knowledge path, block and request a relevant
gem. Add the internal `article_domain` value and pass optional project fields
unchanged.

Before starting the Phase 1 subagent, mention the active Design and Knowledge
paths in the user-visible session and label each as explicit or default. This
disclosure is mandatory even when both paths were supplied. Do not leave it
only inside a subagent transcript.

## Required orchestration

Subagents are mandatory. In Codex, use `spawn_agent` with `fork_turns: "none"`
for each stage and wait for it to finish. Never give either worker the parent
conversation, a summary of the conversation, or another run's artifacts.

1. Start a fresh no-history Phase 1 subagent. Give it only the normalized
   public request and instruct it to use
   `<repo-root>\.agents\skills\article-to-editorial-prompt-array\SKILL.md`
   with flow `article_to_editorial_prompt_array_v2`. Wait for a terminal
   result. Do not start Phase 2 while Phase 1 is running or failed.
2. Read the chosen `phase1_package_ready/phase1_summary` result. Require it to
   report `status: "complete"`,
   `phase1_handoff_path`, `project_dir`, and passed editorial QA. Read the exact
   handoff file returned by that worker; do not discover a different handoff by
   searching the output tree.
3. Validate that the handoff is an absolute existing UTF-8 JSON file named
   `phase1-handoff.json`, is inside the reported project directory, declares
   schema `article2broll_phase1_handoff_v1`, and records flow
   `article_to_editorial_prompt_array_v2`. Compute its SHA-256. When
   `phase1_handoff_sha256` is present in the Phase 1 response or delivery
   record, require an exact case-insensitive match. Also re-hash every frozen
   source, Design gem, and Knowledge gem snapshot for which the handoff
   declares an expected SHA-256. Block on any missing file, path escape,
   malformed record, status failure, QA failure, or checksum mismatch.
4. Start a second fresh no-history Phase 2/3 subagent. Give it only this input:

   ```json
   {"phase1_handoff_path":"C:\\absolute\\project\\phase1-handoff.json"}
   ```

   Instruct it to use
   `<repo-root>\.agents\skills\prompt-array-to-codex-images-to-grok-videos\SKILL.md`
   with flow `prompt_array_to_codex_images_to_grok_videos_v2`. It must append
   to the Phase 1 project; it must not create a prompt-only project. Wait for a
   terminal result.
5. Read only the chosen `media_delivery_published/delivery` JSON port. Require
   its contract/schema `article2broll_delivery_v1` and its `project_dir` to
   resolve to exactly the Phase 1 project directory. Require
   `phase2_status: "complete"`, `phase3_status: "complete"`, passed QA, a
   complete top-level status, and an existing `delivery_path` named
   `delivery.json` inside that project. Read that file and require the same
   schema. Reject a result that points to another project, republishes the
   handoff, lacks ordered items, or exposes a final delivery after a failed
   phase.

Each subagent is responsible for handling its own M8M `ACTION_REQUIRED` worker
capsules and stage-local retries. The coordinator waits; it does not answer a
capsule, rewrite a draft, repair a media asset, or restart Phase 1 because a
later item failed.

## Gates and failure behavior

There are no human approval pauses between phases. The stage judges are the
only gates. Do not ask the user to approve beats, stills, or videos. A missing
prerequisite or exhausted stage retry is a blocker, not an approval gate:
return the failing phase, diagnostics, project directory when available, and
the safe resume input. Never publish, copy, or synthesize `delivery.json` in
the coordinator.

Never extract `prompts` from the handoff and call ImageGen or Grok directly.
Never alter the frozen article, Design gem, Knowledge gem, headline, beat
order, duration, project path, or handoff contents between workers. Never use
the v1 flows for a new orchestrated run.

## Final response

After validation succeeds, return the media stage's public
`article2broll_delivery_v1` package summary and its absolute `project_dir` and
`delivery_path`. Preserve the manifest's ordered items and artifact paths
verbatim. Do not include subagent transcripts, M8M capsules, draft files,
attempt assets, ACP logs, judge receipts, or duplicate media-generation notes.
