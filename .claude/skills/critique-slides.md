---
name: critique-slides
description: "UX/design review: visual hierarchy, cognitive load, emotional resonance, scoring"
user-invocable: true
argument-hint: "[file]"
---

# /critique-slides — Design & UX Critique

[MANDATORY PREPARATION]
- Read `.claude/rules/design-standards.md` for design principles
- Read `.claude/rules/anti-patterns.md` for known bad patterns
- Read `.claude/rules/quality-gates.md` for scoring criteria
- If `.impeccable-quarto.md` exists in project root, read it for style preferences
- Read the target `.qmd` file completely before starting critique

[IMPLEMENTATION STEPS]
1. **Visual Hierarchy Assessment**
   - Does each slide have a clear focal point?
   - Is the heading hierarchy consistent and meaningful?
   - Are visual weights (size, color, position) guiding the eye correctly?
   - Score: Strong / Adequate / Weak per slide

2. **Cognitive Load Evaluation**
   - Count information units per slide (aim for 1 key idea per slide)
   - Check text density: flag slides with >40 words of body text
   - Evaluate whether visuals support or compete with the message
   - Flag "content dump" slides that try to say too much

3. **Emotional Resonance**
   - Does the color palette evoke the intended mood?
   - Are transitions/animations purposeful or distracting?
   - Does the opening slide create engagement?
   - Does the closing slide provide a clear takeaway?

4. **Flow & Narrative**
   - Does the slide sequence tell a coherent story?
   - Are transitions between sections smooth?
   - Is there a clear beginning → middle → end arc?
   - Flag any slides that feel out of place in the sequence

5. **Typography Review**
   - Is font pairing harmonious?
   - Are heading sizes creating clear hierarchy?
   - Is body text readable at projection distance (≥24px)?
   - Check for typographic anti-patterns: all-caps abuse, excessive bold, inconsistent weights

6. **Color & Contrast**
   - Is the palette cohesive (≤5 primary colors)?
   - Are colors used semantically (not randomly)?
   - Is there sufficient contrast for readability?
   - Flag pure black (#000) or pure white (#FFF) — prefer tinted neutrals

7. **Anti-Pattern Scan**
   - Check against every pattern in `anti-patterns.md`
   - Flag each violation with its severity and the specific anti-pattern name

[OUTPUT FORMAT]
```
## Design Critique: <filename>
**Overall Score: XX/100** — <verdict>

### Strengths
- What works well (be specific)

### Visual Hierarchy: X/10
- Findings...

### Cognitive Load: X/10
- Findings...

### Emotional Resonance: X/10
- Findings...

### Flow & Narrative: X/10
- Findings...

### Anti-Pattern Violations
- Pattern name — Slide N — Severity

### Recommendations (prioritized)
1. Highest impact improvement
2. ...
```

[ANTI-PATTERNS TO AVOID]
- Do NOT modify any files — this is a read-only diagnostic skill
- Do NOT be vague ("make it better") — every critique must be specific and actionable
- Do NOT ignore cultural context or audience when critiquing
- Do NOT conflate personal taste with design principles

[QUALITY CHECKS]
- Every critique point references a specific slide
- Strengths are identified, not just weaknesses
- Recommendations are prioritized by impact
- Score aligns with the severity of findings
