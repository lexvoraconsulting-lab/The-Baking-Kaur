@echo off
setlocal
cd /d "%~dp0\..\..\.."
title The Baking Kaur -- AI Vision Pipeline

set "PYTHON_EXE=F:\frameworks\python\python314\python.exe"
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

set "PYTHONPATH=%CD%;%CD%\tbk-spfy-ai;%PYTHONPATH%"

echo ==========================================================
echo  AI Cake Genome ^& Vision Pipeline Runner
echo ==========================================================

echo 1. Testing AI Vision Pipeline...
"%PYTHON_EXE%" -m pytest tbk-spfy-ai/ai/vision/python/test_config_providers.py -q
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Vision pipeline test failed.
    if "%TBK_NO_PAUSE%"=="" pause
    exit /b %ERRORLEVEL%
)

echo.
echo 2. Testing Taxonomy ^& Attribute Validation...
"%PYTHON_EXE%" -m pytest tbk-spfy-ai/ai/taxonomy/test_taxonomy.py -q
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Taxonomy test failed.
    if "%TBK_NO_PAUSE%"=="" pause
    exit /b %ERRORLEVEL%
)

echo.
echo [SUCCESS] All AI Genome ^& Vision tests passed!
if "%TBK_NO_PAUSE%"=="1" goto :end
if "%~1"=="--no-pause" goto :end
echo %cmdcmdline% | findstr /i /c:"%~f0" >nul && pause
:end
endlocal
