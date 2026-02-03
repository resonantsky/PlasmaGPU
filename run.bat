@echo off
REM Consolidated Run Script for PlasmaMandelbrot (Windows CMD)
SETLOCAL

echo --- PlasmaMandelbrot: Smart Launcher ---

REM 1. Check if virtual environment exists
IF NOT EXIST "venv" (
    echo [SETUP] Virtual environment not found. Starting first-time setup...
    python -m venv venv
)

SET PYTHON_EXE=".\venv\Scripts\python.exe"

REM 2. Check if key dependencies are installed
echo [VERIFY] Checking dependencies...
%PYTHON_EXE% -c "import PyQt6; import pyopencl; import glfw; import colorama; print('OK')" > deps_check.tmp 2>nul
set /p CHECK_DEPS=<deps_check.tmp
del deps_check.tmp

IF NOT "%CHECK_DEPS%"=="OK" (
    echo [SETUP] Dependencies missing or broken. Installing/Repairing...
    ".\venv\Scripts\pip.exe" install pyopencl PyQt6 numpy colorama glfw PyOpenGL
) ELSE (
    echo [VERIFY] Environment verified.
)

REM 3. Launch Application
echo [LAUNCH] Starting PlasmaMandelbrot...
%PYTHON_EXE% __main__.py

IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Application exited with error code %ERRORLEVEL%
    pause
)

ENDLOCAL
