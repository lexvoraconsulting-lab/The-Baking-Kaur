#!/usr/bin/env bash
# ==============================================================================
# The Baking Kaur — Master Operations CLI Launcher (macOS / Linux)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

PYTHON_BIN="python3"
if ! command -v "$PYTHON_BIN" &> /dev/null; then
    if command -v python &> /dev/null; then
        PYTHON_BIN="python"
    else
        echo "Error: Python 3 not found in PATH." >&2
        exit 1
    fi
fi

exec "$PYTHON_BIN" "$SCRIPT_DIR/../python/tbk_cli.py" "$@"
