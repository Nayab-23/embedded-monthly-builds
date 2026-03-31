from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
import subprocess
from typing import Any


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def state_path() -> Path:
    return repo_root() / "state" / "current_state.json"


def manifests_dir() -> Path:
    return repo_root() / "manifests" / "projects"


def reports_dir() -> Path:
    return repo_root() / "reports"


def progress_dir() -> Path:
    return repo_root() / "progress"


def local_now() -> datetime:
    return datetime.now().astimezone()


def today_iso() -> str:
    return local_now().date().isoformat()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def save_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n")


def load_state() -> dict[str, Any]:
    return load_json(state_path())


def save_state(payload: dict[str, Any]) -> None:
    save_json(state_path(), payload)


def load_manifests() -> dict[str, dict[str, Any]]:
    manifests: dict[str, dict[str, Any]] = {}
    for path in sorted(manifests_dir().glob("*.json")):
        manifest = load_json(path)
        manifests[manifest["project_id"]] = manifest
    return manifests


def load_runtime_policy() -> dict[str, Any]:
    return load_json(repo_root() / "manifests" / "runtime_policy.json")


def load_global_config() -> dict[str, Any]:
    return load_json(repo_root() / "config" / "global_config.json")


@dataclass
class CommandResult:
    label: str
    command: str
    cwd: str
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False

    @property
    def succeeded(self) -> bool:
        return self.returncode == 0


def run_shell(command: str, cwd: Path, timeout_seconds: int | None = None) -> CommandResult:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
        )
        return CommandResult(
            label=command,
            command=command,
            cwd=str(cwd),
            returncode=completed.returncode,
            stdout=completed.stdout.strip(),
            stderr=completed.stderr.strip(),
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.strip() if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr.strip() if isinstance(exc.stderr, str) else ""
        return CommandResult(
            label=command,
            command=command,
            cwd=str(cwd),
            returncode=124,
            stdout=stdout,
            stderr=stderr or f"timed out after {timeout_seconds} seconds",
            timed_out=True,
        )


def git_head(repo_path: Path) -> str | None:
    if not repo_path.exists():
        return None
    result = subprocess.run(
        ["git", "-C", str(repo_path), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def git_status_porcelain(repo_path: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_path), "status", "--short"],
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def git_log_summary(repo_path: Path, max_count: int = 10) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_path), "log", "--oneline", f"--max-count={max_count}"],
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def render_template(template_path: Path, replacements: dict[str, str]) -> str:
    rendered = template_path.read_text()
    for key, value in replacements.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def ensure_progress_log(state: dict[str, Any], run_mode: str, target_date: str | None = None) -> Path:
    target_date = target_date or today_iso()
    target_path = progress_dir() / f"{target_date}.md"
    if target_path.exists():
        return target_path

    timeline = state["timeline"]
    content = render_template(
        repo_root() / "templates" / "daily_log_template.md",
        {
            "date": target_date,
            "active_project": timeline["current_project"],
            "week_day": f"Week {timeline['current_week']} Day {timeline['current_day_of_week']}",
            "run_mode": run_mode,
        },
    )
    target_path.write_text(content)
    return target_path


def validate_iso_date(raw: str) -> str:
    return date.fromisoformat(raw).isoformat()
