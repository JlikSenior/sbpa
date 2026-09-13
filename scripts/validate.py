#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]; errors=[]
required=[
 ROOT/'plugin.json',ROOT/'skills/sbpa/SKILL.md',ROOT/'skills/sbpa/references/behavior-model.md',
 ROOT/'skills/sbpa/references/artifacts.md',ROOT/'skills/sbpa/references/completion.md',
 ROOT/'skills/sbpa/references/output-language.md',ROOT/'skills/sbpa/references/engine.md',
 ROOT/'schemas/behavior.schema.json',ROOT/'engine/sbpa.py',ROOT/'engine/sbpa_engine/__init__.py',
 ROOT/'engine/sbpa_engine/common.py',ROOT/'engine/sbpa_engine/state.py',
 ROOT/'engine/sbpa_engine/inventory.py',ROOT/'engine/sbpa_engine/validator.py',
 ROOT/'tests/test_engine.py',ROOT/'install.sh',ROOT/'install.ps1']
for p in required:
 if not p.is_file():errors.append('missing required file: '+str(p.relative_to(ROOT)))
try:
 m=json.loads((ROOT/'plugin.json').read_text())
 if m.get('name')!='sbpa':errors.append("plugin.json name must be 'sbpa'")
 if m.get('$schema')!='https://agent-plugins.org/schemas/1.0.0/plugin.schema.json':errors.append('plugin.json must target Agent Plugins schema 1.0.0')
except Exception as e:errors.append('plugin.json invalid: '+str(e))
for p in [ROOT/'schemas/behavior.schema.json']:
 try:json.loads(p.read_text())
 except Exception as e:errors.append(str(p.relative_to(ROOT))+' invalid JSON: '+str(e))
s=ROOT/'skills/sbpa/SKILL.md'
if s.is_file():
 t=s.read_text()
 for needle in ['name: sbpa','ANALYSIS INCOMPLETE','Evidence before interpretation','references/engine.md','structural coverage','verification coverage','EXACT']:
  if needle not in t:errors.append('SKILL.md missing invariant: '+needle)
if errors:
 for e in errors:print('ERROR:',e)
 sys.exit(1)
print('SBPA repository validation passed')
