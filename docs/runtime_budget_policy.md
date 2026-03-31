# Runtime Budget Policy

The month runner must prefer incremental progress over expensive provisioning.

## Rules

- no single automation step may block longer than the configured per-step budget
- heavy provisioning commands are deferred instead of run by default
- simulator-first validation is preferred when hardware or toolchains are absent
- deferred work is recorded in reports and left for an explicit future session

## Current Budget

- maximum single step runtime: 300 seconds
- heavy command patterns deferred:
  - `bootstrap_pi.sh`
  - `apt-get update`
  - `apt-get install`
  - `install_firmware_toolchain.sh`
  - `gcc-arm-none-eabi`
  - `west init`
  - `brew install`

## Practical Effect

- the daily runner can still run tests, smoke checks, dashboards, and simulator workflows
- long SDK or toolchain installs no longer consume an entire day by accident
- timed-out setup work is reported as deferred so the next run can continue cleanly
- project progress remains meaningful even on a hardware-limited or time-bounded Raspberry Pi
