# Phase 3: Quality Infrastructure — Implementation Plan

**Date:** 2026-04-03
**Author:** quality-planner
**Status:** DRAFT
**Phase Dependencies:** Phase 1 (Foundation Fixes), Phase 2 (Operational Governance)

---

## Overview

Phase 3 builds the automated enforcement layer for impeccable-quarto's quality system. It addresses four gaps identified in the synthesis analysis:

1. **No CI/CD** — quality checks are entirely manual
2. **No LLM bias detection** — the system can't detect "AI slop" in generated slides
3. **No hub skill** — each skill independently loads context, risking inconsistency
4. **No report standard** — agent outputs vary in format, making synthesis difficult

---

## Work Item 1: GitHub Actions CI/CD

### Goal
Create a GitHub Actions workflow that automatically renders all example presentations and runs quality scoring on every push to `main`.

### Files to Create

#### `.github/workflows/quality.yml`

```yaml
name: Quality Gate

on:
  push:
    branches: [main]
    paths:
      - 'examples/**'
      - 'themes/**'
      - 'templates/**'
      - 'scripts/quality_score.py'
  pull_request:
    branches: [main]
    paths:
      - 'examples/**'
      - 'themes/**'
      - 'templates/**'
      - 'scripts/quality_score.py'
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: quality-${{ github.ref }}
  cancel-in-progress: true

jobs:
  render:
    name: Render & Score
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: quarto-dev/quarto-actions/setup@v2

      - name: Render all example presentations
        run: |
          failed=0
          for qmd in examples/*.qmd; do
            if [ -f "$qmd" ]; then
              echo "::group::Rendering $qmd"
              if quarto render "$qmd" 2>&1; then
                echo "OK: $qmd"
              else
                echo "::error file=$qmd::Compilation failed for $qmd"
                failed=$((failed + 1))
              fi
              echo "::endgroup::"
            fi
          done
          if [ "$failed" -gt 0 ]; then
            echo "::error::$failed file(s) failed to render"
            exit 1
          fi

      - name: Run quality scoring
        run: |
          pip install --quiet pyyaml 2>/dev/null || true
          failed=0
          echo "## Quality Scores" >> "$GITHUB_STEP_SUMMARY"
          echo "" >> "$GITHUB_STEP_SUMMARY"
          echo "| File | Score | Grade | Status |" >> "$GITHUB_STEP_SUMMARY"
          echo "|------|-------|-------|--------|" >> "$GITHUB_STEP_SUMMARY"
          for qmd in examples/*.qmd; do
            if [ -f "$qmd" ]; then
              echo "::group::Scoring $qmd"
              output=$(python scripts/quality_score.py "$qmd" --verbose 2>&1) || true
              echo "$output"
              # Extract score from output
              score=$(echo "$output" | grep -oP 'Score:\s+\K\d+' | head -1)
              grade=$(echo "$output" | grep -oP 'Score:.*\((\K[A-F])' | head -1)
              if [ -n "$score" ]; then
                if [ "$score" -ge 80 ]; then
                  status="PASS"
                else
                  status="FAIL"
                  failed=$((failed + 1))
                fi
                echo "| $(basename $qmd) | $score/100 | $grade | $status |" >> "$GITHUB_STEP_SUMMARY"
              fi
              echo "::endgroup::"
            fi
          done
          if [ "$failed" -gt 0 ]; then
            echo "" >> "$GITHUB_STEP_SUMMARY"
            echo "> **$failed file(s) below quality threshold (80/100)**" >> "$GITHUB_STEP_SUMMARY"
            echo "::warning::$failed file(s) scored below 80/100"
          fi

      - name: Validate theme SCSS
        run: |
          # Check that theme files are valid SCSS (basic syntax check)
          for scss in themes/*.scss; do
            if [ -f "$scss" ]; then
              echo "Validating $scss..."
              # Basic check: file is not empty and has valid SCSS structure
              if [ ! -s "$scss" ]; then
                echo "::error file=$scss::Empty theme file"
                exit 1
              fi
            fi
          done
```

