#!/bin/bash
# Install script for PlasmaMandelbrot (Unix/Linux/macOS)
# This script sets up a virtual environment and installs dependencies.

echo -e "\033[0;36m--- Setting up PlasmaMandelbrot Environment ---\033[0m"

# Ensure we are in the project root
if [ ! -f "pyproject.toml" ]; then
    echo -e "\033[0;31mError: Could not find pyproject.toml. Please run this script from the project root.\033[0m"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "\033[0;32mCreating virtual environment...\033[0m"
    python3 -m venv venv
else
    echo -e "\033[0;33mVirtual environment already exists.\033[0m"
fi

# Activate venv and install dependencies
echo -e "\033[0;32mInstalling dependencies...\033[0m"
source venv/bin/activate
pip install pyopencl PyQt6 numpy colorama

echo -e "\n\033[0;36m--- Installation Complete ---\033[0m"
echo "To run the application, use: ./venv/bin/python3 -m __main__"
