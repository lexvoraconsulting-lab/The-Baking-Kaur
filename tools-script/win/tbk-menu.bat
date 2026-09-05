@echo off
setlocal
cd /d "%~dp0\..\.."
title The Baking Kaur — Operations Hub

where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python 3 was not found in PATH. Please install or add Python to PATH.
    pause
    exit /b 1
)

python "%~dp0tbk_cli.py" %*
endlocal