### Design Decisions

- **Trigger on paths**: Only runs when presentation-related files change (not on README edits etc.)
- **Concurrency control**: Cancels in-progress runs on the same branch (from paper2pr pattern)
- **Job summary**: Writes a markdown table to `$GITHUB_STEP_SUMMARY` for easy PR review
- **Score reporting only** (not blocking): Quality scores are reported as warnings, not failures. Compilation failures DO block. This is intentional — the CI should catch regressions but not block iteration on new decks that start below 80.
- **No deployment**: Deployment stays in `deploy.sh` for now. CI focuses on quality gating. Deployment CI can be added in Phase 5.

### Dependencies on Prior Phases
- **Phase 1**: `quality_score.py` should have compilation check (CRIT-01) and threshold fixed to 80. If Phase 1 is incomplete, the CI will still work but compilation failures will only be caught by the `quarto render` step, not the scoring step.
- **Phase 2**: No hard dependencies.

### Estimated Complexity
**S** (Small) — Single YAML file, well-understood GitHub Actions patterns, clear reference in paper2pr.

### Acceptance Criteria
1. `.github/workflows/quality.yml` exists and is valid YAML
2. Workflow triggers on push to `main` and on PRs
3. All `examples/*.qmd` files are rendered with `quarto render`
4. Compilation failures cause the workflow to fail (exit 1)
5. `quality_score.py` runs on each `.qmd` and scores are reported in the job summary
6. Theme SCSS files are validated (non-empty, exist)
7. Workflow runs successfully in a manual trigger (`workflow_dispatch`)

---

## Work Item 2: AI Slop Detection Anti-Patterns

### Goal
Add an `AP-LLM` anti-pattern category to `.claude/rules/anti-patterns.md` that codifies 5+ LLM-specific slide design patterns, adapted from impeccable-original's "AI Slop Detection" framework.

### Files to Modify

#### `.claude/rules/anti-patterns.md` — Add new section after Technical Anti-Patterns

Append the following section:

```markdown
## LLM Design Bias Anti-Patterns

These patterns are fingerprints of AI-generated presentations (2024-2025 era). They signal that the LLM produced default output without genuine design thought. The overarching test: "If you showed this deck to someone and said 'AI made this,' would they believe you immediately? If yes, that's the problem."

### AP-LLM01: Generic Theme
- **Detection:** Default Reveal.js theme (`theme: default`, `theme: moon`, `theme: solarized`, etc.) with no custom `.scss` override. Or `theme:` field missing entirely.
- **Severity:** Major
- **Why it's bad:** Every LLM-generated deck defaults to the same handful of Reveal.js themes. Using one signals zero design thought and makes the presentation indistinguishable from thousands of others.
- **Fix:** Apply the impeccable theme (`themes/impeccable.scss`) or create a project-specific variant. Custom theme is the single highest-impact design decision.
- **Related:** AP-D01

### AP-LLM02: Monotonous Structure
- **Detection:** ≥70% of content slides follow the identical pattern: heading + bullet list. No variation in slide layouts (no semantic boxes, no columns, no comparison layouts, no full-bleed images).
- **Severity:** Major
- **Why it's bad:** LLMs default to heading + bullets for every slide because it's the safest structure. Real presentations vary layout to match content type — data gets charts, comparisons get side-by-side, key points get semantic boxes.
- **Fix:** Audit each slide's content type and match layout: use `.two-col` for comparisons, `.keybox` for takeaways, `.methodbox` for processes, images for visual concepts. Aim for ≤50% bullet-list slides.

### AP-LLM03: AI Color Palette
- **Detection:** High-chroma cyan (`#00BCD4`, `#00ACC1`), purple-to-blue gradients, neon accents on dark backgrounds, or any non-OKLCH color values that match the typical AI-generated aesthetic (cyan/purple/neon tones).
- **Severity:** Minor
- **Why it's bad:** The "AI color palette" — cyan-on-dark, purple-to-blue gradients, neon accents — is the single most recognizable visual fingerprint of AI-generated interfaces from 2024-2025. Using these colors screams "AI made this."
- **Fix:** Use the OKLCH palette from the impeccable theme. Colors should be semantically meaningful, not decoratively "techy."

