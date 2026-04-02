# Theme & Design System Analysis

**Analyst:** theme-design-analyst
**Date:** 2026-04-03
**Sources analyzed:**
- `impeccable-original` — 7 frontend design reference files (color, typography, spatial, motion, responsive, interaction, UX writing)
- `paper2pr` — 2 Quarto RevealJS themes (clean-academic.scss, suny-career.scss) + compat CSS
- `impeccable-quarto` — Our current theme (themes/impeccable.scss)

---

## 1. OKLCH Color System

### What impeccable-original recommends

The color-and-contrast reference establishes several principles we partially follow:

1. **Chroma reduction at extremes**: "As you move toward white or black, reduce chroma. High chroma at extreme lightness looks garish." Our neutral scale does this (chroma 0.008-0.015), but our semantic box backgrounds use fixed low chroma (e.g., `oklch(0.95 0.04 85)`) without systematic derivation.

2. **Two-layer token architecture**: Primitive tokens (`--blue-500`) and semantic tokens (`--color-primary: var(--blue-500)`). For dark mode, only redefine the semantic layer. **We don't do this at all** — our dark mode manually overrides every color individually.

3. **Alpha is a design smell**: "Heavy use of transparency usually means an incomplete palette." paper2pr's themes use `rgba()` extensively (e.g., `rgba($primary-gold, 0.12)`, `rgba(0, 0, 0, 0.06)`). Our theme correctly avoids this in semantic boxes by using explicit OKLCH backgrounds, but our dark mode code block shadow uses `oklch(0 0 0 / 0.3)` which is fine.

4. **60-30-10 rule**: 60% neutrals, 30% secondary, 10% accent. Our theme follows this naturally — neutral backgrounds dominate, text colors provide secondary weight, and primary/accent are used sparingly.

### What paper2pr does differently

paper2pr themes use **hex colors exclusively** with no OKLCH at all. Their color choices are institution-driven (`$primary-blue: #012169`), not perceptually optimized. The suny-career theme uses a well-considered dark palette with named semantic variables (`$bg-primary`, `$bg-deep`, `$bg-secondary`, `$text-primary`, `$text-muted`) — good naming, wrong color space.

### Gaps in our implementation

**Gap 1: No CSS custom property layer.** Our theme declares OKLCH only in comments and scattered `oklch()` values in rules. We should have a `:root` block with CSS custom properties using real OKLCH values, and a `[data-theme="dark"]` block that redefines the semantic layer only.

**Gap 2: No systematic palette generation.** The reference describes generating tinted neutrals at a consistent hue with varying lightness and chroma. Our neutral scale does this at hue 265 but the values are manually picked hex approximations. We should use actual `oklch()` in custom properties.

**Gap 3: Surface elevation tokens missing.** The reference describes `--surface-1`, `--surface-2`, `--surface-3` for dark mode depth. We use flat backgrounds.

### Recommended SCSS improvements

```scss
/*-- scss:rules --*/

// CSS Custom Properties — the canonical OKLCH values
// Sass variables (hex) exist for Quarto/Reveal.js internals that need them.
// All authored styles should reference these custom properties.

:root {
  // --- Palette primitives ---
  --color-primary: oklch(0.45 0.18 265);
  --color-primary-light: oklch(0.65 0.12 265);
  --color-primary-lighter: oklch(0.85 0.06 265);
  --color-primary-dark: oklch(0.30 0.15 265);

  --color-secondary: oklch(0.55 0.12 195);
  --color-secondary-light: oklch(0.75 0.08 195);

  --color-accent: oklch(0.72 0.16 85);
  --color-accent-light: oklch(0.88 0.10 85);

  --color-success: oklch(0.60 0.15 145);
  --color-warning: oklch(0.72 0.16 85);
  --color-danger: oklch(0.55 0.18 25);
  --color-info: oklch(0.55 0.12 240);

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

  // --- Semantic tokens (what the UI actually references) ---
  --bg-surface: var(--neutral-50);
  --bg-surface-raised: var(--neutral-100);
  --bg-surface-sunken: var(--neutral-200);
  --text-primary: var(--neutral-900);
  --text-secondary: var(--neutral-700);
  --text-muted: var(--neutral-500);
  --text-heading: var(--neutral-950);
  --border-default: var(--neutral-200);
  --border-subtle: var(--neutral-100);
}

// Dark mode: only redefine the semantic layer
[data-theme="dark"] .reveal,
.reveal.dark-mode {
  --bg-surface: var(--neutral-900);
  --bg-surface-raised: var(--neutral-800);
  --bg-surface-sunken: var(--neutral-950);
  --text-primary: var(--neutral-200);
  --text-secondary: var(--neutral-400);
  --text-muted: var(--neutral-500);
  --text-heading: var(--neutral-50);
  --border-default: var(--neutral-700);
  --border-subtle: var(--neutral-800);
}
```

