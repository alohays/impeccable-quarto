# Impeccable-Original: Deep Pattern Analysis

**Date:** 2026-04-03
**Source:** `.context/references/impeccable-original/`
**Scope:** Patterns NOT covered in existing reviews (01-06)

---

## 1. Reference Documents as LLM Conditioning

The `reference/` subdirectories in impeccable-original serve a dual purpose: human documentation AND implicit LLM training data. When a skill like `/typeset` runs, the typography reference primes the model toward specific, non-generic recommendations.

### Key Reference Knowledge Missing from impeccable-quarto

**Typography:**
- Vertical rhythm as mathematical foundation: "If body text has line-height: 1.5 on 16px (= 24px), spacing values should be multiples of 24px"
- Fallback font metrics override: `size-adjust`, `ascent-override`, `descent-override`, `line-gap-override` via Fontaine
- Dark mode font weight compensation: "Increase line-height by 0.05-0.1 for light text on dark backgrounds"
- OpenType features: `font-variant-numeric: tabular-nums`, `font-variant-caps: all-small-caps`

**Color:**
- Chroma reduction at extremes: "High chroma at extreme lightness looks garish"
- Alpha transparency as design smell: "Heavy use of transparency usually means an incomplete palette"
- 60-30-10 rule: "About visual weight, not pixel count. Accent works because it's rare."
- Dangerous combos: "Gray text on colored backgrounds — gray looks washed out and dead on color"

**Motion:**
- 100/300/500 Rule: 100-150ms (instant feedback), 200-300ms (state changes), 300-500ms (layout changes)
- Exit durations: ~75% of enter duration
- 80ms threshold: "Our brains buffer sensory input for ~80ms to synchronize perception"
- Two-property rule: "ONLY animate transform and opacity"
- Exponential easing over bounce: "Bounce was trendy in 2015 but now feels tacky"

## 2. Mandatory Context Gathering with Cascading Fallbacks

Every design skill in impeccable-original follows a THREE-TIER fallback:
1. Check current instructions
2. Check `.impeccable.md` file
3. **MUST run /teach-impeccable** (hard halt if no context)

This prevents the most common failure mode: skills running without design context, producing generic output.

## 3. Phase-Based Skill Architecture (4-Phase Pattern)

Complex skills follow:
- **Phase 1: Assessment** — Gather info, identify problems, score systematically
- **Phase 2: Presentation** — Format findings (tables, severity ratings)
- **Phase 3: Ask the User** — 2-4 targeted questions grounded in actual findings (NOT generic questions)
- **Phase 4: Recommended Actions** — Prioritized, scoped, only after user feedback

Key: "Do NOT ask generic 'who is your audience?' questions — every question must reference specific findings from Phase 2."

## 4. Severity Scoring with Rating Bands

- 0-4 scoring per dimension, with named bands: "18-20 Excellent", "14-17 Good", "10-13 Acceptable"
- Every finding tagged **[P0-P3]**: P0=Blocking, P1=Major, P2=Minor, P3=Polish
- Named bands create human-readable outcomes beyond raw numbers

## 5. Skill Chain Pattern

```
Diagnostic → Correction → Finishing
/critique, /audit → /animate, /quieter, /bolder, etc. → /polish (always last)
```

Every skill chain ends with `/polish` as the final step.

## 6. The Intentionality Principle

The core philosophy is not "typography-first" but **intentionality-first**:
- "Bold ≠ Chaotic. Bold means intentional drama with constraints."
- "Minimalism ≠ Bland. Refined minimalism requires meticulous attention."
- Both extremes work — the key is **intentionality, not intensity**.
- "Match implementation complexity to aesthetic vision."
