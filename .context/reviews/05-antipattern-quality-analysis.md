# Anti-Pattern & Quality System Analysis

**Analyst:** antipattern-analyst
**Date:** 2026-04-03
**Sources:**
- `.context/references/impeccable-original/` — Frontend design quality system by Paul Bakaus
- `.context/references/paper2pr/` — Academic slide quality pipeline
- `impeccable-quarto` (this project) — Quarto RevealJS slide design system

---

## 1. Anti-Pattern Catalog Comparison

### 1.1 What Each Repo Detects

| Category | impeccable-original | paper2pr | impeccable-quarto |
|----------|-------------------|----------|-------------------|
| **Content density** | — | — | Bullet wall (>5), content dump (>40 words), text overflow |
| **Narrative structure** | — | — | Missing narrative, orphan slides |
| **Typography abuse** | Inter/Roboto/Arial overuse, monospace-as-shorthand, large rounded icons above headings | Font size reduction (minor) | Tiny text (<20px), heading skip, weight overload (>30% bold), line squeeze (<1.3 line-height), font soup (>3 families) |
| **Color misuse** | Gray-on-colored backgrounds, pure black/white, "AI color palette" (cyan/purple gradients), gradient text, dark-mode-as-default | — | Pure black/white, random non-OKLCH colors |
| **Layout abuse** | Card nesting, identical card grids, hero metric layout, center-everything, same-spacing-everywhere | — | Generic theme (no customization) |
| **Visual decoration** | Glassmorphism, rounded-rect + drop-shadow, colored-border-on-one-side, sparklines-as-decoration | — | Decoration noise (borders/shadows without purpose), all-caps abuse |
| **Motion** | Bounce/elastic easing, animating layout properties (width/height/padding) | — | — |
| **Academic/technical** | — | Equation overflow, broken citations, notation inconsistency, missing plotly charts, TikZ label overlap, overfull hbox, missing set.seed() | Broken cross-references, raster diagrams |
| **Compilation** | — | Compilation failure (auto-zero for QMD, TeX, R) | Compilation failure (defined in rules, not in script) |
| **Accessibility** | — | — | Missing alt text, missing speaker notes |
| **Code hygiene** | — | Hardcoded paths, missing library imports | Inline styles, raw HTML |
| **LLM design bias** | 12 explicit "AI fingerprint" tells (see §2) | — | — |
| **Cognitive load** | 8-item checklist based on Cowan's Law (≤4 items in working memory) | — | — |
| **UX writing** | Cliched loading messages ("herding pixels"), button label anti-patterns ("OK"/"Submit") | — | — |

### 1.2 Patterns impeccable-original Catches That We Don't

These are directly relevant to slide design and currently absent from our catalog:

| Pattern | Relevance to Slides | Priority |
|---------|---------------------|----------|
| **LLM design bias / "AI slop"** | High — LLM-generated slides are our primary use case | Critical |
| **Gray text on colored backgrounds** | High — semantic boxes use colored backgrounds | High |
| **Bounce/elastic easing** | Medium — fragment animations in RevealJS | Medium |
| **Gradient text** | Medium — tempting for emphasis on title slides | Medium |
| **Glassmorphism** | Low — rare in slides, but possible in custom themes | Low |
| **Inter/Roboto/Arial overuse** | Medium — we mandate Plus Jakarta Sans, but should detect if author overrides | Medium |
| **Monospace as "technical" shorthand** | Medium — code-heavy talks may abuse this | Medium |
| **Center-everything syndrome** | High — RevealJS defaults to `center: true` | High |
| **Identical repeating patterns** | Medium — repeated box structures across slides | Medium |
| **Cognitive load measurement** | High — directly applicable to slide comprehension | High |

### 1.3 Patterns paper2pr Catches That We Don't

| Pattern | Relevance | Priority |
|---------|-----------|----------|
| **Equation overflow** (single math line >120 chars) | High — academic slides use equations | High |
| **Broken citations** (cross-checking against .bib) | Medium — relevant for academic decks | Medium |
| **Notation inconsistency** | Medium — important for technical presentations | Medium |
| **Compilation as part of automated scoring** | Critical — our script doesn't compile | Critical |

