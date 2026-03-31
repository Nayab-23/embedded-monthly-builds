#!/usr/bin/env bash
set -euo pipefail

OWNER="${1:-Nayab-23}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

declare -a REPOS=(
  "${REPO_ROOT}:embedded-monthly-builds"
  "${REPO_ROOT}/projects/embedded-linux-device-supervisor:embedded-linux-device-supervisor"
  "${REPO_ROOT}/projects/pi-edge-vision-event-detector:pi-edge-vision-event-detector"
  "${REPO_ROOT}/projects/pico-rtos-sensor-hub:pico-rtos-sensor-hub"
  "${REPO_ROOT}/projects/peripheral-protocol-workbench:peripheral-protocol-workbench"
)

for mapping in "${REPOS[@]}"; do
  repo_path="${mapping%%:*}"
  repo_name="${mapping##*:}"
  if [[ ! -d "${repo_path}/.git" ]]; then
    continue
  fi
  git -C "${repo_path}" remote set-url origin "git@github.com:${OWNER}/${repo_name}.git"
  printf 'Configured %s -> %s\n' "${repo_path}" "git@github.com:${OWNER}/${repo_name}.git"
done
