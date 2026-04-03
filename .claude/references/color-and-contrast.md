# Color & Contrast Reference — Impeccable Quarto Design System

## Why OKLCH

The Impeccable system uses **OKLCH** (Oklab Lightness, Chroma, Hue) exclusively. OKLCH is a perceptually uniform color space, meaning:

- **L = 0.50** for two different hues looks equally bright to human eyes
- Chroma adjustments don't shift perceived lightness (unlike HSL)
- Hue interpolation travels through perceptually sensible colors (no muddy midpoints)

This matters for slides because contrast ratios become predictable and palettes feel cohesive without manual per-color tweaking.

### OKLCH vs HSL — Key Differences

| Property | HSL | OKLCH |
|----------|-----|-------|
| Perceptual uniformity | No — hsl(60, 100%, 50%) looks much brighter than hsl(240, 100%, 50%) | Yes — same L value = same perceived brightness |
| Gamut handling | Clips unpredictably | Graceful fallback with `color()` function |
| Chroma control | Saturation is relative to lightness | Chroma is absolute — 0.10 means the same thing at any lightness |
| Browser support | Universal | Modern browsers (Chrome 111+, Safari 16.4+, Firefox 113+) |

### OKLCH Syntax

```scss
// oklch(lightness chroma hue)
// L: 0–1 (0 = black, 1 = white)
// C: 0–0.4 (0 = gray, higher = more saturated)
// H: 0–360 (hue angle in degrees)

$primary: oklch(0.45 0.18 265);  // Deep indigo
```

## The Palette Architecture

### Primary, Secondary, Accent

Every theme variant follows the same three-role structure:

| Role | Purpose | Chroma Range | Usage |
|------|---------|-------------|-------|
| Primary | Brand authority, headings, links, borders | 0.12–0.22 | 30% of colored elements |
| Secondary | Supporting distinction | 0.08–0.14 | 10% of colored elements |
| Accent | Attention, highlights, call-outs | 0.14–0.20 | 10% of colored elements |
| Neutrals | Text, backgrounds, structure | 0.006–0.018 | 50% of all elements |

### The 60-30-10 Rule for Slides

- **60% — Neutral backgrounds and text** — The canvas. Tinted neutrals, body text, structural elements.
- **30% — Primary and secondary** — Headings, borders, key UI elements. Establishes the visual identity.
- **10% — Accent** — Highlights, call-to-action elements, key findings. Draws the eye to what matters.

### DO

- Use accent color for the single most important element per slide
- Keep colored text to headings and emphasis — body text stays neutral
- Use opacity/lightness variations of the same hue for related elements

### DON'T

- Use more than 5 distinct hues in a single deck
- Apply accent color to more than 2 elements per slide
- Use color as the only means of conveying information (accessibility)

## Tinted Neutrals

Pure black (`#000`) and pure white (`#fff`) feel harsh and artificial on screen. The Impeccable system adds a subtle chroma hint (0.01–0.02) at the brand hue to all neutrals.

### How Tinted Neutrals Work

```scss
// Instead of pure gray:
// gray-900: oklch(0.18 0 0)     ← pure gray, feels cold and flat

// Add a whisper of brand hue (265 = indigo):
$neutral-900: oklch(0.18 0.015 265);  // ← warm, cohesive, still reads as "near-black"
```

The chroma values are so low (0.006–0.018) that the tint is invisible in isolation but creates a subtle warmth when many neutral elements appear together.

### Tinted Neutral Scale

| Token | Lightness | Chroma | Usage |
|-------|-----------|--------|-------|
| neutral-950 | 0.12 | 0.015 | Deepest background (code blocks) |
| neutral-900 | 0.18 | 0.015 | Near-black text, dark backgrounds |
| neutral-800 | 0.25 | 0.015 | Primary body text |
| neutral-700 | 0.35 | 0.012 | Secondary body text, paragraphs |
| neutral-600 | 0.45 | 0.010 | Subtle text, descriptions |
| neutral-500 | 0.55 | 0.008 | Placeholder, disabled |
| neutral-400 | 0.65 | 0.008 | Borders, dividers |
| neutral-300 | 0.75 | 0.008 | Light borders |
| neutral-200 | 0.85 | 0.010 | Subtle backgrounds |
| neutral-100 | 0.92 | 0.012 | Card backgrounds |
| neutral-50 | 0.96 | 0.012 | Page background |

