#!/usr/bin/env bash
# ==============================================================================
# The Baking Kaur — PDM Task Management Runner (macOS / Linux)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

PYTHON_BIN="python3"
if ! command -v "$PYTHON_BIN" &> /dev/null; then
    PYTHON_BIN="python"
fi

PDM_BIN="${PDM_BIN:-/usr/local/bin/pdm}"

exec "$PYTHON_BIN" "$PDM_BIN" task "$@"
