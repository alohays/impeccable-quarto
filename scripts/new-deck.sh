#!/usr/bin/env bash
# Scaffold a new Quarto presentation from a template.
# Usage: ./scripts/new-deck.sh [output-path]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[96m'
BOLD='\033[1m'
RESET='\033[0m'

prompt() {
    local var_name="$1"
    local message="$2"
    local default="${3:-}"

    if [[ -n "$default" ]]; then
        echo -en "${CYAN}$message${RESET} [$default]: "
    else
        echo -en "${CYAN}$message${RESET}: "
    fi
    read -r value
    value="${value:-$default}"
    eval "$var_name='$value'"
}

select_template() {
    echo ""
    echo -e "${BOLD}Select a template:${RESET}"
    echo "  1) Academic    — Paper presentation with citations, methodology boxes"
    echo "  2) Corporate   — Product/business deck with clean corporate style"
    echo "  3) Creative    — Tech talk / developer presentation with code focus"
    echo "  4) Lightning   — Short lightning talk (5 min)"
    echo "  5) Blank       — Minimal starter with just a title slide"
    echo ""
    prompt TEMPLATE_CHOICE "Template" "1"

    case "$TEMPLATE_CHOICE" in
        1|academic)   TEMPLATE="academic" ; THEME="impeccable-academic" ;;
        2|corporate)  TEMPLATE="corporate" ; THEME="impeccable-corporate" ;;
        3|creative)   TEMPLATE="creative" ; THEME="impeccable-creative" ;;
        4|lightning)  TEMPLATE="lightning" ; THEME="impeccable-lightning" ;;
        5|blank)      TEMPLATE="blank" ; THEME="impeccable" ;;
        *)
            echo -e "${RED}Invalid choice.${RESET}"
            exit 1
            ;;
    esac
}

gather_info() {
    echo ""
    echo -e "${BOLD}Presentation details:${RESET}"
    prompt TITLE "Title" "My Presentation"
    prompt SUBTITLE "Subtitle (optional)" ""
    prompt AUTHOR "Author" "$(git config user.name 2>/dev/null || echo 'Author')"
    prompt DATE "Date" "$(date +%Y-%m-%d)"
}

compute_theme_path() {
    local output="$1"
    local output_dir
    output_dir="$(dirname "$output")"

    # Compute relative path from output directory to themes/
    local rel
    rel="$(python3 -c "import os.path; print(os.path.relpath('$PROJECT_DIR/themes', '$output_dir'))" 2>/dev/null || echo "themes")"
    THEME_PATH="$rel/${THEME}.scss"
}

write_template() {
    local output="$1"

    local subtitle_line=""
    if [[ -n "$SUBTITLE" ]]; then
        subtitle_line="subtitle: \"$SUBTITLE\""
    fi

    cat > "$output" << EOF
---
title: "$TITLE"
${subtitle_line}
author: "$AUTHOR"
date: "$DATE"
format:
  revealjs:
    theme: [default, $THEME_PATH]
    slide-number: true
    hash: true
    transition: fade
    transition-speed: fast
    width: 1920
    height: 1080
    margin: 0.05
    code-line-numbers: false
    highlight-style: github-dark
    fig-align: center
---

EOF

    case "$TEMPLATE" in
        academic)
            cat >> "$output" << 'EOF'
## Outline

1. Motivation
2. Related Work
3. Methodology
4. Results
5. Conclusion

::: {.notes}
Speaker notes go here.
:::

---

## Motivation

::: {.keybox}
**Key Question:** What problem are you solving?
:::

::: {.notes}
Explain the motivation for your research.
:::

---

## Methodology

::: {.methodbox}
Describe your approach here.
:::

::: {.notes}
Walk through the methodology step by step.
:::

---

## Results

| Metric | Baseline | Ours |
|:---|:---:|:---:|
| Accuracy | 80.0 | **85.0** |

::: {.notes}
Present your key results.
:::

---

## Discussion

::: {.warningbox}
**Limitations:** List known limitations here.
:::

