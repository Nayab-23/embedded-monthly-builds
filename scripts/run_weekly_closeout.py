#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from common import git_log_summary, load_manifests, load_state, render_template, repo_root, save_state, today_iso


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a weekly closeout report for the active project.")
    parser.add_argument("--project-id", help="Override the active project from state.")
    parser.add_argument("--write-state", action="store_true")
    args = parser.parse_args()

    state = load_state()
    manifests = load_manifests()
    project_id = args.project_id or state["timeline"]["current_project"]
    manifest = manifests[project_id]
    project_path = Path(manifest["local_path"])
    project_log = git_log_summary(project_path, max_count=12) if project_path.exists() else "Local repo missing on the Pi."
    week_label = f"Week {manifest['week_index']} - {manifest['display_name']}"

    report = render_template(
        repo_root() / "templates" / "weekly_summary_template.md",
        {
            "week_label": week_label,
        },
    )
    report += "\n## Automation Summary\n\n"
    report += f"- Project ID: `{project_id}`\n"
    report += f"- Local path: `{manifest['local_path']}`\n"
    report += f"- Repo URL: `{manifest['repo_url']}`\n"
    report += f"- Current status: `{manifest['status']}`\n"
    report += "\n## Recent Commits\n\n```text\n"
    report += project_log + "\n```\n"

    report_path = repo_root() / "reports" / "weekly" / f"{today_iso()}-week{manifest['week_index']}-{project_id}.md"
    report_path.write_text(report)
    print(report_path)

    if args.write_state:
        state["last_weekly_closeout"] = {
            "project_id": project_id,
            "report_path": str(report_path),
            "completed_at": datetime.now().astimezone().isoformat(),
        }
        save_state(state)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
