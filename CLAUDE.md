# impeccable-quarto — Claude Code Instructions

## Project Overview

impeccable-quarto is a **Quarto RevealJS slide design quality system**. It provides curated themes, quality scoring, anti-pattern detection, and an adversarial review pipeline for presentations.

**Core philosophy:** Slides should be typography-first, OKLCH-colored, semantically structured, and objectively scored — not left to LLM design bias defaults.

## Directory Structure

```
.claude/          Claude Code integration (canonical)
  agents/         Agent persona definitions (7)
  skills/         Slash commands (18)
  rules/          Governance rules, scoring rubrics, anti-patterns (6)
  references/     Design reference documents (6)
  settings.json   Permissions and hooks

themes/           SCSS themes for Quarto RevealJS
  impeccable.scss Master theme (OKLCH · tinted neutrals · typography-first)

templates/        Starter .qmd templates for common presentation types
examples/         Complete example presentations with scores
scripts/          Build, render, and utility scripts
```

## Key Workflows

### 1. Create a New Deck

```
Input:  Source material (paper, outline, notes, idea)
Output: .qmd file with impeccable theme applied
```

Steps:
1. Read source material and identify key messages
2. Structure content into narrative arc (Context → Problem → Approach → Results → Takeaway)
3. Create `.qmd` with YAML frontmatter referencing `themes/impeccable.scss`
4. Apply semantic box classes (`.keybox`, `.methodbox`, `.warningbox`, `.tipbox`, `.quotebox`, `.infobox`)
5. Use layout classes (`.two-col`, `.three-col`, `.sidebar-left`, `.sidebar-right`, `.comparison`)
6. Add speaker notes to every content slide
7. Run quality audit

### 2. Review Cycle

```
Input:  Existing .qmd file
Output: Improved .qmd file meeting target score
```

Protocol: **Audit → Critique → Fix → Enhance → Verify → Gate Check**

- Each round must produce a score
- If score < target, loop back to Audit
- Maximum 5 rounds (configurable)
- Never skip the Verify step

### 3. Translate Source Material

```
Input:  Any document (PDF, markdown, text, URL)
Output: Structured slide content in .qmd
```

Rules:
- One key idea per slide
- Maximum 5 bullet points per slide
- Maximum 40 words of body text per slide
- Every claim needs context or evidence
- Transform paragraphs into visual structures (boxes, columns, comparisons)

## Quality Gates

| Gate | Score | Status |
|---|---|---|
| Failing | 0–59 | Critical issues present |
| Needs Work | 60–79 | Structural problems |
| Draft | 80–84 | Internal review ready |
| Presentable | 85–89 | Audience ready |
| Excellent | 90–94 | High quality |
| Impeccable | 95–100 | Publication quality |

See `.claude/rules/quality-gates.md` for the complete scoring rubric and deduction table.

## Design Principles

- **OKLCH everywhere** — all colors in perceptually uniform OKLCH; no hex/RGB
- **Tinted neutrals** — never pure `#000` or `#FFF`; neutrals carry subtle hue
- **Typography-first** — Plus Jakarta Sans / Source Sans 3 / JetBrains Mono; 28px base; 1.25 scale
- **One idea per slide** — ≤5 bullets, ≤40 words body text, speaker notes on every content slide
- **Semantic structure** — use `.keybox`, `.methodbox`, `.warningbox`, `.tipbox`, `.quotebox`, `.infobox` and layout classes

See `.claude/rules/design-standards.md` for complete standards.
See `.claude/rules/anti-patterns.md` for the full anti-pattern registry.

## Build Commands

```bash
# Render a single deck
quarto render path/to/deck.qmd

# Render all presentations in the project
quarto render

# Preview with live reload
quarto preview path/to/deck.qmd

# Run quality scorer (Python)
python scripts/quality_score.py path/to/deck.qmd

# Create a new deck from template
./scripts/new-deck.sh path/to/new-deck.qmd

# Render all and report errors
./scripts/render.sh --all

# Compare themes side by side
./scripts/theme-preview.sh
```

## Theme Reference

The master theme is `themes/impeccable.scss`. Key variables:

### Colors
```scss
$primary:        oklch(0.45 0.18 265);  // Deep Indigo
$secondary:      oklch(0.55 0.12 195);  // Warm Teal
$accent:         oklch(0.72 0.16 85);   // Marigold
```

### Semantic Colors
```scss
$color-success:  oklch(0.60 0.15 145);  // Green
$color-warning:  oklch(0.72 0.16 85);   // Gold
$color-danger:   oklch(0.55 0.18 25);   // Red
$color-info:     oklch(0.55 0.12 240);  // Blue
```

### Typography
```scss
$font-family-display: "Plus Jakarta Sans";  // Headings
$font-family-body:    "Source Sans 3";      // Body text
$font-family-code:    "JetBrains Mono";     // Code blocks
$base-size:           28px;                 // Minimum readable
$scale-ratio:         1.25;                 // Major Third
```

## Slide YAML Frontmatter Template

```yaml
---
title: "Presentation Title"
subtitle: "Subtitle if needed"
author: "Author Name"
date: "2025-01-15"
institute: "Affiliation"
format:
  revealjs:
    theme: [default, themes/impeccable.scss]
    slide-number: true
    transition: none
    width: 1920
    height: 1080
    center: false
    embed-resources: true
---
```

## Semantic Box Usage

```markdown
::: {.keybox}
**Key Finding**
Main result or takeaway text.
:::

::: {.methodbox}
**Methodology**
Process or approach description.
:::

::: {.warningbox}
**Caveat**
Limitation or warning text.
:::

::: {.tipbox}
**Best Practice**
Recommendation or tip.
:::

::: {.quotebox}
"Quoted text here."

[Attribution]{.attribution}
:::

::: {.infobox}
**Note**
Supplementary information.
:::
```

## Layout Usage

```markdown
## Two Column Slide

::: {.two-col}
::: {}
Left column content
:::
::: {}
Right column content
:::
:::

## Comparison Slide

::: {.comparison}
::: {.compare-left}
**Before** — problems with old approach
:::
::: {.compare-right}
**After** — benefits of new approach
:::
:::
```

## Speaker Notes

```markdown
## Slide Title

Content visible to audience.

::: {.notes}
These notes are only visible in speaker view.
Include talking points, timing cues, and transition hints.
:::
```

## Project-Level Customization

If `.impeccable-quarto.md` exists in the project root, read it for:
- Color palette overrides
- Content constraints (max slides, required sections)
- Audience context
- Language preferences
- Domain-specific terminology
