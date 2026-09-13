---
name: sbpa
description: Recover, model, compare, and audit software behavior for rewrites, migrations, refactors, legacy replacement, compatibility work, or specification recovery. Use when behavioral preservation and auditable coverage matter more than code summarization.
---

# SBPA — Software Behavior Preservation Auditor

## Objective

Build an auditable preservation chain:

`SOURCE EVIDENCE -> SOFTWARE ELEMENT -> ATOMIC BEHAVIOR -> REQUIREMENT -> TARGET IMPLEMENTATION -> VERIFICATION EVIDENCE`

SBPA is domain- and language-independent. The repository defines its taxonomy. The behavior model is the source of truth; PRDs and reports are derived views.

## Mandatory protocol

1. **Evidence before interpretation.** Inspect evidence before inventing categories. Classify conclusions only as `CONFIRMED`, `INFERRED`, `CONFLICTED`, or `UNKNOWN`.
2. **Atomic behavior.** Split contracts whenever trigger, condition, input, branch, transition, output, effect, failure, ordering, timing, concurrency, persistence, or observable result differs.
3. **No importance filtering.** Minor, internal, repetitive, legacy, rare, defensive, accidental, and undocumented evidence is not permission to omit it.
4. **Explicit uncertainty.** Unknowns and conflicts remain explicit until resolved with evidence.
5. **Semantic equivalence.** Structural similarity does not establish behavioral equivalence. `EXACT` is an evidence-gated claim, not a confidence label.
6. **Measured completeness.** Never infer completeness from prose volume or apparent thoroughness.
7. **No compression of unseen work.** Never hide unreviewed behavior behind `etc.`, `similar cases`, `standard handling`, `same as above`, or equivalent language.
8. **No target bias.** Recover source semantics independently before comparing the target.

## Machine verification layer

Read `references/engine.md` before non-trivial audits. When an SBPA engine is available, use its inventory and validation results for mechanically decidable facts instead of inventing counts in prose.

Keep these coverage dimensions separate:

- structural coverage
- evidence coverage
- behavioral coverage
- verification coverage
- target equivalence coverage

Never report a single percentage as proof of total behavioral completeness.

A changed source/target artifact invalidates dependent conclusions until re-reviewed. Stable IDs survive; stale evidence does not remain valid merely because its ID is stable.

## Output language

Read `references/output-language.md`. Supported baseline values are `auto`, `zh-CN`, and `en`. Human-readable prose may be localized. Stable IDs, schema keys, status values, paths, source identifiers, evidence references, error codes, fingerprints, and semantics-bearing literals remain canonical.

Persist the chosen language in audit scope. Changing language must never change identity or traceability.

## Durable project state

For non-trivial work maintain `.sbpa/` in the audited repository. Read `references/artifacts.md` before writing artifacts and `references/behavior-model.md` before writing behavior records.

If prior state exists, continue from it. Preserve stable IDs and unresolved findings. Do not renumber records for presentation.

## Workflow

### Phase 0 — Scope

Establish source, target if any, analysis root, explicit exclusions, available evidence, output language, and revision anchors when available. Never invent exclusions.

### Phase 1 — Evidence inventory

Enumerate analyzable artifacts from the actual analysis root. Prefer machine-generated inventory when available. Every evidence item resolves to `UNREVIEWED`, `REVIEWED`, `NOT_APPLICABLE`, or `BLOCKED`; the latter two require explanations.

### Phase 2 — Element discovery

Discover native software constructs capable of behavior. Do not impose a fixed language taxonomy. Optional extractors may mechanically discover candidates but never decide semantics.

Every relevant element resolves to `BEHAVIOR_MAPPED`, `NO_BEHAVIORAL_EFFECT` with justification, or `UNKNOWN`.

### Phase 3 — Atomic behavior extraction

Create stable IDs such as `B-000001` and use the canonical behavior model. Record only dimensions supported by evidence. Fingerprints may aid duplicate/split/merge detection but never replace stable IDs.

### Phase 4 — Repository-derived inventories

Create cross-cutting inventories only when evidence supports them. Possible lenses include state, decisions, data contracts, effects, failures, interaction surfaces, temporal/concurrency semantics, configuration, and verification. Extend the taxonomy when evidence reveals another behavior-bearing class.

### Phase 5 — Requirement projection

Project recovered behaviors into requirements with backlinks to Behavior IDs and source evidence. Keep newly requested product behavior separate from recovered source behavior.

### Phase 6 — Target mapping

After source semantics are independently established, map each behavior to exactly one of `EXACT`, `PARTIAL`, `MISSING`, `DIFFERENT`, `UNKNOWN`, `NOT_APPLICABLE`, or `INTENTIONALLY_CHANGED`.

`INTENTIONALLY_CHANGED` requires explicit approval evidence. `EXACT` requires sufficient source, target, and verification evidence across every relevant discovered dimension; otherwise choose a more accurate status.

### Phase 7 — Traceability

Maintain exactly one primary traceability row per discovered Behavior ID connecting source evidence, requirement, target evidence, target status, and verification evidence.

### Phase 8 — Reverse coverage audit

Audit both directions: evidence -> element -> behavior; element -> behavior; behavior -> requirement; requirement -> target when applicable; verification evidence -> behavior. Also audit every repository-derived inventory member back to behavior coverage. Broken chains create gaps.

### Phase 9 — Gap / Unknown / Conflict registers

Use stable `G-000001`, `U-000001`, and `C-000001` IDs. Resolve only with evidence; preserve resolution history where practical.

### Phase 10 — Verification projection

When historical verification is insufficient, derive acceptance specifications from behavior contracts. Clearly mark generated acceptance specifications as generated verification, never as recovered historical evidence.

### Phase 11 — Completion decision

Read `references/completion.md` and apply its gate mechanically. Run machine validation when available. If the gate fails, state `ANALYSIS INCOMPLETE`, unresolved counts, stale evidence, and the next target.

## Decision coverage

Whenever evidence selects among materially different outcomes, enumerate meaningful alternatives. Each must map to an existing/new Behavior ID or `NO_BEHAVIORAL_EFFECT` with justification. Syntax is repository-specific; do not search only for a hard-coded keyword list.

## Verification evidence

Executable expectations are evidence. Map independently meaningful tests, assertions, snapshots, fixtures, contracts, validation scripts, examples, or equivalent artifacts to behaviors. Conflicts remain `CONFLICTED`; no evidence class is automatically authoritative.

## Incremental audits

Context limits are not permission to summarize unseen evidence. Analyze in bounded batches, persist completed ranges and unresolved IDs, and continue from the ledger. If repository revisions change, invalidate and re-review affected evidence/behaviors before retaining equivalence claims.

## Progress reporting

Report coverage dimensions separately plus open gaps, unknowns, conflicts, stale evidence, and next analysis target. Human-readable labels follow output language; canonical values do not.

## Acceptance question

For every discovered source behavior answer:

> What evidence proves it existed, what atomic contract represents it, what requirement projects it, where is it implemented in the target, and what evidence proves preservation?

If an applicable link is missing, the behavior is not fully migrated.

## Priority

Coverage over prose. Evidence over confidence. Traceability over summarization. Explicit unknowns over assumptions. Machine-auditable state over impressive narrative output.
