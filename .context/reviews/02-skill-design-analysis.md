# Skill & Command Design Analysis

**Analyst:** skill-design-analyst  
**Date:** 2026-04-03  
**Scope:** impeccable-original (20 commands), paper2pr (24 skills), impeccable-quarto (18 skills)

---

## 1. Skill Anatomy: Structural Comparison

### 1.1 File Format

| Aspect | impeccable-original | paper2pr | impeccable-quarto |
|--------|-------------------|----------|-------------------|
| **Location** | `source/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` | `.claude/skills/<name>.md` |
| **Nesting** | Subdirectory per skill + `reference/` subdirs | Subdirectory per skill | Flat files (no subdirs) |
| **Frontmatter** | `name`, `description`, `argument-hint`, `user-invocable`, optional `license` | `name`, `description`, `argument-hint`, `allowed-tools`, optional `context`, `version`, `author` | `name`, `description`, `user-invocable`, `argument-hint` |
| **Reference files** | Yes (`critique/reference/`, `frontend-design/reference/`) | No (references inline or in rules) | No |
| **Build system** | Yes (`source/` → `dist/` with provider-specific placeholders) | No (files are canonical) | No (files are canonical) |

**Key Insight:** impeccable-original uses a **two-tier architecture** where `source/` is canonical and gets compiled to provider-specific outputs. It also uses **reference subdirectories** within skills for deep domain knowledge (cognitive load theory, heuristic scoring rubrics, persona definitions, typography guides). This is the most sophisticated content architecture of the three.

paper2pr adds `allowed-tools` (tool restriction per skill) and `context: fork` (agent isolation), which are operational controls absent from the others.

impeccable-quarto uses the simplest structure: flat `.md` files with minimal frontmatter. This works but sacrifices the ability to attach deep reference material to specific skills.

### 1.2 Prompt Structure Patterns

All three repos follow a recognizable prompt engineering pattern, but with distinct flavors:

#### impeccable-original: The "Design Director" Pattern

```
MANDATORY PREPARATION → Context gathering chain → Assessment → Plan → Execute → Verify
```

Every skill starts with:
```markdown
## MANDATORY PREPARATION
Invoke {{command_prefix}}frontend-design — it contains design principles,
anti-patterns, and the **Context Gathering Protocol**. Follow the protocol
before proceeding...
```

This is a **forced dependency chain**: every design skill loads `frontend-design` first, which contains the shared aesthetic guidelines and anti-pattern catalog. The `teach-impeccable` skill is the bootstrap — it gathers project context once and persists it.

**Strengths:**
- Shared context loading ensures consistency across all 20 commands
- The `{{command_prefix}}` / `{{config_file}}` / `{{ask_instruction}}` placeholders enable multi-provider deployment
- Reference files provide deep domain knowledge (e.g., cognitive load theory in `critique/reference/cognitive-load.md`)
- The "AI Slop Test" is threaded through every design skill as a quality gate

**Weaknesses:**
- The dependency on `frontend-design` creates a bottleneck — every skill must load it
- Placeholder system requires a build step

#### paper2pr: The "Phased Workflow" Pattern

```
Phase 0: Pre-flight → Phase 1: Analysis → Phase 2: Execution → Phase 3: QA → Phase N: Report
```

paper2pr skills are structured as **explicit multi-phase workflows** with numbered phases and clear gate conditions:

```markdown
## Phase 0: Pre-Flight Checks
### 0A. Environment Parity Audit
### 0B. TikZ Freshness Verification
### 0C. RDS Data Inventory
### 0D. Citation Key Mapping
```

**Strengths:**
- Extremely explicit about what happens in what order
- Phase gates prevent skipping steps
- Pre-flight checks catch common failures early
- The `allowed-tools` frontmatter restricts what each skill can do (security/focus)
- `context: fork` enables isolated agent execution

**Weaknesses:**
- Very domain-specific (Beamer, LaTeX, econometrics) — harder to generalize
- Some skills are operationally complex (translate-to-quarto has 11 phases)

#### impeccable-quarto: The "Structured Template" Pattern