### AP-LLM04: Gradient Text
- **Detection:** CSS `background-clip: text` with gradient, or `background: linear-gradient(...)` / `background: -webkit-linear-gradient(...)` applied to text elements in `.qmd` inline styles or custom CSS.
- **Severity:** Minor
- **Why it's bad:** Gradient text on headings or metrics is a signature AI design choice. It looks "impressive" on first glance but adds no information and reduces readability. It's decoration masquerading as emphasis.
- **Fix:** Use the theme's semantic emphasis: `.hi` classes for inline highlights, semantic boxes for structural emphasis, or OKLCH accent color for genuine emphasis.

### AP-LLM05: Nested Semantic Boxes
- **Detection:** A semantic box class (`.keybox`, `.methodbox`, `.warningbox`, `.tipbox`, `.quotebox`, `.infobox`) nested inside another semantic box.
- **Severity:** Minor
- **Why it's bad:** LLMs overuse semantic boxes and often nest them (a `.methodbox` inside a `.keybox`) to appear "structured." This creates visual noise, breaks the box hierarchy, and confuses the reader about what's key vs. supporting.
- **Fix:** One box level per slide section. If you need to highlight something within a box, use inline emphasis (`.hi`, bold) not a nested box.

### AP-LLM06: Uniform Depth
- **Detection:** Inconsistent content depth across slides — some slides have 3 words, others have 200+ words. Standard deviation of word count across slides exceeds 3x the mean.
- **Severity:** Minor
- **Why it's bad:** LLMs often produce slides of wildly varying depth — a title slide with "Introduction" followed by a slide with 8 dense paragraphs. This signals the LLM is dumping content without editing for audience pacing.
- **Fix:** Target consistent depth: 20-40 words per slide for body text. Move excess detail to speaker notes. Each slide should take roughly the same time to present (1-2 minutes).

### AP-LLM07: Generic Titles
- **Detection:** Title slide contains generic text: "Presentation Title", "Subtitle Here", "Your Name", "Author Name", "[Topic]", "Click to edit", or any placeholder-like text.
- **Severity:** Major
- **Why it's bad:** Generic placeholder titles are the most obvious sign of auto-generated content. Even draft decks should have specific, descriptive titles.
- **Fix:** Replace with a specific, compelling title that communicates the deck's key message. The title is the audience's first impression — make it count.
```

#### `.claude/rules/quality-gates.md` — Add LLM deductions to scoring table

Add to the Major Deductions table:

```markdown
| MAJ-10 | Generic/placeholder title text | -5 |
| MAJ-11 | Monotonous structure (≥70% identical layout) | -5 |
```

Add to the Minor Deductions table:

```markdown
| MIN-08 | AI color palette (non-OKLCH cyan/purple/neon) | -2 per instance |
| MIN-09 | Gradient text in styles | -2 per instance |
| MIN-10 | Nested semantic boxes | -2 per instance |
| MIN-11 | Uniform depth violation (word count StdDev >3x mean) | -2 |
```

### Design Decisions

- **7 patterns, not 12**: impeccable-original defines 12 AI fingerprints for web interfaces. We adapted the 7 most relevant to RevealJS slides. Patterns like glassmorphism, sparklines-as-decoration, and hero metric layouts are rare in slides and omitted.
- **Severity calibration**: AP-LLM01 (Generic Theme) and AP-LLM07 (Generic Titles) are Major because they are immediately visible and high-impact. The others are Minor because they're subtler.
- **Detection criteria are LLM-parseable**: Each detection criterion is written so an agent can check for it during the `/critique-slides` workflow without needing custom tooling.
- **"Why it's bad" includes the meta-pattern**: Each entry connects back to the overarching "AI slop" principle, helping the agent understand the spirit, not just the letter.
- **AP-LLM01 overlaps with AP-D01**: This is intentional. AP-D01 is the general "generic theme" pattern; AP-LLM01 adds the LLM-specific context (why it happens, the AI slop connection). The deduction is shared (MAJ-09).

### Dependencies on Prior Phases
- **Phase 1**: No hard dependencies. The anti-patterns are rules for agent-driven review, not automated scripts.
- **Phase 2**: No hard dependencies.

### Estimated Complexity
**S** (Small) — Text additions to existing markdown files. No code changes.

### Acceptance Criteria
1. `anti-patterns.md` contains a new "LLM Design Bias Anti-Patterns" section with 7 patterns (AP-LLM01 through AP-LLM07)
2. Each pattern has Detection, Severity, Why it's bad, and Fix fields
3. `quality-gates.md` has corresponding deduction entries (MAJ-10, MAJ-11, MIN-08 through MIN-11)
4. The "AI Slop Test" overarching principle is stated at the section header
5. No existing anti-patterns are modified or removed
6. Severity levels are consistent with the existing deduction scale

---

## Work Item 3: Hub Skill (`/slide-design`)

### Goal
Create a shared foundation skill that loads the core design context — `.impeccable-quarto.md`, theme reference, design vocabulary, and the AI Slop Test. All design-related skills should reference this hub.

### Files to Create

#### `.claude/skills/slide-design.md`

```markdown
---
name: slide-design
description: "Hub skill: loads design context, theme reference, and design vocabulary. Called by all design skills before execution."
user-invocable: true
argument-hint: ""
---

