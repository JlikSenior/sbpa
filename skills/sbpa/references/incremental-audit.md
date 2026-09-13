# Incremental Audit Protocol

SBPA must treat repository changes as evidence invalidation events, not as ordinary continuation.

## Change classes

Compare the current analysis root against the last machine inventory and classify artifacts as:

- `ADDED`
- `CHANGED`
- `DELETED`
- `UNCHANGED`

Content hashes are the baseline mechanism. Repository revisions may be recorded as additional anchors.

## Invalidation rule

A changed or deleted evidence item invalidates every conclusion that materially depends on the previous version of that evidence until it is re-reviewed.

At minimum, affected records must not retain an `EXACT` target status merely because their stable Behavior IDs are unchanged.

An added artifact is `UNREVIEWED` evidence until analyzed or explicitly resolved.

## Dependency propagation

When dependency links are available, propagate staleness through this chain:

`Evidence -> Element -> Behavior -> Requirement -> Target Mapping -> Verification`

A future engine may automate this graph. Until then, the agent must record affected Behavior IDs and unresolved re-review work explicitly.

## Stable identity

Invalidation does not renumber stable IDs. It changes evidence validity and review state, not historical identity.

## Completion gate

Analysis cannot return to `ANALYSIS COMPLETE` while stale evidence or stale dependent conclusions remain unresolved.
