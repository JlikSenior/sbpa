# Extractor Contract

Extractors are optional mechanical discovery adapters. They increase structural visibility without deciding software semantics.

## Core boundary

`Repository evidence -> Extractor candidates -> Agent semantic analysis -> Behavior model`

An extractor MAY identify declarations, branches, tests, configuration items, state-bearing constructs, relations, or other repository-native structures.

An extractor MUST NOT:

- mark behavior as `CONFIRMED` by itself;
- decide that two source/target behaviors are `EXACT`;
- invent requirements;
- hide unsupported structures because they are unfamiliar;
- convert framework conventions into facts without evidence.

## Candidate format

Candidates use stable run-local IDs such as `X-000001` and reference an existing Evidence ID. Use `schemas/extractor-candidate.schema.json` as the interchange contract.

The `kind`, `native_name`, `native_classification`, and `attributes` fields remain repository-native. SBPA does not impose one universal language taxonomy.

## Capabilities

Each extractor should declare which candidate classes it can reliably discover. Missing capability must be explicit; absence of a candidate from an extractor is not proof that the repository lacks that kind of behavior.

## Determinism

Given the same extractor version and identical evidence bytes, candidate identity/order should be deterministic where practical. Extractor version must be recorded so candidate changes can be distinguished from repository changes.

## Evidence anchoring

Every candidate must anchor to evidence and, where available, precise locations. Candidate metadata is derived evidence about structure, not a substitute for the underlying source artifact.

## Composition

Multiple extractors may operate on the same evidence. The semantic analysis layer must reconcile overlap without silently deduplicating materially different candidates.

## Failure behavior

Extractor parse failures, unsupported syntax, partial parsing, or skipped regions must be surfaced as coverage limitations. Do not treat parser success on part of a file as full structural coverage.
