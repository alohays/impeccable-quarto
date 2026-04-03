# Matrix-Game Content Plan — 3 Slide Decks

## Overview

Three decks covering the Matrix-Game series (Skywork AI), each telling a distinct story and showcasing different impeccable-quarto capabilities. Together they form a progressive narrative: foundation → real-time → full vision.

---

## Deck 1: Matrix-Game 1.0 — "Interactive World Foundation Model"

**File:** `decks/matrix-game-1.qmd`
**Theme:** `impeccable-academic.scss` (research paper presentation)
**Template base:** `academic.qmd`
**Target audience:** ML researchers, game AI researchers
**Narrative arc:** Problem (game worlds are static) → Contribution (17B controllable world model) → Benchmark (GameWorld Score) → Evidence (dominates competitors) → Significance (open-source foundation)

### Slide-by-Slide Outline (17 slides)

| # | Title | Key Message | Visual Type | Asset / Diagram | Quarto Features |
|---|---|---|---|---|---|
| 1 | **Title:** Matrix-Game: Interactive World Foundation Model | Skywork AI, 17B params, first open-source interactive world model | Full-bleed background image | `Matrix-Game-1/assets/videos/demo.gif` as background | `background-image`, title slide with `.section-header` |
| 2 | **The Problem: Static Game Worlds** | Current game worlds are hand-crafted; AI can only observe, not create | Diagram (create) | SVG flowchart: Traditional pipeline (artist → asset → engine) vs. world model (input → generation) | `.two-col` layout |
| 3 | **What if AI could dream game worlds?** | Provocative hook — imagine an AI that generates coherent, controllable game environments in real time | Full-bleed image | `GameWorldScore/asset/init_image/forest/01.png` (Minecraft forest) as background with text overlay | `background-image`, `background-opacity: 0.3` |
| 4 | **Section: Approach** | Section divider | Section header | Clean typography only | `.section-header` |
| 5 | **Architecture: Image-to-World Diffusion** | Diffusion-based model conditioned on keyboard + mouse inputs | Diagram (create) | SVG architecture diagram: Input image + action → Diffusion backbone (17B) → Next frame | `.methodbox`, fragment reveal for pipeline stages |
| 6 | **Action Conditioning: Keyboard + Mouse** | Fine-grained control through actual player inputs | Image + diagram | `Matrix-Game-2/assets/images/mouse.png` (cursor) + keyboard layout diagram | `.two-col`, fragment build-up |
| 7 | **Training Data: Matrix-Game Dataset** | Large-scale Minecraft data with fine-grained action annotations | Diagram (create) | SVG infographic: data pipeline (MineDojo → action annotation → training pairs) | `.methodbox` with fragment steps |
| 8 | **Generation in Action** | The model generates coherent Minecraft worlds from player input | Animated GIF | `Matrix-Game-1/assets/videos/demo.gif` (centered, large) | Centered image with `.r-stretch` |
| 9 | **Section: Evaluation** | Section divider | Section header | Clean typography | `.section-header` |
| 10 | **GameWorld Score: A New Benchmark** | 4-dimension benchmark: visual quality, temporal quality, action controllability, physical rules | Diagram (create) | SVG radar/quadrant diagram showing 4 evaluation dimensions | `.keybox` for the 4 dimensions |
| 11 | **Biome Diversity: Testing Across Worlds** | Benchmark tests across 8 distinct Minecraft biomes | Image grid | 2×4 grid of `GameWorldScore/asset/init_image/` — forest, river, beach, desert, hills, icy, mushroom, plain | `.four-col` or CSS grid, each image labeled |
| 12 | **Benchmark Results: We Win Everywhere** | Matrix-Game outperforms Oasis and MineWorld across all 8 metrics | Data table (recreate) | Styled table from README with bold highlights on "Ours" row | Custom styled table, `.hi` on winning values, fragments to reveal columns |
| 13 | **Human Evaluation: 96% Prefer Matrix-Game** | Double-blind evaluation shows overwhelming preference | Chart image | `Matrix-Game-1/assets/imgs/human_win_rate.png` | `.r-stretch`, `.keybox` callout: "96.3% overall win rate" |
| 14 | **Controllability: The Decisive Edge** | Mouse accuracy: 0.95 vs 0.64 (MineWorld) vs 0.56 (Oasis) | Data visualization (create) | SVG bar chart comparing mouse/keyboard accuracy across models | `.keybox` with the key stat, fragment reveal |
| 15 | **Physical Understanding** | Object and scenario consistency superior to baselines | Comparison | Side-by-side: object consistency 0.76 vs 0.56 (Oasis) with visual examples | `.two-col` with `.infobox` |
| 16 | **Open Source, Open Future** | MIT licensed, weights on HuggingFace, reproducible benchmark | Diagram (create) | SVG icons: GitHub, HuggingFace, MIT license badge | `.keybox` with links |
| 17 | **Thank You / Q&A** | Citation, links, acknowledgments | Clean typography | Paper citation in `.quotebox` | Final slide |