# /slide-design — Design Context Hub

This is the shared foundation for all design skills. It ensures every design operation starts with consistent context: project preferences, theme reference, design vocabulary, and the AI Slop Test.

**When to invoke:** Every design-related skill (`/critique-slides`, `/audit-slides`, `/typeset-slides`, `/colorize-slides`, `/bolder-slides`, `/quieter-slides`, `/polish-slides`, `/normalize-slides`, `/arrange-slides`, `/animate-slides`, `/create-deck`) should reference this hub as their first preparation step.

**When invoked standalone:** Provides a summary of the active design context — useful for checking what design system is in effect before starting work.

## STEP 1: Load Project Context

1. **Check `.impeccable-quarto.md`** in the project root:
   - If it exists: read it. This is the project's customized design context (audience, palette, fonts, constraints).
   - If it does NOT exist: note that defaults will be used. Suggest running `/teach-style` to create one.

2. **Check YAML frontmatter** of the target `.qmd` (if one is being worked on):
   - Extract `theme:` — which SCSS file(s) are applied?
   - Extract `width:` and `height:` — what are the slide dimensions?
   - Extract any `css:` overrides
   - Flag if no custom theme is specified (AP-LLM01)

## STEP 2: Load Design System Reference

Read these rules files to establish the design vocabulary:

1. `.claude/rules/design-standards.md` — Typography stack, OKLCH palette, layout grid, accessibility
2. `.claude/rules/anti-patterns.md` — All anti-patterns including LLM Design Bias patterns
3. `.claude/rules/quality-gates.md` — Scoring rubric for quantitative assessment

**Key design vocabulary to keep active:**

### Typography Stack
| Role | Font | Fallback |
|------|------|----------|
| Display | Plus Jakarta Sans | Outfit, sans-serif |
| Body | Source Sans 3 | Source Sans Pro, sans-serif |
| Code | JetBrains Mono | Fira Code, monospace |

### OKLCH Palette
| Role | Value |
|------|-------|
| Primary | oklch(0.45 0.18 265) — Deep Indigo |
| Secondary | oklch(0.55 0.12 195) — Warm Teal |
| Accent | oklch(0.72 0.16 85) — Marigold |
| Near-black | oklch(0.12 0.015 265) |
| Near-white | oklch(0.96 0.012 265) |

### Semantic Boxes
keybox (key findings), methodbox (process), warningbox (caveats), tipbox (recommendations), quotebox (citations), infobox (supplementary)

