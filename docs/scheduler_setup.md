# Scheduler Setup

## Authoritative Units

- Service: `embedded-monthly-builds-daily.service`
- Timer: `embedded-monthly-builds-daily.timer`

These units are the only monthly-build automation that should remain enabled.

## Schedule

The timer is configured to run once per day with `Persistent=true` so missed runs catch up after downtime.

## What the Service Runs

`embedded-monthly-builds-daily.service` executes:

```bash
/bin/bash -lc 'set -a; [ -f /home/nayab/.openclaw/.env ] && . /home/nayab/.openclaw/.env; set +a; exec /usr/bin/python3 /home/nayab/embedded-monthly-builds/embedded-monthly-builds/scripts/run_daily_cycle.py --write-state --select-next-task --use-ai'
```

Working directory:

```text
/home/nayab/embedded-monthly-builds/embedded-monthly-builds
```

Runtime user:

```text
nayab
```

## Installation

Run:

```bash
./scripts/install_scheduler.sh
```

## Operational Notes

- The runner writes state back to `state/current_state.json`.
- The runner selects the next backlog item from unfinished repos before execution.
- The runner uses the OpenAI API as the primary continuation engine and falls back to deterministic validation if AI execution fails.
- Daily reports are written under `reports/daily/`.
- Weekly closeouts are written under `reports/weekly/`.
- The runner uses a file lock to avoid overlapping executions.
- If the active project repo is dirty, the runner records that fact and avoids destructive sync behavior.
- The runner enforces the runtime budget from `manifests/runtime_policy.json` and defers heavy provisioning commands instead of blocking the full day.
