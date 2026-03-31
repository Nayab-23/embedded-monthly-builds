# Monthly Plan

This plan assumes one substantial project per week, a Raspberry Pi as the main host platform, and GitHub-backed tracking for every deliverable. Each week is structured as a 7-day sprint with a working demo by the end of Day 7.

## Week 1: Embedded Linux Device Supervisor

### Project Objective

Build a resilient device-supervisor stack for Raspberry Pi that monitors long-running services, detects unhealthy states, restarts failed processes, records incident history, and exposes a small local control interface for operators.

### Core Features

- Service registry with configurable health checks, restart policies, and start order
- Process supervision for Python, shell, and systemd-managed workloads
- Event logging with restart history and reason codes
- Local status API or CLI for service state, uptime, and last failure
- Fault-injection mode to validate restart and recovery behavior
- Optional GPIO LED or buzzer indicator for unhealthy system states

### System Architecture

- Supervisor daemon written in Python with a declarative service config
- Health-check workers that probe processes, HTTP endpoints, or heartbeat files
- Local state store for incidents, counters, and timestamps
- Operator interface through a CLI and lightweight local dashboard
- systemd unit file to keep the supervisor itself managed and restartable

### Hardware Assumptions

- Raspberry Pi 4 or newer with Raspberry Pi OS or Debian-based Linux
- Network connectivity for pulling dependencies and optional dashboard access
- Optional LED, button, or buzzer on GPIO for physical status feedback

### Fallback Mode If Hardware Is Missing

Run entirely in software with mock services that intentionally hang, crash, or fail health checks. Use the terminal dashboard and local logs instead of GPIO indicators.

### 7-Day Milestone Breakdown

1. Day 1: Define scope, incident model, config schema, repo scaffold, and service manifest format.
2. Day 2: Implement process launch, shutdown, restart policy, and structured logging.
3. Day 3: Add health checks for command, file, and HTTP endpoint targets.
4. Day 4: Add status CLI or web dashboard and persist incident history.
5. Day 5: Implement fault injection, restart backoff, and unhealthy-state signaling.
6. Day 6: Add tests, systemd integration, packaging, and operator docs.
7. Day 7: Run failure demos, polish README, record demo artifacts, and finalize resume bullet.

### Success Criteria

- The supervisor automatically restarts failed services and logs why the recovery happened.
- At least three independent services can be registered with different health-check types.
- Recovery latency is low enough to clearly demonstrate automated resilience in a live demo.
- Operators can inspect status and incident history without reading raw process output.

### Demo Plan

- Start three managed services, including one intentionally fragile workload.
- Trigger a crash and a health-check failure.
- Show automatic detection, restart, and incident logging.
- Show the local status interface and system summary.

### Resume Bullet Draft

- Built an embedded Linux device supervisor on Raspberry Pi that monitored multi-service workloads, detected failures, auto-restarted unhealthy processes, and exposed a local operations interface for resilience debugging.

## Week 2: Edge Vision Event Detector

### Project Objective

Create an edge-vision pipeline on Raspberry Pi that watches a live or prerecorded feed, detects meaningful events, saves evidence, and produces a compact operator view of what happened and when.

### Core Features

- Camera or prerecorded-video ingest path
- Motion gating to reduce unnecessary inference
- Event classification using classical CV, lightweight ML, or both
- Snapshot and clip capture for detected events
- Local storage policy with timestamps and retention limits
- Event timeline or dashboard for reviewing detections

### System Architecture

- Capture layer for Pi camera, USB camera, or prerecorded video stream
- Preprocessing and motion-gating stage
- Detection stage using a lightweight model or OpenCV heuristics
- Event manager for snapshot storage, clip trimming, and metadata persistence
- Review interface that lists events, labels, scores, and file locations

### Hardware Assumptions

- Raspberry Pi with camera support packages installed
- Pi Camera module or USB webcam preferred
- Local storage with enough capacity for image and clip retention

### Fallback Mode If Hardware Is Missing

Use prerecorded clips and CPU-only inference or motion heuristics. Build the pipeline against a repeatable test-video corpus so development can continue even with no attached camera.

### 7-Day Milestone Breakdown

1. Day 1: Define event types, capture abstraction, dataset folder layout, and repo scaffold.
2. Day 2: Implement ingest path for camera and prerecorded clips with frame timestamping.
3. Day 3: Add motion detection, region-of-interest handling, and event gating.
4. Day 4: Integrate classifier or heuristic detector and persist event metadata.
5. Day 5: Add snapshot and clip export with retention policy.
6. Day 6: Build event-review dashboard or CLI report, then add tests and sample fixtures.
7. Day 7: Run end-to-end demo on live or prerecorded input, document performance, and finalize writeup.

### Success Criteria

- The system detects at least one meaningful event class with repeatable output.
- Event records include timestamps, labels, confidence or heuristic score, and saved evidence.
- The pipeline runs locally on the Pi without needing a cloud backend.
- The demo clearly shows end-to-end capture, detection, and review.

### Demo Plan

- Feed the system a live camera stream or prerecorded video with known events.
- Show motion gating and event detection in real time or near real time.
- Open saved snapshots or clips and review the event timeline.
- Report CPU usage, throughput, and any detection tradeoffs.

### Resume Bullet Draft

- Developed an edge-vision event detector on Raspberry Pi that ingested camera or prerecorded video, gated inference with motion detection, classified events locally, and stored timestamped evidence for review.

## Week 3: Pico RTOS Sensor Hub

### Project Objective

