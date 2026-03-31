# Embedded Monthly Builds

This repository is the parent tracking workspace for a four-week embedded and computer-engineering sprint on the Raspberry Pi. It keeps the monthly plan, operating workflow, reusable setup scripts, and daily progress records in one place while each weekly build can live in its own dedicated project repo under `projects/`.

## Weekly Lineup

| Week | Project | Main Outcome |
| --- | --- | --- |
| 1 | Embedded Linux Device Supervisor | A Pi-hosted service supervisor with health checks, recovery logic, and observability |
| 2 | Edge Vision Event Detector | An on-device vision pipeline that captures and classifies edge events |
| 3 | Pico RTOS Sensor Hub | An RP2040/Pico firmware stack for sensor sampling, task scheduling, and host messaging |
| 4 | micro-ROS Peripheral Controller | A ROS 2 and micro-ROS bridge that controls peripherals from the Pi |

## Repository Layout

- `monthly_plan.md`: the four-week build plan, milestones, and demo targets
- `daily_log_template.md`: the reusable template for end-of-day notes
- `docs/`: workflow guidance and machine-environment reports
- `progress/`: dated daily logs and setup notes
- `projects/`: weekly project repos or pointers to them
- `scripts/`: repeatable automation for repo setup and daily logging

## Operating Rules

1. Pick one weekly project and drive it with the 7-day milestones in [`monthly_plan.md`](monthly_plan.md).
2. Start each work session with `scripts/start_daily_log.sh`.
3. Keep commit volume high enough to show real iteration: minimum 4 commits per day, target 4 to 8.
4. Use clear commit categories: `scaffold`, `feature`, `fix`, `docs`, `test`, `refactor`.
5. Run tests, lint, and build checks before pushing.
6. Update the project README and the daily progress log before ending the session.

## Quick Start

```bash
cd "$(git rev-parse --show-toplevel)"
./scripts/start_daily_log.sh
```

For a new weekly project repo, create or enter the project directory and run:

```bash
../scripts/create_project_repo.sh <repo-name> [public|private]
```

## Suggested Cadence

- Monday: scope and scaffold
- Tuesday to Thursday: feature implementation and instrumentation
- Friday: robustness, tests, and demo polish
- Weekend: docs, demo capture, and resume-ready summary
