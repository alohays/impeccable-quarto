# Slide Patterns Reference — Impeccable Quarto Design System

## Overview

This reference catalogs common slide types with layout recipes, Quarto markup, and design guidance. Each pattern solves a specific communication need. Choose the pattern that matches your content, not the one that looks most impressive.

## Pattern 1: Title Slide

### Purpose

First impression. Establishes topic, speaker, and visual tone.

### Layout

```
┌──────────────────────────────────────┐
│                                      │
│  Title (3xl, bold, primary-dark)     │
│  Subtitle (lg, neutral-500)          │
│                                      │
│  Author Name (base, neutral-700)     │
│  Affiliation (sm, neutral-500)       │
│  Date (sm, neutral-500)              │
│                                      │
└──────────────────────────────────────┘
```

### Quarto Markup

```yaml
---
title: "Your Title Here"
subtitle: "A Supporting Line"
author: "Your Name"
date: today
---
```

### DO

- Keep the title under 8 words
- Use subtitle for context, not a second sentence
- Left-align (the Impeccable default) — it's more readable than centered

### DON'T

- Include logos, institutional branding, or decorative images
- Use more than 2 lines for the title
- Add an abstract or summary — save that for the next slide

## Pattern 2: Section Header

### Purpose

Visual break between major sections. Signals a topic shift.

### Layout

```
┌──────────────────────────────────────┐
│                                      │
│                                      │
│  Section Title (2xl, primary)        │
│  ─────────────── (accent underline)  │
│                                      │
│                                      │
└──────────────────────────────────────┘
```

### Quarto Markup

```markdown
## Section Title {.section-header}
```

### DO

- Use section headers to give the audience a mental reset
- Keep to 2-4 words
- Add an optional one-line description below if needed

### DON'T

- Use section headers for every slide — reserve for major topic shifts
- Add content below the section title on the same slide
- Number sections in the heading (use progress bar instead)

## Pattern 3: Content Slide (Single Column)

### Purpose

The workhorse. Present a single idea with supporting text.

### Layout

```
┌──────────────────────────────────────┐
│  Heading (xl)                        │
│                                      │
│  Body paragraph or list              │
│  - Point one                         │
│  - Point two                         │
│  - Point three                       │
│                                      │
│  [Optional: semantic box]            │
└──────────────────────────────────────┘
```

### Guidelines

- Maximum 5 bullet points per slide
- Each bullet: 1 line, maximum 2 lines
- One idea per slide — if you have two ideas, use two slides
- End with a takeaway box (`.keybox`) when appropriate

### DO

- Lead with the heading as a complete thought ("Performance improved 3x" not "Performance")
- Keep bullets parallel in structure (all start with verbs, or all are noun phrases)
- Use fragments to reveal bullets as you discuss them

### DON'T

- Write full sentences as bullets
- Use sub-bullets (nested lists)
- Exceed 5 bullets — this is a wall of text, not a slide

## Pattern 4: Two-Column Comparison

### Purpose

Show two related concepts side by side. Before/after, problem/solution, option A/option B.

### Layout

```
┌──────────────────────────────────────┐
│  Heading (xl)                        │
│  ┌───────────┐   ┌───────────┐      │
│  │ Left col  │   │ Right col │      │
│  │ content   │   │ content   │      │
│  │           │   │           │      │
│  └───────────┘   └───────────┘      │
└──────────────────────────────────────┘
```

### Quarto Markup

```markdown
## Heading

:::: {.two-col}
::: {.div}
### Left Topic
Content here
:::

::: {.div}
### Right Topic
Content here
:::
::::
```

### For Explicit Before/After

```markdown
:::: {.comparison}
::: {.compare-left}
### Before
- Old approach details
:::

::: {.compare-right}
### After
- New approach details
:::
::::
```

### DO

- Keep columns balanced in content volume
- Use comparison (`.comparison`) for explicit good/bad contrasts
- Label columns clearly with subheadings

### DON'T

- Put unrelated content in adjacent columns
- Create drastically unbalanced columns (one with 3 lines, one with 15)
- Nest columns within columns

## Pattern 5: Three-Column Feature/KPI

### Purpose

Present three parallel items: features, metrics, steps, or options.

### Layout

```
┌──────────────────────────────────────┐
│  Heading (xl)                        │
│  ┌─────────┐ ┌─────────┐ ┌────────┐ │
│  │ Item 1  │ │ Item 2  │ │ Item 3 │ │
│  │         │ │         │ │        │ │
│  └─────────┘ └─────────┘ └────────┘ │
└──────────────────────────────────────┘
```

### Quarto Markup

```markdown
## Heading

:::: {.three-col}
::: {.div}
### Feature A
Description
:::

::: {.div}
### Feature B
Description
:::

::: {.div}
### Feature C
Description
:::
::::
```

### DO

