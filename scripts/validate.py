#!/usr/bin/env python3
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

required = [
    ROOT / "plugin.json",
    ROOT / "skills" / "sbpa" / "SKILL.md",
    ROOT / "skills" / "sbpa" / "references" / "behavior-model.md",
    ROOT / "skills" / "sbpa" / "references" / "artifacts.md",
    ROOT / "skills" / "sbpa" / "references" / "completion.md",
    ROOT / "install.sh",
    ROOT / "install.ps1",
]

for path in required:
    if not path.is_file():
        errors.append(f"missing required file: {path.relative_to(ROOT)}")

try:
    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    if manifest.get("name") != "sbpa":
        errors.append("plugin.json name must be 'sbpa'")
    if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        errors.append("plugin.json must target Agent Plugins schema 1.0.0")
except Exception as exc:
    errors.append(f"plugin.json invalid: {exc}")

skill_path = ROOT / "skills" / "sbpa" / "SKILL.md"
if skill_path.is_file():
    skill = skill_path.read_text(encoding="utf-8")
    if not skill.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter")
    if not re.search(r"(?m)^name: sbpa$", skill):
        errors.append("SKILL.md frontmatter must declare name: sbpa")
    if not re.search(r"(?m)^description: .+", skill):
        errors.append("SKILL.md frontmatter must declare a description")
    if "ANALYSIS INCOMPLETE" not in skill:
        errors.append("SKILL.md must preserve the incomplete-analysis status rule")
    if "Evidence before interpretation" not in skill:
        errors.append("SKILL.md must preserve the evidence-first invariant")

if errors:
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(1)

print("SBPA repository validation passed")
