@echo off
setlocal
cd /d "%~dp0\..\.."
title The Baking Kaur -- Surgical Live Theme Deploy

set "LIVE_THEME_ID=152071602345"
set "STORE=ae86ba-2a.myshopify.com"

if "%~1"=="" (
    echo [USAGE] theme_deploy_live.bat ^<path-to-file-relative-to-theme^>
    echo Example: theme_deploy_live.bat sections/hero-image.liquid
    if "%TBK_NO_PAUSE%"=="" pause
    exit /b 1
)

set "FILE_PATH=%~1"

echo ==========================================================
echo  SURGICAL LIVE DEPLOY (RULE 5.3 PROTOCOL)
echo  Target File: %FILE_PATH%
echo  Target Store: %STORE% (Theme #%LIVE_THEME_ID%)
echo ==========================================================
echo.
set /p "CONFIRM=Are you sure you want to push directly to LIVE THEME? [y/N]: "
if /i not "%CONFIRM%"=="y" (
    echo Deployment cancelled.
    if "%TBK_NO_PAUSE%"=="" pause
    exit /b 0
)

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

call "%SHOPIFY_CMD%" theme push --theme %LIVE_THEME_ID% --store %STORE% --only %FILE_PATH% --path tbk-spfy-theme --allow-live --force
if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUCCESS] File pushed to live theme!
    echo Live Verification URL: https://%STORE%/%FILE_PATH%?preview_theme_id=%LIVE_THEME_ID%
) else (
    echo.
    echo [ERROR] Live deployment failed with code %ERRORLEVEL%.
)
if "%TBK_NO_PAUSE%"=="1" goto :end
if "%~1"=="--no-pause" goto :end
echo %cmdcmdline% | findstr /i /c:"%~f0" >nul && pause
:end
endlocal
