@echo off
setlocal
cd /d "%~dp0\..\.."
title The Baking Kaur — Operations Hub

set "PYTHON_EXE=F:\frameworks\Python314\python.exe"
if not exist "%PYTHON_EXE%" (
    where python >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "PYTHON_EXE=python"
    ) else (
        echo [ERROR] Python 3 was not found at F:\frameworks\Python314 or in PATH.
        pause
        exit /b 1
    )
)

"%PYTHON_EXE%" "%~dp0tbk_cli.py" %*
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] CLI exited with code %ERRORLEVEL%.
    pause
)
endlocal