### Hue by Theme Variant

| Theme | Neutral Hue | Character |
|-------|------------|-----------|
| Default | 265 (indigo) | Cool, trustworthy |
| Academic | 45 (warm) | Parchment, scholarly |
| Corporate | 240 (blue) | Professional, neutral |
| Creative | 300 (violet) | Warm, expressive |
| Lightning | 255 (blue) | Cool, dramatic |

## Contrast Requirements for Projection

Projected slides face worse conditions than screens: lower contrast ratio, ambient light, color shift from projectors, and viewing distance. Design for the worst case.

### Minimum Contrast Guidelines

| Element | Minimum Ratio | Recommendation |
|---------|--------------|----------------|
| Body text on background | 7:1 | Use neutral-800 on neutral-50 |
| Heading on background | 4.5:1 | neutral-950 on neutral-50 |
| Colored text (primary) | 4.5:1 | Verify L-difference ≥ 0.45 |
| Text inside colored boxes | 4.5:1 | Dark text on light box fill |
| Chart labels | 3:1 | Larger text can have lower ratio |

### Quick OKLCH Contrast Rule

For OKLCH, a reliable rule of thumb for contrast:

> **If the lightness difference between text and background is ≥ 0.45, contrast is likely sufficient for body text.**

```
Background: oklch(0.96 ...)   Text: oklch(0.25 ...)
L-difference: 0.96 - 0.25 = 0.71 ✓ (well above 0.45)

Background: oklch(0.96 ...)   Text: oklch(0.60 ...)
L-difference: 0.96 - 0.60 = 0.36 ✗ (too low for body text)
```

## Semantic Color Usage

### Box Colors

Each semantic box type uses a specific hue:

| Box | Hue | Meaning | Border | Background |
|-----|-----|---------|--------|------------|
| `.keybox` | Gold/Orange (85°) | Key finding, takeaway | oklch(0.72 0.16 85) | oklch(0.95 0.04 85) |
| `.methodbox` | Primary (265°) | Process, methodology | oklch(0.45 0.18 265) | oklch(0.85 0.06 265) |
| `.warningbox` | Red (25°) | Caution, limitation | oklch(0.55 0.18 25) | oklch(0.95 0.04 25) |
| `.tipbox` | Green (145°) | Best practice, strength | oklch(0.60 0.15 145) | oklch(0.95 0.04 145) |
| `.quotebox` | Neutral | Attribution, voice | neutral-400 | neutral-100 |
| `.infobox` | Blue (240°) | Context, reference | oklch(0.55 0.12 240) | oklch(0.95 0.03 240) |

### Color in Data Visualization

- Use 3–5 distinct hues for categorical data, spaced ≥ 60° apart on the hue wheel
- Use lightness ramps (same hue, different L) for sequential data
- Always provide a non-color encoding (pattern, label, shape) alongside color
- Test with a colorblind simulator — 8% of males have red-green color vision deficiency

## Dark Mode

The dark mode variant inverts the neutral scale and adjusts chroma:

- Backgrounds: neutral-900 (L: 0.18) instead of neutral-50 (L: 0.96)
- Text: neutral-200 (L: 0.85) instead of neutral-800 (L: 0.25)
- Primary/accent: shift to `-light` variants to maintain contrast
- Box backgrounds: L ≈ 0.22, low chroma (0.03)

### DO

- Test dark mode on an actual dark background, not just in your editor
- Increase chroma slightly for colored elements in dark mode (they appear more muted)
- Ensure code blocks maintain sufficient contrast (light text on dark background)

### DON'T

- Simply invert all colors — dark mode needs independent tuning
- Use fully saturated colors on dark backgrounds (they vibrate and cause eye strain)
- Forget to test semantic boxes in both modes

## DO / DON'T Summary

### DO

- Use OKLCH for all color definitions
- Maintain ≥ 0.45 L-difference for text-on-background
- Apply the 60-30-10 rule to every slide
- Add chroma hint (0.01–0.02) to all neutrals
- Test on a projector or in bright ambient light
- Limit to 5 hues per deck

### DON'T

- Use pure black (#000) or pure white (#fff) anywhere
- Use HSL — it doesn't match human perception
- Rely on color alone to convey meaning
- Use more than 2 accent-colored elements per slide
- Apply high-chroma colors to large areas (backgrounds, full-width bars)
- Forget that projectors desaturate and reduce contrast significantly
