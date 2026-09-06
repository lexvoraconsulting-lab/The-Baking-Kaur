@echo off
setlocal
cd /d "%~dp0\..\..\.."
title The Baking Kaur -- ProjectOps v2 Governance

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

set "PDM_PATH=F:\GitRepos\LXC-AI-Skills\skills\projectops-v2\bin\pdm"

echo ==========================================================
echo  ProjectOps v2 Conformance Audit ^& Health Check
echo  Repository Root: %CD%
echo ==========================================================

echo.
echo Running 12-point architectural audit on Support/...
"%PYTHON_EXE%" "%PDM_PATH%" audit Support %*
if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUCCESS] Governance Health: 100 Percent PASS - Zero errors, Zero warnings
) else (
    echo.
    echo [ERROR] Governance audit failed with code %ERRORLEVEL%.
)
if "%TBK_NO_PAUSE%"=="1" goto :end
if "%~1"=="--no-pause" goto :end
echo %cmdcmdline% | findstr /i /c:"%~f0" >nul && pause
:end
endlocal
