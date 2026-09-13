from __future__ import annotations

from pathlib import Path

from .common import iter_files, read_csv, sha256


def detect_changes(root: Path) -> dict[str, list[str]]:
    state = root / ".sbpa"
    recorded_rows = read_csv(state / "evidence.csv")
    recorded = {row.get("location", ""): row for row in recorded_rows if row.get("location")}
    current = {path.relative_to(root).as_posix(): path for path in iter_files(root)}

    added = sorted(set(current) - set(recorded))
    deleted = sorted(set(recorded) - set(current))
    changed = []
    unchanged = []

    for rel in sorted(set(current) & set(recorded)):
        expected = recorded[rel].get("sha256", "")
        actual = sha256(current[rel])
        if expected and expected != actual:
            changed.append(rel)
        else:
            unchanged.append(rel)

    return {
        "added": added,
        "changed": changed,
        "deleted": deleted,
        "unchanged": unchanged,
    }
