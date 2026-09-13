from __future__ import annotations

import csv
import json
from pathlib import Path

from .common import git_head, iter_files, read_csv, sha256
from .state import ensure_state

FIELDS = ["evidence_id", "location", "type", "sha256", "bytes", "status", "relevance", "notes"]


def build_inventory(root: Path) -> int:
    state = ensure_state(root)
    evidence_path = state / "evidence.csv"
    previous = {row.get("location", ""): row for row in read_csv(evidence_path)}

    records = []
    next_number = 1
    used_ids = {row.get("evidence_id", "") for row in previous.values()}

    def new_id() -> str:
        nonlocal next_number
        while f"E-{next_number:06d}" in used_ids:
            next_number += 1
        value = f"E-{next_number:06d}"
        used_ids.add(value)
        next_number += 1
        return value

    for path in iter_files(root):
        rel = path.relative_to(root).as_posix()
        old = previous.get(rel, {})
        records.append(
            {
                "evidence_id": old.get("evidence_id") or new_id(),
                "location": rel,
                "type": path.suffix.lower().lstrip(".") or "file",
                "sha256": sha256(path),
                "bytes": str(path.stat().st_size),
                "status": old.get("status") or "UNREVIEWED",
                "relevance": old.get("relevance") or "UNKNOWN",
                "notes": old.get("notes") or "",
            }
        )

    with evidence_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)

    manifest = {
        "schema_version": "1",
        "generated_from_commit": git_head(root),
        "file_count": len(records),
        "files": [
            {"id": row["evidence_id"], "path": row["location"], "sha256": row["sha256"], "bytes": int(row["bytes"])}
            for row in records
        ],
    }
    (state / "inventory.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return len(records)
