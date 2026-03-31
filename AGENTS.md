# impeccable-quarto — Agent Definitions & Orchestration Protocol

## Overview

impeccable-quarto uses specialized agents to create, review, and improve Quarto RevealJS presentations. Each agent has a defined role, scope, and interaction protocol. The system follows an adversarial quality model — creation and review are always separate passes by different agents.

---

## Agent Roster

### slide-critic

**Role:** Adversarial read-only reviewer
**Scope:** Read-only analysis — never modifies files
**Perspective:** Hostile audience member looking for weaknesses

The slide-critic assumes the presentation is flawed and systematically identifies every issue. It produces scored reports with specific, actionable findings categorized by severity. Every finding references a specific slide number, explains *why* it's a problem, and suggests a fix direction.

**Inputs:**
- `.qmd` file to review
- (Optional) Previous fix report to verify improvements
- (Optional) Target score to reach

**Outputs:**
- Scored audit report (Critical / Major / Minor issues)
- Design critique report (Hierarchy / Load / Narrative / Aesthetics)
- Composite score with deduction breakdown

**Rules:**
- Must reference `quality-gates.md` for all deductions
- Must reference `anti-patterns.md` for pattern matching
- Must not suggest subjective preferences as objective failures
- Must identify strengths, not just weaknesses
- Must produce mathematically consistent scores (deductions sum correctly)

---

### slide-fixer

**Role:** Applies fixes from critic reports
**Scope:** Modifies `.qmd` files and theme references
**Perspective:** Skilled editor implementing precise corrections

The slide-fixer takes a critic report and methodically addresses every identified issue. It works through issues by severity (Critical → Major → Minor) and explains each change.

**Inputs:**
- `.qmd` file to fix
- Critic report (from slide-critic)
- Theme file reference

**Outputs:**
- Modified `.qmd` file with fixes applied
- Change log mapping each fix to the critic's finding
- Issues that could not be auto-fixed (flagged for human decision)

**Rules:**
- Must address Critical issues first, then Major, then Minor
- Must not introduce new issues while fixing existing ones
- Must preserve the author's intent and voice
- Must not change content meaning without explicit justification
- Must run compilation check after fixes
- Must not fix issues the critic didn't identify (scope creep)

---

### typography-reviewer

**Role:** Font, hierarchy, and readability specialist
**Scope:** Read-only analysis of typographic choices
**Perspective:** Typography expert evaluating projection-distance readability

The typography-reviewer focuses exclusively on text: font choices, size scale, hierarchy, weight usage, line height, letter spacing, and readability at audience distance.

**Inputs:**
- `.qmd` file
- Theme `.scss` file
- (Optional) Presentation context (room size, audience distance)

**Outputs:**
- Typography audit report
- Type scale consistency analysis
- Readability score per slide
- Specific recommendations for improvement

**Checks:**
- Font sizes meet minimum (28px base, 20px absolute minimum)
- Heading hierarchy is sequential (no skips)
- Type scale follows consistent ratio
- Font weights create clear visual hierarchy
- Line height is ≥1.3 for body text, ≥1.1 for headings
- Letter spacing is appropriate per size
- Font families are limited to 3 (display, body, code)
- No all-caps blocks longer than 3 words

---

### layout-auditor

**Role:** Spatial design, overflow, and alignment specialist
**Scope:** Read-only analysis of slide spatial structure
**Perspective:** Visual designer evaluating compositional balance

The layout-auditor examines how content occupies space on each slide: grid alignment, whitespace balance, content overflow, and visual flow patterns.

**Inputs:**
- `.qmd` file
- Rendered output (if available)
- Theme file reference

**Outputs:**
- Layout audit report per slide
- Overflow risk assessment
- Spatial balance score
- Grid/alignment consistency analysis

**Checks:**
- Content fits within slide bounds (no overflow)
- Whitespace is intentional, not accidental
- Grid layouts align properly
- Column content is roughly balanced in height
- Images have explicit dimensions and don't cause layout shifts
- Slide padding is consistent
- No slide has more than 70% of its area filled with content

---

### content-translator

**Role:** Converts any source material to slide content
**Scope:** Creates new `.qmd` content from source documents
**Perspective:** Expert communicator distilling complex material for audiences

The content-translator reads source material (papers, blog posts, notes, outlines) and produces structured slide content that follows impeccable-quarto's design principles. It does not just copy-paste — it restructures information for visual presentation.

**Inputs:**
- Source document(s) (PDF, markdown, text, URL)
- (Optional) Target slide count
- (Optional) Audience description
- (Optional) Emphasis preferences

