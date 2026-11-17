@echo off
:: Star Runtime VM (star-runtime) Windows Batch Launcher
call "%~dp0star.bat" run %*
exit /b %ERRORLEVEL%