### Visual Highlight Moments ("Wow" slides)
1. **Slide 3** — Full-bleed Minecraft forest with provocative question overlay
2. **Slide 8** — Animated demo.gif showing real-time world generation
3. **Slide 11** — 8-biome image grid showing environment diversity (visual spectacle)
4. **Slide 13** — Human evaluation chart with devastating 96% win rate callout

### Quarto RevealJS Features Used
- `background-image` for immersive slides (3, title)
- Fragment reveals for architecture diagram build-up (5, 6, 7)
- `.r-stretch` for responsive image sizing (8, 13)
- CSS grid image gallery (11)
- Styled data table with `.hi` emphasis (12)
- `.keybox`, `.methodbox`, `.infobox` semantic boxes throughout
- `.two-col` comparison layouts (2, 6, 15)
- `.section-header` dividers (4, 9)

---

## Deck 2: Matrix-Game 2.0 — "Real-Time Interactive Worlds"

**File:** `decks/matrix-game-2.qmd`
**Theme:** `impeccable-creative.scss` (tech demo / product launch feel)
**Template base:** `creative.qmd`
**Target audience:** Game developers, tech enthusiasts, industry audience
**Narrative arc:** Limitation of v1 (offline, Minecraft-only) → Breakthrough (real-time 25fps) → Generalization (GTA, TempleRun, universal scenes) → Demo (visual showcase) → Impact (streaming interactive worlds)

### Slide-by-Slide Outline (18 slides)

| # | Title | Key Message | Visual Type | Asset / Diagram | Quarto Features |
|---|---|---|---|---|---|
| 1 | **Title:** Matrix-Game 2.0 — Real-Time Interactive Worlds | Open-source, real-time, streaming world model | Full-bleed hero image | `Matrix-Game-2/assets/images/cover.png` (cinematic city) | `background-image`, dark overlay text |
| 2 | **Where We Left Off** | v1 was groundbreaking but offline and Minecraft-only | Comparison diagram | SVG: v1 limitations → v2 goals (real-time, multi-game, streaming) | `.two-col`, left=v1 stats, right=v2 targets |
| 3 | **The Challenge: Real-Time Generation** | Generating 25 coherent frames per second from user input is extremely hard | Typography-focused | Large "25 FPS" stat with supporting text | `.keybox` with large stat number, fragment reveal |
| 4 | **Section: Architecture** | Section divider | Section header | Clean typography | `.section-header` |
| 5 | **Auto-Regressive Diffusion** | AR framework enables streaming: each chunk conditions on the previous | Diagram (create) | SVG: AR chain showing frame chunks flowing left-to-right, each conditioned on prior | `.methodbox`, animated fragment build (chunk by chunk) |
| 6 | **Self-Forcing Training** | Self-Forcing prevents error accumulation over long sequences | Diagram (create) | SVG comparison: naive AR (error drift) vs Self-Forcing (self-correction) | `.two-col` with `.warningbox` (problem) and `.tipbox` (solution) |
| 7 | **Action Control Module** | Keyboard + mouse inputs injected at each denoising step | Image + diagram | `Matrix-Game-2/assets/images/mouse.png` + keyboard diagram | Fragment build-up of control signals |
| 8 | **Section: Results** | Section divider | Section header | | `.section-header` |
| 9 | **GTA: Open-World Driving** | Matrix-Game generates coherent GTA driving sequences from a single image | Image sequence (filmstrip) | `Matrix-Game-2/demo_images/gta_drive/0000-0005.png` as horizontal filmstrip | CSS grid filmstrip (6 frames), fragment reveal left-to-right |
| 10 | **GTA: Detail Comparison** | Generated frames maintain environmental consistency and perspective | Full-bleed comparison | Large `gta_drive/0000.png` + `gta_drive/0003.png` side by side | `.two-col`, full-width images |
| 11 | **TempleRun: Endless Runner** | The model handles rapid camera motion and obstacle avoidance | Image sequence (filmstrip) | `Matrix-Game-2/demo_images/temple_run/0000-0005.png` as filmstrip | CSS grid filmstrip, fragment reveal |
| 12 | **Universal Scenes: Beyond Games** | Generalizes to real-world imagery — paintings, landscapes, streets | Image grid | 3×3 grid sampling `universal/` images (painting, mountain road, street, nature) | CSS 3×3 grid gallery, variety showcase |
| 13 | **Universal Scenes: Real-World Drive** | The model navigates real-world street scenes (Norwegian mountain road) | Full-bleed image | `Matrix-Game-2/demo_images/universal/0005.png` (mountain road) | `background-image` with text overlay |
| 14 | **Speed: 25 FPS on a Single GPU** | Achieves real-time inference on a single A100 | Stat comparison (create) | SVG: speedometer or comparison bars — v1 offline vs v2 25fps | `.keybox` with large "25 FPS" stat |
| 15 | **Hardware: Democratized Access** | Runs on 24GB VRAM — consumer-grade hardware viable | Stat with context | GPU comparison: A100 (80GB) → consumer 24GB card | `.infobox` with hardware specs |
| 16 | **Streaming: Infinite-Length Video** | AR design enables theoretically unbounded generation length | Diagram (create) | SVG: streaming pipeline with "..." extending rightward | `.methodbox` |
| 17 | **From Minecraft to Everything** | v1 proved the concept, v2 made it real-time and universal | Timeline diagram (create) | SVG timeline: v1 (May 2025) → v2 (Aug 2025) with key milestones | Horizontal timeline with fragment reveal |
| 18 | **Open Source: Build With Us** | MIT license, HuggingFace weights, 3 pretrained models | Clean typography | Links + model list (universal, GTA, TempleRun) | `.keybox`, final slide |