---

## 2. LLM Design Bias — The Missing Category

This is the most significant gap. impeccable-original's entire thesis is that LLMs produce recognizably generic output — "AI slop." They define 12 explicit fingerprints of AI-generated work (2024-2025 era):

1. **The AI color palette** — cyan-on-dark, purple-to-blue gradients, neon accents on dark backgrounds
2. **Gradient text** on metrics or headings
3. **Dark mode with glowing accents** as the default choice
4. **Glassmorphism** — blur effects, glass cards, glow borders as decoration
5. **Hero metric layout** — big number, small label, supporting stats, gradient accent
6. **Identical card grids** — icon + heading + text, repeated endlessly
7. **Generic fonts** — Inter, Roboto, Arial, Open Sans
8. **Nested cards** — cards inside cards
9. **Rounded rectangles with generic drop shadows** — safe, forgettable
10. **Large icons with rounded corners above every heading**
11. **Monospace typography** as lazy "technical/developer" shorthand
12. **Sparklines as decoration** — tiny charts that look sophisticated but convey nothing

**The test:** "If you showed this to someone and said 'AI made this,' would they believe you immediately? If yes, that's the problem."

### Slide-Specific Adaptations

Not all 12 apply directly to RevealJS slides. Here's how they map:

| AI Fingerprint | Slide Equivalent | Should We Add? |
|----------------|-----------------|----------------|
| AI color palette | Purple/cyan/neon theme overrides | Yes — AP-D07 |
| Gradient text | Gradient text in headings/emphasis | Yes — AP-D08 |
| Dark mode default | Unnecessary dark theme when content doesn't warrant it | Maybe — context-dependent |
| Glassmorphism | Blur/glow effects in custom CSS | Yes — AP-D09 |
| Hero metric layout | "Big number" title slides | Yes — AP-D10 |
| Identical card grids | Repeated identical semantic box layouts | Yes — AP-C06 |
| Generic fonts | Non-theme fonts (Inter, Roboto) in overrides | Yes — AP-T05 |
| Nested cards | Nested semantic boxes (`.keybox` inside `.methodbox`) | Yes — AP-D11 |
| Generic drop shadows | Box-shadows on elements without purpose | Already covered by AP-D06 |
| Icons above headings | Emoji/icon above every slide heading | Yes — AP-D12 |
| Monospace shorthand | Code font for non-code content | Yes — AP-T06 |
| Sparklines as decoration | Decorative charts/diagrams that add no information | Maybe — rare in slides |

---

## 3. Automated Detection: Scoring Scripts Compared

### 3.1 Architecture Comparison

| Aspect | impeccable-quarto `quality_score.py` | paper2pr `quality_score.py` |
|--------|--------------------------------------|----------------------------|
| **Approach** | Static text analysis only | Static analysis + live compilation |
| **File types** | .qmd only | .qmd, .tex, .R |
| **Starting score** | 100 (deduct down) | 100 (deduct down) |
| **Checks** | 7 functions | 8+ detectors per file type |
| **Exit code** | 0 if ≥70, else 1 | 0 if ≥80, 1 if <80, 2 if auto-fail |
| **Output formats** | Colorized terminal | Terminal + JSON (`--json` flag) |
| **Compilation check** | No | Yes (`quarto render`, `Rscript`, `xelatex`) |
| **External deps** | None (stdlib only) | subprocess (quarto, Rscript) |
| **CI integration** | Not wired | Threshold-based commit blocking |

### 3.2 Our Script: Coverage Gap

Our `quality_score.py` implements **7 out of 21+ rules** defined in `quality-gates.md`:

