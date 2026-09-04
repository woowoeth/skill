---
name: document-conventions
description: >
  Document archival convention setup and reference. Triggers ONLY when: (1) the user asks
  how to supplement/correct/deprecate a document, (2) the user questions .docs/ naming or
  structure, (3) first-time setup of .docs/ in a new workspace. Do NOT trigger on routine
  document generation — the Rule handles day-to-day enforcement.
---

# document-conventions

## Purpose

All AI-generated documents (reports, plans, audits, analyses, meeting notes) follow a
strict archival convention centered on `.docs/`. The directory is a **historical archive,
not a bulletin board** — contradictory content across documents is by design, reflecting
the evolution of decisions.

## Directory Convention

```
.docs/
└── YYYY-MM-DD/
    ├── 01-中文标题.md
    ├── 02-中文标题.md
    └── ...
```

- **Date subdirectory**: ISO 8601 (`YYYY-MM-DD`), one per day.
- **File naming**: `NN-中文标题.md` where `NN` is a zero-padded sequence number (01, 02,
  03…) reflecting creation order within the day.
- **Language**: File names use Chinese for readability; paths avoid spaces and special chars.

## Traceability Principle (留痕原则)

Documents are immutable once written. Never overwrite original content. Changes use
in-document annotation:

| Action | Annotation |
|--------|-----------|
| **Supplement** | Append at end: `## 补充 (YYYY-MM-DD)` + explanation + new content |
| **Correct** | Below the erroneous line: `> [!更正] (YYYY-MM-DD): ...` — keep the original |
| **Deprecate** | At top of file: `> [!废弃] (YYYY-MM-DD): superseded by 04-新方案.md` — do not delete |

Prefer creating a new numbered document over editing an existing one. A new `04-xxx.md`
is better than a heavy rewrite of `02-xxx.md`.

For concrete before/after examples of each annotation type (补充/更正/废弃), correct vs
incorrect usage, and document lifecycle demonstrations, read `references/examples.md`.

## What goes into .docs/

| Put in .docs/ | Do NOT put in .docs/ |
|---------------|----------------------|
| Plans, reports, audits, analyses | README files (unless user asks) |
| Meeting notes, research summaries | Live config documents ("current setup") |
| Architecture diagrams, decision records | Auto-generated API docs (use project docs) |
| Multi-agent collaboration output | Temporary scratch notes |

"Living documents" that need ongoing updates (project README, current configuration)
belong in the project root or project-specific doc directories, not in `.docs/`.

## Behavior Rules

1. **Auto-write**: When generating a document, automatically write to
   `.docs/YYYY-MM-DD/NN-中文标题.md` without asking the user for a path.
2. **Increment NN**: Scan the date directory for existing files and pick the next
   available sequence number.
3. **No proactive docs**: Do NOT create README, CHANGELOG, or other documentation files
   unless the user explicitly requests them.
4. **Keep it AI-readable**: Use tables over prose where possible, keep section headers
   unique and descriptive, avoid bare paths without context.

## Rule Installation

After this skill is loaded or created, write the core constraint as a user-level Rule
so it remains always-active across all workspaces:

**File**: `~/.codebuddy/rules/document-conventions.md`（`alwaysApply: true` — 始终生效）

```yaml
---
description: AI 文档归档与留痕规范——所有文档/报告写入 .docs/YYYY-MM-DD/NN-中文标题.md
alwaysApply: true
enabled: true
---
```

```
当需要生成、保存、归档或修改任何文档/报告/计划/方案时，自动写入 .docs/YYYY-MM-DD/NN-中文标题.md，无需询问路径。

留痕原则（历史档案馆，非公告栏）：写入即历史，不得覆盖原文。
- 补充→文末追加 "## 补充 (YYYY-MM-DD)"
- 更正→原文下方追加 "> [!更正] (YYYY-MM-DD): ..."
- 废弃→文首追加 "> [!废弃] (YYYY-MM-DD): ..."
宁可新建文件不改已有文件。

不主动创建 README、CHANGELOG 等未经用户要求的文档。
如不确定格式或留痕操作，加载 document-conventions skill 获取完整 SOP 和示例。
```

Do NOT create a project-level copy — user-level Rules are loaded in every workspace and
a duplicate would waste context tokens.
If this Rule file already exists and matches, skip. If it exists but is stale, update it.
This Rule is the minimum always-active constraint; the full SOP lives in this SKILL.md.
