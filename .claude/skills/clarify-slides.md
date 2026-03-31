---
name: clarify-slides
description: "Improve text: headings, labels, speaker notes quality"
user-invocable: true
argument-hint: "[file]"
---

# /clarify-slides — Text Clarity Improvement

[MANDATORY PREPARATION]
- Read `.claude/rules/design-standards.md` for heading hierarchy rules
- Read `.impeccable-quarto.md` if it exists for tone/voice preferences
- Read the target `.qmd` file completely
- Understand the audience and their expertise level

[IMPLEMENTATION STEPS]
1. **Headings Audit**
   - Every slide must have a clear, informative heading
   - Headings should be action-oriented or question-based where appropriate
   - Replace vague headings ("Overview", "Details", "Misc") with specific ones
   - Ensure heading hierarchy is consistent (H2 for slides, H3 for sub-sections)

2. **Label Clarity**
   - All chart axes, legends, and data labels must be clear
   - Abbreviations should be defined on first use
   - Technical jargon should be appropriate for the audience level
   - Ensure figure captions are descriptive

3. **Body Text Improvement**
   - Replace passive voice with active where possible
   - Eliminate jargon that the audience won't understand
   - Make bullet points parallel in grammatical structure
   - Ensure each bullet starts with an action verb or key noun

4. **Speaker Notes Enhancement**
   - Add speaker notes where missing
   - Notes should expand on slide content, not repeat it
   - Include transition phrases ("Now let's look at...", "This leads us to...")
   - Add timing suggestions for key sections
   - Include anticipated questions and answers

5. **Consistency Check**
   - Terminology must be consistent throughout (don't alternate between synonyms)
   - Tone should be consistent (formal/informal — pick one)
   - Abbreviation usage should be consistent after first definition

[ANTI-PATTERNS TO AVOID]
- Do NOT rewrite in your own voice — preserve the author's tone
- Do NOT add unnecessary verbosity while "clarifying"
- Do NOT change technical terms that the audience would expect
- Do NOT make speaker notes into full scripts — they should be prompts

[QUALITY CHECKS]
- Every slide has a specific, meaningful heading
- All labels and captions are clear and complete
- Body text is concise and parallel in structure
- Speaker notes exist for all substantive slides
- Terminology is consistent throughout
