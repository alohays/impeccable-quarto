# Anti-Patterns Reference — Impeccable Quarto Design System

## Purpose

This document catalogs what NOT to do when creating Quarto RevealJS presentations. Each anti-pattern includes what it is, why it's harmful, and the correct alternative. Use this as a checklist before finalizing any deck.

---

## 1. Bullet-Point Walls

### The Problem

More than 5 bullet points on a single slide. Often 8-12 bullets, sometimes nested.

### Why It's Harmful

- Audience reads ahead instead of listening to the speaker
- All points receive equal visual weight — nothing stands out
- Signals that the content hasn't been curated
- Reads as a document projected on screen, not a presentation

### Instead

- Maximum 5 bullets per slide. Prefer 3.
- Split into multiple slides, each making one clear point
- Use fragments to reveal bullets progressively
- Convert related bullets into a semantic box (`.keybox`, `.methodbox`)
- Ask: "Can this be a visual instead of a list?"

---

## 2. Font Size Below 20px for Projection

### The Problem

Using `.smaller`, `.smallest`, or custom font sizing that drops text below 20px.

### Why It's Harmful

- Unreadable from beyond the third row
- Signals to the audience that the content isn't important enough to read
- Causes squinting and disengagement
- Projectors further reduce clarity at small sizes

### Instead

- Body text: 28px minimum (the Impeccable default)
- Footnotes: 18px absolute floor, and only for reference material
- If content doesn't fit at readable size, it doesn't fit on this slide — split it
- Reserve `.smallest` for decorative annotations only, never for content the audience needs

---

## 3. Generic RevealJS Default Theme

### The Problem

Using the built-in RevealJS themes (`simple`, `black`, `white`, `moon`, etc.) without customization.

### Why It's Harmful

- Immediately recognizable as "default" — signals low effort
- Poor typography (system fonts, no hierarchy)
- No semantic elements (boxes, emphasis classes)
- Every RevealJS presentation looks the same

### Instead

- Use an Impeccable theme variant that matches your context
- Customize colors, fonts, and spacing to match your content
- Use semantic box classes for structured information

---

## 4. Pure Black or White Backgrounds

### The Problem

Using `#000000` (black) or `#ffffff` (white) as background or text colors.

### Why It's Harmful

- Pure black on pure white creates harsh contrast that causes eye fatigue
- Pure black backgrounds make text appear to vibrate (halation)
- Feels stark and cold compared to tinted alternatives
- Mismatched with any colored elements in the palette

### Instead

- Use tinted neutrals: `oklch(0.96 0.012 265)` instead of white
- Use `oklch(0.12 0.015 265)` instead of pure black
- The slight chroma hint (0.01-0.02) creates warmth without being visible
- Test: put a pure white rectangle next to the tinted neutral — you'll see the difference immediately

---

## 5. Too Many Colors (>5 Per Deck)

### The Problem

Using 6+ distinct hues across a presentation. Often from copy-pasting content from different sources or using a rainbow chart.

### Why It's Harmful

