#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from common import load_global_config, load_manifests, load_state, save_state, today_iso
from continuation import apply_selection_to_state, choose_next_task


def main() -> int:
    parser = argparse.ArgumentParser(description="Choose the next continuation backlog item.")
    parser.add_argument("--write-state", action="store_true")
    parser.add_argument("--force-date", help="Override the selection date in YYYY-MM-DD format.")
    args = parser.parse_args()

    run_date = args.force_date or today_iso()
    state = load_state()
    manifests = load_manifests()
    config = load_global_config()
    selection = choose_next_task(state, manifests, config, run_date)

    if args.write_state:
        apply_selection_to_state(state, manifests, selection, run_date)
        save_state(state)

    print(json.dumps(selection, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
