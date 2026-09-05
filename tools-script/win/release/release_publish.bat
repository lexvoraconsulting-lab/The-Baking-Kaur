@echo off
setlocal
cd /d "%~dp0\..\..\.."
title The Baking Kaur -- Release Manager

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

echo ==========================================================
echo  Release Manager (releases/v[Major]/v[Minor]/)
echo ==========================================================

"%PYTHON_EXE%" "%~dp0\..\..\python\release\release_manager.py" %*
if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUCCESS] Release published successfully!
) else (
    echo.
    echo [ERROR] Release failed with code %ERRORLEVEL%.
)
if "%TBK_NO_PAUSE%"=="1" goto :end
if "%~1"=="--no-pause" goto :end
echo %cmdcmdline% | findstr /i /c:"%~f0" >nul && pause
:end
endlocal
