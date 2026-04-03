#!/usr/bin/env bash
# One-command environment setup for impeccable-quarto development.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
BOLD='\033[1m'
RESET='\033[0m'

PASS="${GREEN}PASS${RESET}"
FAIL="${RED}FAIL${RESET}"
WARN="${YELLOW}WARN${RESET}"

errors=0

check_command() {
    local name="$1"
    local hint="$2"

    if command -v "$name" >/dev/null 2>&1; then
        return 0
    fi

    echo -e "  ${FAIL} ${name} not found. ${hint}"
    errors=$((errors + 1))
    return 1
}

echo -e "${BOLD}Checking prerequisites...${RESET}"

if check_command "quarto" "Install from https://quarto.org/docs/get-started/"; then
    echo -e "  ${PASS} Quarto $(quarto --version)"
fi

if check_command "python3" "Install Python 3.10 or newer."; then
    echo -e "  ${PASS} $(python3 --version)"
fi

if command -v fc-list >/dev/null 2>&1; then
    for font in "Plus Jakarta Sans" "Source Sans 3" "JetBrains Mono"; do
        if fc-list | grep -qi "$font"; then
            echo -e "  ${PASS} Font detected: ${font}"
        else
            echo -e "  ${WARN} Font missing locally: ${font} (fallbacks or web fonts may be used)"
        fi
    done
else
    echo -e "  ${WARN} fc-list not available; skipping local font detection"
fi

echo ""
echo -e "${BOLD}Preparing local directories...${RESET}"
mkdir -p "$PROJECT_DIR/quality_reports" "$PROJECT_DIR/quality_reports/plans"
mkdir -p "$PROJECT_DIR/_extensions/impeccable-quarto"
echo -e "  ${PASS} Local output directories ready"

if [[ -x "$PROJECT_DIR/scripts/sync-extension.sh" ]]; then
    echo ""
    echo -e "${BOLD}Syncing Quarto extension assets...${RESET}"
    "$PROJECT_DIR/scripts/sync-extension.sh"
    echo -e "  ${PASS} Extension assets synced"
fi

echo ""
echo -e "${BOLD}Running smoke checks...${RESET}"

if [[ -f "$PROJECT_DIR/examples/demo.qmd" ]] && command -v quarto >/dev/null 2>&1; then
    if quarto render "$PROJECT_DIR/examples/demo.qmd" --quiet >/dev/null 2>&1; then
        echo -e "  ${PASS} Rendered examples/demo.qmd"
    else
        echo -e "  ${FAIL} Smoke render failed for examples/demo.qmd"
        errors=$((errors + 1))
    fi
else
    echo -e "  ${WARN} Skipping smoke render; missing Quarto or examples/demo.qmd"
fi

if [[ -f "$PROJECT_DIR/scripts/quality_score.py" ]] && command -v python3 >/dev/null 2>&1; then
    if python3 "$PROJECT_DIR/scripts/quality_score.py" "$PROJECT_DIR/examples/demo.qmd" >/dev/null 2>&1; then
        echo -e "  ${PASS} Quality scorer executed against examples/demo.qmd"
    else
        echo -e "  ${WARN} Quality scorer returned a non-zero exit code for examples/demo.qmd"
    fi
fi

echo ""
if [[ "$errors" -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}Environment ready.${RESET}"
    echo "Next steps:"
    echo "  ./scripts/new-deck.sh talks/my-deck.qmd"
    echo "  quarto preview talks/my-deck.qmd"
    echo "  python3 scripts/quality_score.py talks/my-deck.qmd"
else
    echo -e "${RED}${BOLD}${errors} prerequisite or smoke check(s) failed.${RESET}"
    exit 1
fi
