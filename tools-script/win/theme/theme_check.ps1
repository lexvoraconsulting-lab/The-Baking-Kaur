# Shopify Theme Code Health & Linter Check
$RepoRoot = Resolve-Path "$PSScriptRoot\..\..\.."
Set-Location $RepoRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Running Shopify Theme Linter Check..." -ForegroundColor Yellow
Write-Host " Target Directory: tbk-spfy-theme" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Cyan

if (-not (Test-Path "tbk-spfy-theme\layout\theme.liquid")) {
    Write-Host "[NOTICE] Theme directory requires verification. Running pre-flight self-healing..." -ForegroundColor Yellow
    & "F:\frameworks\python\python314\python.exe" "tools-script\python\theme\theme_manager.py"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Theme directory verification cancelled or failed." -ForegroundColor Red
        return
    }
}

$output = shopify theme check --path tbk-spfy-theme 2>&1

$hasErrors = $false
foreach ($line in $output) {
    if ($line -match "error" -or $line -match "failure") {
        Write-Host "  $line" -ForegroundColor Red
        $hasErrors = $true
    } elseif ($line -match "warning") {
        Write-Host "  $line" -ForegroundColor Yellow
    } elseif ($line -match "files inspected" -or $line -match "suggestions") {
        Write-Host "  $line" -ForegroundColor Green
    }
}

if (-not $hasErrors) {
    Write-Host "`n✔ Theme code health check completed cleanly!" -ForegroundColor Green
} else {
    Write-Host "`n⚠ Linter reported issues above." -ForegroundColor Yellow
}

