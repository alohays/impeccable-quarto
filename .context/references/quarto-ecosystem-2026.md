# Quarto RevealJS Ecosystem (2025-2026)

**Date:** 2026-04-03
**Source:** Web research (Quarto docs, GitHub, extension listings)

---

## 1. Quarto 1.8 Key Features (Oct 2025)

### `_brand.yml` System
Official unified branding across all Quarto formats (HTML, RevealJS, dashboards, documents).
Defines: colors, typography (fonts, sizes, weights), logos (light/dark variants).
**Brand extensions**: Share brand definitions via Git repos (`quarto create extension brand`).
**Direct relevance:** impeccable-quarto's design system could be expressed as a `_brand.yml` for cross-format consistency.

### Axe-core Accessibility Checks
Built-in WCAG violation detection for RevealJS output.
Displayed in document previews.
**Direct relevance:** Could replace manual contrast checking in quality scoring pipeline.

### `brand-mode: dark`
Dark-themed presentations supported natively.
**Direct relevance:** Solves ISSUE-04 (dark mode dead code) — use Quarto's native mechanism instead of custom CSS classes.

---

## 2. RevealJS Version Updates

### 5.0 (Oct 2023): Scroll View
Decks viewable as scrollable web pages. Auto-enables on mobile <435px.
Theme should be tested for scroll view rendering.

### 5.2 (Mar 2024): Lightbox
Any element becomes lightbox trigger via `data-preview-image`/`data-preview-video`.
Useful for figures shown inline then expanded on click.

### 6.0 (Mar 2024): React Wrapper + TypeScript
Official React components: `<Deck>`, `<Slide>`, `<Fragment>`.
Migrated Gulp → Vite. MathJax 4. Enhanced accessibility.

---

## 3. Notable Quarto RevealJS Themes

| Theme | Stars | Style | OKLCH? | Quality Scoring? |
|-------|-------|-------|--------|-----------------|
| clean-revealjs (Grant McDermott) | 389 | Academic/LaTeX-inspired | No | No |
| kakashi (Malcolm Barrett) | — | Colorblind-friendly | No | No |
| coeos (Canouil) | — | Polished template | No | No |
| letterbox (Hvitfeldt) | — | Widescreen framing | No | No |
| **impeccable-quarto** | — | Typography-first OKLCH | **Yes** | **Yes** |

**impeccable-quarto is the only Quarto theme with OKLCH and quality scoring.**

---

## 4. Notable Extensions for RevealJS

### Directly Applicable
- **auto-agenda**: Generates agenda slides from headings (aligns with narrative arc requirements)
- **revealjs-a11y**: WCAG enhancements (strengthens accessibility compliance)
- **roughnotation**: Animated hand-drawn annotations (typography-friendly emphasis alternative)
- **reveal-header**: Logo and header text (institutional branding)
- **simplemenu**: Auto-generated section menus (navigation)
- **FontsFirst**: Ensures web fonts load before init (prevents FOUT for custom fonts)
- **CopyCode**: Copy buttons on code blocks

### Interesting but Lower Priority
- **appearance**: Sequential animations like PowerPoint
- **excalidraw**: Hand-drawn diagram canvas
- **revealjs-editable**: Reposition/resize elements in slides (useful for live review)
- **revealjs-tabset**: Keyboard-navigable tabsets with PDF export

---

## 5. W3C Design Tokens Specification (2025.10)

First stable version released October 28, 2025.
- JSON interchange format (`.tokens.json`)
- Full OKLCH and CSS Color Module 4 support
- 10+ tools: Penpot, Figma, Sketch, Framer, Tokens Studio, Style Dictionary, Terrazzo
- Style Dictionary has `color/oklch` transformer

**Opportunity:** impeccable-quarto could be the first presentation system with W3C design tokens:
1. Define design system as `.tokens.json`
2. Compile to SCSS variables, CSS custom properties, `_brand.yml` via Style Dictionary
3. Enable Figma/Sketch interoperability

---

## 6. Competitive Landscape

### Slidev (strongest competitor for developers)
- Shiki Magic Move (code morphing animation) — unique, no equivalent
- Monaco Editor (live REPL in slides)
- UnoCSS (atomic CSS) as default
- Vue components in slides
- MCP server for AI integration (slidev-mcp)
- cc-slidev Claude Code plugin (design guardrails)

### Marp (simplest)
- Tiny HTML output
- PDF/PPTX export
- Majin Slide MCP for AI integration

### Quarto Unique Advantages (vs Slidev/Marp)
- Executable code cells (R/Python)
- Scientific publishing integration
- `_brand.yml` multi-format branding
- Axe-core accessibility built-in
- Cross-reference system (@fig-, @tbl-, @sec-)
- Scroll View for mobile

### Where impeccable-quarto Uniquely Fits
No other project combines: OKLCH design system + quality scoring + adversarial review + Claude Code skills + Quarto.
The closest is claude-code-my-workflow (same architecture, academic focus) and cc-slidev (guardrails, Slidev platform).