### Visual Highlight Moments ("Wow" slides)
1. **Slide 1** — Full-bleed Matrix-Game 2.0 cover image (cinematic city with light trails)
2. **Slide 9** — GTA driving filmstrip showing coherent sequence generation
3. **Slide 11** — TempleRun filmstrip with rapid camera motion
4. **Slide 12** — 3×3 universal scene grid showing incredible diversity (Monet painting → mountain road → urban street)
5. **Slide 13** — Full-bleed Norwegian mountain road (real-world generation)

### Quarto RevealJS Features Used
- `background-image` with dark overlays for immersive slides (1, 13)
- CSS filmstrip grids with fragment reveal for temporal sequences (9, 11)
- CSS 3×3 image gallery for variety showcase (12)
- `.two-col` side-by-side comparisons (2, 6, 10)
- `.warningbox` / `.tipbox` problem-solution pattern (6)
- `.methodbox` for architecture explanations (5, 16)
- `.keybox` for hero statistics (3, 14)
- `.section-header` for narrative pacing (4, 8)
- Fragment animations for sequential reveals throughout
- `.infobox` for technical specifications (15)

---

## Deck 3: Matrix-Game 3.0 — "The Full Vision: Memory, Speed, Scale"

**File:** `decks/matrix-game-3.qmd`
**Theme:** `impeccable.scss` (flagship theme — the "impeccable" look)
**Template base:** None (custom from scratch to showcase full capabilities)
**Target audience:** Broad AI/tech audience, conference keynote style
**Narrative arc:** Vision (what does it mean to truly simulate a world?) → v1-v2 Recap (2-slide speed run) → v3 Breakthroughs (memory, speed, scale, data) → Visual Showcase (10 diverse environments) → The Evolution (v1→v2→v3 comparison) → Future (toward general world simulation)

### Slide-by-Slide Outline (20 slides)

