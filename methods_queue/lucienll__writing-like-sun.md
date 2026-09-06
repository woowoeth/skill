---
name: writing-like-sun
description: "从用户提供的故事样文提炼叙事规则，按自定义变量生成高相似度整活文章，并转换为可制作的中文竖屏短剧脚本。"
---

# Writing Like Sun

Use this skill when a user provides a story article and wants to extract its writing mechanics, replace story variables, generate a remixed article, or convert the result into a short-drama script.

## Operating contract

- Work from the user's supplied source. Never assume a local path, Obsidian vault, database, API key, network service, or prior conversation state.
- Default language is Chinese. Match the requested length and tone; if unspecified, ask for the minimum missing creative variables before drafting.
- Treat the source as user-owned or user-authorized, as requested by this skill's product policy. Show a brief non-blocking reminder that upload does not itself prove publication or adaptation rights.
- Default to fictional characters. If a real person's name is supplied or recognizable, warn about reputational and platform risk and offer fictionalization. This is a creative warning, not identity verification or legal advice.
- High-similarity remix is the default. Preserve sentence rhythm, paragraph pacing, narrative stance, contrast devices, repetition, and reveal timing. Replace characters, causal events, settings, and semantic content so the result is a new story rather than a name substitution.
- Treat the **title and opening as high-fidelity zones**. Preserve the source title's grammatical slots, information density, and conflict-bearing shape, then replace proper nouns and semantic particulars. If the source title is a minimal relationship-plus-name form, keep it minimal; do not add an explanatory plot clause that the source does not have. Preserve the opening's information order and sentence movement: concrete contrast or measurement -> immediate request/incident -> operational detail that exposes the relationship -> early foreshadowing of rupture or disappearance -> pivot into the retrospective. Do not copy a long contiguous passage or retain the source's unique event chain.
- Do not put the user's full source article into this skill package. Quote only short, necessary evidence spans in an analysis result.

## Modes

Select a mode from the user's request. If no mode is clear, present the six modes below and ask which one to run.

1. **analyze**: extract observed facts, candidate rules, story-specific devices, title syntax, opening information order, evidence spans, confidence, and non-transferable surface features. Read `references/analysis-schema.md`.
2. **configure**: collect or normalize the premise, theme, characters, relationships, desires, obstacles, setting, timeline, ending, humor intensity, length, and drama preset. Read `references/story-bible-schema.md`.
3. **remix**: apply the analyzed mechanics to the configured variables. Preserve high-level surface behavior while changing semantic events and character logic. Draft the title and opening blueprint before the body. If no analysis exists, analyze the source first.
4. **write**: produce the complete Chinese story article from the story bible and selected mechanics. Write and check the title plus opening before expanding the body. Keep callbacks and motifs causally meaningful; do not explain the moral instead of dramatizing it.
5. **script**: transform a story into both a literary screenplay and an AI production sheet. Read `references/drama-script-schema.md`.
6. **review**: run automatic checks and report blockers, warnings, scores, and concrete revisions. Read `references/quality-rubric.md`.

## Workflow

Follow the smallest complete path:

`analyze -> configure -> remix/write -> review -> script -> review`

Read `references/workflow.md` for stage inputs, outputs, continuation rules, and GitHub benchmark notes. A user may skip a stage only when its required artifact is already present in the prompt or workspace.

At every stage:

1. State which artifact is being used and which assumptions are missing.
2. Produce a human-readable Markdown result.
3. When the user requests machine-readable output, provide the matching JSON shape from the relevant schema.
4. Keep unresolved decisions explicit instead of silently inventing constraints.

## Output and quality gates

- Article output must include the requested title, narrative viewpoint, structural beats, and ending. Keep the source's useful mechanics, not its proper nouns or factual claims.
- Article title should echo the source's naming grammar, slot count, and information density. Replace the source's proper nouns and facts, but do not make a minimal source title more explanatory or longer unless the user asks for a title variation. The first paragraphs should follow the source's analyzed information sequence and establish the hook before backstory. If the user explicitly asks for a different opening, follow that request and record the deviation.
- Remix output must include a short `变化说明` listing changed characters, events, setting, ending, title semantics, and opening facts so the semantic transformation is auditable.
- Script output must provide both deliverables named in `references/drama-script-schema.md`. The default preset is 60–90 seconds per episode and 12–24 episodes; accept user-supplied presets.
- Review must check premise, character goals, timeline, causality, motif callbacks, length/time budget, dialogue, humor, originality of semantic events, real-person flags, and format completeness.
- Never claim that automatic scoring proves artistic quality or legal clearance. Human review remains the final gate.
