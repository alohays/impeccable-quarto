# Phase 1: Foundation Fixes — Implementation Plan

**Date:** 2026-04-03
**Source:** 6-agent reference analysis (`.context/reviews/00-synthesis.md`)
**Target:** Structural integrity, automation parity, adversarial enforcement

---

## Work Item 1: SSOT Fix

### Decision

**Accept `.claude/` as the canonical location.** Rationale:
- `.claude/` has 32 working files (7 agents, 18 skills, 6 rules, settings.json)
- `source/` has only 9 files (6 references, 3 rules) — it was never populated with agents or skills
- The 3 rules in `source/rules/` are byte-identical copies of files in `.claude/rules/`
- No sync mechanism exists or ever existed
- Creating a build pipeline (source/ → .claude/) adds complexity for zero current benefit
- `source/references/` (6 design reference files: typography, color-and-contrast, motion-design, slide-patterns, spatial-design, anti-patterns) are genuinely separate reference documents, not duplicates — they should be relocated

### Changes

| # | File | Action | Details |
|---|------|--------|---------|
| 1.1 | `source/rules/anti-patterns.md` | **Delete** | Identical copy of `.claude/rules/anti-patterns.md` |
| 1.2 | `source/rules/design-standards.md` | **Delete** | Identical copy of `.claude/rules/design-standards.md` |
| 1.3 | `source/rules/quality-gates.md` | **Delete** | Identical copy of `.claude/rules/quality-gates.md` |
| 1.4 | `source/references/*.md` (6 files) | **Move** to `.claude/references/` | These are design reference docs used by agents/skills. Move them to the canonical tree. |
| 1.5 | `source/` directory | **Delete** (now empty) | Remove the empty directory |
| 1.6 | `CLAUDE.md` lines 9–32 | **Rewrite** Directory Structure section | See Work Item 4 for full CLAUDE.md changes |

### Acceptance Criteria

- [ ] `source/` directory no longer exists
- [ ] `.claude/references/` contains: `typography.md`, `color-and-contrast.md`, `motion-design.md`, `slide-patterns.md`, `spatial-design.md`, `anti-patterns.md`
- [ ] No duplicate files exist in the repo (verified via `md5 -r`)
- [ ] All agent/skill files that reference `source/references/` are updated to `.claude/references/`
- [ ] CLAUDE.md accurately describes the actual directory structure

### Complexity: **S**

### Dependencies: None (do this first; Work Item 4 depends on this)

---

## Work Item 2: quality_score.py Improvements

### Current State (`scripts/quality_score.py`, 391 lines)

- Exit code threshold: `70` (line 386: `sys.exit(0 if report.total >= 70 else 1)`)
- Quality gates docs say minimum passing is `80` (Needs Work = 60–79, Draft = 80–84)
- **Missing checks:**
  - CRIT-01: No `quarto render` call — cannot detect compilation failures
  - MAJ-05: No pure black `#000000` / white `#FFFFFF` detection
  - MIN-02: No per-slide word count check (≤40 words body text)
  - MAJ-07: No OKLCH enforcement for color values in .qmd

### Changes

| # | Location | Action | Details |
|---|----------|--------|---------|
| 2.1 | Line 386 | **Fix threshold** | Change `70` → `80` |
| 2.2 | New function | **Add `check_compilation()`** | Run `subprocess.run(["quarto", "render", str(path), "--to", "html"], capture_output=True, timeout=120)`. If return code ≠ 0, deduct 100 (CRIT-01, auto-fail). Add `--no-clean` to avoid deleting output. Include `import subprocess` at top. |
| 2.3 | New function | **Add `check_pure_bw()`** | Scan content (outside code blocks and frontmatter) for patterns: `#000000`, `#000`, `#fff`, `#ffffff`, `rgb(0,0,0)`, `rgb(255,255,255)`, `#FFF`, `#FFFFFF`. Deduct 3 per instance (MAJ-05), capped at 15. |
| 2.4 | New function | **Add `check_word_count()`** | For each slide, count words in body text (exclude headings, code blocks, speaker notes, div markers). If > 40 words, deduct 2 per slide (MIN-02). |
| 2.5 | `score_file()` (line 297–311) | **Integrate new checks** | Call `check_compilation()` first (before any other checks — if it fails, score is 0 and remaining checks are informational). Then call `check_pure_bw()` and `check_word_count()` alongside existing checks. |
| 2.6 | Line 314–337 | **Update grade display** | Align grade letters with quality gate names: A+ (95–100 Impeccable), A (90–94 Excellent), B (85–89 Presentable), B- (80–84 Draft), C (60–79 Needs Work), F (0–59 Failing) |
| 2.7 | Imports | **Add** | `import subprocess`, `import shutil` (to check quarto availability) |
| 2.8 | CLI options | **Add `--no-render` flag** | Skip compilation check for fast scoring during development. Default: render enabled. |