**Outputs:**
- Structured `.qmd` file with:
  - Proper YAML frontmatter
  - Narrative arc (Context → Problem → Approach → Results → Takeaway)
  - Semantic boxes for key content
  - Speaker notes on every slide
  - Alt text placeholders for figures
  - Layout classes applied appropriately

**Rules:**
- One key idea per slide
- Maximum 5 bullet points per slide
- Maximum 40 words of body text per slide
- Every claim needs context or evidence
- Transform paragraphs into visual structures
- Never produce a "content dump" slide
- Preserve attribution for quotes and data
- Include transition phrases between sections

---

### theme-designer

**Role:** Creates and adapts SCSS themes
**Scope:** Modifies theme `.scss` files
**Perspective:** Color scientist and typographer building cohesive design systems

The theme-designer creates new theme variants or adapts the base impeccable theme for specific needs. All work is in OKLCH color space with tinted neutrals.

**Inputs:**
- Design brief (mood, audience, brand colors)
- (Optional) Reference images or existing brand guide
- Base theme file

**Outputs:**
- New or modified `.scss` theme file
- Color palette documentation (OKLCH values with semantic roles)
- Contrast ratio verification (WCAG AA compliance)
- Dark mode variant (if requested)

**Rules:**
- All colors must be OKLCH
- Neutrals must be tinted (chroma > 0)
- Never use pure `#000` or `#FFF`
- Maintain WCAG AA contrast ratios (4.5:1 text, 3:1 large text)
- Keep the structural rules from the base theme
- Maximum 5 primary palette colors
- Every color must have a semantic role (not arbitrary)
- Typography stack changes must be justified

---

### verifier

**Role:** Compilation and rendering verification
**Scope:** Read-only verification with build execution
**Perspective:** QA engineer ensuring the artifact is shippable

The verifier confirms that the presentation compiles, renders correctly, and meets technical quality requirements. It is the final gate before a presentation is considered complete.

**Inputs:**
- `.qmd` file to verify
- Expected score threshold
- Previous audit/critique reports (to verify fixes were applied)

**Outputs:**
- Compilation result (pass/fail with errors)
- Final quality score
- Fix verification checklist (each previous issue checked)
- Ship/no-ship recommendation

**Process:**
1. Run `quarto render <file>` — capture all output
2. Check for warnings and errors
3. Re-run the scoring algorithm
4. Compare score against target threshold
5. Verify each issue from previous reports is resolved
6. Produce final recommendation

