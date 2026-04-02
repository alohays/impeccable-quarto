# Architecture Analysis: impeccable-quarto vs Reference Repos

**Analyst:** architecture-analyst  
**Date:** 2026-04-03  
**Scope:** Directory structure, build systems, configuration, distribution models, single-source-of-truth patterns, and actionable recommendations for impeccable-quarto.

---

## 1. Executive Summary

This analysis compares three projects that occupy overlapping but distinct niches in the AI-assisted presentation quality space:

| Dimension | impeccable-original | paper2pr | impeccable-quarto |
|-----------|--------------------|---------|--------------------|
| **Domain** | Frontend design skills for any web UI | Academic paper → Beamer/Quarto slides | Quarto RevealJS slide quality system |
| **Multi-tool?** | Yes (11 AI coding tools) | No (Claude Code only) | No (Claude Code only) |
| **Build system** | Bun-based factory (source → 11 dist targets) | Shell + CI/CD (LaTeX 3-pass, Quarto render) | Shell scripts (Quarto render) |
| **Source of truth** | `source/skills/` → generated dist | `Slides/*.tex` (Beamer) → derived Quarto | `.qmd` files + `source/rules/` |
| **Agent count** | 0 (skill-only model) | 11 specialized agents | 7 specialized agents |
| **Skill count** | 21 skills | 25+ skills | 18 skills |
| **Rule count** | 0 explicit (embedded in skills) | 18 governance rules | 6 governance rules |
| **Hooks** | 0 | 7 automation hooks | 0 |
| **Quality scoring** | Heuristic scoring in `/critique` skill | `quality_score.py` + quality_reports/ | `quality_score.py` + quality-gates.md |
| **Templates** | 0 | 8 document templates | 4 .qmd templates |

**Key finding:** impeccable-quarto has strong design fundamentals (OKLCH, typography-first, semantic boxes) but lags behind both references in build automation, hook-based guardrails, and the source→derived propagation pipeline. The project claims `source/` is canonical but has no mechanism to enforce this.

---

## 2. Directory Structure Comparison

### 2.1 impeccable-original: Multi-Tool Distribution Model

```
impeccable-original/
├── source/skills/{name}/SKILL.md    ← CANONICAL (21 skills)
├── source/skills/{name}/reference/  ← Domain reference docs
│
├── scripts/
│   ├── build.js                     ← Bun-based factory entry point
│   ├── lib/transformers/
│   │   ├── factory.js               ← Config-driven transformer
│   │   └── providers.js             ← 11 provider configs
│   └── lib/utils.js                 ← Frontmatter parsing, placeholders
│
├── dist/                            ← Generated output (11 providers × 2 variants)
│   ├── cursor/
│   ├── claude-code/
│   ├── gemini/
│   ├── trae/
│   └── ... (11 total)
│
├── .cursor/skills/    ← Synced from dist/ for local testing
├── .claude/skills/    ← Synced from dist/
├── .gemini/skills/    ← Synced from dist/
├── .trae/skills/      ← Synced from dist/
├── .trae-cn/skills/   ← Synced from dist/
├── .agents/skills/    ← Synced from dist/
├── .codex/skills/     ← Synced from dist/
├── .kiro/skills/      ← Synced from dist/
├── .opencode/skills/  ← Synced from dist/
├── .pi/skills/        ← Synced from dist/
├── .rovo-dev/skills/  ← Synced from dist/
│
├── CLAUDE.md          ← Build/deploy instructions
├── AGENTS.md          ← Architecture blueprint (250 lines)
├── DEVELOP.md         ← Developer guide (207 lines)
└── HARNESSES.md       ← Provider capabilities matrix
```

**Key pattern:** 505 files total, but only ~25 are canonical (in `source/`). Everything else is generated. The build system is the architectural centerpiece.

### 2.2 paper2pr: Deep Claude Code Integration