### Detailed Implementation: `check_compilation()`

```python
def check_compilation(path: Path, report: ScoreReport, skip_render: bool = False) -> bool:
    """Run quarto render and check for compilation failures (CRIT-01)."""
    if skip_render:
        report.warn("Compilation check skipped (--no-render)")
        return True

    if not shutil.which("quarto"):
        report.warn("quarto not found in PATH — compilation check skipped")
        return True

    try:
        result = subprocess.run(
            ["quarto", "render", str(path), "--to", "html"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            error_msg = result.stderr[:200] if result.stderr else "Unknown error"
            report.deduct("CRIT-01", 100, f"Compilation failed: {error_msg}")
            return False
    except subprocess.TimeoutExpired:
        report.deduct("CRIT-01", 100, "Compilation timed out (>120s)")
        return False
    except FileNotFoundError:
        report.warn("quarto not found — compilation check skipped")

    return True
```

### Detailed Implementation: `check_pure_bw()`

```python
PURE_BW_RE = re.compile(
    r"""(?:
        \#(?:000000|000|fff|ffffff)  |
        rgb\(\s*0\s*,\s*0\s*,\s*0\s*\)  |
        rgb\(\s*255\s*,\s*255\s*,\s*255\s*\)
    )""",
    re.IGNORECASE | re.VERBOSE,
)

def check_pure_bw(content: str, report: ScoreReport) -> None:
    """Detect pure black/white color values (MAJ-05)."""
    # Strip code blocks and frontmatter before scanning
    stripped = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    stripped = re.sub(r"^---\n.*?\n---", "", stripped, flags=re.DOTALL)
    matches = PURE_BW_RE.findall(stripped)
    for match in matches[:5]:  # Cap at 5 reports
        report.deduct("pure-bw", 3, f"Pure black/white color value: {match}")
```

### Detailed Implementation: `check_word_count()`

```python
def check_word_count(report: ScoreReport, content: str) -> None:
    """Check per-slide body text word count (MIN-02: max 40 words)."""
    lines = content.split("\n")
    # Re-use slide boundaries from report.slides
    for slide in report.slides:
        # Extract slide text between slide.line_start and next slide start
        start = slide.line_start - 1  # 0-indexed
        # Find end: next slide's line_start or EOF
        next_starts = [s.line_start - 1 for s in report.slides if s.line_start > slide.line_start]
        end = next_starts[0] if next_starts else len(lines)
        slide_lines = lines[start:end]

        # Filter out headings, code blocks, div markers, speaker notes
        body_words = []
        in_code = False
        in_notes = False
        for sl in slide_lines:
            s = sl.strip()
            if s.startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            if s == "::: {.notes}" or s == ":::{.notes}":
                in_notes = True
                continue
            if in_notes and s == ":::":
                in_notes = False
                continue
            if in_notes:
                continue
            if s.startswith("#") or s.startswith(":::") or s == "---" or not s:
                continue
            # Count words in remaining body text
            body_words.extend(s.split())

        word_count = len(body_words)
        if word_count > 40:
            report.deduct(
                "word-count",
                2,
                f"Slide {slide.number} '{slide.heading}': {word_count} words (max 40)",
            )
```

### Acceptance Criteria

- [ ] `python scripts/quality_score.py examples/academic-paper.qmd` runs successfully
- [ ] Exit code is 1 when score < 80 (not 70)
- [ ] Compilation failure produces score 0 with CRIT-01 deduction
- [ ] `--no-render` flag skips compilation check
- [ ] Pure `#000` or `#fff` in .qmd body text triggers MAJ-05 deduction
- [ ] Slides with >40 body words trigger MIN-02 deduction
- [ ] Grade display matches quality gate names from `quality-gates.md`
- [ ] All existing checks still work (no regressions)

### Complexity: **M**

