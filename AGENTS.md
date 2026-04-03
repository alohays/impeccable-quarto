# impeccable-quarto — Agent & Project Instructions

## Project Overview

impeccable-quarto is a **Quarto RevealJS slide design quality system**. It provides curated themes, quality scoring, anti-pattern detection, and an adversarial review pipeline for presentations.

**Core philosophy:** Slides should be typography-first, OKLCH-colored, semantically structured, and objectively scored — not left to LLM design bias defaults.

---

## Design Principles

- **OKLCH everywhere** — all colors in perceptually uniform OKLCH; no hex/RGB
- **Tinted neutrals** — never pure `#000` or `#FFF`; neutrals carry subtle hue
- **Typography-first** — Plus Jakarta Sans / Source Sans 3 / JetBrains Mono; 28px base; 1.25 scale
- **One idea per slide** — max 5 bullets, max 40 words body text, speaker notes on every content slide
- **Semantic structure** — use `.keybox`, `.methodbox`, `.warningbox`, `.tipbox`, `.quotebox`, `.infobox` and layout classes

See `.claude/rules/design-standards.md` for complete standards.
See `.claude/rules/anti-patterns.md` for the full anti-pattern registry (content, design, typography, technical, LLM bias, deck-level).
See `.claude/rules/quality-gates.md` for the scoring rubric and deduction table.

---

## Agent Roster

### slide-critic

**Role:** Adversarial read-only reviewer
**Scope:** Read-only — never modifies files
**Tools:** Read, Glob, Grep, Bash (read-only)
**Context:** fork

Assumes the presentation is flawed. Produces scored reports with findings categorized by severity (Critical/Major/Minor). Every finding references a slide number, explains *why*, and suggests a fix.

**Rules:**
- Reference `quality-gates.md` for all deductions
- Reference `anti-patterns.md` for pattern matching
- Identify strengths, not just weaknesses
- Produce mathematically consistent scores

---

### slide-fixer

**Role:** Applies fixes from critic reports
**Scope:** Modifies `.qmd` files and theme references
**Tools:** Read, Glob, Grep, Edit, Write, Bash
**Context:** fork

Takes a critic report and addresses every issue by severity (Critical -> Major -> Minor).

**Rules:**
- Address Critical issues first
- Must not introduce new issues while fixing
- Preserve the author's intent and voice
- Run compilation check after fixes
- Must not fix issues the critic didn't identify (scope creep)

---

### typography-reviewer

**Role:** Font, hierarchy, and readability specialist
**Scope:** Read-only
**Tools:** Read, Glob, Grep, Bash (read-only)
**Context:** fork

Checks: font sizes (28px base, 20px minimum), heading hierarchy, type scale ratio, font weights, line height (>=1.3 body, >=1.1 headings), letter spacing, font families (max 3).

---

### layout-auditor

**Role:** Spatial design, overflow, and alignment specialist
**Scope:** Read-only
**Tools:** Read, Glob, Grep, Bash (read-only)
**Context:** fork

Checks: content overflow, whitespace, grid alignment, column balance, image dimensions, padding consistency, content fill (max 70%).

---

### content-translator

**Role:** Converts source material to slide content
**Scope:** Creates new `.qmd` content
**Tools:** Read, Glob, Grep, Edit, Write, Bash

Rules: one idea per slide, max 5 bullets, max 40 words, narrative arc (Context -> Problem -> Approach -> Results -> Takeaway), speaker notes on every slide.

---

### theme-designer

**Role:** Creates and adapts SCSS themes
**Scope:** Modifies `.scss` files
**Tools:** Read, Glob, Grep, Edit, Write, Bash

Rules: all colors OKLCH, tinted neutrals (chroma > 0), WCAG AA contrast, max 5 palette colors, every color has a semantic role.

---

### verifier

**Role:** Compilation and rendering verification
**Scope:** Read-only + build execution
**Tools:** Read, Glob, Grep, Bash (including quarto render)
**Context:** fork

