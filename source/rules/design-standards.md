# Design Standards

## Core Principles

1. **Typography-first:** Font choice, scale, and hierarchy drive the design. Every other decision follows typography.
2. **OKLCH color:** All colors in the perceptually uniform OKLCH space. No hex guesswork.
3. **Tinted neutrals:** Never pure black or white. All neutrals carry a subtle hue for warmth and cohesion.
4. **Semantic structure:** Content containers convey meaning (keybox, methodbox, warningbox, tipbox, quotebox, infobox).
5. **One idea per slide:** Each slide has a single clear message. Supporting detail lives in speaker notes.
6. **Whitespace as structure:** Intentional negative space guides the eye and prevents cognitive overload.

## Typography Standards

### Font Stack
| Role | Primary | Fallback |
|---|---|---|
| Display (headings) | Plus Jakarta Sans | Outfit, sans-serif |
| Body (text, lists) | Source Sans 3 | Source Sans Pro, sans-serif |
| Code | JetBrains Mono | Fira Code, monospace |

### Type Scale
- Ratio: **1.25 (Major Third)**
- Base: **28px** (minimum readable at projection distance)
- Scale: 18px → 22px → 28px → 35px → 44px → 55px → 68px

### Minimum Sizes
- Body text: 28px
- Supporting text (`.smaller`): 23px
- Fine print (`.smallest`): 19px — use sparingly
- Absolute minimum: 20px — anything below is an anti-pattern

### Line Height
- Headings: 1.15
- Body text: 1.55
- Code: 1.6
- Minimum acceptable: 1.3

## Color Standards

### Palette (OKLCH)
| Role | Value | Hue | Use |
|---|---|---|---|
| Primary | oklch(0.45 0.18 265) | Indigo | Main accent, links, emphasis |
| Secondary | oklch(0.55 0.12 195) | Teal | Supporting elements |
| Accent | oklch(0.72 0.16 85) | Marigold | Attention, highlights |
| Success | oklch(0.60 0.15 145) | Green | Positive, correct, done |
| Warning | oklch(0.72 0.16 85) | Gold | Caution, note |
| Danger | oklch(0.55 0.18 25) | Red | Error, wrong, warning |
| Info | oklch(0.55 0.12 240) | Blue | Supplementary |

### Neutral Scale
All neutrals at hue 265 with chroma 0.008–0.015:
- Near-black: oklch(0.12 0.015 265)
- Near-white: oklch(0.96 0.012 265)
- 10 steps between for smooth gradation

### Contrast Requirements
- Normal text: 4.5:1 minimum (WCAG AA)
- Large text (≥24px bold or ≥19px regular): 3:1 minimum
- UI components: 3:1 minimum

## Layout Standards

### Slide Dimensions
- Width: 1920px
- Height: 1080px
- Padding: 40px vertical, 60px horizontal
- Maximum content fill: 70% of slide area

### Grid Layouts
- Two column: 1fr 1fr, 2.5em gap
- Three column: 1fr 1fr 1fr, 2em gap
- Sidebar left: 1fr 2fr, 2.5em gap
- Sidebar right: 2fr 1fr, 2.5em gap

### Content Limits Per Slide
- Bullet points: ≤5
- Body text words: ≤40
- Key ideas: 1
- Font families: ≤3
- Primary palette colors: ≤5

## Accessibility Standards

- All images must have descriptive `alt` text
- Heading levels must be sequential (no skips)
- Color must not be the sole means of conveying information
- All animations must respect `prefers-reduced-motion`
- Contrast ratios must meet WCAG AA