::: {.notes}
Discuss strengths, limitations, and future work.
:::

---

## Conclusion

::: {.tipbox}
Summarize key contributions.
:::

::: {.notes}
Wrap up with a concise summary.
:::
EOF
            ;;
        corporate)
            cat >> "$output" << 'EOF'
## The Problem

::: {.keybox}
**Key Statistic:** XX% of teams face this challenge.
:::

::: {.notes}
Set the stage with a compelling problem statement.
:::

---

## Our Solution

:::: {.three-col}
::: {.column}
### Feature 1
Description here.
:::

::: {.column}
### Feature 2
Description here.
:::

::: {.column}
### Feature 3
Description here.
:::
::::

::: {.notes}
Overview of your solution's core features.
:::

---

## Customer Story

::: {.quotebox}
"Quote from a happy customer."

— **Name, Title** at Company
:::

::: {.notes}
Social proof strengthens your pitch.
:::

---

## Get Started

::: {.tipbox}
Call to action goes here.
:::

::: {.notes}
Close with a clear next step.
:::
EOF
            ;;
        creative)
            cat >> "$output" << 'EOF'
## Why This Matters

::: {.keybox}
What makes this talk worth your time?
:::

::: {.notes}
Hook the audience in the first 30 seconds.
:::

---

## Code Example

```python
def example():
    """Your code here."""
    return "Hello, World!"
```

::: {.notes}
Walk through the code step by step.
:::

---

## Architecture

```{mermaid}
flowchart LR
    A[Input] --> B[Process] --> C[Output]
```

::: {.notes}
Explain the system design.
:::

---

## Gotchas

::: {.warningbox}
Watch out for these common mistakes.
:::

::: {.notes}
Share hard-won lessons.
:::

---

## Best Practices

::: {.tipbox}
Summarize actionable takeaways.
:::

::: {.notes}
End with clear, practical advice.
:::
EOF
            ;;
        lightning)
            cat >> "$output" << 'EOF'
## The Problem (30s)

::: {.keybox}
One sentence problem statement.
:::

::: {.notes}
Get to the point immediately.
:::

---

## The Solution (2min)

:::: {.two-col}
::: {.column}
### Before
The old way.
:::

::: {.column}
### After
The new way.
:::
::::

::: {.notes}
Show the contrast clearly.
:::

---

## Demo (1.5min)

::: {.notes}
Live demo or key screenshots.
:::

---

## Try It (30s)

::: {.tipbox}
Link or command to get started.
:::

::: {.notes}
One clear call to action.
:::
EOF
            ;;
        blank)
            cat >> "$output" << 'EOF'
## First Slide

Content goes here.

::: {.notes}
Speaker notes go here.
:::
EOF
            ;;
    esac
}

main() {
    echo -e "${BOLD}New Presentation Scaffolding${RESET}"

    local output="${1:-}"

    if [[ -z "$output" ]]; then
        prompt output "Output path" "examples/new-deck.qmd"
    fi

    # Resolve relative paths
    if [[ ! "$output" = /* ]]; then
        output="$PROJECT_DIR/$output"
    fi

    # Ensure .qmd extension
    if [[ "$output" != *.qmd ]]; then
        output="${output}.qmd"
    fi

    if [[ -f "$output" ]]; then
        echo -e "${YELLOW}File already exists:${RESET} $output"
        prompt OVERWRITE "Overwrite? (y/N)" "N"
        if [[ ! "$OVERWRITE" =~ ^[yY] ]]; then
            echo "Cancelled."
            exit 0
        fi
    fi

    select_template
    gather_info
    compute_theme_path "$output"

    mkdir -p "$(dirname "$output")"
    write_template "$output"

    echo ""
    echo -e "${GREEN}${BOLD}Created:${RESET} $output"
    echo -e "  Template: $TEMPLATE"
    echo -e "  Theme:    $THEME"
    echo ""
    echo "Next steps:"
    echo "  1. Edit $output"
    echo "  2. Preview: quarto preview $output"
    echo "  3. Score:   python scripts/quality_score.py $output"
}

main "$@"
