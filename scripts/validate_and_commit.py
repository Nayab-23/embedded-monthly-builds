#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from common import load_global_config, run_shell


def run_validation(repo_path: Path, commands: list[str]) -> list[dict[str, Any]]:
    timeout_seconds = int(load_global_config()["validation"]["step_timeout_seconds"])
    results: list[dict[str, Any]] = []
    for command in commands:
        result = run_shell(command, repo_path, timeout_seconds=timeout_seconds)
        results.append(
            {
                "command": command,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "timed_out": result.timed_out,
            }
        )
        if result.returncode != 0:
            break
    return results


def _ensure_git_identity(repo_path: Path) -> None:
    git_config = load_global_config()["git"]
    for key, value in (
        ("user.name", git_config["author_name"]),
        ("user.email", git_config["author_email"]),
    ):
        current = subprocess.run(
            ["git", "-C", str(repo_path), "config", "--get", key],
            text=True,
            capture_output=True,
        )
        if current.returncode != 0 or not current.stdout.strip():
            subprocess.run(["git", "-C", str(repo_path), "config", key, value], check=True)


def commit_and_push(repo_path: Path, commit_message: str, changed_files: list[str]) -> dict[str, Any]:
    _ensure_git_identity(repo_path)
    subprocess.run(["git", "-C", str(repo_path), "add", "--", *changed_files], check=True)
    subprocess.run(["git", "-C", str(repo_path), "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "-C", str(repo_path), "push", "origin", "main"], check=True)
    commit_hash = subprocess.run(
        ["git", "-C", str(repo_path), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    return {"commit_hash": commit_hash, "branch": "main"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run validation commands, then commit and push.")
    parser.add_argument("repo_path")
    parser.add_argument("commit_message")
    parser.add_argument("changed_files", nargs="+")
    parser.add_argument("--command", action="append", default=[])
    args = parser.parse_args()

    results = run_validation(Path(args.repo_path), args.command)
    ok = all(item["returncode"] == 0 for item in results)
    payload: dict[str, Any] = {"validation": results, "ok": ok}
    if ok:
        payload["git"] = commit_and_push(Path(args.repo_path), args.commit_message, args.changed_files)
    print(json.dumps(payload, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
