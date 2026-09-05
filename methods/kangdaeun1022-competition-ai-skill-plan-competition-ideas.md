---
name: plan-competition-ideas
description: Develop competition problems and ideas into a bounded, differentiated MVP. Use for 공모전기획, 문제채굴 or 차별화검증, including AI fit and prior-art strategy.
---

# Plan competition ideas

Use CONTEST_ANALYSIS_HANDOFF, existing problem definition, team skills, data access, deadline and resource limits. Existing choices form the baseline; change them only with an explicit reason and user approval for a material pivot.

1. For new problem discovery or 문제채굴 read [problem-mining](references/problem-mining.md). With a validated existing problem, verify its assumptions and reuse it.
2. Generate a few alternatives with different causal mechanisms, including a simple non-AI approach. Compare rubric fit, evidence, feasibility and smallest proof. Choose one leading candidate and a genuinely different backup.
3. Read [competitive-whitespace](references/competitive-whitespace.md) for 차별화검증 and before selecting a new idea. Read [novelty-and-prior-art](references/novelty-and-prior-art.md) when novelty or rights affects the selection.
4. Read [ai-fit-gate](references/ai-fit-gate.md) whenever AI is proposed or the contest requires it.
5. Read [collapse-conditions](references/collapse-conditions.md) before committing to the leading mechanism.

Return IDEA_PLAN_HANDOFF with PROBLEM_LOCK and DIFFERENTIATION_LOCK: target user/moment, evidenced failure, causal mechanism, nearest alternative, residual difference, decisive assumptions, proof plan, collapse conditions, backup, MVP boundary, exclusions, owners and time/data constraints. Label existing implementation, mockup and plan separately. Send unresolved decisive claims to evidence research; do not invent outcome figures or expand scope to satisfy every critique.
