---
name: proofread-slides
description: "Proofread for grammar, typos, terminology consistency, and style"
user-invocable: true
argument-hint: "[file]"
---

# /proofread-slides — Grammar & Consistency Checker

[MANDATORY PREPARATION]
- Read the target `.qmd` file completely, including speaker notes
- If `.impeccable-quarto.md` exists, check for terminology preferences and language settings
- Note the language of the presentation (English, Korean, mixed, etc.)

[IMPLEMENTATION STEPS]
1. **Spelling & Grammar**
   - Check all visible text for spelling errors
   - Check all visible text for grammar issues
   - Check speaker notes for spelling and grammar
   - Flag homophone confusion (their/there/they're, its/it's, etc.)

2. **Terminology Consistency**
   - Build a glossary of key terms used in the deck
   - Flag inconsistencies: same concept called different names on different slides
   - Flag inconsistent abbreviation usage (spelled out on some slides, abbreviated on others)
   - Check capitalization of proper nouns and technical terms is consistent

3. **Punctuation & Style**
   - Check bullet point punctuation is consistent (all periods, or no periods)
   - Check heading capitalization style is consistent (Title Case or Sentence case)
   - Flag inconsistent use of em-dashes, en-dashes, and hyphens
   - Check quote marks are consistent (curly vs straight)
   - Flag double spaces or other spacing anomalies

4. **Number & Date Formatting**
   - Check number formatting is consistent (1,000 vs 1000)
   - Check date formatting is consistent
   - Check percentage formatting (50% vs 50 percent)
   - Flag significant figures inconsistency in reported data

5. **Cross-Language Issues** (if applicable)
   - Flag mixed-language text that may confuse the audience
   - Check romanization consistency for non-Latin terms
   - Verify translation accuracy for bilingual slides

6. **Academic Quality** (if academic presentation)
   - Check citation format is consistent
   - Verify figure/table numbering is sequential
   - Check that all referenced figures/tables exist
   - Flag claims without attribution or evidence

[OUTPUT FORMAT]
```
## Proofread Report: <filename>

### Issues Found: N total (N critical, N minor)

### Spelling/Grammar
| Slide | Issue | Suggestion |
|-------|-------|------------|
| N | "recieve" | "receive" |

### Consistency Issues
| Issue | Occurrences | Recommendation |
|-------|-------------|----------------|
| "machine learning" vs "ML" | Slides 3, 5, 8 vs 12, 15 | Use "machine learning" first, then "ML" consistently |

### Punctuation/Style
| Issue | Slides Affected | Fix |
|-------|----------------|-----|
| Mixed bullet punctuation | 3, 7, 12 | Remove trailing periods from all bullets |

### Summary
- Slides checked: N
- Issues found: N
- Auto-fixable: N
```

[ANTI-PATTERNS TO AVOID]
- Do NOT modify files — this is a read-only diagnostic skill
- Do NOT flag style preferences as errors (e.g., Oxford comma is a preference, not an error)
- Do NOT rewrite content — only flag issues and suggest corrections
- Do NOT flag intentional informal language in speaker notes as errors

[QUALITY CHECKS]
- Every issue references a specific slide number
- Suggestions are concrete (show the corrected text)
- Consistency issues list all affected slides
- The report distinguishes critical errors (wrong words) from minor style issues