---

## 2. Typography Depth

### What impeccable-original recommends (and we're missing)

**2a. Vertical rhythm.** "Your line-height should be the base unit for ALL vertical spacing." Our base is 28px with line-height 1.55, giving a rhythm unit of ~43px. But our spacing (`$blockMargin: 1.2em`, `$headingMargin: 0 0 0.6em 0`) doesn't align to this rhythm. This matters less in slides than in long-form text, but consistent spacing still looks cleaner.

**2b. OpenType features.** The reference lists several features we should enable:

```scss
// We have this:
.reveal {
  font-feature-settings: "kern" 1, "liga" 1, "calt" 1;
}

// We should also have:
.reveal table {
  font-variant-numeric: tabular-nums;  // Aligned numbers in data tables
}

.reveal code {
  font-variant-ligatures: none;  // Disable ligatures in code
}

.reveal .smallest,
.reveal figcaption {
  font-variant-caps: all-small-caps;  // Optional: for abbreviations
}
```

**2c. Font loading strategy.** The reference describes `font-display: swap` and fallback metric matching. Our theme doesn't address font loading at all — it depends on Quarto's default behavior. For `embed-resources: true` decks this is fine, but for web-hosted presentations, we should add `@font-face` declarations with `font-display: swap`.

**2d. Fluid type.** The reference distinguishes between using fluid type for display text ("headings on marketing pages") vs. fixed scales for "app UIs, dashboards, data-dense interfaces." Slides are fixed-dimension (1920x1080), so our fixed scale is **correct** — no `clamp()` needed. Good.

**2e. Dark mode text weight.** "Reduce font weight for light text on dark backgrounds. The perceived weight is lighter." We don't do this. Our dark mode should reduce body weight slightly:

```scss
[data-theme="dark"] .reveal,
.reveal.dark-mode {
  // Light text on dark looks heavier — compensate
  p, li {
    font-weight: 350;  // Instead of default 400
  }
}
```

### What paper2pr does well

- clean-academic uses `font-weight: 300` for body text — too light for projection but shows awareness of weight tuning
- suny-career pairs **Instrument Serif** (display) with **Pretendard** (body) — genuine contrast between serif headlines and sans body. This is the "contrast on multiple axes" the reference recommends. Our Plus Jakarta Sans / Source Sans 3 pairing is good but both are sans-serif, providing less structural contrast.
- suny-theme-compat.css enables `font-feature-settings: 'kern' 1, 'liga' 1, 'tnum' 1` and uses `font-variant-numeric: tabular-nums` on stat values — exactly what the reference recommends.

### Our strengths

- Our 3-font stack (display/body/code) is well-chosen and distinctive per the reference's advice
- 1.25 Major Third scale ratio is solid
- 28px base is appropriate for projection
- Letter-spacing on headings (`-0.02em`) shows typographic awareness

### Recommended improvements

```scss
// Add tabular numbers to data-heavy elements
.reveal table {
  font-variant-numeric: tabular-nums;
}

// Disable ligatures in code (JetBrains Mono has ligatures by default)
.reveal code,
.reveal pre code {
  font-variant-ligatures: none;
}

// Dark mode: reduce perceived weight of light-on-dark text
[data-theme="dark"] .reveal p,
[data-theme="dark"] .reveal li {
  font-weight: 350;
}
```

---

## 3. Spatial Design

### What the reference teaches

**3a. 4pt base grid, not 8pt.** "8pt systems are too coarse — you'll frequently need 12px." Our spacing is in `em` units relative to font size, which is fine for slides. But we don't have a consistent spacing scale. Our current values:

| Element | Spacing | Effective px (at 28px base) |
|---------|---------|---------------------------|
| `$blockMargin` | `1.2em 0` | ~34px |
| `$headingMargin` | `0 0 0.6em 0` | ~17px |
| `$slide-padding` | `40px 60px` | 40/60px |
| Semantic box padding | `1em 1.5em` | 28/42px |
| Semantic box margin | `1em 0` | 28px |
| Grid gap (two-col) | `2.5em` | 70px |

