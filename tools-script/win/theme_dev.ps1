# Theme Development Server Launcher
param (
    [string]$ThemeId = "151370334377",
    [string]$Store = "ae86ba-2a.myshopify.com"
)

$RepoRoot = Resolve-Path "$PSScriptRoot\..\.."
Set-Location $RepoRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Starting Shopify Theme Local Development Server..." -ForegroundColor Yellow
Write-Host " Target Preview Theme: #$ThemeId on $Store" -ForegroundColor Gray
Write-Host " Theme Directory: tbk-spfy-theme" -ForegroundColor Gray
Write-Host " Local Preview will be available at: http://127.0.0.1:9292" -ForegroundColor Green
Write-Host " (Press Ctrl+C to stop the server when finished)" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Cyan

shopify theme dev --store $Store --theme $ThemeId --path tbk-spfy-theme

