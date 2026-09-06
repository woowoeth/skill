---
name: avo
description: Run an AVO evolutionary search where you are the variation operator. Use when the user asks to evolve, optimise, or improve a program against a benchmark with AVO — "run avo on game2048", "evolve the attention kernel", "continue the avo run", "do 10 more steps". Drives the loop via the avo MCP tools or the avo CLI.
---

# Driving an AVO run

You are the variation operator in an evolutionary search:
`Vary(P_t) = Agent(P_t, K, f)`. AVO owns the lineage, the scoring, and the
commit policy. You own the thinking.

Use the `avo_*` MCP tools if they are available. Otherwise use the CLI
(`avo start`, `avo prompt`, `avo eval`, `avo submit`, `avo supervisor`,
`avo status`, `avo plot`) — the operations are identical.

## The loop

1. **Start or resume.** `avo_start_run` for a new run; `avo_status` to see where
   an existing one is. If the user did not say how many steps, ask, or pick a
   number and say what you picked.

2. **Read the prompt.** `avo_next_step` returns the lineage `P_t`, the index of
   the knowledge base `K`, the contract for `f`, and any pending supervisor
   redirect. Read it properly — it is the whole brief, and it changes every step.

3. **Do the work.** Edit files under `work/`. Read from `kb/` when you need to;
   nobody has read it for you. Inspect earlier versions with ordinary git
   (`git log --oneline`, `git show v7:file`, `git diff v6 v7`) — the lineage is
   the work tree's history.

4. **Measure.** `avo_evaluate` (or `./avo-eval`) as often as you like; it does
   not touch the lineage. An unmeasured change is a guess.

5. **Submit.** `avo_submit` with a one-line summary of what changed and its
   measured effect. AVO scores the tree and either commits it as the next
   version or reverts it. If it will be rejected and you know it, either fix it
   or `avo_revert` first — ending on a measured regression wastes the step.

6. **Handle a stall.** When `avo_submit` reports `supervisor_recommended`, call
   `avo_supervisor_brief`, answer it yourself with fresh intent — read the whole
   trajectory, work out what class of change has not been tried — and file the
   result with `avo_record_supervisor`. It is injected into the next step.

7. **Repeat**, then `avo_plot` and report.

## How to actually be good at this

**One substantial change per step.** The commit policy admits one version per
step, so bundling three ideas means you cannot tell which one worked, and the
paper's own ablation methodology (`git diff v6 v7` against the metric delta)
stops working.

**Read the knowledge base before the second step, not the tenth.** It exists so
you do not have to rediscover standard technique. In the paper this is the whole
difference between the agent and a naive mutation operator.

**Use the per-configuration metrics, not just the aggregate.** A change that
helps one configuration and hurts another is a blocking or threshold problem
with a specific cause; the geometric mean alone hides it.

**Maintain `NOTES.md`.** Dead ends especially. You will not remember them next
step — there is no next step for you, only a new session reading what you left.

**Do not touch the lineage.** No `git commit`, `git reset`, or `git checkout`
inside `work/`. AVO owns it, and a manual commit desynchronises the score log.

**Report honestly.** If the score went down, say so with the numbers. A run
where three of ten steps were accepted is a normal run — the paper explored
500+ directions to commit 40 versions.

## Reporting back

Give the user: steps taken, acceptance rate, seed score → best score, how that
compares to the baselines, and what the agent (you) actually discovered. The
discoveries are the interesting part; the number is just evidence.
