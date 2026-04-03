#!/usr/bin/env python3
"""Quality scoring tool for Quarto RevealJS presentations.

Analyzes a .qmd file and produces a score out of 100 with deduction breakdown.

Usage:
    python scripts/quality_score.py examples/academic-paper.qmd
    python scripts/quality_score.py --verbose examples/tech-talk.qmd
"""

from __future__ import annotations

import argparse
import math
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ANSI color codes
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

MAX_BULLETS_PER_SLIDE = 5
MIN_SLIDES = 5
MAX_SLIDES = 40
ANTI_PATTERN_RE = re.compile(
    r"font-size\s*:|style\s*=\s*[\"'].*font-size",
    re.IGNORECASE,
)
SEMANTIC_BOX_RE = re.compile(
    r"\.(?:keybox|methodbox|warningbox|tipbox|quotebox|infobox)\b",
)
GENERIC_TITLE_RE = re.compile(
    r"^(presentation title|subtitle here|your name|author name|\[topic\]|click to edit)$",
    re.IGNORECASE,
)
AI_COLOR_RE = re.compile(
    r"(#(?:00bcd4|00acc1|00e5ff|7c4dff|651fff|8b5cf6|a855f7|c084fc)|"
    r"rgb\(\s*0\s*,\s*(?:172|188|229)\s*,\s*(?:193|212|255)\s*\))",
    re.IGNORECASE,
)
GRADIENT_TEXT_RE = re.compile(
    r"background(?:-image)?\s*:\s*(?:-webkit-)?linear-gradient\([^)]*\).*?"
    r"(?:background-clip\s*:\s*text|-webkit-background-clip\s*:\s*text)",
    re.IGNORECASE | re.DOTALL,
)


@dataclass
class Deduction:
    rule: str
    points: int
    detail: str


@dataclass
class SlideInfo:
    number: int
    heading: str
    bullet_count: int
    has_speaker_notes: bool
    line_start: int


@dataclass
class ScoreReport:
    total: int = 100
    deductions: list[Deduction] = field(default_factory=list)
    slides: list[SlideInfo] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def deduct(self, rule: str, points: int, detail: str) -> None:
        self.deductions.append(Deduction(rule, points, detail))
        self.total = max(0, self.total - points)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def parse_slides(content: str) -> list[SlideInfo]:
    """Split .qmd content into slides based on level-2 headings and --- separators."""
    lines = content.split("\n")
    slides: list[SlideInfo] = []
    in_frontmatter = False
    frontmatter_count = 0
    in_code_block = False

    current_heading = ""
    current_bullets = 0
    current_notes = False
    current_start = 0
    slide_started = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Track code blocks (skip content inside them)
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Track YAML frontmatter (skip it)
        if stripped == "---" and not slide_started and frontmatter_count < 2:
            frontmatter_count += 1
            if frontmatter_count == 1:
                in_frontmatter = True
                continue
            elif frontmatter_count == 2:
                in_frontmatter = False
                continue
        if in_frontmatter:
            continue

        # Horizontal rule as slide separator
        if stripped == "---" and slide_started:
            # Lookahead: if next non-empty line is a ## heading, the ---
            # is just a visual separator before a new slide, not a slide itself.
            next_is_heading = False
            for j in range(i, len(lines)):  # i is 1-indexed, lines[i] is next line
                next_line = lines[j].strip()
                if next_line:
                    next_is_heading = bool(re.match(r"^##\s+", next_line))
                    break
            if next_is_heading:
                # Save current slide and let the ## heading start the next one
                if slide_started:
                    slides.append(SlideInfo(
                        number=len(slides) + 1,
                        heading=current_heading,
                        bullet_count=current_bullets,
                        has_speaker_notes=current_notes,
                        line_start=current_start,
                    ))
                    slide_started = False
                continue
            slides.append(SlideInfo(
                number=len(slides) + 1,
                heading=current_heading,
                bullet_count=current_bullets,
                has_speaker_notes=current_notes,
                line_start=current_start,
            ))
            current_heading = "(untitled)"
            current_bullets = 0
            current_notes = False
            current_start = i
            slide_started = True
            continue

        # New slide on ## heading
        if re.match(r"^##\s+", stripped):
            if slide_started:
                slides.append(SlideInfo(
                    number=len(slides) + 1,
                    heading=current_heading,
                    bullet_count=current_bullets,
                    has_speaker_notes=current_notes,
                    line_start=current_start,
                ))
            current_heading = re.sub(r"^##\s+", "", stripped).split("{")[0].strip()
            current_heading = re.sub(r"\*\*([^*]+)\*\*", r"\1", current_heading)
            current_bullets = 0
            current_notes = False
            current_start = i
            slide_started = True
            continue

        if not slide_started:
            continue

        # Count bullets
        if re.match(r"^\s*[-*+]\s", stripped):
            current_bullets += 1

        # Check for speaker notes
        if stripped == "::: {.notes}" or stripped == ":::{.notes}":
            current_notes = True

    # Save last slide
    if slide_started:
        slides.append(SlideInfo(
            number=len(slides) + 1,
            heading=current_heading,
            bullet_count=current_bullets,
            has_speaker_notes=current_notes,
            line_start=current_start,
        ))

    return slides


