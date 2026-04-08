#!/bin/bash

# Name of the virtual environment directory
VENV_DIR=".venv"

# Ensure script halts on errors
set -e

# Check if the virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating one in '$VENV_DIR'..."
    python3 -m venv "$VENV_DIR"
    
    echo "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
    
    echo "Installing required dependencies..."
    pip install --upgrade pip
    pip install numpy matplotlib scipy
else
    echo "Activating existing virtual environment in '$VENV_DIR'..."
    source "$VENV_DIR/bin/activate"
fi

echo "Starting Cymatic Simulator..."
python3 simulator.py
