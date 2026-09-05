# Shopify Admin GraphQL Automation Runner
param (
    [string]$Operation = "snippets",
    [switch]$Apply
)

$RepoRoot = Resolve-Path "$PSScriptRoot\..\.."
Set-Location $RepoRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Shopify Admin GraphQL Operations Runner" -ForegroundColor Yellow
Write-Host " Store: ae86ba-2a.myshopify.com" -ForegroundColor Gray
Write-Host " Mode: $(if ($Apply) { 'APPLY (Live Store Changes)' } else { 'DRY-RUN (Preview Only)' })" -ForegroundColor $(if ($Apply) { 'Red' } else { 'Green' })
Write-Host "==========================================================" -ForegroundColor Cyan

$scriptMap = @{
    "snippets" = "tbk-spfy-seo\ops\fix_seo_snippets.py"
    "handles" = "tbk-spfy-seo\ops\fix_product_handles.py"
    "mojibake" = "tbk-spfy-seo\ops\fix_mojibake.py"
    "occasion" = "tbk-spfy-seo\ops\fix_description_occasion.py"
    "redirects" = "tbk-spfy-seo\ops\repoint_redirects.py"
}

$targetScript = $scriptMap[$Operation]
if (-not $targetScript) {
    Write-Host "Unknown operation: $Operation. Available: snippets, handles, mojibake, occasion, redirects" -ForegroundColor Red
    exit 1
}

$modeArg = if ($Apply) { "--apply" } else { "--dry-run" }

Write-Host "Running: python $targetScript $modeArg..." -ForegroundColor Yellow
python $targetScript $modeArg

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✔ Operation completed successfully!" -ForegroundColor Green
} else {
    Write-Host "`n✖ Operation encountered an error." -ForegroundColor Red
}
