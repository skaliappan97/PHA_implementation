#!/bin/bash

# Test script for flow mode
# Make sure to set GOOGLE_API_KEY before running

echo "Testing flow mode..."
echo ""

# Activate virtual environment
source .venv/bin/activate

# Run flow mode test
python main.py flow "will eating protein before sleeping improve my sleep quality?"
