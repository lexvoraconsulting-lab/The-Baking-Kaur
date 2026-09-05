#!/usr/bin/env bash
# ==============================================================================
# The Baking Kaur — Deploy to Preview Theme (macOS / Linux)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

THEME_ID="${THEME_ID:-152070258857}"
STORE="${STORE:-ae86ba-2a.myshopify.com}"

echo "=========================================================="
echo " Deploying Theme Code to Preview Theme..."
echo " Target: Theme #$THEME_ID on $STORE"
echo "=========================================================="

shopify theme push --store "$STORE" --theme "$THEME_ID" --path tbk-spfy-theme --nodelete "$@"

echo ""
echo "✔ Preview theme updated successfully!"
echo "Preview URL: https://$STORE/?preview_theme_id=$THEME_ID"
