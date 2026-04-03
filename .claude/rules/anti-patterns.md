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

## LLM Design Bias Anti-Patterns

These patterns are fingerprints of AI-generated presentations (2024-2025 era). They signal that the LLM produced default output without genuine design thought. The overarching test: "If you showed this deck to someone and said 'AI made this,' would they believe you immediately? If yes, that's the problem."

### AP-LLM01: Generic Theme
- **Detection:** Default Reveal.js theme (`theme: default`, `theme: moon`, `theme: solarized`, etc.) with no custom `.scss` override. Or `theme:` field missing entirely.
- **Severity:** Major
- **Why it's bad:** Every LLM-generated deck defaults to the same handful of Reveal.js themes. Using one signals zero design thought and makes the presentation indistinguishable from thousands of others.
- **Fix:** Apply the impeccable theme (`themes/impeccable.scss`) or create a project-specific variant. Custom theme is the single highest-impact design decision.
- **Related:** AP-D01

### AP-LLM02: Monotonous Structure
- **Detection:** >=70% of content slides follow the identical pattern: heading + bullet list. No variation in slide layouts (no semantic boxes, no columns, no comparison layouts, no full-bleed images).
- **Severity:** Major
- **Why it's bad:** LLMs default to heading + bullets for every slide because it's the safest structure. Real presentations vary layout to match content type — data gets charts, comparisons get side-by-side, key points get semantic boxes.
- **Fix:** Audit each slide's content type and match layout: use `.two-col` for comparisons, `.keybox` for takeaways, `.methodbox` for processes, images for visual concepts. Aim for <=50% bullet-list slides.

### AP-LLM03: AI Color Palette
- **Detection:** High-chroma cyan (`#00BCD4`, `#00ACC1`), purple-to-blue gradients, neon accents on dark backgrounds, or any non-OKLCH color values that match the typical AI-generated aesthetic (cyan/purple/neon tones).
- **Severity:** Minor
- **Why it's bad:** The "AI color palette" — cyan-on-dark, purple-to-blue gradients, neon accents — is the single most recognizable visual fingerprint of AI-generated interfaces from 2024-2025. Using these colors screams "AI made this."
- **Fix:** Use the OKLCH palette from the impeccable theme. Colors should be semantically meaningful, not decoratively "techy."

### AP-LLM04: Gradient Text
- **Detection:** CSS `background-clip: text` with gradient, or `background: linear-gradient(...)` / `background: -webkit-linear-gradient(...)` applied to text elements in `.qmd` inline styles or custom CSS.
- **Severity:** Minor
- **Why it's bad:** Gradient text on headings or metrics is a signature AI design choice. It looks "impressive" on first glance but adds no information and reduces readability. It's decoration masquerading as emphasis.
- **Fix:** Use the theme's semantic emphasis: `.hi` classes for inline highlights, semantic boxes for structural emphasis, or OKLCH accent color for genuine emphasis.

### AP-LLM05: Nested Semantic Boxes
- **Detection:** A semantic box class (`.keybox`, `.methodbox`, `.warningbox`, `.tipbox`, `.quotebox`, `.infobox`) nested inside another semantic box.
- **Severity:** Minor
- **Why it's bad:** LLMs overuse semantic boxes and often nest them (a `.methodbox` inside a `.keybox`) to appear "structured." This creates visual noise, breaks the box hierarchy, and confuses the reader about what's key vs. supporting.
- **Fix:** One box level per slide section. If you need to highlight something within a box, use inline emphasis (`.hi`, bold) not a nested box.

### AP-LLM06: Uniform Depth
- **Detection:** Inconsistent content depth across slides — some slides have 3 words, others have 200+ words. Standard deviation of word count across slides exceeds 3x the mean.
- **Severity:** Minor
- **Why it's bad:** LLMs often produce slides of wildly varying depth — a title slide with "Introduction" followed by a slide with 8 dense paragraphs. This signals the LLM is dumping content without editing for audience pacing.
- **Fix:** Target consistent depth: 20-40 words per slide for body text. Move excess detail to speaker notes. Each slide should take roughly the same time to present (1-2 minutes).

### AP-LLM07: Generic Titles
- **Detection:** Title slide contains generic text: "Presentation Title", "Subtitle Here", "Your Name", "Author Name", "[Topic]", "Click to edit", or any placeholder-like text.
- **Severity:** Major
- **Why it's bad:** Generic placeholder titles are the most obvious sign of auto-generated content. Even draft decks should have specific, descriptive titles.
- **Fix:** Replace with a specific, compelling title that communicates the deck's key message. The title is the audience's first impression — make it count.

## Deck-Level Anti-Patterns

### AP-DK01: Monotonous Pacing
- **Detection:** >70% of slides share the same structural template (e.g., heading + bullet list). No variation in slide types (text, image, comparison, data, quote, section break).
- **Severity:** Major
- **Why it's bad:** Uniform structure is hypnotic in the worst way. The audience's attention flatlines when every slide looks the same. Variety in structure signals "pay attention, something new is happening."
- **Fix:** Alternate slide types: text slides, image slides, comparison layouts, data visualizations, quote slides, and section breaks. Aim for no more than 3 consecutive slides with the same structure.

### AP-DK02: Missing Arc
- **Detection:** The deck lacks a clear beginning (motivation/hook), middle (evidence/argument), and end (conclusion/takeaway). No section breaks or transition slides divide the content.
- **Severity:** Major
- **Why it's bad:** Without narrative structure, the presentation is a list of facts, not an argument. The audience can't tell where they are in the story or why they should care.
- **Fix:** Structure as Context -> Problem -> Approach -> Results -> Takeaway. Add section header slides between major parts. The first content slide should establish *why this matters*; the last should state *what to do about it*.

### AP-DK03: Depth Inconsistency
- **Detection:** One section gets 8+ slides while a parallel section of equal importance gets 1-2 slides. Slide count ratio between the longest and shortest non-intro sections exceeds 4:1.
- **Severity:** Major
- **Why it's bad:** Signals the presenter ran out of time, preparation, or interest. The audience infers that shallow sections are unimportant, even if they're crucial.
- **Fix:** Rebalance by splitting overly detailed sections into essentials (slides) and details (speaker notes), or expanding thin sections with supporting evidence, examples, or visuals.

### AP-DK04: Orphan Section
- **Detection:** A section with only 1 content slide (excluding the section header).
- **Severity:** Minor
- **Why it's bad:** A section with one slide doesn't justify being a section. It either needs more content or should be merged into an adjacent section.
- **Fix:** Expand with supporting content, merge into an adjacent section, or remove the section header and integrate the slide into the flow.

### AP-DK05: Data Without Story
- **Detection:** A chart, table, or data visualization appears without interpretive text (no callout, no "what this means" box, no annotation). The slide title is generic (e.g., "Results", "Data").
- **Severity:** Major
- **Why it's bad:** Data doesn't speak for itself. Without interpretation, the audience must decode the chart alone under time pressure — most won't bother. The presenter's job is to tell the audience *what to see* in the data.
- **Fix:** Add a clear interpretive statement: "Key finding: X increases by Y when Z." Use `.keybox` to highlight the takeaway. Add annotations to the chart if possible. Replace generic titles with insight-driven titles (e.g., "Response time drops 3x with caching" instead of "Performance Results").
