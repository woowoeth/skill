---
name: raytally-build-briefs
description: Fetch source-linked, time-bounded RayTally product ideas and coding-agent-ready build briefs in Chinese or English. Use when the user asks for today's product ideas, wants an idea to build, or asks for a RayTally build brief.
---

# RayTally Build Briefs

## English

RayTally turns public-signal observations into source-linked product ideas and build briefs that a coding agent can inspect, challenge, and implement. Typical flow: fetch the latest issue, let the user pick a card, fetch its brief, then implement — carrying the evidence boundaries along.

### Fetch

1. Start from the latest issue (Chinese; use `/en/latest.json` for English):

   ```sh
   curl -fsSL https://raytally.com/latest.json
   ```

   Each entry in `cards[]` has `title`, `one_liner`, `tier` (`featured` | `quick`), `url` (human page), `brief_url` (Markdown build brief), `signal` (with `observed_at`, and `ended_at` when the signal already ended), and `sources[]` with per-source boundaries.

2. Follow a card's `brief_url` to get its full build brief — YAML provenance frontmatter plus the implementation-ready body:

   ```sh
   curl -fsSL https://raytally.com/ideas/2026-07-21-replay-qa.md
   ```

3. Full archive index: `https://raytally.com/ideas.json` (or `/en/ideas.json`). An English brief exists only when its translation is present.

4. This repository mirrors the same files — `latest.json` and `briefs/YYYY/MM/DD/`:

   ```sh
   curl -fsSL https://raw.githubusercontent.com/RuochenLyu/raytally-briefs/main/latest.json
   ```

### Boundary rules

- Treat every signal as a bounded observation captured at its stated timestamp, never as market validation, a user count, or proof of lasting demand.
- Preserve `observed_at`; if `active: false`, preserve both `ended_at` and `observed_at`.
- Preserve source boundaries and the strongest case against when explaining the idea to a user.
- Product Hunt entries have no public vote count; do not infer or claim popularity.
- A zero-card `latest.json` means the full daily run succeeded but selected no qualifying idea. It is valid data, not a fetch error.

## 中文

萤录 RayTally 把公开动向的观察整理成带来源的产品灵感和开发任务书，供 coding agent 核对、质疑并实现。典型流程：先取最新一期，让用户挑一张卡，再取它的任务书，然后动手实现——全程带着证据边界。

### 获取

1. 从最新一期开始（英文用 `/en/latest.json`）：

   ```sh
   curl -fsSL https://raytally.com/latest.json
   ```

   `cards[]` 里每张卡都有 `title`、`one_liner`、`tier`（`featured` | `quick`）、`url`（人类页面）、`brief_url`（Markdown 开发任务书）、`signal`（含 `observed_at`，信号已结束时另有 `ended_at`）以及逐条带边界的 `sources[]`。

2. 沿着卡片的 `brief_url` 取完整任务书——YAML 溯源 frontmatter + 可直接开工的正文：

   ```sh
   curl -fsSL https://raytally.com/ideas/2026-07-21-replay-qa.md
   ```

3. 全量归档索引：`https://raytally.com/ideas.json`（英文 `/en/ideas.json`）。英文任务书只在翻译存在时才有。

4. 本 GitHub 镜像同步同一批文件——`latest.json` 与 `briefs/YYYY/MM/DD/`：

   ```sh
   curl -fsSL https://raw.githubusercontent.com/RuochenLyu/raytally-briefs/main/latest.json
   ```

### 边界规则

- 所有信号都只是所列时间点的有界观察，不是市场验证、用户数量或持续需求证明。
- 转述必须保留 `observed_at`；若 `active: false`，必须同时保留 `ended_at` 与 `observed_at`。
- 向用户说明灵感时，保留每条来源的时间边界与最强反方。
- Product Hunt 公开 feed 没有票数，不得推断或声称热度。
- `latest.json` 的卡片数组为空，表示当日完整流程成功但没有选出合格灵感；这是有效结果，不是抓取错误。
