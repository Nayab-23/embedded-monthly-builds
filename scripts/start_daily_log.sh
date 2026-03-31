#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
progress_dir="${repo_root}/progress"
template_path="${repo_root}/templates/daily_log_template.md"
legacy_template_path="${repo_root}/daily_log_template.md"

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

if [[ -f "$template_path" ]]; then
  python3 - "$template_path" "$target_file" "$log_date" "${latest_commit:-pending}" <<'PY'
from pathlib import Path
import sys

template_path = Path(sys.argv[1])
target_path = Path(sys.argv[2])
log_date = sys.argv[3]
latest_commit = sys.argv[4]

content = template_path.read_text()
content = content.replace("{{date}}", log_date)
content = content.replace("{{active_project}}", "manual-session")
content = content.replace("{{week_day}}", "manual-session")
content = content.replace("{{run_mode}}", "manual")
content = content.replace("- control repo:", f"- control repo: {latest_commit}")
target_path.write_text(content)
PY
else
  cp "$legacy_template_path" "$target_file"
fi

printf '%s\n' "$target_file"
