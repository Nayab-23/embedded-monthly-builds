from __future__ import annotations

from copy import deepcopy
from typing import Any


def _first_open_backlog_item(manifest: dict[str, Any], state: dict[str, Any]) -> dict[str, Any] | None:
    completed = set(state.get("completed_backlog_items", {}).get(manifest["project_id"], []))
    for item in manifest.get("continuation_backlog", []):
        if item["id"] not in completed:
            return deepcopy(item)
    return None


def choose_next_task(
    state: dict[str, Any],
    manifests: dict[str, dict[str, Any]],
    config: dict[str, Any],
    run_date: str,
) -> dict[str, Any]:
    priority_order = config["continuation"]["project_priority"]

    for project_id in priority_order:
        manifest = manifests.get(project_id)
        if not manifest:
            continue
        task = _first_open_backlog_item(manifest, state)
        if task:
            return {
                "selected_at": run_date,
                "project_id": project_id,
                "display_name": manifest["display_name"],
                "task": task,
            }

    raise RuntimeError("no continuation backlog item is available")


def apply_selection_to_state(
    state: dict[str, Any],
    manifests: dict[str, dict[str, Any]],
    selection: dict[str, Any],
    run_date: str,
) -> dict[str, Any]:
    project_id = selection["project_id"]
    manifest = manifests[project_id]
    task = selection["task"]

    state.setdefault("continuation_mode", {})
    state["continuation_mode"].update(
        {
            "enabled": True,
            "saved": True,
            "entered_on": state.get("continuation_mode", {}).get("entered_on") or run_date,
            "source_month": "2026-03",
            "target_month": "2026-04",
            "no_reset": True,
            "selection_strategy": "priority_then_first_open_task",
            "prioritized_project_id": project_id,
            "last_selected_task": {
                "project_id": project_id,
                "task_id": task["id"],
                "title": task["title"],
                "selected_at": run_date,
            },
        }
    )
    state["timeline"]["current_project"] = project_id
    state.setdefault("projects", {}).setdefault(project_id, {})
    state["projects"][project_id]["status"] = manifest["status_category"]
    state["projects"][project_id]["completion_estimate_pct"] = manifest["completion_estimate_pct"]
    state["projects"][project_id]["active_task_id"] = task["id"]
    state["projects"][project_id]["active_task_title"] = task["title"]
    state["active_backlog_item"] = {
        "project_id": project_id,
        "project_name": manifest["display_name"],
        "task_id": task["id"],
        "title": task["title"],
        "description": task["description"],
        "commit_message": task["commit_message"],
        "context_files": task.get("context_files", []),
        "validation_commands": task.get("validation_commands", []),
        "selected_at": run_date,
    }
    return state
