# Workflow Analysis: Multi-Agent Orchestration Patterns

## Reference Systems Analyzed

| System | Focus | Agent Count | Key Innovation |
|--------|-------|-------------|----------------|
| **paper2pr** | Academic slide production (Beamer → Quarto) | 11 specialist agents | Adversarial QA loops, session persistence, hook-based automation |
| **impeccable-original** | Frontend design vocabulary (multi-provider) | 21 skills (no agents) | Single-source multi-harness build, severity-driven action chains |
| **impeccable-quarto** (ours) | Quarto RevealJS slide quality system | 8 agent types | Phased review pipeline, quality gates, semantic design system |

---

## 1. Agent Specialization Comparison

### paper2pr: 11 Specialist Agents

| Agent | Role | Domain |
|-------|------|--------|
| beamer-translator | Beamer LaTeX → Quarto conversion | Translation |
| proofreader | Grammar, typos, overflow, consistency | Content QA |
| script-writer | Speaker notes/scripts (EN/KR) | Content creation |
| domain-reviewer | ML referee review (5 lenses) | Domain expertise |
| verifier | Compilation/rendering (LaTeX + Quarto + R + SVG) | Technical QA |
| slide-auditor | Visual layout (overflow, fonts, spacing) | Design QA |
| r-reviewer | R code quality (10 categories) | Code QA |
| quarto-critic | Adversarial QA: Quarto vs Beamer parity | Adversarial review |
| quarto-fixer | Implements critic fixes in priority order | Fix implementation |
| tikz-reviewer | TikZ diagram visual quality | Specialist review |
| pedagogy-reviewer | 13 pedagogical patterns validation | Learning design |

### Our System: 8 Agent Types

| Agent | Role | Domain |
|-------|------|--------|
| content-translator | Source material → slides | Translation |
| layout-auditor | Spatial design (overflow, alignment, whitespace) | Design QA |
| slide-critic | Adversarial quality reviewer + scoring | Adversarial review |
| slide-fixer | Applies critic fixes (Critical → Major → Minor) | Fix implementation |
| theme-designer | SCSS theme creation (OKLCH, RevealJS) | Creative |
| typography-reviewer | Font pairing, hierarchy, sizes, weights | Design QA |
| verifier | Compilation/rendering check | Technical QA |
| pedagogy-reviewer | Narrative arc, pacing, cognitive load | Learning design |

### Gap Analysis: Agents We're Missing

| Missing Role | paper2pr Equivalent | Impact | Recommendation |
|---|---|---|---|
| **Proofreader** | `proofreader` | No dedicated grammar/typo/consistency checker | **Add** — separate from slide-critic; catches academic writing quality issues the critic doesn't look for |
| **Domain Reviewer** | `domain-reviewer` | No technical accuracy verification | **Consider** — valuable for technical presentations; could be parameterized by domain (ML, stats, engineering) |
| **Script Writer** | `script-writer` | No dedicated speaker notes generator | **Add** — our rules mandate speaker notes on every slide but we have no agent that specializes in writing them |
| **Code Reviewer** | `r-reviewer` | No code block quality review | **Defer** — relevant only if presentations contain significant code |
| **Diagram Reviewer** | `tikz-reviewer` | No visual review of diagrams/figures | **Defer** — less critical for our SVG-first approach |

**Priority additions:**
1. **Proofreader agent** — Read-only, reports to `quality_reports/`, checks grammar, consistency, academic quality, terminology
2. **Script-writer agent** — Creates verbatim speaker notes with transition cues, timing, and bridge-forward structure
3. **Domain-reviewer agent** — Parameterizable by field; validates claims, methodology, accuracy

---

## 2. Adversarial QA Loop Comparison

### paper2pr's Implementation

```
quarto-critic (HOSTILE)
  ├── 7 hard gates (non-negotiable): overflow, plot quality, content parity,
  │   visual regression, slide centering, notation fidelity, equation formatting
  ├── Verdict: APPROVED | NEEDS REVISION | REJECTED
  ├── Zero tolerance for notation differences
  └── Content parity matrix (Beamer vs Quarto, character-by-character for equations)
        ↓
quarto-fixer
  ├── Priority order: Critical → Major → Minor
  ├── Does NOT make independent decisions
  ├── Follows critic instructions exactly
  └── Re-renders after fixes, verifies in docs/ deployment location
        ↓
verifier → re-render → quarto-critic (fresh round)
```

