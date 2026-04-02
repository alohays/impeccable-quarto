# Phase 2: Operational Governance — Implementation Plan

**Date:** 2026-04-03
**Status:** DRAFT
**Source:** .context/reviews/00-synthesis.md (Part 2: Gaps 3, 5; Part 7: Phase 2)
**Reference:** paper2pr hook system (7 hooks), session logging protocol, plan-first workflow

---

## Overview

Phase 2 closes the operational governance gap identified by 3/6 analysis agents. impeccable-quarto has zero hooks, no session persistence, no commit-blocking quality gate, and no session logging. paper2pr demonstrates that these patterns are essential for long review sessions and quality enforcement.

**Goal:** Add the minimum viable governance layer — 2 hooks, session persistence infrastructure, a pre-commit quality gate, and session logging templates.

---

## Work Item 1: Claude Code Hooks

**Complexity:** M (Medium)
**Dependencies:** None
**Files to create/modify:**

| Action | File |
|--------|------|
| Create | `.claude/hooks/verify-reminder.py` |
| Create | `.claude/hooks/protect-files.sh` |
| Modify | `.claude/settings.json` |

### 1a. verify-reminder hook

**File:** `.claude/hooks/verify-reminder.py`
**Event:** PostToolUse (matcher: `Write|Edit`)
**Behavior:** Non-blocking (exit 0). After editing a `.qmd` file, prints a reminder to run `quarto render`.
**Reference:** paper2pr `.claude/hooks/verify-reminder.py` (183 lines)

**Exact content (adapted from paper2pr):**

```python
#!/usr/bin/env python3
"""
Verification Reminder Hook for impeccable-quarto

Non-blocking reminder that fires on Write/Edit to .qmd files
to remind about rendering before marking a task as done.

Hook Event: PostToolUse (matcher: "Write|Edit")
Returns: Exit code 0 (non-blocking)
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
NC = "\033[0m"

VERIFY_EXTENSIONS = {
    ".qmd": "render with: quarto render <file>",
    ".scss": "rebuild theme with: quarto render <any-qmd-using-this-theme>",
}

SKIP_EXTENSIONS = [
    ".md", ".txt", ".json", ".yaml", ".yml", ".toml",
    ".svg", ".png", ".jpg", ".pdf", ".gitignore",
]

SKIP_DIRS = [
    "/quality_reports/", "/templates/", "/.claude/", "/.context/",
]


def get_cache_path() -> Path:
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return Path.home() / ".claude" / "sessions" / "default" / "verify-cache.json"
    import hashlib
    h = hashlib.md5(project_dir.encode()).hexdigest()[:8]
    p = Path.home() / ".claude" / "sessions" / h
    p.mkdir(parents=True, exist_ok=True)
    return p / "verify-cache.json"


def was_recently_reminded(file_path: str) -> bool:
    cache_file = get_cache_path()
    try:
        cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    except (json.JSONDecodeError, IOError):
        cache = {}
    last = cache.get(file_path, 0)
    now = time.time()
    cache[file_path] = now
    cache = {k: v for k, v in cache.items() if now - v < 300}
    try:
        cache_file.write_text(json.dumps(cache))
    except IOError:
        pass
    return (now - last) < 60


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        return 0

    file_path = hook_input.get("tool_input", {}).get("file_path", "")
    if not file_path:
        return 0

    path = Path(file_path)
    if path.suffix.lower() in SKIP_EXTENSIONS:
        return 0
    for skip in SKIP_DIRS:
        if skip in file_path:
            return 0

    suffix = path.suffix.lower()
    if suffix not in VERIFY_EXTENSIONS:
        return 0

    if was_recently_reminded(file_path):
        return 0

    action = VERIFY_EXTENSIONS[suffix]
    print(f"\n{CYAN}Verification reminder:{NC} {path.name}")
    print(f"   -> {GREEN}{action}{NC} before marking task complete\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)  # Fail open
```

