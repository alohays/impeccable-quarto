---
name: challenge-deck
description: "Devil's advocate: tough audience questions, logical gaps, unsupported claims"
user-invocable: true
argument-hint: "[file]"
---

# /challenge-deck — Devil's Advocate Review

[MANDATORY PREPARATION]
- Read `.claude/rules/anti-patterns.md` for content-level patterns (AP-C04 Missing Narrative, AP-C02 Content Dump)
- Read the target `.qmd` file completely, including speaker notes
- Identify the presentation's domain, audience, and apparent thesis
- If `.impeccable-quarto.md` exists, read it for audience context

[IMPLEMENTATION STEPS]
1. **Claim Audit**
   - List every factual claim made in the presentation
   - For each claim, assess: Is it supported? By what evidence?
   - Flag claims presented as fact without citation or data
   - Flag statistics without source attribution
   - Rate each claim: Supported / Partially Supported / Unsupported / Unverifiable

2. **Logic & Argument Review**
   - Trace the logical flow from problem -> evidence -> conclusion
   - Flag logical fallacies: false dichotomy, straw man, appeal to authority, etc.
   - Flag non-sequiturs: conclusions that don't follow from the presented evidence
   - Flag missing counterarguments: obvious objections that aren't addressed
   - Check: does the conclusion follow from the evidence presented?

3. **Generate Tough Questions**
   - Write 5-7 questions a skeptical audience member would ask
   - Each question should target a specific slide or claim
   - Include: 2 factual challenges, 2 methodological challenges, 1-2 scope/generalizability challenges, 1 "so what?" question
   - Rate difficulty: Softball / Moderate / Hard / Devastating

4. **Gap Analysis**
   - What's missing? What would a domain expert expect to see that isn't here?
   - Flag assumed knowledge: concepts used without explanation
   - Flag missing context: claims that need more background for the target audience
   - Flag scope gaps: areas the presentation covers shallowly or skips entirely

5. **Bias & Perspective Check**
   - Is the presentation balanced, or does it present only one side?
   - Are there obvious counterarguments that should be acknowledged?
   - Does the framing unfairly favor or disfavor a position?
   - Would a knowledgeable skeptic find this presentation fair?

6. **Robustness Score**
   - Rate overall argument robustness: 1-10
   - 1-3: Significant gaps, would not survive expert Q&A
   - 4-6: Adequate but has addressable weaknesses
   - 7-8: Strong, with minor gaps
   - 9-10: Bulletproof, all major objections preemptively addressed

[OUTPUT FORMAT]
```
## Devil's Advocate Report: <filename>
**Robustness Score: X/10** — <verdict>

### Unsupported Claims
| Slide | Claim | Evidence Status | Recommendation |
|-------|-------|-----------------|----------------|
| N | "X improves Y by 40%" | No citation | Add source or soften language |

### Logical Issues
- Slide N: [description of logical gap]

### Tough Questions (audience simulation)
1. **[Hard]** "On slide N, you claim X, but what about Y?" — Targets: [specific weakness]
2. **[Moderate]** "How does this generalize beyond your specific case?" — Targets: [scope limitation]
3. ...

### Missing Elements
- Expected but absent: [what a domain expert would look for]
- Assumed knowledge: [concepts that need definition for this audience]

### Recommended Strengthening
1. Highest-priority fix (specific suggestion)
2. ...
```

[ANTI-PATTERNS TO AVOID]
- Do NOT modify any files — this is a read-only diagnostic skill
- Do NOT nitpick style or design — focus exclusively on content and argumentation
- Do NOT be contrarian for its own sake — every challenge must be substantive
- Do NOT assume the presenter is wrong — look for genuine gaps, not manufactured ones
- Do NOT challenge domain conventions the presenter can reasonably assume the audience shares

[QUALITY CHECKS]
- Every challenge references a specific slide
- Tough questions are genuinely tough, not trivially answerable from the deck
- The robustness score is consistent with the findings
- Recommendations are actionable (suggest specific additions or changes)
- The review is fair — it acknowledges strengths as well as weaknesses
