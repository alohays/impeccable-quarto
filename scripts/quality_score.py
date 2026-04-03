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


def check_frontmatter(content: str, report: ScoreReport) -> None:
    """Check that YAML frontmatter has required fields."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        report.deduct("frontmatter", 5, "Missing YAML frontmatter")
        return

    fm = match.group(1)
    required = ["title", "format"]
    for field_name in required:
        if not re.search(rf"^{field_name}\s*:", fm, re.MULTILINE):
            report.deduct("frontmatter", 3, f"Missing frontmatter field: {field_name}")


def score_file(path: Path, verbose: bool = False) -> ScoreReport:
    """Run all quality checks on a .qmd file."""
    content = path.read_text(encoding="utf-8")
    report = ScoreReport()
    report.slides = parse_slides(content)

    check_frontmatter(content, report)
    check_slide_count(report)
    check_bullet_density(report)
    check_speaker_notes(report)
    check_heading_hierarchy(content, report)
    check_image_alt_text(content, report)
    check_anti_patterns(content, report)

    return report


def print_report(path: Path, report: ScoreReport, verbose: bool = False) -> None:
    """Print a colorized report to stdout."""
    score = report.total
    if score >= 90:
        color = GREEN
        grade = "A"
    elif score >= 80:
        color = GREEN
        grade = "B"
    elif score >= 70:
        color = YELLOW
        grade = "C"
    elif score >= 60:
        color = YELLOW
        grade = "D"
    else:
        color = RED
        grade = "F"

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
    args = parser.parse_args()

    path: Path = args.file
    if not path.exists():
        print(f"{RED}Error:{RESET} File not found: {path}", file=sys.stderr)
        sys.exit(1)
    if path.suffix != ".qmd":
        print(f"{YELLOW}Warning:{RESET} File does not have .qmd extension: {path}", file=sys.stderr)

    report = score_file(path, verbose=args.verbose)
    print_report(path, report, verbose=args.verbose)

    sys.exit(0 if report.total >= 80 else 1)


if __name__ == "__main__":
    main()