- Destroys visual coherence — the deck feels like a collage
- No clear color-meaning association (audience can't learn what each color means)
- Overwhelms the eye on any individual slide
- Makes the 60-30-10 rule impossible to follow

### Instead

- Limit to 5 hues maximum: primary, secondary, accent, success, danger
- Use lightness/chroma variations of existing hues for variety
- For charts with 6+ categories, use a single hue with lightness steps
- Audit your deck: list every distinct hue used and eliminate redundancies

---

## 6. Inconsistent Heading Hierarchy

### The Problem

Using h2 on one slide, h3 on the next for the same level of content. Or mixing h1 and h3 without h2.

### Why It's Harmful

- Breaks the visual rhythm — audience can't predict the structure
- Confuses Reveal.js slide structure (h1 = horizontal, h2 = vertical in some configs)
- Creates accessibility issues for screen readers
- Makes the type scale meaningless

### Instead

- Establish a consistent pattern: h2 for all slide titles, h3 for subtitles within slides
- Use h2 with `.section-header` class for section dividers
- Never skip heading levels (h2 → h4 without h3)
- Document your heading convention and stick to it

---

## 7. Text-Heavy Slides Without Visual Anchors

### The Problem

Slides with 3+ paragraphs of running text and no visual structure (no boxes, no columns, no headings, no emphasis).

### Why It's Harmful

- Reads like a paper, not a presentation
- No entry point — the audience doesn't know where to look first
- Speaker becomes redundant (everything is on the slide)
- Glazed eyes within 5 seconds

### Instead

- Break text into a heading + 3-5 short points
- Use a semantic box to highlight the key takeaway
- Use `.two-col` to pair text with a visual or callout
- Move detailed explanations to speaker notes
- Rule of thumb: if you can read the slide content aloud in under 20 seconds, it's about right

---

## 8. Overuse of .smaller/.smallest Classes

### The Problem

Applying `.smaller` or `.smallest` to entire slide content to fit more material.

### Why It's Harmful

- The class exists for footnotes and captions, not for body content
- Signals that too much content is being forced onto one slide
- Creates inconsistent text sizing across the deck
- Defeats the purpose of the modular type scale

### Instead

- If content doesn't fit at base size, split into two slides
- Use `.smaller` only for: captions, footnotes, attribution, reference lists
- Use `.smallest` only for: legal text, decorative annotations, slide numbers
- Never apply size-reduction classes to content the audience needs to read

---

## 9. Centered Everything

### The Problem

Setting `text-align: center` on all content, including paragraphs, lists, and multi-line text.

### Why It's Harmful

- Centered text has ragged both edges — harder to scan than left-aligned
- Each line starts at a different position, so the eye has to search
- Lists lose their alignment and bullet structure breaks
- Only works for single short lines (titles, quotes)

### Instead

- Left-align by default (the Impeccable system does this)
- Center only: single-line titles, short quotes, impact numbers
- Never center: paragraphs, lists, code blocks, multi-line content
- If a slide "needs" centering to look balanced, the content probably needs restructuring

---

## 10. Orphaned Single-Word Lines

### The Problem

A paragraph or bullet point where the last line contains only one word (an "orphan" or "widow").

### Why It's Harmful

- Looks unfinished and unprofessional
- Wastes vertical space
- Creates an awkward visual rhythm
- Especially noticeable on projected slides

### Instead

- Reword the sentence to avoid the orphan
- Use soft breaks (`<br>`) to force better line breaks
- Slightly adjust the slide padding or column width
- In Quarto, use `&nbsp;` (non-breaking space) to keep the last two words together

---

## 11. Stock Gradient Backgrounds

### The Problem

Using CSS gradients as slide backgrounds, especially the default linear-gradient from one saturated color to another.

### Why It's Harmful

- Reduces text contrast unpredictably across the slide
- Feels dated (2010s web design aesthetic)
- Distracts from content
- Makes semantic box backgrounds look wrong (they clash with the gradient)

### Instead

- Use a solid tinted neutral background
- If you must have visual texture, use a very subtle radial gradient with <2% lightness variation
- Save gradients for decorative elements (progress bars, accents), not backgrounds
- The Impeccable system uses flat backgrounds intentionally

---

## 12. Clip Art or Low-Resolution Images

### The Problem

Using clip art, low-resolution photos, or images with visible compression artifacts.

### Why It's Harmful

- Instantly signals low effort
- Pixelated images are distracting and hard to interpret
- Clip art feels unprofessional in any context
- Low-res images become worse when projected at large sizes

### Instead

- Use images at minimum 2x the display resolution (3840×2160 for a 1920×1080 slide)
- Prefer diagrams you create over stock photos
- If you must use photos, use high-quality sources
- Better to have no image than a bad image

---

## 13. Mismatched Icon Styles

### The Problem

Using icons from different icon sets or mixing outline/filled/hand-drawn styles within the same deck.

### Why It's Harmful

- Visual inconsistency is immediately noticeable
- Suggests cobbled-together content from multiple sources
- Different icon weights and styles compete with each other
- Breaks the visual language of the presentation

### Instead

- Choose one icon set and use it exclusively
- Maintain consistent weight (all outline OR all filled, never mixed)
- Match icon color to the text color or primary color
- Prefer no icons over mismatched icons

---

## 14. Content Parity Issues Between Notes and Slides

### The Problem

Speaker notes that contain completely different information than what's on the slide, or slides that make no sense without the speaker notes.

### Why It's Harmful

- Audience who receives the deck later can't follow the narrative
- Speaker who references notes while presenting creates a disconnect
- Slide content should be comprehensible as a standalone artifact
- Notes should supplement, not replace, slide content

### Instead

- Slides should convey the main point even without notes
- Notes add: context, talking points, timing cues, stories, transitions
- Notes do NOT add: critical data, key findings, or conclusions not on the slide
- Test: can someone who missed the talk understand each slide at a glance?

---

## 15. Bounce/Spin/Fly Animations

### The Problem

Using attention-grabbing fragment animations: bounce, elastic, spin, fly-in-from-off-screen.

### Why It's Harmful

- Distracts from content
- Looks unprofessional in academic or corporate settings
- Causes discomfort for motion-sensitive viewers
- Calls attention to the animation, not the information

### Instead

- Use smooth `fade-in` (opacity transition) as the default
- Use `slide-up` (subtle translateY + opacity) for lists
- Keep all transitions under 0.4 seconds
- The Impeccable system provides only subtle, purposeful animations

---

## 16. No Slide Numbers

### The Problem

Disabling slide numbers or using an unhelpful numbering format.

### Why It's Harmful

- Audience can't reference specific slides during Q&A
- Speaker loses track of progress through the deck
- Makes collaboration harder ("on slide 15...")
- No sense of progress or remaining time

### Instead

- Use `slide-number: c/t` (current/total) — e.g., "12/34"
- Position in bottom-right (the Impeccable default)
- Keep the number subtle (small font, neutral color)

---

## 17. Walls of Code

### The Problem

Showing 40+ lines of code on a single slide, often with tiny font size to make it fit.

### Why It's Harmful

- No one reads 40 lines of code on a slide
- Tiny code font is unreadable from beyond the front row
- Suggests the presenter hasn't identified the important part
- Code-heavy slides should teach a concept, not display a file

### Instead

- Maximum 15 lines of code per slide
- Extract only the relevant function or block
- Highlight the important lines with comments or annotations
- Use `.two-col` to pair code with an explanation
- Link to the full source in a footnote

---

## Quick Checklist

Before presenting, verify each slide against this checklist:

- [ ] No more than 5 bullets per slide
- [ ] All text is 20px or larger when projected
- [ ] Maximum 3 hierarchy levels per slide
- [ ] Using a custom theme, not default RevealJS
- [ ] No pure black (#000) or white (#fff)
- [ ] 5 or fewer distinct hues in the entire deck
- [ ] Consistent heading hierarchy throughout
- [ ] Every text-heavy slide has a visual anchor
- [ ] `.smaller`/`.smallest` used only for footnotes/captions
- [ ] Text is left-aligned (centered only for short single lines)
- [ ] No orphaned single-word lines
- [ ] No gradient backgrounds
- [ ] All images are high-resolution
- [ ] Icons are from a single consistent set
- [ ] Slides make sense without speaker notes
- [ ] Only subtle, purposeful animations
- [ ] Slide numbers visible
- [ ] Code blocks are ≤15 lines
