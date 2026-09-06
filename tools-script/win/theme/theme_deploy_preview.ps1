# Deploy Changes to Preview Theme (#152070258857)
param (
    [string]$ThemeId = "152070258857",
    [string]$Store = "ae86ba-2a.myshopify.com"
)

$RepoRoot = Resolve-Path "$PSScriptRoot\..\..\.."
Set-Location $RepoRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Deploying to Preview Theme..." -ForegroundColor Yellow
Write-Host " Target: Theme #$ThemeId on $Store" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Cyan

if (-not (Test-Path "tbk-spfy-theme\layout\theme.liquid")) {
    Write-Host "[NOTICE] Theme directory requires verification. Running pre-flight self-healing..." -ForegroundColor Yellow
    & "F:\frameworks\python\python314\python.exe" "tools-script\python\theme\theme_manager.py"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Theme directory verification cancelled or failed." -ForegroundColor Red
        return
    }
}
$shopifyCmd = "F:\frameworks\nodejs\npm-global\shopify.cmd"
if (-not (Test-Path $shopifyCmd)) {
    $shopifyCmd = "shopify"
}

& $shopifyCmd theme push --store $Store --theme $ThemeId --path tbk-spfy-theme

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✔ Preview theme successfully updated!" -ForegroundColor Green
    Write-Host "🔗 View preview at: https://$Store/?preview_theme_id=$ThemeId" -ForegroundColor Cyan
} else {
    Write-Host "`n✖ Push to preview theme encountered an error." -ForegroundColor Red
}

