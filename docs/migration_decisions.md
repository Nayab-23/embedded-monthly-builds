# Migration Decisions

## Canonical Control Repo

Decision: keep `embedded-monthly-builds` as the sole authoritative control repo.

Reasoning:

- It already exists locally and on GitHub.
- It has the original monthly planning artifacts.
- No competing `embedded-monthly-autobuilder` repo was found locally or remotely.
- Reusing it preserves the existing history and avoids introducing a second control plane.

## Outer Workspace vs Inner Repo

The directory `/home/nayab/embedded-monthly-builds` is only a wrapper workspace. The actual canonical git repository is `/home/nayab/embedded-monthly-builds/embedded-monthly-builds`.

This is not treated as a duplicate control repo.

## Project Repo Handling

Decision: keep weekly projects as independent git repos under `projects/`, but ignore them from the control repo.

Reasoning:

- This preserves each project's history and remote independently.
- It avoids submodule complexity during an autonomous month.
- It removes the current control-repo noise from nested untracked repositories.

## Week 4 Re-scope

Original plan:

- Week 4 was `micro-ROS Peripheral Controller`.

Reconciled plan:

- Week 4 becomes `peripheral-protocol-workbench`.

Reasoning:

- The new target project set explicitly prioritizes the protocol and transport workbench.
- No existing `pi-micro-ros-peripheral-controller` repo or implementation was found to preserve.
- The protocol workbench is a better fit for a deterministic fallback-capable month runner because it can progress without ROS 2 or MCU hardware.

## Current Active Project

Decision: resume on `pico-rtos-sensor-hub`.

Reasoning:

- Weeks 1 and 2 are already substantial enough to count as completed.
- Week 3 already has meaningful implementation in GitHub.
- The missing step is Pi-local integration, validation, and hardening, which is exactly the kind of late-week work the month runner should perform next.

## Scheduler Choice

Decision: install a single systemd timer named `embedded-monthly-builds-daily.timer`.

Reasoning:

- systemd timers are restart-safe and easier to audit than ad hoc cron jobs
- `Persistent=true` covers missed runs after downtime
- the timer can point at one authoritative daily runner script in the canonical control repo

## GitHub Auth on the Pi

Decision: configure direct GitHub push access on the Pi for the month repos using a dedicated SSH key and SSH remotes.

Reasoning:

- the Pi did not have `gh` installed or authenticated
- public HTTPS remotes were only enough for read access
- the autonomous scheduler needs a stable non-interactive push path
