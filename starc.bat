@echo off
:: Star Compiler (starc) Windows Batch Launcher
call "%~dp0star.bat" compile %*
exit /b %ERRORLEVEL%