**Key design decisions in paper2pr:**
- **Hard gates are absolute** — a single hard gate failure = REJECTED, regardless of other quality
- **Fixer has no agency** — it executes the critic's instructions, never improvises
- **Fresh evaluation** — each critic round evaluates independently (no memory of prior rounds)
- **Content parity as first-class concern** — the critic explicitly tracks Beamer↔Quarto equivalence

### Our Implementation

```
slide-critic (adversarial, read-only)
  ├── Systematic review (overflow, typography, color, layout, content, anti-patterns, a11y)
  ├── Score calculation (100 - deductions)
  └── Report with categorized issues
        ↓
slide-fixer
  ├── Priority order: Critical → Major → Minor
  ├── Preserves author's intent
  ├── Never deletes content (moves to speaker notes)
  └── Verifies compilation after fixes
        ↓
verifier → slide-critic (re-evaluation)
```

**Loop termination conditions (both systems):**
| Condition | paper2pr | Ours |
|---|---|---|
| Score meets target | ≥ threshold | ≥ 90/100 default |
| Max rounds | 5 | 5 |
| Score regression | Revert to best | Revert to best |
| Score stalled | Not explicit | 2 unchanged rounds |

### Recommendations for Our System

1. **Add hard gates** — Define 3-5 non-negotiable gates that cause immediate REJECTED verdict regardless of score. Candidates:
   - Compilation failure (already CRIT-01, -100)
   - Content overflow on any slide
   - Missing YAML frontmatter
   - Broken image references

2. **Strengthen fixer constraints** — Our fixer is well-designed but could benefit from paper2pr's "no independent decisions" rule being more explicit. The fixer should implement the critic's exact recommendations, not reinterpret them.

3. **Add "fresh evaluation" rule** — Explicitly state that each critic round should not see prior critic reports. This prevents confirmation bias (looking for things you found before).

4. **Track score progression** — paper2pr logs round-by-round scores to `quality_reports/`. We should do the same to detect stalls and regressions objectively.

---

## 3. Quality Gates Comparison

### Threshold Comparison

| Gate | paper2pr | Ours |
|---|---|---|
| Commit threshold | 80/100 | Not defined (should be) |
| PR/deploy threshold | 90/100 | 90/100 (default target) |
| Aspirational | 95/100 | 95-100 ("Impeccable") |

### Scoring Granularity

**paper2pr** uses fewer, domain-specific deductions:
- Critical: compilation failure (-100), equation overflow (-20), broken citation (-15), equation typo (-10)
- Major: text overflow (-5), TikZ label overlap (-5), notation inconsistency (-3)
- Minor: font size reduction (-1/slide), long lines (-1)

**Our system** has more comprehensive, general-purpose deductions (5 critical, 9 major, 7 minor) with wider coverage but less domain specificity.

### Key Difference: Enforcement

paper2pr enforces quality gates with **concrete actions**:
- Score < 80: **Block commit** — list blocking issues
- Score < 90: **Allow commit, warn** with recommendations
- User can override with justification

Our system defines thresholds but lacks enforcement mechanisms.

### Recommendations

1. **Add commit-blocking** — Define a hook or protocol step that prevents committing presentations scoring below 80
2. **Add override mechanism** — Allow explicit user override with documented justification (paper2pr pattern)
3. **Add domain-specific deductions** — When creating domain-specific decks (ML, engineering), add deductions for domain anti-patterns (e.g., missing ablation, unsupported claims)
4. **Score reporting format** — Standardize score output to `quality_reports/[deck]_score_roundN.md`

---

## 4. Session Management Comparison

### paper2pr: Comprehensive Session Persistence

paper2pr has a **7-hook system** that automates session management:

| Hook | Type | Purpose |
|---|---|---|
| `notify.sh` | Notification | Desktop notifications for permission prompts |
| `protect-files.sh` | PreToolUse | Block edits to protected files (bib, settings) |
| `pre-compact.py` | PreCompact | Capture state before context compaction |
| `post-compact-restore.py` | SessionStart | Restore context after compaction |
| `context-monitor.py` | PostToolUse | Progressive warnings at 40/55/65/80/90% context |
| `verify-reminder.py` | PostToolUse | Remind to compile after editing .tex/.qmd |
| `log-reminder.py` | Stop | Block stop if 15+ responses without session log update |