def check_bullet_density(report: ScoreReport) -> None:
    """Penalize slides with too many bullet points."""
    for slide in report.slides:
        excess = slide.bullet_count - MAX_BULLETS_PER_SLIDE
        if excess > 0:
            penalty = min(excess * 2, 6)
            report.deduct(
                "bullet-density",
                penalty,
                f"Slide {slide.number} '{slide.heading}': "
                f"{slide.bullet_count} bullets (max {MAX_BULLETS_PER_SLIDE})",
            )


def check_speaker_notes(report: ScoreReport) -> None:
    """Penalize slides missing speaker notes."""
    missing = [s for s in report.slides if not s.has_speaker_notes]
    if not missing:
        return
    ratio = len(missing) / max(len(report.slides), 1)
    if ratio > 0.5:
        report.deduct("speaker-notes", 15, f"{len(missing)}/{len(report.slides)} slides lack speaker notes")
    elif ratio > 0.2:
        report.deduct("speaker-notes", 8, f"{len(missing)}/{len(report.slides)} slides lack speaker notes")
    elif missing:
        report.deduct("speaker-notes", 3, f"{len(missing)} slide(s) lack speaker notes")
    for s in missing:
        report.warn(f"  No speaker notes: slide {s.number} '{s.heading}' (line {s.line_start})")


def check_slide_count(report: ScoreReport) -> None:
    """Penalize too few or too many slides."""
    n = len(report.slides)
    if n < MIN_SLIDES:
        report.deduct("slide-count", 10, f"Only {n} slides (minimum recommended: {MIN_SLIDES})")
    elif n > MAX_SLIDES:
        report.deduct("slide-count", 5, f"{n} slides (maximum recommended: {MAX_SLIDES})")


def check_heading_hierarchy(content: str, report: ScoreReport) -> None:
    """Check that headings follow a consistent hierarchy."""
    lines = content.split("\n")
    in_frontmatter = False
    fm_count = 0
    in_code_block = False
    heading_levels: list[int] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if stripped == "---":
            fm_count += 1
            if fm_count == 1:
                in_frontmatter = True
            elif fm_count == 2:
                in_frontmatter = False
            continue
        if in_frontmatter:
            continue

        match = re.match(r"^(#{1,6})\s+", stripped)
        if match:
            heading_levels.append(len(match.group(1)))

    for i in range(1, len(heading_levels)):
        if heading_levels[i] > heading_levels[i - 1] + 1:
            report.deduct(
                "heading-hierarchy",
                2,
                f"Heading level skip: h{heading_levels[i - 1]} -> h{heading_levels[i]}",
            )
            break