| Check | In Script? | In Rules? | paper2pr? |
|-------|-----------|-----------|-----------|
| YAML frontmatter validation | Yes | Yes (CRIT-04) | — |
| Slide count bounds | Yes | — | — |
| Bullet density (>5) | Yes | Yes (MAJ-02) | — |
| Speaker notes presence | Yes | Yes (MAJ-01) | — |
| Heading hierarchy | Yes | Yes (MAJ-06) | — |
| Image alt text | Yes | Yes (MAJ-04) | — |
| Inline font-size overrides | Yes | Related to MAJ-03 | — |
| Size class overuse | Yes | — | — |
| Raw HTML detection | Yes | Related to MIN-06 | — |
| **Compilation check** | **No** | Yes (CRIT-01) | **Yes** |
| **Broken image references** | **No** | Yes (CRIT-02) | — |
| **Content overflow estimation** | **No** | Yes (CRIT-03) | — |
| **Broken cross-references** | **No** | Yes (CRIT-05) | **Yes** (citations) |
| **Pure black/white** | **No** | Yes (MAJ-05) | — |
| **OKLCH color compliance** | **No** | Yes (MAJ-07) | — |
| **Font family count** | **No** | Yes (MAJ-08) | — |
| **Generic theme detection** | **No** | Yes (MAJ-09) | — |
| **Word count per slide** | **No** | Yes (MIN-02) | — |
| **Date in frontmatter** | **No** | Yes (MIN-03) | — |
| **Image dimensions** | **No** | Yes (MIN-04) | — |
| **Raster vs SVG** | **No** | Yes (MIN-05) | — |
| **Slide separator consistency** | **No** | Yes (MIN-01) | — |
| **Equation overflow** | **No** | — | **Yes** |

**Coverage: 33% of our own rubric.** The script is useful as a fast heuristic but misses all Critical checks except frontmatter.

### 3.3 Scoring Methodology Differences

**impeccable-original** uses an additive model (score UP from 0):
- Critique: Nielsen's 10 heuristics, 0-4 each = max 40
- Audit: 5 technical dimensions, 0-4 each = max 20
- Issues rated P0–P3 (blocking → polish)

**paper2pr and impeccable-quarto** use a deductive model (score DOWN from 100):
- Fixed point deductions per issue type
- Cumulative penalties
- Auto-zero on compilation failure

The deductive model is better for objective, verifiable scoring (you can trace every point lost). The additive model is better for holistic assessment where dimensions interact. Both are valid; our project correctly uses the deductive model for automated scoring. However, we should consider adding an additive "design health" dimension similar to impeccable-original's critique score for the agent-driven review phase.

---

## 4. Severity Classification Comparison

### 4.1 Three Systems

| Level | impeccable-original | paper2pr | impeccable-quarto |
|-------|-------------------|----------|-------------------|
| **Blocking/Critical** | P0: "Prevents task completion — fix immediately" | -100 auto-fail; -15 to -20 per issue | -100 auto-fail; -8 to -15 per issue |
| **Major** | P1: "Significant difficulty or WCAG AA violation" | -2 to -5 per issue | -3 to -10 per issue |
| **Minor** | P2: "Annoyance, workaround exists" | -1 per issue | -1 to -2 per issue |
| **Polish** | P3: "No real user impact — fix if time permits" | — | — |

### 4.2 Key Differences

1. **impeccable-original has four levels** (P0–P3); we have three. The P3 "polish" level is missing from our system. This matters because some issues (like inconsistent spacing between slides) are real but too minor for "Minor (-1)." A zero-point warning tier would reduce noise.

2. **paper2pr's critical penalties are steeper**: equation overflow is -20 (vs our content overflow at -10). This reflects that academic content overflow makes equations literally unreadable.

3. **Our system lacks escalation rules**: paper2pr's orchestrator explicitly states "score regression → revert to best version." We have this in `review-protocol.md` but don't encode it in the scoring script.

---

## 5. Frontend-Specific Patterns: Slide Adaptations

### 5.1 Card Nesting → Box Nesting

impeccable-original warns against cards-inside-cards. The slide equivalent is semantic boxes inside semantic boxes:

```markdown
::: {.keybox}
**Key Finding**
::: {.methodbox}       <!-- ANTI-PATTERN: nested boxes -->
Methodology detail
:::
:::
```

