from __future__ import annotations

from collections import defaultdict, deque
from typing import Any


def build_graph(behaviors: list[dict[str, Any]]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = defaultdict(set)
    for behavior in behaviors:
        bid = str(behavior.get("id", ""))
        if not bid:
            continue
        for eid in behavior.get("source_evidence", []):
            graph[str(eid)].add(bid)
        for parent in behavior.get("related_behaviors", []):
            graph[str(parent)].add(bid)
    return dict(graph)


def affected(changed_nodes: set[str], graph: dict[str, set[str]]) -> set[str]:
    result: set[str] = set()
    queue = deque(changed_nodes)
    seen = set(changed_nodes)
    while queue:
        node = queue.popleft()
        for dependent in graph.get(node, set()):
            if dependent in result:
                continue
            result.add(dependent)
            if dependent not in seen:
                seen.add(dependent)
                queue.append(dependent)
    return result


def stale_rows(rows: list[dict[str, str]], stale: set[str]) -> list[dict[str, str]]:
    return [row for row in rows if row.get("behavior_id") in stale]
