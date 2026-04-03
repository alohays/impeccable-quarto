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
