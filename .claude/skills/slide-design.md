---
name: slide-design
description: "Hub skill: loads design context, theme reference, and design vocabulary. Called by all design skills before execution."
user-invocable: true
argument-hint: ""
---

# /slide-design — Design Context Hub

This is the shared foundation for all design skills. It ensures every design operation starts with consistent context: project preferences, theme reference, design vocabulary, and the AI Slop Test.

**When to invoke:** Every design-related skill (`/critique-slides`, `/audit-slides`, `/typeset-slides`, `/colorize-slides`, `/bolder-slides`, `/quieter-slides`, `/polish-slides`, `/normalize-slides`, `/arrange-slides`, `/animate-slides`, `/create-deck`) should reference this hub as their first preparation step.

**When invoked standalone:** Provides a summary of the active design context — useful for checking what design system is in effect before starting work.

## STEP 1: Load Project Context

1. **Check `.impeccable-quarto.md`** in the project root:
   - If it exists: read it. This is the project's customized design context (audience, palette, fonts, constraints).
   - If it does NOT exist: note that defaults will be used. Suggest running `/teach-style` to create one.

2. **Check YAML frontmatter** of the target `.qmd` (if one is being worked on):
   - Extract `theme:` — which SCSS file(s) are applied?
   - Extract `width:` and `height:` — what are the slide dimensions?
   - Extract any `css:` overrides
   - Flag if no custom theme is specified (AP-LLM01)

## STEP 2: Load Design System Reference

Read these rules files to establish the design vocabulary:

1. `.claude/rules/design-standards.md` — Typography stack, OKLCH palette, layout grid, accessibility
2. `.claude/rules/anti-patterns.md` — All anti-patterns including LLM Design Bias patterns
3. `.claude/rules/quality-gates.md` — Scoring rubric for quantitative assessment

**Key design vocabulary to keep active:**

### Typography Stack
| Role | Font | Fallback |
|------|------|----------|
| Display | Plus Jakarta Sans | Outfit, sans-serif |
| Body | Source Sans 3 | Source Sans Pro, sans-serif |
| Code | JetBrains Mono | Fira Code, monospace |

### OKLCH Palette
| Role | Value |
|------|-------|
| Primary | oklch(0.45 0.18 265) — Deep Indigo |
| Secondary | oklch(0.55 0.12 195) — Warm Teal |
| Accent | oklch(0.72 0.16 85) — Marigold |
| Near-black | oklch(0.12 0.015 265) |
| Near-white | oklch(0.96 0.012 265) |

### Semantic Boxes
keybox (key findings), methodbox (process), warningbox (caveats), tipbox (recommendations), quotebox (citations), infobox (supplementary)

### Layout Classes
`.two-col`, `.three-col`, `.sidebar-left`, `.sidebar-right`, `.comparison`

## STEP 3: AI Slop Test

**This check applies to ALL design work.** Before finalizing any design output, verify:

> "If you showed this deck to someone and said 'AI made this,' would they believe you immediately? If yes, that's the problem."

Quick checklist:
- [ ] Custom theme applied (not default Reveal.js)?
- [ ] Layout variety (not all heading + bullets)?
- [ ] OKLCH colors (no cyan/purple AI palette)?
- [ ] No gradient text?
- [ ] No nested semantic boxes?
- [ ] Specific, compelling title (no placeholders)?
- [ ] Consistent content depth across slides?

## STEP 4: Establish Session Design Context

Synthesize into a working context:

```text
DESIGN CONTEXT ACTIVE:
- Theme: [theme name from YAML or .impeccable-quarto.md]
- Palette: [OKLCH values — custom or default]
- Fonts: [display / body / code]
- Audience: [from .impeccable-quarto.md or "general"]
- Constraints: [max slides, required sections, domain terms]
- AI Slop Guard: ACTIVE
```

This context carries through all subsequent design operations in the session.

## Standalone Output

When invoked by the user directly (not as a dependency):

```markdown
## Design Context Report

### Project Configuration
- .impeccable-quarto.md: [found/not found]
- Theme: [theme details]
- Custom palette: [yes/no + details]

### Active Design System
- Typography: [stack]
- Colors: [palette summary]
- Layout classes: [available]
- Semantic boxes: [available]

### AI Slop Guard: [ACTIVE/INACTIVE]

### Recommendation
[If .impeccable-quarto.md is missing, suggest /teach-style]
[If theme is default, suggest applying impeccable.scss]
```