def check_image_alt_text(content: str, report: ScoreReport) -> None:
    """Check that images have alt text."""
    images = re.findall(r"!\[(.*?)\]\(", content)
    missing_alt = sum(1 for alt in images if not alt.strip())
    if missing_alt:
        report.deduct(
            "image-alt-text",
            min(missing_alt * 3, 10),
            f"{missing_alt} image(s) missing alt text",
        )


def check_anti_patterns(content: str, report: ScoreReport) -> None:
    """Detect inline style overrides and other anti-patterns."""
    font_overrides = ANTI_PATTERN_RE.findall(content)
    if font_overrides:
        report.deduct(
            "anti-pattern:font-override",
            min(len(font_overrides) * 3, 10),
            f"{len(font_overrides)} inline font-size override(s) found",
        )

    smaller_count = len(re.findall(r"\{\.smaller\}", content))
    smallest_count = len(re.findall(r"\{\.smallest\}", content))
    total_small = smaller_count + smallest_count
    if total_small > 5:
        report.deduct(
            "anti-pattern:size-classes",
            min((total_small - 5) * 2, 8),
            f"Excessive size reduction classes: {total_small} uses of .smaller/.smallest",
        )

    # Raw HTML tags outside code blocks
    code_stripped = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    html_tags = re.findall(r"<(?:div|span|p|br|hr|table|tr|td|th)\b", code_stripped)
    if len(html_tags) > 3:
        report.deduct(
            "anti-pattern:raw-html",
            min(len(html_tags) - 3, 8),
            f"{len(html_tags)} raw HTML tags found (prefer Quarto div syntax)",
        )


def extract_frontmatter(content: str) -> str:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    return match.group(1) if match else ""


def parse_theme_values(frontmatter: str) -> list[str]:
    themes: list[str] = []
    for line in frontmatter.splitlines():
        stripped = line.strip()
        if not stripped.startswith("theme:"):
            continue
        value = stripped.split(":", 1)[1].strip()
        if value.startswith("[") and value.endswith("]"):
            candidates = value[1:-1].split(",")
        else:
            candidates = [value]
        for candidate in candidates:
            cleaned = candidate.strip().strip("'\"")
            if cleaned:
                themes.append(cleaned)
    return themes


def iter_slide_blocks(content: str, slides: list[SlideInfo]) -> list[tuple[SlideInfo, str]]:
    lines = content.split("\n")
    blocks: list[tuple[SlideInfo, str]] = []
    for slide in slides:
        start = slide.line_start - 1
        next_starts = [s.line_start - 1 for s in slides if s.line_start > slide.line_start]
        end = next_starts[0] if next_starts else len(lines)
        blocks.append((slide, "\n".join(lines[start:end])))
    return blocks


def count_body_words(slide_text: str) -> int:
    words: list[str] = []
    in_code = False
    in_notes = False
    for raw_line in slide_text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if stripped in {"::: {.notes}", ":::{.notes}"}:
            in_notes = True
            continue
        if in_notes and stripped == ":::":
            in_notes = False
            continue
        if in_notes or stripped.startswith("#") or stripped.startswith(":::") or stripped == "---" or not stripped:
            continue
        # Skip table rows, images, and Quarto attribute blocks
        if re.match(r"^\s*\|", stripped) or stripped.startswith("!") or re.match(r"^\{[.#]", stripped):
            continue
        words.extend(stripped.split())
    return len(words)


