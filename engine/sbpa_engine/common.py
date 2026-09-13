from __future__ import annotations

import csv
import hashlib
import os
import subprocess
from pathlib import Path

SKIP_DIRS = {
    ".git", ".sbpa", "node_modules", "target", "dist", "build",
    ".next", ".venv", "venv", "__pycache__",
}

EVIDENCE_STATUSES = {"UNREVIEWED", "REVIEWED", "NOT_APPLICABLE", "BLOCKED"}
ELEMENT_STATUSES = {"BEHAVIOR_MAPPED", "NO_BEHAVIORAL_EFFECT", "UNKNOWN"}
TARGET_STATUSES = {
    "EXACT", "PARTIAL", "MISSING", "DIFFERENT", "UNKNOWN",
    "NOT_APPLICABLE", "INTENTIONALLY_CHANGED",
}
EVIDENCE_CLASSES = {"CONFIRMED", "INFERRED", "CONFLICTED", "UNKNOWN"}


def git_head(root: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_files(root: Path):
    for base, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(names):
            path = Path(base) / name
            rel = path.relative_to(root)
            if any(part in SKIP_DIRS for part in rel.parts):
                continue
            yield path


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))
