# Pull / Sync Theme Files from Shopify (#152070258857)
param (
    [string]$ThemeId = "152070258857",
    [string]$Store = "ae86ba-2a.myshopify.com"
)

$RepoRoot = Resolve-Path "$PSScriptRoot\..\..\.."
Set-Location $RepoRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Pulling / Syncing Theme Files from Shopify..." -ForegroundColor Yellow
Write-Host " Target: Theme #$ThemeId on $Store" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Cyan

& "F:\frameworks\python\python314\python.exe" "tools-script\python\theme\theme_manager.py" --pull --store $Store --theme $ThemeId

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✔ Theme files successfully synchronized into tbk-spfy-theme!" -ForegroundColor Green
} else {
    Write-Host "`n✖ Theme pull encountered an error." -ForegroundColor Red
}
