---
name: review-slides
description: "Full multi-agent review: typography + layout + content + pedagogy"
user-invocable: true
argument-hint: "[file]"
---

# /review-slides — Full Multi-Agent Review

[MANDATORY PREPARATION]
- Read `.claude/rules/review-protocol.md` for the review orchestration protocol
- Read `.claude/rules/quality-gates.md` for scoring criteria
- Read `.claude/rules/design-standards.md` and `.claude/rules/anti-patterns.md`
- Read the target `.qmd` file completely
- This is an orchestration skill — it delegates to specialist agents

[IMPLEMENTATION STEPS]
1. **Phase 1: Parallel Diagnostic** (run concurrently)
   - Invoke `slide-critic` agent for adversarial UX/design review
   - Invoke `layout-auditor` agent for spatial analysis
   - Collect both reports before proceeding

2. **Phase 2: Specialist Review** (run concurrently)
   - Invoke `typography-reviewer` agent for font/type assessment
   - Invoke `verifier` agent for compilation and rendering check
   - Collect both reports before proceeding

3. **Phase 3: Synthesis**
   - Merge all four reports into a unified review
   - De-duplicate overlapping findings
   - Prioritize issues: Critical > Major > Minor
   - Calculate composite score using `quality-gates.md` deduction table

4. **Phase 4: Recommendations**
   - Generate a prioritized action plan
   - Map each issue to the appropriate fix skill:
     - Compilation/ref issues → `/normalize-slides`
     - Typography issues → `/typeset-slides`
     - Color issues → `/colorize-slides`
     - Layout issues → `/arrange-slides`
     - Content density → `/distill-slides`
     - Text clarity → `/clarify-slides`
     - Needs more impact → `/bolder-slides`
     - Too busy → `/quieter-slides`
   - Estimate effort: Quick fix / Moderate / Significant rework

[OUTPUT FORMAT]
```
## Comprehensive Review: <filename>
**Composite Score: XX/100** — <Draft|Presentable|Excellent>

### Executive Summary
Brief 2-3 sentence overview

### Critical Issues (blocks presenting)
1. Issue — Source: <agent> — Fix: <skill> — Deduction: -XX

### Major Issues (should fix before presenting)
1. Issue — Source: <agent> — Fix: <skill> — Deduction: -XX

### Minor Issues (polish items)
1. Issue — Source: <agent> — Fix: <skill> — Deduction: -XX

### Strengths
- What's working well

### Recommended Action Plan
1. First: Run `/normalize-slides` to fix critical issues
2. Then: Run `/typeset-slides` for typography fixes
3. Then: ...

### Agent Reports
<collapsed details of each agent's full report>
```

[ANTI-PATTERNS TO AVOID]
- Do NOT skip any review phase — all four agents must weigh in
- Do NOT edit files during review — this is diagnostic only
- Do NOT let one agent's score override the composite calculation
- Do NOT provide vague recommendations — every issue maps to a fix skill

[QUALITY CHECKS]
- All four review agents produced reports
- Issues are properly categorized and de-duplicated
- Score is mathematically consistent with deductions
- Every issue has a recommended fix skill
- Action plan is prioritized and actionable
