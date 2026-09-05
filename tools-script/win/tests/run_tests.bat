@echo off
setlocal
cd /d "%~dp0\..\..\.."
title The Baking Kaur -- Test Suite

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

set "PYTHONPATH=%CD%;%CD%\tbk-spfy-ai;%CD%\tbk-spfy-seo\ops;%PYTHONPATH%"

echo ==========================================================
echo  Running Full Test Suite (pytest)
echo ==========================================================

"%PYTHON_EXE%" -m pytest %*
if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUCCESS] All test suites passed!
) else (
    echo.
    echo [ERROR] Tests failed with code %ERRORLEVEL%.
)
if "%TBK_NO_PAUSE%"=="1" goto :end
if "%~1"=="--no-pause" goto :end
echo %cmdcmdline% | findstr /i /c:"%~f0" >nul && pause
:end
endlocal
