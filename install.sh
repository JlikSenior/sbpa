#!/usr/bin/env bash
set -euo pipefail

REPO="JlikSenior/sbpa"
REF="main"
TARGET_ROOT="$(pwd)"
GLOBAL=0

usage() {
  cat <<'EOF'
SBPA installer

Usage:
  install.sh [--target PATH] [--global] [--ref REF]

Options:
  --target PATH  Install into PATH/.agents/skills/sbpa
  --global       Install into ~/.agents/skills/sbpa
  --ref REF      Install from a branch, tag, or commit (default: main)
  -h, --help     Show this help
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target)
      [ "$#" -ge 2 ] || { echo "error: --target requires a path" >&2; exit 2; }
      TARGET_ROOT="$2"
      shift 2
      ;;
    --global)
      GLOBAL=1
      shift
      ;;
    --ref)
      [ "$#" -ge 2 ] || { echo "error: --ref requires a value" >&2; exit 2; }
      REF="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [ "$GLOBAL" -eq 1 ]; then
  DEST="${HOME}/.agents/skills/sbpa"
else
  TARGET_ROOT="$(cd "$TARGET_ROOT" && pwd)"
  DEST="${TARGET_ROOT}/.agents/skills/sbpa"
fi

BASE="https://raw.githubusercontent.com/${REPO}/${REF}/skills/sbpa"
TMP="${DEST}.tmp.$$"
BACKUP="${DEST}.backup.$$"

cleanup() {
  rm -rf "$TMP"
}
trap cleanup EXIT

mkdir -p "$TMP/references"

fetch() {
  url="$1"
  output="$2"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$url" -o "$output"
  elif command -v wget >/dev/null 2>&1; then
    wget -q "$url" -O "$output"
  else
    echo "error: curl or wget is required" >&2
    exit 1
  fi
}

fetch "$BASE/SKILL.md" "$TMP/SKILL.md"
fetch "$BASE/references/behavior-model.md" "$TMP/references/behavior-model.md"
fetch "$BASE/references/artifacts.md" "$TMP/references/artifacts.md"
fetch "$BASE/references/completion.md" "$TMP/references/completion.md"

# Minimal integrity checks before replacing an existing installation.
grep -q '^name: sbpa$' "$TMP/SKILL.md" || { echo "error: invalid SBPA skill metadata" >&2; exit 1; }
grep -q '^# SBPA' "$TMP/SKILL.md" || { echo "error: invalid SBPA skill payload" >&2; exit 1; }

mkdir -p "$(dirname "$DEST")"
if [ -e "$DEST" ]; then
  mv "$DEST" "$BACKUP"
fi

if mv "$TMP" "$DEST"; then
  rm -rf "$BACKUP"
else
  [ ! -e "$BACKUP" ] || mv "$BACKUP" "$DEST"
  echo "error: installation failed; previous installation restored" >&2
  exit 1
fi

trap - EXIT

echo "SBPA installed: $DEST"
echo "Use: ask your agent to 'Use SBPA to audit this repository.'"
