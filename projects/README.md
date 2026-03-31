# Projects Directory

This directory is reserved for local clones of the weekly project repos. Each project remains its own git repository and is intentionally ignored by the control repo.

Canonical project mapping:

- `embedded-linux-device-supervisor`
- `pi-edge-vision-event-detector`
- `pico-rtos-sensor-hub`
- `peripheral-protocol-workbench`

The control repo tracks these clones through `manifests/projects/*.json` rather than by embedding them as submodules.
