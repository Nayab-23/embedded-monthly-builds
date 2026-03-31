#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
import os
from pathlib import Path
import platform
import shutil
import subprocess
from typing import Any

from common import repo_root, save_json


def _run(command: list[str], timeout: int = 10) -> tuple[int, str, str]:
    completed = subprocess.run(
        command,
        text=True,
        capture_output=True,
        timeout=timeout,
    )
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def _which(name: str) -> str | None:
    resolved = shutil.which(name)
    return resolved


def _node_version() -> str | None:
    binary = _which("node")
    if not binary:
        return None
    code, stdout, _ = _run([binary, "--version"])
    return stdout if code == 0 else None


def _python_version() -> str:
    code, stdout, _ = _run(["python3", "--version"])
    return stdout if code == 0 else platform.python_version()


def _camera_summary() -> dict[str, Any]:
    video_devices = sorted(str(path) for path in Path("/dev").glob("video*"))
    list_command = None
    for candidate in ("rpicam-hello", "libcamera-hello"):
        if _which(candidate):
            list_command = candidate
            break

    camera_tool_output = None
    if list_command:
        code, stdout, stderr = _run([list_command, "--list-cameras"], timeout=15)
        camera_tool_output = stdout or stderr
        detected = code == 0 and ("Available cameras" in camera_tool_output or "0 :" in camera_tool_output)
    else:
        detected = bool(video_devices)

    return {
        "video_devices": video_devices,
        "tool": list_command,
        "tool_output": camera_tool_output,
        "detected": detected,
    }


def _serial_summary() -> dict[str, Any]:
    serial_devices = sorted(str(path) for path in list(Path("/dev").glob("ttyACM*")) + list(Path("/dev").glob("ttyUSB*")))
    code, stdout, _ = _run(["lsusb"])
    pico_detected = "2e8a" in stdout.lower() or "raspberry pi" in stdout.lower()
    return {
        "serial_devices": serial_devices,
        "lsusb": stdout.splitlines(),
        "pico_detected": pico_detected or any("ttyACM" in path for path in serial_devices),
    }


def _git_push_auth() -> dict[str, Any]:
    ssh_binary = _which("ssh")
    github_ssh_ready = False
    github_ssh_error = None
    if ssh_binary:
        try:
            code, stdout, stderr = _run(
                [ssh_binary, "-T", "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=no", "git@github.com"],
                timeout=10,
            )
            github_ssh_ready = code in (0, 1) and "successfully authenticated" in (stdout + stderr).lower()
            github_ssh_error = stderr or stdout
        except subprocess.TimeoutExpired:
            github_ssh_error = "ssh test timed out"
    return {
        "gh_installed": bool(_which("gh")),
        "github_ssh_ready": github_ssh_ready,
        "github_ssh_check": github_ssh_error,
    }


def _ai_summary() -> dict[str, Any]:
    codex_binary = _which("codex")
    openai_key_present = bool(Path.home().joinpath(".openai").exists()) or bool(os.environ.get("OPENAI_API_KEY"))
    return {
        "codex_binary": codex_binary,
        "openai_api_key_present": openai_key_present,
        "configured": bool(codex_binary or openai_key_present),
    }


def collect_environment() -> dict[str, Any]:
    return {
        "captured_at": datetime.now().astimezone().isoformat(),
        "hostname": platform.node(),
        "platform": platform.platform(),
        "python_version": _python_version(),
        "node_version": _node_version(),
        "camera": _camera_summary(),
        "serial": _serial_summary(),
        "github": _git_push_auth(),
        "ai_mode": _ai_summary(),
        "project_paths": {
            "control_repo": str(repo_root()),
            "projects_dir": str(repo_root() / "projects"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect the current Raspberry Pi environment for the month controller.")
    parser.add_argument("--write", action="store_true", help="Persist the snapshot to state/last_environment.json.")
    args = parser.parse_args()

    payload = collect_environment()
    if args.write:
        save_json(repo_root() / "state" / "last_environment.json", payload)
    print(__import__("json").dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
