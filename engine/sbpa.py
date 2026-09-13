#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sbpa_engine.common import EVIDENCE_STATUSES, TARGET_STATUSES, read_csv
from sbpa_engine.inventory import build_inventory
from sbpa_engine.state import ensure_state
from sbpa_engine.validator import validate


def show_status(root: Path) -> None:
    state = root / ".sbpa"
    evidence = read_csv(state / "evidence.csv")
    trace = read_csv(state / "traceability.csv")
    evidence_counts = {value: 0 for value in sorted(EVIDENCE_STATUSES)}
    target_counts = {value: 0 for value in sorted(TARGET_STATUSES)}
    for row in evidence:
        if row.get("status") in evidence_counts:
            evidence_counts[row["status"]] += 1
    for row in trace:
        if row.get("target_status") in target_counts:
            target_counts[row["target_status"]] += 1
    print("Evidence:", len(evidence), evidence_counts)
    print("Target:", len(trace), target_counts)


def main() -> int:
    parser = argparse.ArgumentParser(prog="sbpa")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="initialize durable .sbpa audit state")
    init.add_argument("--language", choices=["auto", "zh-CN", "en"], default="auto")
    sub.add_parser("inventory", help="inventory repository evidence with content hashes")
    sub.add_parser("validate", help="validate audit state and strong evidence claims")
    sub.add_parser("status", help="show mechanically calculated coverage counts")
    args = parser.parse_args()
    root = Path.cwd().resolve()

    if args.command == "init":
        ensure_state(root, args.language)
        print(f"Initialized {root / '.sbpa'} (language={args.language})")
        return 0
    if args.command == "inventory":
        count = build_inventory(root)
        print(f"Inventoried {count} file(s)")
        return 0
    if args.command == "status":
        show_status(root)
        return 0

    errors, warnings = validate(root)
    for message in warnings:
        print("WARN:", message)
    for message in errors:
        print("ERROR:", message)
    print(f"SBPA validate: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
