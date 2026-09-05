@echo off
setlocal
cd /d "%~dp0\..\.."
title The Baking Kaur -- Theme Health Check

echo ==========================================================
echo  Running Shopify Theme Linter Check...
echo  Target Directory: tbk-spfy-theme
echo ==========================================================

set "SHOPIFY_CMD=%APPDATA%\npm\shopify.cmd"
if not exist "%SHOPIFY_CMD%" (
    where shopify >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "SHOPIFY_CMD=shopify"
    ) else (
        echo [ERROR] Shopify CLI was not found.
        if "%TBK_NO_PAUSE%"=="" pause
        exit /b 1
    )
)

call "%SHOPIFY_CMD%" theme check tbk-spfy-theme %*
if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUCCESS] Theme check completed cleanly!
) else (
    echo.
    echo [WARNING] Theme check reported warnings or errors.
)
if "%TBK_NO_PAUSE%"=="1" goto :end
if "%~1"=="--no-pause" goto :end
echo %cmdcmdline% | findstr /i /c:"%~f0" >nul && pause
:end
endlocal