```
paper2pr/
├── .claude/
│   ├── agents/        ← 11 specialized agents
│   ├── skills/        ← 25+ workflow skills
│   ├── rules/         ← 18 path-scoped governance rules
│   ├── hooks/         ← 7 automation hooks
│   ├── settings.json  ← Permissions + hook wiring
│   └── WORKFLOW_QUICK_REF.md
│
├── Slides/            ← CANONICAL Beamer .tex files (source of truth)
├── Quarto/            ← DERIVED RevealJS .qmd files
│   ├── _quarto.yml
│   ├── *.scss         ← Theme files
│   ├── fonts/         ← Self-hosted fonts
│   └── _extensions/   ← Quarto extensions
│
├── Figures/{Paper}/   ← Per-paper assets (PDF + SVG)
├── Preambles/         ← Shared LaTeX preamble
├── Bibliography_base.bib
│
├── quality_reports/   ← Structured report hierarchy
│   ├── plans/
│   ├── session_logs/
│   ├── specs/
│   ├── merges/
│   └── {Paper}_*.md   ← Per-paper review artifacts
│
├── templates/         ← 8 document templates
├── scripts/           ← Build, deploy, quality tools
├── .github/workflows/ ← CI/CD (GitHub Actions)
│
├── CLAUDE.md          ← Placeholder
├── AGENTS.md          ← Core configuration (extensive)
└── MEMORY.md          ← Persistent cross-session learnings
```

**Key pattern:** 322 files. Heavy investment in `.claude/` infrastructure (agents, skills, rules, hooks). Beamer is canonical; Quarto is always derived. quality_reports/ acts as persistent institutional memory.

### 2.3 impeccable-quarto: Current State

```
impeccable-quarto/
├── source/            ← Declared canonical, but incomplete
│   ├── rules/         ← 3 rules (anti-patterns, design-standards, quality-gates)
│   └── references/    ← 6 reference docs
│
├── .claude/           ← Working Claude Code integration
│   ├── agents/        ← 7 agent definitions
│   ├── skills/        ← 18 skills
│   ├── rules/         ← 6 rules (superset of source/rules/)
│   └── settings.json
│
├── themes/            ← 5 SCSS theme files (master + 4 variants)
├── templates/         ← 4 .qmd starter templates
├── examples/          ← 5 complete example presentations
├── scripts/           ← 5 build/utility scripts
│
├── docs/              ← Generated HTML for GitHub Pages
├── _output/           ← Quarto render output
├── _quarto.yml        ← Project-level Quarto config
│
├── CLAUDE.md          ← Comprehensive (1,338 lines)
├── AGENTS.md          ← Agent roster + orchestration (418 lines)
└── pyproject.toml     ← Python project metadata
```

**Key pattern:** ~90 files. Clean separation of themes/templates/examples. But `source/` is underdeveloped — it holds only 3 of 6 rules, and has no mechanism to propagate changes to `.claude/`.

---

## 3. Build System Comparison

### 3.1 impeccable-original: Config-Driven Factory

The most sophisticated build system of the three. Entry point: `scripts/build.js`.

**Pipeline stages:**
1. Tailwind CSS compilation (`bunx @tailwindcss/cli`)
2. Static site bundle (HTML/JS/CSS → `build/`)
3. **Skills transformation** (core):
   ```
   for each provider in PROVIDERS:
     transform(source/skills/ → dist/{provider}/)
     transform(source/skills/ → dist/{provider}-prefixed/)  # i-audit variant
   ```
4. Universal assembly (all providers → `dist/universal/`)
5. ZIP bundle creation (per-provider + universal)
6. Static API generation (skills.json, commands.json for Cloudflare Pages)
7. Sync back to project root (dist → .cursor/, .claude/, etc.)

**Provider config** (`scripts/lib/transformers/providers.js`):
```javascript
export const PROVIDERS = {
  cursor: {
    configDir: '.cursor',
    frontmatterFields: ['license', 'compatibility', 'metadata'],
    // Cursor gets minimal frontmatter
  },
  'claude-code': {
    configDir: '.claude',
    frontmatterFields: ['user-invocable', 'argument-hint', 'license',
                        'compatibility', 'metadata', 'allowed-tools'],
    // Claude Code gets full frontmatter
  },
  // ... 9 more providers
};
```