**Session Logging Protocol:**
- **Post-plan log**: Goal, approach, rationale, key context
- **Incremental logs**: 1-3 lines on design decisions, solved problems, corrections
- **End-of-session log**: Summary, scores, open questions, blockers
- **Location**: `quality_reports/session_logs/YYYY-MM-DD_description.md`

**Context Survival:**
- Pre-compact hook saves: active plan path/status, current task, recent decisions → JSON file
- Post-compact hook restores: reads JSON, prints recovery message with plan status and next task
- Result: Claude survives context compression without losing its place

### Our System: Minimal Session Management

Our orchestrator-protocol.md mentions session management but lacks implementation:
- "Multi-round sessions should track score progression, issues found/fixed, time per phase"
- "If a session is interrupted, the .qmd file state is authoritative"
- No hooks defined for session persistence
- No compaction survival mechanism

### Recommendations

1. **Add pre/post-compact hooks** (HIGH PRIORITY) — Context compaction destroys working state. paper2pr's pattern of saving to JSON and restoring is elegant and essential for long review sessions.

2. **Add context monitor hook** — Progressive warnings help the orchestrator pace its work. Particularly useful during multi-round QA loops that consume significant context.

3. **Add verify-reminder hook** — Non-blocking reminder to compile after editing .qmd files. Prevents forgetting the mandatory verification step.

4. **Add session logging protocol** — Define location (`quality_reports/session_logs/`), format, and timing for session logs. The 3-trigger model (post-plan, incremental, end-of-session) is well-structured.

5. **Add log-reminder hook** — Gentle enforcement of session logging discipline, especially for multi-round review work.

6. **Implement file protection hook** — Protect critical files (impeccable.scss master theme, settings.json) from accidental modification.

### Hook Implementation Priority

| Hook | Priority | Effort | Impact |
|---|---|---|---|
| pre/post-compact | P0 | Medium | Critical for long sessions |
| context-monitor | P1 | Low | Prevents context blowout |
| verify-reminder | P1 | Low | Catches compilation skips |
| file-protection | P2 | Low | Safety net |
| log-reminder | P2 | Low | Session discipline |
| notification | P3 | Low | Nice-to-have |

---

## 5. Orchestrator Pattern Comparison

### paper2pr Orchestrator

```
Plan (approved) → Implement → Verify → Review → Fix → Re-verify → Score
                                         ↑                          |
                                         └──── loop if score < target ←─┘
```

**Key features:**
- **"Just do it" mode**: Skip approval pause, auto-commit if score ≥ 80 — useful for routine tasks
- **Max rounds clearly enforced**: Main loop 5 rounds, critic-fixer sub-loop 5 rounds, verification retries 2 attempts
- **Review agents are file-type-aware**: Different agents activate based on file extension (.tex, .qmd, .R, .svg)

### Our Orchestrator

```
Phase 1 (Diagnostic): slide-critic + layout-auditor [parallel]
Phase 2 (Specialist): typography-reviewer + verifier [parallel]
Phase 3 (QA Loop): merge findings → fixer → verifier → critic [iterative]
Phase 4 (Final): verifier [single pass]
```

**Key features:**
- **Phase gates**: All agents in a phase must complete before next phase
- **Parallel execution within phases**: Maximizes throughput
- **Early termination**: Score ≥ 95 in Phase 1 → skip to Phase 4
- **Stall detection**: 2 unchanged rounds → STALLED

### Comparison

| Feature | paper2pr | Ours | Assessment |
|---|---|---|---|
| Phase structure | Linear with loop | 4-phase with gates | Ours is more structured |
| Parallelism | Within review step | Within phases | Similar approach |
| Early termination | Not explicit | Score ≥ 95 → skip | We have this, they don't |
| "Just do it" mode | Yes (skip approval, auto-commit) | No | Should add |
| File-type routing | Yes (agents per extension) | No | Should add |
| Stall detection | Not explicit | 2 unchanged rounds | We have this, they don't |
| Regression handling | Revert to best version | Revert to best version | Equivalent |
| Round limits | 5 main + 5 sub + 2 verify | 5 rounds + 2 unchanged | Both reasonable |

### Recommendations

1. **Add "just do it" mode** — For routine tasks (single slide fix, minor update), allow skipping the plan-and-approve step. Auto-commit if score ≥ 80 after fix. Reduces friction for small changes.

2. **Add file-type routing** — Different file types should activate different agent combinations. For .scss files, skip content agents and focus on theme-designer + verifier. For .qmd files, run the full pipeline.

