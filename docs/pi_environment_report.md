# Pi Environment Report

Generated on 2026-03-30 from the Raspberry Pi host `rpi4`.

## System Summary

- Hostname: `rpi4`
- OS: Debian GNU/Linux 12 (bookworm)
- Kernel: `Linux rpi4 6.12.25+rpt-rpi-v8 #1 SMP PREEMPT Debian 1:6.12.25-1+rpt1 (2025-04-30) aarch64 GNU/Linux`
- Architecture: `aarch64`

## Toolchain

- Python: `Python 3.11.2`
- Node.js: `v22.22.0`
- npm: `10.9.4`

## Camera Detection

- Installed camera tools:
  - `rpicam-hello`: `/usr/bin/rpicam-hello`
  - `libcamera-hello`: `/usr/bin/libcamera-hello`
  - `vcgencmd`: `/usr/bin/vcgencmd`
- Camera probe result: `No cameras available!`
- Video device nodes present:
  - `/dev/video10`
  - `/dev/video11`
  - `/dev/video12`
  - `/dev/video13`
  - `/dev/video14`
  - `/dev/video15`
  - `/dev/video16`
  - `/dev/video18`
  - `/dev/video19`
  - `/dev/video20`
  - `/dev/video21`
  - `/dev/video22`
  - `/dev/video23`
  - `/dev/video31`
- Assessment: the Pi camera stack is installed, but no active camera was detected during setup.

## Serial and USB Detection

- Enumerated serial devices: none
- `lsusb` devices detected:
  - `0781:5581` SanDisk Ultra
  - `1d6b:0003` Linux Foundation 3.0 root hub
  - `2357:0120` TP-Link Archer T2U PLUS
  - `2109:3431` VIA Labs Hub
  - `1d6b:0002` Linux Foundation 2.0 root hub

## Pico and Pico W Detection

- Raspberry Pi Pico or Pico W over USB: not detected
- Evidence:
  - No `ttyACM*` or `ttyUSB*` serial devices were present
  - No Raspberry Pi USB vendor entry appeared in `lsusb`
  - No recent `dmesg` lines matched Pico, RP2040, or USB serial attachment patterns

## Development Implications

- Week 2 should start in prerecorded-video mode until a camera is attached.
- Weeks 3 and 4 should begin with host-side mocks or simulated transport until a Pico or Pico W is connected.
- The current Pi software environment is strong enough for Python, Node-based tooling, and camera-stack development without extra base setup.
