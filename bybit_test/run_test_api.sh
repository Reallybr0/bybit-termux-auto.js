#!/bin/bash

# Bybit API Test Script Runner
# This script runs the Bybit API connection test

echo "========================================="
echo "  Bybit API Connection Test"
echo "========================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Navigate to script directory
cd "$SCRIPT_DIR"

# Check if .env file exists in project root
ENV_PATH="../../../.env"
if [ ! -f "$ENV_PATH" ]; then
    echo " WARNING: .env file not found at $ENV_PATH"
    echo "   Make sure your .env file exists in the project root."
    echo "   Required variables: BYBIT_API_KEY, BYBIT_API_SECRET, BYBIT_TESTNET"
    echo ""
fi

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo " ERROR: Python3 is not installed!"
    echo "   Please install Python3 and try again."
    exit 1
fi

# Check if required packages are installed
echo " Checking Python packages..."
python3 -c "import dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo " WARNING: python-dotenv not installed. Installing..."
    pip install python-dotenv
fi

python3 -c "import pybit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo " WARNING: pybit not installed. Installing..."
    pip install pybit
fi

echo ""
echo " Running test_api.py..."
echo ""

# Run the Python script
python3 test_api.py

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo " Script completed successfully."
else
    echo ""
    echo " Script failed with errors. Check output above."
fi