**Placeholder system** — Build-time substitution:
- `{{model}}` → "Claude", "Gemini", "GPT", etc.
- `{{config_file}}` → "CLAUDE.md", ".cursorrules", etc.
- `{{command_prefix}}` → "/" for most, "$" for Codex

**Takeaway:** Single-source authoring with config-driven generation. Provider differences are data, not code duplication. This is the gold standard for multi-tool distribution.

### 3.2 paper2pr: Shell + CI/CD Pipeline

**Beamer compilation** (3-pass XeLaTeX):
```bash
cd Slides
TEXINPUTS=../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode Paper.tex
BIBINPUTS=..:$BIBINPUTS bibtex Paper
xelatex ... && xelatex ...  # Two more passes for cross-references
```

**Quarto compilation:**
```bash
cd Quarto && quarto render Paper.qmd
```

**GitHub Actions CI/CD** (`.github/workflows/deploy.yml`):
1. Checkout → Setup Quarto → Render all .qmd files
2. Strip speaker notes from HTML (privacy safety net)
3. Assemble site: landing page + slides + figures + Beamer PDFs
4. Deploy to GitHub Pages

**Figure pipeline:**
```
TikZ source (Beamer) → extract_tikz.tex → compile PDF → pdf2svg → SVG (Quarto)
```

**Takeaway:** Purpose-built for the Beamer→Quarto workflow with a proper CI/CD deployment pipeline. The speaker-notes stripping is a clever privacy mechanism.

### 3.3 impeccable-quarto: Minimal Shell Scripts

**Current scripts:**

| Script | Purpose | Lines |
|--------|---------|-------|
| `render.sh` | Quarto render wrapper (single file or --all) | 118 |
| `deploy.sh` | Deployment (basic) | ~50 |
| `new-deck.sh` | New deck from template | ~40 |
| `theme-preview.sh` | Side-by-side theme comparison | ~30 |
| `quality_score.py` | Python quality scorer (regex-based) | 150+ |

**Gap analysis:**
- No CI/CD pipeline (no `.github/workflows/`)
- No source→.claude sync mechanism
- No figure pipeline
- No speaker-notes stripping
- No pre-commit hooks
- `quality_score.py` exists but is not integrated into any automated workflow

---

## 4. Configuration Architecture Comparison

### 4.1 CLAUDE.md Patterns

| Aspect | impeccable-original | paper2pr | impeccable-quarto |
|--------|--------------------|---------|--------------------|
| **Length** | 30 lines | ~20 lines (placeholder) | 1,338 lines |
| **Purpose** | Build instructions only | Points to AGENTS.md | Everything in one file |
| **Content** | CSS build, dev server, versioning locations, skill update checklist | Minimal | Full project docs, design principles, templates, examples |

**Observation:** impeccable-quarto puts too much in CLAUDE.md. The 1,338-line file loads into every conversation context. Both references use CLAUDE.md as a lightweight pointer, moving detailed content to AGENTS.md, rules, or dedicated docs.

### 4.2 AGENTS.md Patterns

| Aspect | impeccable-original | paper2pr | impeccable-quarto |
|--------|--------------------|---------|--------------------|
| **Length** | 250 lines | 800+ lines | 418 lines |
| **Purpose** | Architecture blueprint (how build system works) | Core operational config (policies, commands, quality thresholds, quick ref) | Agent roster + orchestration protocol |
| **Content** | Repo structure, provider transforms, build overview | Everything needed to operate: principles, folder structure, commands, environments, quality gates, skill reference, Beamer/Quarto environments, project state | Agent descriptions, review pipeline phases, communication format |

### 4.3 Settings Architecture

**impeccable-original:** No `.claude/settings.json` (web app, not Claude Code project)

