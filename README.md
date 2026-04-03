# impeccable-quarto

> **The design vocabulary you didn't know your slides needed.**
> Any source. Any presentation. Impeccable Quarto slides.

**[Live Demo](https://alohays.github.io/impeccable-quarto/)** | [GitHub](https://github.com/alohays/impeccable-quarto)

---

## What is impeccable-quarto?

**impeccable-quarto** is a design quality system for [Quarto RevealJS](https://quarto.org/docs/presentations/revealjs/) presentations. It combines two philosophies into a single, opinionated toolkit:

1. **impeccable** — A curated design vocabulary that fights LLM design bias. Instead of producing generic, forgettable slides, impeccable enforces typography-first design, OKLCH color science, tinted neutrals, and semantic content structures. It knows what good slides look like because it encodes design expertise as executable rules, not vague guidelines.

2. **paper2pr-style quality pipelines** — An adversarial multi-agent review system with quality gates, scoring rubrics, and iterative fix loops. Your slides don't just get created — they get critiqued, scored, fixed, and verified until they meet a measurable quality bar.

The result: a system where **any source material** (research papers, blog posts, meeting notes, outlines, raw ideas) can be transformed into **professionally designed Quarto RevealJS presentations** that score well on objective quality metrics.

### Why does this exist?

LLMs produce slides that all look the same: centered headings, generic sans-serif fonts, walls of bullet points, pure black on pure white, meaningless color choices. This is **design bias** — the model defaults to the most common (not the best) patterns from its training data.

impeccable-quarto breaks this cycle by:

- **Encoding design expertise as rules**, not suggestions
- **Scoring slides objectively** with deduction-based quality gates
- **Catching anti-patterns** before they reach an audience
- **Providing curated themes** built on color science (OKLCH) and typography fundamentals
- **Running adversarial review loops** where specialized agents critique and improve slides

---

## Philosophy

### Design Principles

| Principle | What it means | What it rejects |
|---|---|---|
| **Typography-first** | Font choice, scale, and hierarchy drive the design | Decoration-first thinking; clip-art aesthetics |
| **OKLCH color** | Perceptually uniform color space for all palette work | Hex/RGB guesswork; "looks good to me" colors |
| **Tinted neutrals** | Never pure `#000` or `#FFF`; all neutrals carry a subtle hue | Flat, lifeless black/white defaults |
| **Semantic structure** | Content boxes convey meaning (`.keybox`, `.warningbox`, etc.) | Generic `<div>` wrappers with arbitrary styling |
| **One idea per slide** | Each slide has a single clear message | Content dumps; bullet-point walls |
| **Anti-pattern aware** | Known bad patterns are explicitly codified and caught | "It compiled, ship it" mentality |

### Quality Pipeline

Presentations move through measurable quality gates:

| Gate | Score | Meaning |
|---|---|---|
| **Draft** | 80/100 | Structurally sound, renders cleanly, no critical issues |
| **Presentable** | 90/100 | Good design, clear narrative, minor issues only |
| **Excellent** | 95/100 | Publication-quality, polished typography, strong story arc |

Scores are computed by deduction from 100. Every deduction maps to a specific, fixable issue.

---

## Quick Start

### Prerequisites

- [Quarto](https://quarto.org/docs/get-started/) v1.4 or later
- Python 3.10 or later
- [Claude Code](https://claude.com/claude-code) (for the AI-powered quality pipeline)

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/alohays/impeccable-quarto.git
cd impeccable-quarto
```

2. **Copy the skill system into your project** (optional — for use in other repos):

```bash
# Copy the Claude Code integration
cp -r impeccable-quarto/.claude/ your-project/.claude/

# Copy the theme
cp impeccable-quarto/themes/impeccable.scss your-project/themes/

# Add theme reference to your _quarto.yml
# theme: [default, themes/impeccable.scss]
```

3. **Or work directly in this repo:**

```bash
# Prepare the local development environment
./scripts/setup.sh

# Create a new presentation from a template
./scripts/new-deck.sh my-talk.qmd

# Preview live
quarto preview my-talk.qmd
```

## Contributing

Contributor setup, architecture notes, and script documentation live in [`DEVELOP.md`](/Users/iyunseong/.clawteam/workspaces/impl/codex-2/DEVELOP.md).

### Creating Your First Deck

#### From scratch

```bash
# 1. Start from a template
cp templates/basic.qmd talks/my-topic.qmd

# 2. Edit the .qmd file with your content

# 3. Preview
quarto preview talks/my-topic.qmd

# 4. Run the quality audit
# (In Claude Code, use the /audit-slides command)
/audit-slides talks/my-topic.qmd

# 5. Get design critique
/critique-slides talks/my-topic.qmd
```

#### From source material (paper, blog post, notes)

```bash
# 1. Place your source material in the project
cp ~/paper.pdf source-material/

# 2. Use Claude Code to translate it
# "Translate source-material/paper.pdf into a 15-slide deck using impeccable-quarto"

# 3. The system will:
#    - Extract key content from your source
#    - Structure it into a narrative arc
#    - Apply the impeccable theme
#    - Run quality checks
#    - Iterate until the quality gate is met
```

---

## Command Reference

impeccable-quarto provides slash commands for Claude Code organized into four categories:

### Diagnostic Commands (Read-Only)

These commands analyze your slides without modifying them.

| Command | Description | Output |
|---|---|---|
| `/audit-slides [file]` | Technical quality audit: overflow, compilation, broken refs, image resolution, accessibility | Scored report with categorized issues |
| `/critique-slides [file]` | UX/design review: visual hierarchy, cognitive load, emotional resonance | Design critique with recommendations |
| `/score-deck [file]` | Quick composite score combining audit + critique | Single score with breakdown |
| `/check-antipatterns [file]` | Scan for known anti-patterns only | Anti-pattern violation list |

### Fix-It Commands (Modify Files)

These commands apply fixes to your slides.

| Command | Description | What it changes |
|---|---|---|
| `/fix-slides [file]` | Apply all fixes from most recent audit/critique report | `.qmd` content and structure |
| `/fix-overflow [file]` | Fix content overflow issues specifically | Text, layout, font sizes |
| `/fix-typography [file]` | Fix typography issues: hierarchy, sizing, font pairing | Heading levels, font references |
| `/fix-colors [file]` | Replace non-OKLCH colors, fix contrast issues | Color values in `.qmd` and `.scss` |

### Enhance Commands (Improve Quality)

These commands actively improve slides beyond fixing issues.

| Command | Description | Effect |
|---|---|---|
| `/enhance-narrative [file]` | Improve story arc, pacing, transitions | Slide order, section structure |
| `/enhance-visuals [file]` | Upgrade visual design: better layouts, semantic boxes | Layout classes, box types |
| `/add-speaker-notes [file]` | Generate speaker notes for slides missing them | `::: {.notes}` blocks |
| `/translate-source [source] [target]` | Convert any source material into slide content | Creates new `.qmd` file |

### Review Commands (Multi-Agent Pipeline)

These commands invoke the full adversarial review pipeline.

| Command | Description | Pipeline |
|---|---|---|
| `/review-cycle [file]` | Full review cycle: audit + critique + fix + verify | Multi-pass improvement |
| `/review-cycle [file] --target 90` | Review cycle targeting a specific score | Iterates until target met |
| `/review-cycle [file] --max-rounds 3` | Limit the number of improvement rounds | Bounded iteration |

---

## Theme System

### The Impeccable Base Theme

The core theme (`themes/impeccable.scss`) is built on three pillars:

#### 1. OKLCH Color Palette

All colors are defined in the [OKLCH color space](https://oklch.com/) — a perceptually uniform model where equal numeric steps produce equal visual differences. This means:

- Color relationships are mathematically precise
- Lightness and saturation are independent
- Palette variations are predictable and harmonious

```scss
// Primary: Deep Indigo — authority, trust
$primary:        oklch(0.45 0.18 265);
$primary-light:  oklch(0.65 0.12 265);

// Secondary: Warm Teal — clarity, balance
$secondary:       oklch(0.55 0.12 195);

// Accent: Marigold — attention, energy
$accent:       oklch(0.72 0.16 85);
```

#### 2. Tinted Neutrals

Every neutral carries a subtle hue (chroma 0.008–0.015 at hue 265) instead of being pure gray. This gives the palette warmth and cohesion without visible color:

```scss
$neutral-950: oklch(0.12 0.015 265);   // near-black (not #000)
$neutral-50:  oklch(0.96 0.012 265);   // near-white (not #FFF)
```

#### 3. Typography Stack

Three carefully paired fonts for distinct roles:

| Role | Font | Why |
|---|---|---|
| **Display** (headings) | Plus Jakarta Sans | Modern geometric with personality; distinctive without being distracting |
| **Body** (paragraphs, lists) | Source Sans 3 | Superb readability at all sizes; clear at projection distance |
| **Code** | JetBrains Mono | Programming ligatures; wide characters for readability |

Type scale follows a **1.25 Major Third** ratio with a 28px base size (minimum readable at projection distance).

### Semantic Box Classes

Content boxes convey meaning through consistent visual language:

| Class | Purpose | Visual |
|---|---|---|
| `.keybox` | Key finding or takeaway | Gold border, warm background |
| `.methodbox` | Methodology or process | Indigo border, blue background |
| `.warningbox` | Warning or caveat | Red border, pink background |
| `.tipbox` | Tip or best practice | Green border, mint background |
| `.quotebox` | Attribution quote | Gray border, italic text |
| `.infobox` | Supplementary information | Blue border, sky background |

Usage in `.qmd`:

```markdown
::: {.keybox}
**Key Finding**

The intervention reduced error rates by 47% across all test conditions.
:::
```

### Layout Classes

Grid-based layouts for multi-column slides:

| Class | Layout | Use case |
|---|---|---|
| `.two-col` | Equal two columns | Side-by-side content |
| `.three-col` | Equal three columns | Feature comparison |
| `.sidebar-left` | 1:2 ratio | Image + description |
| `.sidebar-right` | 2:1 ratio | Content + sidebar |
| `.comparison` | Two columns with colored headers | Before/after, pros/cons |

Usage:

```markdown
::: {.two-col}
::: {}
Left column content
:::
::: {}
Right column content
:::
:::
```

### Emphasis Classes

Inline highlighting for drawing attention:

| Class | Effect |
|---|---|
| `.hi` | Primary color emphasis |
| `.hi-gold` | Gold/accent emphasis |
| `.hi-green` | Success/positive emphasis |
| `.hi-red` | Danger/negative emphasis |
| `.subtle` | De-emphasized text |
| `.smaller` | 82% size text |
| `.smallest` | 68% size text |
| `.larger` | 125% size text |

### Dark Mode

The theme includes a complete dark mode variant. Activate with:

```yaml
# In YAML frontmatter
format:
  revealjs:
    theme: [dark, themes/impeccable.scss]
```

Or use the `.dark-mode` class on the reveal container.

### Fragment Animations

Smooth, purposeful animations for progressive disclosure:

| Class | Effect |
|---|---|
| `.fragment` | Smooth fade-in (default) |
| `.fragment.slide-up` | Slide up + fade in |
| `.fragment.fade-in-smooth` | Explicit fade (same as default) |
| `.fragment.scale-in` | Scale from 92% + fade in |

All animations respect `prefers-reduced-motion`.

---

## Quality Gates

### How Scoring Works

Every presentation starts at **100 points**. Issues cause deductions:

#### Critical Issues (automatic fail or major deduction)

| Issue | Deduction |
|---|---|
| Compilation failure | -100 (automatic zero) |
| Broken image reference | -15 per instance |
| Content overflow (text outside slide bounds) | -10 per slide |
| Missing YAML frontmatter | -10 |
| Broken cross-reference | -8 per instance |

#### Major Issues

| Issue | Deduction |
|---|---|
| No speaker notes on content slide | -5 per slide |
| More than 5 bullet points on a slide | -5 per slide |
| Font size below 20px | -5 per instance |
| Missing alt text on image | -5 per image |
| Pure black (#000) or white (#FFF) used | -3 per instance |
| Heading hierarchy skipped | -3 per instance |
| Non-OKLCH color used in theme override | -3 per instance |

#### Minor Issues

| Issue | Deduction |
|---|---|
| Inconsistent slide separator style | -2 |
| Missing date in frontmatter | -1 |
| Image without explicit dimensions | -1 per image |
| More than 40 words of body text on a slide | -2 per slide |
| Raster image used where SVG would be better | -1 per image |

### Gate Thresholds

| Gate | Score Range | What it means |
|---|---|---|
| **Failing** | 0–59 | Critical issues; not ready for any audience |
| **Needs Work** | 60–79 | Structural issues; needs another round of fixes |
| **Draft** | 80–84 | Acceptable for internal review |
| **Presentable** | 85–89 | Ready for most audiences |
| **Excellent** | 90–94 | High quality; minor polish remaining |
| **Impeccable** | 95–100 | Publication-ready; meets all quality criteria |

---

## Anti-Patterns

impeccable-quarto explicitly codifies and detects these common slide design anti-patterns:

### Content Anti-Patterns

| Anti-Pattern | Description | Fix |
|---|---|---|
| **Bullet Wall** | More than 5 bullets on a single slide | Split across multiple slides or use semantic boxes |
| **Content Dump** | Slide tries to communicate more than one idea | One idea per slide; move supporting detail to speaker notes |
| **Text Overflow** | Content exceeds slide boundaries | Reduce content, increase slide count, or use `.smaller` |
| **Missing Narrative** | Slides are a list of facts with no story arc | Structure as: Context → Problem → Approach → Result → Takeaway |
| **Orphan Slide** | A slide that doesn't connect to neighbors | Add transition text or restructure the sequence |

### Design Anti-Patterns

| Anti-Pattern | Description | Fix |
|---|---|---|
| **Generic Theme** | Using default Reveal.js theme without customization | Apply impeccable theme or create a variant |
| **Pure Black/White** | Using `#000000` or `#FFFFFF` | Use tinted neutrals from the theme |
| **Random Colors** | Colors chosen without semantic meaning | Use the OKLCH palette; assign colors to meanings |
| **Font Soup** | More than 3 font families on a single slide | Stick to the theme's display/body/code triad |
| **All-Caps Abuse** | Overusing uppercase text for emphasis | Use `.hi` classes or semantic boxes instead |
| **Decoration Noise** | Borders, shadows, gradients that don't convey meaning | Remove purely decorative elements; let typography lead |

### Typography Anti-Patterns

| Anti-Pattern | Description | Fix |
|---|---|---|
| **Tiny Text** | Font size below 20px (unreadable at projection distance) | Use 28px base minimum; `.smaller` for supporting text only |
| **Heading Skip** | Jumping from H1 to H3 without H2 | Maintain sequential heading hierarchy |
| **Weight Overload** | Overusing bold text to the point where nothing stands out | Reserve bold for genuine emphasis; use color for variety |
| **Line Squeeze** | Line height below 1.3 (text feels cramped) | Use 1.5+ for body text |

### Technical Anti-Patterns

| Anti-Pattern | Description | Fix |
|---|---|---|
| **Missing Speaker Notes** | Content slides without notes (presenter has no guide) | Add `::: {.notes}` block to every content slide |
| **Missing Alt Text** | Images without `alt` attributes (accessibility failure) | Add descriptive alt text to all images |
| **Inline Styles** | CSS in the `.qmd` file instead of theme/class | Use theme variables and utility classes |
| **Raster Diagrams** | Using PNG/JPG for diagrams/charts | Export diagrams as SVG |
| **Broken References** | Cross-references (`@fig-`, `@tbl-`) that don't resolve | Verify all references before committing |

---

## Directory Structure

```
impeccable-quarto/
├── source/                     # Source of truth for all definitions
│   ├── skills/                 # Skill definitions (SKILL.md per skill)
│   ├── agents/                 # Agent persona definitions
│   ├── rules/                  # Governance rules and scoring rubrics
│   └── references/             # Design reference documents
├── themes/                     # SCSS themes for Quarto RevealJS
│   └── impeccable.scss         # The master theme
├── templates/                  # Presentation starter templates (.qmd)
├── examples/                   # Example presentations
├── scripts/                    # Build and utility scripts
├── .claude/                    # Claude Code integration (generated from source/)
│   ├── skills/                 # Slash commands for Claude Code
│   ├── agents/                 # Agent definitions for Claude Code
│   ├── rules/                  # Rules for Claude Code
│   └── settings.json           # Permissions configuration
├── CLAUDE.md                   # Claude Code project instructions
├── AGENTS.md                   # Agent definitions and orchestration protocol
├── CONTRIBUTING.md             # Contributor guidelines
├── README.md                   # This file
├── _quarto.yml                 # Quarto project configuration
├── pyproject.toml              # Python tooling configuration
└── .gitignore                  # Git ignore rules
```

### Source Directory

The `source/` directory is the **single source of truth** for all skill definitions, agent personas, rules, and reference material. Files in `.claude/` are derived from `source/` — when in doubt, `source/` is canonical.

### Themes Directory

SCSS themes for Quarto RevealJS. The master theme is `impeccable.scss`. Theme variants (e.g., `impeccable-dark.scss`, `impeccable-academic.scss`) extend the base.

### Templates Directory

Starter `.qmd` files for common presentation types:

- `basic.qmd` — Minimal starter with title slide and a few content slides
- `academic.qmd` — Research presentation with methods/results structure
- `technical.qmd` — Technical talk with code blocks and architecture diagrams
- `lightning.qmd` — 5-minute lightning talk format

### Examples Directory

Complete example presentations demonstrating impeccable-quarto features. Each example includes the `.qmd` source and its quality score.

---

## Creating Theme Variants

To create a theme variant:

1. Create `themes/impeccable-<name>.scss`
2. Override OKLCH color variables at the top
3. Keep typography and structural rules from the base theme
4. Reference it in your `.qmd` frontmatter:

```yaml
format:
  revealjs:
    theme: [default, themes/impeccable-<name>.scss]
```

### Color Variant Example

```scss
/*-- scss:defaults --*/

// Override just the palette — structure stays the same
$primary:        oklch(0.50 0.16 160);  // Forest green
$primary-light:  oklch(0.70 0.10 160);
$primary-dark:   oklch(0.35 0.14 160);

$accent:         oklch(0.68 0.14 45);   // Burnt orange

// Neutral tint follows primary hue
$neutral-950: oklch(0.12 0.015 160);
$neutral-50:  oklch(0.96 0.012 160);

// Everything else inherits from the base
@import 'impeccable';
```

---

## Build & Render

### Render a single presentation

```bash
quarto render path/to/deck.qmd
```

### Render all presentations

```bash
quarto render
```

### Preview with live reload

```bash
quarto preview path/to/deck.qmd
```

### Utility scripts

| Script | Purpose |
|---|---|
| `scripts/render.sh` | Render all `.qmd` files with error reporting |
| `scripts/new-deck.sh` | Create a new presentation from a template |
| `scripts/theme-preview.sh` | Generate side-by-side theme comparison |
| `scripts/quality_score.py` | Run the scoring algorithm on a `.qmd` file |

---

## Integration with Claude Code

impeccable-quarto is designed to work as a Claude Code skill system. When the `.claude/` directory is present in a project, Claude Code gains access to:

1. **Slash commands** (`/audit-slides`, `/critique-slides`, etc.)
2. **Design rules** that guide how Claude generates and modifies slides
3. **Agent personas** for specialized review roles
4. **Quality gates** that enforce measurable standards

### Using in Your Own Project

Copy the `.claude/` directory and `themes/` directory to any Quarto project:

```bash
cp -r impeccable-quarto/.claude/ my-project/.claude/
cp -r impeccable-quarto/themes/ my-project/themes/
```

Then add to your `_quarto.yml`:

```yaml
format:
  revealjs:
    theme: [default, themes/impeccable.scss]
```

Claude Code will now use impeccable-quarto's design system when working on presentations in your project.

### Project-Level Customization

Create `.impeccable-quarto.md` in your project root to customize behavior:

```markdown
# Project Design Preferences

## Color Override
- Primary: oklch(0.50 0.16 160) — forest green for environmental theme

## Content Rules
- Maximum slides: 20 (conference has a 15-minute slot)
- Required sections: Introduction, Methods, Results, Discussion
- Language: Korean with English technical terms

## Audience
- Domain experts in machine learning
- Familiar with the paper being presented
- Expects detailed methodology slides
```

---

## The Adversarial Review Pipeline

### How It Works

The review pipeline is modeled after adversarial quality assurance:

```
Source Material
     │
     ▼
┌──────────────┐
│  Translate   │  Convert source → slide content
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Compose    │  Structure slides with theme + layout
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│   Audit      │────▶│   Fix        │  Technical issues
└──────┬───────┘     └──────┬───────┘
       │                    │
       ▼                    ▼
┌──────────────┐     ┌──────────────┐
│  Critique    │────▶│   Enhance    │  Design issues
└──────┬───────┘     └──────┬───────┘
       │                    │
       ▼                    ▼
┌──────────────┐
│   Verify     │  Compilation + score check
└──────┬───────┘
       │
       ▼
  Score ≥ target?
   ╱          ╲
  YES          NO → back to Audit
   │
   ▼
  Done ✓
```

### Review Cycle Protocol

1. **Audit** — Technical quality check (compilation, overflow, broken refs, accessibility)
2. **Critique** — Design quality review (hierarchy, cognitive load, narrative, aesthetics)
3. **Fix** — Apply automated fixes for all identified issues
4. **Enhance** — Improve design beyond basic fixes (better layouts, semantic boxes, transitions)
5. **Verify** — Re-render and re-score to confirm improvements
6. **Gate Check** — If score meets target, done. Otherwise, loop back to Audit.

Maximum rounds are configurable (default: 5) to prevent infinite loops.

---

## Comparison with Other Approaches

| Feature | Raw Quarto | Quarto + Custom CSS | impeccable-quarto |
|---|---|---|---|
| Color system | None (browser defaults) | Ad-hoc hex values | OKLCH with semantic roles |
| Typography | System defaults | Manual font loading | Curated stack with modular scale |
| Quality scoring | Manual review | Manual review | Automated 0-100 scoring |
| Anti-pattern detection | None | None | 20+ codified patterns |
| Speaker notes | Optional | Optional | Required + generated |
| Accessibility | Manual | Manual | Automated WCAG checks |
| Dark mode | Not included | DIY | Built-in, complete |
| Review pipeline | Human-only | Human-only | Adversarial multi-agent |

---

## FAQ

**Q: Do I need Claude Code to use impeccable-quarto?**
A: No. The theme and templates work with any Quarto installation. Claude Code enables the automated quality pipeline and slash commands, but you can apply the design principles manually.

**Q: Can I use this with other Quarto formats (not RevealJS)?**
A: The theme is specifically designed for RevealJS presentations. The design principles and anti-patterns apply broadly, but the SCSS and layout classes are RevealJS-specific.

**Q: How do I customize the color palette?**
A: Create a theme variant (see "Creating Theme Variants" above). Override the OKLCH color variables while keeping the structural rules. Never use non-OKLCH colors.

**Q: What's the minimum Quarto version?**
A: Quarto 1.4 or later. Earlier versions may work but are not tested.

**Q: Can I use impeccable-quarto for non-academic presentations?**
A: Absolutely. The system is designed for **any** presentation type: technical talks, business pitches, teaching materials, conference keynotes, lightning talks. The quality pipeline and design system are content-agnostic.

**Q: Why OKLCH instead of HSL or Hex?**
A: OKLCH is perceptually uniform — equal numeric changes produce equal visual changes. HSL has perceptual inconsistencies (yellow at 50% lightness looks much lighter than blue at 50%). OKLCH gives predictable, harmonious palettes with mathematical precision.

**Q: Why tinted neutrals instead of pure gray?**
A: Pure grays feel cold and disconnected from the color palette. A subtle hue tint (chroma 0.01–0.015) in the neutrals creates visual cohesion with the primary palette without being consciously perceived as a color. It's the difference between "clean" and "clinical."

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Adding themes and theme variants
- Creating example presentations
- Adding new skills and slash commands
- Quality standards for contributions

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgments

impeccable-quarto builds on ideas from:

- [impeccable.style](https://impeccable.style) — The original design vocabulary system
- paper2pr — Multi-agent quality pipeline for academic presentations
- [Quarto](https://quarto.org) — The open-source scientific publishing system
- [Reveal.js](https://revealjs.com) — The HTML presentation framework
- [OKLCH](https://oklch.com) — Perceptually uniform color space
