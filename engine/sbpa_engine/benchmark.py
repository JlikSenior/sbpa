from __future__ import annotations

from typing import Any


def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())


def score_fixture(expected: dict[str, Any], discovered: list[str]) -> dict[str, Any]:
    found = {normalize(item) for item in discovered}
    required = [normalize(item) for item in expected.get("expected_behaviors", [])]
    matched = [item for item in required if item in found]
    minimum = int(expected.get("minimum_behavior_count", len(required)))
    compressions = [
        item for item in expected.get("forbidden_compressions", [])
        if normalize(item) in found
    ]
    recall = (len(matched) / len(required)) if required else 1.0
    passed = recall == 1.0 and len(discovered) >= minimum and not compressions
    return {
        "fixture": expected.get("fixture"),
        "expected": len(required),
        "matched": len(matched),
        "behavior_recall": recall,
        "discovered_count": len(discovered),
        "minimum_behavior_count": minimum,
        "forbidden_compressions_found": compressions,
        "passed": passed,
    }


def aggregate(scores: list[dict[str, Any]]) -> dict[str, Any]:
    if not scores:
        return {"fixtures": 0, "passed": 0, "mean_behavior_recall": 0.0}
    return {
        "fixtures": len(scores),
        "passed": sum(1 for score in scores if score.get("passed")),
        "mean_behavior_recall": sum(float(s.get("behavior_recall", 0)) for s in scores) / len(scores),
    }