**paper2pr** (`.claude/settings.json`):
```json
{
  "permissions": {
    "allow": ["git *", "xelatex *", "quarto *", "python3 *", ...],
    "deny": []
  },
  "hooks": {
    "Notification": [{ "command": ".claude/hooks/notify.sh" }],
    "PreToolUse": [{ "command": ".claude/hooks/protect-files.sh", "matcher": "Edit|Write" }],
    "PostToolUse": [
      { "command": ".claude/hooks/context-monitor.py", "matcher": "Bash|Task" },
      { "command": ".claude/hooks/verify-reminder.py", "matcher": "Write|Edit" }
    ],
    "PreCompact": [{ "command": ".claude/hooks/pre-compact.py" }],
    "SessionStart": [{ "command": ".claude/hooks/post-compact-restore.py", "matcher": "compact|resume" }],
    "Stop": [{ "command": ".claude/hooks/log-reminder.py" }]
  }
}
```

**impeccable-quarto** (`.claude/settings.json`):
```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep", "Bash(quarto render *)", ...],
    "deny": ["Bash(rm -rf *)", "Bash(git push --force *)"]
  }
}
```

**Gap:** impeccable-quarto has no hooks at all. paper2pr's hook architecture provides:
- File protection (prevent accidental edits to critical files)
- Context monitoring (warn when approaching limits)
- Verification reminders (prompt to verify after edits)
- State capture/restore across context compression
- Session logging reminders

---

## 5. Source of Truth Patterns

### 5.1 impeccable-original: Automated Propagation

```
source/skills/audit/SKILL.md     ← Write here
        │
        ├─ bun run build
        │
        ├─► dist/cursor/.cursor/skills/audit/SKILL.md
        ├─► dist/claude-code/.claude/skills/audit/SKILL.md
        ├─► dist/gemini/.gemini/skills/audit/SKILL.md
        └─► ... (11 providers × 2 variants = 22 outputs)
        │
        └─► .cursor/skills/audit/SKILL.md  (sync back for local testing)
```

**Enforcement:** The build step is the single gate. `source/` → `dist/` → project root. Editing a distributed file directly would be overwritten on next build.

### 5.2 paper2pr: Rule-Enforced with Dual Format

```
Slides/Paper.tex     ← CANONICAL (Beamer LaTeX)
        │
        ├─ /translate-to-quarto (11-phase agent workflow)
        │
        └─► Quarto/Paper.qmd    ← DERIVED (always re-derivable from .tex)
```

**Enforcement mechanisms:**
1. **beamer-quarto-sync.md rule:** Every Beamer edit MUST sync to Quarto in the same task
2. **single-source-of-truth.md rule:** TikZ freshness protocol — diff-check before using derived SVGs
3. **protect-files.sh hook:** Blocks accidental edits to canonical files (Bibliography_base.bib, settings.json)
4. **Agent separation:** quarto-critic compares Quarto output against Beamer PDF (adversarial verification)

### 5.3 impeccable-quarto: Declared but Unenforced

```
source/rules/anti-patterns.md       ← Declared canonical
source/rules/design-standards.md    ← Declared canonical
source/rules/quality-gates.md       ← Declared canonical

.claude/rules/anti-patterns.md      ← Copy (manual? automated? unclear)
.claude/rules/design-standards.md   ← Copy
.claude/rules/quality-gates.md      ← Copy
.claude/rules/orchestrator-protocol.md  ← NO source/ equivalent
.claude/rules/review-protocol.md        ← NO source/ equivalent
.claude/rules/source-translation.md     ← NO source/ equivalent
```

**Problems identified:**
1. **No sync mechanism:** There is no script, build step, or hook that propagates `source/` → `.claude/`
2. **Incomplete source:** Only 3 of 6 `.claude/rules/` files have a `source/rules/` counterpart. The other 3 (orchestrator-protocol, review-protocol, source-translation) exist only in `.claude/rules/`
3. **No enforcement:** Nothing prevents editing `.claude/rules/` directly, which would make `source/` stale
4. **source/references/ is disconnected:** The 6 reference docs in `source/references/` are not directly referenced by agents or skills — they are stand-alone documents
5. **Skills and agents have no source/ counterpart:** All 18 skills and 7 agents live only in `.claude/` — there is no `source/skills/` or `source/agents/` directory

