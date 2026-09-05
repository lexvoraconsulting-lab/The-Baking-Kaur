# AI Cake Genome & Vision Pipeline Runner
param (
    [string]$Target = "all"
)

$RepoRoot = Resolve-Path "$PSScriptRoot\..\.."
Set-Location $RepoRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " AI Cake Genome & Vision Pipeline Runner" -ForegroundColor Yellow
Write-Host " Target: $Target" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Cyan

if ($Target -eq "vision" -or $Target -eq "all") {
    Write-Host "`n1. Running Vision Pipeline Test Harness..." -ForegroundColor Yellow
    python -m unittest tbk-spfy-ai/ai/vision/python/test_vision.py
}

if ($Target -eq "taxonomy" -or $Target -eq "all") {
    Write-Host "`n2. Running Taxonomy & Attribute Validation..." -ForegroundColor Yellow
    python -m unittest tbk-spfy-ai/ai/taxonomy/test_taxonomy.py
}

Write-Host "`n✔ AI Pipeline validation completed!" -ForegroundColor Green
