---
name: bolder-slides
description: "Amplify safe/boring slides with more visual impact"
user-invocable: true
argument-hint: "[file]"
---

## MANDATORY PREPARATION

Before proceeding with any work:

1. **Read `/slide-design`** to load the active design context, theme reference, and AI Slop Test.
2. **Check `.impeccable-quarto.md`** in the project root for project-specific overrides.
   - If it does NOT exist: note that defaults will be used. Suggest `/teach-style` to the user.
3. **Verify** a custom theme is specified in the target `.qmd` YAML frontmatter.

Do NOT proceed without confirming design context is active.

# /bolder-slides — Visual Impact Amplification

[MANDATORY PREPARATION]
- Load design context: Read `.claude/skills/slide-design.md` and follow Steps 1-3 to establish design context
- Read `.claude/rules/design-standards.md` for design boundaries
- Read `.claude/rules/anti-patterns.md` to know the limits of "bold"
- Read `.impeccable-quarto.md` if it exists for style preferences
- Read the target `.qmd` file completely
- Identify slides that feel "safe" or generic — these are the targets

[IMPLEMENTATION STEPS]
1. **Identify Flat Slides**
   - Flag slides with: plain text only, default styling, no visual anchor
   - Flag slides that look like a word processor document
   - Flag title slides that are just centered text on a blank background
   - Flag section breaks with no visual identity

2. **Add Visual Anchors**
   - Every slide should have at least one non-text visual element
   - Options: relevant image, icon, diagram, chart, decorative shape, colored block
   - Use background images with overlay for impact slides (key messages, section titles)
   - Add subtle decorative elements: accent lines, geometric shapes, gradient panels

3. **Typography Bold Moves**
   - Use large display type for key statements (48-72px)
   - Apply font weight contrast: light body + bold heading
   - Use color-highlighted keywords within text
   - Pull quotes: extract key phrases and display them large

4. **Color Boldness**
   - Use full-bleed background colors for emphasis slides
   - Apply color blocking: split slides into colored sections
   - Use dark backgrounds with light text for impact slides
   - Introduce an accent color more aggressively for visual punch

5. **Layout Boldness**
   - Use asymmetric layouts instead of centered-everything
   - Try full-bleed images with text overlay
   - Use dramatic whitespace (large empty areas as design elements)
   - Apply the "billboard test": would this slide work at highway speed?

6. **Moderation Check**
   - After boldening, check against anti-patterns (not too many colors, not too busy)
   - Ensure readability is maintained
   - Keep consistency — bold doesn't mean chaotic
   - Verify the bolder version still serves the content

[ANTI-PATTERNS TO AVOID]
- Do NOT make slides busy or cluttered in the name of "bold"
- Do NOT sacrifice readability for visual impact
- Do NOT use gradient text — it rarely works well
- Do NOT add animations to compensate for weak design
- Do NOT change every slide — some slides should be quiet to create contrast

[QUALITY CHECKS]
- Every slide has at least one visual anchor
- Key message slides have high visual impact
- Readability is maintained despite bolder design
- The presentation has rhythm: bold slides + quieter slides
- Design consistency is preserved
- No anti-patterns were introduced