**Recommendation:** Add AP-D11 "Box Nesting" — nested semantic boxes (`.keybox` inside `.methodbox`, etc.). Severity: Minor. Detection: regex for `:::.*\{\..*box\}` within another box div.

### 5.2 Gray-on-Colored → Muted Text on Semantic Boxes

impeccable-original's "gray text on colored backgrounds" maps directly to our semantic boxes. If someone uses `.subtle` (gray text) inside a `.warningbox` (red background tint), contrast fails.

**Recommendation:** Add AP-D07 "Muted Text on Colored Background" — `.subtle` or gray text inside semantic boxes. Severity: Major (accessibility). Detection: check for `.subtle` class within semantic box divs; also check theme for gray text color against box background colors.

### 5.3 Bounce Easing → Fragment Animation

impeccable-original prohibits bounce/elastic easing. Our theme defines fragment animations (`.slide-up`, `.scale-in`, `.fade-in-smooth`). While our current animations use reasonable easing, custom CSS overrides could introduce bounce.

**Recommendation:** Add guidance to theme documentation (not a scored anti-pattern, since our theme prevents it). If we add a theme customization system, add a validation rule.

### 5.4 Inter Font Overuse → Generic Font Override

Our theme mandates Plus Jakarta Sans / Source Sans 3 / JetBrains Mono. But nothing prevents a `.qmd` from overriding with:
```yaml
format:
  revealjs:
    mainfont: "Inter"
```

**Recommendation:** Add AP-T05 "Generic Font Override" — detection of Inter, Roboto, Arial, Open Sans, Lato, Montserrat in YAML frontmatter or inline CSS. Severity: Minor. This is a soft check (author may have reasons), but it should flag.

---

## 6. Enforcement Mechanisms Compared

| Mechanism | impeccable-original | paper2pr | impeccable-quarto |
|-----------|-------------------|----------|-------------------|
| **Pre-commit hooks** | None | Korean text blocker | None |
| **CI/CD** | Build + test (verifies skill compilation) | Quarto render + note stripping + deploy | None |
| **Automated scoring** | LLM-driven (`/critique`, `/audit` skills) | Python script (`quality_score.py`) + LLM agents | Python script (`quality_score.py`) + LLM agents |
| **LLM enforcement** | Mandatory `/frontend-design` before any skill; "AI Slop Detection" is first check | Rules files loaded into agent context | Rules files loaded into agent context |
| **Context persistence** | `.impeccable.md` persists design context across sessions | `MEMORY.md` + session logs + hooks | `MEMORY.md` |
| **Blocking hooks** | — | `protect-files.sh` blocks edits to protected files; `log-reminder.py` blocks stop without logging | — |
| **Compile-on-edit** | — | `verify-reminder.py` reminds to compile after edits | — |
| **Context monitoring** | — | `context-monitor.py` warns at 40/55/65/80/90% context usage | — |
| **Score thresholds** | Score bands in `/critique` (0-40) and `/audit` (0-20) | Script exit code: 0 if ≥80, 1 if <80, 2 if auto-fail | Script exit code: 0 if ≥70, 1 if <70 |

### Key Gaps in Our Enforcement

1. **No CI/CD pipeline.** Neither compilation nor scoring runs automatically. Every quality check depends on manual invocation or agent initiative.

2. **No pre-commit hooks.** paper2pr blocks Korean text; impeccable-original doesn't need hooks (LLM-enforced). We should at minimum hook `quality_score.py` into pre-commit.

3. **No compile-on-edit reminder.** paper2pr's `verify-reminder.py` nudges the agent to compile after file edits. We rely on the verifier agent, but only during formal review cycles.

4. **Script threshold mismatch.** Our script exits successfully at 70, but our rules say 80 is the minimum for "Draft" quality. The script should gate at 80 to match.

5. **No protected files.** paper2pr blocks edits to `Bibliography_base.bib` and `settings.json`. We should protect `themes/impeccable.scss` and `.claude/rules/` from accidental agent modification.