### Dependencies: None (independent of other work items)

---

## Work Item 3: Agent Enforcement (tools + context frontmatter)

### Current State

All 7 agent files in `.claude/agents/` have only `name` and `description` in their YAML frontmatter:

```yaml
---
name: slide-critic
description: "Adversarial reviewer: ..."
---
```

**Missing:**
- `tools:` — no tool restrictions enforced. Critic agents can write files; the fixer has no explicit write permission grant. Paper2pr enforces this per-agent.
- `context: fork` — no context isolation. Critic and fixer share the same context window, violating adversarial integrity.

### Changes

| # | File | Add `tools:` | Add `context:` | Rationale |
|---|------|-------------|---------------|-----------|
| 3.1 | `.claude/agents/slide-critic.md` | `Read, Grep, Glob` | `fork` | Read-only reviewer. Fork ensures adversarial isolation from fixer. |
| 3.2 | `.claude/agents/slide-fixer.md` | `Read, Grep, Glob, Write, Edit, Bash` | `fork` | Needs write access for fixes + Bash for `quarto render` verification. Fork ensures isolation from critic. |
| 3.3 | `.claude/agents/typography-reviewer.md` | `Read, Grep, Glob` | `fork` | Read-only specialist. |
| 3.4 | `.claude/agents/layout-auditor.md` | `Read, Grep, Glob` | `fork` | Read-only specialist. |
| 3.5 | `.claude/agents/content-translator.md` | `Read, Grep, Glob, Write, Edit` | `fork` | Creates .qmd files. No Bash needed. |
| 3.6 | `.claude/agents/theme-designer.md` | `Read, Grep, Glob, Write, Edit` | `fork` | Creates/edits .scss files. No Bash needed. |
| 3.7 | `.claude/agents/verifier.md` | `Read, Grep, Glob, Bash` | `fork` | Needs Bash for `quarto render`. No Write — verifier reports, doesn't fix. |

### Example: Updated `slide-critic.md` frontmatter

```yaml
---
name: slide-critic
description: "Adversarial reviewer: finds issues, scores, produces actionable reports. Never edits files."
tools:
  - Read
  - Grep
  - Glob
context: fork
---
```

### Example: Updated `slide-fixer.md` frontmatter

```yaml
---
name: slide-fixer
description: "Applies fixes from critic reports. Prioritizes Critical > Major > Minor."
tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash
context: fork
---
```

### Acceptance Criteria

