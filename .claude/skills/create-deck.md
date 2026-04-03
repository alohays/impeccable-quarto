---
name: create-deck
description: "Create a new presentation from any source material (paper, doc, outline, topic)"
user-invocable: true
argument-hint: "[topic/source]"
---

# /create-deck — New Presentation Creator

[MANDATORY PREPARATION]
- Load design context: Read `.claude/skills/slide-design.md` and follow Steps 1-3 to establish design context
- Read `.claude/rules/design-standards.md` for all design standards
- Read `.claude/rules/anti-patterns.md` for all anti-patterns to avoid
- Read `.claude/rules/source-translation.md` for source material conversion rules
- Read `.impeccable-quarto.md` if it exists for style preferences
- Determine source type: topic (from scratch), paper (PDF/URL), document, outline, or raw text
- If source is a file, read it completely. If URL, fetch it.

[IMPLEMENTATION STEPS]
1. **Analyze Source Material**
   - Topic: Research key points, structure a narrative arc
   - Paper: Extract core contribution, methodology, key figures, conclusions
   - Document: Distill to key messages, identify natural section breaks
   - Outline: Validate structure, identify where visuals are needed
   - Apply rules from `source-translation.md`

2. **Plan the Deck Structure**
   - Define the narrative arc: Hook → Problem → Solution → Evidence → Conclusion
   - Allocate slides: ~1 slide per minute of talk time
   - Plan section breaks
   - Identify which slides need: text only, image + text, diagram, chart, quote

3. **Create YAML Frontmatter**
   ```yaml
   ---
   title: "Presentation Title"
   subtitle: "Optional Subtitle"
   author: "Author Name"
   date: today
   format:
     revealjs:
       theme: [default, custom.scss]
       slide-number: true
       transition: fade
       width: 1920
       height: 1080
   ---
   ```

4. **Build Slides**
   - Title slide with strong visual identity
   - Section breaks between major topics
   - One idea per slide
   - Include speaker notes for every slide
   - Use `.columns` for image + text layouts
   - Use `.fragment` for progressive reveals where it helps

5. **Create Theme File**
   - If no theme exists, create a minimal `custom.scss` with:
     - OKLCH color palette (no pure black/white)
     - Font imports (heading + body)
     - Tinted neutral backgrounds
     - Basic custom property definitions

6. **Validate**
   - Run `quarto render` to ensure compilation
   - Check against design standards
   - Verify no anti-patterns present
   - Confirm slide count is appropriate for time slot

[ANTI-PATTERNS TO AVOID]
- Do NOT create bullet-point walls — use visual variety
- Do NOT use default RevealJS theme without customization
- Do NOT dump all source content onto slides
- Do NOT skip speaker notes
- Do NOT create slides without visual anchors

[QUALITY CHECKS]
- File compiles without errors
- Every slide has a visual anchor
- One idea per slide
- Speaker notes present for all slides
- Color palette is cohesive (≤5 hues, OKLCH, no pure black/white)
- Typography follows design standards (≥24px body)
- Narrative arc is clear and compelling