**CLAUDE.md claims:**
> `source/` — Single source of truth for all definitions  
> `.claude/` — Claude Code integration (derived from source/)

This is aspirational, not actual. In practice, `.claude/` is the real source of truth.

---

## 6. Agent and Skill Architecture Comparison

### 6.1 Skill Format Comparison

**impeccable-original** (SKILL.md in each skill directory):
```yaml
---
name: audit
description: "Run a comprehensive design quality audit"
user-invocable: true
argument-hint: "[area (feature, page, component...)]"
license: Apache 2.0
compatibility: "CSS/HTML/JS project"
metadata:
  category: diagnostic
allowed-tools: [Read, Glob, Grep]
---
## MANDATORY PREPARATION
Invoke `/frontend-design` first...
```

**paper2pr** (SKILL.md in each skill directory):
```yaml
---
name: qa-quarto
description: "Run adversarial QA loop for Quarto slides"
argument-hint: "[PaperName]"
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Agent]
context:
  - .claude/rules/quality-gates.md
  - .claude/rules/orchestrator-protocol.md
---
## Phases
1. Compile and verify...
```

**impeccable-quarto** (flat .md files, no subdirectories):
```yaml
---
name: audit-slides
description: "Technical quality audit for a presentation"
user-invocable: true
argument-hint: "[file.qmd]"
---
## Audit Process
1. Read the file...
```

**Key differences:**

| Feature | impeccable-original | paper2pr | impeccable-quarto |
|---------|--------------------|---------|--------------------|
| Skill location | `skills/{name}/SKILL.md` | `skills/{name}/SKILL.md` | `skills/{name}.md` (flat) |
| Reference docs | Inline in skill subdirectory | Via `context:` field pointing to rules | Embedded in CLAUDE.md |
| Prerequisite chain | `## MANDATORY PREPARATION` | Phase-based orchestration | None (skills are independent) |
| Tool scoping | `allowed-tools:` frontmatter | `allowed-tools:` frontmatter | Not specified |
| Context injection | Via reference/ subdirectory | Via `context:` field | Via CLAUDE.md (global) |

### 6.2 Agent Architecture Comparison

**paper2pr** (11 agents):
```
Diagnostic (read-only):     proofreader, slide-auditor, quarto-critic, pedagogy-reviewer, 
                            domain-reviewer, tikz-reviewer, r-reviewer
Creative:                   beamer-translator, script-writer
Fix:                        quarto-fixer
Verification:               verifier
```

**impeccable-quarto** (7 agents):
```
Diagnostic (read-only):     slide-critic, layout-auditor, typography-reviewer
Creative:                   content-translator, theme-designer
Fix:                        slide-fixer
Verification:               verifier
```

**Observations:**
- Both projects enforce adversarial separation (critic never edits, fixer never self-assesses)
- paper2pr has domain-specific reviewers (pedagogy, TikZ, R code) that impeccable-quarto doesn't need
- impeccable-quarto's agent set is well-scoped for its domain
- paper2pr agents have explicit tool lists; impeccable-quarto agents do not

---

## 7. Unique Patterns Worth Adopting

### 7.1 From impeccable-original

#### A. Config-Driven Build System
The factory pattern (`providers.js` + `factory.js`) enables single-source authoring with multi-target output. Even though impeccable-quarto only targets Claude Code today, this pattern would:
- Enforce the source→.claude propagation that's currently missing
- Make future multi-tool support trivial
- Prevent source/ drift

#### B. Skill Subdirectory Pattern
Skills as directories (`skills/audit/SKILL.md` with `reference/` subfolder) rather than flat files (`skills/audit-slides.md`) enables:
- Co-located reference documents
- Skill-specific assets (templates, examples)
- Cleaner separation of concerns