- [ ] All 7 agent files have `tools:` frontmatter with appropriate tool lists
- [ ] All 7 agent files have `context: fork`
- [ ] Read-only agents (slide-critic, typography-reviewer, layout-auditor) do NOT have Write, Edit, or Bash
- [ ] Write agents (slide-fixer, content-translator, theme-designer) have Write and Edit
- [ ] Only agents that need shell access (slide-fixer, verifier) have Bash
- [ ] Verifier does NOT have Write or Edit (reports only, doesn't fix)
- [ ] Frontmatter is valid YAML (no syntax errors)

### Complexity: **S**

### Dependencies: None (independent)

---

## Work Item 4: CLAUDE.md Cleanup

### Current State (337 lines)

CLAUDE.md contains:
1. **Project Overview** (lines 1–7) — accurate, keep
2. **Directory Structure** (lines 9–32) — **inaccurate** (claims source/ is canonical)
3. **Key Workflows** (lines 34–68) — useful, keep
4. **Quality Gates** (lines 70–105) — **duplicates** `.claude/rules/quality-gates.md` entirely
5. **Design Principles** (lines 107–150) — **duplicates** `.claude/rules/design-standards.md` partially
6. **Anti-Patterns Quick Reference** (lines 152–180) — **duplicates** `.claude/rules/anti-patterns.md` (abbreviated)
7. **Build Commands** (lines 182–205) — useful, keep
8. **Theme Reference** (lines 207–245) — useful quick reference, keep (abbreviated)
9. **Slide YAML Frontmatter Template** (lines 247–265) — useful, keep
10. **Semantic Box Usage** (lines 267–300) — useful, keep
11. **Layout Usage** (lines 302–320) — useful, keep
12. **Fragment** (lines 322–330) — useful, keep
13. **Speaker Notes** (lines 332–337) — useful, keep

### Changes

| # | Section | Action | Details |
|---|---------|--------|---------|
| 4.1 | Directory Structure (lines 9–32) | **Rewrite** | Reflect actual structure: `.claude/` as canonical, no `source/` |
| 4.2 | Quality Gates (lines 70–105) | **Replace with pointer** | Replace full table with: "See `.claude/rules/quality-gates.md` for the complete scoring rubric." Keep just the gate threshold table (6 rows) for quick reference. |
| 4.3 | Design Principles — ALWAYS/NEVER (lines 107–150) | **Replace with pointer** | Replace with: "See `.claude/rules/design-standards.md` for complete design standards." Keep a 5-item bullet summary. |
| 4.4 | Anti-Patterns Quick Reference (lines 152–180) | **Replace with pointer** | Replace with: "See `.claude/rules/anti-patterns.md` for the full anti-pattern registry." Remove the table entirely. |
| 4.5 | "When in doubt" callout (line 32) | **Remove** | No longer applicable (source/ gone) |

### Estimated Result

CLAUDE.md shrinks from ~337 lines to ~220 lines. Content is not lost — it lives in the rules files that Claude Code already loads via `.claude/rules/`.

### New Directory Structure Section

```markdown
## Directory Structure

\```
.claude/          Claude Code integration (canonical)
  agents/         Agent persona definitions (7)
  skills/         Slash commands (18)
  rules/          Governance rules, scoring rubrics, anti-patterns (6)
  references/     Design reference documents (6)
  settings.json   Permissions and hooks

themes/           SCSS themes for Quarto RevealJS
  impeccable.scss Master theme (OKLCH · tinted neutrals · typography-first)

templates/        Starter .qmd templates for common presentation types
examples/         Complete example presentations with scores
scripts/          Build, render, and utility scripts
\```
```

### Acceptance Criteria

- [ ] Directory Structure section matches actual repo layout
- [ ] No mention of `source/` as canonical
- [ ] Quality gates, design principles, and anti-patterns sections replaced with pointers to `.claude/rules/`
- [ ] CLAUDE.md is under 250 lines
- [ ] All information from removed sections is already present in `.claude/rules/` files (verified)
- [ ] Quick-reference summary items (gate thresholds, 5-point ALWAYS/NEVER) are retained for fast scanning

### Complexity: **S**

### Dependencies: Work Item 1 (SSOT fix must be done first so directory structure is accurate)

---

## Execution Order

```
┌─────────────────┐     ┌──────────────────────┐     ┌──────────────────┐
│ WI-1: SSOT Fix  │     │ WI-2: quality_score.py│     │ WI-3: Agent      │
│ (S, no deps)    │     │ (M, no deps)          │     │ enforcement (S)  │
└────────┬────────┘     └──────────────────────┘     └──────────────────┘
         │                                            
         │ depends on                                 
         ▼                                            
┌──────────────────┐
│ WI-4: CLAUDE.md  │
│ cleanup (S)      │
└──────────────────┘
```

**Parallel execution:** WI-1, WI-2, and WI-3 can all run in parallel.
**Sequential:** WI-4 must wait for WI-1 to complete.

---

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| Moving `source/references/` breaks agent/skill references | Grep all `.claude/` files for `source/references` before moving; update any paths found |
| `quarto render` in quality_score.py is slow | `--no-render` flag for fast mode; timeout=120s prevents hangs |
| `context: fork` may not be supported in current Claude Code version | Verify with a test invocation; if unsupported, document as aspirational and omit |
| Agent tool restrictions may break existing workflows | Test each agent with a simple invocation after changes |
| CLAUDE.md reduction removes useful quick-reference | Keep gate threshold table and 5-point ALWAYS/NEVER summary |

---

## Validation Plan

After all 4 work items are complete:

1. **Structural check:** `find source/ -type f` returns nothing (or directory doesn't exist)
2. **No duplicates:** `md5 -r .claude/rules/*.md` shows unique hashes
3. **quality_score.py:** Run against all examples — check scores and exit codes
4. **Agent frontmatter:** `grep -l "^tools:" .claude/agents/*.md | wc -l` returns 7
5. **CLAUDE.md accuracy:** Every path mentioned in Directory Structure section exists
6. **No broken references:** `grep -r "source/" .claude/ CLAUDE.md AGENTS.md` returns no hits

---

*Plan generated 2026-04-03 by foundation-planner*
*Based on analysis from 6 ClawTeam agents (3,928 lines of reports)*
