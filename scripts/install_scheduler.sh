#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SERVICE_NAME="embedded-monthly-builds-daily"

sudo cp "${REPO_ROOT}/systemd/${SERVICE_NAME}.service" "/etc/systemd/system/${SERVICE_NAME}.service"
sudo cp "${REPO_ROOT}/systemd/${SERVICE_NAME}.timer" "/etc/systemd/system/${SERVICE_NAME}.timer"
sudo systemctl daemon-reload

# Remove any stale alternate month controller if it exists.
if systemctl list-unit-files | grep -q '^embedded-monthly-autobuilder.timer'; then
  sudo systemctl disable --now embedded-monthly-autobuilder.timer || true
fi

sudo systemctl enable --now "${SERVICE_NAME}.timer"
systemctl status "${SERVICE_NAME}.timer" --no-pager
systemd-analyze calendar "$(systemctl show "${SERVICE_NAME}.timer" --property=NextElapseUSecRealtime --value)" 2>/dev/null || true
