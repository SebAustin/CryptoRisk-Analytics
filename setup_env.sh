#!/bin/bash
# CryptoRisk Analytics - Python Environment Setup Script
# This script creates a Python virtual environment and installs all dependencies

set -e  # Exit on error

echo "=================================="
echo "CryptoRisk Analytics - Environment Setup"
echo "=================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    echo "   macOS: brew install python3"
    echo "   Linux: sudo apt-get install python3 python3-pip"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating Python virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Removing old one..."
    rm -rf venv
fi

python3 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel --quiet
echo "✓ Pip upgraded"
echo ""

# Install dependencies
echo "📥 Installing dependencies from requirements.txt..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Verify installations
echo "🔍 Verifying installations..."
python3 -c "import pandas; print(f'  pandas: {pandas.__version__}')"
python3 -c "import numpy; print(f'  numpy: {numpy.__version__}')"
python3 -c "import yfinance; print(f'  yfinance: {yfinance.__version__}')"
echo ""

echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the data preparation scripts:"
echo "  source venv/bin/activate"
echo "  python3 scripts/prepare_crypto_data.py"
echo "  python3 scripts/prepare_crypto_data_with_kpis.py"
echo ""
echo "To deactivate when done:"
echo "  deactivate"
echo ""
