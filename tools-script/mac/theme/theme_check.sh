#!/usr/bin/env bash
# ==============================================================================
# The Baking Kaur — Theme Linter & Code Health Check (macOS / Linux)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$REPO_ROOT"

echo "=========================================================="
echo " Running Shopify Theme Check (Linter)..."
echo " Target Directory: tbk-spfy-theme"
echo "=========================================================="

shopify theme check --path tbk-spfy-theme "$@"

