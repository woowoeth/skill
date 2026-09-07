---
name: player-eval
description: Evaluate whether a specific NFL player is worth playing this week and how risky he is — role, environment, matchup, injury risk, and cash vs GPP verdict. Use when the user asks "should I play X", "is X worth it", "how risky is X", or wants two players compared.
---

# Player Evaluation — "Is he worth playing, and how risky?"

Produce a verdict for a specific player (or head-to-head comparison). Always
use fresh web research for current role/injury/lines — never stale knowledge.

**Roster-verification rule (mandatory first step):** confirm the player's
current team and backfield/target competition from the week's DK salary CSV
in `data/` and/or a fresh search BEFORE reasoning about his role. Training
knowledge of rosters is stale; a wrong committee/team assumption invalidates
the whole verdict.

## Gather (web research + docs)

1. **Role right now:** snap share, route participation or opportunity share,
   target share, red-zone usage — last 3 weeks, not season averages. Rising or
   falling?
2. **Environment this week:** implied team total, spread, likely game script,
   pace, weather (docs/vegas-and-context.md).
3. **Matchup:** schedule-adjusted defense vs his *role* (slot/perimeter/RB
   receiving), CB shadow risk, O-line vs D-line (docs/advanced-metrics.md).
4. **Injury risk score:** run the 5-factor table in docs/injury-risk.md
   (designation, injury type, recency, history, role protection) → 0–10.
5. **Regression check:** points vs expected points — is recent production
   backed by usage, or TD luck?
6. **Context flags:** new team/scheme ramp-up (docs/player-movement-2026.md),
   rookie trajectory (docs/rookies-2026.md), coaching tendency
   (docs/coaching-trends-2026.md).
7. **Price & ownership** (if DK salaries/ownership available): points per
   dollar, and is the field over/under on him?

## Deliver: a verdict card

```
PLAYER — pos, team, opp, salary (if known)
Role:        [locked / rising / shaky] — key numbers
Environment: implied total X, script read
Matchup:     [smash / neutral / tough] — why
Injury risk: N/10 — driver
Ceiling:     what has to happen for a 25+ pt game
Floor:       realistic bad outcome
VERDICT:     Cash: play/avoid | GPP: core/leverage/fade — one-line reason
```

Rules of thumb:
- Cash = floor: locked volume + injury risk ≤2 + environment ≥ neutral.
- GPP = ceiling × leverage: a flawed player can be a great GPP play if
  ownership overreacts to the flaw; a great player can be a bad GPP play if
  everyone has him.
- When comparing two players at the same price, the tiebreak order is:
  role security → environment → ceiling path → matchup.
- Never fabricate numbers. If usage data isn't findable, say so and downgrade
  confidence explicitly.
