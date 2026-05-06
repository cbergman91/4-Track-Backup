#!/bin/bash

# Run this from the repository root or via the autostart desktop entry.
cd "$(dirname "$0")"
source ./venv/bin/activate
python main.py
