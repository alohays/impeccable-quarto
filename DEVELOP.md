# Developer Guide

This guide covers the local development workflow for `impeccable-quarto`: Quarto themes, example decks, Claude Code integration, and the distribution artifacts added in Phase 5.

## Architecture Overview

The repository currently has two parallel documentation trees:

- `source/` contains canonical design references and rules for the Quarto system.
- `.claude/` contains the Claude Code runtime assets: slash-command skills, agents, and rule copies used by the AI workflow.

Primary working directories:

- `themes/` — SCSS theme files for RevealJS decks
- `templates/` — starter `.qmd` files for common presentation modes
- `examples/` — example presentations used for smoke tests and demo output
- `scripts/` — local automation for setup, rendering, scaffolding, scoring, and previews
- `docs/` — static project site and rendered demo artifacts
- `_extensions/` — Quarto extension packaging for `quarto add`

## Prerequisites

- Quarto `>= 1.4.0`
- Python `>= 3.10`
- Recommended fonts:
  - Plus Jakarta Sans
  - Source Sans 3
  - JetBrains Mono
- Optional:
  - `fc-list` for local font detection
  - GitHub Pages access if you are updating `docs/`

## Quick Start

1. Clone the repository.
2. Run `./scripts/setup.sh`.
3. Create a deck with `./scripts/new-deck.sh talks/my-deck.qmd`.
4. Preview it with `quarto preview talks/my-deck.qmd`.
5. Score it with `python3 scripts/quality_score.py talks/my-deck.qmd`.

## Daily Workflow

1. Sync your branch with the latest team state.
2. Use `./scripts/new-deck.sh` or copy an existing file from `templates/` or `examples/`.
3. Render locally with `./scripts/render.sh path/to/deck.qmd`.
4. Run the quality scorer on edited decks.
5. If you changed the main theme, run `./scripts/sync-extension.sh` so the Quarto extension stays in sync.

## Adding a Theme Variant

1. Copy `themes/impeccable.scss` to `themes/impeccable-<variant>.scss`.
2. Override only the variables and component styles that need to change.
3. Add or update a matching starter deck in `templates/`.
4. Add a representative deck in `examples/`.
5. Render the example and compare it with `./scripts/theme-preview.sh`.
6. If the variant should ship via the Quarto extension later, update the extension packaging in the same change set.

## Adding a Template

1. Create `templates/<name>.qmd`.
2. Include complete YAML frontmatter: `title`, `author`, `date`, and `format`.
3. Reference the correct theme file.
4. Include enough slides to demonstrate the intended use case.
5. Update `scripts/new-deck.sh` if the template should be scaffoldable interactively.

## Modifying Quality Scoring

- Rubric references live in [`.claude/rules/quality-gates.md`](/Users/iyunseong/.clawteam/workspaces/impl/codex-2/.claude/rules/quality-gates.md) and [`source/rules/quality-gates.md`](/Users/iyunseong/.clawteam/workspaces/impl/codex-2/source/rules/quality-gates.md).
- The scoring implementation is [`scripts/quality_score.py`](/Users/iyunseong/.clawteam/workspaces/impl/codex-2/scripts/quality_score.py).
- Keep deductions traceable to a documented rule when you add or change checks.
- Re-run the scorer against at least one example deck after any scoring change.

## Adding Skills or Agents

Current Claude Code runtime assets live in:

- [`.claude/skills/`](/Users/iyunseong/.clawteam/workspaces/impl/codex-2/.claude/skills)
- [`.claude/agents/`](/Users/iyunseong/.clawteam/workspaces/impl/codex-2/.claude/agents)
- [`.claude/rules/`](/Users/iyunseong/.clawteam/workspaces/impl/codex-2/.claude/rules)

When adding a skill or agent:

1. Create or update the markdown file in `.claude/`.
2. Update [`CLAUDE.md`](/Users/iyunseong/.clawteam/workspaces/impl/codex-2/CLAUDE.md) if the command surface or architecture description changed.
3. If the plugin metadata exposes counts or highlighted commands, update `.claude-plugin/` as well.

## Quarto Extension Development

The packaged Quarto extension lives in `_extensions/impeccable-quarto/`.

- `_extension.yml` defines the contributed RevealJS format.
- `impeccable.scss` is the extension-local theme copy used by `quarto add`.
- `scripts/sync-extension.sh` refreshes the extension theme from `themes/impeccable.scss`.

If you change the base theme, re-sync before testing the extension.

## Scripts Reference

| Script | Purpose |
|---|---|
| `scripts/setup.sh` | Local environment checks and smoke setup |
| `scripts/new-deck.sh` | Interactive deck scaffolding |
| `scripts/render.sh` | Render one or more decks |
| `scripts/deploy.sh` | Build and deploy the static site |
| `scripts/quality_score.py` | Deck quality scoring |
| `scripts/theme-preview.sh` | Side-by-side preview generation |
| `scripts/sync-extension.sh` | Sync theme assets into `_extensions/` |

## Troubleshooting

### Quarto render fails

- Check `quarto --version`.
- Validate YAML frontmatter indentation and paths.
- Confirm the referenced theme file exists.

### Fonts do not match the theme

- Install the recommended fonts locally when possible.
- If `fc-list` is unavailable, the setup script cannot confirm local installation.
- The web demos rely on Google Fonts, but local exports may still use fallbacks if fonts are missing.

### Quality score looks wrong

- Score the source `.qmd`, not the rendered HTML.
- Compare the deduction with the current rule files.
- Verify the deck still follows the expected semantic-box and notes conventions.

### Extension output looks stale

- Run `./scripts/sync-extension.sh`.
- Re-render the target deck after syncing.
- Make sure the deck is using the extension format rather than a direct local theme override.
