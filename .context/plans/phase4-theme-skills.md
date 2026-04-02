# Phase 4: Theme & Skills Enhancement — Implementation Plan

**Date:** 2026-04-03
**Status:** Planning
**Dependencies:** Phase 1-3 (SSOT fix, hooks, CI/CD) are independent; this phase can start in parallel.
**Source analysis:** 03-theme-design-analysis.md, 02-skill-design-analysis.md, 00-synthesis.md

---

## Work Item 1: CSS Custom Properties + Two-Layer Token Architecture

**Files to modify:**
- `themes/impeccable.scss` (primary target, ~796 lines currently)

**Complexity:** L (Large) — architectural refactor touching the entire theme
**Estimated net change:** +60 lines (new `:root` block), -70 lines (dark mode simplification) = ~-10 net

### 1.1 Add `:root` Block with Primitive Tokens

Insert after line 110 (`/*-- scss:rules --*/`) and before the BASE STYLES section (line 112).

**Before** (line 110-113):
```scss
/*-- scss:rules --*/

// ============================================================================
// BASE STYLES
```

**After:**
```scss
/*-- scss:rules --*/

// ============================================================================
// DESIGN TOKENS — CSS Custom Properties (OKLCH canonical values)
// ============================================================================
// Layer 1: Primitive tokens — raw OKLCH palette values.
// Layer 2: Semantic tokens — what the UI actually references.
// Sass variables ($primary, etc.) remain for Quarto/Reveal.js internals
// that need hex. All authored styles should use var(--token-name).

:root {
  // --- Palette primitives (Layer 1) ---
  --color-primary:         oklch(0.45 0.18 265);
  --color-primary-light:   oklch(0.65 0.12 265);
  --color-primary-lighter: oklch(0.85 0.06 265);
  --color-primary-dark:    oklch(0.30 0.15 265);

  --color-secondary:       oklch(0.55 0.12 195);
  --color-secondary-light: oklch(0.75 0.08 195);

  --color-accent:          oklch(0.72 0.16 85);
  --color-accent-light:    oklch(0.88 0.10 85);

  --color-success:         oklch(0.60 0.15 145);
  --color-warning:         oklch(0.72 0.16 85);
  --color-danger:          oklch(0.55 0.18 25);
  --color-info:            oklch(0.55 0.12 240);

  // --- Neutral scale (hue 265, tinted) ---
  --neutral-950: oklch(0.12 0.015 265);
  --neutral-900: oklch(0.18 0.015 265);
  --neutral-800: oklch(0.25 0.015 265);
  --neutral-700: oklch(0.35 0.012 265);
  --neutral-600: oklch(0.45 0.010 265);
  --neutral-500: oklch(0.55 0.008 265);
  --neutral-400: oklch(0.65 0.008 265);
  --neutral-300: oklch(0.75 0.008 265);
  --neutral-200: oklch(0.85 0.010 265);
  --neutral-100: oklch(0.92 0.012 265);
  --neutral-50:  oklch(0.96 0.012 265);

  // --- Semantic tokens (Layer 2) ---
  --bg-surface:        var(--neutral-50);
  --bg-surface-raised: var(--neutral-100);
  --bg-surface-sunken: var(--neutral-200);
  --text-heading:      var(--neutral-950);
  --text-primary:      var(--neutral-900);
  --text-body:         var(--neutral-800);
  --text-secondary:    var(--neutral-700);
  --text-muted:        var(--neutral-500);
  --border-default:    var(--neutral-200);
  --border-subtle:     var(--neutral-100);
  --color-link:        var(--color-primary);
  --color-link-hover:  var(--color-primary-light);

  // --- Semantic box backgrounds (light mode) ---
  --box-bg-key:     oklch(0.95 0.04 85);
  --box-bg-method:  var(--color-primary-lighter);
  --box-bg-warning: oklch(0.95 0.04 25);
  --box-bg-tip:     oklch(0.95 0.04 145);
  --box-bg-info:    oklch(0.95 0.03 240);
  --box-bg-quote:   var(--neutral-100);
}

// ============================================================================
// BASE STYLES
```

### 1.2 Simplify Dark Mode via Token Remapping

**Before** (lines 648-749, ~100 lines):
```scss
.reveal.dark-mode,
[data-theme="dark"] .reveal {
  background-color: $neutral-900;

  .slides {
    color: $neutral-200;
  }

  h1, h2, h3, h4 {
    color: $neutral-50;
  }

  p, li {
    color: $neutral-300;
  }

  strong {
    color: $neutral-100;
  }
  // ... ~80 more lines of individual overrides ...
}
```

