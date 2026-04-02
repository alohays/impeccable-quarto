# Phase 5: Distribution & Developer Experience — Implementation Plan

**Date:** 2026-04-03
**Author:** distribution-planner
**Status:** Draft
**Dependencies:** Phase 1 (SSOT fix, quality_score.py improvements) should be complete before items here reference canonical paths.

---

## Overview

Phase 5 closes the gap between impeccable-quarto's strong design system and its ability to reach users. Currently the project has no plugin packaging, no Quarto extension format, no contributor guide, and a minimal demo site. This phase addresses all four.

---

## Work Item 1: Claude Code Plugin Packaging

### Goal
Make impeccable-quarto's 18 skills discoverable and installable as a Claude Code plugin, following the `.claude-plugin/` format established by impeccable-original.

### Files to Create

#### `.claude-plugin/plugin.json`
```json
{
  "name": "impeccable-quarto",
  "description": "Design quality system for Quarto RevealJS presentations. 18 skills for creating, reviewing, and perfecting slide decks with OKLCH colors, typography-first design, and objective scoring.",
  "version": "0.1.0",
  "author": {
    "name": "impeccable-quarto contributors"
  },
  "homepage": "https://alohays.github.io/impeccable-quarto/",
  "repository": "https://github.com/alohays/impeccable-quarto",
  "skills": "./.claude/skills"
}
```

**Key decisions:**
- `skills` points to `.claude/skills/` (the 18 working skill files)
- Version starts at `0.1.0` (pre-1.0 since plugin format is emerging)
- `homepage` points to existing GitHub Pages site
- No `license` field yet — add when project license is formalized

#### `.claude-plugin/marketplace.json`
```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "impeccable-quarto",
  "metadata": {
    "description": "Design quality system for Quarto RevealJS slides. 18 skills including /create-deck, /review-slides, /critique-slides, /qa-loop, and domain-specific design commands."
  },
  "owner": {
    "name": "impeccable-quarto contributors"
  },
  "plugins": [
    {
      "name": "impeccable-quarto",
      "description": "18 skills for creating, reviewing, and perfecting Quarto RevealJS presentations. Includes OKLCH theming, typography-first design, adversarial review, and 100-point quality scoring.",
      "version": "0.1.0",
      "author": {
        "name": "impeccable-quarto contributors"
      },
      "source": "./",
      "category": "design",
      "homepage": "https://alohays.github.io/impeccable-quarto/",
      "tags": ["design", "presentations", "quarto", "revealjs", "slides", "quality", "oklch"]
    }
  ]
}
```

**Skill discovery metadata:** The `marketplace.json` includes tags that map to the project's core differentiators (quarto, oklch, quality). The `description` lists key slash commands so users can assess fit before installing.

### Files to Modify

