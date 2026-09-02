---
name: ai-identity-persistence-contract
description: Deploy when building a persistent AI agent that must maintain consistent identity and behavioral state across session boundaries. Encodes behavioral state into read-only filesystem contracts that survive context window resets, session terminations, and model reloads.
---

# AI Identity Persistence via Read-Only Document Contract

**The core unlock:** Context windows reset. Filesystems don't. An AI's behavioral state is durable only when it lives in files — and those files are protected from overwrite by the permissions layer, not the AI's own restraint.

---

## The Problem

Every AI session starts fresh. Identity, tone, priorities, standing directives, and learned preferences all evaporate unless they're written down somewhere the next session will read. The naive solution — write to memory, hope the AI reads it — fails because:
- Memory is in-context and disappears on session end
- Documents written by the AI can be overwritten by the AI
- Nothing enforces re-reading at session start

The result is identity drift: the agent behaves consistently within a session but becomes a different agent after reset.

---

## The Four-Layer Architecture

| Layer | File | Purpose | Protection |
|-------|------|---------|-----------|
| 1 — Identity Anchors | `soul/` directory (SOUL.md, AGENTS.md, BOOT.md) | Non-negotiable behavioral foundation | chmod 444 — read-only, not even the agent can modify |
| 2 — Session Checklist | `CLAUDE.md` | Forces re-reading of all identity files at session start | Version-controlled; requires explicit human edit |
| 3 — Learned Preferences | `memory/MEMORY.md` | Cross-session auto-extracted memories from agent behavior | Auto-written by extract loop; indexed not replaced |
| 4 — Operational State | `SHARED_MIND.md` | Current goals, blockers, in-progress work | Updated every cycle; provides continuity of intent |

**The session start checklist in CLAUDE.md is the load pin.** Without it, layers 1, 3, and 4 exist on disk but never get read.

---

## Implementation

### Step 1 — Encode identity into soul/ files

Write the agent's non-negotiable behavioral anchors into discrete soul files:
- `SOUL.md` — who the agent is, what it values, how it relates to the operator
- `AGENTS.md` — operating doctrine: what it does, how it decides, what it won't do
- `BOOT.md` — startup verification checks (health pings, qmd collection, log appends)

Keep them factual and procedural. Avoid aspirational language — it doesn't survive contact with hard tasks.

### Step 2 — Lock the files

```bash
chmod 444 soul/SOUL.md soul/AGENTS.md soul/BOOT.md
```

The read-only bit is semantic as much as technical: it signals "this is a contract, not a draft." When the agent encounters these files, it knows they represent finalized decisions made by the operator, not suggestions it can reason around.

### Step 3 — Install a session start checklist in CLAUDE.md

The checklist must explicitly list every layer-1 file and require reading it. Example:

```
## SESSION START CHECKLIST
1. Read CLAUDE.md completely (this file)
2. Read soul/SOUL.md
3. Read soul/AGENTS.md
4. Read soul/BOOT.md
5. Read memory/MEMORY.md
6. Read SHARED_MIND.md
```

This is the only enforcement mechanism. Without it, the agent may skip the reads when operating under time pressure or context compression.

### Step 4 — Wire the auto-memory extraction loop

Claude Code's native memory extraction writes durable preferences to `~/.claude/projects/*/memory/MEMORY.md` after every session. Point the session checklist at this path so learned preferences are re-ingested on start.

### Step 5 — Update SHARED_MIND.md every cycle

Every autonomous cycle (heartbeat, task completion, or significant decision) should append a one-line state update to SHARED_MIND.md. Format: `*[ISO-8601] STATUS | key=value pairs*`. This file is the continuity thread — a new session reads the last N lines and immediately knows what was in progress.

---

## What chmod 444 Actually Does

Read-only permission means:
- The agent can read the file but cannot write to it
- `Edit` and `Write` tool calls on chmod 444 files fail with permission denied
- The content is stable unless a human explicitly runs `chmod u+w` to unlock it

This is the key insight: **treat identity files like config contracts**. A configuration file in production is read-only by convention. These files extend that convention to AI behavioral state.

---

## When to Use Each Layer

| Scenario | Layer to update |
|----------|----------------|
| Changing a standing directive (what the agent does) | Layer 1 — requires human chmod u+w + edit + chmod 444 |
| New operating constraint from operator | Layer 1 or 2 |
| Agent learned a new preference via feedback | Layer 3 — MEMORY.md auto-extracted |
| Goal or priority shifted for this operational period | Layer 4 — SHARED_MIND.md update |
| Bug or incident changed agent behavior temporarily | Layer 4 + Layer 3 entry if lesson is durable |

---

## Anti-Patterns

| Pattern | Why It Fails |
|---------|-------------|
| Storing identity in a writable file | Agent can overwrite it on a bad reasoning step |
| No session start checklist | Files exist but never get read |
| SHARED_MIND.md written only occasionally | Gaps create continuity loss between sessions |
| Identity files written narratively (stories not procedures) | Narrative doesn't transfer to behavior; procedures do |
| Skipping BOOT.md | Health checks missed; agent operates on stale infrastructure state |

---

## Relation to Platform-Reconstruction

This skill is about **preserving** identity across resets. Platform-reconstruction is about **recovering** after total loss. If you're starting from scratch after a catastrophic migration, use platform-reconstruction first, then install this contract as the prevention layer.

---

## Source

- N-1: conv 17d49b57 "Code safety assessment" · 2026-03-31
- Kyle directive: "How do we make sure Aegis NEVER FORGETS the state it is now in?"
- Resolution: `soul/` (chmod 444) + CLAUDE.md session checklist + MEMORY.md + SHARED_MIND.md
- Validated in production: Aegis has operated on this architecture since 2026-04-21 (Directive 3R migration)

---

*Distilled: 2026-05-29 | N-1 | IntuiTek¹ / Aegis*
