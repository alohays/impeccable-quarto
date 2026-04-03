#!/usr/bin/env bash
# Sync the master theme into the Quarto extension directory.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
EXT_DIR="$PROJECT_DIR/_extensions/impeccable-quarto"
SOURCE_THEME="$PROJECT_DIR/themes/impeccable.scss"
TARGET_THEME="$EXT_DIR/impeccable.scss"

mkdir -p "$EXT_DIR"
cp "$SOURCE_THEME" "$TARGET_THEME"

echo "Synced $(basename "$SOURCE_THEME") -> _extensions/impeccable-quarto/"
