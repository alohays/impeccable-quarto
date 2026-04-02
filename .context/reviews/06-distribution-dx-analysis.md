# Distribution & Developer Experience Analysis

## Executive Summary

This analysis compares how **impeccable-original** (multi-tool design skills), **paper2pr** (academic slide pipeline), and **impeccable-quarto** (Quarto slide quality system) handle packaging, distribution, developer experience, and documentation. The goal is to identify high-impact improvements impeccable-quarto can adopt.

**Key finding:** impeccable-quarto has strong design foundations but lacks the distribution infrastructure of the reference projects. It has no CI/CD, no package distribution, no multi-tool support, and limited onboarding automation. The references provide clear blueprints for each gap.

---

## 1. Multi-Tool Distribution

### impeccable-original: Best-in-Class

impeccable-original supports **11 AI tools** from a single `source/skills/` directory:

| Tool | Config Dir | Notes |
|------|-----------|-------|
| Claude Code | `.claude/` | Full support: frontmatter, allowed-tools, hooks |
| Cursor | `.cursor/` | Skills with argument hints |
| Gemini CLI | `.gemini/` | Basic skill support |
| Codex CLI | `.codex/` | Skills + YAML sidecar |
| GitHub Copilot | `.agents/` | Skills, user-invocable |
| Kiro | `.kiro/` | Community-reported support |
| OpenCode | `.opencode/` | Skills, argument hints |
| Pi | `.pi/` | Skills, allowed-tools |
| Trae (CN/Intl) | `.trae-cn/`, `.trae/` | Skills, argument hints |
| Rovo Dev | `.rovodev/` | Skills, argument hints |

**Architecture:** Factory pattern (`scripts/lib/transformers/factory.js`) generates per-tool output from unified source. Five placeholder tokens (`{{model}}`, `{{config_file}}`, `{{ask_instruction}}`, `{{command_prefix}}`, `{{available_commands}}`) are resolved per-provider during build.

**Output:** Each provider gets its own `dist/{provider}/` directory with properly structured skill files. Universal bundles combine all providers. ZIP files generated for download.

### paper2pr: Single-Tool

paper2pr targets Claude Code exclusively. Its `.claude/` directory contains 11 agents, 26+ skills, and 18 rules. No multi-tool distribution.

### impeccable-quarto: Single-Tool

Currently Claude Code only. 7 agents, 18 skills, 6 rules in `.claude/`. No build system for multi-tool output.

### Gap Assessment

impeccable-quarto's skills and rules could serve Cursor, Gemini CLI, and other tools with a build step. The placeholder system from impeccable-original is directly applicable — the skill content is tool-agnostic, only the invocation mechanics differ.

**Priority: Medium.** Multi-tool support broadens reach but requires build infrastructure first.

---

## 2. Build Pipeline

### impeccable-original: Bun-Based, Automated

```
source/skills/ → [build.js] → dist/{provider}/ → build/ → Cloudflare Pages
```

- **Runtime:** Bun (fast JS runtime + bundler)
- **Key scripts:**
  - `scripts/build.js` (367 lines) — orchestrates full build
  - `scripts/lib/utils.js` (437 lines) — parsing, placeholders, frontmatter
  - `scripts/lib/transformers/factory.js` — provider-specific transforms
  - `scripts/lib/zip.js` — bundle packaging
- **Build outputs:**
  - 22 provider directories (11 providers x 2: unprefixed + prefixed)
  - ZIP bundles per provider + universal
  - Static JSON API data for website
  - Compiled CSS (Tailwind v4)
  - Bundled HTML/JS/CSS for website
  - Cloudflare config files (`_headers`, `_redirects`, `_routes.json`)
- **Commands:** `bun run build`, `bun run dev`, `bun run preview`, `bun run deploy`
- **CI:** Not explicitly found in repo, but deployment via `wrangler pages deploy`

### paper2pr: Shell + Python, CI-Driven

```
Slides/*.tex + Quarto/*.qmd → [GitHub Actions] → _site/ → GitHub Pages
```

