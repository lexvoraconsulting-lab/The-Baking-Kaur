@echo off
@chcp 65001 >nul
setlocal
cd /d "%~dp0"
call "%~dp0tools-script\win\tbk-menu.bat" %*
endlocal