```
[MANDATORY PREPARATION] → [IMPLEMENTATION STEPS] → [OUTPUT FORMAT] → [ANTI-PATTERNS TO AVOID] → [QUALITY CHECKS]
```

Our skills use a clean sectioned format:
```markdown
[MANDATORY PREPARATION]
- Read rules...
- Gather context...

[IMPLEMENTATION STEPS]
1. Step one...
2. Step two...

[OUTPUT FORMAT]
```markdown template...```

[ANTI-PATTERNS TO AVOID]
- Do NOT...

[QUALITY CHECKS]
- Verify...
```

**Strengths:**
- Highly consistent structure across all 18 skills
- The `[OUTPUT FORMAT]` section with markdown templates ensures predictable output
- Explicit `[ANTI-PATTERNS TO AVOID]` section per skill
- Clear separation of diagnostic vs. fix skills

**Weaknesses:**
- Lacks the deep reference material that impeccable-original provides
- No shared context loading mechanism (each skill independently reads rules)
- No tool restriction or agent isolation controls

---

## 2. Command Composition: How Commands Chain Together

### 2.1 impeccable-original: The Hub-and-Spoke Model

impeccable-original uses `frontend-design` as a **hub skill** that every other skill invokes first. The composition model is:

```
teach-impeccable (bootstrap, one-time)
       ↓
frontend-design (hub — loaded by every design skill)
       ↓
┌──────┼──────┐
audit  critique  normalize  polish  ...
```

The recommended workflow chains commands sequentially:
```
/audit → identifies issues → /normalize → fixes them → /polish → final pass
/critique → design review → /bolder or /quieter → tone adjustment → /polish
```

The `audit` and `critique` skills both end with **explicit command recommendations**:
```markdown
## Recommended Actions
1. **[P?] `/command-name`** — Brief description (specific context from findings)
```

This creates a natural **command recommendation pipeline**: diagnostic skills suggest which fix skills to run next, using the specific findings as context.

**Notable patterns:**
- **Intensity dial:** `/bolder` ↔ `/quieter` act as opposing forces on a spectrum
- **Pipeline terminator:** Every recommended fix sequence ends with `/polish`
- **Cross-references:** `audit` maps issues to specific skills; `critique` maps issues to specific skills
- **Dual assessment:** `audit` is technical (measurable), `critique` is design (subjective) — they complement each other

### 2.2 paper2pr: The Orchestrated Pipeline Model

paper2pr uses **explicit multi-agent orchestration** within individual skills. The `/slide-excellence` skill is the clearest example:

```
/slide-excellence [file]
  ├── Agent 1: Visual Audit (parallel)
  ├── Agent 2: Pedagogical Review (parallel)
  ├── Agent 3: Proofreading (parallel)
  ├── Agent 4: TikZ Review (conditional, parallel)
  ├── Agent 5: Content Parity (conditional, parallel)
  └── Agent 6: Substance Review (optional, parallel)
       ↓
  Synthesize Combined Summary
```

The `/qa-quarto` skill implements an **adversarial loop**:
```
Critic audit → Fixer → Re-audit → Loop until APPROVED (max 5 rounds)
```

And `/translate-to-quarto` is a **full translation pipeline** with 11 phases, gated by verification steps.

**Notable patterns:**
- **Conditional agents:** TikZ review only runs if file contains TikZ
- **Hard gates:** Non-negotiable quality conditions (no overflow, content parity, notation fidelity)
- **Max loop limits:** Every iterative process has explicit termination conditions (max 5 rounds)
- **Report persistence:** Every agent saves output to `quality_reports/` for later reference

### 2.3 impeccable-quarto: The Review Protocol Model

Our project defines command composition primarily through the **review protocol** (`review-protocol.md`), not within individual skills:

```
/review-slides [file]
  Phase 1: slide-critic + layout-auditor (parallel)
  Phase 2: typography-reviewer + verifier (parallel)
  Phase 3: Synthesis → Action plan
  Phase 4: Fix recommendations → map to skills
```

The `/qa-loop` implements the adversarial cycle similar to paper2pr.

**What we do well:**
- Clean separation between diagnostic skills and fix skills
- Clear review protocol with phase gates
- Score-based quality gates

