# Theme Development Server Launcher (Intelligent Theme Resolver)
param (
    [string]$ThemeId = "152070258857",
    [string]$Store = "ae86ba-2a.myshopify.com",
    [switch]$Sync,
    [switch]$ListThemes,
    [int]$Port = 9292
)

$RepoRoot = Resolve-Path "$PSScriptRoot\..\..\.."
Set-Location $RepoRoot

$pythonExe = "F:\frameworks\Python314\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonCmd = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($pythonCmd) {
        $pythonExe = $pythonCmd.Source
    } else {
        Write-Host "[ERROR] Python was not found at F:\frameworks\Python314 or in PATH." -ForegroundColor Red
        exit 1
    }
}

$pyArgs = @("$PSScriptRoot\..\..\python\theme\theme_dev_server.py")
if ($ListThemes) {
    $pyArgs += "--list-themes"
} else {
    if ($ThemeId) { $pyArgs += @("--theme", $ThemeId) }
    if ($Sync) { $pyArgs += "--sync" }
    if ($Port) { $pyArgs += @("--port", $Port) }
}
if ($args) { $pyArgs += $args }

& $pythonExe $pyArgs