---

## 7. Cognitive Load — The Missing Framework

impeccable-original includes a cognitive load framework from `critique/reference/cognitive-load.md`:

- **Three types:** intrinsic (inherent complexity), extraneous (bad design), germane (learning-productive)
- **8-item checklist** with scoring (0-1 failures = good, 4+ = critical)
- **Cowan's Law:** humans hold ≤4 items in working memory at once
- **5 test personas** for evaluating from different perspectives

This is highly applicable to slide design:
- Our "one idea per slide" rule is a cognitive load principle, but we don't frame it that way
- Our "≤5 bullets" rule could be strengthened to "≤4 items" per Cowan's Law
- We have no persona-based evaluation (e.g., "would a confused first-timer understand this slide?")

**Recommendation:** Add a cognitive load dimension to our agent-driven review (not the script). The `slide-critic` agent should evaluate against 3-4 test personas and flag slides that exceed 4 distinct information items.

---

## 8. Gap Analysis: Uncovered Anti-Patterns

### 8.1 Patterns Neither Repo Covers (Slide-Specific)

These are anti-patterns specific to RevealJS slide design that we've identified through this analysis:

| Proposed ID | Pattern | Description | Severity |
|-------------|---------|-------------|----------|
| AP-C07 | **Transition Abuse** | Excessive or inconsistent slide transitions (fade, slide, zoom mixed randomly) | Minor |
| AP-C08 | **Fragment Overload** | >5 progressive disclosure steps on a single slide | Major |
| AP-C09 | **Slide Count Extremes** | <5 or >40 slides for a standard presentation | Minor |
| AP-D13 | **Aspect Ratio Mismatch** | Slides designed for 16:9 but presented at 4:3 (or vice versa) | Major |
| AP-D14 | **Screenshot-as-Content** | Full-screen screenshot used instead of recreating content natively | Minor |
| AP-T07 | **Code Block Overflow** | Code blocks wider than slide bounds without wrapping or `.smaller` | Major |
| AP-X06 | **Dead Fragments** | Fragment classes on elements that don't benefit from progressive disclosure | Minor |
| AP-X07 | **Embed-Resources False** | `embed-resources: false` in YAML when deck should be portable | Minor |

### 8.2 Summary of All Recommended Additions

**From impeccable-original (adapt for slides):**
- AP-D07: Muted Text on Colored Background (Major)
- AP-D08: Gradient Text (Minor)
- AP-D09: Glassmorphism / Blur Effects (Minor)
- AP-D10: Hero Metric Layout (Minor)
- AP-D11: Nested Semantic Boxes (Minor)
- AP-D12: Icon/Emoji Above Every Heading (Minor)
- AP-T05: Generic Font Override (Minor)
- AP-T06: Monospace for Non-Code Content (Minor)
- AP-LLM01: AI Slop Composite Check (Major) — the meta-pattern encompassing multiple tells

**From paper2pr (adapt for our context):**
- AP-X08: Equation Overflow (Critical) — single math line >120 chars
- AP-X09: Broken Citation (Critical) — citation key not in bibliography

**Novel (slide-specific gaps):**
- AP-C06: Identical Repeating Structure (Minor)
- AP-C07: Transition Abuse (Minor)
- AP-C08: Fragment Overload (Major)
- AP-T07: Code Block Overflow (Major)

---

## 9. Recommendations

### 9.1 Immediate (High Impact, Low Effort)

1. **Fix script threshold**: Change `quality_score.py` exit gate from 70 to 80 to match our quality-gates.md rules.

2. **Add compilation check to script**: Call `quarto render` (like paper2pr does) and auto-zero on failure. This is the most impactful single improvement — CRIT-01 is currently unenforceable by automation.

3. **Add pure black/white detection**: Simple regex for `#000`, `#fff`, `rgb(0,0,0)`, `rgb(255,255,255)` in `.qmd` and `.scss` files. Currently MAJ-05 exists in rules but has no automated detection.