**After** (~35 lines — semantic token remapping + remaining box overrides):
```scss
// ============================================================================
// DARK MODE — Token Remapping
// ============================================================================
// Only redefine the semantic layer. Primitive tokens stay the same.

.reveal.dark-mode,
[data-theme="dark"] .reveal {
  // Surface & text
  --bg-surface:        var(--neutral-900);
  --bg-surface-raised: var(--neutral-800);
  --bg-surface-sunken: var(--neutral-950);
  --text-heading:      var(--neutral-50);
  --text-primary:      var(--neutral-200);
  --text-body:         var(--neutral-300);
  --text-secondary:    var(--neutral-400);
  --text-muted:        var(--neutral-500);
  --border-default:    var(--neutral-700);
  --border-subtle:     var(--neutral-800);
  --color-link:        var(--color-primary-light);
  --color-link-hover:  var(--color-primary);

  // Semantic box backgrounds (dark mode)
  --box-bg-key:     oklch(0.22 0.03 85);
  --box-bg-method:  oklch(0.22 0.03 265);
  --box-bg-warning: oklch(0.22 0.03 25);
  --box-bg-tip:     oklch(0.22 0.03 145);
  --box-bg-info:    oklch(0.22 0.03 240);
  --box-bg-quote:   var(--neutral-800);

  // Remaining element-specific overrides not capturable by tokens
  background-color: var(--bg-surface);

  pre {
    background: var(--neutral-950);
    box-shadow: 0 4px 20px oklch(0 0 0 / 0.3);
  }

  table thead th {
    background: var(--color-primary-dark);
  }

  .comparison .compare-left {
    background: oklch(0.22 0.03 25);
  }

  .comparison .compare-right {
    background: oklch(0.22 0.03 145);
  }
}
```

### 1.3 Update Existing Rules to Use Semantic Tokens

This is a progressive migration. Key changes:

```scss
// BEFORE (scattered throughout)
.reveal p, .reveal li { color: $neutral-800; }
.reveal strong { color: $neutral-950; }
.reveal blockquote { background: $neutral-100; color: $neutral-700; }

// AFTER
.reveal p, .reveal li { color: var(--text-body); }
.reveal strong { color: var(--text-heading); }
.reveal blockquote { background: var(--bg-surface-raised); color: var(--text-secondary); }
```

Migrate these selectors to use `var()`:
- `.reveal p, .reveal li` → `var(--text-body)`
- `.reveal strong` → `var(--text-heading)`
- `.reveal em` → `var(--text-secondary)`
- `.reveal a` → `var(--color-link)`
- `.reveal blockquote` → `var(--bg-surface-raised)`, `var(--text-secondary)`
- `.reveal code` → `var(--bg-surface-raised)`, `var(--color-primary-dark)`
- `.reveal table tbody td` → `var(--text-body)`, `var(--border-default)`
- `.reveal .keybox` → `var(--box-bg-key)`
- `.reveal .methodbox` → `var(--box-bg-method)`
- `.reveal .warningbox` → `var(--box-bg-warning)`
- `.reveal .tipbox` → `var(--box-bg-tip)`
- `.reveal .infobox` → `var(--box-bg-info)`
- `.reveal .quotebox` → `var(--box-bg-quote)`
- Title slide: `$primary-dark` → `var(--color-primary-dark)`, etc.

**Important:** Keep `$primary`, `$neutral-*` Sass variables in `scss:defaults` for Quarto internals that need hex (e.g., `lighten()`, `darken()`, `rgba()`). Only migrate color references in authored rules.

### Acceptance Criteria
- [ ] `:root` block contains all OKLCH primitive tokens and semantic tokens
- [ ] Dark mode section reduced from ~100 lines to ~35 lines via token remapping
- [ ] All semantic box backgrounds use `var(--box-bg-*)` tokens
- [ ] Text colors use `var(--text-*)` tokens throughout authored rules
- [ ] Sass hex variables remain in `scss:defaults` for Quarto internals
- [ ] Theme compiles without errors: `quarto render examples/demo.qmd` (or any test file)
- [ ] Light mode visual output is identical to before (pixel-level regression check)
- [ ] Dark mode visual output is identical to before

---

## Work Item 2: Motion & Accessibility Enhancements

**Files to modify:**
- `themes/impeccable.scss` (add motion tokens, update transitions, add accessibility rules)