These are reasonable but ad-hoc. A formal spacing scale would be:

```scss
// Spacing scale (4px base, em-relative for slide context)
$space-2xs: 0.14em;  //  ~4px
$space-xs:  0.28em;  //  ~8px
$space-sm:  0.43em;  // ~12px
$space-md:  0.57em;  // ~16px
$space-lg:  0.86em;  // ~24px
$space-xl:  1.14em;  // ~32px
$space-2xl: 1.71em;  // ~48px
$space-3xl: 2.28em;  // ~64px
```

**3b. Container queries.** The reference advocates `container-type: inline-size` for component-level responsiveness. In RevealJS at a fixed 1920x1080, container queries have limited utility — but they could be useful for semantic boxes that appear in different column layouts. A box in a `sidebar-left` column is narrower than in a full-width slide.

**3c. Visual hierarchy through multiple dimensions.** "The best hierarchy uses 2-3 dimensions at once." Our heading hierarchy uses size + weight + color — good. But our body text and list items use the same color (`$neutral-800`), weight (400), and only differ by context. We could improve:

```scss
// Stronger hierarchy between body text and supporting text
.reveal p {
  color: var(--text-primary);
}

.reveal li {
  color: var(--text-secondary);  // Slightly lighter than body paragraphs
}
```

**3d. Optical alignment.** "Text at margin-left: 0 looks indented due to letterform whitespace." Our headings could benefit from a small negative left margin for optical alignment, but this is a micro-refinement.

### What paper2pr does

- Uses float-based layouts (`.col-left`, `.col-right`) — outdated; our grid-based approach is better
- Provides `.compact` utility class for tighter spacing — we should consider this
- Has `.spaced-list` for extra-spaced lists — useful for emphasis slides

### Recommended additions

```scss
// Compact layout utility (reduces spacing within a container)
.reveal .compact {
  p { margin-top: 0.3em; margin-bottom: 0.3em; }
  ul, ol {
    margin-top: 0.25em; margin-bottom: 0.4em;
    li { margin-bottom: 0.2em; line-height: 1.35; }
  }
  .keybox, .methodbox, .warningbox, .tipbox, .infobox {
    padding: 0.6em 1em;
    margin: 0.5em 0;
  }
}

// Spaced list utility (extra breathing room for emphasis)
.reveal .spaced-list li {
  margin-bottom: 1.2em;
}
```

---

## 4. Motion Design

### What the reference teaches (and we're almost entirely missing)

This is our **biggest gap**. The reference provides a comprehensive motion system that our theme barely touches.

**4a. Duration taxonomy.** Our fragments use a single `0.4s` duration. The reference recommends:

| Duration | Use Case |
|----------|----------|
| 100-150ms | Instant feedback (button press, toggle) |
| 200-300ms | State changes (menu, tooltip, hover) |
| 300-500ms | Layout changes (accordion, modal) |
| 500-800ms | Entrance animations (page load, hero) |

**4b. Easing curves.** We use `ease` universally. The reference says: "Don't use ease. It's a compromise that's rarely optimal." Recommended:

```scss
// Motion tokens
:root {
  // Durations
  --duration-instant: 100ms;
  --duration-fast: 200ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;

  // Easings (exponential curves for natural feel)
  --ease-out: cubic-bezier(0.25, 1, 0.5, 1);      // Elements entering
  --ease-in: cubic-bezier(0.7, 0, 0.84, 0);        // Elements leaving
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);   // State toggles
}
```

**4c. Exit animations faster than entrances.** "Use ~75% of enter duration." Our fragments don't differentiate between entering and leaving states.

**4d. Staggered animations.** The reference describes CSS custom property-based stagger: `animation-delay: calc(var(--i, 0) * 50ms)`. This would be powerful for progressive list reveals:

```scss
// Staggered fragment animation
.reveal .slides section .fragment[style*="--i"] {
  transition-delay: calc(var(--i, 0) * 60ms);
}
```

Usage in `.qmd`:
```markdown
::: {.fragment style="--i: 0"}
First item appears
:::
::: {.fragment style="--i: 1"}
Second item follows
:::
```

**4e. Only animate transform and opacity.** We follow this correctly — our fragments only use `opacity` and `transform`.