4. **Add word count per slide**: Count words in body text (excluding headings, notes, code) and flag >40 words. MIN-02 is defined but unimplemented.

### 9.2 Short-Term (High Impact, Medium Effort)

5. **Add "AI Slop" detection category**: Create AP-LLM anti-pattern class. Start with the most slide-relevant tells: gradient text in `.qmd`/`.scss`, generic font overrides in YAML, nested semantic boxes, and the "AI color palette" (high-chroma cyan/purple in non-OKLCH color space).

6. **Wire quality_score.py into pre-commit**: Create `.git/hooks/pre-commit` that runs the scoring script on staged `.qmd` files and blocks commits below 80.

7. **Add CI/CD pipeline**: GitHub Actions workflow that runs `quarto render` on all examples and `quality_score.py` on all `.qmd` files.

8. **Implement broken-reference detection**: Parse `.qmd` for `@fig-`, `@tbl-`, `@sec-` references and verify they resolve. CRIT-05 is defined but unimplemented.

### 9.3 Medium-Term (Medium Impact, Higher Effort)

9. **Add cognitive load scoring to slide-critic agent**: Incorporate Cowan's Law (≤4 items), the three cognitive load types, and 2-3 test personas into the adversarial review cycle.

10. **Add gray-on-colored background detection**: Requires analyzing the theme's semantic box background colors against text colors used within those boxes. Complex but important for accessibility.

11. **Create a "design health" additive score**: Supplement the deductive score (100 → down) with a positive assessment (0 → up) covering design distinctiveness, cognitive load, and narrative arc — similar to impeccable-original's 40-point heuristic score.

12. **Add Claude Code hooks**: Implement `verify-reminder` (compile after edit), `protect-files` (block theme/rules edits), and `context-monitor` (warn on high context usage) following paper2pr's model.

### 9.4 Long-Term (Strategic)

13. **Unify scoring models**: Consider whether the deductive (our script) and additive (agent review) scores should be combined into a single composite quality score, or kept separate for different purposes.

14. **Build a "slide fingerprint" system**: Automated detection of repeated structural patterns across slides (impeccable-original's "identical card grids" adapted for slide boxes). This requires comparing slide ASTs, not just text.

15. **Create a theme validator**: A standalone tool that checks `.scss` themes for OKLCH compliance, contrast ratios, font stack validity, and anti-pattern color combinations — independent of any specific `.qmd` file.

---

## 10. Summary Matrix

| Dimension | impeccable-original | paper2pr | impeccable-quarto | Gap Severity |
|-----------|-------------------|----------|-------------------|-------------|
| Anti-pattern breadth | 25+ patterns | 10+ patterns | 15 patterns | Medium — missing LLM bias, motion, cognitive load |
| Automated detection | LLM-only (no script) | Script + compilation + LLM | Script (partial) + LLM | High — script covers 33% of rubric |
| Compilation check | N/A | Yes (in script) | No (in script) | Critical |
| CI/CD | Build/test | Render + deploy | None | High |
| Pre-commit hooks | None | Korean text block | None | Medium |
| LLM enforcement | Strong (mandatory skill chain) | Strong (rules + hooks) | Medium (rules only) | Medium |
| Cognitive load | Full framework (8-item checklist + personas) | None | None | Medium |
| AI slop detection | Centerpiece (12 tells, scored 0-4) | None | None | High for our use case |
| Score model | Additive (0→40) | Deductive (100→0) | Deductive (100→0) | N/A (different by design) |
| Threshold enforcement | Score bands | Exit codes + commit blocking | Exit codes only | Medium |
| Session continuity | `.impeccable.md` persistence | Hooks + logs + pre-compact | Memory system | Low |

**Overall assessment:** Our anti-pattern catalog and quality rules are well-designed but under-automated. The biggest gaps are (1) no LLM design bias detection, (2) script covers only 33% of our own rubric, (3) no CI/CD enforcement, and (4) no compilation check in automated scoring. Addressing items 1-4 from §9.1 would close the most critical gaps with minimal effort.
