---
name: typeset-slides
description: "Typography improvements: font choices, hierarchy, sizing, weight"
user-invocable: true
argument-hint: "[file]"
---

# /typeset-slides — Typography Enhancement

[MANDATORY PREPARATION]
- Read `.claude/rules/design-standards.md` for typography rules
- Read `.claude/rules/anti-patterns.md` for font-related anti-patterns
- Read `.impeccable-quarto.md` if it exists for font preferences
- Read the target `.qmd` file and any associated SCSS theme files
- Check which fonts are currently loaded (Google Fonts, local, system)

[IMPLEMENTATION STEPS]
1. **Font Pairing Assessment**
   - Evaluate current font choices for harmony
   - Recommend pairings: typically one serif + one sans-serif, or two complementary sans-serifs
   - Ensure fonts are available (Google Fonts, system fonts, or bundled)
   - Apply via SCSS custom properties or Quarto YAML

2. **Hierarchy Establishment**
   - Define a clear type scale (e.g., 1.25 ratio: 24, 30, 38, 47px)
   - Maximum 3 levels of hierarchy per slide (heading, subheading, body)
   - Ensure headings are visually distinct from body text (size + weight)
   - Set minimum body text to 24px for projection readability

3. **Weight & Style**
   - Use font weight for emphasis: Regular (400) for body, Semi-bold (600) for emphasis, Bold (700) for headings
   - Limit to 2-3 weights per font family
   - Use italic sparingly — for citations, foreign words, or subtle emphasis only
   - Never use bold + italic + underline simultaneously

4. **Line Spacing & Measure**
   - Set line-height: 1.4–1.6 for body text
   - Set line-height: 1.1–1.2 for headings
   - Optimal line length: 45–75 characters for body text
   - Adjust letter-spacing for all-caps text (+0.05em minimum)

5. **Code Typography**
   - Ensure code blocks use a quality monospace font (JetBrains Mono, Fira Code, Source Code Pro)
   - Code font size should be ~85-90% of body text size
   - Syntax highlighting colors should complement the theme palette

6. **Implementation**
   - Apply changes via SCSS theme customization or inline Quarto YAML
   - Use CSS custom properties for easy theme-wide changes
   - Test at projected resolution (1920×1080 minimum)

[ANTI-PATTERNS TO AVOID]
- Do NOT use more than 2 font families
- Do NOT set body text below 24px for projection
- Do NOT use decorative/display fonts for body text
- Do NOT use font-size abuse (<20px) to cram more content
- Do NOT mix too many weights (max 3 per family)

[QUALITY CHECKS]
- Font pairing is harmonious and readable
- Type scale follows a consistent ratio
- Min 24px body text for projection
- Max 3 hierarchy levels per slide
- Line spacing is comfortable for reading
- Code blocks have appropriate monospace font
- All fonts are properly loaded/available