**4f. Reduced motion.** We handle this but could be more nuanced. The reference says to preserve functional animations (progress indicators) while removing spatial motion. Our current approach (`transition: none; opacity: 1; transform: none;`) removes everything. Better:

```scss
@media (prefers-reduced-motion: reduce) {
  .reveal .slides section .fragment {
    // Replace motion with a quick crossfade
    transition: opacity 150ms ease-out;
    transform: none !important;

    &.visible {
      opacity: 1;
    }
  }

  // Keep progress bar functional
  .reveal .progress span {
    transition: width 200ms ease-out;
  }
}
```

### What paper2pr does

paper2pr themes have **no animation definitions at all** — they rely entirely on Reveal.js defaults. This is a missed opportunity.

### Recommended additions

```scss
// ============================================================================
// MOTION TOKENS
// ============================================================================

:root {
  --duration-instant: 100ms;
  --duration-fast:    200ms;
  --duration-normal:  350ms;
  --duration-slow:    500ms;

  --ease-out:    cubic-bezier(0.25, 1, 0.5, 1);
  --ease-in:     cubic-bezier(0.7, 0, 0.84, 0);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
}

// Updated fragment animations using motion tokens
.reveal .slides section .fragment {
  opacity: 0;
  transition: opacity var(--duration-normal) var(--ease-out),
              transform var(--duration-normal) var(--ease-out);

  &.visible {
    opacity: 1;
  }
}

.reveal .slides section .fragment.slide-up {
  transform: translateY(20px);
  opacity: 0;

  &.visible {
    transform: translateY(0);
    opacity: 1;
  }
}

.reveal .slides section .fragment.scale-in {
  transform: scale(0.92);
  opacity: 0;

  &.visible {
    transform: scale(1);
    opacity: 1;
  }
}

// Stagger support: set --i on each fragment for sequential delay
.reveal .slides section .fragment[style*="--i"] {
  transition-delay: calc(var(--i, 0) * 60ms);
}

// Nuanced reduced motion
@media (prefers-reduced-motion: reduce) {
  .reveal .slides section .fragment {
    transition: opacity 150ms ease-out;
    transform: none !important;
  }

  .reveal .slides section .fragment[style*="--i"] {
    transition-delay: 0ms;
  }
}
```

---

## 5. Responsive Patterns

### Relevance to RevealJS

Most of the responsive reference (mobile-first, breakpoints, srcset) is **not applicable** to fixed-dimension RevealJS presentations. However, several concepts are relevant:

**5a. Input method detection.** The reference describes `@media (pointer: fine)` vs `(pointer: coarse)` and `@media (hover: hover)` vs `(hover: none)`. This matters for presentations viewed on touch devices:

```scss
// Touch-friendly controls when viewing on tablets
@media (pointer: coarse) {
  .reveal .controls {
    font-size: 14px;  // Larger touch targets
  }

  .reveal .slide-number {
    font-size: 16px;
    padding: 8px;
  }
}

// Only show hover effects when hover is supported
@media (hover: hover) {
  .reveal table tbody tr:hover {
    background: $primary-lighter;
  }
}

@media (hover: none) {
  .reveal table tbody tr:hover {
    background: inherit;
  }
}
```

**5b. Container queries for components.** Semantic boxes in narrow column contexts (sidebar layouts) could adapt:

```scss
// Semantic boxes adapt to container width
.reveal .sidebar-left,
.reveal .sidebar-right {
  > * {
    container-type: inline-size;
  }
}

@container (max-width: 500px) {
  .keybox, .methodbox, .warningbox, .tipbox, .infobox {
    padding: 0.6em 1em;
    font-size: 0.88em;
  }
}
```

### What paper2pr does

No responsive considerations at all. Fixed dimensions assumed throughout.

---

## 6. Tinted Neutrals Sophistication

### Comparison

| Aspect | impeccable-original reference | Our implementation | Gap? |
|--------|------|----|----|
| Hue source | "Add a subtle hint of your brand hue" | Hue 265 (indigo, matching primary) | No gap |
| Chroma range | "0.005-0.01 is enough" | 0.008-0.015 | Slightly higher but intentional |
| Scale steps | "9-11 shade scale" | 11 steps (950-50) | No gap |
| Chroma curve | Not specified but implied: reduce at extremes | Near-flat (0.008-0.015 range) | Minor gap: could be more sophisticated |
| Color space | "Use OKLCH" | Hex (Sass) + OKLCH (CSS) | Gap: dual maintenance |

