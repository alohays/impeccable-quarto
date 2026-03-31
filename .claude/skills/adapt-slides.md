---
name: adapt-slides
description: "Adapt slides to different template/context (academic→corporate, etc.)"
user-invocable: true
argument-hint: "[file] [template]"
---

# /adapt-slides — Context & Template Adaptation

[MANDATORY PREPARATION]
- Read `.claude/rules/design-standards.md` for design standards
- Read `.claude/rules/anti-patterns.md` for anti-patterns
- Read `.impeccable-quarto.md` if it exists for target context preferences
- Read the source `.qmd` file completely
- Understand the target context: academic → corporate, corporate → casual, etc.
- If a template file is specified, read it to understand the target format

[IMPLEMENTATION STEPS]
1. **Context Analysis**
   - Identify source context: academic, corporate, startup, educational, personal
   - Identify target context and its conventions:
     - **Academic**: detailed methodology, citations, formal tone, data-heavy
     - **Corporate**: executive summary, KPIs, action items, branded
     - **Startup**: bold visuals, storytelling, minimal text, high energy
     - **Educational**: progressive complexity, examples, exercises
     - **Conference talk**: engaging hook, clear narrative, memorable takeaway

2. **Tone Adaptation**
   - Adjust language formality to match target context
   - Rewrite headings to match conventions (academic: descriptive; corporate: action-oriented)
   - Adjust technical depth (simplify for executives, add detail for researchers)
   - Update speaker notes for the new audience

3. **Visual Adaptation**
   - Swap color palette to match target brand/context
   - Adjust typography: serif for academic, sans-serif for corporate/startup
   - Modify layout density: academic can be denser; startup should be sparser
   - Update visual style: academic (clean, data-focused) vs. startup (bold, image-heavy)

4. **Content Restructuring**
   - Reorder slides to match target context expectations:
     - Academic: Background → Method → Results → Discussion
     - Corporate: Summary → Problem → Solution → ROI → Next Steps
     - Startup: Hook → Pain Point → Solution → Traction → Ask
   - Add/remove slides as needed for the target structure
   - Ensure narrative arc suits the new audience

5. **Template Application**
   - If a specific template is provided, apply its SCSS theme
   - Match the template's grid, spacing, and typography conventions
   - Apply template-specific components (branded headers, footers, logos)
   - Preserve template's slide master conventions

6. **Validate**
   - Compile with `quarto render`
   - Verify the adapted version is appropriate for the target context
   - Check all design standards are met in the new context
   - Ensure no source content was lost without intent

[ANTI-PATTERNS TO AVOID]
- Do NOT just change colors and call it "adapted"
- Do NOT lose substantive content during adaptation
- Do NOT apply corporate polish to academic content that needs technical depth
- Do NOT assume all contexts want the same level of simplification
- Do NOT mix conventions from source and target contexts

[QUALITY CHECKS]
- Tone matches the target context
- Visual style is appropriate for the target audience
- Content depth is adjusted for the target audience
- Slide structure follows target context conventions
- All design standards are maintained
- File compiles cleanly