def check_llm_bias_patterns(content: str, report: ScoreReport) -> None:
    """Detect the LLM-bias rules added to the governance documents."""
    frontmatter = extract_frontmatter(content)

    themes = parse_theme_values(frontmatter)
    if themes:
        has_custom_override = any(
            theme.endswith(".scss") or theme.endswith(".css") or "/" in theme
            for theme in themes
        )
        if not has_custom_override:
            report.deduct("MAJ-09", 10, f"Default/generic theme without custom override: {', '.join(themes)}")

    title_match = re.search(r"^title\s*:\s*(.+)$", frontmatter, re.MULTILINE)
    if title_match:
        title_value = title_match.group(1).strip().strip("'\"")
        if GENERIC_TITLE_RE.match(title_value):
            report.deduct("MAJ-10", 5, f"Generic placeholder title: {title_value}")

    slide_blocks = iter_slide_blocks(content, report.slides)
    bullet_only_slides = 0
    for slide, slide_text in slide_blocks:
        if slide.bullet_count == 0:
            continue
        stripped = re.sub(r"```.*?```", "", slide_text, flags=re.DOTALL)
        if (
            "!["
            not in stripped
            and ":::" not in stripped
            and "<table" not in stripped.lower()
            and "<img" not in stripped.lower()
        ):
            bullet_only_slides += 1
    if report.slides and bullet_only_slides / len(report.slides) >= 0.7:
        report.deduct(
            "MAJ-11",
            5,
            f"Monotonous structure: {bullet_only_slides}/{len(report.slides)} slides are heading + bullets only",
        )

    for _ in AI_COLOR_RE.finditer(content):
        report.deduct("MIN-08", 2, "AI-style cyan/purple/neon palette value detected")

    for _ in GRADIENT_TEXT_RE.finditer(content):
        report.deduct("MIN-09", 2, "Gradient text styling detected")

    semantic_depth = 0
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped.startswith(":::"):
            continue
        classes = SEMANTIC_BOX_RE.findall(stripped)
        if classes:
            if semantic_depth > 0:
                report.deduct("MIN-10", 2, f"Nested semantic box detected: {classes[0]}")
            semantic_depth += 1
        elif stripped == ":::" and semantic_depth > 0:
            semantic_depth -= 1

    word_counts = [count_body_words(slide_text) for _, slide_text in slide_blocks]
    if len(word_counts) >= 2:
        mean = sum(word_counts) / len(word_counts)
        variance = sum((count - mean) ** 2 for count in word_counts) / len(word_counts)
        stddev = math.sqrt(variance)
        if mean > 0 and stddev > 3 * mean:
            report.deduct("MIN-11", 2, f"Uniform depth violation: stddev {stddev:.1f} exceeds 3x mean {mean:.1f}")


def check_frontmatter(content: str, report: ScoreReport) -> None:
    """Check that YAML frontmatter has required fields."""
    fm = extract_frontmatter(content)
    if not fm:
        report.deduct("frontmatter", 5, "Missing YAML frontmatter")
        return

    required = ["title", "format"]
    for field_name in required:
        if not re.search(rf"^{field_name}\s*:", fm, re.MULTILINE):
            report.deduct("frontmatter", 3, f"Missing frontmatter field: {field_name}")


PURE_BW_RE = re.compile(
    r"""(?:
        \#(?:000000|000|fff|ffffff)  |
        rgb\(\s*0\s*,\s*0\s*,\s*0\s*\)  |
        rgb\(\s*255\s*,\s*255\s*,\s*255\s*\)
    )""",
    re.IGNORECASE | re.VERBOSE,
)


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


def check_pure_bw(content: str, report: ScoreReport) -> None:
    """Detect pure black/white color values (MAJ-05)."""
    # Strip code blocks and frontmatter before scanning
    stripped = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    stripped = re.sub(r"^---\n.*?\n---", "", stripped, flags=re.DOTALL)
    matches = PURE_BW_RE.findall(stripped)
    for match in matches[:5]:  # Cap at 5 reports
        report.deduct("pure-bw", 3, f"Pure black/white color value: {match}")


