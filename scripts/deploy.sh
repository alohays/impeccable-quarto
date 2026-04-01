#!/usr/bin/env bash
# Deploy presentations to GitHub Pages via docs/ directory.
# Usage: ./scripts/deploy.sh [--push]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DOCS_DIR="$PROJECT_DIR/docs"

RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
BOLD='\033[1m'
RESET='\033[0m'

DO_PUSH=false
if [[ "${1:-}" == "--push" ]]; then
    DO_PUSH=true
fi

check_quarto() {
    if ! command -v quarto &>/dev/null; then
        echo -e "${RED}Error:${RESET} quarto is not installed."
        exit 1
    fi
}

render_all() {
    echo -e "${BOLD}Step 1: Rendering all presentations...${RESET}"
    "$SCRIPT_DIR/render.sh" --all
}

copy_to_docs() {
    echo -e "${BOLD}Step 2: Copying output to docs/...${RESET}"

    # Preserve handcrafted landing page files
    local landing_files=("index.html" "style.css" "script.js")
    local tmp_dir
    tmp_dir="$(mktemp -d)"
    for f in "${landing_files[@]}"; do
        [[ -f "$DOCS_DIR/$f" ]] && cp "$DOCS_DIR/$f" "$tmp_dir/"
    done

    rm -rf "$DOCS_DIR"
    mkdir -p "$DOCS_DIR"

    # Restore landing page files
    for f in "${landing_files[@]}"; do
        [[ -f "$tmp_dir/$f" ]] && cp "$tmp_dir/$f" "$DOCS_DIR/"
    done
    rm -rf "$tmp_dir"

    local output_dir="$PROJECT_DIR/_output"
    if [[ ! -d "$output_dir" ]]; then
        output_dir="$PROJECT_DIR/_site"
    fi

    if [[ -d "$output_dir" ]]; then
        # Copy rendered presentations but don't overwrite the landing page
        for item in "$output_dir"/*; do
            local base
            base="$(basename "$item")"
            [[ "$base" == "index.html" ]] && continue
            cp -R "$item" "$DOCS_DIR/"
        done
    fi

    # Also copy any standalone HTML files from examples
    for html in "$PROJECT_DIR"/examples/*.html; do
        [[ -f "$html" ]] || continue
        cp "$html" "$DOCS_DIR/"
    done

    echo -e "  ${GREEN}OK${RESET} Copied to docs/"
}

create_index() {
    echo -e "${BOLD}Step 3: Creating index.html...${RESET}"

    local index="$DOCS_DIR/index.html"

    # Skip if a handcrafted landing page already exists
    if [[ -f "$index" ]] && grep -q 'impeccable-quarto.*Design Quality System' "$index" 2>/dev/null; then
        echo -e "  ${GREEN}OK${RESET} Handcrafted landing page detected, skipping auto-generation"
        return
    fi

    cat > "$index" << 'HEADER'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>impeccable-quarto — Example Presentations</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: system-ui, sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; padding: 3rem 1.5rem; }
  .container { max-width: 800px; margin: 0 auto; }
  h1 { font-size: 2rem; margin-bottom: 0.5rem; color: #f1f5f9; }
  .subtitle { color: #94a3b8; margin-bottom: 2.5rem; }
  .card { background: #1e293b; border: 1px solid #334155; border-radius: 0.75rem; padding: 1.5rem; margin-bottom: 1rem; transition: border-color 0.2s; }
  .card:hover { border-color: #60a5fa; }
  .card a { color: #93c5fd; text-decoration: none; font-size: 1.25rem; font-weight: 600; }
  .card a:hover { text-decoration: underline; }
  .card p { color: #94a3b8; margin-top: 0.5rem; font-size: 0.9rem; }
  .tag { display: inline-block; background: #334155; color: #cbd5e1; padding: 0.15rem 0.5rem; border-radius: 0.25rem; font-size: 0.75rem; margin-right: 0.25rem; }
  footer { margin-top: 3rem; color: #475569; font-size: 0.85rem; text-align: center; }
</style>
</head>
<body>
<div class="container">
<h1>impeccable-quarto</h1>
<p class="subtitle">Example presentations showcasing the design quality system</p>
HEADER

    # List all HTML files (except index.html)
    for html in "$DOCS_DIR"/*.html; do
        [[ -f "$html" ]] || continue
        local name
        name="$(basename "$html")"
        [[ "$name" == "index.html" ]] && continue

        local title
        title="${name%.html}"
        title="${title//-/ }"

        # Determine theme tag from filename
        local tag="presentation"
        case "$name" in
            *academic*) tag="academic" ;;
            *product*|*launch*|*corporate*) tag="corporate" ;;
            *tech*|*creative*) tag="creative" ;;
        esac

        cat >> "$index" << EOF
<div class="card">
  <a href="$name">$title</a>
  <p><span class="tag">$tag</span> <span class="tag">revealjs</span></p>
</div>
EOF
    done

    cat >> "$index" << 'FOOTER'
<footer>
  <p>Built with <a href="https://quarto.org" style="color:#60a5fa">Quarto</a> + impeccable-quarto themes</p>
</footer>
</div>
</body>
</html>
FOOTER

    echo -e "  ${GREEN}OK${RESET} Created index.html"
}

push_to_remote() {
    if ! $DO_PUSH; then
        echo -e "${YELLOW}Skipping push.${RESET} Use --push to commit and push."
        return
    fi

    echo -e "${BOLD}Step 4: Committing and pushing...${RESET}"
    cd "$PROJECT_DIR"
    git add docs/
    git commit -m "Deploy presentations to GitHub Pages" || echo "Nothing to commit"
    git push
    echo -e "  ${GREEN}OK${RESET} Pushed to remote"
}

main() {
    check_quarto
    render_all
    copy_to_docs
    create_index
    push_to_remote
    echo ""
    echo -e "${GREEN}${BOLD}Deploy complete!${RESET}"
    echo "Open docs/index.html to preview locally."
}

main