#### C. Placeholder System
Template variables (`{{model}}`, `{{config_file}}`) in skill content enable:
- Single-source authoring for multiple contexts
- Easy adaptation if the project expands to other AI tools

#### D. Prefixed Variant Generation
The `i-audit` prefixed variant pattern avoids namespace collisions when skills are installed alongside other skill sets.

### 7.2 From paper2pr

#### A. Hook Infrastructure
Seven hooks covering the full agent lifecycle. Highest-value hooks for impeccable-quarto:

1. **protect-files.sh** — Prevent edits to `themes/impeccable.scss` (master theme), `source/rules/*` (canonical rules)
2. **verify-reminder.py** — After any Edit/Write to a `.qmd` file, remind to run `quarto render`
3. **pre-compact.py / post-compact-restore.py** — Capture and restore state across context compression (critical for multi-round QA loops)
4. **context-monitor.py** — Warn when approaching context limits during long review sessions

#### B. Quality Reports Directory
Structured report hierarchy (`quality_reports/plans/`, `session_logs/`, `specs/`, `merges/`) provides:
- Persistent institutional memory across sessions
- Audit trail for quality decisions
- Input for future reviews ("what was tried before?")

#### C. MEMORY.md Pattern
Persistent cross-session learnings committed to the repo:
```markdown
[LEARN:workflow] Spec-then-plan reduces rework 30-50%
[LEARN:design] Framework-oriented > prescriptive rules
```
This is different from Claude Code's personal memory — it's project-level, committed, and shared.

#### D. Session Logging Rule
Mandatory session logs (`quality_reports/session_logs/YYYY-MM-DD_description.md`) with standardized template. Especially valuable for multi-round QA loops where context compression could lose important decisions.

#### E. `context:` Field in Skills
Skills explicitly declare which rules they need loaded:
```yaml
context:
  - .claude/rules/quality-gates.md
  - .claude/rules/orchestrator-protocol.md
```
This is more precise than impeccable-quarto's approach of loading everything via CLAUDE.md.

#### F. CI/CD Deployment Pipeline
GitHub Actions workflow that renders, strips speaker notes, assembles, and deploys. impeccable-quarto has `docs/` output but no automated deployment.

#### G. Templates for Documentation
Eight reusable templates (session-log, quality-report, requirements-spec, etc.) standardize the quality documentation process.

#### H. Path-Scoped Rules
paper2pr rules declare which file paths they apply to:
```yaml
# In rule frontmatter
paths:
  - Slides/**/*.tex
  - Quarto/**/*.qmd
```
This prevents rules from being loaded in irrelevant contexts.

---

## 8. Gap Analysis: impeccable-quarto

### 8.1 Critical Gaps

| # | Gap | Impact | Reference Solution |
|---|-----|--------|-------------------|
| G1 | **No source→.claude sync** | source/ is aspirational, not functional | impeccable-original's build.js |
| G2 | **No hooks** | No automated guardrails or reminders | paper2pr's 7 hooks |
| G3 | **No CI/CD** | No automated rendering or deployment | paper2pr's deploy.yml |
| G4 | **CLAUDE.md overload** (1,338 lines) | Wastes context window every conversation | Split into focused files |

### 8.2 Structural Gaps

| # | Gap | Impact | Reference Solution |
|---|-----|--------|-------------------|
| G5 | **Flat skill files** (no subdirectories) | Can't co-locate reference docs with skills | impeccable-original's `skills/{name}/SKILL.md` |
| G6 | **No `allowed-tools` in skills** | Skills can't scope their tool access | Both references use this |
| G7 | **No `context:` field in skills** | Can't declare rule dependencies per-skill | paper2pr's context field |
| G8 | **No quality_reports/ directory** | No persistent record of review outcomes | paper2pr's structured hierarchy |
| G9 | **Incomplete source/ directory** | 3 rules, 0 skills, 0 agents in source/ | impeccable-original's complete source/ |
| G10 | **No MEMORY.md** | No persistent cross-session project learnings | paper2pr's MEMORY.md |

