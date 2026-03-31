#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fcntl
import json
from pathlib import Path
import subprocess
from typing import Any

from common import (
    ensure_progress_log,
    git_head,
    git_status_porcelain,
    load_manifests,
    load_state,
    local_now,
    repo_root,
    run_shell,
    save_state,
    today_iso,
)
from detect_environment import collect_environment


def _run_group(project_path: Path, commands: list[str], heading: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for command in commands:
        result = run_shell(command, project_path)
        results.append(
            {
                "heading": heading,
                "command": command,
                "cwd": result.cwd,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        )
        if result.returncode != 0:
            break
    return results


def _write_report(report_path: Path, payload: dict[str, Any]) -> None:
    lines: list[str] = []
    lines.append(f"# Daily Cycle Report - {payload['date']}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Active project: `{payload['project_id']}`")
    lines.append(f"- Run mode: `{payload['run_mode']}`")
    lines.append(f"- Project path: `{payload['project_path']}`")
    lines.append(f"- AI configured: `{payload['ai_configured']}`")
    lines.append(f"- Progress log: `{payload['progress_log']}`")
    lines.append("")
    lines.append("## Environment Highlights")
    lines.append("")
    lines.append(f"- Camera detected: `{payload['environment']['camera']['detected']}`")
    lines.append(f"- Pico detected: `{payload['environment']['serial']['pico_detected']}`")
    lines.append(f"- GitHub SSH ready: `{payload['environment']['github']['github_ssh_ready']}`")
    lines.append("")
    lines.append("## Command Results")
    lines.append("")
    if not payload["command_results"]:
        lines.append("- No fallback commands were executed.")
    else:
        for item in payload["command_results"]:
            lines.append(f"### {item['heading']}: `{item['command']}`")
            lines.append("")
            lines.append(f"- Return code: `{item['returncode']}`")
            if item["stdout"]:
                lines.append("")
                lines.append("```text")
                lines.append(item["stdout"][:4000])
                lines.append("```")
            if item["stderr"]:
                lines.append("")
                lines.append("```text")
                lines.append(item["stderr"][:4000])
                lines.append("```")
    lines.append("")
    lines.append("## Git Status")
    lines.append("")
    lines.append(f"- HEAD before run: `{payload['head_before']}`")
    lines.append(f"- HEAD after run: `{payload['head_after']}`")
    lines.append(f"- Status after run: `{payload['status_after'] or 'clean'}`")
    report_path.write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the authoritative daily month cycle.")
    parser.add_argument("--write-state", action="store_true")
    parser.add_argument("--force-project", help="Override the active project from state.")
    parser.add_argument("--force-date", help="Override the report date in YYYY-MM-DD format.")
    parser.add_argument("--skip-commands", action="store_true")
    args = parser.parse_args()

    root = repo_root()
    lock_path = root / "state" / "daily_cycle.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    with lock_path.open("w") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)

        state = load_state()
        manifests = load_manifests()
        environment = collect_environment()
        run_date = args.force_date or today_iso()
        ai_configured = environment["ai_mode"]["configured"]
        run_mode = "ai-assisted" if ai_configured else "deterministic-backlog"
        progress_log = ensure_progress_log(state, run_mode, target_date=run_date)

        project_id = args.force_project or state["timeline"]["current_project"]
        manifest = manifests[project_id]
        project_path = Path(manifest["local_path"])
        command_results: list[dict[str, Any]] = []
        head_before = git_head(project_path)

        if project_path.exists() and not args.skip_commands:
            if git_status_porcelain(project_path):
                command_results.append(
                    {
                        "heading": "repo-guard",
                        "command": "git status --short",
                        "cwd": str(project_path),
                        "returncode": 0,
                        "stdout": git_status_porcelain(project_path),
                        "stderr": "",
                    }
                )
            else:
                if not ai_configured:
                    for heading in ("test", "smoke"):
                        commands = manifest.get("health_commands", {}).get(heading, [])
                        command_results.extend(_run_group(project_path, commands, heading))
                else:
                    command_results.append(
                        {
                            "heading": "ai-mode",
                            "command": "ai-assisted mode detected",
                            "cwd": str(project_path),
                            "returncode": 0,
                            "stdout": "AI mode is available, but this runner still executes deterministic validation unless a dedicated AI executor is configured.",
                            "stderr": "",
                        }
                    )
        else:
            command_results.append(
                {
                    "heading": "repo-missing",
                    "command": "project path check",
                    "cwd": str(project_path),
                    "returncode": 1,
                    "stdout": "",
                    "stderr": "Active project repo is missing on this machine.",
                }
            )

        head_after = git_head(project_path)
        report_path = root / "reports" / "daily" / f"{run_date}-{project_id}.md"
        payload = {
            "date": run_date,
            "project_id": project_id,
            "project_path": str(project_path),
            "run_mode": run_mode,
            "ai_configured": ai_configured,
            "progress_log": str(progress_log),
            "environment": environment,
            "command_results": command_results,
            "head_before": head_before,
            "head_after": head_after,
            "status_after": git_status_porcelain(project_path) if project_path.exists() else "missing",
        }
        _write_report(report_path, payload)
        print(json.dumps({"report": str(report_path), "mode": run_mode, "project": project_id}, indent=2))

        if args.write_state:
            project_state = state["projects"].setdefault(project_id, {})
            previous_head = project_state.get("last_seen_commit")
            all_commands_succeeded = all(item["returncode"] == 0 for item in command_results)
            if previous_head and head_after and previous_head != head_after and all_commands_succeeded:
                state["timeline"]["current_day_of_week"] = min(7, state["timeline"]["current_day_of_week"] + 1)
                project_state["day_equivalent"] = state["timeline"]["current_day_of_week"]
            if head_after:
                project_state["last_seen_commit"] = head_after

            state["ai_mode"]["configured"] = ai_configured
            state["ai_mode"]["detected_command"] = environment["ai_mode"]["codex_binary"]
            state["last_run"] = {
                "completed_at": local_now().isoformat(),
                "project_id": project_id,
                "report_path": str(report_path),
                "run_mode": run_mode,
            }
            save_state(state)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
