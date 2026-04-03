---
name: review-protocol
description: "Multi-agent review orchestration: phases, agent coordination, QA loop governance"
---

# Review Protocol

## Overview

The review process uses multiple specialized agents in a structured pipeline. Each phase has specific goals and agents, and phases execute in order.

## Phase 1: Parallel Diagnostic

**Goal**: Get a comprehensive understanding of the presentation's current state.

**Agents** (run concurrently):
- `slide-critic` — Adversarial design/UX review, produces scored report
- `layout-auditor` — Spatial analysis, overflow detection, density assessment

**Gate**: Both agents must complete before Phase 2 begins.

**Output**: Two independent reports with issue lists and scores.

## Phase 2: Specialist Review

**Goal**: Deep assessment in specific domains.

**Agents** (run concurrently):
- `typography-reviewer` — Font, hierarchy, sizing, spacing analysis
- `verifier` — Compilation check, output validation, reference integrity

**Gate**: Both agents must complete before Phase 3 begins.

**Output**: Two specialist reports. If verifier finds compilation failure, escalate immediately (skip to fix).

## Phase 3: Adversarial QA Loop

**Goal**: Iterative improvement through critic→fixer cycles.

**Process**:
1. Merge Phase 1 and Phase 2 findings into a unified issue list
2. Invoke `slide-fixer` with the merged report
3. After fixes, invoke `verifier` to confirm compilation
4. If compilation passes, invoke `slide-critic` for re-evaluation
5. Repeat until:
   - Score ≥ target threshold (default: 90/100) → **PASS**
   - 5 rounds exhausted → **MAX ROUNDS** (present best version)
   - Score regresses → **REGRESSION** (revert to best version)
   - Score unchanged for 2 rounds → **STALLED** (stop)

**Governance Rules**:
- Critic and fixer MUST be separate agent invocations (adversarial integrity)
- Fixer must not see critic's previous reports from other rounds (fresh evaluation)
- Score must monotonically improve or loop terminates
- Each round must include a verification step

## Phase 4: Final Verification

**Goal**: Confirm the final version meets quality gates.

**Agent**: `verifier`

**Checks**:
- Compilation succeeds without warnings
- All references resolve
- Output HTML is valid
- Speaker notes are present
- No regressions from the original

**Gate**: Verification must pass for the review to be considered complete.

## Orchestration Rules

1. **Parallel when possible**: Phases 1 and 2 run agents concurrently within each phase
2. **Sequential between phases**: Phase N must complete before Phase N+1 begins
3. **Early termination**: If Phase 1 finds score ≥ 95, skip directly to Phase 4
4. **Escalation**: If any agent encounters an unresolvable issue, escalate to user
5. **Logging**: Each phase's results are recorded for the final report

## Agent Communication

Agents communicate through reports, not direct messaging:
- Critic produces reports → Fixer consumes reports
- All agents read the same rules files for consistency
- No agent modifies another agent's report

### Report Format Standard

All agent reports MUST use the template in `templates/agent-report.md`. Key requirements:
- Hard Gate Status table must be filled for critic agents
- Score section must include previous score and delta (after round 1)
- Issues must be categorized by severity with deduction point values
- Recommended Next Actions must map to specific skills or agents
- Strengths section must not be empty — identify at least 2 positive aspects

## Time Budget

For a typical 20-slide presentation:
- Phase 1: ~2 minutes (parallel)
- Phase 2: ~2 minutes (parallel)
- Phase 3: ~3-5 minutes per round, max 5 rounds
- Phase 4: ~1 minute
- Total maximum: ~30 minutes