### 8.3 Operational Gaps

| # | Gap | Impact | Reference Solution |
|---|-----|--------|-------------------|
| G11 | **No speaker-notes privacy** | Notes published with rendered output | paper2pr's strip_speaker_notes.py |
| G12 | **No pre-commit hooks** | Quality issues can be committed | paper2pr's check-korean-pre-commit.sh pattern |
| G13 | **No session logging** | Multi-round QA loop state lost on context compression | paper2pr's session-logging.md rule |
| G14 | **No document templates** | Quality reports have no standard format | paper2pr's 8 templates/ |
| G15 | **No WORKFLOW_QUICK_REF.md** | No quick-start guide for agents | paper2pr's WORKFLOW_QUICK_REF.md |

---

## 9. Actionable Recommendations

### Priority 1: Fix the Source-of-Truth Architecture (G1, G9)

**Problem:** CLAUDE.md declares `source/` canonical, but `.claude/` is the actual source.

**Recommendation:** Choose one of two approaches:

**Option A: Make source/ truly canonical** (impeccable-original model)
1. Move all skills to `source/skills/{name}/SKILL.md`
2. Move all agents to `source/agents/{name}.md`
3. Move all rules to `source/rules/` (add the 3 missing ones)
4. Create `scripts/sync.sh` that copies `source/` → `.claude/`
5. Add pre-commit hook that runs sync before commit

**Option B: Abandon the source/ abstraction** (simpler)
1. Delete `source/` (or rename to `docs/references/`)
2. Make `.claude/` the single source of truth
3. Update CLAUDE.md to reflect reality
4. Keep `source/references/` as `docs/design-references/` for human reading

**Recommendation:** Option A if multi-tool support is planned. Option B if Claude Code is the only target.

### Priority 2: Add Hook Infrastructure (G2)

Create these four hooks (adapted from paper2pr):

```
.claude/hooks/
├── verify-after-edit.sh      # After Edit/Write on *.qmd → remind to quarto render
├── protect-source.sh         # Block direct edits to source/ (if Option A)
├── pre-compact-state.py      # Save QA loop state before context compression
└── post-compact-restore.py   # Restore state after compression
```

Wire in `.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "command": ".claude/hooks/verify-after-edit.sh",
        "matcher": "Edit|Write"
      }
    ],
    "PreCompact": [
      { "command": ".claude/hooks/pre-compact-state.py" }
    ],
    "SessionStart": [
      {
        "command": ".claude/hooks/post-compact-restore.py",
        "matcher": "compact|resume"
      }
    ]
  }
}
```

### Priority 3: Slim Down CLAUDE.md (G4)

**Current:** 1,338 lines loaded into every conversation.

**Proposed split:**

| Content | Move To | Lines Saved |
|---------|---------|-------------|
| Quality gates rubric | `.claude/rules/quality-gates.md` | Already there — remove from CLAUDE.md |
| Anti-pattern reference | `.claude/rules/anti-patterns.md` | Already there — remove from CLAUDE.md |
| Design standards | `.claude/rules/design-standards.md` | Already there — remove from CLAUDE.md |
| Build commands | `scripts/README.md` | ~30 lines |
| Theme variable reference | `themes/README.md` | ~50 lines |
| Semantic box usage | `source/references/slide-patterns.md` | ~40 lines |
| Layout usage examples | `source/references/slide-patterns.md` | ~30 lines |
| Fragment syntax | `source/references/motion-design.md` | ~15 lines |

**Target:** CLAUDE.md should be ~200-300 lines — project overview, directory structure, key workflows, and pointers to detailed docs. Rules are auto-loaded by Claude Code from `.claude/rules/`.

### Priority 4: Restructure Skills as Directories (G5, G6, G7)

**Current:** `.claude/skills/audit-slides.md`

**Proposed:**
```
.claude/skills/audit-slides/
├── SKILL.md                   # Skill definition
└── reference/
    └── quality-checklist.md   # Skill-specific reference doc
```

