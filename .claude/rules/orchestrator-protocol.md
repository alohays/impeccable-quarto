---
name: orchestrator-protocol
description: "Workflow governance: planning, source of truth, verification, session management"
---

# Orchestrator Protocol

## Core Principles

1. **Plan first for non-trivial work** — Any deck with >5 slides or multi-agent involvement requires a plan before execution
2. **Single source of truth** — The `.qmd` file is authoritative. All changes flow through it. Never edit rendered output.
3. **Mandatory verification** — No work is marked complete without a `verifier` agent pass
4. **Session logging** — Multi-round work must track state for continuity

## Workflow Governance

### Simple Tasks (single skill, <5 slides affected)
```
1. Read the file
2. Apply the skill
3. Verify compilation
4. Done
```

### Standard Tasks (single skill, full deck)
```
1. Read the file and rules
2. Plan changes (mental — no formal plan document needed)
3. Apply the skill
4. Run verifier
5. Report results
```

### Complex Tasks (multi-agent, full review, QA loops)
```
1. Read the file and all relevant rules
2. Create a formal plan with phases
3. Execute Phase 1 (diagnostic — parallel agents)
4. Synthesize Phase 1 results
5. Execute Phase 2 (specialist review — parallel agents)
6. Synthesize Phase 2 results
7. Execute Phase 3 (QA loop — iterative)
8. Execute Phase 4 (final verification)
9. Produce final report
```

### Deck Creation (from source material)
```
1. Read source material completely
2. Read source-translation rules
3. Plan the deck structure (outline)
4. Get user approval on outline (if interactive)
5. Generate .qmd content
6. Create/apply theme
7. Run verifier
8. Run slide-critic for quality check
9. Fix any critical issues
10. Final verification
```

## Agent Coordination Rules

### Separation of Concerns
- **Diagnostic agents** (critic, typography-reviewer, layout-auditor): READ-ONLY. Never edit files.
- **Fix agents** (slide-fixer): Edit files based on reports. Never self-assess quality.
- **Verification agent** (verifier): Compilation and technical validation only. No design opinions.
- **Creative agents** (content-translator, theme-designer): Create content/themes. Not responsible for quality review.

### Adversarial Integrity
- The critic and fixer must never be the same agent context
- A critic must not see the fixer's rationale — only the resulting file
- A fixer must not soften fixes to please the critic
- Verification is independent of both critic and fixer

### Parallel Execution
- Run independent agents concurrently when possible
- Never run critic and fixer concurrently on the same file
- Phase gates must be respected — all agents in a phase complete before the next phase

## File Governance

### Source of Truth
- The `.qmd` file is the single source of truth
- Never edit rendered HTML, PDF, or other output files
- Theme changes go in `.scss` files
- Style preferences go in `.impeccable-quarto.md`

### File Modification Rules
- Always read the full file before modifying
- Make targeted edits, not full rewrites (unless creating a new file)
- Preserve the author's voice and intent
- Never delete content without moving it to speaker notes

### Backup and Recovery
- Before a QA loop, note the initial file state (for regression recovery)
- If a fix round causes regression, revert to the best-scoring version
- Keep track of what was changed in each round

## Session Management

### Logging
- Multi-round sessions should track:
  - Score progression (round-by-round)
  - Issues found and fixed
  - Time spent per phase
  - Final outcome

### Continuity
- If a session is interrupted, the `.qmd` file state is authoritative
- Re-read the file and re-assess rather than relying on stale session state
- Reports can be cached but scores should be re-verified

## Completion Criteria

A task is complete when ALL of the following are true:
1. The `.qmd` file compiles without errors
2. The verifier agent has passed the final version
3. All critical issues from the last critic report are resolved
4. The score meets the target threshold (default: 90/100 for review tasks)
5. Results are reported to the user

## Error Handling

- **Compilation failure**: Stop all other work. Fix compilation first.
- **Agent failure**: Retry once. If it fails again, escalate to user.
- **Score regression**: Revert to last best version, report to user.
- **Infinite loop detection**: If 3 consecutive rounds have the same score (±2 points), terminate.
- **Conflicting agent recommendations**: Higher-severity issue takes priority. If equal, prefer the change with fewer side effects.