| # | Title | Key Message | Visual Type | Asset / Diagram | Quarto Features |
|---|---|---|---|---|---|
| 1 | **Title:** Matrix-Game 3.0 — Real-Time World Simulation with Long-Horizon Memory | Skywork AI, 720p, 40fps, minute-long coherent generation | Full-bleed background | `Matrix-Game-3/demo_images/006/image.png` (ancient stone ruins, atmospheric) | `background-image`, title with dark overlay |
| 2 | **"What does it take to simulate a world?"** | Philosophical hook — a world model must see, remember, and react | Typography-focused | Large question text, minimal design | Centered text, fragment reveal of 3 sub-points |
| 3 | **The Journey So Far** | Speed recap of v1 and v2 milestones | Timeline diagram (create) | SVG horizontal timeline: v1 (17B, Minecraft, May 2025) → v2 (real-time 25fps, multi-game, Aug 2025) → v3 (720p 40fps, memory, Mar 2026) | Fragment-animated timeline |
| 4 | **Section: Breakthrough 1 — Memory** | Section divider | Section header | | `.section-header` |
| 5 | **The Memory Problem** | Without memory, long sequences drift — objects disappear, scenes change randomly | Comparison (create) | SVG: "No memory" showing scene drift vs "With memory" showing consistency | `.two-col`, `.warningbox` (problem) vs `.tipbox` (solution) |
| 6 | **Prediction Residuals + Frame Re-injection** | Self-correction mechanism: compare prediction to reality, feed errors back | Diagram (create) | SVG: feedback loop diagram — predicted frame → residual computation → correction → next prediction | `.methodbox`, fragment build-up of the loop |
| 7 | **Camera-Aware Memory** | Spatiotemporal consistency through camera pose tracking | Diagram (create) | SVG: camera path through 3D space with memory anchors at keyframes | `.methodbox` |
| 8 | **Section: Breakthrough 2 — Speed** | Section divider | Section header | | `.section-header` |
| 9 | **40 FPS at 720p** | 60% faster than v2 at 4× the resolution | Hero stat | Large "40 FPS / 720p" typography with comparison to v2 (25fps/lower res) | `.keybox` with large stat, comparison below |
| 10 | **DMD Distillation: 50 Steps → 3 Steps** | Distribution Matching Distillation compresses inference from 50 denoising steps to just 3 | Diagram (create) | SVG: compression funnel — 50 steps (slow) distilled to 3 steps (fast) with quality preserved | `.methodbox`, fragment showing compression |
| 11 | **LightVAE + Quantization** | VAE decoder distillation + INT8 quantization for deployment efficiency | Tech specs | Specs table: pruning rates (0.5, 0.75), model variants, speed vs quality | Styled table with `.hi` on best tradeoffs |
| 12 | **Section: Breakthrough 3 — Scale** | Section divider | Section header | | `.section-header` |
| 13 | **28B MoE: Scaling with Experts** | 2×14B Mixture-of-Experts improves quality, dynamics, and generalization | Diagram (create) | SVG: MoE architecture — input routed to expert subnetworks | `.methodbox` |
| 14 | **Upgraded Data Engine** | Three data sources: Unreal Engine synthetic + AAA game data + real-world video | Diagram (create) | SVG: three-stream data pipeline converging into training | `.three-col` with icons for each source |
| 15 | **Section: Visual Showcase** | Section divider | Section header | | `.section-header` |
| 16 | **Worlds Matrix-Game Can Dream** | 10 diverse environments — from sci-fi corridors to snowy forests | Full-screen image gallery | 2×5 grid of ALL `Matrix-Game-3/demo_images/001-010` images | CSS grid gallery, the visual spectacle centerpiece |
| 17 | **Environment Close-ups** | Zooming into 4 standout environments | 2×2 grid | `001/image.png` (city), `005/image.png` (neon graffiti), `008/image.png` (sci-fi corridor), `002/image.png` (desert town) | `.four-col` or 2×2 grid, each with caption |
| 18 | **The Evolution: v1 → v2 → v3** | Visual comparison of capability progression across all three versions | Side-by-side-by-side | Three images: Minecraft (v1 forest) → GTA (v2 drive) → Unreal (v3 ruins) | `.three-col` with labels, the "wow" progression shot |
| 19 | **Toward General World Simulation** | Matrix-Game 3.0 is a step toward AI that truly understands and generates worlds | Typography-focused with image | `Matrix-Game-3/demo_images/007/image.png` (colorful forest path) as subtle background | `background-image` with low opacity, reflective closing text |
| 20 | **Open Source: Apache 2.0** | Model weights, code, and data pipeline — all open | Clean typography | HuggingFace link, citation, team credit | `.keybox`, final slide |