Process: `quarto render` -> check errors -> re-run scoring -> compare against threshold -> verify previous fixes. Compilation failure = automatic no-ship.

---

### pedagogy-reviewer

**Role:** Narrative arc, pacing, and cognitive load
**Scope:** Read-only
**Tools:** Read, Glob, Grep, Bash (read-only)
**Context:** fork

Checks: narrative arc, pacing balance, cognitive load (1 key idea/slide), transitions, engagement variety, opening hook, closing takeaway.

---

## Agent Enforcement

| Agent | Access | Context |
|-------|--------|---------|
| slide-critic | Read-only | fork |
| typography-reviewer | Read-only | fork |
| layout-auditor | Read-only | fork |
| pedagogy-reviewer | Read-only | fork |
| slide-fixer | Read + Write | fork |
| theme-designer | Read + Write | standard |
| content-translator | Read + Write | standard |
| verifier | Read + Build | fork |

---

## Orchestration Protocol

```
Phase 1: PLAN — Define scope, audience, source, target score, constraints
Phase 2: IMPLEMENT — content-translator + theme-designer -> .qmd
Phase 3: REVIEW — slide-critic + typography-reviewer + layout-auditor + pedagogy-reviewer (independent, parallel)
Phase 4: FIX — slide-fixer (Critical -> Major -> Minor)
Phase 5: VERIFY — verifier (compile, score, check fixes)
Phase 6: GATE — score >= target? Done. Else -> Phase 3 (max 5 rounds)
```

### Adversarial QA Rules

1. Creator must not review. Reviewer must not fix. Fixer must not verify.
2. Reviewers work independently — no groupthink.
3. No self-approval in the same context.
4. Severity honesty: Critical = can't show, Major = audience notices, Minor = professional notices.
5. Fixer addresses only identified issues (no scope creep).
6. Verifier independently re-calculates score.

### Round Limits

- Rounds 1-3: Full pipeline (all reviewers + fixer + verifier)
- Rounds 4-5: Focused (slide-critic + slide-fixer + verifier only)
- After round 5: Stop. Report final score and remaining issues.

### Agent Report Format

All agents use `templates/agent-report.md`:

```markdown
# [Agent] Report: [filename]
**Round:** N | **Score:** XX/100 | **Verdict:** APPROVED | NEEDS REVISION | REJECTED
## Hard Gate Status
## Issues Found (Critical / Major / Minor tables with slide refs, deductions, fixes)
## Strengths
## Recommended Next Actions
```

---

## Quality Gates

| Gate | Score |
|------|-------|
| Failing | 0-59 |
| Needs Work | 60-79 |
| Draft | 80-84 |
| Presentable | 85-89 |
| Excellent | 90-94 |
| Impeccable | 95-100 |

Minimum commit threshold: 80. See `.claude/rules/quality-gates.md` for full deduction table.

---

## Build Commands

```bash
quarto render path/to/deck.qmd          # Render single deck
quarto preview path/to/deck.qmd         # Live reload preview
python scripts/quality_score.py deck.qmd # Quality scoring (threshold 80, includes render check)
python scripts/quality_score.py deck.qmd --no-render  # Skip compilation check
bash scripts/setup.sh                    # One-command environment setup
```

---

## Key References

- `.claude/rules/design-standards.md` — OKLCH palette, typography, layout grid, accessibility
- `.claude/rules/anti-patterns.md` — Content, design, typography, technical, LLM bias, deck-level patterns
- `.claude/rules/quality-gates.md` — Scoring rubric, all deduction IDs
- `.claude/rules/orchestrator-protocol.md` — Multi-agent coordination rules
- `.claude/rules/review-protocol.md` — Phase-by-phase review pipeline
- `.claude/rules/source-translation.md` — Paper/document -> slide translation rules
- `.claude/skills/slide-design.md` — Hub skill (shared context for all design skills)
