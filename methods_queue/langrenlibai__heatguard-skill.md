---
name: heatguard-skill
description: Diagnose macOS thermal pressure, operate the bundled Heatguard watcher, and safely clean only orphaned tasks previously launched with heatguard run. Use when asked why a Mac is hot, to reduce heat, install or inspect Heatguard, or protect automation jobs from leaked child processes. Do not use it as a generic process killer or treat PPID 1 as proof of an orphan.
---

# Heatguard

Use the bundled native tool for durable monitoring and managed-task cleanup. Use ordinary macOS diagnostics for live heat attribution. These are separate workflows: thermal pressure never proves that a process is orphaned.

## Route the request

- For “why is this Mac hot?” or “cool it down,” run `scripts/collect-diagnostics.sh`. Read [references/diagnostics.md](references/diagnostics.md) when interpreting sustained load or choosing a mitigation.
- For installing, starting, checking, or uninstalling Heatguard, read [references/operations.md](references/operations.md). Build and test before installing.
- For any process termination or orphan-cleanup decision, first read [references/safety-model.md](references/safety-model.md). Use `scripts/inspect-process.sh PID` for targeted identity and process-group inspection.
- To protect a long-running command, launch it as `heatguard run -- <command>`. Do not retroactively register an arbitrary existing process.

## Essential behavior

- Report Apple `ProcessInfo.thermalState` as `nominal`, `fair`, `serious`, or `critical`. Do not invent CPU/GPU Celsius values when macOS does not expose them.
- Treat `diagnose` as read-only sampling. The binary does not control fans, change clock speeds, or kill applications because they are hot.
- Automatic cleanup applies only to records created by `heatguard run` whose owner is gone and whose UID, PID start time, original PGID, marker token, marker device/inode, and in-group member identities still match.
- Programs that deliberately daemonize with `setsid` or move descendants to another PGID are outside managed coverage. Report those descendants as unmanaged residuals; do not imply that Heatguard will discover or clean them automatically.
- `audit` may list same-user `PPID=1` processes, but it never signals them. `PPID=1`, high CPU, age, or a process name alone is not proof of an orphan.
- If any identity read or verification fails, leave the process untouched and report the uncertainty.

## Live cooling workflow

1. Collect read-only evidence first. Compare more than one CPU sample and inspect `pmset` assertions for screen, video, microphone, or sleep-prevention activity.
2. Separate active foreground work from stale background work. Explicitly protect Codex, terminals, installers, builds, meetings, recordings, and user-named applications.
3. Explain the exact candidate, PID/PGID, age, parent, command purpose, and expected impact. For any unmanaged process, obtain explicit confirmation after this disclosure before signaling it, unless the user already named that exact PID/PGID and requested termination. Always ask again before closing an interactive app or using `SIGKILL`.
4. Prefer app-level quit or IPC. Otherwise send `SIGTERM` only to a freshly revalidated PID or a fully enumerated, isolated process group.
5. Wait, then re-read identity. Use `SIGKILL` only with explicit approval and only if the same verified target ignored graceful termination.
6. Re-run the thermal and load checks. Report what stopped, whether the thermal state changed, and what remains active.

Never use `pkill -f`, fuzzy process-name matching, or an unverified negative PID. Do not run Heatguard as root.