- **Build steps in CI:** Quarto render → strip speaker notes → assemble site → deploy
- **Local mirror:** `scripts/sync_to_docs.sh` replicates CI locally
- **Quality gate:** `scripts/quality_score.py` blocks commits below score 80
- **Git hooks:** pre-commit (Korean text), clean filter (speaker notes)

### impeccable-quarto: Shell Scripts, Manual

```
examples/*.qmd → [render.sh] → docs/ → [deploy.sh --push] → GitHub Pages
```

- **Scripts:**
  - `render.sh` — wraps `quarto render` with timing/color output
  - `deploy.sh` — render all → copy to `docs/` → optional git push
  - `new-deck.sh` — interactive template scaffolding
  - `theme-preview.sh` — side-by-side theme comparison
  - `quality_score.py` — scoring tool (100-point rubric)
- **No package.json, no Makefile, no automated builds**
- **No CI/CD workflows** — deployment is entirely manual

### Gap Assessment

impeccable-quarto has functional scripts but no automation. The deploy.sh script is a good foundation but would benefit from CI/CD for:
- Automatic rendering on push
- Quality gate enforcement (block merge if score < 80)
- Theme compilation validation
- Example presentation health checks

**Priority: High.** CI/CD is table stakes for a quality system that claims to enforce standards.

---

## 3. Website / Demo

### impeccable-original: Full Marketing Site

**URL:** impeccable.style

- Vanilla JS + Tailwind v4 + Cloudflare Pages
- Landing page with case studies, command gallery, antipattern examples
- Interactive demos for each skill (before/after)
- Cheatsheet page for quick reference
- Static JSON API (`/api/skills`, `/api/commands`, `/api/patterns`)
- SEO: Open Graph images, sitemap.xml, robots.txt
- ~900 lines of HTML + supporting JS modules

### paper2pr: Functional GitHub Pages

- Auto-generated landing page with links to rendered slides
- Speaker notes stripped before deployment (multi-layer protection)
- Figures and R scripts served alongside slides
- No custom marketing — purely functional

### impeccable-quarto: GitHub Pages with Handcrafted Landing

- `docs/index.html` — custom landing page (in repo)
- Rendered examples served as static HTML
- `deploy.sh` handles site assembly
- No SEO metadata, no interactive demos, no case studies

### Gap Assessment

impeccable-quarto's landing page exists but is minimal. For a design quality system, the website should demonstrate the quality it advocates. Interactive before/after demos (like impeccable-original) would be high-impact for adoption.

**Priority: Medium.** A polished demo site builds credibility but isn't blocking core functionality.

---

## 4. Template System

### impeccable-original: Source Skills as Templates

Not a template system per se — skills act as transformation recipes. The `teach-impeccable` skill gathers design context, then all other skills apply consistently. No starter project templates.

### paper2pr: Rich Template Library

8 templates for structured workflows:
- `skill-template.md` — create new skills (with trigger phrases, examples, troubleshooting)
- `session-log.md` — work tracking (status, decisions, learnings)
- `requirements-spec.md` — complex task specification (MUST/SHOULD/MAY)
- `quality-report.md` — merge-time quality documentation
- `constitutional-governance.md` — immutable vs. flexible rules
- `exploration-readme.md` — experimental work documentation
- `speaker-notes-report.md` — notes backup/restore status

These templates formalize the workflow, not the content. They're meta-templates for process governance.

### impeccable-quarto: Content Templates

4 starter `.qmd` templates for common presentation types:
- `academic.qmd` — research presentation structure
- `corporate.qmd` — business/product deck
- `creative.qmd` — tech/developer talk
- `lightning.qmd` — 5-minute pitch

Plus `new-deck.sh` interactive scaffolding with 5 modes (Academic, Corporate, Creative, Lightning, Blank).

### Gap Assessment

impeccable-quarto has solid content templates but lacks process templates. Adopting paper2pr's session-log and quality-report patterns would strengthen the review workflow. The existing `new-deck.sh` is a strength worth preserving and enhancing.

**Priority: Low-Medium.** Templates are functional. Process templates add structure but aren't critical.

---

## 5. CI/CD