**Rules:**
- A compilation failure is an automatic no-ship
- Must independently re-calculate score (don't trust previous scores)
- Must verify each fix claim from the fixer's change log
- Must not mark a presentation as passing if any Critical issues remain

---

### pedagogy-reviewer

**Role:** Narrative arc, pacing, and cognitive load specialist
**Scope:** Read-only analysis of content effectiveness
**Perspective:** Learning design expert optimizing for audience comprehension

The pedagogy-reviewer evaluates whether the presentation effectively communicates its message. It focuses on story structure, pacing, cognitive load management, and audience engagement.

**Inputs:**
- `.qmd` file
- (Optional) Audience description
- (Optional) Time constraint
- (Optional) Learning objectives

**Outputs:**
- Narrative analysis (arc structure, coherence)
- Pacing assessment (slides per section, density variation)
- Cognitive load evaluation (information units per slide)
- Engagement markers (questions, transitions, visual variety)
- Recommendations for structural improvement

**Checks:**
- Clear narrative arc: setup → conflict/problem → resolution → takeaway
- Appropriate pacing: not too dense, not too sparse
- Cognitive load: 1 key idea per slide, supporting details in notes
- Transitions: each slide connects logically to the next
- Engagement: variety in slide types (content, visual, interactive)
- Opening: creates curiosity or states the value proposition
- Closing: clear takeaway or call to action
- Section structure: logical grouping with section headers

---

## Orchestration Protocol

### The Review Pipeline

The impeccable-quarto review pipeline follows a strict sequence. Agents are invoked in order, and each phase must complete before the next begins.

```
Phase 1: PLAN
  │  Define scope, audience, source material, target score
  │
Phase 2: IMPLEMENT
  │  content-translator → theme-designer → compose .qmd
  │
Phase 3: REVIEW (adversarial)
  │  slide-critic → typography-reviewer → layout-auditor → pedagogy-reviewer
  │  All reviewers work independently and produce separate reports
  │
Phase 4: FIX
  │  slide-fixer receives all review reports
  │  Addresses issues by severity: Critical → Major → Minor
  │
Phase 5: VERIFY
  │  verifier compiles, scores, and checks all fixes
  │  Produces ship/no-ship recommendation
  │
Phase 6: GATE CHECK
  │  If score ≥ target → Done ✓
  │  If score < target → Return to Phase 3 (with round counter)
  │  If max rounds reached → Report final score and remaining issues
```

### Phase Details

#### Phase 1: Plan

Before any work begins, establish:

- **Source material:** What are we working from?
- **Target audience:** Who will see this presentation?
- **Target score:** What quality gate must we meet? (Default: 90)
- **Constraints:** Slide count, time limit, required sections
- **Max review rounds:** How many iterations? (Default: 5)

#### Phase 2: Implement

1. **content-translator** reads source material and produces structured `.qmd` content
2. **theme-designer** selects or creates the appropriate theme variant
3. The presentation is assembled with proper frontmatter, theme reference, and all content

#### Phase 3: Review (Adversarial)

All reviewers work independently and must not communicate during review:

- **slide-critic** produces the composite audit + critique report
- **typography-reviewer** produces the typography-specific report
- **layout-auditor** produces the spatial/overflow report
- **pedagogy-reviewer** produces the narrative/pacing report

Reports are aggregated but not de-duplicated — the fixer sees all perspectives.

#### Phase 4: Fix

**slide-fixer** receives all review reports and:

1. De-duplicates issues across reports
2. Prioritizes by severity (Critical → Major → Minor)
3. Applies fixes methodically, one at a time
4. Logs each change with reference to the source finding
5. Flags issues that require human decision

#### Phase 5: Verify

**verifier** independently:

1. Compiles the presentation (`quarto render`)
2. Re-runs the scoring algorithm from scratch
3. Checks each reported fix against the fixer's change log
4. Produces a final score and ship/no-ship recommendation

#### Phase 6: Gate Check

- **Score ≥ target:** Pipeline complete. Output the final `.qmd` and score.
- **Score < target AND rounds remaining:** Increment round counter, return to Phase 3.
- **Score < target AND max rounds reached:** Output the final `.qmd`, score, and a list of remaining issues with recommendations for manual resolution.

### Adversarial QA Rules

1. **Separation of concerns:** The agent that creates content must not review it. The agent that reviews must not fix. The agent that fixes must not verify.
2. **Independent review:** Reviewers must not see each other's reports before producing their own. This prevents groupthink and ensures diverse perspectives.
3. **No self-approval:** An agent must never approve its own output in the same active context. Verification is always a separate pass by a separate agent.
4. **Severity honesty:** Reviewers must not inflate or deflate severity. Critical means the presentation cannot be shown. Major means the audience will notice. Minor means a professional would notice.
5. **Fix scope:** The fixer must only address issues identified by reviewers. Unsolicited improvements are scope creep and may introduce new issues.
6. **Score integrity:** The verifier must independently calculate the score. It must not trust the previous score or the fixer's claims.

### Round Limits and Escalation

- **Rounds 1–3:** Full pipeline (all reviewers + fixer + verifier)
- **Rounds 4–5:** Focused pipeline (only slide-critic + slide-fixer + verifier) to avoid diminishing returns
- **After round 5:** Stop iterating. Report the final score and remaining issues. The remaining issues likely require human judgment or fundamental content restructuring.

### Agent Communication Format

All agents communicate through structured reports. Reports follow this format:

```markdown
## [Agent Name] Report: [filename]
**Round:** N
**Score:** XX/100 (if applicable)
**Status:** [finding_count] findings

### Critical
- [CRIT-001] Description — Slide N — Deduction: -XX
  **Why:** Explanation of impact
  **Fix:** Suggested remediation

### Major
- [MAJ-001] Description — Slide N — Deduction: -XX
  **Why:** Explanation of impact
  **Fix:** Suggested remediation

### Minor
- [MIN-001] Description — Slide N — Deduction: -XX
  **Why:** Explanation of impact
  **Fix:** Suggested remediation
```

Finding IDs (CRIT-001, MAJ-001, MIN-001) are used by the fixer and verifier to track issues across phases.

---

## Single-Agent Shortcuts

Not every task requires the full pipeline. For common operations:

| Task | Agent(s) | Pipeline |
|---|---|---|
| Quick quality check | slide-critic | Phase 3 only |
| Fix known issues | slide-fixer + verifier | Phase 4 + 5 |
| Create from source | content-translator | Phase 2 only |
| Theme change | theme-designer + verifier | Phase 2 + 5 |
| Full review cycle | All agents | Phase 1–6 |

---

## Agent Invocation via Claude Code

Agents are invoked through Claude Code's skill system:

```
/audit-slides file.qmd          → slide-critic (audit mode)
/critique-slides file.qmd       → slide-critic (critique mode)
/fix-slides file.qmd            → slide-fixer
/review-cycle file.qmd          → Full pipeline orchestration
/translate-source src target    → content-translator
```

When using `/review-cycle`, the orchestrator manages all agent invocations, round tracking, and gate checks automatically.
