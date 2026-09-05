#!/usr/bin/env bash
# ==============================================================================
# The Baking Kaur — AI Vision Engine & Cake Genome Pipeline (macOS / Linux)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

PYTHON_BIN="python3"
if ! command -v "$PYTHON_BIN" &> /dev/null; then
    PYTHON_BIN="python"
fi

export PYTHONPATH="$REPO_ROOT:$REPO_ROOT/tbk-spfy-ai:${PYTHONPATH:-}"

echo "=========================================================="
echo " The Baking Kaur — AI Vision & Cake Genome Engine"
echo "=========================================================="

exec "$PYTHON_BIN" tbk-spfy-ai/ai/vision/python/main.py "$@"
