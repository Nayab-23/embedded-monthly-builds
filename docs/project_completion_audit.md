# Project Completion Audit

Evidence basis: git history, repo contents on the Raspberry Pi, documented run commands, and tests already exercised during the March 30-31 reconciliation work.

## Completion Table

| Repo | Status Category | Completion Estimate | What Is Implemented | What Is Missing | What Is Deferred | What “Done” Means |
| --- | --- | --- | --- | --- | --- | --- |
| `embedded-linux-device-supervisor` | late-stage | 84% | FastAPI backend, SQLite alerts/events, dashboard, service health page, systemd unit, tests, deployment docs | longer soak validation, richer operator config/reporting, deeper recovery-hook verification | physical GPIO heartbeat wiring, deployment hardening beyond local Pi | stable long-run service, recovery behavior verified, polished operator/demo workflow |
| `pi-edge-vision-event-detector` | late-stage | 79% | source abstraction, motion/event pipeline, recording, SQLite, dashboard, config page, systemd unit, tests | stronger retention/storage visibility, more performance polish, richer service health surfacing | hardware-specific camera tuning, accelerated object detection path | long-run stable capture service, operator-friendly retention health, polished demo package |
| `pico-rtos-sensor-hub` | mid-build | 58% | Pico SDK + FreeRTOS workspace, host monitor/dashboard, simulator path, flash/build helpers, tests, hardware docs | verified real-hardware flash/run, deeper firmware-side validation, more host-side session reporting | heavy toolchain bootstrap on daily path, real Pico bring-up until hardware is attached | simulator and hardware paths both validated, build artifact produced on demand, bring-up flow exercised on hardware |
| `peripheral-protocol-workbench` | early-stage | 28% | frame encode/decode, loopback transport, replay demo, protocol tests | streaming parser, serial/UART transport, session logging, operator inspection tooling | real CAN/I2C/SPI hardware adapters | bounded protocol workbench with parser, transport, replay, fault injection, and operator review surface |

## Evidence Notes

- `embedded-linux-device-supervisor`
  - Recent commits show backend, dashboard, docs, tests, and cleanup work.
  - The repo contains `backend/`, `templates/`, `static/`, `systemd/`, and test coverage.
- `pi-edge-vision-event-detector`
  - Recent commits show detection, storage, dashboard/API, deployment docs, and sample demo assets.
  - The repo contains `app/`, `templates/`, `static/`, `systemd/`, and non-camera tests.
- `pico-rtos-sensor-hub`
  - Recent commits show firmware architecture, host monitor/dashboard, simulator-first recovery, and Pi validation.
  - The repo contains real `firmware/src/*.c` files plus host-side Python tooling and tests.
- `peripheral-protocol-workbench`
  - Only two commits exist so far, and the repo still has a narrow scope.
  - The repo currently contains core protocol files, a replay demo, and limited tests.
