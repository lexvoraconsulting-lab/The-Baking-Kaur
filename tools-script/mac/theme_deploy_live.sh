#!/usr/bin/env bash
# ==============================================================================
# The Baking Kaur — Guarded Single-File Live Deploy (macOS / Linux)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

LIVE_THEME_ID="${LIVE_THEME_ID:-152071602345}"
STORE="${STORE:-ae86ba-2a.myshopify.com}"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <path-to-file-relative-to-theme>"
    echo "Example: $0 sections/hero-image.liquid"
    exit 1
fi

FILE_PATH="$1"

# Invariant check: product page protected module
if [[ "$FILE_PATH" =~ product\.json|main-product-premium-v2\.liquid ]]; then
    echo "🛑 VIOLATION: The product page is a strictly PROTECTED module!" >&2
    echo "Modifications to $FILE_PATH are strictly forbidden by Support/rules.md." >&2
    exit 1
fi

echo "=========================================================="
echo " SURGICAL LIVE DEPLOY (RULE 5.3 PROTOCOL)"
echo " Target File: $FILE_PATH"
echo " Target Store: $STORE (Theme #$LIVE_THEME_ID)"
echo "=========================================================="
echo ""

read -rp "Are you sure you want to push directly to LIVE THEME? [y/N]: " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi

shopify theme push --store "$STORE" --theme "$LIVE_THEME_ID" --path tbk-spfy-theme --only "$FILE_PATH" --nodelete --allow-live
echo ""
echo "✔ Successfully deployed $FILE_PATH to Live Theme #$LIVE_THEME_ID!"
