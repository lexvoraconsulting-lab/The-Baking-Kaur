# PowerShell Launcher for The Baking Kaur Master Operations CLI
$pythonExe = "F:\frameworks\Python314\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonCmd = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($pythonCmd) {
        $pythonExe = $pythonCmd.Source
    } else {
        Write-Host "[ERROR] Python 3 was not found at F:\frameworks\Python314 or in PATH." -ForegroundColor Red
        exit 1
    }
}

& $pythonExe "$PSScriptRoot\tools-script\python\tbk_cli.py" $args

