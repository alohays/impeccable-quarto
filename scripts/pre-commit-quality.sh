#!/bin/bash
# Pre-commit quality gate for impeccable-quarto
# Runs quality_score.py on staged .qmd files
# Blocks commit if any file scores below 80
#
# Installation:
#   ln -sf ../../scripts/pre-commit-quality.sh .git/hooks/pre-commit
#   chmod +x scripts/pre-commit-quality.sh
#
# Override (emergency):
#   git commit --no-verify -m "message"

set -euo pipefail

RED="\033[91m"
GREEN="\033[92m"
YELLOW="\033[93m"
BOLD="\033[1m"
RESET="\033[0m"

THRESHOLD=80
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "$SCRIPT_DIR/..")"
QUALITY_SCRIPT="$PROJECT_ROOT/scripts/quality_score.py"

# Check if quality_score.py exists
if [ ! -f "$QUALITY_SCRIPT" ]; then
  echo -e "${YELLOW}Warning:${RESET} quality_score.py not found at $QUALITY_SCRIPT"
  echo "Skipping quality gate check."
  exit 0
fi

# Check whether any .qmd files are staged
if ! git diff --cached --name-only --diff-filter=ACM | grep -q '\.qmd$'; then
  # No .qmd files staged — nothing to check
  exit 0
fi

echo -e "${BOLD}Pre-commit quality gate${RESET} (threshold: ${THRESHOLD}/100)"
echo "========================================"

FAILED=0
while IFS= read -r -d '' FILE; do
  if [ ! -f "$FILE" ]; then
    continue
  fi

  # Run quality_score.py and capture exit code
  OUTPUT=$(python3 "$QUALITY_SCRIPT" "$FILE" 2>&1) || true

  # Strip ANSI color codes before extracting "Score: XX/100"
  CLEAN_OUTPUT=$(printf '%s\n' "$OUTPUT" | sed -E $'s/\x1B\\[[0-9;]*[[:alpha:]]//g')
  SCORE=$(printf '%s\n' "$CLEAN_OUTPUT" | sed -n 's/.*Score:[^0-9]*\([0-9][0-9]*\)\/100.*/\1/p' | head -1)

  if [ -z "$SCORE" ]; then
    echo -e "${RED}FAIL${RESET} $FILE — could not parse score output"
    echo "$OUTPUT"
    FAILED=1
    continue
  fi

  if [ "$SCORE" -lt "$THRESHOLD" ]; then
    echo -e "${RED}FAIL${RESET} $FILE — score ${SCORE}/100 (need ${THRESHOLD}+)"
    FAILED=1
  else
    echo -e "${GREEN}PASS${RESET} $FILE — score ${SCORE}/100"
  fi
done < <(git diff --cached --name-only --diff-filter=ACM -z -- '*.qmd')

echo "========================================"

if [ "$FAILED" -eq 1 ]; then
  echo ""
  echo -e "${RED}${BOLD}Commit blocked:${RESET} One or more .qmd files scored below ${THRESHOLD}/100."
  echo -e "Fix issues and re-stage, or override with: ${YELLOW}git commit --no-verify${RESET}"
  exit 1
fi

echo -e "${GREEN}All staged .qmd files pass quality gate.${RESET}"
exit 0
