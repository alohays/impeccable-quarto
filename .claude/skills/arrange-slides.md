---
name: arrange-slides
description: "Layout improvements: grid, rhythm, whitespace, visual flow"
user-invocable: true
argument-hint: "[file]"
---

# /arrange-slides — Layout Enhancement

[MANDATORY PREPARATION]
- Read `.claude/rules/design-standards.md` for layout standards
- Read `.claude/rules/anti-patterns.md` for layout anti-patterns
- Read the target `.qmd` file and associated SCSS theme
- Note the slide dimensions (default RevealJS: 960×700 or custom)

[IMPLEMENTATION STEPS]
1. **Grid System**
   - Establish a consistent alignment grid (e.g., 12-column, 40px gutters)
   - Align all text blocks, images, and elements to the grid
   - Use Quarto's column classes (`.columns`, `.column`) consistently
   - Ensure gutters between columns are uniform

2. **Visual Flow**
   - Apply Z-pattern or F-pattern reading flow per slide
   - Place the most important element at the primary focal point (top-left or center)
   - Guide the eye with element placement, size, and contrast
   - Ensure each slide has a clear visual entry point

3. **Whitespace Balance**
   - Ensure generous margins (minimum 5% of slide width on each side)
   - Balance whitespace: don't cluster elements on one side
   - Use whitespace to create visual grouping (proximity principle)
   - Avoid "packed" slides — let content breathe

4. **Slide Density**
   - Evaluate content-to-whitespace ratio (aim for ~60:40 content:space)
   - Flag overcrowded slides for splitting or simplification
   - Ensure images have breathing room (padding around them)

5. **Multi-Column Layouts**
   - Ensure column widths are consistent across similar slide types
   - Image + text slides: consistent image placement (left or right, not mixed)
   - Two-column comparisons: equal width, parallel structure
   - Avoid more than 3 columns per slide

6. **Vertical Rhythm**
   - Space between heading and first content: consistent
   - Space between bullet items: consistent
   - Space between sections within a slide: consistent
   - Bottom padding: enough to avoid feeling crowded at bottom

[ANTI-PATTERNS TO AVOID]
- Do NOT center everything — "centered everything syndrome" is an anti-pattern
- Do NOT use inconsistent column widths for similar content types
- Do NOT leave large empty areas while other areas are cramped
- Do NOT change layout conventions mid-presentation without reason

[QUALITY CHECKS]
- Elements align to a consistent grid
- Whitespace is balanced and intentional
- Visual flow is clear on every slide
- Column layouts are consistent across similar slide types
- Content-to-whitespace ratio is approximately 60:40
- Vertical rhythm is maintained
