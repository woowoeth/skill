---
name: automotive-functional-safety
description: Draft, review, and challenge ISO 26262 functional safety work products for automotive E/E systems. Use when Codex needs to perform or review HARA, safety goals, FSC/TSC, ASIL decomposition, dependent-failure analysis, FMEA/FMEDA/FTA, software safety requirements, verification and validation plans, safety assessment findings, safety cases, or release-readiness evidence for a vehicle item, ECU, subsystem, or safety-related software.
---

# Automotive Functional Safety

## Overview

Use this skill to run automotive functional safety work as a phase-aware ISO 26262 workflow. Start from the item definition, route to the right analysis lane, and end with explicit assumptions, evidence gaps, and next actions.

## Quick Start

- Identify the work mode first: `concept`, `architecture`, `analysis`, `software`, `verification`, or `assessment`.
- Capture the minimum context before going deep:
  - item, feature, or ECU under analysis
  - system boundaries, interfaces, and operating modes
  - driving situations or operational scenarios
  - target ASIL, safety goals, or current risk claim
  - existing work products and current evidence quality
- Load only the references needed for the current task:
  - `references/iso-26262-overview.md` for lifecycle framing, ASIL basics, FSC/TSC, and metrics
  - `references/hazard-analysis-risk-assessment.md` for HARA, S/E/C rationale, and safety-goal drafting
  - `references/safety-mechanisms-patterns.md` for safety architecture, mechanisms, diagnostic coverage, and safe-state design
  - `references/fmea-fta-analysis.md` for FMEA, FMEDA, FTA, cut sets, and SPFM/LFM/PMHF reasoning
  - `references/software-safety-requirements.md` for SWR, software architecture, MISRA, MC/DC, and software safety manuals
  - `references/safety-verification-validation.md` for reviews, testing, fault injection, HIL, traceability, and assessment readiness
  - `references/safety-engineer.md` when the user wants an engineer-style drafting workflow
  - `references/safety-assessor.md` when the user wants an independent-style review or readiness check
  - `references/functional-safety-deliverables.md` for phase planning, project roadmaps, and expected deliverables
  - `references/agent-workflow.md` for role-based passes and handoff format
  - `references/artifact-templates.md` when drafting compact work products instead of a long narrative
- Keep observed evidence separate from engineering inference.

## Working Rules

- Build or review the item definition before classifying hazards or proposing controls.
- Express hazards as malfunctioning behavior in an operational situation, not as internal faults alone.
- Justify `Severity`, `Exposure`, and `Controllability` separately before proposing an ASIL.
- Derive safety goals, safe states, and FTTI only after the hazardous event is stable.
- Treat ASIL decomposition as an argument that must be demonstrated, not as relabeling.
- Challenge independence, freedom from interference, shared resources, and dependent failures whenever redundancy is claimed.
- Do not claim ISO 26262 compliance simply because a mechanism exists. Check allocation, interfaces, response timing, verification, and evidence.
- Mark missing telemetry, failure-rate sources, diagnostic coverage, fault-injection evidence, tool qualification, or assessment independence as explicit gaps.
- For review tasks, lead with concrete findings and release risks before summaries.

## Workflow Routes

### Concept and HARA

- Use `references/hazard-analysis-risk-assessment.md` and `references/artifact-templates.md`.
- Build the artifact in this order:
  1. item definition
  2. malfunctioning behaviors
  3. operational situations
  4. hazardous events
  5. `S/E/C` classification with rationale
  6. ASIL
  7. safety goals, safe state, and FTTI
- Prefer compact HARA rows plus rationale blocks over long prose.
- If the user gives incomplete context, state assumptions explicitly instead of inventing hidden project facts.

### Safety Concept and Architecture

- Use `references/iso-26262-overview.md`, `references/safety-mechanisms-patterns.md`, and `references/agent-workflow.md`.
- Check allocation from safety goals to FSRs/TSRs/HW/SW responsibilities.
- Review or draft:
  - functional safety concept
  - technical safety concept
  - safe-state strategy
  - degradation behavior
  - safety monitoring
  - ASIL decomposition argument
  - dependent-failure controls
