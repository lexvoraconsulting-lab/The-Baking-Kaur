@echo off
setlocal
cd /d "%~dp0\..\..\.."
title The Baking Kaur -- Theme Dev Server

set "PYTHON_EXE=F:\frameworks\python\python314\python.exe"
if not exist "%PYTHON_EXE%" (
    where python >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "PYTHON_EXE=python"
    ) else (
        echo [ERROR] Python was not found at F:\frameworks\python\python314 or in PATH.
        if "%TBK_NO_PAUSE%"=="" pause
        exit /b 1
    )
)

"%PYTHON_EXE%" "%~dp0\..\..\python\theme\theme_dev_server.py" %*
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Theme dev server exited with code %ERRORLEVEL%.
    if "%TBK_NO_PAUSE%"=="" pause
)
endlocal
