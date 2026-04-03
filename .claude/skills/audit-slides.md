---
name: audit-slides
description: "Technical quality audit: overflow, compilation, broken refs, image resolution, accessibility"
user-invocable: true
argument-hint: "[file]"
---

# /audit-slides — Technical Quality Audit

[MANDATORY PREPARATION]
- Load design context: Read `.claude/skills/slide-design.md` and follow Steps 1-3 to establish design context
- Read `.claude/rules/design-standards.md` and `.claude/rules/anti-patterns.md` for reference criteria
- Read `.claude/rules/quality-gates.md` for the scoring/deduction table
- Gather context: identify the target `.qmd` file and any associated theme/assets
- If no file argument given, find all `.qmd` files in the project and ask which to audit

[IMPLEMENTATION STEPS]
1. **Compilation Check**
   - Run `quarto render <file>` and capture all warnings/errors
   - A compilation failure is an automatic -100 deduction — flag immediately

2. **Overflow Detection**
   - Scan each slide for content that may overflow its container
   - Check for overly long text blocks, excessive bullet lists (>5 items), wide images without max-width
   - Flag any slide with `font-size` below 20px

3. **Broken References**
   - Check all internal cross-references (`@fig-`, `@tbl-`, `@sec-`)
   - Verify all image paths resolve to existing files
   - Check all hyperlinks for valid format (not necessarily live — just well-formed)

4. **Image Quality**
   - Verify images exist at referenced paths
   - Check for missing `alt` text (accessibility)
   - Flag images without explicit width/height that could cause layout shifts
   - Recommend SVG over raster for diagrams

5. **Accessibility Audit**
   - Verify all images have descriptive `alt` attributes
   - Check color contrast ratios meet WCAG AA (4.5:1 for text, 3:1 for large text)
   - Ensure heading hierarchy is logical (no skipping levels)
   - Check for content that relies solely on color to convey meaning

6. **Structure Check**
   - Validate YAML frontmatter is well-formed
   - Check slide separators are consistent (`---` or `##`)
   - Verify speaker notes syntax is correct (`::: {.notes}`)

7. **Score Calculation**
   - Start at 100, apply deductions per `quality-gates.md`
   - Produce a categorized issue list: Critical / Major / Minor

[OUTPUT FORMAT]
```
## Audit Report: <filename>
**Score: XX/100** — <Draft|Presentable|Excellent>

### Critical Issues (must fix)
- [ ] Issue description — Slide N — Deduction: -XX

### Major Issues (should fix)
- [ ] Issue description — Slide N — Deduction: -XX

### Minor Issues (nice to fix)
- [ ] Issue description — Slide N — Deduction: -XX

### Summary
- Total slides: N
- Slides with issues: N
- Compilation: ✅/❌
- Accessibility: N issues
```

[ANTI-PATTERNS TO AVOID]
- Do NOT modify any files — this is a read-only diagnostic skill
- Do NOT skip the compilation check even if it seems slow
- Do NOT report subjective design preferences as audit failures
- Do NOT conflate technical issues with design critique (that's `/critique-slides`)

[QUALITY CHECKS]
- Every reported issue must reference a specific slide number
- Every deduction must match the `quality-gates.md` deduction table
- The score must be mathematically consistent with listed deductions
- The report must be actionable — every issue should suggest a fix direction
