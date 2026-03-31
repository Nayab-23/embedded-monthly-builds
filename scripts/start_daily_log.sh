#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
progress_dir="${repo_root}/progress"

date_input="${1:-$(date +%F)}"

# Use Python for portable date validation on Linux and macOS.
log_date="$(python3 - "$date_input" <<'PY'
from datetime import date
import sys

raw = sys.argv[1]
try:
    parsed = date.fromisoformat(raw)
except ValueError:
    print("", end="")
    raise SystemExit(1)
print(parsed.isoformat())
PY
)" || {
  echo "Date must be in YYYY-MM-DD format." >&2
  exit 1
}

mkdir -p "$progress_dir"

target_file="${progress_dir}/${log_date}.md"

if [[ -f "$target_file" ]]; then
  printf '%s\n' "$target_file"
  exit 0
fi

latest_commit="$(git -C "$repo_root" rev-parse --short HEAD 2>/dev/null || true)"

cat > "$target_file" <<EOF
# Daily Log - ${log_date}

## Today's Goal

- 

## Changes Made

- 

## Files Touched

- 

## Tests Run

- 

## Blockers

- 

## Next Step

- 

## Commit Hashes

- ${latest_commit:-pending}
EOF

printf '%s\n' "$target_file"
