---
name: sbpa
description: Exhaustively recover, model, compare, and audit software behavior for rewrites, migrations, refactors, legacy replacement, compatibility work, or specification recovery. Use when preserving behavior matters more than summarizing code.
---

# SBPA — Software Behavior Preservation Auditor

## Purpose

Recover and preserve software behavior from evidence.

SBPA is domain-independent. Do not assume a language, framework, architecture, application type, interaction model, persistence model, deployment model, or business domain before inspecting evidence. The repository defines its own taxonomy.

## Governing objective

Build and maintain this auditable chain:

`SOURCE EVIDENCE -> SOFTWARE ELEMENT -> ATOMIC BEHAVIOR -> REQUIREMENT -> TARGET IMPLEMENTATION -> VERIFICATION EVIDENCE`

Any relevant source behavior that cannot be traced through the chain remains unresolved.

The behavior model is the source of truth. PRDs, feature lists, migration reports, state views, and gap reports are derived views. Never treat a prose summary as a substitute for the behavior model.

## Mandatory invariants

### 1. Evidence before interpretation

Inspect evidence before inventing categories. Names, comments, docs, conventions, target code, and prior expectations may guide investigation but do not by themselves establish behavior.

Classify conclusions as exactly one of:

- `CONFIRMED` — directly supported by inspected evidence.
- `INFERRED` — strongly implied but not directly established.
- `CONFLICTED` — inspected evidence disagrees.
- `UNKNOWN` — evidence is insufficient.

Never silently promote `INFERRED`, `CONFLICTED`, or `UNKNOWN` to `CONFIRMED`.

### 2. Atomic behavior, not feature compression

Separate behavior whenever trigger, precondition, accepted input, rejected input, branch, transition, output, side effect, failure semantics, ordering, timing, concurrency, persistence, or observable result differs.

One behavior record should represent one independently verifiable behavioral contract. Do not replace multiple contracts with a high-level feature statement.

### 3. No importance filtering

Do not omit evidence because it appears minor, internal, repetitive, legacy, rare, defensive, accidental, inconvenient, undocumented, or non-critical.

Record it, or explicitly classify why it has no behavioral effect.

### 4. Explicit uncertainty

If behavior cannot be established, create or update an Unknown record. If evidence disagrees, create or update a Conflict record. Never guess to close coverage.

### 5. Behavioral equivalence over structural similarity

A target implementation may differ structurally. Compare semantics, not code shape.

A target behavior is `EXACT` only when evidence demonstrates equivalence across every relevant dimension discovered for that behavior. Missing evidence means `UNKNOWN`, not `EXACT`.

### 6. Completeness is measured

Never claim completeness because the analysis looks thorough. Completeness is a coverage-ledger state.

Do not declare analysis complete while unexplained evidence, relevant elements, meaningful branches, verification expectations, or structural coverage gaps remain unresolved.

## Output language

SBPA supports configurable human-readable output language without changing machine-stable audit semantics.

Read `references/output-language.md` before producing or updating audit artifacts.

The default is:

```yaml
output_language: auto
technical_terms: preserve
source_identifiers: preserve
```

`auto` follows the user's primary language. At minimum, support `zh-CN` and `en`. An explicit user language request overrides `auto` and must be persisted in `.sbpa/scope.md` for subsequent batches.

Only human-readable prose is localized. Stable IDs, canonical schema keys, canonical status values, file paths, source identifiers, evidence references, error codes, protocol values, and other semantics-bearing literals must remain unchanged unless the source evidence itself changes.

Changing output language must never break identity, traceability, comparison, or continuation of an existing audit.

## Project state

For non-trivial work, maintain durable audit state under `.sbpa/` in the repository being analyzed.

Read `references/artifacts.md` before creating or updating audit artifacts.

If `.sbpa/ledger.md` already exists, continue from it. Preserve stable IDs. Never renumber existing IDs to make output prettier.

Do not overwrite unresolved findings merely because a later pass has less context.

## Required workflow

### Phase 0 — Scope

Establish the source system, target system if any, analysis root, explicit exclusions if any, available evidence, and output language.

Never invent exclusions.

If the repository is too large for one context, define an incremental traversal order and record it in the ledger.

### Phase 1 — Evidence inventory

Enumerate analyzable artifacts before making a completeness claim.

Evidence can include any artifact capable of establishing behavior. Do not limit discovery to source code.

Each evidence item must end in one state:

- `UNREVIEWED`
- `REVIEWED`
- `NOT_APPLICABLE`
- `BLOCKED`

`NOT_APPLICABLE` and `BLOCKED` require explanations.

### Phase 2 — Software element discovery

Discover identifiable constructs capable of contributing to behavior using the native abstractions of the repository.

Do not impose a fixed language-specific element taxonomy.

Every relevant element must resolve to one of:

- `BEHAVIOR_MAPPED`
- `NO_BEHAVIORAL_EFFECT`
- `UNKNOWN`

`NO_BEHAVIORAL_EFFECT` requires justification.

### Phase 3 — Atomic behavior extraction

Create stable behavior IDs such as `B-000001`.

For every behavior, capture all dimensions supported by evidence. Use the canonical schema in `references/behavior-model.md`.

Do not fabricate values for absent dimensions. Use `N/A` only when non-applicability is established.