### impeccable-original: Cloudflare Pages (Manual Trigger)

Build and deploy via `bun run deploy` (wraps `wrangler pages deploy`). No GitHub Actions workflow found in the reference. Deployment is developer-initiated.

### paper2pr: Full GitHub Actions Pipeline

`.github/workflows/deploy.yml`:
1. Trigger: push to `main` or manual dispatch
2. Checkout → Setup Quarto → Render all `.qmd` files
3. Strip speaker notes from HTML (safety net)
4. Assemble `_site/` with slides, figures, code
5. Configure → Upload → Deploy to GitHub Pages

**Concurrency control:** single deployment at a time.
**Permissions:** read contents, write pages, write id-token.

### impeccable-quarto: None

No `.github/` directory. No workflows. Deployment is manual via `deploy.sh`.

### Gap Assessment

This is the biggest infrastructure gap. A GitHub Actions workflow modeled on paper2pr's would:
- Render all examples on push (catch compilation regressions)
- Run quality scoring (gate enforcement)
- Deploy to GitHub Pages automatically
- Validate theme SCSS compilation

**Priority: Critical.** A quality system without CI is self-contradictory.

---

## 6. Documentation Quality

### impeccable-original: Developer-Focused

| Document | Lines | Purpose |
|----------|-------|---------|
| `DEVELOP.md` | 207 | Architecture, build, adding providers, troubleshooting |
| `HARNESSES.md` | 87 | Feature matrix across 11 AI tools |
| `CLAUDE.md` | 68 | Build commands, versioning checklist |
| `AGENTS.md` | 100+ | Architecture overview, design philosophy |
| `README.md` | ~200 | User guide, installation, commands |

**Strengths:**
- Clear separation of user docs (README) vs. developer docs (DEVELOP)
- Feature matrix (HARNESSES.md) makes tool support transparent
- Checklists for common operations (versioning, adding skills)
- Troubleshooting sections

### paper2pr: Workflow-Focused

| Document | Lines | Purpose |
|----------|-------|---------|
| `AGENTS.md` | 100+ | Canonical project instructions |
| `MEMORY.md` | 73 | Persistent learnings from sessions |
| `README.md` | ~100 | Project overview, quick start |
| `guide/workflow-guide.qmd` | 200+ | Comprehensive workflow documentation |

**Strengths:**
- Living documentation (MEMORY.md captures learnings)
- Quarto-rendered guide with TOC and styling
- Clear Day 1 checklist for onboarding
- Template-driven documentation consistency

### impeccable-quarto: Comprehensive but Static

| Document | Lines | Purpose |
|----------|-------|---------|
| `README.md` | ~700 | Full project documentation |
| `CLAUDE.md` | ~250 | Claude Code integration guide |
| `AGENTS.md` | ~400 | Agent definitions and protocols |
| `CONTRIBUTING.md` | ~50 | Contribution guidelines |

**Strengths:**
- CLAUDE.md is thorough (design principles, anti-patterns, scoring, templates)
- AGENTS.md covers orchestration protocols well
- Clear ALWAYS/NEVER lists prevent common mistakes

**Weaknesses:**
- No DEVELOP.md (developer contribution guide separate from CONTRIBUTING)
- No HARNESSES.md equivalent (only supports one tool)
- No workflow guide (how to use the system end-to-end)
- CONTRIBUTING.md is minimal compared to the project's sophistication

### Gap Assessment

