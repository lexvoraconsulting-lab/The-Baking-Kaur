@echo off
setlocal
cd /d "%~dp0\..\.."
title The Baking Kaur -- Task Management

set "PYTHON_EXE=F:\frameworks\Python314\python.exe"
if not exist "%PYTHON_EXE%" (
    where python >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "PYTHON_EXE=python"
    ) else (
        echo [ERROR] Python was not found at F:\frameworks\Python314 or in PATH.
        if "%TBK_NO_PAUSE%"=="" pause
        exit /b 1
    )
)

set "PDM_PATH=F:\GitRepos\LXC-AI-Skills\skills\projectops-v2\bin\pdm"

echo ==========================================================
echo  Task Workflow Manager (ProjectOps v2)
echo ==========================================================

if "%~1"=="" (
    echo Active Delivery Plans ^& Task Matrix:
    "%PYTHON_EXE%" "%PDM_PATH%" context check
    echo.
    echo Usage:
    echo   pdm_tasks.bat list
    echo   pdm_tasks.bat start ^<TASK_ID^>
    echo   pdm_tasks.bat complete ^<TASK_ID^>
    if "%TBK_NO_PAUSE%"=="" pause
    exit /b 0
)

if /i "%~1"=="list" (
    "%PYTHON_EXE%" "%PDM_PATH%" context check
) else if /i "%~1"=="start" (
    if "%~2"=="" (
        echo [ERROR] Task ID required. Example: pdm_tasks.bat start HOME-01.01
    ) else (
        "%PYTHON_EXE%" "%PDM_PATH%" worklog start %~2
    )
) else if /i "%~1"=="complete" (
    if "%~2"=="" (
        echo [ERROR] Task ID required. Example: pdm_tasks.bat complete HOME-01.01
    ) else (
        "%PYTHON_EXE%" "%PDM_PATH%" worklog complete %~2
    )
) else (
    "%PYTHON_EXE%" "%PDM_PATH%" %*
)
endlocal
