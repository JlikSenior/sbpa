# SBPA Engine Contract

The Skill is the semantic protocol. The engine is the independent bookkeeping and verification layer. Agents MUST NOT manufacture coverage counts when an SBPA engine command is available.

## Commands

A conforming engine should expose four baseline operations:

- `sbpa init` — create durable audit state and pin audit metadata.
- `sbpa inventory` — derive an evidence inventory from the actual analysis root rather than model memory.
- `sbpa validate` — reject structurally invalid audit state and unsupported completion claims.
- `sbpa status` — calculate coverage dimensions from persisted artifacts.

## Machine authority

For filesystem membership, hashes, schema validity, duplicate IDs, referential integrity, and mechanically calculable coverage counts, engine output takes precedence over agent-authored prose.

The agent remains responsible for semantic interpretation. The engine must not pretend that structural coverage proves behavioral completeness.

## Coverage dimensions

Report coverage separately. Never collapse them into one misleading percentage.

- **Structural coverage**: discovered repository artifacts/elements accounted for.
- **Evidence coverage**: inventoried evidence reviewed or explicitly resolved.
- **Behavioral coverage**: discovered behavior-bearing constructs mapped to atomic contracts.
- **Verification coverage**: behavior contracts backed by verification evidence.
- **Target equivalence coverage**: source behaviors mapped to target statuses with sufficient evidence.

A 100% value in one dimension does not imply 100% in another.

## EXACT gate

`EXACT` is a claim requiring evidence, not a confidence label. A validator SHOULD reject an EXACT mapping unless it has source evidence, target evidence, and verification evidence for every relevant discovered semantic dimension. If verification is unavailable, use `UNKNOWN` or another more accurate status rather than EXACT.

## Inventory freshness

Inventories SHOULD bind entries to content hashes and, when available, repository revisions. A changed source artifact invalidates conclusions that depend on the previous artifact version until re-reviewed.

## Incremental invalidation

When source or target revisions change, compare the new revision to the pinned revision. Mark affected evidence and dependent behaviors stale. Do not preserve an old EXACT status solely because its Behavior ID still exists.

## Behavior fingerprints

Stable Behavior IDs are human audit identities. A fingerprint is a machine aid for duplicate/split/merge detection. Fingerprints MUST NOT replace IDs. Generate fingerprints from canonical, language-neutral contract identity and source anchors; changing human-readable output language must not change the fingerprint.

## Extractor boundary

SBPA core remains language-independent. Language/framework extractors are optional adapters that mechanically expose candidate elements, branches, declarations, tests, and other behavior-bearing structures. Extractors discover candidates; they do not decide semantic behavior.

This separation is intentional:

`Extractor -> candidates -> Agent semantic analysis -> Behavior Store -> Validator`

## Acceptance specifications

When existing verification is insufficient, SBPA SHOULD project behaviors into acceptance specifications without pretending those generated specifications are historical source evidence. Keep generated verification distinct from recovered evidence.
