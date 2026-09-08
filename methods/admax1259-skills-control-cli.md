---
name: control-cli
description: Exercise or profile an interactive CLI or TUI with a repeatable terminal harness, captured state, and bounded input steps.
---

# Control a CLI

Reuse the repository's terminal tests or demo harness first. Otherwise select tools actually provided by the host: a managed terminal session, tmux, Expect, or a PTY library. POSIX PTY examples do not imply Windows support; use a host-supported equivalent or explain the limitation.

1. Identify the executable, arguments, working directory, environment, and target flow. Inspect commands before running them and use disposable test data.
2. Start an owned session with a deadline and record its process/session ID. A pipe may not reproduce TUI behavior; use a PTY when the program relies on terminal detection, interactive input, or resize events.
3. Capture current output before sending input. Send one intentional action, then wait for a specific prompt/state before the next. Record input, output, exit status, elapsed time, and any timeout.
4. Handle EOF and child exit explicitly. Polling an empty stream forever is not a valid wait. If a test hangs, capture useful state before interrupting that owned process.
5. For performance claims, compare equivalent baselines and treatment with repeated measurements. Keep inspector endpoints bound locally; use existing profiling tools rather than adding global configuration.
6. Clean up owned processes, descriptors, and temporary sessions in a finally/cleanup path. Preserve user-owned terminals and requested evidence.

Do not type credentials or destructive production commands into a test session without task-specific authorization. A successful process exit does not prove layout or interaction correctness; inspect the actual behavior. Report unavailable terminal controls separately from product failures.
