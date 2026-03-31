# Typography Reference — Impeccable Quarto Design System

## Core Principles

Typography is the single most impactful design decision in presentation slides. Unlike web or print, slides are viewed at a distance, in varied lighting, for brief durations. Every typographic choice must optimize for **scanability** and **hierarchy clarity**.

## Font Pairing Strategy

### Display + Body + Code Stack

The Impeccable system uses a three-tier font stack:

| Role | Primary | Fallback | Purpose |
|------|---------|----------|---------|
| Display | Plus Jakarta Sans | Outfit | Headings, titles, emphasis |
| Body | Source Sans 3 | IBM Plex Sans | Running text, lists, notes |
| Code | JetBrains Mono | Fira Code | Code blocks, inline code |

### Why These Fonts

**Plus Jakarta Sans** — Modern geometric sans-serif with distinctive character. Slightly rounded terminals give warmth without losing professionalism. Wide weight range (200–800) allows precise hierarchy expression.

**Source Sans 3** — Adobe's open-source workhorse. Excellent x-height for readability. Clear distinction between similar characters (1, l, I). Optimized for screen rendering. Has true italics, not slanted romans.

**Cormorant Garamond** (Academic variant) — High-contrast serif that reads beautifully at display sizes. Evokes scholarly tradition without feeling dated. Pairs naturally with sans-serif body text.

### Pairing Rules

- DO: Use display font for headings, body font for content. Two fonts maximum per slide.
- DO: Use weight contrast (700 vs 400) rather than size alone for hierarchy.
- DON'T: Mix more than 2 font families on a single slide.
- DON'T: Use display font for body text — geometric sans loses readability below 24px.
- DON'T: Use Inter, Roboto, or system fonts — they are ubiquitous and add no design distinction.

## Modular Type Scale

The system uses a **1.25 (Major Third)** ratio for the default theme:

| Token | Computation | Size | Usage |
|-------|------------|------|-------|
| `$size-3xl` | base × 1.25⁴ | ~68px | Title slides only |
| `$size-2xl` | base × 1.25³ | ~55px | Section headers |
| `$size-xl` | base × 1.25² | ~44px | Slide headings (h2) |
| `$size-lg` | base × 1.25¹ | ~35px | Subheadings (h3) |
| `$size-base` | base | 28px | Body text, lists |
| `$size-sm` | base ÷ 1.25 | ~22px | Captions, footnotes |
| `$size-xs` | base ÷ 1.25² | ~18px | Legal text, annotations |

### Variant Scales

| Theme | Ratio | Character |
|-------|-------|-----------|
| Default (1.25) | Major Third | Balanced, versatile |
| Academic (1.25) | Major Third | Conservative, readable |
| Corporate (1.25) | Major Third | Clean, professional |
| Creative (1.333) | Perfect Fourth | Dramatic, expressive |
| Lightning (1.414) | Augmented Fourth | Maximum impact |

## Slide-Specific Type Rules

### Minimum Sizes for Projection

- **Body text:** 28px minimum (24px absolute floor for footnotes)
- **Headings:** 35px+ for visibility from the back of the room
- **Code blocks:** 20px minimum — code is already harder to read in monospace
- **Footnotes/citations:** 18px — acceptable only for reference material

### Maximum Hierarchy Levels

- DO: Use maximum **3 hierarchy levels** per slide (heading + subheading + body)
- DON'T: Use h1 through h4 on a single slide — this creates visual confusion
- DON'T: Rely on size alone — combine size, weight, and color for clear hierarchy

### Line Length

- **Optimal:** 45–65 characters per line on a 1920px-wide slide
- Columns help control line length — use `.two-col` or `.sidebar-right` for text-heavy slides
- DO: Let whitespace breathe. A half-empty slide is better than a cramped one.
- DON'T: Fill the full slide width with a single column of text.

### Line Height (Leading)

- **Headings:** 1.0–1.15 — tight leading for impact, especially at large sizes
- **Body text:** 1.5–1.6 — generous leading improves scanability on projected screens
- **Code:** 1.5–1.6 — code needs room between lines for pattern recognition

### Letter Spacing (Tracking)

- **Display headings:** -0.02em to -0.04em — tighter tracking at large sizes is standard
- **Body text:** 0 (default) — don't adjust tracking on body text
- **All caps text:** +0.05em minimum — caps without tracking look cramped

### Font Weight Usage

| Weight | Name | Usage |
|--------|------|-------|
| 400 | Regular | Body text, descriptions |
| 500 | Medium | Subtle emphasis, author names |
| 600 | Semi-bold | Subheadings, labels |
| 650 | (custom) | Inline emphasis (`.hi` classes) |
| 700 | Bold | Headings, key terms |
| 800 | Extra-bold | Title slides, section headers |
| 900 | Black | Lightning theme titles only |

## Text Rendering

### Anti-Aliasing

Always apply these properties for crisp text rendering:

```scss
font-feature-settings: "kern" 1, "liga" 1, "calt" 1;
text-rendering: optimizeLegibility;
-webkit-font-smoothing: antialiased;
-moz-osx-font-smoothing: grayscale;
```

### OpenType Features

- **Kerning** (`kern`): Always on — improves letter spacing between specific pairs
- **Ligatures** (`liga`): On for body text, especially for code fonts with ligature support
- **Contextual alternates** (`calt`): On — provides contextually appropriate glyph variants

## DO / DON'T Summary

### DO

- Start with 28px body text and scale up, never down
- Use weight + color to establish hierarchy, not size alone
- Load fonts from Google Fonts with `display=swap` for fast rendering
- Test typography on a projector (or large external monitor at arms length)
- Use the `.smaller` class sparingly and only for supplementary information
- Set `text-align: left` as default — centered text is harder to scan

### DON'T

- Go below 20px for anything projected on screen
- Use more than 3 hierarchy levels on one slide
- Set body text in the display font (geometry hurts readability at small sizes)
- Use all caps for more than 2-3 words (labels and acronyms only)
- Center long paragraphs — left-aligned text has a consistent anchor point
- Use Inter, Roboto, or system defaults — they signal "I didn't think about type"
- Apply `.smallest` to content the audience needs to read — it's for decorative annotations only
