---
name: teach-style
description: "One-time setup: gather presentation context and style preferences, save to .impeccable-quarto.md"
user-invocable: true
argument-hint: ""
---

# /teach-style — Style Preference Setup

[MANDATORY PREPARATION]
- Check if `.impeccable-quarto.md` already exists in the project root
  - If it exists, read it and offer to update rather than recreate
- This is an interactive skill — it requires user input through a series of questions

[IMPLEMENTATION STEPS]
1. **Context Gathering** — Ask the user:
   - What is the primary context? (academic, corporate, startup, educational, personal)
   - Who is the typical audience? (researchers, executives, students, general public)
   - What is the typical venue? (conference talk, lecture, board meeting, webinar)
   - Typical talk duration? (5 min lightning, 15-20 min conference, 45-60 min lecture)

2. **Visual Preferences** — Ask the user:
   - Do you have brand colors? (provide hex/OKLCH values)
   - Font preferences? (serif, sans-serif, specific font names)
   - Visual style? (minimal, bold, data-heavy, image-rich, mixed)
   - Dark or light mode preference?
   - Any inspirational presentations or styles to emulate?

3. **Content Preferences** — Ask the user:
   - Text density preference? (minimal text, moderate, detailed)
   - Speaker notes style? (bullet prompts, full script, key phrases)
   - Code display preferences? (if applicable: language, highlighting theme)
   - How much animation? (none, minimal reveals, moderate, rich)

4. **Technical Preferences** — Ask the user:
   - Slide dimensions? (16:9 default, 4:3, custom)
   - Export needs? (HTML only, PDF, self-contained)
   - Version control considerations?
   - Any required templates or branding guidelines?

5. **Anti-Pattern Preferences** — Ask the user:
   - Any specific things to always avoid?
   - Any "rules" they've established for their presentations?
   - Pet peeves about presentations they've seen?

6. **Save Configuration**
   - Compile all responses into `.impeccable-quarto.md` in the project root
   - Use a clear, structured format that other skills can parse
   - Include both preferences and the reasoning behind them

[OUTPUT FORMAT for .impeccable-quarto.md]
```markdown
# Impeccable Quarto — Style Guide

## Context
- Primary context: <context>
- Audience: <audience>
- Venue: <venue>
- Duration: <duration>

## Visual Style
- Color palette: <colors in OKLCH>
- Fonts: heading=<font>, body=<font>, code=<font>
- Mode: <light/dark>
- Style: <minimal/bold/data-heavy/etc>

## Content
- Text density: <minimal/moderate/detailed>
- Speaker notes: <bullet/script/phrases>
- Animation level: <none/minimal/moderate/rich>

## Technical
- Dimensions: <width>x<height>
- Export: <formats>

## Rules
- Always: <list>
- Never: <list>

## Inspiration
- <links or descriptions>
```

[ANTI-PATTERNS TO AVOID]
- Do NOT skip questions — gather complete preferences
- Do NOT impose your own preferences over the user's
- Do NOT make the file overly complex — keep it parseable
- Do NOT ask all questions at once — group them conversationally

[QUALITY CHECKS]
- All sections of the style guide are populated
- Color values are in OKLCH format (convert if needed)
- Preferences are specific enough to be actionable by other skills
- The file is saved to the project root as `.impeccable-quarto.md`