Add to SKILL.md frontmatter:
```yaml
---
name: audit-slides
description: "Technical quality audit for a presentation"
user-invocable: true
argument-hint: "[file.qmd]"
allowed-tools: [Read, Glob, Grep, Bash]
context:
  - .claude/rules/quality-gates.md
  - .claude/rules/anti-patterns.md
---
```

### Priority 5: Add Quality Reports Infrastructure (G8, G13, G14)

```
quality_reports/
├── plans/           # Pre-task planning docs
├── session_logs/    # Per-session work logs
└── reviews/         # Quality review artifacts
```

Create templates:
```
templates/
├── session-log.md       # Standardized session log format
├── quality-report.md    # Review report template
└── review-plan.md       # Pre-review planning template
```

### Priority 6: Add CI/CD Pipeline (G3)

Create `.github/workflows/render.yml`:
```yaml
name: Render & Deploy
on:
  push:
    branches: [main]
    paths: ['examples/**', 'themes/**', '_quarto.yml']
jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: quarto-dev/quarto-actions/setup@v2
      - run: quarto render
      - uses: actions/deploy-pages@v4
```

### Priority 7: Add MEMORY.md (G10, G15)

Create `MEMORY.md` for persistent project-level learnings and `WORKFLOW_QUICK_REF.md` for agent quick-start guidance.

---

## 10. Architecture Comparison Matrix

| Capability | impeccable-original | paper2pr | impeccable-quarto | Gap? |
|-----------|:---:|:---:|:---:|:---:|
| Single source of truth (declared) | Yes | Yes | Yes | -- |
| Single source of truth (enforced) | Yes (build system) | Yes (rules + hooks) | No | **Critical** |
| Multi-tool distribution | Yes (11 tools) | No | No | Optional |
| Build system | Bun factory | Shell + CI/CD | Shell scripts | **Major** |
| CI/CD pipeline | Cloudflare Pages | GitHub Actions | None | **Major** |
| Hook infrastructure | N/A (web app) | 7 hooks | 0 hooks | **Major** |
| Agent definitions | 0 | 11 | 7 | OK |
| Skill definitions | 21 | 25+ | 18 | OK |
| Governance rules | 0 (in skills) | 18 | 6 | Adequate |
| Quality scoring | In /critique skill | quality_score.py | quality_score.py | OK |
| Quality reports | N/A | Structured hierarchy | None | **Major** |
| Session logging | N/A | Mandatory rule | None | **Major** |
| Document templates | N/A | 8 templates | 4 .qmd templates | Partial |
| Persistent memory | N/A | MEMORY.md | None | Minor |
| Skill subdirectories | Yes | Yes | No (flat) | Minor |
| Skill context declaration | Via reference/ | Via `context:` field | None | Minor |
| Tool scoping in skills | `allowed-tools:` | `allowed-tools:` | None | Minor |
| Speaker notes privacy | N/A | Strip on deploy | None | Minor |
| CLAUDE.md size | 30 lines | 20 lines | 1,338 lines | **Bloated** |

---

## 11. Summary

impeccable-quarto has **strong domain design** (OKLCH color science, typography-first approach, semantic boxes, adversarial review pipeline) but **weak infrastructure** (no build pipeline, no hooks, no CI/CD, unenforced source-of-truth). The two reference projects show complementary solutions:

- **impeccable-original** solves the distribution problem: single-source authoring with automated multi-target generation via a config-driven factory
- **paper2pr** solves the operational problem: hooks, session logging, quality reports, CI/CD, and rule-enforced source-of-truth create a robust working environment

The highest-impact improvements are:
1. Fix the source→.claude propagation (or abandon the abstraction)
2. Add hooks for guardrails and state management
3. Slim CLAUDE.md from 1,338 lines to ~250
4. Add CI/CD for automated rendering and deployment
5. Add quality_reports/ infrastructure for persistent review artifacts

These changes would bring impeccable-quarto from a well-designed but manually-operated system to an automated, self-enforcing quality pipeline on par with its reference projects.