### Layout Classes
`.two-col`, `.three-col`, `.sidebar-left`, `.sidebar-right`, `.comparison`

## STEP 3: AI Slop Test

**This check applies to ALL design work.** Before finalizing any design output, verify:

> "If you showed this deck to someone and said 'AI made this,' would they believe you immediately? If yes, that's the problem."

Quick checklist:
- [ ] Custom theme applied (not default Reveal.js)?
- [ ] Layout variety (not all heading + bullets)?
- [ ] OKLCH colors (no cyan/purple AI palette)?
- [ ] No gradient text?
- [ ] No nested semantic boxes?
- [ ] Specific, compelling title (no placeholders)?
- [ ] Consistent content depth across slides?

## STEP 4: Establish Session Design Context

Synthesize into a working context:

```
DESIGN CONTEXT ACTIVE:
- Theme: [theme name from YAML or .impeccable-quarto.md]
- Palette: [OKLCH values — custom or default]
- Fonts: [display / body / code]
- Audience: [from .impeccable-quarto.md or "general"]
- Constraints: [max slides, required sections, domain terms]
- AI Slop Guard: ACTIVE
```

This context carries through all subsequent design operations in the session.

## Standalone Output

When invoked by the user directly (not as a dependency):

```
## Design Context Report

### Project Configuration
- .impeccable-quarto.md: [found/not found]
- Theme: [theme details]
- Custom palette: [yes/no + details]

### Active Design System
- Typography: [stack]
- Colors: [palette summary]
- Layout classes: [available]
- Semantic boxes: [available]

### AI Slop Guard: [ACTIVE/INACTIVE]

### Recommendation
[If .impeccable-quarto.md is missing, suggest /teach-style]
[If theme is default, suggest applying impeccable.scss]
```
```

### Design Decisions

- **User-invocable**: Yes — users can run `/slide-design` standalone to check the current design context. This doubles as a diagnostic.
- **Not a forced dependency**: Unlike impeccable-original where `frontend-design` is literally invoked by every skill, our hub is referenced in the MANDATORY PREPARATION section of other skills. This is lighter-weight and doesn't require a chaining mechanism.
- **AI Slop Test integrated**: The hub is the natural home for the AI Slop Test since it's loaded by every design skill.
- **No `argument-hint`**: The hub doesn't operate on a specific file — it establishes context.

### Files to Modify

Update the `[MANDATORY PREPARATION]` section of the following skills to reference the hub:

#### Skills that should add `/slide-design` reference:

These 11 design-related skills should have their `[MANDATORY PREPARATION]` section updated to start with:

```markdown
[MANDATORY PREPARATION]
- Load design context: Read `.claude/skills/slide-design.md` and follow Steps 1-3 to establish design context
```

**Skills to update** (add the hub reference as the FIRST item in `[MANDATORY PREPARATION]`):

1. `.claude/skills/critique-slides.md`
2. `.claude/skills/audit-slides.md`
3. `.claude/skills/typeset-slides.md`
4. `.claude/skills/colorize-slides.md`
5. `.claude/skills/bolder-slides.md`
6. `.claude/skills/quieter-slides.md`
7. `.claude/skills/polish-slides.md`
8. `.claude/skills/normalize-slides.md`
9. `.claude/skills/arrange-slides.md`
10. `.claude/skills/animate-slides.md`
11. `.claude/skills/create-deck.md`

The following skills do NOT need the hub:
- `teach-style.md` — creates the context that the hub reads
- `translate-source.md` — content-focused, not design-focused
- `review-slides.md` — orchestrator, delegates to agents
- `qa-loop.md` — orchestrator, delegates to agents
- `clarify-slides.md` — content-focused
- `distill-slides.md` — content-focused
- `adapt-slides.md` — audience adaptation, could optionally include hub

### Dependencies on Prior Phases
- **Phase 1**: Ideally SSOT is resolved (source/ vs .claude/ canonical question). If not, the hub works with `.claude/` as-is.
- **Phase 2**: No dependencies.
- **Work Item 2** (this phase): AI Slop patterns should exist in `anti-patterns.md` before the hub references them. Implement WI-2 before or concurrently with WI-3.

### Estimated Complexity
**M** (Medium) — One new skill file + modifications to 11 existing skill files.

### Acceptance Criteria
1. `.claude/skills/slide-design.md` exists with the 4-step structure
2. Hub loads `.impeccable-quarto.md`, design rules, and AI Slop Test
3. Hub provides a standalone output format when invoked directly
4. 11 design-related skills reference the hub in `[MANDATORY PREPARATION]`
5. Non-design skills (`teach-style`, `translate-source`, `review-slides`, `qa-loop`) are NOT modified
6. The hub does NOT attempt to execute any file modifications — it is context-only

---

## Work Item 4: Agent Report Standard

### Goal
Create a standardized report template that all agents use for their output, ensuring consistent format for synthesis and tracking.

### Files to Create

#### `templates/agent-report.md`

```markdown
---
template: agent-report
version: 1.0
description: "Standard output format for all diagnostic and review agents"
---

