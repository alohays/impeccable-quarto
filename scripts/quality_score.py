#!/usr/bin/env python3
"""Quality scoring tool for Quarto RevealJS presentations.

Analyzes a .qmd file and produces a score out of 100 with deduction breakdown.

Usage:
    python scripts/quality_score.py examples/academic-paper.qmd
    python scripts/quality_score.py --verbose examples/tech-talk.qmd
"""

from __future__ import annotations

import argparse
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
            current_start = 0
            slide_started = False
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
            if not stripped or stripped.startswith(":::"):
                continue
            current_heading = "(untitled)"
            current_bullets = 0
            current_notes = False
            current_start = i
            slide_started = True

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
    """Penalize slides with too many bullet points (MAJ-02)."""
    for slide in report.slides:
        if slide.bullet_count > MAX_BULLETS_PER_SLIDE:
            report.deduct(
                "MAJ-02",
                5,
                f"Slide {slide.number} '{slide.heading}': "
                f"{slide.bullet_count} bullets (max {MAX_BULLETS_PER_SLIDE})",
            )


def check_speaker_notes(report: ScoreReport) -> None:
    """Penalize slides missing speaker notes (MAJ-01)."""
    for slide in report.slides:
        if slide.has_speaker_notes:
            continue
        report.deduct(
            "MAJ-01",
            5,
            f"Slide {slide.number} '{slide.heading}' lacks speaker notes",
        )
        report.warn(f"  No speaker notes: slide {slide.number} '{slide.heading}' (line {slide.line_start})")


def check_slide_count(report: ScoreReport) -> None:
    """Penalize too few or too many slides."""
    n = len(report.slides)
    if n < MIN_SLIDES:
        report.deduct("slide-count", 10, f"Only {n} slides (minimum recommended: {MIN_SLIDES})")
    elif n > MAX_SLIDES:
        report.deduct("slide-count", 5, f"{n} slides (maximum recommended: {MAX_SLIDES})")


def check_heading_hierarchy(content: str, report: ScoreReport) -> None:
    """Check that headings follow a consistent hierarchy (MAJ-06)."""
    lines = content.split("\n")
    in_frontmatter = False
    fm_count = 0
    in_code_block = False
    previous_level: int | None = None

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
            level = len(match.group(1))
            if previous_level is not None and level > previous_level + 1:
                report.deduct(
                    "MAJ-06",
                    3,
                    f"Heading level skip: h{previous_level} -> h{level}",
                )
            previous_level = level


def check_frontmatter(content: str, report: ScoreReport) -> None:
    """Check YAML frontmatter requirements (CRIT-04, MIN-03)."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        report.deduct("CRIT-04", 10, "Missing YAML frontmatter")
        return

    fm = match.group(1)
    if not re.search(r"^date\s*:", fm, re.MULTILINE):
        report.deduct("MIN-03", 1, "Missing frontmatter field: date")


def check_image_alt_text(content: str, report: ScoreReport) -> None:
    """Check that images have alt text (MAJ-04)."""
    images = re.findall(r"!\[(.*?)\]\(", content)
    for index, alt in enumerate(images, 1):
        if alt.strip():
            continue
        report.deduct(
            "MAJ-04",
            5,
            f"Image {index} missing alt text",
        )


def check_anti_patterns(content: str, report: ScoreReport) -> None:
    """Detect inline style overrides and other anti-patterns."""
    font_overrides = ANTI_PATTERN_RE.findall(content)
    for _ in font_overrides:
        report.deduct(
            "MIN-06",
            1,
            "Inline font-size override found",
        )

    smaller_count = len(re.findall(r"\{\.smaller\}", content))
    smallest_count = len(re.findall(r"\{\.smallest\}", content))
    total_small = smaller_count + smallest_count
    if total_small > 5:
        report.warn(
            f"Excessive size reduction classes: {total_small} uses of .smaller/.smallest",
        )

    # Raw HTML tags outside code blocks are noisy but not part of the documented rubric.
    # Keep warning-only so the score remains traceable to quality-gates.md.
    code_stripped = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    html_tags = re.findall(r"<(?:div|span|p|br|hr|table|tr|td|th)\b", code_stripped)
    if len(html_tags) > 3:
        report.warn(f"{len(html_tags)} raw HTML tags found (prefer Quarto div syntax)")


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
    for match in matches[:5]:
        report.deduct("MAJ-05", 3, f"Pure black/white color value: {match}")


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
            body_words.extend(s.split())

        word_count = len(body_words)
        if word_count > 40:
            report.deduct(
                "MIN-02",
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


def score_and_print(path: Path, verbose: bool = False, skip_render: bool = False) -> int:
    """Score one file, print the report, and return the process status code."""
    if not path.exists():
        print(f"{RED}Error:{RESET} File not found: {path}", file=sys.stderr)
        return 1
    if path.suffix != ".qmd":
        print(f"{YELLOW}Warning:{RESET} File does not have .qmd extension: {path}", file=sys.stderr)

    report = score_file(path, verbose=verbose, skip_render=skip_render)
    print_report(path, report, verbose=verbose)
    return 0 if report.total >= 80 else 1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Score a Quarto presentation for design quality.",
    )
    parser.add_argument("file", type=Path, nargs="+", help="Path(s) to .qmd file(s)")
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

    exit_code = 0
    for path in args.file:
        exit_code = max(exit_code, score_and_print(path, verbose=args.verbose, skip_render=args.no_render))

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
