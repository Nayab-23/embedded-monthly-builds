#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from ai_client import chat_json, resolve_ai_settings
from apply_generated_changes import apply_change_set, rollback_change_set
from common import load_global_config, load_manifests, load_state, save_state, today_iso
from continuation import apply_selection_to_state, choose_next_task
from validate_and_commit import commit_and_push, run_validation


def _git_status(repo_path: Path) -> str:
    result = subprocess.run(["git", "-C", str(repo_path), "status", "--short"], text=True, capture_output=True, check=True)
    return result.stdout.strip()


def _repo_snapshot(repo_path: Path) -> str:
    result = subprocess.run(["git", "-C", str(repo_path), "ls-files"], text=True, capture_output=True, check=True)
    files = result.stdout.splitlines()
    return "\n".join(files[:120])


def _read_context_files(repo_path: Path, context_files: list[str]) -> list[dict[str, str]]:
    sections: list[dict[str, str]] = []
    for relative_path in context_files:
        path = repo_path / relative_path
        if not path.exists():
            continue
        sections.append({"path": relative_path, "content": path.read_text()[:12000]})
    return sections


def build_messages(repo_path: Path, manifest: dict[str, Any], selection: dict[str, Any]) -> list[dict[str, str]]:
    config = load_global_config()["ai_execution"]
    task = selection["task"]
    context_sections = _read_context_files(repo_path, task.get("context_files", []))
    context_blob = "\n\n".join(
        f"FILE: {section['path']}\n```text\n{section['content']}\n```" for section in context_sections
    )
    user_prompt = f"""
Repository: {manifest['repo_name']}
Task ID: {task['id']}
Task title: {task['title']}
Task description: {task['description']}
Commit message: {task['commit_message']}
Maximum files you may change: {config['max_files_per_run']}

Repository file snapshot:
```text
{_repo_snapshot(repo_path)}
```

Current context files:
{context_blob}

Return a JSON object with:
- summary: short summary
- commit_message: commit message to use
- files: array of objects with path and full content

Rules:
- make only this incremental change
- preserve the existing architecture and public API unless the task requires a small additive extension
- do not touch more than {config['max_files_per_run']} files
- do not delete large working sections
- keep tests passing
- do not include markdown fences
- do not mention secrets
""".strip()

    return [
        {
            "role": "system",
            "content": "You are a conservative code generator. Return only strict JSON for bounded repository edits.",
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]


def execute_task(state: dict[str, Any], manifests: dict[str, dict[str, Any]], run_date: str, write_state: bool) -> dict[str, Any]:
    config = load_global_config()
    selection = state.get("active_backlog_item")
    if not selection:
        picked = choose_next_task(state, manifests, config, run_date)
        apply_selection_to_state(state, manifests, picked, run_date)
        selection = state["active_backlog_item"]

    project_id = selection["project_id"]
    manifest = manifests[project_id]
    repo_path = Path(manifest["local_path"])
    if _git_status(repo_path):
        raise RuntimeError(f"{project_id} is dirty; refusing AI execution")

    task_selection = {
        "project_id": project_id,
        "task": {
            "id": selection["task_id"],
            "title": selection["title"],
            "description": selection["description"],
            "commit_message": selection["commit_message"],
            "context_files": selection.get("context_files", []),
        },
    }
    messages = build_messages(repo_path, manifest, task_selection)
    proposal, metadata = chat_json(messages)
    applied = apply_change_set(repo_path, proposal)

    validation_commands = selection.get("validation_commands") or task_selection["task"].get("validation_commands") or []
    results = run_validation(repo_path, validation_commands)
    ok = all(item["returncode"] == 0 for item in results)
    if not ok:
        rollback_change_set(repo_path, applied["backups"])
        result_payload = {
            "status": "validation_failed",
            "project_id": project_id,
            "task_id": selection["task_id"],
            "validation": results,
            "model": metadata["model"],
            "usage": metadata["usage"],
            "touched_files": applied["touched_files"],
        }
    else:
        commit_payload = commit_and_push(repo_path, proposal.get("commit_message", selection["commit_message"]), applied["touched_files"])
        result_payload = {
            "status": "success",
            "project_id": project_id,
            "task_id": selection["task_id"],
            "validation": results,
            "model": metadata["model"],
            "usage": metadata["usage"],
            "touched_files": applied["touched_files"],
            "commit_hash": commit_payload["commit_hash"],
            "branch": commit_payload["branch"],
        }

    if write_state:
        state["last_ai_execution"] = {
            "executed_at": run_date,
            "project_id": project_id,
            "task_id": selection["task_id"],
            "title": selection["title"],
            "status": result_payload["status"],
            "model": metadata["model"],
            "usage": metadata["usage"],
            "touched_files": result_payload["touched_files"],
            "commit_hash": result_payload.get("commit_hash"),
        }
        if result_payload["status"] == "success":
            completed = state.setdefault("completed_backlog_items", {}).setdefault(project_id, [])
            if selection["task_id"] not in completed:
                completed.append(selection["task_id"])
        save_state(state)

    return result_payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute one AI-assisted continuation task.")
    parser.add_argument("--write-state", action="store_true")
    parser.add_argument("--force-date", help="Override the execution date in YYYY-MM-DD format.")
    args = parser.parse_args()

    run_date = args.force_date or today_iso()
    state = load_state()
    manifests = load_manifests()
    resolve_ai_settings()
    payload = execute_task(state, manifests, run_date, write_state=args.write_state)
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