Documentation is strong for Claude Code integration but weak for human developers. A DEVELOP.md and a rendered workflow guide (like paper2pr's) would significantly improve contributor onboarding.

**Priority: Medium.** Documentation gaps slow adoption but don't block functionality.

---

## 7. Developer Onboarding

### impeccable-original

**Getting started:**
1. Clone repo
2. `bun install`
3. `bun run dev` (local server)
4. Edit `source/skills/`, run `bun run build`

**Time to first output:** ~2 minutes (clone + install + dev server)

**Developer guardrails:**
- `biome.json` for code linting
- Checklists in DEVELOP.md for adding skills/versions
- 12-location checklist for adding new skills (could be automated but is documented)

### paper2pr

**Getting started:**
1. Fork + clone
2. Run `claude` in project directory
3. Paste starter prompt
4. Approve configuration plan

**Time to first output:** ~5 minutes

**Developer guardrails:**
- Git hooks (pre-commit, clean filters)
- Quality gates (automated scoring)
- Protected files (hooks prevent editing key configs)
- Context monitoring (hook tracks token usage)

### impeccable-quarto

**Getting started:**
1. Clone repo
2. Install Quarto
3. `./scripts/new-deck.sh my-deck.qmd`
4. `quarto preview my-deck.qmd`

**Time to first output:** ~5 minutes (if Quarto already installed)

**Developer guardrails:**
- Quality scoring (manual: `python scripts/quality_score.py`)
- No git hooks
- No protected files
- No linting configuration beyond `pyproject.toml` (ruff)

### Gap Assessment

Onboarding is functional but lacks automation. Key improvements:
- Git hooks for quality gate enforcement (like paper2pr)
- A `setup.sh` script that checks prerequisites (Quarto, Python, fonts)
- Protected file hooks (prevent editing master theme accidentally)

**Priority: Medium.** Manual onboarding works but doesn't scale to team adoption.

---

## 8. Plugin Packaging

### impeccable-original: Claude Code Marketplace Ready

`.claude-plugin/` directory:

**`plugin.json`:**
```json
{
  "name": "impeccable",
  "version": "1.6.0",
  "author": { "name": "Paul Bakaus" },
  "homepage": "https://impeccable.style",
  "skills": "./.claude/skills"
}
```

**`marketplace.json`:**
```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "impeccable",
  "plugins": [{
    "name": "impeccable",
    "version": "1.6.0",
    "category": "design",
    "tags": ["design", "frontend", "ui", "ux"]
  }]
}
```

This is the emerging standard for distributing Claude Code skill packs.

### paper2pr & impeccable-quarto: None

Neither project has plugin packaging.

### Gap Assessment

impeccable-quarto should adopt the `.claude-plugin/` format. Its 18 skills could be distributed as an installable package for Claude Code users working with Quarto presentations.

**Priority: High.** Plugin packaging is the primary distribution channel for Claude Code skills.

---

## 9. Multi-Framework Potential

### Could impeccable-quarto support frameworks beyond Quarto?

**Current Quarto-specific elements:**
- YAML frontmatter format (`format: revealjs`)
- Pandoc markdown extensions (`::: {.class}` divs, `.notes` blocks)
- `.scss` theme files (RevealJS-specific variables)
- `quarto render` build command
- Cross-reference syntax (`@fig-`, `@tbl-`)

**Framework-portable elements:**
- Design principles (typography-first, OKLCH, tinted neutrals) — universal
- Quality scoring rubric — adaptable to any slide format
- Anti-pattern detection — mostly content-based, format-independent
- Agent orchestration protocols — tool-agnostic
- Source translation rules — input-format agnostic

**Potential targets:**
- **Marp** (Markdown → slides, VS Code extension)
- **Slidev** (Vue-based, developer-focused)
- **reveal.js** (direct, without Quarto wrapper)
- **Beamer** (LaTeX, academic standard — paper2pr already does this)
- **Google Slides / PowerPoint** (via API, limited styling control)

**Feasibility assessment:**

| Framework | Effort | Design Control | Value |
|-----------|--------|---------------|-------|
| Marp | Medium | Moderate (CSS themes) | Medium — different audience |
| Slidev | Medium | High (Vue components, CSS) | High — developer audience |
| reveal.js | Low | High (same CSS, no Quarto) | Medium — subset of Quarto users |
| Beamer | High | Low (LaTeX theming is complex) | Medium — paper2pr covers this |
| PPTX | Very High | Very Low (limited API) | Low — wrong tool for the job |

**Recommendation:** Focus on Quarto as the primary target. If expanding, start with raw reveal.js (minimal delta) then Slidev (similar audience, high design control). Don't chase Beamer or PPTX — they have fundamentally different styling models.

**Priority: Low.** Multi-framework dilutes focus. Quarto is the right bet for now.

---

## 10. Comparative Summary

| Capability | impeccable-original | paper2pr | impeccable-quarto |
|-----------|-------------------|----------|------------------|
| **AI Tools Supported** | 11 | 1 (Claude Code) | 1 (Claude Code) |
| **Build System** | Bun (JS, automated) | Shell + Python | Shell + Python (manual) |
| **CI/CD** | Cloudflare (manual deploy) | GitHub Actions (auto) | None |
| **Website** | Full marketing site | Functional GH Pages | Minimal GH Pages |
| **Templates** | Skills (not starter files) | 8 process templates | 4 content templates |
| **Quality Gates** | N/A (design skills, not QA) | Automated (score-gated commits) | Manual (run script) |
| **Plugin Packaging** | `.claude-plugin/` ready | None | None |
| **Developer Docs** | DEVELOP.md, HARNESSES.md | Workflow guide (Quarto) | README + CLAUDE.md |
| **Git Hooks** | None documented | Pre-commit, clean filters | None |
| **Onboarding Time** | ~2 min | ~5 min | ~5 min |

---

## 11. Prioritized Roadmap

### Phase 1: Infrastructure Foundation (Critical)

#### 1.1 GitHub Actions CI/CD
**What:** Create `.github/workflows/ci.yml` that:
- Renders all example `.qmd` files on push/PR
- Runs `quality_score.py` on all examples
- Fails if any example scores below 80
- Deploys to GitHub Pages on push to `main`

**Model:** paper2pr's `deploy.yml` with Quarto setup action.

**Effort:** Small (< 1 day). High impact.

#### 1.2 Claude Code Plugin Packaging
**What:** Create `.claude-plugin/plugin.json` and `marketplace.json` following impeccable-original's format. Package the 18 skills for distribution.

**Effort:** Small (< 1 hour). High impact — enables discovery.

#### 1.3 Quality Gate Hooks
**What:** Add a pre-commit or pre-push hook that runs `quality_score.py` on modified `.qmd` files and blocks if score < 80.

**Model:** paper2pr's hook architecture.

**Effort:** Small (< 1 day). Enforces the standards the project advocates.

### Phase 2: Developer Experience (High)

#### 2.1 Setup Script
**What:** Create `scripts/setup.sh` that:
- Checks Quarto installation and version
- Checks Python 3.10+
- Verifies font availability (Plus Jakarta Sans, Source Sans 3, JetBrains Mono)
- Installs git hooks
- Runs a test render to verify everything works

**Effort:** Medium (1 day).

#### 2.2 Developer Guide (DEVELOP.md)
**What:** Separate developer documentation from user README:
- Architecture overview (source/ vs .claude/ distinction)
- Adding theme variants (step-by-step)
- Adding templates (checklist)
- Modifying quality scoring
- Agent development guide
- Troubleshooting common issues

**Model:** impeccable-original's DEVELOP.md structure.

**Effort:** Medium (1 day).

#### 2.3 Workflow Guide
**What:** Create a Quarto-rendered workflow guide (like paper2pr's `guide/workflow-guide.qmd`) that walks through:
- Creating a deck from scratch
- Running the review cycle
- Using Claude Code skills
- Deploying to GitHub Pages
- Customizing for your organization

**Effort:** Medium (1-2 days).

### Phase 3: Distribution Expansion (Medium)

#### 3.1 Multi-Tool Build System
**What:** Implement a build step that generates skill files for Cursor and Gemini CLI from the same `source/` definitions. Start with these two (largest market share after Claude Code).

**Approach:**
- Create `scripts/build-skills.py` (or `.js` if adopting Bun)
- Define placeholder tokens (subset of impeccable-original's 5)
- Generate `.cursor/skills/` and `.gemini/skills/` directories
- Add to CI/CD build step

**Model:** impeccable-original's factory pattern, simplified.

**Effort:** Large (2-3 days). Medium impact — broadens adoption.

#### 3.2 Quarto Extension Format
**What:** Package the theme + templates as a [Quarto extension](https://quarto.org/docs/extensions/) so users can install with:
```bash
quarto add impeccable-quarto/impeccable
```

This is Quarto's native distribution mechanism and would dramatically simplify adoption.

**Effort:** Medium (1-2 days). High impact for Quarto users.

#### 3.3 Enhanced Demo Site
**What:** Upgrade `docs/index.html` to showcase:
- Interactive before/after demos (antipattern → fixed)
- Live theme previews (switch between variants)
- Score visualization (what each gate level looks like)
- Quick-start copy-paste snippets

**Model:** impeccable-original's landing page with interactive demos.

**Effort:** Large (3-5 days). Medium impact — builds credibility.

### Phase 4: Advanced (Low Priority)

#### 4.1 npm Package
**What:** Publish theme + templates as an npm package for JavaScript-ecosystem discoverability.

**Effort:** Medium. Low impact — Quarto extension is more natural.

#### 4.2 Feature Matrix (HARNESSES.md)
**What:** If multi-tool support is added, document which features each tool supports.

**Effort:** Small. Depends on 3.1.

#### 4.3 Session Logging Templates
**What:** Adopt paper2pr's session-log and quality-report templates for structured review workflows.

**Effort:** Small. Low impact — process formality most teams won't need initially.

---

## 12. Key Recommendations

1. **Add CI/CD immediately.** A quality enforcement system without automated enforcement undermines its own value proposition. Use GitHub Actions with Quarto's official setup action.

2. **Package as a Claude Code plugin.** The `.claude-plugin/` format is trivial to add and makes the 18 skills discoverable. This is the lowest-effort, highest-return improvement.

3. **Package as a Quarto extension.** This is the native distribution channel for Quarto users. `quarto add` is how the ecosystem distributes themes and templates.

4. **Don't chase multi-framework yet.** The design principles are portable, but the implementation is deeply Quarto-specific. Focus on being the best Quarto slide system rather than a mediocre multi-framework one.

5. **Adopt quality gate hooks from paper2pr.** The scoring system exists but isn't enforced. A pre-commit hook closes the loop.

6. **Write DEVELOP.md.** The project is sophisticated enough that contributors need a guide beyond CONTRIBUTING.md. impeccable-original's structure is a good model.

7. **Multi-tool support is a Phase 3 concern.** It's valuable but requires build infrastructure that doesn't exist yet. Get CI/CD and plugin packaging first.

---

## Appendix A: impeccable-original Placeholder System

For reference when implementing multi-tool support:

```javascript
// Provider → Placeholder values
{
  'claude-code': {
    model: 'Claude',
    config_file: 'CLAUDE.md',
    ask_instruction: 'STOP and call the AskUserQuestion tool to clarify.',
    command_prefix: '/',
    available_commands: '<computed from skills>'
  },
  'cursor': {
    model: 'the model',
    config_file: '.cursorrules',
    ask_instruction: 'ask the user directly to clarify what you cannot infer.',
    command_prefix: '/',
    available_commands: '<computed>'
  },
  // ... 9 more providers
}
```

## Appendix B: paper2pr CI/CD Pipeline

For reference when building GitHub Actions workflow:

```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: quarto-dev/quarto-actions/setup@v2
      - name: Render
        run: |
          for f in Quarto/*.qmd; do
            [[ "$f" == *_backup* ]] && continue
            quarto render "$f"
          done
      - name: Assemble _site
        run: |
          mkdir -p _site/slides
          cp Quarto/*.html _site/slides/
          cp -r Quarto/*_files _site/slides/ 2>/dev/null || true
          touch _site/.nojekyll
          cp pages/index.html _site/
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with: { path: '_site' }
      - uses: actions/deploy-pages@v4
```

## Appendix C: Plugin Packaging Template

For impeccable-quarto adoption:

```json
// .claude-plugin/plugin.json
{
  "name": "impeccable-quarto",
  "description": "Design quality system for Quarto RevealJS presentations. 18 skills for creating, reviewing, and perfecting slide decks.",
  "version": "0.1.0",
  "author": { "name": "impeccable-quarto contributors" },
  "repository": "https://github.com/alohays/impeccable-quarto",
  "skills": "./.claude/skills"
}
```
