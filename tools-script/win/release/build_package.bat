@echo off
setlocal
cd /d "%~dp0\..\..\.."
title The Baking Kaur -- Build Packager

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

echo ==========================================================
echo  Theme Build Packager (build/vX.Y.Z/)
echo ==========================================================

"%PYTHON_EXE%" "%~dp0\..\..\python\release\build_packager.py" %*
if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUCCESS] Build packaging completed!
) else (
    echo.
    echo [ERROR] Build packaging failed with code %ERRORLEVEL%.
)
if "%TBK_NO_PAUSE%"=="1" goto :end
if "%~1"=="--no-pause" goto :end
echo %cmdcmdline% | findstr /i /c:"%~f0" >nul && pause
:end
endlocal
