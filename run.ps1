# Consolidated Run Script for PlasmaMandelbrot (Windows PowerShell)
Write-Host "--- PlasmaMandelbrot: Smart Launcher ---" -ForegroundColor Cyan

$ProjectRoot = Get-Location
$VenvPath = "$ProjectRoot\venv"
$PythonPath = "$VenvPath\Scripts\python.exe"

# 1. Check if virtual environment exists
if (-not (Test-Path $VenvPath)) {
    Write-Host ">> Virtual environment not found. Starting first-time setup..." -ForegroundColor Yellow
    python -m venv venv
}

# 2. Check if key dependencies are installed (using PyQt6 as a proxy)
Write-Host ">> Verifying dependencies..." -ForegroundColor Gray
$CheckPyQt = & $PythonPath -c "import PyQt6; import pyopencl; import glfw; import colorama; print('OK')" 2>$null

if ($CheckPyQt -ne "OK") {
    Write-Host ">> Dependencies missing or broken. Installing/Repairing..." -ForegroundColor Yellow
    & "$VenvPath\Scripts\pip" install pyopencl PyQt6 numpy colorama glfw PyOpenGL
} else {
    Write-Host ">> Environment verified." -ForegroundColor Green
}

# 3. Launch Application
Write-Host ">> Launching PlasmaMandelbrot..." -ForegroundColor Cyan
& $PythonPath __main__.py