**Key adaptations from paper2pr:**
- Removed `.tex` and `.R` extensions (not relevant to impeccable-quarto)
- Added `.scss` extension (theme files need re-render to verify)
- Adjusted SKIP_DIRS to match our directory structure
- Kept 60-second throttle and 5-minute cache cleanup
- Kept fail-open pattern (never block Claude due to hook bug)

### 1b. protect-files hook

**File:** `.claude/hooks/protect-files.sh`
**Event:** PreToolUse (matcher: `Edit|Write`)
**Behavior:** Blocking (exit 2 to block). Prevents accidental edits to master theme and settings.

**Exact content (adapted from paper2pr):**

```bash
#!/bin/bash
# Block accidental edits to protected files
# Exit 2 = block the tool call with error message
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
FILE=""

if [ "$TOOL" = "Edit" ] || [ "$TOOL" = "Write" ]; then
  FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
fi

if [ -z "$FILE" ]; then
  exit 0
fi

# Protected files for impeccable-quarto
PROTECTED_PATTERNS=(
  "themes/impeccable.scss"
  "settings.json"
)

for PATTERN in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE" == *"$PATTERN" ]]; then
    echo "Protected file: $(basename "$FILE"). Edit manually or remove protection in .claude/hooks/protect-files.sh" >&2
    exit 2
  fi
done

exit 0
```

**Key adaptations from paper2pr:**
- Changed protected files from `Bibliography_base.bib` + `settings.json` to `themes/impeccable.scss` + `settings.json`
- Uses path suffix matching (`*"$PATTERN"`) instead of basename-only to catch `themes/impeccable.scss`

### 1c. settings.json modification

**File:** `.claude/settings.json`
**Change:** Add `hooks` section while preserving existing `permissions`

