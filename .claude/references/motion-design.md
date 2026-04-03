# Motion Design Reference — Impeccable Quarto Design System

## Philosophy

Motion in presentations should be **invisible infrastructure**. Good transitions guide attention without the audience noticing they're being guided. Bad transitions call attention to themselves and away from your content.

The Impeccable system favors **subtle, fast, purposeful** motion. No bounces. No spins. No zoom-throughs.

## Slide Transitions

### Default: Fade

```yaml
# In YAML frontmatter
format:
  revealjs:
    transition: fade
    transition-speed: default
    background-transition: fade
```

Fade is the safest and most professional transition. It creates a gentle shift between slides without implying directional movement or hierarchy.

### Available Transitions

| Transition | Effect | When to Use | When NOT to Use |
|-----------|--------|-------------|-----------------|
| `fade` | Cross-dissolve | Default for all presentations | — |
| `slide` | Horizontal slide | Sequential/timeline content | Academic, formal |
| `none` | Instant switch | Rapid-fire slides, lightning talks | Standard pacing |
| `convex` | 3D rotation | Never recommended | Always |
| `concave` | 3D rotation inward | Never recommended | Always |
| `zoom` | Scale in/out | Never recommended | Always |

### DO

- Use `fade` as the default. It works everywhere.
- Use `none` for lightning talks where speed matters
- Keep the same transition throughout the entire deck

### DON'T

- Mix different transitions within a single deck
- Use 3D transitions (convex, concave, zoom) — they look gimmicky
- Use `slide` transition for non-sequential content

## Transition Speed

| Speed | Duration | Use Case |
|-------|----------|----------|
| `fast` | ~400ms | Lightning talks, rapid pacing |
| `default` | ~600ms | Standard presentations |
| `slow` | ~800ms | Never recommended — feels sluggish |

### Rule

Match transition speed to presentation pacing. If you're spending 1-2 minutes per slide, `default` is fine. If slides are 15-30 seconds, use `fast` or `none`.

## Fragment Animations

Fragments are elements that appear progressively within a single slide. They're the most common form of motion in presentations.

### Built-in Fragment Types

The Impeccable system provides these custom fragment animations:

#### Standard Fade-In (default)

```markdown
::: {.fragment}
This text fades in smoothly.
:::
```

CSS: `opacity: 0 → 1` over 0.35–0.4s with `ease` timing.

#### Slide-Up

```markdown
::: {.fragment .slide-up}
This text slides up while fading in.
:::
```

CSS: `translateY(20px) + opacity 0 → translateY(0) + opacity 1` over 0.35–0.4s.

Use for: lists, sequential points, building up an argument.

#### Scale-In

```markdown
::: {.fragment .scale-in}
This element scales in from 92% to 100%.
:::
```

CSS: `scale(0.92) + opacity 0 → scale(1) + opacity 1` over 0.3–0.4s.

Use for: emphasizing a key point, revealing a conclusion.

#### Fade-In Smooth (explicit)

```markdown
::: {.fragment .fade-in-smooth}
Explicit smooth fade.
:::
```

Same as default fragment but explicitly named for clarity in markup.

### Fragment Timing by Theme

| Theme | Duration | Translate Distance | Character |
|-------|----------|--------------------|-----------|
| Default | 0.4s | 20px | Balanced |
| Academic | 0.35s | 15px | Subtle, restrained |
| Corporate | 0.35s | 18px | Clean, professional |
| Creative | 0.3s | 24px | Energetic |
| Lightning | 0.25s | 30px | Snappy, immediate |

### Fragment Ordering

```markdown
::: {.fragment fragment-index=1}
First to appear
:::

::: {.fragment fragment-index=2}
Second to appear
:::

::: {.fragment fragment-index=2}
Also second (same index = simultaneous)
:::
```

### DO

- Use fragments to build a narrative — reveal points as you discuss them
- Keep fragment count to 3-5 per slide maximum
- Use `slide-up` for lists and sequential content
- Reveal the conclusion last (`.keybox` as the final fragment)

### DON'T

- Make every element a fragment — it slows the pacing and feels heavy
- Use fragments for decorative effect (flying, spinning, bouncing)
- Have more than 5 fragment steps per slide — split into multiple slides instead
- Mix different animation types on the same slide (all slide-up OR all fade-in, not both)

## Auto-Animate

Reveal.js auto-animate smoothly transitions elements that exist on consecutive slides:

```yaml
format:
  revealjs:
    auto-animate: true
    auto-animate-easing: ease
    auto-animate-duration: 0.6
```

### Usage

```markdown
## Step 1 {auto-animate=true}

- First point

## Step 1 {auto-animate=true}

- First point
- Second point (smoothly appears)
```

### DO

- Use auto-animate for progressive build-up of diagrams or lists
- Keep the same heading text between auto-animated slides for visual continuity
- Use for before/after comparisons where elements shift position

### DON'T

- Over-rely on auto-animate — it adds complexity to the markup
- Auto-animate between slides with completely different content
- Combine auto-animate with fragment animations on the same content

## Reduced Motion Support

The Impeccable system respects `prefers-reduced-motion`:

```scss
@media (prefers-reduced-motion: reduce) {
  .reveal .slides section .fragment {
    transition: none;
    opacity: 1;
    transform: none;
  }
}
```

When this media query is active:

- All fragments are immediately visible (no animation)
- Slide transitions become instant
- Auto-animate is disabled

### Why This Matters

- Approximately 25% of users have motion sensitivity settings enabled
- Vestibular disorders can cause physical discomfort from screen motion
- Reduced motion mode should still deliver the full content, just without animation

### DO

- Test your presentation with `prefers-reduced-motion: reduce` enabled
- Ensure content makes sense without fragment ordering (flat layout should still be logical)
- Keep animation as enhancement, not information — nothing should be lost without it

### DON'T

- Use motion to convey meaning that isn't available in static form
- Assume all audience members can see your animations

## Timing and Easing

### Easing Curves

| Curve | CSS | Usage |
|-------|-----|-------|
| `ease` | `ease` | Default for all transitions |
| `ease-out` | `ease-out` | Elements entering the viewport |
| `ease-in-out` | `ease-in-out` | Auto-animate position changes |

### DO

- Use `ease` for everything unless you have a specific reason not to
- Keep all animations under 0.5s — presentations aren't loading screens

### DON'T

- Use `linear` easing — it feels mechanical and unnatural
- Use `ease-in` for entering elements — they start slow and speed up, which feels wrong
- Use bounce, elastic, or spring easing — they belong in UI, not in presentations
- Add delays to fragment animations — they make the speaker wait awkwardly

## Animation Performance

### Best Practices

- **Animate only `opacity` and `transform`** — these properties are GPU-accelerated and don't cause layout reflow
- Avoid animating `width`, `height`, `margin`, `padding`, or `top`/`left`
- Keep the number of simultaneously animating elements under 10
- Test on the actual presentation hardware — conference laptops may be underpowered

### In the Impeccable System

All fragment animations use only `opacity` and `transform` (translate, scale). This ensures:

- 60fps animation on all modern hardware
- No layout thrashing
- Smooth performance even with large code blocks or images
