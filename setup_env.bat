@echo off
REM CryptoRisk Analytics - Python Environment Setup Script (Windows)
REM This script creates a Python virtual environment and installs all dependencies

echo ==================================
echo CryptoRisk Analytics - Environment Setup
echo ==================================
echo.

REM Check if Python 3 is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python 3 is not installed. Please install Python 3.8+ first.
    echo   Download from: https://www.python.org/downloads/
    exit /b 1
)

echo Python found:
python --version
echo.

REM Create virtual environment
echo Creating Python virtual environment...
if exist venv (
    echo Warning: Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)

python -m venv venv
echo Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel --quiet
echo Pip upgraded
echo.

REM Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
echo Dependencies installed
echo.

REM Verify installations
echo Verifying installations...
python -c "import pandas; print(f'  pandas: {pandas.__version__}')"
python -c "import numpy; print(f'  numpy: {numpy.__version__}')"
python -c "import yfinance; print(f'  yfinance: {yfinance.__version__}')"
echo.

echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo To activate the virtual environment in the future, run:
echo   venv\Scripts\activate.bat
echo.
echo To run the data preparation scripts:
echo   venv\Scripts\activate.bat
echo   python scripts\prepare_crypto_data.py
echo   python scripts\prepare_crypto_data_with_kpis.py
echo.
echo To deactivate when done:
echo   deactivate
echo.
pause
