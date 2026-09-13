# Canonical Behavior Model

Use this schema as the canonical record shape for discovered behavior. Store records in `.sbpa/behaviors.yaml` unless the audited project already has an explicit compatible format.

```yaml
- id: B-000001
  title: concise behavior name
  evidence_class: CONFIRMED # CONFIRMED | INFERRED | CONFLICTED | UNKNOWN
  description: >-
    One independently verifiable behavioral contract.

  source_evidence:
    - evidence_id: E-000001
      location: path-or-artifact-location
      locator: native symbol, range, key, node, assertion, or equivalent
      note: why this evidence establishes the behavior

  trigger:
    description: null
  preconditions: []
  inputs: []
  validation: []
  decision_logic: []

  state:
    before: null
    transition: null
    after: null

  outputs: []
  observable_effects: []
  side_effects: []
  persistence_effects: []

  temporal_semantics: []
  ordering_semantics: []
  concurrency_semantics: []

  failure_behavior: []
  recovery_behavior: []
  edge_conditions: []
  external_dependencies: []

  related_behaviors: []
  verification_evidence: []

  requirement_ids: []
  target_mapping:
    status: UNKNOWN # EXACT | PARTIAL | MISSING | DIFFERENT | UNKNOWN | NOT_APPLICABLE | INTENTIONALLY_CHANGED
    evidence: []
    note: null

  gap_ids: []
  unknown_ids: []
  conflict_ids: []
```

## Atomicity test

Split a record when any independently testable contract differs in a material way, including a different trigger, precondition, accepted or rejected input, branch outcome, transition, output, observable effect, side effect, failure path, recovery path, ordering constraint, timing constraint, concurrency rule, persistence rule, or compatibility rule.

Do not split merely because implementation is distributed across multiple files. A behavior can cite multiple evidence items.

Do not merge merely because multiple behaviors belong to one feature.

## Evidence strength

`CONFIRMED` requires direct inspected evidence sufficient to support the recorded contract.

`INFERRED` requires the inference path to be written down. It must not be used as a convenience when evidence could simply be inspected.

`CONFLICTED` requires entries in the conflict register.

`UNKNOWN` requires an entry in the unknown register when the uncertainty can block migration equivalence or coverage closure.

## Target equivalence

Use `EXACT` only when target evidence covers every source-semantic dimension relevant to the behavior. Similar names, similar structure, compilation success, or a passing unrelated test are insufficient.

Use `PARTIAL` when some but not all required semantics are evidenced.

Use `DIFFERENT` when the target demonstrably implements a conflicting semantic.

Use `MISSING` when no target implementation exists for a required source behavior and search coverage is sufficient to establish absence.

Use `UNKNOWN` when target coverage is insufficient to decide.

Use `INTENTIONALLY_CHANGED` only with explicit approval evidence and retain the source behavior for historical traceability.
