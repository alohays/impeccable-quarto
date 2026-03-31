#!/usr/bin/env bash
# Render Quarto presentations.
# Usage: ./scripts/render.sh [file.qmd | --all]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
BOLD='\033[1m'
RESET='\033[0m'

usage() {
    echo "Usage: $0 [file.qmd | --all]"
    echo ""
    echo "  file.qmd    Render a specific .qmd file"
    echo "  --all       Render all .qmd files in examples/"
    echo ""
    echo "Examples:"
    echo "  $0 examples/academic-paper.qmd"
    echo "  $0 --all"
}

check_quarto() {
    if ! command -v quarto &>/dev/null; then
        echo -e "${RED}Error:${RESET} quarto is not installed."
        echo "Install from: https://quarto.org/docs/get-started/"
        exit 1
    fi
    echo -e "${GREEN}Quarto found:${RESET} $(quarto --version)"
}

render_file() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo -e "${RED}Error:${RESET} File not found: $file"
        return 1
    fi

    local name
    name="$(basename "$file")"
    echo -e "${BOLD}Rendering:${RESET} $name"

    local start_time
    start_time=$(date +%s)

    if quarto render "$file" 2>&1; then
        local end_time
        end_time=$(date +%s)
        local elapsed=$(( end_time - start_time ))
        echo -e "  ${GREEN}OK${RESET} ($name) in ${elapsed}s"
        return 0
    else
        echo -e "  ${RED}FAILED${RESET} ($name)"
        return 1
    fi
}

main() {
    check_quarto

    if [[ $# -eq 0 ]]; then
        usage
        exit 1
    fi

    local total=0
    local passed=0
    local failed=0
    local overall_start
    overall_start=$(date +%s)

    if [[ "$1" == "--all" ]]; then
        echo -e "${BOLD}Rendering all presentations...${RESET}"
        echo ""
        for qmd in "$PROJECT_DIR"/examples/*.qmd; do
            [[ -f "$qmd" ]] || continue
            total=$(( total + 1 ))
            if render_file "$qmd"; then
                passed=$(( passed + 1 ))
            else
                failed=$(( failed + 1 ))
            fi
            echo ""
        done
    else
        for file in "$@"; do
            total=$(( total + 1 ))
            # Resolve relative to project dir if not absolute
            if [[ ! "$file" = /* ]]; then
                file="$PROJECT_DIR/$file"
            fi
            if render_file "$file"; then
                passed=$(( passed + 1 ))
            else
                failed=$(( failed + 1 ))
            fi
            echo ""
        done
    fi

    local overall_end
    overall_end=$(date +%s)
    local overall_elapsed=$(( overall_end - overall_start ))

    echo "=============================="
    echo -e "${BOLD}Results:${RESET} $passed/$total passed, $failed failed (${overall_elapsed}s total)"

    if [[ $failed -gt 0 ]]; then
        exit 1
    fi
}

main "$@"