Build an RP2040/Pico firmware project with an RTOS-based task model that samples sensors, timestamps measurements, communicates with the Raspberry Pi, and demonstrates robust concurrent embedded design.

### Core Features

- FreeRTOS or equivalent RTOS task scheduling on Pico or Pico W
- Sensor acquisition task with deterministic sampling intervals
- Queue-based message passing between acquisition, comms, and diagnostics tasks
- USB serial or UART transport to stream structured telemetry to the Pi
- Heartbeat, watchdog, and fault-state reporting
- Host-side parser or dashboard to inspect incoming telemetry

### System Architecture

- RTOS scheduler running acquisition, comms, and diagnostics tasks
- Driver layer for I2C, SPI, ADC, or mock sensor sources
- Message queue for decoupled sensor read and host transmit stages
- Host utility on the Pi for parsing telemetry and recording traces
- Optional test harness with fake drivers for repeatable CI-like checks

### Hardware Assumptions

- Raspberry Pi Pico or Pico W with USB connection to the Pi
- One or more simple sensors such as temperature, IMU, light, or potentiometer
- Breadboard and jumper wires for quick experiments

### Fallback Mode If Hardware Is Missing

Build the firmware with mocked sensor drivers and verify the host protocol using a simulator on the Pi. Keep the RTOS tasking, queues, and message format real even if sensor values are synthetic.

### 7-Day Milestone Breakdown

1. Day 1: Choose RTOS stack, define telemetry protocol, scaffold firmware and host tools.
2. Day 2: Bring up RTOS tasks, heartbeat, and logging over serial.
3. Day 3: Implement one real or mocked sensor driver and queue-based telemetry.
4. Day 4: Add more sensors or richer telemetry plus host-side parser.
5. Day 5: Add watchdog, fault handling, and reconnect behavior.
6. Day 6: Add build automation, unit tests for host parser, and wiring documentation.
7. Day 7: Record end-to-end demo from sensor read to host visualization and finalize summary.

### Success Criteria

- The firmware demonstrates true concurrent task structure rather than a single loop.
- Telemetry is timestamped, structured, and readable on the Pi side.
- Fault handling shows watchdog or degraded-mode behavior under injected failures.
- The system can be demoed with either real hardware or a faithful mock path.

### Demo Plan

- Show RTOS tasks starting and reporting heartbeat over serial.
- Stream sensor telemetry to the Pi and display it in a parser or dashboard.
- Trigger a simulated sensor failure and show recovery or degraded-mode behavior.
- Review the task architecture and protocol design in the README.

### Resume Bullet Draft

- Built an RTOS-based RP2040 sensor hub with concurrent acquisition and communications tasks, structured telemetry streaming to Raspberry Pi, and watchdog-backed fault handling for robust embedded operation.

## Week 4: micro-ROS Peripheral Controller

### Project Objective

Create a distributed control stack where the Raspberry Pi runs ROS 2 and a microcontroller runs micro-ROS, allowing sensors or actuators to be exposed as ROS topics, services, and safety-aware peripherals.

### Core Features

- ROS 2 workspace on the Pi with launch files and operator nodes
- micro-ROS agent bridging serial transport to the microcontroller
- Peripheral node that publishes state and subscribes to commands
- Failsafe behavior when commands stop arriving or invalid states appear
- Telemetry logging and diagnostic topics
- Demo application such as LED state control, servo actuation, or relay toggling

### System Architecture

- ROS 2 nodes on the Pi for command generation, diagnostics, and visualization
- micro-ROS agent bridging serial data between the Pi and MCU
- MCU firmware exposing topics, parameters, and optional services
- Peripheral abstraction layer for LEDs, motors, relays, or simulated devices
- Test mode on the Pi that replays command sequences for regression checks

### Hardware Assumptions

- Raspberry Pi with ROS 2-compatible environment
- Pico, Pico W, or another supported microcontroller for micro-ROS firmware
- At least one peripheral such as LED, servo, relay, or motor driver

### Fallback Mode If Hardware Is Missing

Run the ROS 2 side and a simulated peripheral endpoint on the Pi, keeping the topic, service, and safety logic intact. Treat the hardware layer as a mock transport until a board is connected.

### 7-Day Milestone Breakdown

1. Day 1: Set up ROS 2 workspace, define control interface, and choose peripheral target.
2. Day 2: Bring up micro-ROS agent and basic Pi-side publisher and subscriber nodes.
3. Day 3: Implement MCU-side peripheral node and command decoding.
4. Day 4: Add state feedback, diagnostics, and failsafe behavior.
5. Day 5: Add launch files, scripted demos, and host-side validation tools.
6. Day 6: Add documentation, tests, and performance or latency measurements.
7. Day 7: Run live demo, capture video or terminal proof, and produce polished final summary.

### Success Criteria

- Commands flow from ROS 2 on the Pi to the peripheral controller and state comes back reliably.
- The system fails safe when transport is interrupted or bad commands arrive.
- Launching the demo is repeatable from documented scripts or launch files.
- The README explains how to run both the real-hardware and simulated path.

### Demo Plan

- Launch ROS 2 nodes and the micro-ROS agent.
- Send commands to the peripheral controller and observe state updates.
- Interrupt transport or stop command publishing to demonstrate failsafe behavior.
- Show logs, launch files, and the final architecture diagram or summary.

### Resume Bullet Draft

- Implemented a micro-ROS peripheral controller that bridged ROS 2 on Raspberry Pi to MCU-driven peripherals, added fail-safe command handling, and exposed device state through a reproducible robotics control workflow.