3. **Add task complexity classifier** — paper2pr classifies tasks as simple/standard/complex upfront. Our protocol mentions this but could formalize the decision criteria:
   - Simple: Single skill, <5 slides affected → no plan needed
   - Standard: Single skill, full deck → mental plan
   - Complex: Multi-agent, full review → formal plan document

---

## 6. Plan-First Workflow

### paper2pr's Approach

1. **Enter Plan Mode** (Claude Code feature)
2. Check MEMORY.md for relevant learnings
3. **Requirements specification** (if complex/ambiguous):
   - AskUserQuestion (max 3-5 questions)
   - Create spec with MUST/SHOULD/MAY framework
   - Declare clarity status: CLEAR / ASSUMED / BLOCKED
   - Get user approval
4. Draft plan (what changes, which files, in what order)
5. **Save plan to disk**: `quality_reports/plans/YYYY-MM-DD_short-description.md`
6. Present to user; wait for approval
7. Exit plan mode
8. Save initial session log
9. Implement via orchestrator protocol

**Key innovation:** Plans are persisted to disk, surviving context compaction. The pre-compact hook captures active plan path/status so post-compact can restore it.

### Our Approach

Our orchestrator-protocol.md states:
- "Plan first for non-trivial work" (>5 slides or multi-agent involvement)
- Simple tasks: no plan needed
- Standard tasks: "mental plan" (not persisted)
- Complex tasks: "formal plan with phases"

But we lack:
- Plan persistence to disk
- MUST/SHOULD/MAY framework for requirements
- Clarity status declarations
- Plan recovery after compaction

### Recommendations

1. **Persist plans to disk** — Save to `quality_reports/plans/YYYY-MM-DD_description.md`. Essential for long sessions and compaction survival.

2. **Adopt MUST/SHOULD/MAY framework** — Clarifies scope boundaries and prevents scope creep during execution.

3. **Add clarity status** — CLEAR/ASSUMED/BLOCKED tags on each requirement help the orchestrator know where it can proceed autonomously vs. where it needs user input.

4. **Integrate with compact hooks** — When implemented, the pre-compact hook should capture active plan path so post-compact can restore it.

---

## 7. Meta-Governance: Dual-Nature Pattern

### paper2pr's Approach

paper2pr operates as both a **working project** (specific academic slides) and a **public template** (patterns for others to fork).

**Two-tier memory system:**
- `MEMORY.md` (root, committed, ~200 lines) — Generic learnings for ALL users
  - Format: `[LEARN:category] wrong → right`
  - Decision test: "Would a biology PhD forking this repo benefit?"
- `.claude/state/personal-memory.md` (gitignored, local) — Machine-specific learnings
  - Example: XeLaTeX TEXINPATHS setup, tool version quirks, local paths

**Dogfooding rule:** The project follows its own patterns — plan-first, spec-then-plan, quality gates, doc standards.

### Our Position

impeccable-quarto is also dual-natured:
- **Working project**: Curated themes, scoring, review pipeline
- **Template**: Design quality system others can adopt

We already have `source/` as canonical and `.claude/` as derived, which is a form of separation.

### Recommendations

1. **Formalize the dual-nature** — Add a meta-governance rule that distinguishes template patterns from project-specific configuration
2. **Adopt the memory decision test** — "Would someone forking impeccable-quarto for their own presentations benefit from this learning?"
3. **Dogfooding** — Our review pipeline should be used on our own example presentations in `examples/`

---

## 8. Hook System Analysis

### paper2pr: 7 Hooks (Python + Bash)

| Hook | Language | Event | Blocking? |
|---|---|---|---|
| notify.sh | Bash | Notification | No |
| protect-files.sh | Bash | PreToolUse (Edit/Write) | Yes (blocks edit) |
| pre-compact.py | Python | PreCompact | No (captures state) |
| post-compact-restore.py | Python | SessionStart | No (restores state) |
| context-monitor.py | Python | PostToolUse (Bash/Task) | No (progressive warnings) |
| verify-reminder.py | Python | PostToolUse (Write/Edit) | No (reminder only) |
| log-reminder.py | Python | Stop | Yes (blocks stop if no log) |

