---
name: colorize-slides
description: "Color improvements: palette coherence, contrast, semantic use"
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

## REFERENCE MATERIAL

Before color work, read `.context/references/impeccable-original-deep-patterns.md` section 1 (Color).
Key rules: chroma reduction at lightness extremes, 60-30-10 visual weight rule, gray-on-color danger.

# /colorize-slides — Color Enhancement

[MANDATORY PREPARATION]
- Load design context: Read `.claude/skills/slide-design.md` and follow Steps 1-3 to establish design context
- Read `.claude/rules/design-standards.md` for color rules (OKLCH, no pure black/white, tinted neutrals)
- Read `.claude/rules/anti-patterns.md` for color anti-patterns (color salad, pure black/white)
- Read `.impeccable-quarto.md` if it exists for brand colors or preferences
- Read the target `.qmd` file and associated SCSS theme
- Identify the current color usage across all slides

[IMPLEMENTATION STEPS]
1. **Palette Audit**
   - Extract all colors currently used in the presentation
   - Identify the intended primary, secondary, and accent colors
   - Flag inconsistencies: same semantic meaning using different colors
   - Flag "color salad" — more than 5 distinct hues

2. **Build Coherent Palette**
   - Define palette using OKLCH color space for perceptual uniformity
   - Primary: 1 color for main brand/theme identity
   - Secondary: 1 complementary or analogous color
   - Accent: 1 color for highlights, CTAs, emphasis
   - Neutrals: 2-3 tinted neutrals (warm or cool, never pure gray)
   - Semantic: success (green-ish), warning (amber-ish), error (red-ish) if needed

3. **Replace Pure Black & White**
   - Replace `#000000` with a dark tinted neutral (e.g., `oklch(15% 0.02 250)`)
   - Replace `#FFFFFF` with an off-white (e.g., `oklch(98% 0.005 250)`)
   - Apply consistently across text, backgrounds, and borders

4. **Contrast Verification**
   - Check all text/background combinations meet WCAG AA:
     - Normal text: 4.5:1 ratio minimum
     - Large text (≥24px or ≥19px bold): 3:1 ratio minimum
   - Fix any failing combinations by adjusting lightness in OKLCH

5. **Semantic Color Application**
   - Use color consistently for meaning: all links one color, all emphasis one color
   - Ensure data visualization colors are distinguishable (colorblind-safe)
   - Apply accent color purposefully — not randomly scattered

6. **Implementation**
   - Define colors as CSS custom properties in SCSS
   - Use OKLCH format: `oklch(L C H)` for all color definitions
   - Create light/dark mode variants if applicable

[ANTI-PATTERNS TO AVOID]
- Do NOT use pure black (#000) or pure white (#FFF)
- Do NOT use more than 5 distinct hues (color salad)
- Do NOT use gradient text for impact
- Do NOT use color as the sole indicator of meaning (accessibility)
- Do NOT pick colors that look similar to colorblind viewers

[QUALITY CHECKS]
- Palette has ≤5 distinct hues
- No pure black or pure white anywhere
- All text passes WCAG AA contrast ratios
- Colors are used semantically and consistently
- OKLCH format used for color definitions
- Palette works for common forms of color blindness