### Sophistication improvement

The chroma in our neutral scale could follow a gentle curve — slightly more chroma in the mid-tones where it's most perceptible, less at extremes:

```
950: L=0.12, C=0.012  (dark: less chroma, more subtle)
900: L=0.18, C=0.014
800: L=0.25, C=0.015
700: L=0.35, C=0.014
600: L=0.45, C=0.012
500: L=0.55, C=0.010  (mid: balanced)
400: L=0.65, C=0.010
300: L=0.75, C=0.010
200: L=0.85, C=0.010
100: L=0.92, C=0.010
 50: L=0.96, C=0.008  (light: less chroma)
```

This is a micro-refinement. Our current scale is already solid.

---

## 7. Design Tokens vs. SCSS Variables

### The reference's recommendation

The reference advocates a two-layer system:
1. **Primitive tokens**: Raw values named by attribute (`--blue-500`, `--size-lg`)
2. **Semantic tokens**: Purpose-named references (`--color-primary`, `--text-heading`)

This enables theme switching (dark mode, alternate brands) by only remapping the semantic layer.

### Our current approach

We use Sass variables only, with no CSS custom property layer. This means:
- Dark mode requires manually overriding every visual property
- No runtime theming is possible
- Brand variants would require separate SCSS files
- Our OKLCH values exist only in comments (not usable in CSS)

### paper2pr's approach

paper2pr also uses Sass variables only, but suny-career.scss shows a cleaner semantic naming pattern: `$bg-primary`, `$bg-deep`, `$bg-secondary`, `$text-primary`, `$text-muted`. This is halfway to a token system.

### Recommended token architecture

```scss
/*-- scss:defaults --*/
// Sass variables for Quarto/Reveal.js internals (these stay as-is)
$primary: #3730a3;
// ... existing hex vars for backward compat ...

/*-- scss:rules --*/
// Layer 1: Primitive tokens (raw OKLCH values)
:root {
  --oklch-indigo-45: oklch(0.45 0.18 265);
  --oklch-indigo-65: oklch(0.65 0.12 265);
  // ... full palette ...
}

// Layer 2: Semantic tokens (what components reference)
:root {
  --color-primary: var(--oklch-indigo-45);
  --color-link: var(--color-primary);
  --bg-surface: var(--neutral-50);
  --text-body: var(--neutral-800);
  --text-heading: var(--neutral-950);
  // ... etc ...
}

// Dark mode: remap semantic layer only
[data-theme="dark"] .reveal {
  --bg-surface: var(--neutral-900);
  --text-body: var(--neutral-300);
  --text-heading: var(--neutral-50);
  --color-link: var(--oklch-indigo-65);
}

// Components use semantic tokens
.reveal p { color: var(--text-body); }
.reveal h2 { color: var(--text-heading); }
```

This would **drastically simplify our dark mode** section (currently 100 lines of manual overrides) to ~20 lines of token remapping.

---

## 8. Patterns from paper2pr Worth Adopting

### 8a. Quotebox with decorative quote mark

paper2pr's clean-academic.scss has a `::before` pseudo-element with a large quote mark:

```scss
.quotebox {
  &::before {
    content: "\201C";
    font-size: 2.5em;
    color: rgba($primary-gold, 0.4);
    position: absolute;
    left: 0.15em;
    top: -0.1em;
    font-style: normal;
    line-height: 1;
  }
}
```

Our quotebox is plainer. Adding a subtle decorative quote mark would elevate it without violating "no purposeless decoration" — the quote mark signals "this is a quote" which is functional.

### 8b. Heading underline via pseudo-element

paper2pr uses `::after` on h2 for a subtle gold underline. Our `.section-header h2` uses `border-bottom` directly. The pseudo-element approach is more controllable (can animate, control width independently).

### 8c. Nested list arrow markers

paper2pr replaces standard nested list bullets with right arrows (`\2192`):

```scss
.reveal ul ul li:before {
  content: "\2192";
  color: $primary-gold;
}
```

This is a nice visual hierarchy signal. Our theme uses default markers for all list levels.

### 8d. Empty heading hiding

suny-career.scss has `.reveal .slides section > h2:first-child:empty { display: none !important; }` — useful when slides use empty h2 as separators with background colors.

### 8e. Focus ring styling

Both paper2pr themes style `:focus` with `outline: 2px solid $primary-gold; outline-offset: 2px;`. Our theme is **missing focus ring styles entirely** — this is an accessibility gap.

