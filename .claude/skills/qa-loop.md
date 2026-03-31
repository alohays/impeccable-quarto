---
name: qa-loop
description: "Adversarial QA: critic finds issues, fixer applies fixes, loop until approved (max 5 rounds)"
user-invocable: true
argument-hint: "[file]"
---

# /qa-loop — Adversarial Quality Assurance Loop

[MANDATORY PREPARATION]
- Read `.claude/rules/review-protocol.md` for QA loop protocol
- Read `.claude/rules/quality-gates.md` for pass/fail thresholds
- Read `.claude/rules/design-standards.md` and `.claude/rules/anti-patterns.md`
- Read the target `.qmd` file completely
- Determine the target quality level (default: 90/100 — Presentable)

[IMPLEMENTATION STEPS]
1. **Round 1: Initial Critique**
   - Invoke `slide-critic` agent on the current file
   - Critic produces a scored report with categorized issues
   - If score ≥ target threshold → **PASS** (skip to step 5)
   - If score < target threshold → proceed to fix

2. **Round N: Fix Cycle** (max 5 rounds)
   - Invoke `slide-fixer` agent with the critic's report
   - Fixer applies fixes in priority order: Critical → Major → Minor
   - Fixer reports: what was fixed, what was skipped and why
   - After fixes, invoke `verifier` agent to confirm compilation
   - If compilation fails → fixer must resolve before re-critique

3. **Round N: Re-Critique**
   - Invoke `slide-critic` agent on the updated file
   - Critic scores the fixed version
   - If score ≥ target threshold → **PASS**
   - If score < previous round → flag regression, revert problematic fixes
   - If score improved but still below threshold → continue loop

4. **Loop Termination**
   - **PASS**: Score meets threshold
   - **MAX ROUNDS**: 5 rounds exhausted — present final state with remaining issues
   - **REGRESSION**: Score decreased — revert to best-scoring version
   - **STALLED**: Same score for 2 consecutive rounds — stop and report

5. **Final Report**
   - Produce a summary of all rounds
   - Show score progression: Round 1 → Round 2 → ... → Final
   - List any remaining issues that could not be fixed
   - Recommend manual intervention if needed

[OUTPUT FORMAT]
```
## QA Loop Report: <filename>

### Result: PASS / FAIL (max rounds) / STALLED
**Target: XX/100** | **Final Score: XX/100**

### Score Progression
| Round | Score | Issues Fixed | Issues Remaining |
|-------|-------|-------------|-----------------|
| 1     | XX    | -           | N               |
| 2     | XX    | N           | N               |
| ...   | ...   | ...         | ...             |

### Changes Made
- Round 2: Fixed overflow on slide 5, added alt text to 3 images...
- Round 3: Fixed typography consistency, adjusted color contrast...

### Remaining Issues (if any)
- Issue — Reason it couldn't be auto-fixed

### Recommendation
Next steps for the author
```

[ANTI-PATTERNS TO AVOID]
- Do NOT exceed 5 rounds — this prevents infinite loops
- Do NOT let the fixer make changes that regress the score
- Do NOT skip the verification step between fix and re-critique
- Do NOT let the critic and fixer be the same agent context (adversarial separation)
- Do NOT accept a score decrease as "progress"

[QUALITY CHECKS]
- Critic and fixer operate as separate agents (adversarial integrity)
- Score monotonically improves or the loop terminates
- Every fix is verified via compilation before re-critique
- Final report shows complete score progression
- Remaining issues have clear explanations for why they weren't fixed
