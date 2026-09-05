# Task Management Workflow Runner (ProjectOps v2)
param (
    [string]$Action = "list",
    [string]$TaskId = ""
)

$RepoRoot = Resolve-Path "$PSScriptRoot\..\..\.."
Set-Location $RepoRoot
$pdmPath = "F:\GitRepos\LXC-AI-Skills\skills\projectops-v2\bin\pdm"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Task Workflow Manager (ProjectOps v2)" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

if ($Action -eq "list") {
    Write-Host "Active Delivery Plans & Task Matrix:" -ForegroundColor Yellow
    python $pdmPath context check
} elseif ($Action -eq "start") {
    if (-not $TaskId) {
        $TaskId = Read-Host "Enter Task ID to start (e.g. SLOT-01.01, HOME-01.01)"
    }
    if ($TaskId) {
        Write-Host "Starting task: $TaskId..." -ForegroundColor Yellow
        python $pdmPath worklog start $TaskId
        Write-Host "`n✔ Task $TaskId set to IN PROGRESS [~]" -ForegroundColor Green
    }
} elseif ($Action -eq "complete") {
    if (-not $TaskId) {
        $TaskId = Read-Host "Enter Task ID to complete (e.g. SLOT-01.01, HOME-01.01)"
    }
    if ($TaskId) {
        Write-Host "Completing task: $TaskId..." -ForegroundColor Yellow
        python $pdmPath worklog complete $TaskId
        Write-Host "`n✔ Task $TaskId marked COMPLETED [x]" -ForegroundColor Green
    }
}

