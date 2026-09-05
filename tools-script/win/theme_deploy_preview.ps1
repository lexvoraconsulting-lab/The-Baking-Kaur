# Deploy Changes to Preview Theme (#151370334377)
param (
    [string]$ThemeId = "151370334377",
    [string]$Store = "ae86ba-2a.myshopify.com"
)

$RepoRoot = Resolve-Path "$PSScriptRoot\..\.."
Set-Location $RepoRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Deploying to Preview Theme..." -ForegroundColor Yellow
Write-Host " Target: Theme #$ThemeId on $Store" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Cyan

shopify theme push --store $Store --theme $ThemeId --path tbk-spfy-theme

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✔ Preview theme successfully updated!" -ForegroundColor Green
    Write-Host "🔗 View preview at: https://$Store/?preview_theme_id=$ThemeId" -ForegroundColor Cyan
} else {
    Write-Host "`n✖ Push to preview theme encountered an error." -ForegroundColor Red
}

