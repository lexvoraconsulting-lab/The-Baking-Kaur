#!/usr/bin/env bash
# ==============================================================================
# The Baking Kaur — SEO Operations Runner (macOS / Linux)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$REPO_ROOT"

PYTHON_BIN="python3"
if ! command -v "$PYTHON_BIN" &> /dev/null; then
    PYTHON_BIN="python"
fi

export PYTHONPATH="$REPO_ROOT:$REPO_ROOT/tbk-spfy-seo/ops:${PYTHONPATH:-}"

echo "=========================================================="
echo " The Baking Kaur — SEO Intelligence & Metafield Operations"
echo "=========================================================="

exec "$PYTHON_BIN" tbk-spfy-seo/ops/apply_seo_fixes.py "$@"