# [Agent Name] Report: [Deck Name]

**Date:** YYYY-MM-DD
**Agent:** [agent type — slide-critic | layout-auditor | typography-reviewer | verifier | etc.]
**Round:** N (if applicable, omit for single-pass reviews)
**File:** [path to .qmd file]
**Verdict:** APPROVED | NEEDS REVISION | REJECTED

---

## Hard Gate Status

Non-negotiable quality conditions. A single FAIL = REJECTED verdict.

| Gate | Status | Detail |
|------|--------|--------|
| Compilation | PASS / FAIL | `quarto render` exit code |
| Content overflow | PASS / FAIL | Slides with overflow: [list or "none"] |
| Image references | PASS / FAIL | Broken refs: [list or "none"] |
| YAML frontmatter | PASS / FAIL | Missing fields: [list or "none"] |
| Cross-references | PASS / FAIL | Broken refs: [list or "none"] |

## Score

| Metric | Value |
|--------|-------|
| **Current** | XX/100 |
| **Previous** | YY/100 (if applicable) |
| **Delta** | +/-ZZ |
| **Gate** | [Failing / Needs Work / Draft / Presentable / Excellent / Impeccable] |
| **Target** | [threshold, default 90/100] |

## Issues Found

### Critical (X issues, -N points total)

| ID | Slide | Issue | Deduction | Recommended Fix |
|----|-------|-------|-----------|----------------|
| CRIT-XX | N | Description | -X | Fix description |

### Major (X issues, -N points total)

| ID | Slide | Issue | Deduction | Recommended Fix |
|----|-------|-------|-----------|----------------|
| MAJ-XX | N | Description | -X | Fix description |

### Minor (X issues, -N points total)

| ID | Slide | Issue | Deduction | Recommended Fix |
|----|-------|-------|-----------|----------------|
| MIN-XX | N | Description | -X | Fix description |

## Strengths

Identify what works well — this prevents the review from being purely negative and helps preserve good design decisions during fixes.

- [Specific strength with slide reference]
- [Specific strength with slide reference]

## Recommended Next Actions

Prioritized list of what to do next. Each action maps to a skill or agent.

1. **[Priority: Critical/Major/Minor]** — [Action description] — invoke [skill or agent name]
2. **[Priority: Critical/Major/Minor]** — [Action description] — invoke [skill or agent name]

---

*Generated by [agent-name] agent on [date]*
```

### Design Decisions

- **Hard Gate section**: Adopted from paper2pr's binary pass/fail gates. These are the non-negotiable conditions — a single FAIL makes the verdict REJECTED regardless of score.
- **Score section with delta**: Tracks improvement across rounds. The delta and previous score enable stall detection (2 rounds with same score ±2 = terminate loop).
- **Issues tables by severity**: Mirrors our existing quality-gates.md structure (CRIT/MAJ/MIN with IDs and point values).
- **Strengths section**: Ensures the report isn't purely negative. This is important because the fixer needs to know what to preserve.
- **Recommended Next Actions**: Each action maps to a specific skill or agent, creating the "command recommendation pipeline" pattern from impeccable-original.
- **Template frontmatter**: Includes version for future evolution of the format.

### Files to Modify

#### `.claude/rules/review-protocol.md` — Add report standard reference

Add to the "Agent Communication" section:

```markdown
### Report Format Standard

