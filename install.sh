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

command -v tar >/dev/null 2>&1 || { echo "error: tar is required" >&2; exit 1; }
if command -v curl >/dev/null 2>&1; then
  FETCHER="curl"
elif command -v wget >/dev/null 2>&1; then
  FETCHER="wget"
else
  echo "error: curl or wget is required" >&2
  exit 1
fi

WORK="$(mktemp -d 2>/dev/null || mktemp -d -t sbpa)"
ARCHIVE="$WORK/sbpa.tar.gz"
EXTRACT="$WORK/extract"
STAGED="$WORK/staged"
BACKUP="${DEST}.backup.$$"

cleanup() {
  rm -rf "$WORK"
}
trap cleanup EXIT

URL="https://github.com/${REPO}/archive/${REF}.tar.gz"
if [ "$FETCHER" = "curl" ]; then
  curl -fsSL "$URL" -o "$ARCHIVE"
else
  wget -q "$URL" -O "$ARCHIVE"
fi

mkdir -p "$EXTRACT"
tar -xzf "$ARCHIVE" -C "$EXTRACT"

SOURCE="$(find "$EXTRACT" -type f -path '*/skills/sbpa/SKILL.md' -print -quit | sed 's#/SKILL.md$##')"
[ -n "$SOURCE" ] || { echo "error: skills/sbpa/SKILL.md not found in archive" >&2; exit 1; }

cp -R "$SOURCE" "$STAGED"

grep -q '^name: sbpa$' "$STAGED/SKILL.md" || { echo "error: invalid SBPA skill metadata" >&2; exit 1; }
grep -q '^# SBPA' "$STAGED/SKILL.md" || { echo "error: invalid SBPA skill payload" >&2; exit 1; }

mkdir -p "$(dirname "$DEST")"
if [ -e "$DEST" ]; then
  mv "$DEST" "$BACKUP"
fi

if mv "$STAGED" "$DEST"; then
  rm -rf "$BACKUP"
else
  [ ! -e "$BACKUP" ] || mv "$BACKUP" "$DEST"
  echo "error: installation failed; previous installation restored" >&2
  exit 1
fi

trap - EXIT
rm -rf "$WORK"

echo "SBPA installed: $DEST"
echo "Use: ask your agent to 'Use SBPA to audit this repository.'"