- Use exactly three items — the pattern is designed for three
- Keep each item to 3-5 lines maximum
- Use semantic boxes (`.methodbox`, `.keybox`) inside columns for visual grouping

### DON'T

- Force a fourth item into three columns
- Use three columns for items of very different lengths
- Make columns too content-heavy — three columns means each one must be concise

## Pattern 6: Data/Results Table

### Purpose

Present structured data, experimental results, or comparisons.

### Quarto Markup

```markdown
## Results

| Method | Accuracy | Speed | Memory |
|--------|----------|-------|--------|
| Baseline | 82.3% | 1.2s | 4.1GB |
| Method A | 87.1% | 0.8s | 3.2GB |
| **Ours** | **91.4%** | **0.6s** | **2.8GB** |
```

### DO

- Bold the winning/important row
- Keep tables to 5-7 rows maximum
- Right-align numeric columns for easy comparison
- Include units in the header, not in every cell
- Use `.smaller` class for tables with many columns

### DON'T

- Present more than 7 rows — summarize or link to full data
- Use tables when a chart would communicate the pattern better
- Forget to highlight the key finding (bold, color, or note)

## Pattern 7: Quote/Attribution

### Purpose

Feature a memorable quote, testimonial, or guiding principle.

### Quarto Markup (semantic box)

```markdown
::: {.quotebox}
"The best developer experience is one where the tool disappears."

[— Someone, Somewhere]{.attribution}
:::
```

### Quarto Markup (blockquote)

```markdown
> "The best developer experience is one where the tool disappears."
>
> — Someone, Somewhere
```

### DO

- Keep quotes under 30 words
- Always provide attribution
- Use the `.quotebox` class for styled quotes in the Impeccable system
- Give the quote its own slide or prominent position

### DON'T

- Use long quotes (> 2 sentences) — paraphrase instead
- Use quotes without attribution
- Stack multiple quotes on one slide

## Pattern 8: Impact/Statement Slide

### Purpose

Maximum visual impact for a single number, statement, or insight. Used in lightning talks and key moments.

### Layout

```
┌──────────────────────────────────────┐
│                                      │
│            [Big Number]              │
│            [Label]                   │
│                                      │
└──────────────────────────────────────┘
```

### Quarto Markup (Lightning theme)

```markdown
::: {.impact}
::: {.impact-number}
47%
:::
::: {.impact-label}
Reduction in deployment time
:::
:::
```

### DO

- One number or one statement per slide
- Use for the single most important finding
- Let whitespace do the work — nothing else on the slide
- Pair with a speaker note that provides context

### DON'T

- Use impact slides more than 2-3 times per deck
- Add supplementary text, footnotes, or citations to the same slide
- Use for numbers that aren't genuinely impressive

## Pattern 9: Sidebar + Content

### Purpose

Main content with a supporting sidebar (callout box, summary, image).

### Quarto Markup

```markdown
## Heading

:::: {.sidebar-right}
::: {.div}
### Main Content
Extended discussion here with full paragraphs
and detailed explanation.
:::

::: {.keybox}
**Key Takeaway**

The essential point summarized in 1-2 sentences.
:::
::::
```

### DO

- Put the narrative in the main area, the takeaway in the sidebar
- Use `.sidebar-right` for takeaway boxes
- Use `.sidebar-left` for navigation labels or category markers

### DON'T

- Put the most important content in the sidebar — it's secondary by position
- Use sidebar layout when both columns have equal importance (use `.two-col` instead)

## Pattern 10: Code + Explanation

### Purpose

Show code alongside a description or annotation. Common in tech talks.

### Quarto Markup

```markdown
## Feature Name

:::: {.two-col}
::: {.div}
### What It Does

Brief explanation of the code behavior,
why it matters, and what to look for.

::: {.tipbox}
**Key Insight**

The non-obvious part that makes this interesting.
:::
:::

::: {.div}
```python
def example_function(data):
    result = process(data)
    return optimize(result)
```
:::
::::
```

### DO

- Put explanation on the left, code on the right (reading order)
- Highlight the key lines with comments or by keeping code minimal
- Use `.tipbox` to call out the non-obvious insight
- Keep code blocks to 15 lines maximum — extract the relevant portion

### DON'T

- Show full files — extract only the relevant function or section
- Use code without explanation — the audience needs context
- Reduce code font size below 20px to fit more lines

## Choosing the Right Pattern

| Communication Need | Pattern |
|-------------------|---------|
| Introduce the topic | Title Slide |
| Signal a new section | Section Header |
| Explain one concept | Content (Single Column) |
| Compare two things | Two-Column Comparison |
| Present three parallel items | Three-Column Feature |
| Show structured data | Data/Results Table |
| Feature a memorable phrase | Quote/Attribution |
| Maximize impact of one number | Impact/Statement |
| Main content + supporting detail | Sidebar + Content |
| Show and explain code | Code + Explanation |