All agent reports MUST use the template in `templates/agent-report.md`. Key requirements:
- Hard Gate Status table must be filled for critic agents
- Score section must include previous score and delta (after round 1)
- Issues must be categorized by severity with deduction point values
- Recommended Next Actions must map to specific skills or agents
- Strengths section must not be empty — identify at least 2 positive aspects
```

#### `.claude/agents/slide-critic.md` — Add report format instruction

Add to the agent definition:

```markdown
## Output Format
Use the standard agent report format from `templates/agent-report.md`. Fill all sections including Hard Gate Status and Strengths.
```

Similarly update:
- `.claude/agents/layout-auditor.md`
- `.claude/agents/typography-reviewer.md`
- `.claude/agents/verifier.md`

### Dependencies on Prior Phases
- **Phase 1**: No dependencies.
- **Phase 2**: If `quality_reports/` directory structure is established in Phase 2, reports can be saved there. If not, the template still works — agents just output to the conversation rather than to files.

### Estimated Complexity
**S** (Small) — One new template file + minor additions to 5 existing files (review-protocol + 4 agent definitions).

### Acceptance Criteria
1. `templates/agent-report.md` exists with full template structure
2. Template includes: Header (agent, date, verdict), Hard Gate Status, Score (with delta), Issues (3 severity tables), Strengths, Recommended Next Actions
3. `review-protocol.md` references the template in its Agent Communication section
4. Agent definitions for `slide-critic`, `layout-auditor`, `typography-reviewer`, `verifier` reference the report format
5. Template version is `1.0`
6. Template is self-documenting (clear instructions in each section)

---

## Implementation Order

```
WI-2 (AI Slop Detection) ──┐
                            ├──→ WI-3 (Hub Skill) ──→ Done
WI-4 (Agent Report)  ──────┘
WI-1 (CI/CD) ──────────────────────────────────────→ Done
```

- **WI-1** (CI/CD) is independent — can be implemented in parallel with everything else
- **WI-2** (AI Slop) should be done before **WI-3** (Hub Skill) since the hub references the AI Slop Test
- **WI-4** (Agent Report) is independent — can be implemented in parallel with WI-1 and WI-2
- **WI-3** (Hub Skill) depends on WI-2 being complete

**Recommended parallel execution:**
- Stream A: WI-1 (CI/CD) + WI-4 (Agent Report) — both independent, small
- Stream B: WI-2 (AI Slop) → WI-3 (Hub Skill) — sequential dependency

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| CI/CD `quarto render` times out on large decks | Medium | Set job timeout to 10 min; our examples are small |
| Quality score regex parsing fails in CI | Low | Score reporting is warning-only; render failures are the real gate |
| Hub skill creates redundant context loading (slower) | Low | Hub is read-only context; cost is one extra file read per skill invocation |
| AI Slop patterns are too strict | Low | All new patterns are Minor severity (except Generic Theme/Title which are Major and already existed as AP-D01) |
| Agent report format is too rigid for some agents | Low | Template is a guide — agents can add sections but must include the required fields |

---

## Verification Plan

After all 4 work items are implemented:

1. **CI/CD**: Manually trigger `workflow_dispatch` and verify all examples render + score
2. **AI Slop**: Run `/critique-slides` on an example deck and verify AP-LLM patterns appear in the review
3. **Hub Skill**: Run `/slide-design` standalone and verify context report is generated
4. **Agent Report**: Run `/review-slides` on an example and verify agent outputs match the template format

---

*Phase 3 plan generated by quality-planner on 2026-04-03*