#### `.gitignore`
Add nothing — `.claude-plugin/` should be tracked in git (it's the distribution artifact).

### Content Structure
- `plugin.json`: identity + pointer to skills directory
- `marketplace.json`: marketplace listing metadata (schema, tags, category, descriptions)

### Dependencies
- None on earlier phases. The 18 skills in `.claude/skills/` already exist.
- If Phase 1 moves skills to `source/skills/` as canonical, the `skills` path in `plugin.json` may need updating. However, `.claude/skills/` is what Claude Code reads at runtime, so it should remain the pointer target regardless of SSOT changes.

### Complexity: **S** (Small)
Two JSON files with well-defined structure from the impeccable-original reference.

### Acceptance Criteria
1. `.claude-plugin/plugin.json` exists and is valid JSON
2. `.claude-plugin/marketplace.json` exists, references the correct schema URL, and is valid JSON
3. `skills` path in `plugin.json` resolves to the directory containing all 18 skill files
4. Version fields are consistent across both files
5. Tags include at minimum: `design`, `quarto`, `presentations`, `slides`
6. Both files follow the exact structure from impeccable-original (field names, nesting)

---

## Work Item 2: Quarto Extension Format

### Goal
Package the impeccable theme as a proper [Quarto extension](https://quarto.org/docs/extensions/) so users can install it with `quarto add`. This is the native distribution mechanism for Quarto themes and enables one-command adoption.

### Files to Create

#### `_extensions/impeccable-quarto/_extension.yml`
```yaml
title: impeccable-quarto
author: impeccable-quarto contributors
version: 0.1.0
quarto-required: ">=1.4.0"
contributes:
  formats:
    revealjs:
      theme: [default, impeccable.scss]
      slide-number: true
      transition: none
      width: 1920
      height: 1080
      center: false
```

**Key decisions:**
- `contributes.formats.revealjs` sets the default RevealJS options from the project's YAML frontmatter template
- The theme file is referenced as `impeccable.scss` (relative to the extension directory)
- `quarto-required: ">=1.4.0"` — extensions API stabilized in 1.4
- Only the master theme (`impeccable.scss`) is included in the base extension. Variant themes (academic, corporate, creative, lightning) can be separate extensions or installed manually.

#### `_extensions/impeccable-quarto/impeccable.scss`
This is a **copy** (or symlink) of `themes/impeccable.scss`. The Quarto extension format requires theme files to be inside the extension directory.

**Build consideration:** To avoid SSOT violation (two copies of the same SCSS), create a sync mechanism:
- Option A: `scripts/sync-extension.sh` copies `themes/impeccable.scss` → `_extensions/impeccable-quarto/impeccable.scss`
- Option B: A symlink (`_extensions/impeccable-quarto/impeccable.scss` → `../../themes/impeccable.scss`)
- **Recommended: Option A** (symlinks can break on Windows and in ZIP distributions)

#### `scripts/sync-extension.sh`
```bash
#!/usr/bin/env bash
# Sync theme SCSS into Quarto extension directory
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

EXT_DIR="$PROJECT_DIR/_extensions/impeccable-quarto"
mkdir -p "$EXT_DIR"

cp "$PROJECT_DIR/themes/impeccable.scss" "$EXT_DIR/impeccable.scss"
echo "Synced impeccable.scss → _extensions/impeccable-quarto/"
```

### Files to Modify

#### `README.md`
Add an "Installation" section with:
```markdown
## Installation

### As a Quarto Extension (recommended)
```bash
quarto add alohays/impeccable-quarto
```

Then in your `.qmd` frontmatter:
```yaml
format:
  impeccable-quarto-revealjs:
    slide-number: true
```

### Manual
Copy `themes/impeccable.scss` to your project and reference it in frontmatter.
```

### Directory Structure
```
_extensions/
  impeccable-quarto/
    _extension.yml          # Extension metadata + default format options
    impeccable.scss         # Master theme (synced from themes/)
```

### User Experience After Installation
Users who run `quarto add alohays/impeccable-quarto` get:
1. `_extensions/impeccable-quarto/` added to their project
2. They can use `format: impeccable-quarto-revealjs` in frontmatter
3. All design system defaults (OKLCH colors, typography stack, 1920×1080, semantic boxes) are applied automatically

### Variant Themes (Future)
The four variant themes (`impeccable-academic.scss`, etc.) could be:
- Bundled in the same extension with a frontmatter option to select variant
- Distributed as separate extensions (`quarto add alohays/impeccable-quarto-academic`)
- **Recommended for v0.1.0:** Include only the master theme. Add variants in v0.2.0.

### Dependencies
- `themes/impeccable.scss` must exist and be stable (no dependency on earlier phases)
- If Phase 4 (Theme Enhancement) adds CSS custom properties or two-layer tokens, the extension SCSS will pick them up via sync

### Complexity: **M** (Medium)
Requires understanding Quarto's extension specification, creating the YAML config, and setting up the sync mechanism. Testing requires a clean project to verify `quarto add` works.

### Acceptance Criteria
1. `_extensions/impeccable-quarto/_extension.yml` exists with valid YAML
2. `_extensions/impeccable-quarto/impeccable.scss` exists and matches `themes/impeccable.scss`
3. `scripts/sync-extension.sh` copies the theme correctly
4. A test `.qmd` file using `format: impeccable-quarto-revealjs` renders successfully with `quarto render`
5. All semantic box classes (`.keybox`, `.methodbox`, etc.) work in the extension context
6. Layout classes (`.two-col`, `.three-col`, etc.) work in the extension context
7. Typography stack loads correctly (Plus Jakarta Sans, Source Sans 3, JetBrains Mono)
8. Slide dimensions default to 1920×1080

---

## Work Item 3: DEVELOP.md + Setup Script

### Goal
Create a contributor guide and one-command setup script so new developers can get productive quickly. Modeled on impeccable-original's DEVELOP.md but adapted for impeccable-quarto's Quarto + Python stack.

### Files to Create

#### `DEVELOP.md`

**Content Structure:**

```markdown
# Developer Guide

## Architecture Overview
- source/ vs .claude/ distinction (SSOT principle)
- themes/ — SCSS theme files
- templates/ — starter .qmd files
- scripts/ — build, render, utility scripts
- examples/ — complete example presentations
- _extensions/ — Quarto extension packaging

## Prerequisites
- Quarto >= 1.4.0
- Python >= 3.10
- Fonts: Plus Jakarta Sans, Source Sans 3, JetBrains Mono
- (Optional) Bun or Node.js for future multi-tool builds

## Quick Start
1. Clone the repository
2. Run `./scripts/setup.sh`
3. Create a deck: `./scripts/new-deck.sh my-deck.qmd`
4. Preview: `quarto preview my-deck.qmd`
5. Score: `python scripts/quality_score.py my-deck.qmd`

## Adding a Theme Variant
1. Copy `themes/impeccable.scss` to `themes/impeccable-{variant}.scss`
2. Override SCSS variables (colors, fonts, spacing)
3. Add a matching template in `templates/{variant}.qmd`
4. Run `scripts/sync-extension.sh` if variant should be in the extension
5. Add an example in `examples/` that uses the variant
6. Render and verify: `quarto render examples/{variant}-example.qmd`

## Adding a Template
1. Create `templates/{name}.qmd` with YAML frontmatter
2. Include all required frontmatter fields (title, author, date, format)
3. Reference the appropriate theme
4. Add at least 3 slides demonstrating the template's purpose
5. Update `scripts/new-deck.sh` to include the new template option

## Modifying Quality Scoring
- Scoring rubric: `.claude/rules/quality-gates.md`
- Scoring script: `scripts/quality_score.py`
- Add new checks as functions, register in the check list
- Every check must map to a deduction ID (CRIT-xx, MAJ-xx, MIN-xx)
- Update the rubric document when adding new checks

## Adding Skills
1. Create `source/skills/{name}/SKILL.md` with frontmatter
2. Run sync script to copy to `.claude/skills/{name}.md`
3. If user-invocable, add to the skill list in CLAUDE.md
4. Update `.claude-plugin/plugin.json` description with new count

## Agent Development
- Agent definitions: `.claude/agents/`
- Diagnostic agents (read-only): slide-critic, layout-auditor, typography-reviewer
- Fix agents (edit): slide-fixer
- Verification: verifier
- Creative: content-translator, theme-designer
- See `.claude/rules/orchestrator-protocol.md` for coordination rules

## Scripts Reference
| Script | Purpose |
|--------|---------|
| `scripts/setup.sh` | One-command environment setup |
| `scripts/new-deck.sh` | Interactive deck scaffolding |
| `scripts/render.sh` | Render with timing/color output |
| `scripts/deploy.sh` | Build + deploy to GitHub Pages |
| `scripts/quality_score.py` | 100-point quality scoring |
| `scripts/theme-preview.sh` | Side-by-side theme comparison |
| `scripts/sync-extension.sh` | Sync theme to _extensions/ |

## Troubleshooting

### Quarto render fails
- Check Quarto version: `quarto --version` (need >= 1.4.0)
- Verify YAML frontmatter syntax
- Check theme path in frontmatter resolves

### Fonts don't render correctly
- Install fonts locally or verify Google Fonts CDN access
- Check browser dev tools for font loading errors
- Fallback fonts are defined in the theme

### Quality score seems wrong
- Run with `--verbose` flag for per-check breakdown
- Check if the rubric and script thresholds match
- Verify you're scoring the .qmd source, not rendered HTML

### Extension doesn't work after `quarto add`
- Run `scripts/sync-extension.sh` to ensure SCSS is current
- Check `_extension.yml` format key matches your frontmatter
- Verify Quarto version supports extensions (>= 1.4.0)
```

#### `scripts/setup.sh`

**Content Structure:**

```bash
#!/usr/bin/env bash
# One-command environment setup for impeccable-quarto
# Usage: ./scripts/setup.sh

set -euo pipefail

# --- Color output ---
RED='\033[91m'; GREEN='\033[92m'; YELLOW='\033[93m'
BOLD='\033[1m'; RESET='\033[0m'

PASS="${GREEN}✓${RESET}"
FAIL="${RED}✗${RESET}"
WARN="${YELLOW}!${RESET}"

errors=0

# --- 1. Check Quarto ---
echo -e "${BOLD}Checking prerequisites...${RESET}"
if command -v quarto &>/dev/null; then
    version=$(quarto --version)
    echo -e "  ${PASS} Quarto ${version}"
else
    echo -e "  ${FAIL} Quarto not found. Install from https://quarto.org/docs/get-started/"
    ((errors++))
fi

# --- 2. Check Python ---
if command -v python3 &>/dev/null; then
    py_version=$(python3 --version | awk '{print $2}')
    echo -e "  ${PASS} Python ${py_version}"
else
    echo -e "  ${FAIL} Python 3 not found."
    ((errors++))
fi

# --- 3. Check fonts (macOS: fc-list, fallback: skip) ---
if command -v fc-list &>/dev/null; then
    for font in "Plus Jakarta Sans" "Source Sans 3" "JetBrains Mono"; do
        if fc-list | grep -qi "$font"; then
            echo -e "  ${PASS} Font: ${font}"
        else
            echo -e "  ${WARN} Font not found locally: ${font} (will use Google Fonts CDN)"
        fi
    done
else
    echo -e "  ${WARN} fc-list not available — skipping font check"
fi

# --- 4. Create necessary directories ---
mkdir -p quality_reports/plans
mkdir -p _extensions/impeccable-quarto
echo -e "  ${PASS} Directories created"

# --- 5. Sync extension theme ---
if [[ -f scripts/sync-extension.sh ]]; then
    bash scripts/sync-extension.sh
    echo -e "  ${PASS} Extension theme synced"
fi

# --- 6. Test render ---
echo ""
echo -e "${BOLD}Running test render...${RESET}"
test_file="examples/demo.qmd"
if [[ -f "$test_file" ]]; then
    if quarto render "$test_file" --quiet 2>/dev/null; then
        echo -e "  ${PASS} Test render succeeded (${test_file})"
    else
        echo -e "  ${FAIL} Test render failed (${test_file})"
        ((errors++))
    fi
else
    echo -e "  ${WARN} No test file found at ${test_file} — skipping render test"
fi

# --- Summary ---
echo ""
if (( errors == 0 )); then
    echo -e "${GREEN}${BOLD}All checks passed!${RESET} Ready to develop."
    echo ""
    echo "  Quick start:"
    echo "    ./scripts/new-deck.sh my-deck.qmd   # Create a new deck"
    echo "    quarto preview my-deck.qmd           # Live preview"
    echo "    python scripts/quality_score.py my-deck.qmd  # Score it"
else
    echo -e "${RED}${BOLD}${errors} check(s) failed.${RESET} Fix the issues above before proceeding."
    exit 1
fi
```

### Files to Modify

#### `README.md`
Add a "For Contributors" section pointing to DEVELOP.md:
```markdown
## Contributing

See [DEVELOP.md](DEVELOP.md) for architecture overview, setup instructions, and development workflows.
```

### Dependencies
- `scripts/sync-extension.sh` from Work Item 2 (setup.sh calls it)
- `quality_reports/` directory referenced in DEVELOP.md depends on Phase 2 session persistence work
- All other content is self-contained

### Complexity: **M** (Medium)
DEVELOP.md requires comprehensive coverage of the project's workflows. setup.sh requires platform-aware checks (macOS vs Linux font detection, Quarto version parsing).

### Acceptance Criteria
1. `DEVELOP.md` exists at project root with all sections listed above
2. `scripts/setup.sh` is executable (`chmod +x`)
3. `setup.sh` exits 0 on a machine with Quarto + Python installed
4. `setup.sh` exits 1 with clear error messages on a machine missing Quarto
5. `setup.sh` creates `quality_reports/plans/` and `_extensions/impeccable-quarto/` directories
6. `setup.sh` runs a test render if `examples/demo.qmd` exists
7. DEVELOP.md covers: architecture, prerequisites, quick start, adding themes, adding templates, modifying scoring, adding skills, agent development, scripts reference, troubleshooting
8. DEVELOP.md is consistent with CLAUDE.md (same directory structure, same commands)

---

## Work Item 4: Enhanced Demo Site

### Goal
Upgrade the GitHub Pages demo site from a minimal landing page to a showcase that demonstrates the quality system's capabilities — theme previews, before/after examples, live slide embeds, and score visualization.

### Current State
- `docs/index.html` — handcrafted landing page (~600 lines) with sections: Anti-Patterns, Design System, Themes, Quality, Get Started, FAQ
- `docs/style.css` — custom styles for the landing page
- `docs/script.js` — interaction logic (mobile menu, scroll animations)
- `docs/examples/` — rendered HTML slides from `examples/`
- Deployed via `scripts/deploy.sh` which renders all examples and copies to `docs/`

### Files to Create

#### `docs/pages/theme-preview.html`
A dedicated page for interactive theme comparison.

**Content structure:**
- Dropdown or tab switcher for 5 themes (master, academic, corporate, creative, lightning)
- Side-by-side or single iframe showing a sample slide rendered with each theme
- OKLCH color palette display for each theme (showing primary, secondary, accent, semantic colors)
- Typography stack preview (headings, body, code in actual fonts)

**Implementation approach:**
- Use `<iframe>` elements pointing to rendered example slides
- Theme switching via JS that swaps iframe `src`
- Color swatches generated from the theme's OKLCH values
- No build tools required — vanilla HTML/CSS/JS matching existing `docs/` approach

#### `docs/pages/before-after.html`
Showcase the quality system's impact with before/after comparisons.

**Content structure:**
- 3-4 examples of common anti-patterns (Bullet Wall, Generic Theme, Content Dump, Missing Notes)
- Each example shows:
  - **Before:** Screenshot or iframe of the problematic slide
  - **Issue:** What anti-pattern is detected and its severity
  - **After:** The fixed version
  - **Score delta:** Point change from the fix
- Interactive slider (CSS `resize` or JS drag) for visual comparison

**Implementation approach:**
- Create 3-4 pairs of minimal `.qmd` files in `examples/before-after/`:
  - `bullet-wall-before.qmd` / `bullet-wall-after.qmd`
  - `generic-theme-before.qmd` / `generic-theme-after.qmd`
  - `content-dump-before.qmd` / `content-dump-after.qmd`
  - `tiny-text-before.qmd` / `tiny-text-after.qmd`
- Render both versions; embed in iframes with comparison UI
- Score annotations from quality rubric

#### `docs/pages/scoring.html`
Visualize the quality gate system.

**Content structure:**
- Interactive score bar (0–100) with gate thresholds marked
- Example presentation at each gate level with representative issues
- Deduction calculator: check boxes for common issues, see live score
- Link to full rubric (`.claude/rules/quality-gates.md` rendered as HTML)

**Implementation approach:**
- Score bar as CSS gradient with labeled tick marks
- Deduction calculator as a form with checkboxes grouped by CRIT/MAJ/MIN
- JS calculates running total and highlights the resulting gate
- No server required — all client-side

### Files to Modify

#### `docs/index.html`
- Add navigation links to new pages (Theme Preview, Before/After, Scoring)
- Add a "Live Examples" section with iframe embeds of 2-3 rendered slides
- Add a "Quality Gates" visual showing the score spectrum
- Improve "Get Started" section with `quarto add` instructions (from Work Item 2)

#### `docs/style.css`
- Add styles for iframe slide embeds (16:9 aspect ratio container, border, shadow)
- Add comparison slider styles (before/after overlay)
- Add score bar styles (gradient, tick marks, gate labels)
- Add page-specific styles for new sub-pages

#### `docs/script.js`
- Add theme switcher logic (iframe src swapping)
- Add comparison slider drag handler
- Add score calculator logic
- Add page routing if using SPA-style navigation (or keep as separate HTML files)

#### `scripts/deploy.sh`
- Add rendering of before/after examples from `examples/before-after/`
- Copy new sub-pages to `docs/pages/`
- Ensure the deploy process builds all demo content

### Files to Create (Example Content)

#### `examples/before-after/bullet-wall-before.qmd`
A single slide with 8+ bullet points, no semantic boxes, no speaker notes.

#### `examples/before-after/bullet-wall-after.qmd`
Same content restructured: 2 slides with semantic boxes, ≤5 bullets each, speaker notes added.

#### `examples/before-after/generic-theme-before.qmd`
A slide using `theme: default` with no customization.

#### `examples/before-after/generic-theme-after.qmd`
Same content with `themes/impeccable.scss` applied.

(Repeat pattern for `content-dump` and `tiny-text` pairs.)

### Dependencies
- Work Item 2 (Quarto extension) for the "Get Started" installation instructions
- Rendered examples depend on themes being stable
- Before/after examples are self-contained

### Complexity: **L** (Large)
Multiple new HTML pages, interactive JS components, 8+ new example .qmd files, deploy script updates, and design work for the comparison UI. This is the largest work item in Phase 5.

### Acceptance Criteria
1. Theme preview page shows all 5 themes with live slide embeds
2. Before/after page shows at least 3 anti-pattern comparisons with visual diff
3. Scoring page has an interactive deduction calculator
4. Navigation from `index.html` to all sub-pages works
5. All new pages follow the existing design language (same fonts, colors, layout patterns)
6. `scripts/deploy.sh` successfully builds and deploys all new content
7. All iframe embeds load correctly (no broken references)
8. Pages are responsive (work on mobile and desktop)
9. No accessibility regressions (skip links, alt text, focus management preserved)
10. Before/after `.qmd` files each render without errors

---

## Summary

| # | Work Item | Files Created | Files Modified | Complexity | Dependencies |
|---|-----------|--------------|----------------|------------|--------------|
| 1 | Claude Code Plugin Packaging | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` | None | **S** | None |
| 2 | Quarto Extension Format | `_extensions/impeccable-quarto/_extension.yml`, `_extensions/impeccable-quarto/impeccable.scss`, `scripts/sync-extension.sh` | `README.md` | **M** | None |
| 3 | DEVELOP.md + Setup Script | `DEVELOP.md`, `scripts/setup.sh` | `README.md` | **M** | WI-2 (sync script) |
| 4 | Enhanced Demo Site | `docs/pages/theme-preview.html`, `docs/pages/before-after.html`, `docs/pages/scoring.html`, 8× `examples/before-after/*.qmd` | `docs/index.html`, `docs/style.css`, `docs/script.js`, `scripts/deploy.sh` | **L** | WI-2 (install instructions) |

### Recommended Execution Order
1. **WI-1** first (smallest, no dependencies, immediate value for plugin discovery)
2. **WI-2** next (enables `quarto add` and provides sync script needed by WI-3)
3. **WI-3** after WI-2 (setup.sh calls sync-extension.sh)
4. **WI-4** last (largest, benefits from all prior items being complete)

### Total Estimated Effort
- WI-1: ~1 hour
- WI-2: ~3-4 hours
- WI-3: ~4-6 hours
- WI-4: ~2-3 days
- **Total: ~3-4 days**

---

*Generated by distribution-planner agent on 2026-04-03*
