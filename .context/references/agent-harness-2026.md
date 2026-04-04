# Agent Harness Engineering Trends (2025-2026)

**Date:** 2026-04-03
**Source:** Web research (Claude Code docs, awesome-claude-code, research papers)

---

## 1. Claude Code Canonical `.claude/` Structure

### Agent Frontmatter (Official Fields)
`name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `isolation`, `color`, `effort`, `initialPrompt`

### Skill Frontmatter (Official Fields)
`name`, `description`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`, `effort`, `context`, `agent`, `hooks`, `paths`, `shell`, `argument-hint`

**Critical distinction:** `context: fork` is a **skill** field, NOT an agent field. Agents use `isolation: worktree` for git-worktree-based isolation.

### New Agent Capabilities (2026)
- `memory: project|user|local` — persistent learning across sessions
- `model: haiku|sonnet|opus|inherit` — per-agent model routing for cost optimization
- `isolation: worktree` — git worktree-based isolation

### Hook Lifecycle Events
`PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`

Hook handlers: `command` (shell) or `prompt` (LLM single-turn evaluation)

---

## 2. Agent Teams (Claude Code Native, Experimental)

Independent Claude Code sessions coordinating via:
- **Shared task list** — teammates claim and complete tasks
- **Direct inter-agent messaging** (mailbox)
- **Parallel git worktrees** — each teammate works on an isolated copy

Applicable to impeccable-quarto: critic, typography-reviewer, layout-auditor as independent teammates sharing findings via task list, then fixer teammate claims and resolves.

---

## 3. Multi-Agent Orchestration Patterns

### Blackboard Pattern
Shared state object. Agents read, process, write back. All diagnostic agents contribute to a shared issue list in real time (vs. producing independent reports to merge).

### Plan-and-Execute
Expensive model plans, cheap models execute. Opus plans review strategy → Haiku/Sonnet runs individual checks. 70-90% token cost reduction.

### Ralph Wiggum Pattern
Stop hook checks completion criteria (quality score ≥ threshold). Agent cannot stop until criteria met, with safety limits. Replaces fixed round limits.

### Competing Hypotheses
Multiple agents investigate different theories, then debate. Maps to adversarial review where critic and fixer present competing views.

---

## 4. Quality Gate Systems

### Hybrid Deterministic + LLM Scoring
Deterministic checks (regex, word count, compilation) run first → results feed into LLM evaluation. impeccable-quarto has both pieces but they're separate.

### LLM-as-Judge Best Practices
- Chain-of-thought evaluation (explain reasoning, not just score)
- Dynamic rubric criteria per presentation domain
- Inter-judge reliability metrics (Cohen's Kappa between multiple passes)

### CI Integration Pattern (CodeScene model)
Quality score runs automatically in PRs. AI fix recommendations alongside score. Gate blocks merge below threshold.

---

## 5. Plugin Distribution

Claude Code plugin marketplace (launched 2026-01-30, 9000+ plugins).
`.claude-plugin/plugin.json` manifest for bundled distribution.
impeccable-quarto already has this structure — confirm it's up-to-date with latest spec.

---

## 6. MCP Server Integration

Slidev, Marp both have MCP servers for programmatic slide creation.
No Quarto MCP server exists — opportunity for impeccable-quarto.
MCP server would make the quality scorer usable from Claude Desktop, VS Code Copilot, n8n, etc.

---

## Comparable Projects

| Project | Platform | Agents | Quality Scoring | AI Integration |
|---------|----------|--------|----------------|----------------|
| impeccable-quarto | Quarto RevealJS | 7 | 100-point deductive | Claude Code skills |
| claude-code-my-workflow (pedrohcgs) | Beamer + Quarto | 10 | Quality gates 80/90/95 | Claude Code |
| cc-slidev (rhuss) | Slidev | N/A | Design guardrails | Claude Code plugin |
| impeccable-original (pbakaus) | Generic frontend | 0 (skills only) | Heuristic scoring | Multi-tool |
