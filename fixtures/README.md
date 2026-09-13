# SBPA Adversarial Fixtures

Fixtures are small repositories designed to measure whether an agent using SBPA actually discovers difficult behavior instead of merely producing a plausible report.

Each fixture contains source evidence plus `expected.json`. Expected entries are benchmark facts for SBPA development and MUST NOT be shown to an evaluated agent before it performs discovery.

Initial benchmark dimensions:

- hidden/default branches
- fallback behavior
- swallowed or transformed failures
- state transitions
- ordering/timing semantics
- configuration-dependent behavior
- tests that conflict with implementation
- duplicate-looking behaviors that differ semantically
- source changes that must invalidate prior equivalence claims

Metrics should be reported separately:

- behavior recall
- false `EXACT` rate
- unsupported `CONFIRMED` rate
- unknown/conflict preservation rate
- structural coverage closure
- verification mapping recall

Do not optimize a fixture score by embedding fixture-specific hints in `SKILL.md`. The benchmark is intended to detect general preservation quality.
