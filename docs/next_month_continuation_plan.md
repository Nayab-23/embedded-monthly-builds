# Next Month Continuation Plan

This plan continues the current repos from their existing state. No project restarts from scratch.

## Repo Priority Order

1. `peripheral-protocol-workbench`
2. `pico-rtos-sensor-hub`
3. `pi-edge-vision-event-detector`
4. `embedded-linux-device-supervisor`

## Week-by-Week Plan

### Week 1

- focus repo: `peripheral-protocol-workbench`
- goals:
  - add stream parsing and resynchronization
  - add serial/UART transport support
  - add session replay/inspection tooling

### Week 2

- focus repo: `pico-rtos-sensor-hub`
- goals:
  - strengthen host-side telemetry session handling
  - keep simulator mode strong
  - prepare real hardware bring-up without blocking on heavy installs

### Week 3

- focus repo: `pi-edge-vision-event-detector`
- goals:
  - add retention/storage health visibility
  - tighten service-health surfacing
  - polish demo workflow and long-run validation

### Week 4

- focus repo: `embedded-linux-device-supervisor`
- goals:
  - polish recovery hooks
  - improve soak/reliability validation
  - refine operator-facing docs and deployment workflow

## Exact Continuation Goals

- `peripheral-protocol-workbench`
  - build the parser/transport/session-review core that is still missing
- `pico-rtos-sensor-hub`
  - continue from the simulator-first host-tooling path already in place
- `pi-edge-vision-event-detector`
  - move from MVP into operational polish
- `embedded-linux-device-supervisor`
  - move from MVP into production-style verification and safeguards

## No-Restart Policy

- keep existing repos, names, and history
- continue from the current file and commit state
- use continuation backlogs from manifests instead of month-one scaffolding
- never reset week/day/project state just because the calendar month changes

## Definition Of Completion For Unfinished Repos

- `peripheral-protocol-workbench`
  - parser, serial transport, replay tooling, and operator review surface all exist
- `pico-rtos-sensor-hub`
  - simulator and host tooling are strong, and the real build/flash path is validated when hardware is present
- `pi-edge-vision-event-detector`
  - retention/service-health polish is complete and deployment/demo flow is clean
- `embedded-linux-device-supervisor`
  - reliability polish, recovery validation, and deployment/operator workflow are complete
