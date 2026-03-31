# AI Execution Layer

The Raspberry Pi now uses the OpenAI API as the primary continuation engine for daily project work.

## Configuration Mechanism

- environment file candidate: `/home/nayab/.openclaw/.env`
- environment variable names:
  - `OPENAI_API_KEY`
  - `OPENAI_BASE_URL`
  - `MONTHLY_BUILDS_OPENAI_MODEL`
  - `OPENAI_MODEL`

Secrets are never written into docs, logs, or committed files.

## How Tasks Are Selected

- the daily runner loads `config/global_config.json`
- unfinished repos are prioritized using the configured order
- the next open backlog item is chosen from each project manifest
- the selected task is written into `state/current_state.json`

## How Prompts Are Formed

- the executor reads only the bounded context files listed on the selected backlog item
- it includes a small repo file snapshot plus the concrete task description
- it instructs the model to:
  - make only the requested incremental change
  - preserve existing architecture
  - avoid secret leakage
  - touch only a small number of files
  - return strict JSON with full file contents

## Validation And Commit Flow

- generated files are applied through the bounded change applier
- destructive rewrites are rejected when they look too large
- repo-local validation commands run before any commit
- if validation fails, the executor restores the original files
- if validation succeeds, the repo is committed and pushed

## Fallback Mode

- if API access fails or AI execution raises an error, `run_daily_cycle.py` falls back to deterministic validation commands
- the backlog selection state is preserved so the next run can retry the same unfinished work