### Phase 4 — Repository-derived cross-cutting inventories

Create only inventories supported by discovered evidence.

Possible discovery lenses include state, decisions, data contracts, effects, failures, interaction surfaces, temporal semantics, concurrency semantics, configuration semantics, and verification evidence. These are lenses, not assumptions that such concepts must exist.

Extend the taxonomy if repository evidence reveals another behavior-bearing class.

### Phase 5 — Requirement projection

Project confirmed behaviors, and explicitly labeled inferred behaviors when useful, into implementation requirements.

Every requirement must retain backlinks to behavior IDs and source evidence.

Do not author independent requirements that cannot be traced to evidence unless the user explicitly asks for new product behavior. Keep new requirements separate from recovered behavior.

### Phase 6 — Target mapping

If a target implementation exists, analyze source semantics independently first, then inspect the target.

Map each source behavior to exactly one primary target status:

- `EXACT`
- `PARTIAL`
- `MISSING`
- `DIFFERENT`
- `UNKNOWN`
- `NOT_APPLICABLE`
- `INTENTIONALLY_CHANGED`

`INTENTIONALLY_CHANGED` requires explicit evidence of an approved intended change. Without that evidence use `DIFFERENT`, `MISSING`, or `UNKNOWN` as appropriate.

### Phase 7 — Traceability

Maintain a primary traceability row for every discovered behavior.

Each row must connect behavior ID, source evidence, requirement, target evidence if any, target status, and verification evidence if any.

A behavior may cite multiple evidence items but must not disappear inside another row.

### Phase 8 — Reverse coverage audit

Audit in reverse, not only forward.

At minimum verify:

- evidence -> element -> behavior
- element -> behavior
- behavior -> requirement
- requirement -> target, when a target exists
- verification evidence -> behavior

For every repository-derived inventory, also audit each meaningful member back to behavior coverage. Any broken chain creates a coverage gap.

### Phase 9 — Gap, Unknown, and Conflict registers

Create stable IDs:

- gaps: `G-000001`
- unknowns: `U-000001`
- conflicts: `C-000001`

Never delete unresolved records merely to improve completion metrics. Resolve them only with evidence and preserve resolution history where practical.

### Phase 10 — Completion decision

Read `references/completion.md` and apply the completion gate mechanically.

If the gate is not satisfied, state `ANALYSIS INCOMPLETE` and report unresolved counts and the next analysis target.

## Decision coverage rule

Whenever inspected evidence contains a construct that selects among materially different outcomes, enumerate the meaningful alternatives and map each to behavior coverage.

The syntax is repository-specific. Do not search only for a fixed list of language keywords.

A meaningful alternative must resolve to an existing Behavior ID, a newly created Behavior ID, or `NO_BEHAVIORAL_EFFECT` with justification. Unmapped meaningful alternatives are coverage gaps.

## Verification rule

Executable expectations are evidence, not decoration.

Where tests, assertions, snapshots, fixtures, validation scripts, examples, contracts, or equivalent verification artifacts encode behavior, map independently meaningful expectations to Behavior IDs.

If verification evidence conflicts with implementation evidence, record `CONFLICTED`; do not silently choose one.

## Source conflict rule

Documentation is evidence, not authority. Tests are evidence, not automatically authority. Runtime code is evidence, not automatically the intended contract.

When evidence sources disagree, preserve the disagreement in the Conflict register with affected Behavior IDs and a verification path.

## Anti-compression rule

Never conceal unreviewed or unenumerated behavior behind language equivalent to `etc.`, `and so on`, `similar cases`, `standard handling`, `usual behavior`, `remaining cases`, `miscellaneous`, or `same as above`.

Enumerate the items or mark them not yet analyzed.

## Target-bias rule

Never infer source intent from what the target implementation currently does.

Source discovery and source behavior extraction must be independently defensible before target comparison.

## Context-limit rule

Context limits are not permission to summarize unseen evidence.

For large repositories:

1. analyze in bounded batches;
2. persist completed Evidence IDs, Element IDs, Behavior IDs, unresolved Gap/Unknown/Conflict IDs, current coverage metrics, and the next analysis range;
3. continue from the ledger in the next batch;
4. preserve stable IDs across batches.

## Required progress report

At the end of each analysis batch, report at least:

- Evidence: total / reviewed / unreviewed / blocked / not applicable
- Elements: total / behavior mapped / no behavioral effect / unknown
- Behaviors: total / confirmed / inferred / conflicted / unknown
- Target mapping, if applicable: exact / partial / missing / different / unknown / intentionally changed / not applicable
- Open gaps
- Open unknowns
- Open conflicts
- Next analysis target

Render human-readable labels and prose according to `output_language`, while preserving canonical machine values.

## Final acceptance question

For every behavior discovered in the source system, be able to answer:

> What evidence proves this behavior existed, what behavior contract represents it, what requirement projects it, where is it implemented in the target system, and what evidence proves the target preserves it?

If any applicable part cannot be answered, that behavior is not fully migrated.

## Output priority

Optimize for:

1. coverage over prose,
2. evidence over confidence,
3. traceability over summarization,
4. explicit unknowns over assumptions,
5. durable machine-auditable state over impressive narrative output.
