# Durable Audit Artifacts

For non-trivial audits, keep state under `.sbpa/` in the repository being analyzed. These files are working evidence records, not polished documentation.

## Required core artifacts

### `.sbpa/scope.md`

Record:

- analysis root
- source system
- target system, if any
- explicit user-provided exclusions
- discovered evidence classes
- traversal strategy for large repositories
- audit start/update metadata
- output language configuration

Recommended language block:

```yaml
output_language: auto
technical_terms: preserve
source_identifiers: preserve
```

Apply `references/output-language.md`. Once selected, preserve the configured language across later batches unless the user explicitly changes it.

Never invent exclusions.

### `.sbpa/evidence.csv`

Columns:

```text
evidence_id,location,type,status,relevance,notes
```

Allowed status values:

```text
UNREVIEWED,REVIEWED,NOT_APPLICABLE,BLOCKED
```

`NOT_APPLICABLE` and `BLOCKED` require notes.

### `.sbpa/elements.csv`

Columns:

```text
element_id,evidence_id,native_name,native_classification,status,behavior_ids,notes
```

Allowed status values:

```text
BEHAVIOR_MAPPED,NO_BEHAVIORAL_EFFECT,UNKNOWN
```

`NO_BEHAVIORAL_EFFECT` requires justification in notes.

### `.sbpa/behaviors.yaml`

Use `behavior-model.md`. Stable IDs are mandatory. Append and amend; do not renumber existing records.

### `.sbpa/traceability.csv`

Columns:

```text
behavior_id,source_evidence,requirement,target_evidence,target_status,verification_evidence,notes
```

Every discovered Behavior ID must have exactly one primary row.

### `.sbpa/gaps.md`

Each gap uses a stable `G-000001` style ID and records:

- related behavior IDs
- source evidence
- target evidence if any
- discrepancy
- impact without unsupported severity assumptions
- confidence
- recommended resolution
- verification method
- status and resolution evidence

### `.sbpa/unknowns.md`

Each unknown uses a stable `U-000001` style ID and records:

- related evidence and behavior IDs
- unresolved question
- why it is unresolved
- which conclusion it blocks
- verification method
- status and resolution evidence

### `.sbpa/conflicts.md`

Each conflict uses a stable `C-000001` style ID and records:

- evidence A
- evidence B and additional conflicting evidence if needed
- conflict description
- affected behavior IDs
- required resolution or verification path
- status and resolution evidence

### `.sbpa/ledger.md`

This is the continuation checkpoint. Keep it compact and current.

At minimum record:

```text
Audit status: ANALYSIS INCOMPLETE | ANALYSIS COMPLETE
Last completed batch:
Next analysis target:

Evidence: TOTAL / REVIEWED / UNREVIEWED / BLOCKED / NOT_APPLICABLE
Elements: TOTAL / BEHAVIOR_MAPPED / NO_BEHAVIORAL_EFFECT / UNKNOWN
Behaviors: TOTAL / CONFIRMED / INFERRED / CONFLICTED / UNKNOWN
Target: TOTAL / EXACT / PARTIAL / MISSING / DIFFERENT / UNKNOWN / INTENTIONALLY_CHANGED / NOT_APPLICABLE
Gaps: OPEN / RESOLVED
Unknowns: OPEN / RESOLVED
Conflicts: OPEN / RESOLVED

Completed evidence IDs/ranges:
Completed element IDs/ranges:
Newest behavior ID:
Newest gap ID:
Newest unknown ID:
Newest conflict ID:
Pending structural audits:
```

## Optional repository-derived artifacts

Create separate inventories only when evidence supports them and they materially improve auditability. Examples include state, data contracts, decisions, effects, failures, interaction contracts, timing/concurrency, configuration, or verification inventories.

Do not create conceptual inventories just because a template suggests them. Do not omit a newly discovered behavior-bearing category because it is not named here.

## PRD and human-readable reports

A PRD is a generated view over the behavior model. It may group behaviors for readability, but every statement that represents recovered source behavior must retain Behavior IDs.

Human-readable prose follows the configured `output_language`. Canonical IDs, schema keys, status values, source identifiers, paths, and evidence references remain stable across languages.

Never use the PRD as the only persistence format for recovered behavior.
