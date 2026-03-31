# Current Month Plan

This is the reconciled month plan after auditing the real state of the Raspberry Pi and GitHub repos on 2026-03-30.

## Status Overview

| Week | Project | Status | Day Equivalent | Notes |
| --- | --- | --- | --- | --- |
| 1 | `embedded-linux-device-supervisor` | Completed enough | 7/7 | Real implementation, tests, docs, and service assets already exist |
| 2 | `pi-edge-vision-event-detector` | Completed enough | 7/7 | Real implementation, tests, docs, and sample demo artifacts already exist |
| 3 | `pico-rtos-sensor-hub` | Active | 6/7 | Pi-local validation now follows a simulator-first path; heavy firmware provisioning is deferred |
| 4 | `peripheral-protocol-workbench` | Scaffolded | 1/7 | New week-4 target replacing the previously planned micro-ROS repo |

## Current Focus

Current active project:

- `pico-rtos-sensor-hub`

Current inferred position:

- Week 3
- Day 6 equivalent

Current objective:

- bring the repo into the Pi workspace
- validate the simulator and host tools on the Pi
- validate or repair the firmware build path on the Pi
- prepare the repo for a clean week closeout

## Planned Next Transition

When Week 3 is validated locally on the Pi and its closeout artifacts are generated, the next active project becomes:

- `peripheral-protocol-workbench`

Week 4 should begin from a clean scaffold with:

- protocol definitions
- transport adapters
- replay and fault-injection tooling
- simulator-first development
