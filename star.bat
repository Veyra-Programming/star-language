@echo off
REM =====================================================================
REM Star Programming Language - Windows Enterprise Batch Launcher
REM Architecture: Universal 64-bit and 32-bit (x64 / x86) Compatibility
REM =====================================================================
setlocal enabledelayedexpansion

REM Configure UTF-8 Code Page and Environment
chcp 65001 >nul 2>&1
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

REM 1. Detect System Architecture and Bitness (AMD64, ARM64, x86)
set "STAR_HOST_ARCH=%PROCESSOR_ARCHITECTURE%"
if defined PROCESSOR_ARCHITEW6432 (
    set "STAR_HOST_ARCH=%PROCESSOR_ARCHITEW6432%"
)
if /i "!STAR_HOST_ARCH!"=="AMD64" (
    set "STAR_HOST_BITNESS=64"
) else if /i "!STAR_HOST_ARCH!"=="ARM64" (
    set "STAR_HOST_BITNESS=64"
) else (
    set "STAR_HOST_BITNESS=32"
)

REM 2. Locate star.py Entrypoint Script
set "STAR_PY=%~dp0star.py"
if not exist "!STAR_PY!" (
    if exist "%~dp0..\star.py" (
        set "STAR_PY=%~dp0..\star.py"
    ) else if exist "%~dp0..\..\star.py" (
        set "STAR_PY=%~dp0..\..\star.py"
    )
)

if not exist "!STAR_PY!" (
    echo ============================================================
    echo [ERROR] Star entrypoint script 'star.py' could not be found!
    echo Looked relative to: %~dp0
    echo ============================================================
    exit /b 1
)

REM 3. Custom Override Check
if defined STAR_PYTHON (
    if exist "%STAR_PYTHON%" (
        "%STAR_PYTHON%" "!STAR_PY!" %*
        exit /b !ERRORLEVEL!
    )
)

REM 4. Check Windows 'py' Launcher (Supports 64-bit and 32-bit selection)
py -3 -c "import sys; sys.exit(0)" >nul 2>&1
if !ERRORLEVEL! equ 0 (
    py -3 "!STAR_PY!" %*
    exit /b !ERRORLEVEL!
)

REM 5. Check 'python' directly usable in PATH (ignoring 0-byte Store stubs)
python -c "import sys; sys.exit(0)" >nul 2>&1
if !ERRORLEVEL! equ 0 (
    python "!STAR_PY!" %*
    exit /b !ERRORLEVEL!
)

REM 6. Check User LocalAppData Python Installations (64-bit / 32-bit)
if exist "%APPDATA%\uv\python" (
    for /d %%D in ("%APPDATA%\uv\python\*") do (
        if exist "%%D\python.exe" (
            "%%D\python.exe" "!STAR_PY!" %*
            exit /b !ERRORLEVEL!
        )
    )
)
if exist "%LOCALAPPDATA%\Programs\Haven\python.exe" (
    "%LOCALAPPDATA%\Programs\Haven\python.exe" "!STAR_PY!" %*
    exit /b !ERRORLEVEL!
)
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" "!STAR_PY!" %*
    exit /b !ERRORLEVEL!
)
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" "!STAR_PY!" %*
    exit /b !ERRORLEVEL!
)
if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" "!STAR_PY!" %*
    exit /b !ERRORLEVEL!
)
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" "!STAR_PY!" %*
        exit /b !ERRORLEVEL!
    )
)

REM 7. Check 64-bit Program Files Python Installations
for /d %%D in ("%ProgramFiles%\Python3*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" "!STAR_PY!" %*
        exit /b !ERRORLEVEL!
    )
)

REM 8. Check 32-bit Program Files (x86) Python Installations
if defined ProgramFiles(x86) (
    for /d %%D in ("%ProgramFiles(x86)%\Python3*") do (
        if exist "%%D\python.exe" (
            "%%D\python.exe" "!STAR_PY!" %*
            exit /b !ERRORLEVEL!
        )
    )
)

REM 9. Check Root C:\Python3* Installations
for /d %%D in ("C:\Python3*") do (
    if exist "%%D\python.exe" (
        "%%D\python.exe" "!STAR_PY!" %*
        exit /b !ERRORLEVEL!
    )
)

REM 10. Check Anaconda / Miniconda in UserProfile
if exist "%USERPROFILE%\anaconda3\python.exe" (
    "%USERPROFILE%\anaconda3\python.exe" "!STAR_PY!" %*
    exit /b !ERRORLEVEL!
)
if exist "%USERPROFILE%\miniconda3\python.exe" (
    "%USERPROFILE%\miniconda3\python.exe" "!STAR_PY!" %*
    exit /b !ERRORLEVEL!
)

REM 11. Diagnostic Banner If No Runtime Found
echo ============================================================
echo [ERROR] No compatible 64-bit or 32-bit Python 3.10+ runtime found!
echo Host Architecture: !STAR_HOST_ARCH! (!STAR_HOST_BITNESS!-bit)
echo.
echo Please install Python using Windows Package Manager:
echo   winget install Python.Python.3.12
echo.
echo Or download from: https://www.python.org/downloads/
echo ============================================================
exit /b 1
