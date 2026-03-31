# Contributing to impeccable-quarto

Thank you for your interest in improving impeccable-quarto!

## Getting Started

1. Install [Quarto](https://quarto.org/docs/get-started/) (v1.4+).
2. Clone this repository.
3. Run `./scripts/render.sh --all` to verify your setup.

## Adding a New Theme Variant

1. Create `themes/impeccable-<name>.scss` following the structure of existing variants.
2. Add a preview slide in `examples/` that uses the new theme.
3. Run `./scripts/theme-preview.sh` to compare side-by-side.

## Adding an Example Presentation

1. Run `./scripts/new-deck.sh examples/<name>.qmd` and follow the prompts.
2. Ensure every slide has speaker notes.
3. Check your score: `python scripts/quality_score.py examples/<name>.qmd`
4. Aim for a score of 80/100 or higher before submitting.

## Quality Guidelines

- **No walls of text.** Keep bullet points to 5 or fewer per slide.
- **Use semantic boxes** (`.keybox`, `.methodbox`, `.warningbox`, `.tipbox`, `.quotebox`) to structure content.
- **Add speaker notes** on every slide — they are checked by the quality scorer.
- **Include alt text** for all images.
- **Don't override font sizes inline.** Use `.smaller` or `.smallest` sparingly.

## Pull Requests

- One theme or example per PR.
- Include a quality score screenshot for new/modified presentations.
- All scripts must be executable (`chmod +x`).

## Code Style

- Shell scripts: follow [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html).
- Python: formatted with `ruff format`, linted with `ruff check`.