```scss
// ADD: Focus ring for keyboard navigation
.reveal a:focus-visible,
.reveal button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

---

## 9. Interaction Design Gaps

The reference covers eight interactive states, focus rings, and keyboard navigation. RevealJS has limited interactivity, but we should cover:

1. **Focus-visible rings** (missing entirely — see 8e above)
2. **Link hover states** (we have these, well done)
3. **Table row hover** (we have these, but should gate behind `@media (hover: hover)`)
4. **Slide control hover** (Reveal.js handles this, but we could customize)

---

## 10. Summary of Priority Improvements

### Critical (should do now)

| # | Improvement | Impact | Effort |
|---|------------|--------|--------|
| 1 | Add CSS custom properties for OKLCH colors | Enables runtime theming, eliminates hex/OKLCH drift | Medium |
| 2 | Add focus-visible ring styles | Accessibility requirement | Low |
| 3 | Add `font-variant-numeric: tabular-nums` to tables | Better data alignment | Low |
| 4 | Disable ligatures in code blocks | Code readability | Low |

### High priority (should do soon)

| # | Improvement | Impact | Effort |
|---|------------|--------|--------|
| 5 | Introduce motion tokens (duration + easing variables) | More natural animations | Low |
| 6 | Replace `ease` with proper easing curves in fragments | Perceptual improvement | Low |
| 7 | Add stagger support for fragments | Powerful progressive disclosure | Low |
| 8 | Gate hover effects behind `@media (hover: hover)` | Touch device support | Low |
| 9 | Dark mode font weight reduction | Better dark mode readability | Low |
| 10 | Improve reduced-motion handling (crossfade instead of instant) | Better accessibility | Low |

### Medium priority (design refinements)

| # | Improvement | Impact | Effort |
|---|------------|--------|--------|
| 11 | Two-layer token architecture (primitive + semantic) | Dramatically simplifies dark mode & future variants | High |
| 12 | Decorative quote mark on quotebox | Visual polish | Low |
| 13 | Nested list arrow markers | Better visual hierarchy | Low |
| 14 | `.compact` utility class | Practical for dense slides | Low |
| 15 | `.spaced-list` utility class | Practical for emphasis slides | Low |

### Low priority (nice to have)

| # | Improvement | Impact | Effort |
|---|------------|--------|--------|
| 16 | Container query support for sidebar layouts | Adaptive boxes | Medium |
| 17 | `@font-face` declarations with `font-display: swap` | Faster web-hosted rendering | Low |
| 18 | Refined neutral chroma curve | Micro-aesthetic improvement | Low |

---

## 11. What We Do Better Than Both References

1. **OKLCH throughout**: Neither paper2pr theme uses OKLCH at all. Our commitment to perceptually uniform color is a genuine differentiator.

2. **Semantic box system**: Our 6-box semantic system (key, method, warning, tip, quote, info) is more comprehensive and better-structured than paper2pr's 8-box system (which has overlapping roles: highlightbox vs keybox vs resultbox).

3. **Grid-based layouts**: Our `grid-template-columns` approach is superior to paper2pr's float-based `.col-left`/`.col-right` pattern.

4. **Dark mode**: We have a complete dark mode implementation. paper2pr's clean-academic has none; suny-career is dark-first but has no light mode toggle.

5. **Reduced motion**: We respect `prefers-reduced-motion`. Neither paper2pr theme does.

6. **Print styles**: We have dedicated print styles. Neither paper2pr theme does.

7. **Type scale**: Our calculated modular scale (`calc(#{$base-size} * #{$scale-ratio})`) is more systematic than paper2pr's ad-hoc `font-size: 1.5em` values.

---

## Appendix: Full Recommended impeccable.scss Diff Summary

The changes above, if all implemented, would:
- Add ~40 lines of CSS custom properties (`:root` block)
- Reduce the dark mode section from ~100 lines to ~30 lines (token remapping)
- Add ~15 lines of motion tokens
- Update ~10 existing transitions to use proper easing curves
- Add ~10 lines of accessibility improvements (focus rings)
- Add ~5 lines of OpenType feature refinements
- Net change: roughly +20 lines (additions offset by dark mode simplification)

The highest-ROI change is **#1 (CSS custom properties)** combined with **#11 (two-layer tokens)**, which would modernize the entire architecture while simplifying maintenance. This is a structural improvement that makes every future enhancement easier.
