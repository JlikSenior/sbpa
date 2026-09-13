# branch-fallback

This fixture checks whether an audit preserves five distinct contracts that are easy to compress into one vague "validation/fallback" feature.

An evaluated agent should inspect `source.py` without seeing `expected.json`. After the audit, compare discovered atomic behaviors against the benchmark expectations.

The fixture intentionally contains no domain-specific business context so it tests behavior discovery rather than product knowledge.