**Design principles:**
- **Throttling**: context-monitor and verify-reminder throttle to 60-second intervals to avoid noise
- **State files**: Hooks use JSON state files in `~/.claude/sessions/[project_hash]/` for persistence
- **Cross-platform**: notify.sh detects macOS vs Linux for notification commands
- **Non-invasive**: Most hooks are advisory, not blocking. Only protect-files and log-reminder can block.

### Our System: No Hooks

Our `.claude/settings.json` defines permissions but no hooks.

### Recommended Hook Implementation Plan

**Phase 1 (Essential):**
```json
{
  "hooks": {
    "PreCompact": [{
      "type": "command",
      "command": "python .claude/hooks/pre-compact.py"
    }],
    "SessionStart": [{
      "type": "command",
      "command": "python .claude/hooks/post-compact-restore.py",
      "matcher": "compact|resume"
    }]
  }
}
```

**Phase 2 (Productivity):**
- `verify-reminder.py` — PostToolUse on Write/Edit for .qmd files
- `context-monitor.py` — PostToolUse on Bash/Task with progressive warnings

**Phase 3 (Safety):**
- `protect-files.py` — PreToolUse on Edit/Write for themes/impeccable.scss, .claude/settings.json
- `log-reminder.py` — Stop hook for multi-round review sessions

---

## 9. impeccable-original Patterns Worth Adopting

While impeccable-original uses a fundamentally different architecture (skills, not agents), several patterns are relevant:

### 9.1 Severity-Driven Action Chains

impeccable-original's critique/audit commands suggest next actions based on severity:
- P0 (Blocking) → immediate fix required
- P1 (Major) → fix before shipping
- P2 (Minor) → fix in next iteration
- P3 (Polish) → nice-to-have

**Recommendation:** Our critic reports should include "Recommended Next Actions" ordered by severity, with specific skill/agent to invoke.

### 9.2 Cognitive Load as First-Class Concern

impeccable-original has a dedicated cognitive load framework:
- 3 types: Intrinsic, Extraneous, Germane
- 8-item checklist (single focus, chunking ≤4, visual grouping, clear hierarchy, one-at-a-time, minimal choices ≤4, working memory, progressive disclosure)
- 8 common violations (Wall of Options, Memory Bridge, Hidden Navigation, etc.)

**Recommendation:** Add cognitive load assessment to our pedagogy-reviewer. Currently it checks "1 key idea per slide" but lacks the formal framework.

### 9.3 Anti-Slop Detection

impeccable-original's explicit "AI Slop Test" — "If someone sees this and says 'AI made this,' that's the problem" — with catalogued tells:
- Gradient text on dark backgrounds
- Purple-to-blue gradients everywhere
- Dark mode with neon glows
- Card nesting (cards within cards within cards)
- Generic fonts (Inter, system-ui)

**Recommendation:** Add an "AI slop" anti-pattern category to our anti-patterns.md. Slides generated by LLMs have their own tells (excessive gradients, over-decorated boxes, symmetric layouts, stock metaphor images).

### 9.4 Context Persistence via Project File

impeccable-original persists design context to `.impeccable.md` in the project root, which all skills check before proceeding.

**Recommendation:** We already support `.impeccable-quarto.md` for project-level customization. Ensure all agents actually check for and load this file.

---

## 10. Consolidated Recommendations

### Critical (Implement First)

| # | Recommendation | Source Pattern | Impact |
|---|---|---|---|
| C1 | Add pre/post-compact hooks for session persistence | paper2pr hooks | Prevents state loss in long review sessions |
| C2 | Persist plans to disk (`quality_reports/plans/`) | paper2pr plan-first | Enables plan recovery after compaction |
| C3 | Add proofreader agent | paper2pr agent roster | Catches writing quality issues critic misses |
| C4 | Add hard gates to critic (non-negotiable failures) | paper2pr quarto-critic | Clearer quality thresholds |

### High Priority

| # | Recommendation | Source Pattern | Impact |
|---|---|---|---|
| H1 | Add context-monitor hook | paper2pr hooks | Prevents context blowout in QA loops |
| H2 | Add verify-reminder hook | paper2pr hooks | Catches skipped compilation |
| H3 | Add script-writer agent for speaker notes | paper2pr agent roster | Fills mandatory speaker notes requirement |
| H4 | Add "just do it" mode for simple tasks | paper2pr orchestrator | Reduces friction for routine fixes |
| H5 | Add session logging protocol | paper2pr session management | Enables continuity across sessions |
| H6 | Standardize score report format and location | paper2pr quality_reports | Objective score tracking |

