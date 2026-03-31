# Anti-Patterns — Codified Bad Practices

## Overview

These patterns are explicitly recognized as harmful to slide quality. Each pattern has a name, detection criteria, severity level, and recommended fix.

## Content Anti-Patterns

### AP-C01: Bullet Wall
- **Detection:** More than 5 bullet points on a single slide
- **Severity:** Major
- **Why it's bad:** Audiences stop reading after 3-4 items. Walls of bullets signal the presenter hasn't distilled their message.
- **Fix:** Split across slides, use semantic boxes, or move detail to speaker notes

### AP-C02: Content Dump
- **Detection:** Slide communicates more than one key idea; >40 words of body text
- **Severity:** Major
- **Why it's bad:** Cognitive overload. The audience can read or listen, not both simultaneously.
- **Fix:** One idea per slide. Supporting detail goes in speaker notes.

### AP-C03: Text Overflow
- **Detection:** Content extends beyond slide boundaries at 1920×1080
- **Severity:** Critical
- **Why it's bad:** Content is literally invisible to the audience.
- **Fix:** Reduce content, split slide, use `.smaller` class, or restructure with layout classes

### AP-C04: Missing Narrative
- **Detection:** Slides are a sequence of facts with no connecting story
- **Severity:** Major
- **Why it's bad:** Without narrative, the audience can't follow *why* information matters.
- **Fix:** Structure as Context → Problem → Approach → Results → Takeaway

### AP-C05: Orphan Slide
- **Detection:** A slide that doesn't logically connect to its neighbors
- **Severity:** Minor
- **Why it's bad:** Breaks the flow; audience momentarily loses context.
- **Fix:** Add transition text, move to appropriate section, or remove

## Design Anti-Patterns

### AP-D01: Generic Theme
- **Detection:** Default Reveal.js theme with no customization
- **Severity:** Major
- **Why it's bad:** Signals no thought was given to visual communication. Every LLM-generated deck looks the same.
- **Fix:** Apply impeccable theme or create a variant

### AP-D02: Pure Black/White
- **Detection:** `#000000` or `#FFFFFF` (or `rgb(0,0,0)`, `rgb(255,255,255)`) in source
- **Severity:** Major
- **Why it's bad:** Pure black/white is harsh and disconnected from the palette. Creates a clinical feel.
- **Fix:** Use tinted neutrals from the theme ($neutral-950, $neutral-50)

### AP-D03: Random Colors
- **Detection:** Colors without semantic mapping; colors not from the OKLCH palette
- **Severity:** Minor
- **Why it's bad:** Arbitrary colors create visual noise and undermine the design system.
- **Fix:** Use semantic color roles (primary, secondary, accent, success, warning, danger, info)

### AP-D04: Font Soup
- **Detection:** More than 3 font families on a single slide
- **Severity:** Major
- **Why it's bad:** Competing typefaces create visual chaos. The eye doesn't know where to look.
- **Fix:** Stick to the theme's display/body/code triad

### AP-D05: All-Caps Abuse
- **Detection:** Uppercase text longer than 3 words, or multiple all-caps elements per slide
- **Severity:** Minor
- **Why it's bad:** All-caps reduces readability by 13–18%. When everything shouts, nothing stands out.
- **Fix:** Use `.hi` emphasis classes or semantic boxes for emphasis

### AP-D06: Decoration Noise
- **Detection:** Borders, shadows, gradients, or ornaments that don't convey information
- **Severity:** Minor
- **Why it's bad:** Decoration without purpose is noise. It competes with content for attention.
- **Fix:** Remove purely decorative elements. Let typography and whitespace lead the design.

## Typography Anti-Patterns

### AP-T01: Tiny Text
- **Detection:** Font size below 20px (absolute) or below the theme's $size-xs
- **Severity:** Major
- **Why it's bad:** Unreadable at projection distance. The back row sees nothing.
- **Fix:** Use 28px base minimum. `.smaller` (82%) for supporting text only.

### AP-T02: Heading Skip
- **Detection:** Heading levels skip (H1 → H3 without H2)
- **Severity:** Major
- **Why it's bad:** Breaks semantic hierarchy. Assistive technology relies on sequential headings.
- **Fix:** Use sequential heading levels. H1 for title, H2 for slides, H3 for subsections.

### AP-T03: Weight Overload
- **Detection:** More than 30% of text on a slide is bold
- **Severity:** Minor
- **Why it's bad:** When everything is bold, nothing is emphasized. Emphasis requires contrast with non-emphasis.
- **Fix:** Reserve bold for genuine emphasis. Use color (`.hi` classes) for variety.

### AP-T04: Line Squeeze
- **Detection:** Line-height below 1.3 for body text
- **Severity:** Minor
- **Why it's bad:** Cramped text is hard to read. The eye struggles to track between lines.
- **Fix:** Use 1.5+ for body text, 1.15+ for headings.

## Technical Anti-Patterns

### AP-X01: Missing Speaker Notes
- **Detection:** Content slide without `::: {.notes}` block
- **Severity:** Major
- **Why it's bad:** The presenter has no guide. Speaker notes ensure consistent delivery.
- **Fix:** Add `::: {.notes}` with talking points, timing cues, transition hints.

### AP-X02: Missing Alt Text
- **Detection:** Image without `alt` attribute or with empty `alt=""`
- **Severity:** Major
- **Why it's bad:** Accessibility failure (WCAG). Screen readers cannot describe the image.
- **Fix:** Add descriptive alt text that conveys the image's message, not just its content.

### AP-X03: Inline Styles
- **Detection:** `style=` attributes in `.qmd` file
- **Severity:** Minor
- **Why it's bad:** Inline styles bypass the design system, create inconsistency, and are hard to maintain.
- **Fix:** Use theme variables and utility classes (`.smaller`, `.hi`, semantic boxes).

### AP-X04: Raster Diagrams
- **Detection:** PNG/JPG files for diagrams, charts, or architecture drawings
- **Severity:** Minor
- **Why it's bad:** Raster images blur at non-native resolutions. SVG scales perfectly.
- **Fix:** Export diagrams as SVG. Reserve raster for photographs.

### AP-X05: Broken References
- **Detection:** Cross-references (`@fig-`, `@tbl-`, `@sec-`) that don't resolve
- **Severity:** Critical
- **Why it's bad:** Renders as "??" in the output. Unprofessional and confusing.
- **Fix:** Verify all references. Use consistent label naming.
