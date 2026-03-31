# Recovery Strategy

## Principles

- never wipe project repos
- never hard-reset a dirty repo automatically
- prefer recording an issue and continuing in a degraded mode
- always write state and reports even if a build or test step fails

## Daily Runner Recovery Rules

1. Acquire a lock before doing work.
2. Snapshot the environment to `state/last_environment.json`.
3. Load `state/current_state.json`.
4. Detect missing repos, dirty repos, auth gaps, and missing hardware.
5. If the active project repo is missing, record the failure and continue with reporting.
6. If a command fails, capture the exit code and stderr summary in the daily report.
7. If a command exceeds the runtime budget, mark it deferred and continue.
8. If AI mode is unavailable, execute deterministic fallback actions instead of stopping.
9. Update the next-run pointer and save state before exit.

## Git Recovery

- clean repo: fetch and fast-forward pull when possible
- dirty repo: skip auto-pull and record the reason
- push failure: keep the commit locally, note the failure in the report, and retry on the next run

## Hardware Recovery

- no camera: use sample-video or non-camera tasks in the relevant project
- no Pico: use simulator mode and host-side validation
- no microcontroller for Week 4: use simulated peripheral node and replay tooling

## AI Recovery

When AI-assisted generation is unavailable, the month runner continues using deterministic backlog mode:

- run tests and build checks
- regenerate reports and environment snapshots
- execute simulator-mode smoke tests
- rotate through manifest-defined maintenance commands
- update progress logs, summaries, and backlog status

The month therefore keeps producing validation, documentation, and operational progress rather than stalling.