**Complexity:** M (Medium) — localized additions and updates
**Estimated change:** +50 lines added, ~10 lines modified

### 2.1 Add Motion Tokens to `:root` Block

Add inside the `:root` block from Work Item 1 (or at the end of it):

```scss
  // --- Motion tokens ---
  --duration-instant: 100ms;
  --duration-fast:    200ms;
  --duration-normal:  350ms;
  --duration-slow:    500ms;

  --ease-out:    cubic-bezier(0.25, 1, 0.5, 1);      // Elements entering
  --ease-in:     cubic-bezier(0.7, 0, 0.84, 0);       // Elements leaving
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);      // State toggles
```

### 2.2 Update All Transitions to Use Motion Tokens

**Before** (line 169):
```scss
.reveal a {
  transition: color 0.2s ease, text-decoration-color 0.2s ease;
}
```

**After:**
```scss
.reveal a {
  transition: color var(--duration-fast) var(--ease-out),
              text-decoration-color var(--duration-fast) var(--ease-out);
}
```

**Before** (lines 518-525, fragment animations):
```scss
.reveal .slides section .fragment {
  opacity: 0;
  transition: opacity 0.4s ease, transform 0.4s ease;

  &.visible {
    opacity: 1;
  }
}
```

**After:**
```scss
.reveal .slides section .fragment {
  opacity: 0;
  transition: opacity var(--duration-normal) var(--ease-out),
              transform var(--duration-normal) var(--ease-out);

  &.visible {
    opacity: 1;
  }
}
```

Apply same pattern to `.fragment.slide-up`, `.fragment.scale-in`, `.fragment.fade-in-smooth`.

### 2.3 Add Fragment Stagger Support

Add after the existing fragment animations (~line 556):

```scss
// Stagger support: set --i on each fragment for sequential delay
// Usage: ::: {.fragment style="--i: 0"} ... ::: {.fragment style="--i: 1"}
.reveal .slides section .fragment[style*="--i"] {
  transition-delay: calc(var(--i, 0) * 60ms);
}
```

### 2.4 Add Focus-Visible Ring Styles

Add new section after the PROGRESS BAR & CONTROLS section (~line 643):

```scss
// ============================================================================
// FOCUS & ACCESSIBILITY
// ============================================================================

.reveal a:focus-visible,
.reveal button:focus-visible,
.reveal .controls button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
  border-radius: 2px;
}
```

### 2.5 Add font-variant-numeric for Tables

**Before** (line 562):
```scss
.reveal table {
  border-collapse: collapse;
  width: 100%;
  font-size: 0.88em;
  margin: 1em 0;
}
```

**After:**
```scss
.reveal table {
  border-collapse: collapse;
  width: 100%;
  font-size: 0.88em;
  margin: 1em 0;
  font-variant-numeric: tabular-nums;
}
```

### 2.6 Disable Code Block Ligatures

**Before** (line 212):
```scss
.reveal code {
  font-family: $font-family-code;
  font-size: $codeFontSize;
  background: $neutral-100;
  padding: 0.15em 0.4em;
  border-radius: 4px;
  color: $primary-dark;
}
```

**After:**
```scss
.reveal code {
  font-family: $font-family-code;
  font-size: $codeFontSize;
  background: $neutral-100;
  padding: 0.15em 0.4em;
  border-radius: 4px;
  color: $primary-dark;
  font-variant-ligatures: none;
}
```

### 2.7 Gate Table Hover Behind @media (hover: hover)

**Before** (line 589):
```scss
.reveal table tbody tr:hover {
  background: $primary-lighter;
}
```

**After:**
```scss
@media (hover: hover) {
  .reveal table tbody tr:hover {
    background: $primary-lighter;
  }
}
```

Also wrap the dark mode table hover:
```scss
// In dark mode section:
@media (hover: hover) {
  table tbody tr:hover {
    background: oklch(0.25 0.02 265);
  }
}
```

### 2.8 Improve Reduced Motion Handling

**Before** (lines 785-795):
```scss
@media (prefers-reduced-motion: reduce) {
  .reveal .slides section .fragment {
    transition: none;
    opacity: 1;
    transform: none;
  }

  .reveal .slide-transition {
    transition: none;
  }
}
```

