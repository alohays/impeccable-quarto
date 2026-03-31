#!/usr/bin/env bash
# Generate preview renders for each theme variant and open in browser.
# Usage: ./scripts/theme-preview.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PREVIEW_DIR="$PROJECT_DIR/_preview"

RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
BOLD='\033[1m'
RESET='\033[0m'

SAMPLE_QMD="$PREVIEW_DIR/_sample.qmd"

check_quarto() {
    if ! command -v quarto &>/dev/null; then
        echo -e "${RED}Error:${RESET} quarto is not installed."
        exit 1
    fi
}

create_sample() {
    mkdir -p "$PREVIEW_DIR"
    cat > "$SAMPLE_QMD" << 'EOF'
---
title: "Theme Preview"
subtitle: "impeccable-quarto design system"
author: "Theme Tester"
date: today
format:
  revealjs:
    slide-number: true
    transition: fade
    width: 1920
    height: 1080
---

## Section Title

::: {.keybox}
**Key Point:** This is a keybox demonstrating the gold accent border styling.
:::

## Two Column Layout

:::: {.two-col}
::: {.column}
### Left Column
- First bullet point
- Second with [emphasis]{.hi}
- Third with [gold highlight]{.hi-gold}
:::

::: {.column}
### Right Column

::: {.methodbox}
A method box with blue border styling.
:::
:::
::::

## Semantic Boxes

::: {.warningbox}
**Warning:** This is a warning box with red styling.
:::

::: {.tipbox}
**Tip:** This is a tip box with green styling.
:::

::: {.quotebox}
"This is a quotebox with italic styling for testimonials and citations."
:::

## Code Block

```python
def hello(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"
```

## Three Columns

:::: {.three-col}
::: {.column}
### Feature A
Description of the first feature.
:::

::: {.column}
### Feature B
Description of the second feature.
:::

::: {.column}
### Feature C
Description of the third feature.
:::
::::
EOF
}

render_themes() {
    local themes_found=0

    for scss in "$PROJECT_DIR"/themes/impeccable*.scss; do
        [[ -f "$scss" ]] || continue
        themes_found=$(( themes_found + 1 ))

        local theme_name
        theme_name="$(basename "$scss" .scss)"
        local output_name="${theme_name}.html"
        local output_path="$PREVIEW_DIR/$output_name"

        echo -e "${BOLD}Rendering:${RESET} $theme_name"

        # Create a temporary .qmd with this theme
        local tmp_qmd="$PREVIEW_DIR/_tmp_${theme_name}.qmd"
        sed "s|^format:.*|format:|;s|revealjs:.*|  revealjs:|" "$SAMPLE_QMD" > "$tmp_qmd"

        # Use quarto render with theme override
        if quarto render "$tmp_qmd" \
            --to revealjs \
            -M "theme:[default,$scss]" \
            --output "$output_name" \
            2>&1; then
            echo -e "  ${GREEN}OK${RESET} -> $output_name"
        else
            echo -e "  ${RED}FAILED${RESET} $theme_name"
        fi

        rm -f "$tmp_qmd"
    done

    if [[ $themes_found -eq 0 ]]; then
        echo -e "${YELLOW}No theme files found in themes/ directory.${RESET}"
        exit 1
    fi
}

create_comparison_page() {
    local index="$PREVIEW_DIR/index.html"
    cat > "$index" << 'HEADER'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Theme Preview — impeccable-quarto</title>
<style>
  body { font-family: system-ui, sans-serif; background: #111; color: #eee; padding: 2rem; }
  h1 { margin-bottom: 1rem; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; }
  .card { background: #222; border-radius: 8px; overflow: hidden; }
  .card h2 { padding: 0.75rem 1rem; margin: 0; font-size: 1rem; background: #333; }
  .card iframe { width: 100%; height: 300px; border: none; }
  .card a { display: block; padding: 0.5rem 1rem; color: #60a5fa; text-decoration: none; font-size: 0.85rem; }
</style>
</head>
<body>
<h1>Theme Preview</h1>
<p>Side-by-side comparison of all impeccable-quarto themes.</p>
<div class="grid">
HEADER

    for html in "$PREVIEW_DIR"/impeccable*.html; do
        [[ -f "$html" ]] || continue
        local name
        name="$(basename "$html" .html)"
        cat >> "$index" << EOF
<div class="card">
  <h2>$name</h2>
  <iframe src="$(basename "$html")"></iframe>
  <a href="$(basename "$html")" target="_blank">Open full size</a>
</div>
EOF
    done

    cat >> "$index" << 'FOOTER'
</div>
</body>
</html>
FOOTER
}

open_browser() {
    local url="$PREVIEW_DIR/index.html"
    echo ""
    echo -e "${GREEN}${BOLD}Preview ready!${RESET}"
    echo "Opening: $url"

    if command -v open &>/dev/null; then
        open "$url"
    elif command -v xdg-open &>/dev/null; then
        xdg-open "$url"
    else
        echo "Open $url in your browser."
    fi
}

main() {
    check_quarto
    echo -e "${BOLD}Generating theme previews...${RESET}"
    echo ""
    create_sample
    render_themes
    create_comparison_page
    open_browser
}

main