**What we're missing compared to the references:**
- No hub skill providing shared context (like impeccable-original's `frontend-design`)
- No conditional agent execution (like paper2pr's TikZ-conditional agents)
- No report persistence to files (the reference repos save to `quality_reports/`)
- No explicit command recommendation in diagnostic skills (impeccable-original's audit → "run /normalize" pattern)

---

## 3. Skill-Agent Integration

### 3.1 impeccable-original: Skill-Only Architecture

impeccable-original does NOT use a separate agent system. Skills ARE the agents — each skill contains all the persona, methodology, and domain knowledge needed. The `critique` skill embeds persona-based testing directly:

```markdown
### Persona Red Flags
> *Consult [personas](reference/personas.md)*
Auto-select 2-3 personas most relevant to this interface type
```

The reference files within skills serve as **embedded knowledge bases** that the skill can consult during execution.

### 3.2 paper2pr: Skill-to-Agent Delegation

paper2pr explicitly delegates from skills to specialized agents. Skills are **orchestrators** that invoke named agents:

```markdown
### 2. Run Review Agents in Parallel
**Agent 1: Visual Audit** (slide-auditor)
**Agent 2: Pedagogical Review** (pedagogy-reviewer)
**Agent 3: Proofreading** (proofreader)
```

The agent definitions live in `.claude/agents/` and define specialized personas (slide-auditor, pedagogy-reviewer, quarto-critic, quarto-fixer, etc.). Skills coordinate agents; agents do the actual work.

**Notable feature:** The `allowed-tools` frontmatter restricts skills to only the tools they need:
- Read-only skills: `["Read", "Grep", "Glob", "Write", "Task"]` (Write is for reports only)
- Fix skills: `["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Task"]`
- Infrastructure skills: `["Bash", "Read", "Glob"]`

### 3.3 impeccable-quarto: Agent Definitions + Skill Orchestration

Our project has both agent definitions (`.claude/agents/`) and skills (`.claude/skills/`). The `/review-slides` skill delegates to our agents:

```markdown
- Invoke `slide-critic` agent for adversarial UX/design review
- Invoke `layout-auditor` agent for spatial analysis
- Invoke `typography-reviewer` agent for font/type assessment
- Invoke `verifier` agent for compilation and rendering check
```

**Comparison:**
| Feature | impeccable-original | paper2pr | impeccable-quarto |
|---------|-------------------|----------|-------------------|
| Agent definitions | None (skills are self-contained) | `.claude/agents/` | `.claude/agents/` |
| Skill-agent delegation | N/A | Explicit (`slide-auditor`, `pedagogy-reviewer`) | Explicit (`slide-critic`, `layout-auditor`) |
| Tool restrictions | None | `allowed-tools` in frontmatter | None |
| Agent isolation | None | `context: fork` | None |
| Adversarial separation | N/A | Critic ≠ Fixer enforced by design | Critic ≠ Fixer enforced by protocol |

---

## 4. Prompt Engineering Patterns: What Makes Them Effective

### 4.1 The "Never" List Pattern

All three repos use explicit "NEVER" lists, but impeccable-original elevates this to an art form:

```markdown
**NEVER**:
- Use bounce or elastic easing curves—they feel dated
- Animate layout properties (width, height, top, left)
- Use durations over 500ms for feedback—it feels laggy
- Animate without purpose—every animation needs a reason
- Ignore `prefers-reduced-motion`—this is an accessibility violation
```

Each "NEVER" includes the **reason why**, not just the prohibition. This is critical because it allows the LLM to generalize to novel situations.

**paper2pr** uses hard gates:
```markdown
## Hard Gates (Non-Negotiable)
| Gate | Condition |
|------|-----------|
| **Overflow** | NO content cut off |
| **Plot Quality** | Interactive charts >= static plots |
```

**impeccable-quarto** uses the `[ANTI-PATTERNS TO AVOID]` section consistently:
```markdown
[ANTI-PATTERNS TO AVOID]
- Do NOT modify any files — this is a read-only diagnostic skill
- Do NOT skip the compilation check even if it seems slow
```

**Recommendation:** Our "NEVER" lists are good but could benefit from adding the *reason why* for each prohibition, following impeccable-original's pattern.

### 4.2 The "Role Casting" Pattern

impeccable-original consistently ends skills with a persona assignment:

```markdown
Remember: You're a technical quality auditor. Document systematically,
prioritize ruthlessly, cite specific code locations, and provide clear
paths to improvement.
```

```markdown
Remember: You have impeccable attention to detail and exquisite taste.
Polish until it feels effortless, looks intentional, and works flawlessly.
```

This "role casting" at the end reinforces the agent's persona for the task.

paper2pr uses this sparingly but effectively:
```markdown
**Philosophy:** "We arrive at the best possible presentation through
active dialogue."
```

impeccable-quarto does NOT use this pattern — our skills end with `[QUALITY CHECKS]` which is functional but lacks the motivational role-casting.

### 4.3 The "Output Template" Pattern

impeccable-quarto excels here with explicit markdown output templates in every diagnostic skill:

```markdown
[OUTPUT FORMAT]
```
## Audit Report: <filename>
**Score: XX/100** — <Draft|Presentable|Excellent>

### Critical Issues (must fix)
- [ ] Issue description — Slide N — Deduction: -XX
```
```

paper2pr also uses this pattern:
```markdown
## Quality Score Rubric
| Score | Critical | Medium | Meaning |
|-------|----------|--------|---------|
| Excellent | 0-2 | 0-5 | Ready to present |
```

impeccable-original uses it in `audit` and `critique` but leaves more room for LLM interpretation in fix skills.

**Assessment:** impeccable-quarto's consistent output templates are a strength — they make skill output predictable and parseable.

### 4.4 The "Forced Dependency" Pattern

impeccable-original's most powerful pattern is the forced dependency chain:

```markdown
## MANDATORY PREPARATION
Invoke {{command_prefix}}frontend-design — it contains design principles,
anti-patterns, and the **Context Gathering Protocol**.
```

This ensures every skill execution starts with the same shared context, creating consistency across 20+ commands. The pattern has three levels:
1. `teach-impeccable` → gathers project context → persists to `.impeccable.md`
2. `frontend-design` → provides design system knowledge → loaded by every skill
3. Reference files → deep domain knowledge → loaded by specific skills

paper2pr achieves similar consistency through `AGENTS.md` (which Claude Code loads automatically) and `.claude/rules/`.

impeccable-quarto uses `[MANDATORY PREPARATION]` sections that independently load the same rules files, but without a hub skill that ensures shared context.

### 4.5 The "Ask-Then-Act" Pattern

impeccable-original's `critique` skill has a sophisticated interaction pattern:

```markdown
## Phase 3: Ask the User
**After presenting findings**, use targeted questions...
Ask questions along these lines (adapt to specific findings):
1. **Priority direction**: "Which area should we tackle first?"
2. **Design intent**: "Is that clinical tone intentional?"
3. **Scope**: "All issues, or focus on top 3?"

## Phase 4: Recommended Actions
**After receiving the user's answers**, present a prioritized action summary
```

This creates a **diagnostic → dialogue → action** loop where the user guides the fix strategy. paper2pr's `interview-me` skill is entirely built around this pattern.

impeccable-quarto's diagnostic skills (audit, critique, review) skip the dialogue step and go straight to recommendations. This is faster but less collaborative.

### 4.6 The "Graduated Intensity" Pattern

impeccable-original provides opposing intensity commands:
- `/bolder` — amplifies safe designs
- `/quieter` — tones down aggressive designs

These create a **design intensity dial** that the user can adjust in either direction. The existence of both commands signals that quality exists on a spectrum, not a binary.

paper2pr has a similar pattern with:
- `/pedagogy-review` — checks teaching effectiveness
- `/devils-advocate` — challenges design assumptions

impeccable-quarto has `/bolder-slides` and `/quieter-slides` but they could be enhanced with impeccable-original's depth.

---

## 5. Missing Skills: What impeccable-quarto Needs

### 5.1 Skills to Adopt from impeccable-original

| Skill | What It Does | Why We Need It | Adaptation |
|-------|-------------|----------------|------------|
| **`frontend-design` (hub)** | Shared design context loaded by all skills | Our skills independently load rules; a hub would ensure consistency | Create a `/slide-design` hub skill that loads all rules and the impeccable-quarto theme context |
| **`teach-impeccable`** → **`/teach-style`** | Already have this | ✅ Already adapted | Minor: add persona-gathering like impeccable-original |
| **`extract`** | Extract reusable components into design system | We could extract reusable slide patterns (e.g., comparison layouts, data slides) into templates | `/extract-patterns` — identify reusable slide structures and codify as templates |
| **`delight`** | Add moments of joy | Presentations benefit from "delight moments" — audience engagement devices | `/engage-audience` — add interactive elements, strategic humor, audience participation hooks |
| **`harden`** | Edge case resilience | We need to handle: very long titles, code that overflows, math that exceeds bounds | Already partially covered by `/normalize-slides`, could be enhanced |
| **`onboard`** | First-run experience | A `/new-user-guide` could help first-time impeccable-quarto users | Lower priority — CLAUDE.md serves this role |

### 5.2 Skills to Adopt from paper2pr

| Skill | What It Does | Why We Need It | Adaptation |
|-------|-------------|----------------|------------|
| **`deploy`** | Render + deploy | We have build scripts but no deployment skill | `/deploy-deck` — render and deploy to GitHub Pages or similar |
| **`write-speaker-notes`** | Generate presentation scripts | Our `/create-deck` adds notes, but a dedicated notes-generation skill would be valuable for existing decks | `/write-notes` — generate or regenerate speaker notes for an existing deck |
| **`proofread`** | Grammar, typos, consistency | We have no proofreading-specific skill | `/proofread-slides` — check grammar, spelling, consistency, academic quality |
| **`deep-audit`** | Repository-wide consistency check | Useful for checking that all themes, rules, and skills are internally consistent | `/deep-audit` — verify impeccable-quarto infrastructure consistency |
| **`devils-advocate`** | Challenge assumptions | Valuable for presentations — challenge claims, evidence, logical flow | `/challenge-deck` — 5-7 tough audience questions, logical gaps, claims without evidence |
| **`context-status`** | Session health check | Useful for long review sessions | Lower priority — operational tool |
| **`learn`** | Extract discoveries into skills | Meta-skill for growing the skill library | `/learn-pattern` — codify a new slide pattern or design rule discovered during use |
| **`commit`** | Stage, commit, PR, merge | Standardize git workflow | Lower priority — can use Claude Code's built-in commit |

### 5.3 Net-New Skills Suggested

| Skill | What It Does | Rationale |
|-------|-------------|-----------|
| **`/compare-themes`** | Side-by-side theme comparison | The project supports theme variants; a skill to compare would aid theme selection |
| **`/accessibility-audit`** | Deep WCAG compliance check | Goes beyond basic alt-text and contrast checking in `/audit-slides` |
| **`/export-deck`** | Export to PDF, PPTX, or self-contained HTML | Common need not covered by current skills |
| **`/timing-check`** | Validate slide count vs. talk duration | Source translation rules mention ~1 slide/minute but no skill enforces this |

### Priority Ranking

1. **`/write-notes`** — High value, moderate effort. Many decks need notes retrofitted.
2. **`/proofread-slides`** — High value, low effort. Grammar/consistency checking is clearly missing.
3. **`/challenge-deck`** — High value, moderate effort. Adversarial content review is a gap.
4. **`/deploy-deck`** — Medium value, low effort. Standardize the render-deploy workflow.
5. **`/deep-audit`** — Medium value, high effort. Needed as the project grows.
6. **`/extract-patterns`** — Medium value, medium effort. Builds template library over time.

---

## 6. Anti-Pattern Detection: How Each Repo Codifies "Don't"

### 6.1 impeccable-original: The "AI Slop" Framework

impeccable-original's most innovative anti-pattern system is its **AI Slop Detection** framework, woven into nearly every skill:

```markdown
### 1. AI Slop Detection (CRITICAL)
**This is the most important check.** Does this look like every other
AI-generated interface from 2024-2025?

Review the design against ALL the **DON'T** guidelines in the
frontend-design skill — they are the fingerprints of AI-generated work.
```

The anti-patterns are categorized as **"tells" of AI-generated work**:
- Cyan-on-dark color palette
- Purple-to-blue gradients
- Glassmorphism everywhere
- Hero metric layouts
- Identical card grids
- Generic fonts (Inter, Roboto)
- Gradient text on headings
- Bounce/elastic easing

This is extraordinarily effective because it names specific, recognizable patterns and provides an overarching principle: **"If you showed this to someone and said 'AI made this,' would they believe you immediately?"**

### 6.2 paper2pr: The "Hard Gate" Framework

paper2pr uses **non-negotiable hard gates** rather than a point deduction system:

```markdown
## Hard Gates (Non-Negotiable)
| Gate | Condition |
|------|-----------|
| **Overflow** | NO content cut off |
| **Plot Quality** | Interactive charts >= static plots |
| **Content Parity** | No missing slides/equations/text |
| **Notation Fidelity** | All math verbatim from Beamer |
```

These are binary pass/fail — no partial credit. This is appropriate for their domain (academic lectures where a missing equation is unacceptable).

paper2pr also codifies anti-patterns through **constraints per skill**:
```markdown
## CONSTRAINTS (Non-Negotiable)
1. Every new symbol MUST be checked against the notation registry
2. Motivation before formalism — no exceptions
3. Worked example within 2 slides of every definition
4. Max 2 colored boxes per slide
```

### 6.3 impeccable-quarto: The Deduction Table Framework

Our project uses a **point deduction system** codified in `quality-gates.md`:

```markdown
| ID | Issue | Deduction | Auto-fail? |
|---|---|---|---|
| CRIT-01 | Compilation failure | -100 | Yes |
| MAJ-01 | Missing speaker notes | -5 per slide |
| MIN-01 | Inconsistent separators | -2 |
```

The deduction table is referenced from `anti-patterns.md` which provides detection criteria and recommended fixes.

**What we do well:**
- Quantitative scoring enables objective measurement
- ID-based issues enable tracking and cross-referencing
- Three severity tiers (Critical/Major/Minor) with clear deduction amounts

**What we could improve:**
- No equivalent to impeccable-original's "AI Slop Test" — we should add a "Generic Slide Deck Test" that checks for AI-generated presentation anti-patterns (default themes, bullet-point walls, no visual variety, stock photo overuse)
- Our anti-patterns are slide-specific; we lack deck-level anti-patterns (monotonous pacing, no narrative arc, inconsistent depth across sections)

---

## 7. Actionable Recommendations

### 7.1 Structural Improvements

1. **Add reference subdirectories to key skills.** The `/critique-slides` skill would benefit from reference files for:
   - Cognitive load assessment for presentations (adapted from impeccable-original)
   - Audience persona definitions (conference attendee, lecturer, student, executive)
   - Presentation scoring rubric (detailed version of quality-gates.md)

2. **Create a hub skill (`/slide-design`).** This should be invoked by every design-related skill and should:
   - Load `.impeccable-quarto.md` if it exists
   - Load the theme reference
   - Provide the shared design vocabulary
   - Include the "Generic Slide Deck Test" (our equivalent of AI Slop Detection)

3. **Add `allowed-tools` to skill frontmatter.** Diagnostic skills should be restricted to read-only tools. Fix skills should be allowed to edit. This prevents accidental file modification during audits.

4. **Add role-casting closers to skills.** End each skill with a persona reinforcement:
   - Audit: "You are a rigorous technical auditor..."
   - Critique: "You are an experienced presentation coach..."
   - Polish: "You have an impeccable eye for detail..."

### 7.2 Prompt Engineering Improvements

5. **Add "why" to every "NEVER" item.** Transform:
   ```markdown
   - Do NOT use font sizes below 20px
   ```
   Into:
   ```markdown
   - Do NOT use font sizes below 20px — text below this size is unreadable
     at projection distance; the back row of a 200-seat auditorium sees nothing
   ```

6. **Add explicit command recommendations to diagnostic skills.** Both `/audit-slides` and `/critique-slides` should end with:
   ```markdown
   ## Recommended Actions
   Based on findings, run these skills in order:
   1. `/normalize-slides` — Fix [specific issues found]
   2. `/typeset-slides` — Fix [specific typography issues]
   3. `/polish-slides` — Final pass
   ```

7. **Add an "Ask-Then-Act" phase to `/critique-slides`.** After presenting findings, ask 2-3 targeted questions before recommending actions:
   - "I found issues with X, Y, Z. Which area should we tackle first?"
   - "Your deck has [N] slides for a [M]-minute talk. Should we add/remove slides, or adjust pacing?"

### 7.3 Missing Skills (Priority Order)

8. **`/write-notes`** — Generate or update speaker notes for existing decks. Adapt paper2pr's `write-speaker-notes` workflow (Phase 0-5 with batch generation, count verification, timing report).

9. **`/proofread-slides`** — Grammar, typos, terminology consistency, academic quality. Read-only skill producing a report. Adapt paper2pr's `proofread` skill.

10. **`/challenge-deck`** — Devil's advocate for presentations. Generate 5-7 tough questions an audience member might ask. Check for: unsupported claims, logical gaps, missing caveats, assumed knowledge, controversial statements without evidence. Adapt paper2pr's `devils-advocate`.

11. **`/deploy-deck`** — Standardize the render-deploy workflow. Render, verify, optionally deploy to GitHub Pages.

### 7.4 Anti-Pattern Enhancements

12. **Add a "Generic Slide Deck Test"** (equivalent to AI Slop Detection). Create a checklist of presentation anti-patterns that signal "AI made this without design thought":
    - Default RevealJS theme with no customization
    - Every slide is a bullet list (no visual variety)
    - Inconsistent depth (some slides have 3 words, others have 200)
    - No section breaks or transition slides
    - Stock photo on every other slide
    - All slides follow the same heading + bullets template
    - No speaker notes anywhere
    - Generic title like "Presentation Title"

13. **Add deck-level anti-patterns** to `anti-patterns.md`:
    - **Monotonous Pacing** — Every slide has the same structure and density
    - **Missing Arc** — No clear beginning-middle-end structure
    - **Depth Inconsistency** — Some sections get 10 slides, others get 1
    - **Orphan Section** — A section with only 1 slide
    - **Missing Context** — Technical content without motivation
    - **Data Without Story** — Charts/tables without interpretation

---

## 8. Summary: Lessons by Category

### From impeccable-original (20 commands)
- **Hub skill pattern** — shared context loading creates consistency
- **Reference subdirectories** — deep domain knowledge attached to skills
- **AI Slop Detection** — name the anti-patterns explicitly
- **Intensity dial** — opposing skills (bolder/quieter) for nuanced control
- **Role casting** — end each skill with a persona reinforcement
- **Ask-Then-Act** — dialogue before action in diagnostic skills
- **Command recommendation** — diagnostic skills suggest which fix skills to run
- **Build system with placeholders** — enables multi-provider deployment

### From paper2pr (24 skills)
- **Phased workflows** — numbered phases with explicit gate conditions
- **Tool restrictions** — `allowed-tools` prevents accidental file modification
- **Agent isolation** — `context: fork` for true adversarial separation
- **Hard gates** — binary pass/fail for non-negotiable quality criteria
- **Report persistence** — save every agent's output to `quality_reports/`
- **Conditional execution** — agents that only run when relevant (TikZ check)
- **Max loop limits** — every iterative process has explicit termination
- **Meta-skills** — `/learn` for growing the skill library, `/context-status` for session health
- **Speaker notes as first-class** — dedicated workflow with word/character budget compliance

### Our strengths to preserve
- **Quantitative scoring** — point deduction system is more precise than pass/fail
- **Consistent skill structure** — `[MANDATORY PREPARATION]` / `[IMPLEMENTATION STEPS]` / `[OUTPUT FORMAT]` / `[ANTI-PATTERNS]` / `[QUALITY CHECKS]` is clean and predictable
- **Design-system-first approach** — OKLCH, tinted neutrals, typography-first philosophy
- **Adversarial review protocol** — critic/fixer separation with score tracking
- **Comprehensive theme reference** — impeccable.scss as a curated design system