**After:**
```scss
@media (prefers-reduced-motion: reduce) {
  .reveal .slides section .fragment {
    // Replace spatial motion with a quick crossfade
    transition: opacity var(--duration-fast) var(--ease-out);
    transform: none !important;

    &.visible {
      opacity: 1;
    }
  }

  .reveal .slides section .fragment[style*="--i"] {
    transition-delay: 0ms;
  }

  .reveal .slide-transition {
    transition: none;
  }

  // Keep progress bar functional
  .reveal .progress span {
    transition: width var(--duration-fast) var(--ease-out);
  }
}
```

### 2.9 Dark Mode Font Weight Reduction

Add inside the dark mode section:

```scss
// Light text on dark backgrounds appears heavier — compensate
p, li {
  font-weight: 350;
}
```

### Acceptance Criteria
- [ ] Motion tokens (3 durations, 3 easings) defined in `:root`
- [ ] All `ease` values in transitions replaced with proper cubic-bezier tokens
- [ ] Fragment stagger works: `style="--i: N"` produces incremental delay
- [ ] `focus-visible` ring visible when tabbing through links/buttons
- [ ] Table numbers align properly with `tabular-nums`
- [ ] Code blocks show `!=` as two characters, not a ligature
- [ ] Table row hover only activates on hover-capable devices
- [ ] Reduced motion shows crossfade instead of instant appear
- [ ] Dark mode body text renders slightly lighter weight (350 vs 400)
- [ ] Theme compiles without errors

---

## Work Item 3: New Skills

**Files to create:**
- `.claude/skills/write-notes.md`
- `.claude/skills/proofread-slides.md`
- `.claude/skills/challenge-deck.md`

**Complexity:** M (Medium) — 3 new files following established patterns
**Dependencies:** None (independent of theme changes)

### 3.1 `/write-notes` — Speaker Notes Generator

**File:** `.claude/skills/write-notes.md`

```markdown
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
```

### 3.2 `/proofread-slides` — Grammar & Consistency Checker

**File:** `.claude/skills/proofread-slides.md`

```markdown
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
```

### 3.3 `/challenge-deck` — Devil's Advocate Review

**File:** `.claude/skills/challenge-deck.md`

```markdown
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
   - Trace the logical flow from problem → evidence → conclusion
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
```

### Acceptance Criteria (All 3 Skills)
- [ ] Each skill follows the standard structure: frontmatter → MANDATORY PREPARATION → IMPLEMENTATION STEPS → OUTPUT FORMAT → ANTI-PATTERNS TO AVOID → QUALITY CHECKS
- [ ] Frontmatter has `name`, `description`, `user-invocable: true`, `argument-hint`
- [ ] `/write-notes` modifies files (adds `::: {.notes}` blocks); `/proofread-slides` and `/challenge-deck` are read-only
- [ ] Each skill references the appropriate rules files in MANDATORY PREPARATION
- [ ] OUTPUT FORMAT templates are parseable and consistent with other skills' output

---

## Work Item 4: Deck-Level Anti-Patterns

**Files to modify:**
- `.claude/rules/anti-patterns.md` (add new section)
- `.claude/rules/quality-gates.md` (add corresponding deductions)

**Complexity:** S (Small) — additive content to existing files
**Dependencies:** None

### 4.1 Add Deck-Level Anti-Patterns Section to `anti-patterns.md`

Append after the "Technical Anti-Patterns" section (after line 134):

