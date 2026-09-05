# Safe Guarded Single-File Deploy to Live Theme (#152071602345)
param (
    [Parameter(Mandatory=$true)]
    [string]$File,
    [string]$LiveThemeId = "152071602345",
    [string]$Store = "ae86ba-2a.myshopify.com"
)

$RepoRoot = Resolve-Path "$PSScriptRoot\..\.."
Set-Location $RepoRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " SAFE GUARDED LIVE DEPLOY PROTOCOL" -ForegroundColor Red
Write-Host " Target File: $File" -ForegroundColor Yellow
Write-Host " Live Theme: #$LiveThemeId" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Cyan

# Check if file is protected product page
if ($File -match "product\.json" -or $File -match "main-product-premium-v2\.liquid") {
    Write-Host "🛑 VIOLATION: The product page is a strictly PROTECTED module!" -ForegroundColor Red
    Write-Host "Modifications to $File are forbidden by Support/rules.md." -ForegroundColor Red
    exit 1
}

$tempDir = Join-Path $RepoRoot "temp_diff_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

try {
    Write-Host "1. Pulling live version of $File for divergence check..." -ForegroundColor Yellow
    shopify theme pull --store $Store --theme $LiveThemeId --only $File --path $tempDir --force

    $liveFile = Join-Path $tempDir $File
    $localFile = Join-Path $RepoRoot "tbk-spfy-theme\$File"

    if (Test-Path $liveFile) {
        Write-Host "2. Running differential analysis..." -ForegroundColor Yellow
        $diff = git diff --no-index $liveFile $localFile
        if ($diff) {
            Write-Host "  Changes detected between live and local:" -ForegroundColor Cyan
            $diff | Select-Object -First 20 | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
        } else {
            Write-Host "  ✔ No divergence found. Files are identical." -ForegroundColor Green
        }
    }

    $confirmation = Read-Host "`nDo you confirm pushing '$File' to LIVE THEME #$LiveThemeId? (type YES to proceed)"
    if ($confirmation -eq "YES") {
        Write-Host "3. Pushing verified file to live theme..." -ForegroundColor Yellow
        shopify theme push --store $Store --theme $LiveThemeId --only $File --path tbk-spfy-theme --allow-live --force
        Write-Host "`n✔ Successfully deployed $File to live theme!" -ForegroundColor Green
    } else {
        Write-Host "`nDeployment cancelled by user. Live theme untouched." -ForegroundColor Yellow
    }
} finally {
    if (Test-Path $tempDir) {
        Remove-Item -Recurse -Force $tempDir
    }
}

