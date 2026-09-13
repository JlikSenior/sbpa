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

$Work = Join-Path ([System.IO.Path]::GetTempPath()) ("sbpa-" + [Guid]::NewGuid().ToString("N"))
$Zip = Join-Path $Work "sbpa.zip"
$Extract = Join-Path $Work "extract"
$Staged = Join-Path $Work "staged"
$Backup = "$Dest.backup.$PID"
$Url = "https://github.com/$Repo/archive/$Ref.zip"

try {
  New-Item -ItemType Directory -Force -Path $Work | Out-Null
  Invoke-WebRequest -Uri $Url -OutFile $Zip -UseBasicParsing
  Expand-Archive -Path $Zip -DestinationPath $Extract -Force

  $SkillFile = Get-ChildItem -Path $Extract -Recurse -File -Filter "SKILL.md" |
    Where-Object { $_.FullName -match '[\\/]skills[\\/]sbpa[\\/]SKILL\.md$' } |
    Select-Object -First 1

  if (-not $SkillFile) { throw "skills/sbpa/SKILL.md not found in archive" }

  $Source = Split-Path -Parent $SkillFile.FullName
  Copy-Item -Path $Source -Destination $Staged -Recurse

  $Skill = Get-Content (Join-Path $Staged "SKILL.md") -Raw
  if ($Skill -notmatch "(?m)^name: sbpa$") { throw "Invalid SBPA skill metadata" }
  if ($Skill -notmatch "(?m)^# SBPA") { throw "Invalid SBPA skill payload" }

  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Dest) | Out-Null

  if (Test-Path $Dest) {
    Move-Item $Dest $Backup
  }

  try {
    Move-Item $Staged $Dest
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
  if (Test-Path $Work) { Remove-Item -Recurse -Force $Work }
}
