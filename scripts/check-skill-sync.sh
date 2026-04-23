#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

BASE_FILE=".codex/skills/find-skills/SKILL.md"
FILES="
.claude/skills/find-skills/SKILL.md
.cursor/skills/find-skills/SKILL.md
.gemini/skills/find-skills/SKILL.md
"

tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT

normalize() {
  sed \
    -e 's/Use in Codex/Use in <HOST>/g' \
    -e 's/Use in Claude Code/Use in <HOST>/g' \
    -e 's/Use in Cursor/Use in <HOST>/g' \
    -e 's/Use in Gemini CLI/Use in <HOST>/g' \
    -e 's/# Find Skills For Codex/# Find Skills For <HOST>/g' \
    -e 's/# Find Skills For Claude Code/# Find Skills For <HOST>/g' \
    -e 's/# Find Skills For Cursor/# Find Skills For <HOST>/g' \
    -e 's/# Find Skills For Gemini CLI/# Find Skills For <HOST>/g' \
    -e 's/Use this Codex skill/Use this <HOST> skill/g' \
    -e 's/Use this Claude Code skill/Use this <HOST> skill/g' \
    -e 's/Use this Cursor skill/Use this <HOST> skill/g' \
    -e 's/Use this Gemini CLI skill/Use this <HOST> skill/g' \
    -e 's/relevant Codex skills/relevant project skills/g' \
    -e 's/use Codex skills/use project skills/g' \
    -e 's/## Codex Workflow/## <HOST> Workflow/g' \
    -e 's/## Claude Code Workflow/## <HOST> Workflow/g' \
    -e 's/## Cursor Workflow/## <HOST> Workflow/g' \
    -e 's/## Gemini CLI Workflow/## <HOST> Workflow/g' \
    -e 's/Search Codex skill metadata first\./Search <HOST> skill metadata first./g' \
    -e 's/Search available skill metadata first\./Search <HOST> skill metadata first./g' \
    -e 's#\.codex/skills/find-skills#.<HOST_DIR>/skills/find-skills#g' \
    -e 's#\.claude/skills/find-skills#.<HOST_DIR>/skills/find-skills#g' \
    -e 's#\.cursor/skills/find-skills#.<HOST_DIR>/skills/find-skills#g' \
    -e 's#\.gemini/skills/find-skills#.<HOST_DIR>/skills/find-skills#g' \
    -e 's#\.codex/skills/#.<HOST_DIR>/skills/#g' \
    -e 's#\.claude/skills/#.<HOST_DIR>/skills/#g' \
    -e 's#\.cursor/skills/#.<HOST_DIR>/skills/#g' \
    -e 's#\.gemini/skills/#.<HOST_DIR>/skills/#g' \
    -e 's#~/\.codex/skills#~/.<HOST_DIR>/skills#g' \
    -e 's#~/\.claude/skills#~/.<HOST_DIR>/skills#g' \
    -e 's#~/\.cursor/skills#~/.<HOST_DIR>/skills#g' \
    -e 's#~/\.gemini/skills#~/.<HOST_DIR>/skills#g' \
    -e 's#<project-root>/\.codex/skills#<project-root>/.<HOST_DIR>/skills#g' \
    -e 's#<project-root>/\.claude/skills#<project-root>/.<HOST_DIR>/skills#g' \
    -e 's#<project-root>/\.cursor/skills#<project-root>/.<HOST_DIR>/skills#g' \
    -e 's#<project-root>/\.gemini/skills#<project-root>/.<HOST_DIR>/skills#g' \
    "$1"
}

cd "$ROOT_DIR"

if [ ! -f "$BASE_FILE" ]; then
  echo "Missing baseline skill file: $BASE_FILE" >&2
  exit 1
fi

normalize "$BASE_FILE" > "$tmp_dir/base.md"

failed=0

for file in $FILES; do
  if [ ! -f "$file" ]; then
    echo "Missing host skill file: $file" >&2
    failed=1
    continue
  fi

  normalized="$tmp_dir/$(printf '%s' "$file" | tr '/.' '__').md"
  normalize "$file" > "$normalized"

  if ! diff -u "$tmp_dir/base.md" "$normalized"; then
    echo "Drift detected in $file" >&2
    failed=1
  fi
done

if [ "$failed" -ne 0 ]; then
  echo "Host-specific SKILL.md files have drifted. Keep only host labels and install paths different." >&2
  exit 1
fi

echo "Host-specific SKILL.md files are aligned."
