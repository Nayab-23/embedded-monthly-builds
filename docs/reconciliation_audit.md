# Reconciliation Audit

Audit date: 2026-03-30

## Scope

This audit inspected the Raspberry Pi workspace, the GitHub account `Nayab-23`, existing git repositories, systemd services and timers, cron, and any existing monthly-build automation artifacts.

## Control Repo Findings

| Item | Result |
| --- | --- |
| `embedded-monthly-builds` local wrapper directory | Present at `/home/nayab/embedded-monthly-builds` |
| `embedded-monthly-builds` control repo | Present at `/home/nayab/embedded-monthly-builds/embedded-monthly-builds` |
| `embedded-monthly-autobuilder` local repo | Not found |
| `embedded-monthly-autobuilder` GitHub repo | Not found |
| Control repo GitHub remote | `https://github.com/Nayab-23/embedded-monthly-builds.git` |
| Control repo current status | Two bootstrap commits, no authoritative scheduler, no persisted state machine |
| Control repo confusion | Nested project repos appear as untracked directories because the control repo was not yet configured to ignore local project clones |

## Project Repo Findings

| Target Concept | Actual Repo Name | Local Path on Pi | GitHub URL | Current Status | Next Phase |
| --- | --- | --- | --- | --- | --- |
| Raspberry Pi supervisor | `embedded-linux-device-supervisor` | `/home/nayab/embedded-monthly-builds/embedded-monthly-builds/projects/embedded-linux-device-supervisor` | `https://github.com/Nayab-23/embedded-linux-device-supervisor` | Substantial implementation present locally and remotely; 7 commits; API, dashboard, SQLite, tests, systemd assets | Treat as completed enough for week closeout, with later maintenance only |
| Edge vision detector | `pi-edge-vision-event-detector` | `/home/nayab/embedded-monthly-builds/embedded-monthly-builds/projects/pi-edge-vision-event-detector` | `https://github.com/Nayab-23/pi-edge-vision-event-detector` | Substantial implementation present locally and remotely; 7 commits; dashboard, storage, sample demo asset, tests | Treat as completed enough for week closeout, with later tuning only |
| RTOS sensor hub | `pico-rtos-sensor-hub` | Missing locally on the Pi at audit time | `https://github.com/Nayab-23/pico-rtos-sensor-hub` | Remote repo exists and already contains substantial work, but it had not yet been cloned into the Pi workspace | Clone into the Pi workspace and perform Pi-local build and simulator validation |
| Protocol / transport tooling | `peripheral-protocol-workbench` | Missing | Missing | Not started | Create the repo and schedule it as the remaining week after the current active work closes out |

## Current Progress Inference

- Week 1 is effectively complete.
- Week 2 is effectively complete.
- Week 3 already has substantial implementation in the remote `pico-rtos-sensor-hub` repo, but Pi-local integration has not been performed yet.
- Week 4 has not started.

The most mature Pi-local repos are `embedded-linux-device-supervisor` and `pi-edge-vision-event-detector`.

The correct current active project is therefore `pico-rtos-sensor-hub`, with the month position inferred as the equivalent of Week 3, Day 6.

## Scheduler / Automation Findings

| Area | Result |
| --- | --- |
| systemd monthly timer | Not found |
| systemd monthly service | Not found |
| duplicate month scheduler | Not found |
| cron entries related to monthly build system | Not found |
| unrelated cron entries | Present for `button_listener.py` and `agentlink_data/auto_bid.sh`; left untouched |
| related long-running monthly process | Not found |

The Pi did not already have an installed monthly-build scheduler, so there was no duplicate automation to disable.

## GitHub Auth Findings on the Pi

| Check | Result |
| --- | --- |
| `gh` installed on the Pi | No |
| GitHub SSH auth from the Pi | Not configured; `git@github.com` returned `Permission denied (publickey)` |
| Read access to current GitHub remotes | Works over HTTPS because the repos are public |
| Write path for autonomous pushes | Not ready at audit time; direct GitHub auth on the Pi must be installed for the scheduler to push independently |

## Environment Snapshot

- Existing virtual environments under the month workspace: Week 1 and Week 2 repos only
- Existing Pi-local project services: service files exist inside the project repos, but matching installed systemd units were not present
- Existing progress tracking: one bootstrap progress note at `progress/2026-03-30.md`

## Conclusion

`embedded-monthly-builds` should remain the canonical control repo, but it must be upgraded from a bootstrap tracker into a true orchestrator with:

- manifests for each project
- persisted month state
- environment detection
- a daily runner
- weekly closeout reporting
- recovery documentation
- one authoritative scheduler