**Exact new content:**

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(quarto render*)",
      "Bash(quarto preview*)",
      "Bash(ls *)",
      "Bash(cat *)",
      "Bash(mkdir *)",
      "Bash(cp *)",
      "Bash(git status*)",
      "Bash(git log*)",
      "Bash(git diff*)",
      "Bash(git add*)",
      "Bash(git commit*)",
      "Bash(npm run*)",
      "Bash(python scripts/*)"
    ],
    "deny": [
      "Bash(rm -rf /)*",
      "Bash(git push --force*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/verify-reminder.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### Acceptance Criteria

- [ ] `python3 .claude/hooks/verify-reminder.py` runs without error when given `{"tool_name":"Edit","tool_input":{"file_path":"test.qmd"}}` on stdin
- [ ] `echo '{"tool_name":"Edit","tool_input":{"file_path":"themes/impeccable.scss"}}' | bash .claude/hooks/protect-files.sh` exits with code 2
- [ ] `echo '{"tool_name":"Edit","tool_input":{"file_path":"examples/test.qmd"}}' | bash .claude/hooks/protect-files.sh` exits with code 0
- [ ] `.claude/settings.json` is valid JSON with both `permissions` and `hooks` sections
- [ ] Hook files are executable (`chmod +x`)

---

## Work Item 2: Session Persistence Infrastructure

**Complexity:** S (Small)
**Dependencies:** None
**Files to create/modify:**

| Action | File |
|--------|------|
| Create | `MEMORY.md` (project root) |
| Create | `quality_reports/.gitkeep` |
| Create | `quality_reports/plans/.gitkeep` |
| Create | `quality_reports/session_logs/.gitkeep` |
| Modify | `.gitignore` (add quality_reports exceptions) |

### 2a. MEMORY.md

**File:** `MEMORY.md` (project root)
**Purpose:** Index file for Claude Code's auto-memory system. Persists generic learnings across sessions.

**Exact content:**

```markdown
# MEMORY.md — impeccable-quarto

Persistent learnings for Claude Code sessions. Keep under 200 lines.
Each entry links to a detailed file in `.claude/projects/*/memory/`.

## Format

- [Title](memory-file.md) — one-line description (<150 chars)

## Learnings

<!-- Add entries as learnings accumulate during review sessions -->
```

**Note:** This is the root-level MEMORY.md for the project. The Claude Code auto-memory system uses a separate directory (`~/.claude/projects/*/memory/`). This file serves as a project-level knowledge base that can be committed to git — following paper2pr's pattern of generic learnings that help all users who fork the repo.

### 2b. quality_reports/ directory structure

**Purpose:** Centralized location for plans, session logs, and agent reports. Follows paper2pr's `quality_reports/` pattern (see Appendix B of 04-workflow-analysis.md).

**Directory layout:**

```
quality_reports/
├── .gitkeep                    # Ensure directory is tracked
├── plans/                      # YYYY-MM-DD_description.md
│   └── .gitkeep
└── session_logs/               # YYYY-MM-DD_description.md
    └── .gitkeep
```

Agent reports (critic, fixer, layout, typography, etc.) are written directly into `quality_reports/` at the top level, following the naming convention: `[deck]_[agent]_round[N].md`

### 2c. .gitignore additions

**File:** `.gitignore`
**Change:** Ensure quality_reports/ is tracked but allow gitignoring specific files if needed.

**Add these lines:**

```gitignore
# Quality reports — track plans and session logs
# Agent reports are ephemeral but may be committed for reference
# quality_reports/*.tmp
```

No actual gitignore entries needed — quality_reports should be fully committed. The comment documents the intent.

### Acceptance Criteria

- [ ] `MEMORY.md` exists at project root with format documentation
- [ ] `quality_reports/plans/` directory exists
- [ ] `quality_reports/session_logs/` directory exists
- [ ] All directories are git-trackable (have .gitkeep files)

---

## Work Item 3: Pre-Commit Quality Gate

**Complexity:** M (Medium)
**Dependencies:** `scripts/quality_score.py` must exist (it does — verified)
**Files to create/modify:**

| Action | File |
|--------|------|
| Create | `scripts/pre-commit-quality.sh` |
| Modify | `scripts/quality_score.py` (exit code threshold change: 70 → 80) |

### 3a. Pre-commit hook script

**File:** `scripts/pre-commit-quality.sh`
**Purpose:** Git pre-commit hook that runs quality_score.py on staged .qmd files. Blocks commit if any file scores below 80.
**Reference:** paper2pr quality gates (commit threshold: 80/100)

**Exact content:**

```bash
#!/bin/bash
# Pre-commit quality gate for impeccable-quarto
# Runs quality_score.py on staged .qmd files
# Blocks commit if any file scores below 80
#
# Installation:
#   ln -sf ../../scripts/pre-commit-quality.sh .git/hooks/pre-commit
#   chmod +x scripts/pre-commit-quality.sh
#
# Override (emergency):
#   git commit --no-verify -m "message"

set -euo pipefail

RED="\033[91m"
GREEN="\033[92m"
YELLOW="\033[93m"
BOLD="\033[1m"
RESET="\033[0m"

THRESHOLD=80
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
QUALITY_SCRIPT="$SCRIPT_DIR/quality_score.py"

# Check if quality_score.py exists
if [ ! -f "$QUALITY_SCRIPT" ]; then
  echo -e "${YELLOW}Warning:${RESET} quality_score.py not found at $QUALITY_SCRIPT"
  echo "Skipping quality gate check."
  exit 0
fi

# Get staged .qmd files
STAGED_QMD=$(git diff --cached --name-only --diff-filter=ACM | grep '\.qmd$' || true)

if [ -z "$STAGED_QMD" ]; then
  # No .qmd files staged — nothing to check
  exit 0
fi

echo -e "${BOLD}Pre-commit quality gate${RESET} (threshold: ${THRESHOLD}/100)"
echo "========================================"

FAILED=0
for FILE in $STAGED_QMD; do
  if [ ! -f "$FILE" ]; then
    continue
  fi

  # Run quality_score.py and capture exit code
  # quality_score.py exits 1 if score < threshold (currently 70, will be 80)
  OUTPUT=$(python3 "$QUALITY_SCRIPT" "$FILE" 2>&1) || true
  
  # Extract score from output (matches "Score: XX/100")
  SCORE=$(echo "$OUTPUT" | grep -oP 'Score:.*?(\d+)/100' | grep -oP '\d+(?=/100)' || echo "")
  
  if [ -z "$SCORE" ]; then
    # macOS grep fallback (no -P flag)
    SCORE=$(echo "$OUTPUT" | sed -n 's/.*Score:.*\([0-9][0-9]*\)\/100.*/\1/p' | head -1)
  fi

  if [ -z "$SCORE" ]; then
    echo -e "${YELLOW}Warning:${RESET} Could not parse score for $FILE"
    echo "$OUTPUT"
    continue
  fi

  if [ "$SCORE" -lt "$THRESHOLD" ]; then
    echo -e "${RED}FAIL${RESET} $FILE — score ${SCORE}/100 (need ${THRESHOLD}+)"
    FAILED=1
  else
    echo -e "${GREEN}PASS${RESET} $FILE — score ${SCORE}/100"
  fi
done

echo "========================================"

if [ "$FAILED" -eq 1 ]; then
  echo ""
  echo -e "${RED}${BOLD}Commit blocked:${RESET} One or more .qmd files scored below ${THRESHOLD}/100."
  echo -e "Fix issues and re-stage, or override with: ${YELLOW}git commit --no-verify${RESET}"
  exit 1
fi

echo -e "${GREEN}All staged .qmd files pass quality gate.${RESET}"
exit 0
```

### 3b. quality_score.py threshold fix

**File:** `scripts/quality_score.py`
**Change:** Line 386 — change exit threshold from 70 to 80 to match documentation

**Current (line 386):**
```python
    sys.exit(0 if report.total >= 70 else 1)
```

**New:**
```python
    sys.exit(0 if report.total >= 80 else 1)
```

**Rationale:** The synthesis report (00-synthesis.md) flagged this as a Gap 2 issue: "script threshold 70 → 80 to match documentation." The quality gates document (.claude/rules/quality-gates.md) and paper2pr both use 80 as the commit threshold.

### Acceptance Criteria

- [ ] `scripts/pre-commit-quality.sh` is executable
- [ ] Running it with no staged .qmd files exits 0
- [ ] Running it with a staged .qmd that scores >= 80 exits 0
- [ ] Running it with a staged .qmd that scores < 80 exits 1 with error message
- [ ] `quality_score.py` exits 1 for files scoring below 80 (not 70)
- [ ] Installation instructions are in the script header comment

---

## Work Item 4: Session Logging Protocol

**Complexity:** S (Small)
**Dependencies:** Work Item 2 (quality_reports/ directory must exist)
**Files to create/modify:**

| Action | File |
|--------|------|
| Create | `templates/session-log.md` |
| Create | `templates/quality-report.md` |

### 4a. Session log template

**File:** `templates/session-log.md`
**Purpose:** Template for session logs saved to `quality_reports/session_logs/YYYY-MM-DD_description.md`
**Reference:** paper2pr `session-logging.md` (3-trigger model)

**Exact content:**

```markdown
---
deck: "{{deck_name}}"
date: "{{YYYY-MM-DD}}"
session_type: "{{review|creation|fix|theme}}"
target_score: {{90}}
---

# Session Log: {{description}}

## Goal
<!-- What are we trying to accomplish? -->

## Approach
<!-- High-level strategy chosen -->

## Key Context
<!-- Important constraints, user preferences, relevant history -->

---

## Progress

### Post-Plan
<!-- Captured immediately after plan approval -->
- **Plan:** {{link to quality_reports/plans/ if applicable}}
- **Starting score:** {{N/A or score}}/100
- **Key decisions:** 

### Incremental Notes
<!-- 1-3 lines per event: design decisions, problems solved, corrections -->
<!-- Format: [HH:MM] Note -->

### End of Session
<!-- Captured when wrapping up -->
- **Final score:** /100
- **Rounds completed:** 
- **Issues resolved:** 
- **Issues remaining:** 
- **Open questions:** 

---

## Score Progression

| Round | Score | Delta | Key Change |
|-------|-------|-------|------------|
| 0 (initial) | | | Baseline |
| 1 | | | |

---

## Learnings
<!-- Anything worth adding to MEMORY.md? Use the decision test:
     "Would someone forking impeccable-quarto benefit from this?" -->
```

### 4b. Quality report template

**File:** `templates/quality-report.md`
**Purpose:** Standardized agent report format. Used by all diagnostic/review agents.
**Reference:** paper2pr agent communication format (04-workflow-analysis.md Appendix C)

**Exact content:**

```markdown
---
agent: "{{agent_name}}"
deck: "{{deck_name}}"
date: "{{YYYY-MM-DD}}"
round: {{N}}
---

# {{Agent Name}} Report: {{Deck Name}}

**Date:** {{YYYY-MM-DD}}
**Round:** {{N}}
**Verdict:** APPROVED | NEEDS REVISION | REJECTED

## Hard Gate Status

- [ ] Compilation: PASS / FAIL
- [ ] Content overflow: PASS / FAIL
- [ ] Image references: PASS / FAIL
- [ ] YAML frontmatter: PASS / FAIL
- [ ] Cross-references: PASS / FAIL

## Score

**Current:** /100 (Gate: )
**Previous:** /100
**Delta:** 

## Issues Found

### Critical (0 issues, -0 points)

| ID | Slide | Issue | Deduction | Recommended Fix |
|----|-------|-------|-----------|-----------------|

### Major (0 issues, -0 points)

| ID | Slide | Issue | Deduction | Recommended Fix |
|----|-------|-------|-----------|-----------------|

### Minor (0 issues, -0 points)

| ID | Slide | Issue | Deduction | Recommended Fix |
|----|-------|-------|-----------|-----------------|

## Strengths

- 

## Recommended Next Actions

1. [Action] — invoke [agent/skill]
```

### Acceptance Criteria

- [ ] `templates/session-log.md` exists with all 3 trigger sections (post-plan, incremental, end-of-session)
- [ ] `templates/quality-report.md` exists with hard gates, score, issues tables, and next actions
- [ ] Templates use `{{placeholder}}` syntax for fillable fields
- [ ] Templates follow paper2pr's report structure while adapted for our quality gates

---

## Implementation Order

```
Work Item 2 (Session Persistence)     — no dependencies, simple directory creation
    ↓
Work Item 4 (Session Logging)         — depends on quality_reports/ existing
    
Work Item 1 (Claude Code Hooks)       — no dependencies, but test after creation
Work Item 3 (Pre-Commit Hook)         — no dependencies, modifies quality_score.py
```

**Recommended execution:** Items 1 and 2 can be done in parallel. Item 4 depends on Item 2. Item 3 is independent.

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| protect-files.sh blocks legitimate theme edits | Script header documents how to remove protection; user can also `--no-verify` |
| verify-reminder noise during rapid editing | 60-second throttle prevents spam |
| pre-commit hook breaks existing workflow | Override with `git commit --no-verify`; threshold matches documented standard |
| quality_score.py threshold change (70→80) breaks existing usage | Documented in synthesis as needed fix; scripts should match docs |
| macOS `grep -P` not available | Pre-commit script includes `sed` fallback for score parsing |

---

## Verification Plan

After implementation, verify:

1. **Hooks load correctly:** Start a new Claude Code session and trigger an Edit on a .qmd file — verify reminder appears
2. **File protection works:** Attempt to edit `themes/impeccable.scss` — verify block message
3. **Pre-commit blocks low scores:** Stage a minimal .qmd with no speaker notes — verify commit blocked
4. **Pre-commit passes good files:** Stage a well-formed .qmd — verify commit succeeds
5. **Directory structure exists:** `ls -R quality_reports/` shows plans/ and session_logs/
6. **Templates are usable:** Templates render correctly as markdown

---

*Plan created by governance-planner agent on 2026-04-03*
*Reference: 00-synthesis.md Phase 2, 04-workflow-analysis.md sections 4+8*
