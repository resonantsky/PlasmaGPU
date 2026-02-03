# Launcher script for PlasmaMandelbrot (Windows)
$ProjectRoot = Get-Location

if (-not (Test-Path "$ProjectRoot\venv")) {
    Write-Host "Error: Virtual environment not found. Please run ./install.ps1 first." -ForegroundColor Red
    Pause
    exit 1
}

Write-Host "Starting PlasmaMandelbrot..." -ForegroundColor Cyan
& "$ProjectRoot\venv\Scripts\python" __main__.py
