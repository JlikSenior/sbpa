from __future__ import annotations

import json
from pathlib import Path

from .common import git_head


def ensure_state(root: Path, language: str = "auto") -> Path:
    state = root / ".sbpa"
    state.mkdir(exist_ok=True)

    scope = state / "scope.json"
    if not scope.exists():
        scope.write_text(
            json.dumps(
                {
                    "schema_version": "1",
                    "output_language": language,
                    "technical_terms": "preserve",
                    "source_identifiers": "preserve",
                    "analysis_root": ".",
                    "source_commit": git_head(root),
                    "target_commit": None,
                    "explicit_exclusions": [],
                },
                indent=2,
                ensure_ascii=False,
            ) + "\n",
            encoding="utf-8",
        )

    tables = {
        "elements.csv": "element_id,evidence_id,native_name,native_classification,status,behavior_ids,notes\n",
        "traceability.csv": "behavior_id,source_evidence,requirement,target_evidence,target_status,verification_evidence,notes\n",
    }
    for name, header in tables.items():
        path = state / name
        if not path.exists():
            path.write_text(header, encoding="utf-8")

    behaviors = state / "behaviors.jsonl"
    if not behaviors.exists():
        behaviors.write_text("", encoding="utf-8")

    for name in ("gaps.md", "unknowns.md", "conflicts.md", "ledger.md"):
        path = state / name
        if not path.exists():
            path.write_text(f"# {name[:-3].title()}\n", encoding="utf-8")

    return state
