# Spatial Design Reference — Impeccable Quarto Design System

## The Slide as a Canvas

A Reveal.js slide at 1920×1080 is not a page — it's a visual field seen at distance. Spatial design determines how the audience's eyes move through content and what they perceive as important.

## Slide Grid System

### The Impeccable Grid

The default slide has a 5% margin (set via Reveal.js `margin: 0.05`), giving a usable area of approximately **1728×972px**. Internal padding adds structure:

```
┌──────────────────────────────────────────┐
│ 60px padding                              │
│  ┌────────────────────────────────────┐   │
│  │                                    │   │
│  │  Content Area: ~1608 × 892px       │   │
│  │                                    │   │
│  │                                    │   │
│  │                                    │   │
│  └────────────────────────────────────┘   │
│                                  40px     │
└──────────────────────────────────────────┘
```

### Padding Values by Theme

| Theme | Padding | Rationale |
|-------|---------|-----------|
| Default | 40px 60px | Balanced whitespace |
| Academic | 45px 65px | Slightly more margin for formality |
| Corporate | 40px 60px | Standard professional |
| Creative | 40px 55px | Slightly tighter for visual impact |
| Lightning | 50px 60px | More vertical breathing room |

## Column Layouts

### Available Layouts

| Class | Grid | Use Case |
|-------|------|----------|
| `.two-col` | 1fr 1fr | Side-by-side comparison, text + visual |
| `.three-col` | 1fr 1fr 1fr | Feature comparison, KPI cards |
| `.sidebar-left` | 1fr 2fr | Navigation/label + main content |
| `.sidebar-right` | 2fr 1fr | Main content + supplementary info |
| `.comparison` | 1fr 1fr | Before/after, pro/con |

### Gap Sizing

- Two-column: **2.5em** gap — enough breathing room between columns
- Three-column: **2em** gap — tighter to fit three columns comfortably
- Sidebar: **2.5em** gap — clear separation between sidebar and main

### DO

- Use `.two-col` when you have a text block paired with a visual or box
- Use `.three-col` for exactly three parallel items (features, metrics, steps)
- Use `.sidebar-right` for main content with a supporting callout box
- Keep columns balanced — avoid a wall of text in one column and a single line in another

### DON'T

- Nest columns inside columns — one level of grid is sufficient
- Force three columns when two would be clearer
- Put critical content in a sidebar and supplementary content in the main area
- Create columns with drastically different content heights

## Visual Hierarchy

### The F-Pattern and Z-Pattern

Slide audiences scan in predictable patterns:

- **F-pattern**: For text-heavy slides. Heading first (top-left), then left edge of content, scanning rightward less with each line.
- **Z-pattern**: For minimal slides. Top-left → top-right → diagonal to bottom-left → bottom-right.

### Hierarchy Signals (strongest to weakest)

1. **Position** — Top-left is seen first. Bottom-right is seen last.
2. **Size** — Larger elements demand attention before smaller ones.
3. **Weight** — Bold text pulls the eye more than regular weight.
4. **Color** — Saturated or contrasting color attracts attention.
5. **Whitespace** — Isolated elements with space around them feel important.
6. **Border/background** — Boxed elements read as distinct units.

### Three-Level Rule

Every slide should have exactly **three hierarchy levels**:

1. **Primary** — The one thing the audience should read first (heading or key number)
2. **Secondary** — Supporting detail they read next (body text, subheading)
3. **Tertiary** — Reference material they can skip (footnotes, citations, captions)

### DO

- Place the most important element in the top-left quadrant
- Use size + weight + color together to reinforce primary hierarchy
- Leave the bottom third of the slide for supporting information

### DON'T

- Give everything equal visual weight (nothing stands out → nothing is read)
- Place critical content in the bottom-right corner
- Use more than 3 hierarchy levels on a single slide

## Whitespace as Design Element

Whitespace is not empty space — it's a structural element that creates breathing room, groups related elements, and directs attention.

### Principles

**Proximity:** Elements close together are perceived as related. Use consistent spacing to group related content and larger gaps to separate distinct sections.

**Breathing room:** Every content block needs space around it. Crowded slides feel chaotic even when the content is well-organized.

**Negative space speaks:** A slide with 40% whitespace communicates confidence. A slide at 95% capacity communicates anxiety ("I need to fit everything").

### Spacing Scale

Use consistent spacing multiples:

| Token | Value | Usage |
|-------|-------|-------|
| xs | 0.4em | Between list items, tight groups |
| sm | 0.8em | Between paragraphs within a section |
| md | 1.2em | Between sections, around boxes |
| lg | 2.0em | Between column items, major separations |
| xl | 2.5em | Column gaps, between slide regions |

### DO

- Aim for 30-40% whitespace on content slides
- Use equal spacing between similar elements
- Leave the bottom 15% of slides relatively empty
- Use horizontal rules or extra spacing (not lines) to separate sections

### DON'T

- Fill every pixel — resist the urge to "use the space"
- Use inconsistent spacing between similar elements
- Compress content to fit more on one slide — split into two slides instead
- Add decorative elements to fill whitespace

## Alignment

### Left-Align by Default

The Impeccable system sets `text-align: left` as the default. This is intentional:

- Left-aligned text has a consistent anchor point (the left edge)
- Eyes return to the same horizontal position at the start of each line
- Lists, code, and mixed content align naturally

### When to Center

Center alignment is appropriate for:

- Single-line statements or quotes on otherwise empty slides
- Impact numbers (the `.impact` class in the lightning theme)
- Image captions that are shorter than the image width

### When NOT to Center

- Paragraphs longer than one line
- Lists (bulleted or numbered)
- Multi-line headings
- Content inside semantic boxes

### DO

- Align all elements to the same left edge when possible
- Use grid columns to create multiple left-aligned zones
- Center only isolated, short elements

### DON'T

- Center everything because "it looks balanced" — it makes text harder to read
- Mix left-align and center-align within the same content block
- Use right-alignment for anything except numbers in data tables

## Semantic Box Spacing

Semantic boxes (`.keybox`, `.methodbox`, etc.) follow consistent spatial rules:

- **Padding:** 1em vertical, 1.4–1.5em horizontal
- **Margin:** 0.8–1em vertical
- **Border-left:** 4–6px (weight increases with theme boldness)
- **Border-radius:** 0 on left (flush with border), 6–12px on right

### Box Placement Guidelines

- Place key-finding boxes (`.keybox`) in prominent positions — right column or below the main content
- Method boxes (`.methodbox`) work well at the top of a slide to frame the content below
- Warning boxes (`.warningbox`) are attention-grabbing — use sparingly, max 1 per slide
- Don't stack more than 2 semantic boxes on a single slide

## Responsive Considerations

While Reveal.js slides have a fixed aspect ratio, they scale to different viewport sizes:

- `min-scale: 0.2` and `max-scale: 2.0` allow range of display sizes
- Avoid absolute pixel values for content sizing — use `em` units
- Test at both small (laptop) and large (projector) scales
- The `margin: 0.05` provides consistent breathing room at all scales
