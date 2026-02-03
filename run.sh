#!/bin/bash
# Consolidated Run Script for PlasmaMandelbrot (Unix/Linux/macOS)

echo -e "\033[0;36m--- PlasmaMandelbrot: Smart Launcher ---\033[0m"

# 1. Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "\033[0;33m>> Virtual environment not found. Starting first-time setup...\033[0m"
    python3 -m venv venv
fi

PYTHON_BIN="./venv/bin/python3"

# 2. Check if key dependencies are installed
echo -e "\033[0;90m>> Verifying dependencies...\033[0m"
CHECK_DEPS=$($PYTHON_BIN -c "import PyQt6; import pyopencl; import glfw; import colorama; print('OK')" 2>/dev/null)

if [ "$CHECK_DEPS" != "OK" ]; then
    echo -e "\033[0;33m>> Dependencies missing or broken. Installing/Repairing...\033[0m"
    ./venv/bin/pip install pyopencl PyQt6 numpy colorama glfw PyOpenGL
else
    echo -e "\033[0;32m>> Environment verified.\033[0m"
fi

# 3. Launch Application
echo -e "\033[0;36m>> Launching PlasmaMandelbrot...\033[0m"
$PYTHON_BIN __main__.py