### Medium Priority

| # | Recommendation | Source Pattern | Impact |
|---|---|---|---|
| M1 | Add cognitive load framework to pedagogy-reviewer | impeccable-original | Deeper learning design assessment |
| M2 | Add AI slop anti-patterns | impeccable-original | Catches LLM design bias |
| M3 | Add file-type routing in orchestrator | paper2pr orchestrator | Right agents for right files |
| M4 | Add file-protection hook for critical files | paper2pr hooks | Safety net for theme/config |
| M5 | Add MUST/SHOULD/MAY framework for requirements | paper2pr plan-first | Clearer scope boundaries |
| M6 | Enforce commit-blocking for score < 80 | paper2pr quality gates | Quality enforcement |
| M7 | Add domain-reviewer agent (parameterizable) | paper2pr agent roster | Technical accuracy validation |

### Low Priority

| # | Recommendation | Source Pattern | Impact |
|---|---|---|---|
| L1 | Add notification hook | paper2pr hooks | UX polish |
| L2 | Add log-reminder hook | paper2pr hooks | Session discipline |
| L3 | Formalize dual-nature meta-governance | paper2pr meta-governance | Template clarity |
| L4 | Add severity-driven action chains to critic output | impeccable-original | Guided next steps |

---

## Appendix A: paper2pr Hook Architecture Detail

### Pre-Compact Hook Flow
```
Claude context approaching limit
  → PreCompact event fires
  → pre-compact.py executes:
    1. Read active plan from quality_reports/plans/
    2. Identify current task status
    3. Extract recent decisions from conversation
    4. Save to ~/.claude/sessions/[hash]/pre-compact-state.json
    5. Append note to session log
  → Context compaction occurs (conversation trimmed)
  → SessionStart event fires (with "compact" matcher)
  → post-compact-restore.py executes:
    1. Read pre-compact-state.json
    2. Delete state file (one-time use)
    3. Print recovery message:
       "Restored context: Plan [path] at step [N], last task: [description]"
  → Claude resumes with recovered state
```

### Context Monitor Thresholds
```
40% → "Consider /learn to extract reusable patterns"
55% → "Context growing — prioritize remaining work"
65% → "Focus on essential tasks, defer nice-to-haves"
80% → "Auto-compact approaching — complete current task fully"
90% → "Complete current task NOW — no shortcuts, no partial work"
```

## Appendix B: Quality Report Directory Structure (Recommended)

Based on paper2pr's pattern, adapted for our system:

```
quality_reports/
├── plans/                              # YYYY-MM-DD_description.md
├── session_logs/                       # YYYY-MM-DD_description.md
├── [deck]_critic_round[N].md           # slide-critic output
├── [deck]_fixer_round[N].md            # slide-fixer implementation report
├── [deck]_layout_audit.md              # layout-auditor output
├── [deck]_typography_review.md         # typography-reviewer output
├── [deck]_pedagogy_review.md           # pedagogy-reviewer output
├── [deck]_proofread_report.md          # proofreader output (when added)
├── [deck]_verification.md              # verifier output
└── [deck]_score_history.md             # Round-by-round score progression
```

## Appendix C: Agent Communication Format (Recommended Standard)

Based on paper2pr's report structure, adapted for our agents:

```markdown
# [Agent Name] Report: [Deck Name]
**Date:** YYYY-MM-DD
**Round:** N (if applicable)
**Verdict:** APPROVED | NEEDS REVISION | REJECTED

## Hard Gate Status (if critic)
- [ ] Compilation: PASS/FAIL
- [ ] Content overflow: PASS/FAIL
- [ ] Image references: PASS/FAIL
- [ ] YAML frontmatter: PASS/FAIL
- [ ] Cross-references: PASS/FAIL

## Score
**Current:** X/100 (Gate: [threshold name])
**Previous:** Y/100 (if applicable)
**Delta:** +/-Z

## Issues Found
### Critical (X issues, -N points)
| ID | Slide | Issue | Deduction | Fix |
|---|---|---|---|---|

### Major (X issues, -N points)
| ID | Slide | Issue | Deduction | Fix |
|---|---|---|---|---|

### Minor (X issues, -N points)
| ID | Slide | Issue | Deduction | Fix |
|---|---|---|---|---|

## Strengths
- ...

## Recommended Next Actions
1. [Action] — invoke [agent/skill]
2. ...
```
