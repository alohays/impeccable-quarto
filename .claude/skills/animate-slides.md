---
name: animate-slides
description: "Add purposeful fragment animations and transitions"
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

Before animation work, read `.context/references/impeccable-original-deep-patterns.md` section 1 (Motion).
Key rules: 100/300/500ms timing rule, exit = 75% of enter duration, 80ms perception threshold, only animate transform+opacity.

# /animate-slides — Animation Enhancement

[MANDATORY PREPARATION]
- Load design context: Read `.claude/skills/slide-design.md` and follow Steps 1-3 to establish design context
- Read `.claude/rules/design-standards.md` for animation guidelines
- Read `.claude/rules/anti-patterns.md` (especially "too many animations")
- Read the target `.qmd` file completely
- Understand the presentation flow: where does progressive reveal help the narrative?

[IMPLEMENTATION STEPS]
1. **Identify Animation Opportunities**
   - Progressive reveal: bullet lists where each point builds on the previous
   - Before/after comparisons: show "before" first, then reveal "after"
   - Complex diagrams: build up components incrementally
   - Data reveals: show the question, then reveal the answer/data
   - Do NOT animate for decoration — every animation must serve the narrative

2. **Fragment Animations**
   - Use Quarto/RevealJS fragment classes:
     - `.fragment` — basic appear
     - `.fragment .fade-in` — fade in
     - `.fragment .fade-up` — slide up while fading in
     - `.fragment .highlight-current-blue` — highlight the current item
     - `.fragment .semi-fade-out` — dim previous items while showing current
   - Apply consistent fragment style within a section

3. **Slide Transitions**
   - Choose one transition style for the entire deck (consistency)
   - Recommended: `slide` (default), `fade`, or `none`
   - Use `none` for information-dense slides where transitions would distract
   - Section breaks can use a different transition to signal a topic change
   - Set via YAML: `transition: fade` or per-slide with `{transition="fade"}`

4. **Timing & Pacing**
   - Set appropriate transition speed: `transition-speed: default` (usually best)
   - Avoid auto-advance unless this is a kiosk/loop presentation
   - Ensure animations don't make the speaker wait too long
   - Add speaker note reminders: "(click to advance)" where fragments exist

5. **Implementation**
   - Add `.fragment` classes to elements that should reveal progressively
   - Set global transition in YAML frontmatter
   - Use `{.fragment fragment-index=N}` for custom ordering
   - Test the full presentation flow with animations

[ANTI-PATTERNS TO AVOID]
- Do NOT animate every element — use animation sparingly and purposefully
- Do NOT use flashy transitions (zoom, convex, cube) for professional presentations
- Do NOT mix multiple transition styles randomly
- Do NOT use auto-advance timing in speaker-driven presentations
- Do NOT add animations that require >3 clicks per slide

[QUALITY CHECKS]
- Every animation serves a narrative purpose
- Fragment style is consistent within sections
- Transition style is consistent throughout (with intentional exceptions for section breaks)
- No slide requires more than 3 clicks to fully reveal
- Speaker notes mention fragment clicks where relevant
- Animations enhance, not distract from, the content
