---
name: polish-slides
description: "Final quality pass: micro-details, consistency, spacing harmony"
user-invocable: true
argument-hint: "[file]"
---

# /polish-slides — Final Quality Polish

[MANDATORY PREPARATION]
- Load design context: Read `.claude/skills/slide-design.md` and follow Steps 1-3 to establish design context
- Read `.claude/rules/design-standards.md` and `.claude/rules/anti-patterns.md`
- Read `.impeccable-quarto.md` if it exists for style preferences
- Read the target `.qmd` file completely
- This skill assumes major issues are already fixed — it handles micro-details

[IMPLEMENTATION STEPS]
1. **Consistency Pass**
   - Standardize heading capitalization (Title Case or Sentence case — pick one, apply everywhere)
   - Normalize bullet point punctuation (all with periods, or none)
   - Ensure consistent use of em-dashes, en-dashes, and hyphens
   - Standardize quote marks (curly vs straight)

2. **Spacing Harmony**
   - Verify consistent vertical rhythm between elements
   - Check that padding/margins follow a consistent scale (e.g., 8px base)
   - Ensure whitespace around images is balanced
   - Remove orphan lines (single words on the last line of a paragraph)

3. **Typography Micro-Details**
   - Check for proper ligatures where supported
   - Ensure code blocks use a monospace font consistently
   - Verify emphasis (bold/italic) is used sparingly and purposefully
   - Check for widows and orphans in text blocks

4. **Color Consistency**
   - Verify accent colors are used consistently for the same semantic purpose
   - Check that linked text color is distinct and consistent
   - Ensure syntax highlighting theme matches the presentation palette

5. **Speaker Notes Quality**
   - Ensure notes exist for all substantive slides
   - Check notes provide talking points, not just a repeat of slide text
   - Verify timing cues are present for longer sections

6. **Final Compilation**
   - Render and verify no warnings
   - Check that the polished version maintains the original intent

[ANTI-PATTERNS TO AVOID]
- Do NOT make major structural changes — this is for micro-details only
- Do NOT spend time on slides that need `/normalize-slides` first
- Do NOT add decorative elements — polish means refine, not embellish
- Do NOT change the content meaning while fixing style

[QUALITY CHECKS]
- All text follows consistent capitalization and punctuation rules
- Spacing is harmonious and follows a consistent scale
- No orphan lines or widows remain
- Speaker notes are present and useful for all key slides
- The file compiles cleanly
