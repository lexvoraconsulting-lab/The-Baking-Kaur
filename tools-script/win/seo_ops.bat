@echo off
setlocal
cd /d "%~dp0\..\.."
title The Baking Kaur -- SEO Operations

set "PYTHON_EXE=F:\frameworks\Python314\python.exe"
if not exist "%PYTHON_EXE%" (
    where python >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "PYTHON_EXE=python"
    ) else (
        echo [ERROR] Python was not found.
        if "%TBK_NO_PAUSE%"=="" pause
        exit /b 1
    )
)

set "PYTHONPATH=%CD%;%CD%\tbk-spfy-seo\ops;%PYTHONPATH%"

echo ==========================================================
echo  Shopify SEO Automation Runner
echo ==========================================================

set "TARGET_SCRIPT=tbk-spfy-seo\ops\fix_seo_snippets.py"
set "MODE=--dry-run"

if /i "%~1"=="apply" set "MODE=--apply"

echo Running: "%PYTHON_EXE%" %TARGET_SCRIPT% %MODE%
"%PYTHON_EXE%" %TARGET_SCRIPT% %MODE%
if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUCCESS] SEO operation completed cleanly!
) else (
    echo.
    echo [ERROR] SEO operation failed with code %ERRORLEVEL%.
)
if "%TBK_NO_PAUSE%"=="1" goto :end
if "%~1"=="--no-pause" goto :end
echo %cmdcmdline% | findstr /i /c:"%~f0" >nul && pause
:end
endlocal
