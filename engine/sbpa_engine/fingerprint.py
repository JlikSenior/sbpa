from __future__ import annotations

import hashlib
import json
from typing import Any

VOLATILE_KEYS = {"title", "description", "notes", "output_language", "fingerprint"}


def _canonical(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _canonical(value[k]) for k in sorted(value) if k not in VOLATILE_KEYS}
    if isinstance(value, list):
        return [_canonical(v) for v in value]
    return value


def behavior_fingerprint(behavior: dict[str, Any]) -> str:
    """Return a language-neutral SHA-256 identity aid for a behavior contract.

    Stable IDs remain authoritative. This fingerprint intentionally ignores
    human-readable presentation fields so language changes do not alter it.
    """
    payload = {
        "source_evidence": sorted(behavior.get("source_evidence", [])),
        "contract": _canonical(behavior.get("contract", {})),
        "related_behaviors": sorted(behavior.get("related_behaviors", [])),
    }
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def duplicate_fingerprints(behaviors: list[dict[str, Any]]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for behavior in behaviors:
        fp = behavior_fingerprint(behavior)
        groups.setdefault(fp, []).append(str(behavior.get("id", "")))
    return {fp: ids for fp, ids in groups.items() if len(ids) > 1}
