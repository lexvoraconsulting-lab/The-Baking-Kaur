#!/usr/bin/env bash
# ==============================================================================
# The Baking Kaur — PDM 12-Point Governance Audit (macOS / Linux)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$REPO_ROOT"

PYTHON_BIN="python3"
if ! command -v "$PYTHON_BIN" &> /dev/null; then
    PYTHON_BIN="python"
fi

PDM_BIN="${PDM_BIN:-/usr/local/bin/pdm}"
if [ ! -f "$PDM_BIN" ]; then
    # Fallback to relative repository check
    if [ -f "Support/pdm" ]; then
        PDM_BIN="Support/pdm"
    fi
fi

echo "=========================================================="
echo " Running PDM Conformance Audit on Support/..."
echo "=========================================================="

exec "$PYTHON_BIN" "$PDM_BIN" audit Support "$@"

