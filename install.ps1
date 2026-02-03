# Install script for PlasmaMandelbrot (Windows)
# This script sets up a virtual environment and installs dependencies.

Write-Host "--- Setting up PlasmaMandelbrot Environment ---" -ForegroundColor Cyan

# Ensure we are in the project root
$ProjectRoot = Get-Location
if (-not (Test-Path "$ProjectRoot\pyproject.toml")) {
    Write-Error "Could not find pyproject.toml. Please run this script from the project root."
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "$ProjectRoot\venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Green
    python -m venv venv
} else {
    Write-Host "Virtual environment already exists." -ForegroundColor Yellow
}

# Activate venv and install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Green
& "$ProjectRoot\venv\Scripts\pip" install pyopencl PyQt5 numpy

Write-Host "`n--- Installation Complete ---" -ForegroundColor Cyan
Write-Host "To run the application, use: .\venv\Scripts\python -m PlasmaMandelbrot"
