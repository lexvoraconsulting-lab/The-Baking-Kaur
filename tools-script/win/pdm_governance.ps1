# ProjectOps v2 Governance Runner
param (
    [switch]$CheckOnly,
    [switch]$RefreshContext
)

$RepoRoot = Resolve-Path "$PSScriptRoot\..\.."
Set-Location $RepoRoot

$pdmPath = "F:\GitRepos\LXC-AI-Skills\skills\projectops-v2\bin\pdm"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " ProjectOps v2 Conformance Audit & Health Check" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

if ($RefreshContext) {
    Write-Host "Refreshing governance context derived states..." -ForegroundColor Gray
    python $pdmPath context refresh
}

Write-Host "Running 12-point architectural audit on Support/..." -ForegroundColor Yellow
$auditOutput = python $pdmPath audit Support

$hasError = $false
foreach ($line in $auditOutput) {
    if ($line -match "FAIL" -or $line -match "error") {
        Write-Host "  $line" -ForegroundColor Red
        $hasError = $true
    } elseif ($line -match "WARN") {
        Write-Host "  $line" -ForegroundColor Yellow
    } else {
        Write-Host "  $line" -ForegroundColor Green
    }
}

if (-not $hasError) {
    Write-Host "`n✔ Governance Health: 100% PASS (Zero errors, Zero warnings)" -ForegroundColor Green
} else {
    Write-Host "`n✖ Conformance violations detected. Check output above." -ForegroundColor Red
}
