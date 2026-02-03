#!/bin/bash
# Launcher script for PlasmaMandelbrot (Unix/Linux/macOS)

if [ ! -d "venv" ]; then
    echo -e "\033[0;31mError: Virtual environment not found. Please run ./install.sh first.\033[0m"
    exit 1
fi

echo -e "\033[0;36mStarting PlasmaMandelbrot...\033[0m"
./venv/bin/python3 __main__.py
