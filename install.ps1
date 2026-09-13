param(
  [string]$Target = (Get-Location).Path,
  [switch]$Global,
  [string]$Ref = "main"
)

$ErrorActionPreference = "Stop"
$Repo = "JlikSenior/sbpa"

if ($Global) {
  $Dest = Join-Path $HOME ".agents/skills/sbpa"
} else {
  $resolved = (Resolve-Path $Target).Path
  $Dest = Join-Path $resolved ".agents/skills/sbpa"
}

$Base = "https://raw.githubusercontent.com/$Repo/$Ref/skills/sbpa"
$Tmp = "$Dest.tmp.$PID"
$Backup = "$Dest.backup.$PID"

function Fetch-File([string]$Url, [string]$OutFile) {
  $parent = Split-Path -Parent $OutFile
  New-Item -ItemType Directory -Force -Path $parent | Out-Null
  Invoke-WebRequest -Uri $Url -OutFile $OutFile -UseBasicParsing
}

try {
  New-Item -ItemType Directory -Force -Path (Join-Path $Tmp "references") | Out-Null

  Fetch-File "$Base/SKILL.md" (Join-Path $Tmp "SKILL.md")
  Fetch-File "$Base/references/behavior-model.md" (Join-Path $Tmp "references/behavior-model.md")
  Fetch-File "$Base/references/artifacts.md" (Join-Path $Tmp "references/artifacts.md")
  Fetch-File "$Base/references/completion.md" (Join-Path $Tmp "references/completion.md")

  $skill = Get-Content (Join-Path $Tmp "SKILL.md") -Raw
  if ($skill -notmatch "(?m)^name: sbpa$") { throw "Invalid SBPA skill metadata" }
  if ($skill -notmatch "(?m)^# SBPA") { throw "Invalid SBPA skill payload" }

  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Dest) | Out-Null

  if (Test-Path $Dest) {
    Move-Item $Dest $Backup
  }

  try {
    Move-Item $Tmp $Dest
    if (Test-Path $Backup) { Remove-Item -Recurse -Force $Backup }
  } catch {
    if ((Test-Path $Backup) -and -not (Test-Path $Dest)) {
      Move-Item $Backup $Dest
    }
    throw
  }

  Write-Host "SBPA installed: $Dest"
  Write-Host "Use: ask your agent to 'Use SBPA to audit this repository.'"
} finally {
  if (Test-Path $Tmp) { Remove-Item -Recurse -Force $Tmp }
}
