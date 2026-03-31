---
name: distill-slides
description: "Strip unnecessary complexity, reduce text, increase clarity"
user-invocable: true
argument-hint: "[file]"
---

# /distill-slides — Simplify & Clarify

[MANDATORY PREPARATION]
- Read `.claude/rules/design-standards.md` (especially max bullets, 1-idea-per-slide)
- Read `.claude/rules/anti-patterns.md` (especially "bullet-point walls" and "content dump")
- Read the target `.qmd` file completely
- Understand the presentation's core message and audience before cutting

[IMPLEMENTATION STEPS]
1. **Identify Overloaded Slides**
   - Flag slides with >5 bullet points
   - Flag slides with >40 words of body text
   - Flag slides trying to convey multiple distinct ideas
   - Flag slides with redundant information

2. **Apply the "One Idea Per Slide" Rule**
   - Split multi-idea slides into separate slides
   - Each slide should have one clear takeaway
   - Move supporting details to speaker notes

3. **Reduce Text**
   - Convert sentences to concise phrases where possible
   - Replace paragraphs with key phrases + speaker notes
   - Remove filler words and redundant qualifiers
   - Turn text-heavy explanations into visuals where feasible

4. **Simplify Visuals**
   - Remove decorative elements that don't support the message
   - Simplify complex diagrams (can they be split across slides?)
   - Ensure every visual element earns its space

5. **Preserve Information**
   - Move cut content to speaker notes — don't delete information
   - Ensure the narrative flow still works after distillation
   - Verify key data points and citations are preserved

6. **Validate**
   - Re-read the distilled version: does it still convey the full message?
   - Check that no critical information was lost
   - Verify the slide count is reasonable for the time slot

[ANTI-PATTERNS TO AVOID]
- Do NOT delete information without moving it to speaker notes
- Do NOT distill to the point of losing meaning
- Do NOT remove all personality — concise doesn't mean sterile
- Do NOT split slides excessively (avoid "death by 1000 slides")

[QUALITY CHECKS]
- No slide has >5 bullet points
- No slide has >40 words of body text (excluding speaker notes)
- Each slide conveys exactly one key idea
- All cut content is preserved in speaker notes
- The narrative arc remains coherent
