# Generated Acceptance Specifications

SBPA may project recovered behaviors into acceptance specifications when historical verification is missing or insufficient.

Generated acceptance specifications are **verification artifacts**, not historical source evidence.

## Identity

Use stable IDs such as `A-000001`. Every acceptance specification must reference exactly one primary Behavior ID. Multiple acceptance specifications may verify different dimensions of the same behavior.

## Required distinction

Always set:

`origin: GENERATED_VERIFICATION`

Do not cite a generated acceptance specification as proof that the source system historically behaved that way. Its authority comes from the recovered Behavior contract and its source evidence.

## Structure

Use Given / When / Then semantics:

- `given`: preconditions and relevant starting state;
- `when`: triggering action/event/input;
- `then`: observable outputs, state changes, side effects, failures, ordering, timing, or other contract dimensions that must hold.

The schema is `schemas/acceptance-spec.schema.json`.

## Completeness

One acceptance specification does not automatically verify an entire behavior. Verification should cover every relevant discovered semantic dimension before supporting an `EXACT` claim.

Where a behavior has multiple branches or edge conditions, create additional acceptance specifications rather than compressing distinct outcomes.

## Automation status

Generated specifications may be marked `NOT_IMPLEMENTED`, `IMPLEMENTED`, `PARTIAL`, or `BLOCKED`. A written specification without an executable test is not executable verification evidence.

## Traceability

Maintain this chain:

`Source Evidence -> Behavior -> Acceptance Specification -> Executable Verification (if implemented)`

Do not reverse the direction and use generated verification to invent source behavior.
