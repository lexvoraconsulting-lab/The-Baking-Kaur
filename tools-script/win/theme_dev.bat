@echo off
setlocal
cd /d %~dp0\..\..
title The Baking Kaur ? Theme Dev Server

set THEME_ID=151370334377
set STORE=ae86ba-2a.myshopify.com

echo ==========================================================
echo  Starting Shopify Theme Local Development Server...
echo  Store: %STORE%
echo  Theme Directory: tbk-spfy-theme
echo  Local Preview will be at: http://127.0.0.1:9292
echo  (Press Ctrl+C to stop the server when finished)
echo ==========================================================

set "SHOPIFY_CMD=%APPDATA%\npm\shopify.cmd"
if not exist "%SHOPIFY_CMD%" (
    where shopify >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "SHOPIFY_CMD=shopify"
    ) else (
        echo [ERROR] Shopify CLI was not found.
        pause
        exit /b 1
    )
)

call "%SHOPIFY_CMD%" theme dev --store %STORE% --path tbk-spfy-theme %*
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Theme dev server exited with code %ERRORLEVEL%.
    pause
)
endlocal
