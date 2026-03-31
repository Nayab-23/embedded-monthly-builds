#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import load_global_config


def _repo_relative(repo_path: Path, relative_path: str) -> Path:
    target = (repo_path / relative_path).resolve()
    target.relative_to(repo_path.resolve())
    return target


def apply_change_set(repo_path: Path, proposal: dict[str, Any]) -> dict[str, Any]:
    config = load_global_config()["ai_execution"]
    files = proposal.get("files", [])
    if not files:
        raise RuntimeError("proposal does not contain files")
    if len(files) > int(config["max_files_per_run"]):
        raise RuntimeError("proposal exceeds max_files_per_run")

    backups: list[dict[str, Any]] = []
    touched: list[str] = []
    for file_spec in files:
        relative_path = file_spec["path"]
        content = file_spec["content"]
        if len(content) > int(config["max_file_chars"]):
            raise RuntimeError(f"{relative_path} exceeds max_file_chars")

        target = _repo_relative(repo_path, relative_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        existed = target.exists()
        original = target.read_text() if existed else None

        if original and len(original.splitlines()) > 60 and len(content.splitlines()) < len(original.splitlines()) * 0.5:
            raise RuntimeError(f"refusing large destructive rewrite for {relative_path}")

        backups.append({"path": relative_path, "existed": existed, "content": original})
        target.write_text(content)
        touched.append(relative_path)

    return {"touched_files": touched, "backups": backups}


def rollback_change_set(repo_path: Path, backups: list[dict[str, Any]]) -> None:
    for backup in reversed(backups):
        target = _repo_relative(repo_path, backup["path"])
        if backup["existed"]:
            target.write_text(backup["content"])
        elif target.exists():
            target.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply a JSON-coded AI change set.")
    parser.add_argument("repo_path")
    parser.add_argument("proposal_path")
    args = parser.parse_args()

    proposal = json.loads(Path(args.proposal_path).read_text())
    payload = apply_change_set(Path(args.repo_path), proposal)
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