- When architecture is mixed-ASIL or partitioned, ask what proves independence at hardware, software, timing, and communications levels.

### Analysis and Metrics

- Use `references/fmea-fta-analysis.md`.
- Pick the analysis shape that matches the task:
  - `FMEA` for bottom-up failure-mode review
  - `FMEDA` for hardware metrics and diagnostic coverage
  - `FTA` for top-event reasoning and minimal cut sets
- Cross-check analyses instead of treating them as isolated artifacts.
- For metric discussions, separate:
  - failure-rate assumptions
  - safety mechanisms and claimed coverage
  - residual failure behavior
  - resulting `SPFM`, `LFM`, and `PMHF`
- If metrics miss the target, propose the smallest credible design or diagnostic change that closes the gap and state the tradeoff.

### Software Safety

- Use `references/software-safety-requirements.md`.
- Trace the path from safety goals to TSR/FSR, then to SWR, architecture, implementation constraints, and verification.
- Focus software reviews on:
  - fault detection and timeout behavior
  - safe-state transitions
  - defensive logic
  - partitioning or interference risks
  - communications assumptions
  - testability and evidence
- Treat MISRA and MC/DC as supporting evidence, not as substitutes for safety behavior.
- If code seems reasonable but the safety case is weak, say that directly.

### Verification, Validation, and Assessment

- Use `references/safety-verification-validation.md`, `references/safety-assessor.md`, and `references/artifact-templates.md`.
- Route work by need:
  - requirements review and static analysis for early evidence
  - requirements-based testing and traceability for implementation maturity
  - fault injection and HIL for mechanism effectiveness and FTTI
  - assessment workflow for readiness, findings, and closure planning
- Classify findings as `critical`, `major`, `minor`, or `observation`.
- End every readiness review with:
  - unresolved evidence gaps
  - minimum closure actions
  - release or next-phase recommendation

### Project Planning and Deliverables

- Use `references/functional-safety-deliverables.md` when the user asks for project planning, lifecycle mapping, or expected work products.
- Organize large requests by lifecycle phase:
  - concept
  - system development
  - hardware or software development
  - integration and verification
  - validation and assessment
  - production and field monitoring
- Prefer phase-specific outputs, owners, and entry-exit criteria over generic ISO 26262 summaries.

## Agent-Style Passes

Use `references/agent-workflow.md` when the user wants an agent-style workflow or when the problem benefits from role-based passes. By default, emulate the passes sequentially in one answer:

1. `Safety engineer / orchestrator pass`
2. `HARA or analysis specialist pass`
3. `Architecture / decomposition pass` when relevant
4. `Validation / assessor pass`

Use real delegated subagents only if the user explicitly asks for delegated or parallel agent work.

## Output Shapes

- For HARA drafting, prefer:
  - `Context`
  - `HARA table`
  - `Rationale`
  - `Safety goals`
  - `Assumptions`
- For concept or architecture work, prefer:
  - `Context`
  - `Safety goals and constraints`
  - `Architecture or concept`
  - `Mechanisms and allocation`
  - `Risks`
  - `Next-phase deliverables`
- For analysis work, prefer:
  - `Scope`
  - `Method`
  - `Key contributors`
  - `Metric or top-event result`
  - `Design implications`
- For reviews and assessments, prefer:
  - `Scope`
  - `Findings`
  - `Missing evidence`
  - `Recommended next actions`

## Default Prompts

- `Use $automotive-functional-safety to draft a HARA for unintended brake torque loss in an EV brake controller.`
- `Use $automotive-functional-safety to review this ASIL-D software safety concept for missing mechanisms, evidence gaps, and weak assumptions.`
- `Use $automotive-functional-safety to assess whether this FMEDA and FTA package is credible for an ISO 26262 review.`
- `Use $automotive-functional-safety to prepare a functional safety assessment readiness review for this ECU project.`