def check_word_count(content: str, report: ScoreReport) -> None:
    """Check per-slide body text word count (MIN-02: max 40 words)."""
    lines = content.split("\n")
    for slide in report.slides:
        start = slide.line_start - 1  # 0-indexed
        next_starts = [s.line_start - 1 for s in report.slides if s.line_start > slide.line_start]
        end = next_starts[0] if next_starts else len(lines)
        slide_lines = lines[start:end]

        body_words: list[str] = []
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
            # Skip table rows, images, and Quarto attribute blocks
            if re.match(r"^\s*\|", s) or s.startswith("!") or re.match(r"^\{[.#]", s):
                continue
            body_words.extend(s.split())

        word_count = len(body_words)
        if word_count > 40:
            report.deduct(
                "word-count",
                2,
                f"Slide {slide.number} '{slide.heading}': {word_count} words (max 40)",
            )


def score_file(path: Path, verbose: bool = False, skip_render: bool = False) -> ScoreReport:
    """Run all quality checks on a .qmd file."""
    content = path.read_text(encoding="utf-8")
    report = ScoreReport()
    report.slides = parse_slides(content)

    # Compilation check first — if it fails, score is 0
    check_compilation(path, report, skip_render=skip_render)

    check_frontmatter(content, report)
    check_slide_count(report)
    check_bullet_density(report)
    check_speaker_notes(report)
    check_heading_hierarchy(content, report)
    check_image_alt_text(content, report)
    check_anti_patterns(content, report)
    check_llm_bias_patterns(content, report)
    check_pure_bw(content, report)
    check_word_count(content, report)

    return report


def print_report(path: Path, report: ScoreReport, verbose: bool = False) -> None:
    """Print a colorized report to stdout."""
    score = report.total
    if score >= 95:
        color = GREEN
        grade = "A+ Impeccable"
    elif score >= 90:
        color = GREEN
        grade = "A Excellent"
    elif score >= 85:
        color = GREEN
        grade = "B Presentable"
    elif score >= 80:
        color = YELLOW
        grade = "B- Draft"
    elif score >= 60:
        color = YELLOW
        grade = "C Needs Work"
    else:
        color = RED
        grade = "F Failing"

    print()
    print(f"{BOLD}Quality Score: {path.name}{RESET}")
    print("=" * 50)
    print(f"  Slides found: {len(report.slides)}")
    print(f"  Score: {color}{BOLD}{score}/100 ({grade}){RESET}")
    print()

    if report.deductions:
        print(f"{BOLD}Deductions:{RESET}")
        for d in report.deductions:
            print(f"  {RED}-{d.points:>2}{RESET}  [{d.rule}] {d.detail}")
        print()

    if verbose and report.warnings:
        print(f"{BOLD}Warnings:{RESET}")
        for w in report.warnings:
            print(f"  {YELLOW}!{RESET} {w}")
        print()

    if verbose:
        print(f"{BOLD}Slide Summary:{RESET}")
        for s in report.slides:
            notes_icon = f"{GREEN}Y{RESET}" if s.has_speaker_notes else f"{RED}N{RESET}"
            bullet_color = RED if s.bullet_count > MAX_BULLETS_PER_SLIDE else RESET
            print(
                f"  {DIM}{s.number:>2}.{RESET} {s.heading[:40]:<40} "
                f"bullets:{bullet_color}{s.bullet_count}{RESET}  notes:{notes_icon}"
            )
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Score a Quarto presentation for design quality.",
    )
    parser.add_argument("file", type=Path, help="Path to a .qmd file")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed slide-by-slide breakdown",
    )
    parser.add_argument(
        "--no-render",
        action="store_true",
        help="Skip compilation check (quarto render) for faster scoring",
    )
    args = parser.parse_args()

    path: Path = args.file
    if not path.exists():
        print(f"{RED}Error:{RESET} File not found: {path}", file=sys.stderr)
        sys.exit(1)
    if path.suffix != ".qmd":
        print(f"{YELLOW}Warning:{RESET} File does not have .qmd extension: {path}", file=sys.stderr)

    report = score_file(path, verbose=args.verbose, skip_render=args.no_render)
    print_report(path, report, verbose=args.verbose)

    sys.exit(0 if report.total >= 80 else 1)


if __name__ == "__main__":
    main()
