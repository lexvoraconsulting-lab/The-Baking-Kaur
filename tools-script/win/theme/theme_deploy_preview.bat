@echo off
setlocal
cd /d "%~dp0\..\..\.."
title The Baking Kaur -- Deploy Preview Theme

set "THEME_ID=152070258857"
set "STORE=ae86ba-2a.myshopify.com"

echo ==========================================================
echo  Deploying Theme Code to Preview Theme...
echo  Target: Theme #%THEME_ID% on %STORE%
echo ==========================================================

set "SHOPIFY_CMD=F:\frameworks\nodejs\npm-global\shopify.cmd"
if not exist "%SHOPIFY_CMD%" set "SHOPIFY_CMD=%APPDATA%\npm\shopify.cmd"
if not exist "%SHOPIFY_CMD%" (
    where shopify >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "SHOPIFY_CMD=shopify"
    ) else (
        echo [ERROR] Shopify CLI was not found at F:\frameworks\nodejs\npm-global or in PATH.
        if "%TBK_NO_PAUSE%"=="" pause
        exit /b 1
    )
)

if not exist "tbk-spfy-theme\layout\theme.liquid" (
    echo [NOTICE] Theme directory requires verification. Running pre-flight self-healing...
    F:\frameworks\python\python314\python.exe tools-script\python\theme\theme_manager.py
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Theme directory verification cancelled or failed.
        if "%TBK_NO_PAUSE%"=="" pause
        exit /b 1
    )
)

call "%SHOPIFY_CMD%" theme push --store %STORE% --theme %THEME_ID% --path tbk-spfy-theme %*
if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUCCESS] Preview theme updated successfully!
    echo Preview URL: https://%STORE%/?preview_theme_id=%THEME_ID%
) else (
    echo.
    echo [ERROR] Deployment to preview theme failed with code %ERRORLEVEL%.
)
if "%TBK_NO_PAUSE%"=="1" goto :end
if "%~1"=="--no-pause" goto :end
echo %cmdcmdline% | findstr /i /c:"%~f0" >nul && pause
:end
endlocal
