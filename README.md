# SBPA

**Software Behavior Preservation Auditor** — a domain-independent Agent Skill for exhaustive software behavior discovery, specification recovery, migration auditing, and behavioral equivalence tracking.

SBPA is designed for rewrites, refactors, language/framework migrations, legacy replacement, compatibility audits, and specification recovery. It does **not** assume a language, framework, UI, database, network stack, architecture, or business domain.

## Install into a project

macOS / Linux / WSL:

```bash
curl -fsSL https://raw.githubusercontent.com/JlikSenior/sbpa/main/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://raw.githubusercontent.com/JlikSenior/sbpa/main/install.ps1 | iex
```

The default installation target is:

```text
<project>/.agents/skills/sbpa/
```

`.agents/skills/` is the portable Agent Skills project convention and is supported by compatible coding agents. Project-level skills take precedence over user-level skills.

Install globally instead:

```bash
curl -fsSL https://raw.githubusercontent.com/JlikSenior/sbpa/main/install.sh | bash -s -- --global
```

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/JlikSenior/sbpa/main/install.ps1))) -Global
```

Install into a specific project:

```bash
curl -fsSL https://raw.githubusercontent.com/JlikSenior/sbpa/main/install.sh | bash -s -- --target /path/to/project
```

Re-run the same command to update SBPA. The installer replaces only `.agents/skills/sbpa` and leaves the rest of the project untouched.

## Use

Ask your agent to use SBPA, for example:

```text
Use SBPA to recover the complete behavioral specification of this repository.
```

```text
Use SBPA to compare the source implementation with the rewrite and produce a traceability matrix and migration gap report.
```

```text
Use SBPA to continue the previous audit from the existing .sbpa ledger.
```

SBPA maintains analysis state under `.sbpa/` in the audited repository so large codebases can be processed incrementally without silently compressing unreviewed code.

## Portable package

This repository is also an [Agent Plugins](https://agent-plugins.org/) compatible package:

```text
sbpa/
├── plugin.json
├── skills/
│   └── sbpa/
│       ├── SKILL.md
│       └── references/
├── install.sh
└── install.ps1
```

The canonical skill source lives only in `skills/sbpa/`. Installers copy that directory into the target project's `.agents/skills/` path, avoiding duplicated skill definitions.

## Design principles

SBPA is built around five invariants:

1. **Evidence before interpretation** — repository facts define the taxonomy.
2. **Atomic behavior over feature summaries** — independent contracts remain independently traceable.
3. **Explicit uncertainty** — unknown, inferred, and conflicting evidence are never silently promoted to fact.
4. **Measured coverage** — completeness is a ledger state, not a confidence statement.
5. **Bidirectional traceability** — source evidence → behavior → requirement → target → verification, plus reverse coverage audits.

## Output model

The behavior model is the source of truth. PRDs, requirement tables, gap reports, state views, and migration reports are generated views over that model rather than independent summaries.

Default project artifacts live under `.sbpa/`:

```text
.sbpa/
├── scope.md
├── evidence.csv
├── elements.csv
├── behaviors.yaml
├── traceability.csv
├── gaps.md
├── unknowns.md
├── conflicts.md
└── ledger.md
```

Only inventories supported by repository evidence need to be created.

## License

MIT
