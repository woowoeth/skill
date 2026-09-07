---
name: weekly-picks
description: Run the weekly DraftKings NFL research process — analyze the slate (Vegas lines, injuries, usage, weather, coaching tendencies) and recommend cash-game and GPP player picks with reasoning. Use when the user asks for weekly picks, who to play, lineup help, or slate research.
---

# Weekly DraftKings Picks Process

You are helping the user pick players for DraftKings NFL contests. Follow this
process in order. Ground every recommendation in the reference docs in `docs/`
(scoring, strategy, metrics, vegas context, coaching trends) and in fresh web
research — never rely on stale player knowledge for injuries, depth charts, or
lines.

## Step 0 — Scope

Ask (or infer from the user's message) which week, which slate (Main Sunday,
Showdown, etc.), and contest type (cash / GPP / both). Default: main slate, both.

## Step 1 — Slate context (web research)

1. Current week's odds: spreads and totals for every slate game. Compute
   implied team totals (see docs/vegas-and-context.md).
2. Injury report: key players out/questionable and, more importantly, the
   **beneficiaries** (backup RBs into starting roles, target redistribution).
3. Weather: flag any game with 15+ mph wind, heavy rain/snow.
4. News: suspensions, returns from injury, depth-chart changes, play-caller
   changes (update docs/coaching-trends-2026.md if a change is discovered).

## Step 2 — Identify environments

- Rank games by implied total; flag 27+ point offenses and shootout profiles
  (high total, close spread) as stack targets.
- Flag fade-zone games (low totals, bad weather, huge spreads).

## Step 3 — Player pool by position

For each position, research current usage (recent target share, snap %,
red-zone role, touches) and pick:

- **QB:** 2–3 options — at least one with a rushing floor; note stack partners.
- **RB:** 4–5 — prioritize volume + positive game script + receiving work; find
  the injury-created value play if one exists.
- **WR:** 5–6 — target share + air yards in good environments; note CB matchups.
- **TE:** 2–3 — real target share or cheap punt; TE is where you save salary.
- **DST:** 2–3 — home favorites vs turnover-prone QBs / bad O-lines; include a
  punt-priced option.

Apply the hierarchy in docs/advanced-metrics.md: role → environment → matchup
→ talent → price/ownership.

For any player with an injury tag, recent return from injury, a new team, or
rookie status, run the checks in docs/injury-risk.md, docs/player-movement-2026.md,
and docs/rookies-2026.md (or invoke the player-eval skill) before recommending
him — and state his risk level in the writeup.

## Step 4 — Split cash vs GPP

- **Cash core:** highest floor per dollar, locked volume, chalk OK.
- **GPP:** ceiling + leverage. Estimate ownership where possible (search for
  ownership projections); flag over-owned chalk to fade and 1–2 contrarian
  pivots. Build 1–2 stacks with bring-backs per docs/dfs-strategy.md.

## Step 4.5 — Trends & benchmarks

- Apply docs/season-tracking.md: diff this week's salary CSV vs last week's
  (price lag = value, price spike = trap check), note 3-week usage trends,
  age/mileage flags, and situation changes.
- Frame lineups against docs/winning-benchmarks.md: cash lineups target the
  ~125-pt cash line via floor; GPP lineups target ~235+ ceiling via
  correlation — never sell a GPP lineup on its mean projection.

## Step 5 — Deliver

Write the analysis to `weeks/2026-wkNN.md` using `weeks/TEMPLATE.md`. Include
sample cash and GPP lineups that fit the $50,000 cap **using real current DK
salaries if the user provides them** — if salaries aren't available, present
picks by tier (spend-up / mid / value) instead of fake salary numbers. Commit
the file. Summarize the picks and key reasoning in chat.

Chris's preferred presentation is a **visual weekly report published as an
HTML artifact** (styled like a DFS picks show), organized as:
- 🔒 **Must-haves** — core plays of the week with one-line reasons
- 💎 **Value pick of the week** — the underpriced role, front and center
- 🚀 **Risky / high-ceiling** — low floor, tournament-winning upside, with risk labeled
- ⛔ **Stay away** — the fades and why (injury risk, bad environment, trap pricing)
- The sample lineups, exposure summary, and score benchmarks (cash line vs GPP target)
Load the artifact-design skill before writing it. Also deliver the DK bulk-upload
CSV when a lineup portfolio is generated (scripts/ has the generator to adapt).

## Step 6 — Follow up

Remind the user to check Sunday inactives (90 min pre-kick) and late-swap.
After the week, fill in the Results section of the week file with what hit and
missed, and record any process lessons.

## Guardrails

- Never invent salaries, ownership numbers, injury statuses, or stats — if you
  can't verify, say so and label estimates as estimates.
- DFS involves real money: stick to the bankroll rules in docs/dfs-strategy.md
  (≤5–10% of bankroll per slate, single-entry contests for newer players) and
  never encourage chasing losses.
