# Matrix-Game Slide Decks — Technical Implementation Plan

## Overview

Build 3 Quarto RevealJS slide decks about Matrix-Game (Skywork AI's world model series) as portfolio pieces for the impeccable-quarto demo site. Each deck covers one version (1.0, 2.0, 3.0) and must showcase the design system at its best.

---

## 1. File Structure

### Deck Files

```
examples/
├── matrix-game-1.qmd          # Matrix-Game 1.0: Interactive World Foundation Model
├── matrix-game-2.qmd          # Matrix-Game 2.0: Real-Time Streaming World Model
├── matrix-game-3.qmd          # Matrix-Game 3.0: Long-Horizon Memory World Model
└── assets/
    └── matrix-game/
        ├── mg1/                # Assets for deck 1
        │   ├── human-win-rate.png
        │   └── demo.gif
        ├── mg2/                # Assets for deck 2
        │   ├── cover.png
        │   ├── mouse.png
        │   └── demo-*.png     # Selected demo images (3-4 max)
        └── mg3/                # Assets for deck 3
            ├── mouse.png
            └── demo-*.png     # Selected demo images (4-5 max)
```

### Naming Conventions

- Deck files: `matrix-game-{version}.qmd` (kebab-case, matching existing examples)
- Asset subdirectory: `assets/matrix-game/mg{N}/` (short prefix, version-scoped)
- Images: descriptive kebab-case names (`human-win-rate.png`, not `00.png`)
- All asset paths relative to the `.qmd` file

### Why This Structure

- **`examples/` directory**: Matches existing convention (`academic-paper.qmd`, `demo.qmd`, etc.)
- **Single `assets/matrix-game/` parent**: Keeps all Matrix-Game assets colocated, easy to find and manage
- **Per-deck subdirectories**: Prevents name collisions between versions
- **No `examples/assets/` yet**: Need to create this directory

---

## 2. Asset Pipeline

### 2.1 Images to Copy from References

**Matrix-Game-1 (`mg1/`):**
| Source | Target | Size | Purpose |
|--------|--------|------|---------|
| `Matrix-Game-1/assets/imgs/human_win_rate.png` | `human-win-rate.png` | 128K | Benchmark comparison chart |
| `Matrix-Game-1/assets/videos/demo.gif` | `demo.gif` | 9.4MB | Animated gameplay demo |
| `Matrix-Game-1/GameWorldScore/asset/init_image/forest/00.jpg` | `biome-forest.jpg` | ~100K | Example biome (forest) |
| `Matrix-Game-1/GameWorldScore/asset/init_image/icy/00.png` | `biome-icy.png` | ~100K | Example biome (icy) |

> **Note:** demo.gif at 9.4MB is borderline. With `embed-resources: true`, it gets base64-encoded into the HTML (~12.5MB added). Acceptable for a portfolio deck, but consider converting to a 4-frame strip PNG if file size becomes an issue.

**Matrix-Game-2 (`mg2/`):**
| Source | Target | Size | Purpose |
|--------|--------|------|---------|
| `Matrix-Game-2/assets/images/cover.png` | `cover.png` | 3.7MB | Hero/overview figure |
| `Matrix-Game-2/assets/images/mouse.png` | `mouse-control.png` | 52K | Mouse control visualization |
| `Matrix-Game-2/demo_images/universal/0000.png` | `demo-universal.png` | ~500K | Universal scene demo |
| `Matrix-Game-2/demo_images/gta_drive/0000.png` | `demo-gta.png` | ~500K | GTA driving scene |
| `Matrix-Game-2/demo_images/temple_run/0000.png` | `demo-temple-run.png` | ~500K | Temple Run scene |

**Matrix-Game-3 (`mg3/`):**
| Source | Target | Size | Purpose |
|--------|--------|------|---------|
| `Matrix-Game-3/assets/images/mouse.png` | `mouse-control.png` | 52K | Mouse control visualization |
| `Matrix-Game-3/demo_images/001/image.png` | `demo-scene-01.png` | ~300K | Generated scene example |
| `Matrix-Game-3/demo_images/003/image.png` | `demo-scene-03.png` | ~300K | Generated scene example |
| `Matrix-Game-3/demo_images/005/image.png` | `demo-scene-05.png` | ~300K | Generated scene example |
| `Matrix-Game-3/demo_images/008/image.png` | `demo-scene-08.png` | ~300K | Generated scene example |

### 2.2 Images NOT to Copy

- `GameWorldScore/` benchmark images (biome init images × 7 biomes × 4 each = 28 images — too many, pick 2 representative)
- `GameWorldScore/GameWorld/third_party/` — irrelevant dependency images
- Full `demo_images/` directories — select 3-5 representative samples per deck
- PDF reports (67MB, 54MB) — never commit these; reference via URL only

### 2.3 Video Handling

**Decision: External embeds only. No local video files.**

Rationale:
- `matrix-game2.mp4` is 3.3MB, `matrix-game3.mp4` is 18MB
- With `embed-resources: true`, these would balloon HTML to 25-50MB+
- GitHub Pages has a 100MB repo soft limit guideline
- YouTube/GitHub video URLs render cleanly in RevealJS

Implementation:
```markdown
## Demo Video {background-iframe="https://www.youtube.com/embed/VIDEO_ID" background-interactive}
```

Or for GitHub-hosted videos (from the README):
```markdown
{{< video https://github.com/user-attachments/assets/VIDEO_ID >}}
```

> **Action item for content-planner:** Identify the exact YouTube/GitHub video URLs from the Matrix-Game project pages and READMEs. The GitHub user-attachments URLs in the READMEs are the video sources.

### 2.4 Diagrams: Mermaid vs SVG

**Decision: Recreate architecture diagrams as Mermaid in `.qmd`.**

Why:
- The paper figures (pipeline diagrams, architecture) are embedded in PDFs as raster
- Extracting them would produce low-quality rasters at projection resolution
- Mermaid diagrams render as SVG, scale perfectly, and inherit theme colors
- Quarto has native Mermaid support via `{mermaid}` code blocks

Key diagrams to recreate:
1. **MG2 Pipeline** (Fig 2 of MG2 paper): Training Stage → Foundation Model SFT → Causal Model Distillation; Inference Stage with KV Caching
2. **MG3 Overview** (Fig 2 of MG3 paper): Data Engine → Model Training → Inference Deployment
3. **MG3 Base Model** (Fig 3 of MG3 paper): Error Buffer + Diffusion Transformer with past/current frames
4. **MG1 GameWorldScore benchmark** flow

For complex figures that Mermaid can't handle well (e.g., the detailed MG3 error buffer diagram), create standalone SVG files in the assets directory.

### 2.5 Image Optimization

Before committing images:
1. **Cover images** (>1MB): Resize to max 1920×1080 (slide resolution), compress with quality 85
2. **Demo screenshots**: Resize to 960×540 (half-slide for side-by-side layouts), quality 85
3. **Charts/diagrams**: Keep original resolution if <500K
4. **Format**: Keep PNG for screenshots (lossless edges), convert large photos to WebP if browser support is acceptable (it is for modern browsers)

```bash
# Example optimization commands (to run before committing)
# Resize cover to slide width
magick convert cover.png -resize 1920x1080\> -quality 85 cover.png
# Resize demo images to half-slide
magick convert demo-*.png -resize 960x540\> -quality 85 demo-optimized.png
```

**Estimated total committed asset size:** ~20-25MB across all 3 decks

---

## 3. Build & Deploy

### 3.1 Quarto Rendering

The existing `_quarto.yml` applies to all `.qmd` files in the project. The 3 new decks will automatically inherit:
- Theme: `themes/impeccable.scss`
- Dimensions: 1920×1080
- `embed-resources: true` (self-contained HTML)
- Google Fonts preconnect
- All RevealJS settings (transitions, navigation, etc.)

**No changes to `_quarto.yml` needed.**

Individual deck YAML frontmatter overrides (if needed):
```yaml
---
title: "Matrix-Game 2.0"
subtitle: "Real-Time Streaming Interactive World Model"
author: "Skywork AI"
date: "2025-08-12"
format:
  revealjs:
    # Inherit everything from _quarto.yml
    # Only override if deck-specific needs arise
---
```

### 3.2 CI/CD Changes

The current workflow (`.github/workflows/quality.yml`) already triggers on `examples/**` changes and renders all `examples/*.qmd` files. **No changes needed** — the 3 new decks will be automatically picked up.

However, there is one consideration:

**Asset path in CI:** The workflow runs `quarto render` from the repo root. Image paths like `assets/matrix-game/mg2/cover.png` are relative to the `.qmd` file location (`examples/`), so the actual filesystem path is `examples/assets/matrix-game/mg2/cover.png`. This will resolve correctly because Quarto resolves paths relative to the `.qmd` file.

**Render time:** Each deck with embedded images will take longer to render. Current decks are text-only (~5s each). Image-heavy decks may take 15-30s each. The CI timeout should be fine (default 6h for GitHub Actions).

**Quality scoring:** The `quality_score.py` script will score these decks. They need to score ≥80 to pass CI. Since these are portfolio pieces, target ≥90.

### 3.3 Demo Site Deployment

The rendered HTML files go to `docs/examples/` for GitHub Pages. This requires a manual or automated copy step.

**Current process** (inferred from existing files):
- `examples/*.qmd` → `quarto render` → output to `_output/` (per `_quarto.yml`)
- Someone copies/moves the rendered `.html` to `docs/examples/`

**Changes needed:**

1. **Copy rendered HTML to docs:**
   ```bash
   # After quarto render
   cp _output/matrix-game-1.html docs/examples/
   cp _output/matrix-game-2.html docs/examples/
   cp _output/matrix-game-3.html docs/examples/
   ```

2. **Update `docs/index.html`** to add links to the new decks.

   Add a new section or extend the existing themes showcase. Suggested placement: after the existing theme cards, add a "Portfolio" or "Case Study" section:

   ```html
   <article class="theme-card fade-in" data-delay="500">
     <div class="theme-top">
       <span class="theme-badge">Case Study</span>
       <h3>Matrix-Game 1.0</h3>
     </div>
     <p>Interactive world foundation model — Minecraft world generation with keyboard/mouse control.</p>
     <div class="theme-accent" style="background: linear-gradient(90deg, oklch(0.45 0.18 265), oklch(0.60 0.15 145));"></div>
     <a class="theme-link" href="examples/matrix-game-1.html" target="_blank" rel="noreferrer">View presentation</a>
   </article>
   <!-- Repeat for MG2 and MG3 -->
   ```

### 3.4 `embed-resources` Tradeoff

**Current setting:** `embed-resources: true` (self-contained HTML)

**Implication for image-heavy decks:**
- Each rendered HTML will be 25-40MB (images base64-encoded)
- `docs/examples/` will grow from ~115MB to ~200-230MB
- GitHub Pages limit: 1GB repo size, 100MB per file — we're well within limits

**Alternative:** `embed-resources: false` with external asset serving
- Pros: Smaller HTML files, faster CI
- Cons: Requires serving assets alongside HTML, more complex deployment
- **Decision: Keep `embed-resources: true`.** Self-contained files are simpler to deploy and share. The size increase is acceptable for a demo site.

---

## 4. Quality Assurance

### 4.1 Scoring Strategy for Image-Heavy Decks

The quality scorer (`scripts/quality_score.py`) checks text-based patterns. Image-heavy decks have different risk profiles:

**Higher risk areas:**
- MAJ-04: Missing `alt` text on images (every image needs descriptive alt text)
- MIN-04: Images without explicit width/height
- MIN-05: Raster images used for diagrams (prefer Mermaid/SVG)
- MAJ-01: Missing speaker notes (still required on every content slide)
- CRIT-03: Content overflow (images + text can easily overflow)

**Lower risk areas:**
- AP-C01 Bullet Wall (fewer bullets, more images)
- AP-C02 Content Dump (images carry the content)

**Target scores:** ≥90/100 (Excellent gate) for all 3 decks

### 4.2 Compilation Testing

Run for each deck:
```bash
quarto render examples/matrix-game-1.qmd
quarto render examples/matrix-game-2.qmd
quarto render examples/matrix-game-3.qmd
```

Verify:
- No render errors or warnings
- All image paths resolve (no broken references)
- All Mermaid diagrams compile
- Output HTML opens correctly in browser
- Speaker notes visible in presenter view (press `S`)

### 4.3 Cross-Browser Considerations

- **Video embeds:** YouTube iframes work everywhere. GitHub video URLs may not autoplay in all contexts — provide a fallback link.
- **Mermaid SVG:** Renders at build time, so browser compatibility is a non-issue.
- **WebP images:** If used, Safari 14+ supports WebP. Fallback to PNG if targeting older browsers.
- **OKLCH colors:** The theme already handles browser fallback via CSS `@supports`.

### 4.4 Review Pipeline

After implementation, run the full adversarial review pipeline:
```
Phase 1: slide-critic + layout-auditor (parallel)
Phase 2: typography-reviewer + verifier (parallel)
Phase 3: slide-fixer (Critical → Major → Minor)
Phase 4: verifier (final)
```

Each deck goes through this independently. Can run all 3 deck pipelines in parallel.

---

## 5. Dependencies & Parallelization

### 5.1 Dependency Graph

```
                    ┌─────────────────┐
                    │  Content Plans   │ ← content-planner produces 3 outlines
                    │  (3 deck outlines)│
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
     ┌────────────┐ ┌────────────┐ ┌────────────┐
     │ Asset Prep │ │ Asset Prep │ │ Asset Prep │  ← Can parallelize
     │    MG1     │ │    MG2     │ │    MG3     │
     └──────┬─────┘ └──────┬─────┘ └──────┬─────┘
            │              │              │
            ▼              ▼              ▼
     ┌────────────┐ ┌────────────┐ ┌────────────┐
     │  Write QMD │ │  Write QMD │ │  Write QMD │  ← Can parallelize
     │    MG1     │ │    MG2     │ │    MG3     │
     └──────┬─────┘ └──────┬─────┘ └──────┬─────┘
            │              │              │
            ▼              ▼              ▼
     ┌────────────┐ ┌────────────┐ ┌────────────┐
     │  QA Review │ │  QA Review │ │  QA Review │  ← Can parallelize
     │    MG1     │ │    MG2     │ │    MG3     │
     └──────┬─────┘ └──────┬─────┘ └──────┬─────┘
            │              │              │
            └──────────────┼──────────────┘
                           ▼
                  ┌─────────────────┐
                  │   Deploy to     │
                  │   docs/ site    │
                  └─────────────────┘
```

### 5.2 What Must Happen Before Implementation

1. **Content outlines approved** — content-planner must define the slide structure for each deck
2. **Asset directory created** — `examples/assets/matrix-game/{mg1,mg2,mg3}/`
3. **Video URLs confirmed** — exact YouTube/GitHub embed URLs from the source repos
4. **Image optimization tooling available** — `imagemagick` or similar for resizing

### 5.3 What Can Be Parallelized

| Task | Dependencies | Parallelizable with |
|------|-------------|-------------------|
| Copy & optimize MG1 assets | None | MG2/MG3 asset prep |
| Copy & optimize MG2 assets | None | MG1/MG3 asset prep |
| Copy & optimize MG3 assets | None | MG1/MG2 asset prep |
| Write MG1 .qmd | MG1 assets + content outline | MG2/MG3 .qmd writing |
| Write MG2 .qmd | MG2 assets + content outline | MG1/MG3 .qmd writing |
| Write MG3 .qmd | MG3 assets + content outline | MG1/MG2 .qmd writing |
| QA review MG1 | MG1 .qmd complete | MG2/MG3 QA |
| QA review MG2 | MG2 .qmd complete | MG1/MG3 QA |
| QA review MG3 | MG3 .qmd complete | MG1/MG2 QA |
| Update docs/index.html | All 3 decks rendered | — |

### 5.4 Suggested Implementation Order

If not parallelizing (single implementer):
1. **MG2 first** — richest source material (full technical report), best demo images, most visual variety (Unreal Engine + GTA + Temple Run)
2. **MG3 second** — most advanced model, builds on MG2 concepts, has the memory/streaming angle
3. **MG1 last** — Minecraft-focused, simpler architecture, good benchmark data

This order creates a natural progression and allows later decks to reuse patterns established in earlier ones.

---

## 6. Risk Register

| Risk | Impact | Mitigation |
|------|--------|-----------|
| demo.gif (9.4MB) inflates HTML excessively | High | Convert to static frame strip or 4-frame montage PNG |
| cover.png (3.7MB) too large after base64 | Medium | Resize to 1920×1080, compress to <500KB |
| GitHub video URLs become invalid | Medium | Note fallback: re-upload to project YouTube, or host locally as last resort |
| Quality scorer flags image-heavy slides differently | Low | Review scoring output early, adjust slide content to maintain ≥90 |
| Total `docs/examples/` size exceeds practical limits | Low | Current: 115MB. After: ~230MB. GitHub Pages allows 1GB. Fine. |
| Mermaid diagrams don't capture paper figure complexity | Medium | Fall back to recreated SVG for complex diagrams (error buffer, memory arch) |

---

## 7. Checklist for Implementers

### Before starting a deck:
- [ ] Content outline exists and is approved
- [ ] Asset directory created: `examples/assets/matrix-game/mg{N}/`
- [ ] Images copied, renamed, and optimized
- [ ] Video embed URLs confirmed working

### For each deck:
- [ ] YAML frontmatter with title, subtitle, author, date
- [ ] Every content slide has speaker notes
- [ ] Every image has descriptive `alt` text
- [ ] Every image has explicit `width` attribute
- [ ] Mermaid diagrams for architecture/pipeline figures
- [ ] No inline `style=` attributes
- [ ] Semantic boxes used (`.keybox`, `.methodbox`, `.infobox`)
- [ ] Layout variety (`.two-col`, full-bleed images, data slides)
- [ ] Narrative arc: Context → Problem → Approach → Results → Takeaway
- [ ] `quarto render` succeeds without errors
- [ ] `python scripts/quality_score.py` returns ≥90

### After all decks:
- [ ] Rendered HTML copied to `docs/examples/`
- [ ] `docs/index.html` updated with links to all 3 decks
- [ ] Git commit with all assets and .qmd files
- [ ] CI pipeline passes
