---
name: write-notes
description: "Generate or update speaker notes: talking points, timing cues, transitions"
user-invocable: true
argument-hint: "[file]"
---

# /write-notes — Speaker Notes Generator

[MANDATORY PREPARATION]
- Read `.claude/rules/source-translation.md` for speaker notes standards
- Read `.claude/rules/quality-gates.md` — missing notes is MAJ-01 (-5 per slide)
- Read the target `.qmd` file completely
- Identify the presentation's topic, audience, and estimated talk duration
- If `.impeccable-quarto.md` exists, read it for audience context and language preferences

[IMPLEMENTATION STEPS]
1. **Inventory Existing Notes**
   - List all slides and mark which have `::: {.notes}` blocks
   - For slides with existing notes, assess quality: do they expand on slide content or merely repeat it?
   - Calculate: total slides, slides with notes, slides needing notes

2. **Determine Talk Parameters**
   - Estimate ~1-2 minutes per content slide
   - Total slides x 1.5 min = approximate talk length
   - Allocate time budget per section proportionally

3. **Generate Notes for Each Content Slide**
   For each slide missing notes (or with low-quality notes), write:
   - **Opening line**: How to introduce this slide (transition from previous)
   - **Key talking points**: 2-4 bullet points expanding on visible content
   - **Supporting detail**: Data, context, or examples not on the slide
   - **Timing cue**: Approximate time to spend on this slide
   - **Transition hint**: How to lead into the next slide

4. **Skip Title/Section Slides**
   - Title slides: Brief welcome note only
   - Section header slides: 1-line transition note only
   - Q&A slides: Suggested questions to seed if audience is quiet

5. **Consistency Pass**
   - Ensure notes don't repeat slide text verbatim
   - Verify all notes follow the same structure and voice
   - Check total estimated time matches target talk duration
   - Ensure technical terms in notes match those on slides

6. **Word Budget**
   - Target: 80-150 words per content slide
   - Minimum: 40 words (enough for 2 talking points)
   - Maximum: 200 words (beyond this, the slide may need splitting)

[OUTPUT FORMAT]
Apply changes directly to the `.qmd` file by adding/updating `::: {.notes}` blocks.

After applying, report:
```
## Notes Summary: <filename>
- Total slides: N
- Notes added: N
- Notes updated: N
- Estimated talk duration: ~MM minutes
- Average words per note: N
```

[ANTI-PATTERNS TO AVOID]
- Do NOT repeat slide text verbatim in notes — notes must expand, not echo
- Do NOT write notes in a different voice than the slide content
- Do NOT add notes to purely decorative or transition slides unless they need timing cues
- Do NOT exceed 200 words per slide — if you need more, the slide has too much content

[QUALITY CHECKS]
- Every content slide has a `::: {.notes}` block
- Notes contain talking points, not a script to read verbatim
- At least one timing cue exists per section
- Transition hints connect consecutive slides
- Total estimated duration is within 10% of target talk length