```markdown
## Deck-Level Anti-Patterns

### AP-DK01: Monotonous Pacing
- **Detection:** >70% of slides share the same structural template (e.g., heading + bullet list). No variation in slide types (text, image, comparison, data, quote, section break).
- **Severity:** Major
- **Why it's bad:** Uniform structure is hypnotic in the worst way. The audience's attention flatlines when every slide looks the same. Variety in structure signals "pay attention, something new is happening."
- **Fix:** Alternate slide types: text slides, image slides, comparison layouts, data visualizations, quote slides, and section breaks. Aim for no more than 3 consecutive slides with the same structure.

### AP-DK02: Missing Arc
- **Detection:** The deck lacks a clear beginning (motivation/hook), middle (evidence/argument), and end (conclusion/takeaway). No section breaks or transition slides divide the content.
- **Severity:** Major
- **Why it's bad:** Without narrative structure, the presentation is a list of facts, not an argument. The audience can't tell where they are in the story or why they should care.
- **Fix:** Structure as Context → Problem → Approach → Results → Takeaway. Add section header slides between major parts. The first content slide should establish *why this matters*; the last should state *what to do about it*.

### AP-DK03: Depth Inconsistency
- **Detection:** One section gets 8+ slides while a parallel section of equal importance gets 1-2 slides. Slide count ratio between the longest and shortest non-intro sections exceeds 4:1.
- **Severity:** Major
- **Why it's bad:** Signals the presenter ran out of time, preparation, or interest. The audience infers that shallow sections are unimportant, even if they're crucial.
- **Fix:** Rebalance by splitting overly detailed sections into essentials (slides) and details (speaker notes), or expanding thin sections with supporting evidence, examples, or visuals.

### AP-DK04: Orphan Section
- **Detection:** A section with only 1 content slide (excluding the section header).
- **Severity:** Minor
- **Why it's bad:** A section with one slide doesn't justify being a section. It either needs more content or should be merged into an adjacent section.
- **Fix:** Expand with supporting content, merge into an adjacent section, or remove the section header and integrate the slide into the flow.

### AP-DK05: Data Without Story
- **Detection:** A chart, table, or data visualization appears without interpretive text (no callout, no "what this means" box, no annotation). The slide title is generic (e.g., "Results", "Data").
- **Severity:** Major
- **Why it's bad:** Data doesn't speak for itself. Without interpretation, the audience must decode the chart alone under time pressure — most won't bother. The presenter's job is to tell the audience *what to see* in the data.
- **Fix:** Add a clear interpretive statement: "Key finding: X increases by Y when Z." Use `.keybox` to highlight the takeaway. Add annotations to the chart if possible. Replace generic titles with insight-driven titles (e.g., "Response time drops 3x with caching" instead of "Performance Results").
```

### 4.2 Add Deck-Level Deductions to `quality-gates.md`

Add a new subsection under "### Major Deductions" table:

```markdown
| MAJ-10 | Monotonous pacing (>70% same structure) | -5 |
| MAJ-11 | Missing narrative arc (no beginning-middle-end) | -8 |
| MAJ-12 | Depth inconsistency (>4:1 section ratio) | -3 per instance |
| MAJ-13 | Data without interpretation | -3 per slide |
```

Add under "### Minor Deductions" table:

```markdown
| MIN-08 | Orphan section (1-slide section) | -1 per instance |
```

### Acceptance Criteria
- [ ] 5 new anti-patterns (AP-DK01 through AP-DK05) added to `anti-patterns.md`
- [ ] Each anti-pattern has: Detection criteria, Severity, "Why it's bad", Fix
- [ ] Corresponding deductions added to `quality-gates.md` with consistent ID scheme
- [ ] Severity ratings are appropriate (Major for audience-impact issues, Minor for structural)
- [ ] Detection criteria are objective and can be evaluated by scanning the `.qmd` file
- [ ] Deduction amounts are proportional to existing patterns (e.g., missing arc at -8 is comparable to generic theme at -10)

---

## Implementation Order & Dependencies

```
Work Item 1 (Tokens)     Work Item 3 (Skills)     Work Item 4 (Anti-Patterns)
     │                         │                          │
     ▼                         ▼                          ▼
Work Item 2 (Motion)     (independent)              (independent)
     │
     ▼
  (depends on :root
   block from WI-1)
```

- **Work Items 3 and 4** are fully independent — can be done in parallel with everything else.
- **Work Item 2** depends on Work Item 1's `:root` block (motion tokens go inside it) and the semantic token migration (dark mode hover needs `var()` references).
- **Recommended execution order:** WI-1 → WI-2 (sequential), WI-3 + WI-4 (parallel with WI-1/2).

---

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| SCSS compilation failure after token refactor | Test with `quarto render` after each sub-step of WI-1 |
| Visual regression in dark mode | Screenshot before/after comparison |
| OKLCH browser support | All modern browsers support OKLCH; Quarto's embed-resources mode uses a modern renderer |
| Skill format inconsistency | Validate against 3 existing skills as templates |
| Anti-pattern deduction conflicts | Cross-check with existing deduction IDs to avoid collisions |

---

## Summary

| Work Item | Files | Complexity | Lines Changed |
|-----------|-------|-----------|---------------|
| 1. CSS Custom Properties + Tokens | `themes/impeccable.scss` | L | +60, -70 |
| 2. Motion & Accessibility | `themes/impeccable.scss` | M | +50, ~10 modified |
| 3. New Skills (3) | `.claude/skills/{write-notes,proofread-slides,challenge-deck}.md` | M | +3 new files (~300 lines total) |
| 4. Deck-Level Anti-Patterns | `.claude/rules/anti-patterns.md`, `.claude/rules/quality-gates.md` | S | +60 lines |

**Total estimated:** ~470 lines of new/modified content across 5 files + 3 new files.
