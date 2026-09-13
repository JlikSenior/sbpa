from __future__ import annotations

import json
from pathlib import Path

from .common import EVIDENCE_CLASSES, EVIDENCE_STATUSES, TARGET_STATUSES, iter_files, read_csv, sha256


def validate(root: Path) -> tuple[list[str], list[str]]:
    state = root / ".sbpa"
    errors: list[str] = []
    warnings: list[str] = []
    if not state.exists():
        return [".sbpa does not exist; run `sbpa init` first"], []

    evidence = read_csv(state / "evidence.csv")
    evidence_ids: set[str] = set()
    for row in evidence:
        eid = row.get("evidence_id", "")
        if not eid or eid in evidence_ids:
            errors.append(f"invalid or duplicate evidence ID: {eid!r}")
        evidence_ids.add(eid)
        status = row.get("status", "")
        if status not in EVIDENCE_STATUSES:
            errors.append(f"{eid}: invalid evidence status {status!r}")
        if status in {"BLOCKED", "NOT_APPLICABLE"} and not row.get("notes", "").strip():
            errors.append(f"{eid}: {status} requires notes")
        path = root / row.get("location", "")
        if not path.is_file():
            errors.append(f"{eid}: inventoried file is missing: {row.get('location', '')}")
        elif row.get("sha256") and sha256(path) != row["sha256"]:
            warnings.append(f"{eid}: file changed since inventory: {row.get('location', '')}")

    behavior_ids: set[str] = set()
    behavior_path = state / "behaviors.jsonl"
    if behavior_path.exists():
        for line_no, line in enumerate(behavior_path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                behavior = json.loads(line)
            except Exception as exc:
                errors.append(f"behaviors.jsonl:{line_no}: invalid JSON: {exc}")
                continue
            bid = behavior.get("id")
            if not bid or bid in behavior_ids:
                errors.append(f"behaviors.jsonl:{line_no}: invalid or duplicate behavior ID")
            behavior_ids.add(bid)
            evidence_class = behavior.get("evidence_class")
            if evidence_class not in EVIDENCE_CLASSES:
                errors.append(f"{bid}: invalid evidence_class {evidence_class!r}")
            refs = behavior.get("source_evidence") or []
            if not refs:
                errors.append(f"{bid}: source_evidence is required")
            for ref in refs:
                if ref not in evidence_ids:
                    errors.append(f"{bid}: unknown source evidence {ref}")

    trace_rows = read_csv(state / "traceability.csv")
    trace_counts: dict[str, int] = {}
    for row in trace_rows:
        bid = row.get("behavior_id", "")
        trace_counts[bid] = trace_counts.get(bid, 0) + 1
        status = row.get("target_status", "")
        if status and status not in TARGET_STATUSES:
            errors.append(f"{bid}: invalid target status {status!r}")
        if status == "EXACT":
            if not row.get("target_evidence", "").strip() or not row.get("verification_evidence", "").strip():
                errors.append(f"{bid}: EXACT requires target_evidence and verification_evidence")
        if status == "INTENTIONALLY_CHANGED" and not row.get("notes", "").strip():
            errors.append(f"{bid}: INTENTIONALLY_CHANGED requires approval evidence in notes")

    for bid in behavior_ids:
        count = trace_counts.get(bid, 0)
        if count != 1:
            errors.append(f"{bid}: requires exactly one primary traceability row; found {count}")

    current = {path.relative_to(root).as_posix() for path in iter_files(root)}
    recorded = {row.get("location", "") for row in evidence}
    unseen = current - recorded
    if unseen:
        errors.append(f"inventory is stale: {len(unseen)} untracked file(s); run `sbpa inventory`")

    return errors, warnings
