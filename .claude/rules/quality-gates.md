# Quality Gates — Scoring Rubric

## Overview

Every presentation starts at **100 points**. Issues cause deductions. The final score determines which quality gate the presentation meets.

## Gate Thresholds

| Gate | Score | Status |
|---|---|---|
| Failing | 0–59 | Critical issues; not shippable |
| Needs Work | 60–79 | Structural problems; another round needed |
| Draft | 80–84 | Internal review ready |
| Presentable | 85–89 | Audience ready |
| Excellent | 90–94 | High quality |
| Impeccable | 95–100 | Publication quality |

## Deduction Table

### Critical Deductions

| ID | Issue | Deduction | Auto-fail? |
|---|---|---|---|
| CRIT-01 | Compilation failure (`quarto render` errors) | -100 | Yes |
| CRIT-02 | Broken image reference (file not found) | -15 each | No |
| CRIT-03 | Content overflow (text outside slide bounds) | -10 per slide | No |
| CRIT-04 | Missing YAML frontmatter | -10 | No |
| CRIT-05 | Broken cross-reference (`@fig-`, `@tbl-`, `@sec-`) | -8 each | No |

### Major Deductions

| ID | Issue | Deduction |
|---|---|---|
| MAJ-01 | Missing speaker notes on content slide | -5 per slide |
| MAJ-02 | More than 5 bullet points on a slide | -5 per slide |
| MAJ-03 | Font size below 20px | -5 per instance |
| MAJ-04 | Missing alt text on image | -5 per image |
| MAJ-05 | Pure black (#000000) or white (#FFFFFF) used | -3 per instance |
| MAJ-06 | Heading hierarchy skip (e.g., H1 → H3) | -3 per instance |
| MAJ-07 | Non-OKLCH color in theme override | -3 per instance |
| MAJ-08 | More than 3 font families on a slide | -3 per slide |
| MAJ-09 | Generic/default Reveal.js theme (no customization) | -10 |
| MAJ-10 | Monotonous pacing (>70% same structure) | -5 |
| MAJ-11 | Missing narrative arc (no beginning-middle-end) | -8 |
| MAJ-12 | Depth inconsistency (>4:1 section ratio) | -3 per instance |
| MAJ-13 | Data without interpretation | -3 per slide |

### Minor Deductions

| ID | Issue | Deduction |
|---|---|---|
| MIN-01 | Inconsistent slide separator style (`---` vs `##`) | -2 |
| MIN-02 | Body text exceeds 40 words on a slide | -2 per slide |
| MIN-03 | Missing date in YAML frontmatter | -1 |
| MIN-04 | Image without explicit width/height | -1 per image |
| MIN-05 | Raster image used for diagram (should be SVG) | -1 per image |
| MIN-06 | Inline CSS in `.qmd` file | -1 per instance |
| MIN-07 | Missing transition text between sections | -1 per gap |
| MIN-08 | Orphan section (1-slide section) | -1 per instance |

## Scoring Rules

1. Start at 100
2. Apply all deductions
3. Score cannot go below 0
4. CRIT-01 (compilation failure) is an automatic 0 regardless of other scores
5. Deductions are cumulative (a slide with 7 bullets AND no notes gets -5 + -5 = -10)
6. The same issue type on different slides is counted separately
7. The score must be mathematically verifiable from the deduction list
