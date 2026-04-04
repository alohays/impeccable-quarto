---
name: quieter-slides
description: "Tone down overstimulating designs for clarity and calm"
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

# /quieter-slides — Visual Calm & Focus

[MANDATORY PREPARATION]
- Load design context: Read `.claude/skills/slide-design.md` and follow Steps 1-3 to establish design context
- Read `.claude/rules/design-standards.md` for baseline standards
- Read `.claude/rules/anti-patterns.md` for common overstimulation patterns
- Read the target `.qmd` file completely
- Identify slides that feel overwhelming, busy, or distracting

[IMPLEMENTATION STEPS]
1. **Identify Overstimulating Slides**
   - Flag slides with: too many colors (>4 on one slide), too many animations, competing visual elements
   - Flag slides with: busy backgrounds, excessive iconography, too many font styles
   - Flag slides where the eye doesn't know where to look first

2. **Reduce Color Noise**
   - Limit each slide to 2-3 colors from the palette
   - Replace bright/saturated accents with muted versions (lower chroma in OKLCH)
   - Use neutral backgrounds instead of colored ones for data-heavy slides
   - Remove color where it doesn't add meaning

3. **Simplify Visual Elements**
   - Remove decorative elements that compete with content
   - Replace complex backgrounds with simple ones (solid or subtle gradient)
   - Reduce icon count — use text labels instead where icons aren't essential
   - Simplify borders, shadows, and other chrome

4. **Calm Typography**
   - Remove all-caps unless it's a single short label
   - Replace bold + color + size emphasis with just one emphasis method
   - Increase whitespace around text blocks
   - Use lighter font weights where appropriate

5. **Reduce Animations**
   - Remove decorative animations that don't serve the narrative
   - Simplify transitions: prefer `fade` or `none`
   - Reduce fragment count per slide (max 2-3 reveals)
   - Remove auto-playing elements

6. **Create Visual Breathing Room**
   - Increase margins and padding
   - Add empty space between sections
   - Reduce the number of elements per slide
   - Ensure every element has breathing room around it

[ANTI-PATTERNS TO AVOID]
- Do NOT strip all visual interest — quiet ≠ boring
- Do NOT remove functional visual elements (charts, diagrams)
- Do NOT make everything gray — use muted colors, not no colors
- Do NOT over-correct into a "wall of text" presentation

[QUALITY CHECKS]
- No slide uses more than 3-4 colors
- No slide has competing focal points
- Animations are minimal and purposeful
- Whitespace is generous throughout
- The presentation still has visual interest and personality
- Readability improved from the original