### Visual Highlight Moments ("Wow" slides)
1. **Slide 1** — Full-bleed ancient ruins (atmospheric, sets cinematic tone)
2. **Slide 9** — Hero stat "40 FPS / 720p" (the headline number)
3. **Slide 16** — Full-screen 2×5 gallery of 10 diverse environments (the visual spectacle peak — this is the slide people photograph)
4. **Slide 17** — Close-up quad of standout environments (neon graffiti, sci-fi corridor, desert, city)
5. **Slide 18** — v1→v2→v3 three-column evolution shot (narrative payoff)

### Quarto RevealJS Features Used
- `background-image` for immersive opening/closing (1, 19)
- CSS grid 2×5 image gallery — the most ambitious layout (16)
- CSS 2×2 spotlight grid (17)
- `.three-col` for evolution comparison (14, 18)
- `.two-col` with semantic boxes for problem/solution (5)
- `.methodbox` for technical architecture (6, 7, 10, 13)
- `.keybox` for hero statistics (9)
- `.warningbox` / `.tipbox` pairing (5)
- `.section-header` for pacing (4, 8, 12, 15)
- Fragment animations for timeline (3), diagram build-ups (6, 10)
- Styled data table (11)
- `background-opacity` for text-over-image slides (19)

---

## Cross-Deck Strategy

### Visual Consistency
All three decks share the impeccable design system (OKLCH colors, tinted neutrals, Plus Jakarta Sans / Source Sans 3 / JetBrains Mono). Each uses a different theme variant to show range while maintaining cohesion.

### Progressive Complexity
| Deck | Layout Complexity | Quarto Features Showcased |
|---|---|---|
| Deck 1 (v1) | Standard academic | Tables, `.keybox`, `.methodbox`, image grids, `.two-col` |
| Deck 2 (v2) | Creative tech demo | Filmstrip sequences, full-bleed images, 3×3 galleries, `.warningbox`/`.tipbox` pairs |
| Deck 3 (v3) | Keynote spectacle | 2×5 mega-gallery, `.three-col` evolution, hero stats, `background-image` with overlays |

### Asset Reuse Plan
- **Minecraft biome images** (GameWorldScore/): Used only in Deck 1 (biome grid, slide 11)
- **demo.gif**: Used only in Deck 1 (hero demo, slide 8)
- **human_win_rate.png**: Used only in Deck 1 (evaluation, slide 13)
- **cover.png**: Used only in Deck 2 (title hero, slide 1)
- **GTA/TempleRun/Universal demos**: Used only in Deck 2 (filmstrips + gallery, slides 9-13)
- **Matrix-Game-3 demo_images/**: Used only in Deck 3 (showcase gallery, slides 16-17)
- **mouse.png**: Used in Deck 1 (action control) and referenced conceptually in Deck 2
- **Cross-deck reference**: Deck 3 slide 18 uses one image from each version for the evolution comparison

### Diagrams to Create (SVG)
These diagrams need to be created for the decks:

**Deck 1:**
1. Traditional vs. world model pipeline comparison
2. Diffusion architecture (input → backbone → output)
3. Data pipeline (MineDojo → annotation → training)
4. Radar/quadrant diagram for GameWorld Score dimensions
5. Bar chart for controllability comparison

**Deck 2:**
1. Auto-regressive chunk chain
2. Naive AR vs Self-Forcing comparison
3. Streaming pipeline (infinite-length)
4. v1→v2 timeline

**Deck 3:**
1. v1→v2→v3 timeline with milestones
2. Prediction residual feedback loop
3. Camera-aware memory with 3D path
4. DMD distillation compression funnel
5. MoE routing architecture
6. Three-stream data pipeline

### Speaker Notes Strategy
Every content slide gets speaker notes containing:
- Talking points (what to say, not what's on screen)
- Key numbers for verbal delivery
- Transition cue to the next slide
- Timing target (1-2 min per slide)

---

## Implementation Order

1. **Deck 1** first — straightforward academic structure, validates the theme and build process
2. **Deck 3** second — most visually ambitious, benefits from lessons learned in Deck 1
3. **Deck 2** third — filmstrip sequences are the unique challenge; benefits from both prior decks

Each deck should pass `quarto render` and score >= 85 on `quality_score.py` before moving to the next.
