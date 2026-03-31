# Codex Usage Workflow

This repository is intended to support one substantial project per week over a four-week embedded-systems sprint. The parent repo tracks planning, environment notes, and progress logs while weekly build repos hold the implementation for each project.

## Expected Workflow

1. Pick the active weekly project from `monthly_plan.md`.
2. Open or create that week's project repo under `projects/`.
3. Start the work session by creating a dated log with `scripts/start_daily_log.sh`.
4. Work against the current day's milestone, not an unbounded task list.
5. Update the project README and the daily progress log before ending the session.

## Daily Execution Rules

- Build against the current milestone for the active week.
- Make a minimum of 4 commits per day.
- Target 4 to 8 commits per day when actively developing.
- Use milestone-sized commits instead of one large end-of-day dump.
- Keep the parent repo updated when plans, decisions, or environment details change.

## Commit Categories

Use these prefixes consistently in commit messages:

- `scaffold`: bootstrapping structure, configs, or skeleton code
- `feature`: new functional behavior
- `fix`: bug fixes and stability patches
- `docs`: README, design notes, demo writeups, progress updates
- `test`: automated tests, fixtures, simulation harnesses
- `refactor`: internal cleanup without intended behavior changes

## Quality Gate Before Push

- Run tests relevant to the project.
- Run lint or formatting checks where available.
- Run the build or firmware compilation path where applicable.
- Verify the README still matches reality.
- Verify the progress log captures the day's work and remaining blockers.

## Recommended Session Pattern

1. Create the daily log.
2. Review the current milestone and success criteria.
3. Implement one narrow change at a time.
4. Commit after each meaningful checkpoint.
5. Run tests and build checks before the final push.
6. Update docs and log files before closing the session.
