# PowerShell Launcher for The Baking Kaur Master Operations CLI
try {
    if ($Host.Name -match "ConsoleHost") {
        $rawUI = $Host.UI.RawUI
        $bufSize = $rawUI.BufferSize
        $bufSize.Width = [Math]::Max($bufSize.Width, 94)
        $rawUI.BufferSize = $bufSize
        $winSize = $rawUI.WindowSize
        $winSize.Width = 94
        $winSize.Height = 44
        $rawUI.WindowSize = $winSize
    }
} catch {}

$pythonExe = "F:\frameworks\python\python314\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonCmd = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($pythonCmd) {
        $pythonExe = $pythonCmd.Source
    } else {
        Write-Host "[ERROR] Python 3 was not found at F:\frameworks\python\python314 or in PATH." -ForegroundColor Red
        exit 1
    }
}

& $pythonExe "$PSScriptRoot\tools-script\python\cli\tbk_cli.py" $args

