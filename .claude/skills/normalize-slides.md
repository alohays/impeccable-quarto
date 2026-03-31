---
name: normalize-slides
description: "Fix issues from audit: alignment, spacing, broken refs, overflow"
user-invocable: true
argument-hint: "[file]"
---

# /normalize-slides — Fix Audit Issues

[MANDATORY PREPARATION]
- Run `/audit-slides <file>` first (or read an existing audit report) to identify issues
- Read `.claude/rules/design-standards.md` for correct values
- Read the target `.qmd` file completely before making changes
- Back up context: note the current slide count and structure

[IMPLEMENTATION STEPS]
1. **Fix Critical Issues First**
   - Resolve compilation errors (malformed YAML, broken syntax)
   - Fix broken image paths and cross-references
   - Correct any slide separator issues

2. **Fix Overflow**
   - Reduce text on slides exceeding content bounds
   - Add explicit `max-width` / `max-height` to oversized images
   - Split overstuffed slides into multiple slides if needed
   - Ensure no font-size drops below 20px

3. **Fix Alignment & Spacing**
   - Standardize margins and padding across slides
   - Align elements to a consistent grid
   - Normalize whitespace between sections
   - Ensure consistent column widths in multi-column layouts

4. **Fix References**
   - Correct broken cross-references
   - Fix malformed URLs
   - Update image paths that have moved

5. **Fix Accessibility**
   - Add missing `alt` text to images
   - Ensure heading levels don't skip
   - Add `::: {.notes}` blocks where speaker notes are needed but missing

6. **Validate Fixes**
   - Run `quarto render <file>` to confirm compilation
   - Re-check that no new issues were introduced

[ANTI-PATTERNS TO AVOID]
- Do NOT redesign or restyle — only fix identified issues
- Do NOT remove content to "fix" overflow without preserving the information elsewhere
- Do NOT change the author's intended message or structure
- Do NOT fix minor issues before critical ones

[QUALITY CHECKS]
- All critical issues from the audit report are resolved
- The file compiles without errors
- No new issues were introduced by the fixes
- The slide count and overall structure are preserved (unless splitting was necessary)
