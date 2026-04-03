#!/bin/bash
# Block accidental edits to protected files
# Exit 2 = block the tool call with error message
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
FILE=""

if [ "$TOOL" = "Edit" ] || [ "$TOOL" = "Write" ]; then
  FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
fi

if [ -z "$FILE" ]; then
  exit 0
fi

# Protected files for impeccable-quarto
PROTECTED_PATTERNS=(
  "themes/impeccable.scss"
  "settings.json"
)

for PATTERN in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE" == *"$PATTERN" ]]; then
    echo "Protected file: $(basename "$FILE"). Edit manually or remove protection in .claude/hooks/protect-files.sh" >&2
    exit 2
  fi
done

exit 0
