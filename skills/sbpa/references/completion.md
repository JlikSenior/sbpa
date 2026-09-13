# Completion Gate

Apply this gate mechanically before claiming that an SBPA audit is complete.

## Required closure conditions

All of the following must be true within the declared scope:

1. Evidence inventory has no unexplained `UNREVIEWED` items.
2. Every relevant element is `BEHAVIOR_MAPPED` or justified `NO_BEHAVIORAL_EFFECT`.
3. Every meaningful decision alternative is behavior-mapped or justified as having no behavioral effect.
4. Every independently meaningful verification expectation is behavior-mapped or explicitly unresolved.
5. Every discovered behavior has a primary traceability row.
6. Every applicable requirement points back to behavior IDs.
7. When a target exists, every behavior has a target status supported by evidence.
8. Structural reverse audits have no open unmapped items.
9. Open gaps, unknowns, and conflicts are explicitly counted and represented.
10. No region was silently skipped because of context limits, repetition, perceived importance, unfamiliar syntax, or output length.

## Completion states

Use `ANALYSIS COMPLETE` only when scope coverage is closed.

Open Unknown or Conflict records do not automatically prevent scope coverage from closing if the uncertainty itself is explicitly inventoried and all evidence has been reviewed. In that case, distinguish:

- coverage complete
- semantic certainty incomplete

Never imply that unresolved semantics are migrated successfully.

Use `ANALYSIS INCOMPLETE` whenever repository traversal or structural mapping remains unfinished.

## Required final summary

Report:

```text
Audit status:
Coverage closure:
Semantic certainty:

Evidence: TOTAL / REVIEWED / UNREVIEWED / BLOCKED / NOT_APPLICABLE
Elements: TOTAL / BEHAVIOR_MAPPED / NO_BEHAVIORAL_EFFECT / UNKNOWN
Behaviors: TOTAL / CONFIRMED / INFERRED / CONFLICTED / UNKNOWN
Target: TOTAL / EXACT / PARTIAL / MISSING / DIFFERENT / UNKNOWN / INTENTIONALLY_CHANGED / NOT_APPLICABLE
Gaps: OPEN / RESOLVED
Unknowns: OPEN / RESOLVED
Conflicts: OPEN / RESOLVED
```

If incomplete, also report the exact next analysis target.
