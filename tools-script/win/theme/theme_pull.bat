@echo off
setlocal
cd /d "%~dp0\..\..\.."
title The Baking Kaur -- Pull Theme Code

set "STORE=ae86ba-2a.myshopify.com"
set "THEME_ID=152070258857"

echo ==========================================================
echo  Pulling / Syncing Theme Files from Shopify...
echo  Store: %STORE%
echo  Target Directory: tbk-spfy-theme
echo ==========================================================

set "PYTHON_EXE=F:\frameworks\python\python314\python.exe"
if not exist "%PYTHON_EXE%" set "PYTHON_EXE=python"

"%PYTHON_EXE%" "tools-script\python\theme\theme_manager.py" --pull --store "%STORE%" --theme "%THEME_ID%" %*
if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUCCESS] Theme files synchronized cleanly!
) else (
    echo.
    echo [ERROR] Theme pull encountered an error.
)
if "%TBK_NO_PAUSE%"=="1" goto :end
if "%~1"=="--no-pause" goto :end
echo %cmdcmdline% | findstr /i /c:"%~f0" >nul && pause
:end
endlocal
