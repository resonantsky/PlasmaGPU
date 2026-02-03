@echo off
REM Launcher script for PlasmaMandelbrot (Windows CMD)
SETLOCAL

IF NOT EXIST "venv" (
    echo [ERROR] Virtual environment not found.
    echo Please run ./install.ps1 first to set up the environment.
    pause
    exit /b 1
)

echo Starting PlasmaMandelbrot...
".\venv\Scripts\python.exe" __main__.py

IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Application exited with error code %ERRORLEVEL%
    pause
)

ENDLOCAL
