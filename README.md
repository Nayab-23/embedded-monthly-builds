# Embedded Monthly Builds

This repository is the canonical control and orchestration repo for an autonomous four-project embedded/computer-engineering month on the Raspberry Pi. It tracks the reconciled plan, project manifests, saved state, daily and weekly reports, recovery logic, and the single scheduler that should remain active for the rest of the month.

This repo intentionally does not absorb the weekly project histories. Each project remains an independent git repo under `projects/`, while this control repo tracks where those repos live, what state each one is in, and what the next daily run should do.

## Canonical Status

- Canonical control repo: `embedded-monthly-builds`
- Canonical local path: `/home/nayab/embedded-monthly-builds/embedded-monthly-builds`
- Non-canonical control repo: none detected
- Authoritative scheduler: `embedded-monthly-builds-daily.timer`

## Reconciled Project Lineup

| Week | Project | Main Outcome |
| --- | --- | --- |
| 1 | Embedded Linux Device Supervisor | A Pi-hosted service supervisor with health checks, recovery logic, and observability |
| 2 | Edge Vision Event Detector | An on-device vision pipeline that captures and classifies edge events |
| 3 | Pico RTOS Sensor Hub | An RP2040/Pico firmware stack with FreeRTOS tasks, host-side telemetry tooling, and simulator fallback |
| 4 | Peripheral Protocol Workbench | A transport and protocol workbench for packet tooling, serial abstractions, replay, and fault injection |

## Repository Layout

- `docs/`: audit reports, migration decisions, recovery notes, and scheduler setup
- `manifests/`: authoritative project manifests and automation metadata
- `state/`: persisted month state, environment snapshots, and runner locks
- `templates/`: daily and weekly report templates used by the runner
- `reports/`: generated daily and weekly automation outputs
- `progress/`: operator-facing daily notes and migration-day logs
- `projects/`: local clones of the weekly project repos, ignored by this control repo
- `scripts/`: orchestration scripts, environment detection, scheduler installation, and legacy helpers

## Operating Model

1. `scripts/run_daily_cycle.py` is the one authoritative day runner.
2. `scripts/run_weekly_closeout.py` generates recruiter-friendly summaries and advances weekly state when appropriate.
3. `scripts/detect_environment.py` records current hardware, tooling, and auth facts so the runner can choose real-hardware or fallback paths.
4. AI-assisted mode is optional; deterministic fallback mode is mandatory and should never stall the month.
5. Weekly project repos keep their own code and history. This control repo stores the state machine and coordination logic.

## Current Progress Snapshot

- Week 1 `embedded-linux-device-supervisor`: complete enough to treat as finished and maintenance-ready
- Week 2 `pi-edge-vision-event-detector`: complete enough to treat as finished and maintenance-ready
- Week 3 `pico-rtos-sensor-hub`: active and late-stage; simulator-first Pi validation is working and heavy firmware provisioning is deferred
- Week 4 `peripheral-protocol-workbench`: scaffolded and waiting for the week transition

The saved month state therefore resumes at an inferred equivalent of Week 3, Day 6 rather than restarting from Day 1.

## Quick Start

```bash
./scripts/detect_environment.py --write
./scripts/run_daily_cycle.py --write-state
```

To install the scheduler on the Raspberry Pi:

```bash
./scripts/install_scheduler.sh
```

Useful documents:

- [`docs/reconciliation_audit.md`](docs/reconciliation_audit.md)
- [`docs/migration_decisions.md`](docs/migration_decisions.md)
- [`docs/current_month_plan.md`](docs/current_month_plan.md)
- [`docs/scheduler_setup.md`](docs/scheduler_setup.md)
- [`docs/recovery_strategy.md`](docs/recovery_strategy.md)
- [`docs/runtime_budget_policy.md`](docs/runtime_budget_policy.md)
