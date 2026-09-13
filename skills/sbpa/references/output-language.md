# Output Language Protocol

SBPA separates human-readable language from machine-stable audit semantics.

## Configuration

Record the selected language in `.sbpa/scope.md`:

```yaml
output_language: auto
technical_terms: preserve
source_identifiers: preserve
```

### `output_language`

Supported values:

- `auto` — default. Follow the user's primary language for human-readable output.
- `zh-CN` — Simplified Chinese.
- `en` — English.

If the user explicitly requests another language, use the requested BCP 47 language tag when practical and record it in `scope.md`. Do not silently change the configured language between analysis batches.

Explicit user instruction always overrides `auto`.

Examples:

- "Use SBPA in Chinese." -> `zh-CN`
- "用中文执行 SBPA。" -> `zh-CN`
- "Use SBPA in English." -> `en`
- no language instruction -> `auto`

When continuing an existing audit, reuse the language stored in `.sbpa/scope.md` unless the user explicitly changes it.

## What is localized

Translate or author in `output_language`:

- behavior titles and descriptions
- requirement prose
- PRD prose
- gap descriptions and recommendations
- unknown questions and explanations
- conflict descriptions
- coverage reports
- progress reports
- human-readable notes
- headings in generated human-facing reports when doing so does not break a machine schema

## What must remain stable

Do NOT translate or rewrite machine-stable values solely because the output language changes:

- stable IDs such as `B-000001`, `G-000001`, `U-000001`, `C-000001`
- evidence IDs and element IDs
- canonical enum/status values defined by SBPA, including `CONFIRMED`, `INFERRED`, `CONFLICTED`, `UNKNOWN`, `EXACT`, `PARTIAL`, `MISSING`, `DIFFERENT`, `NOT_APPLICABLE`, `INTENTIONALLY_CHANGED`, `UNREVIEWED`, `REVIEWED`, `BLOCKED`, `BEHAVIOR_MAPPED`, and `NO_BEHAVIORAL_EFFECT`
- CSV/YAML field names defined by the canonical SBPA schemas
- file and directory paths
- source identifiers
- function, method, type, class, module, package, variable, constant, command, route, event, and symbol names taken from evidence
- error codes and protocol values taken from evidence
- literal values where translation would change semantics

A language change must never break traceability or make two records appear to be different behaviors.

## Technical terms

Default: `technical_terms: preserve`.

Preserve source-native technical terms when translation could introduce ambiguity. Explanatory prose may include a localized explanation, but the canonical technical term should remain available where needed for precision.

Do not translate identifiers merely to make prose look natural.

## Source identifiers

Default: `source_identifiers: preserve`.

Always preserve identifiers exactly as evidenced, including spelling and case. If a localized explanation is useful, put it in prose around the identifier rather than replacing the identifier.

## Machine-readable artifacts

Canonical schema keys and status values stay language-neutral and stable.

Example in Chinese mode:

```yaml
id: B-000123
title: 配置加载失败时使用默认值
evidence_class: CONFIRMED
source_evidence:
  - src/config.rs::load_config
target_status: EXACT
```

Example in English mode:

```yaml
id: B-000123
title: Use the default value when configuration loading fails
evidence_class: CONFIRMED
source_evidence:
  - src/config.rs::load_config
target_status: EXACT
```

The ID, keys, evidence references, and canonical status values remain unchanged.

## Existing audit language changes

If the user changes language during an existing audit:

1. update `output_language` in `.sbpa/scope.md`;
2. use the new language for subsequent human-readable output;
3. do not renumber or recreate stable records;
4. do not alter source evidence or canonical status values;
5. do not mass-translate historical artifacts unless the user requests it;
6. if historical artifacts are translated, preserve IDs, schema keys, evidence references, and semantic meaning exactly.

## Governing rule

Localization is a presentation concern, not a behavioral transformation.

Language may change.

Evidence, identity, status semantics, and traceability must not.