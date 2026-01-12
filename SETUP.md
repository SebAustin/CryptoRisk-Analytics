# Python Environment Setup

Quick guide to set up your Python environment and run the data preparation scripts.

---

## 🚀 Quick Start

### macOS / Linux

```bash
# 1. Run the setup script
chmod +x setup_env.sh
./setup_env.sh

# 2. Activate the environment (already done by setup script)
source venv/bin/activate

# 3. Run data generation scripts
python3 scripts/prepare_crypto_data.py
python3 scripts/prepare_crypto_data_with_kpis.py
```

### Windows

```cmd
# 1. Run the setup script
setup_env.bat

# 2. Activate the environment (already done by setup script)
venv\Scripts\activate.bat

# 3. Run data generation scripts
python scripts\prepare_crypto_data.py
python scripts\prepare_crypto_data_with_kpis.py
```

---

## 📋 Prerequisites

- **Python 3.8 or higher**
  - macOS: `brew install python3`
  - Linux: `sudo apt-get install python3 python3-pip`
  - Windows: Download from [python.org](https://www.python.org/downloads/)

- **Internet connection** (for downloading real cryptocurrency data from Yahoo Finance)

---

## 🔧 Manual Setup (if scripts don't work)

### Step 1: Create Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate.bat
```

### Step 2: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install pandas>=2.0.0
pip install numpy>=1.24.0
pip install yfinance>=0.2.28

# Or install all at once
pip install -r requirements.txt
```

### Step 3: Run Scripts

```bash
# Generate core data (fetches real crypto prices)
python3 scripts/prepare_crypto_data.py

# Generate pre-calculated KPIs
python3 scripts/prepare_crypto_data_with_kpis.py
```

---

## 📊 Expected Output

After running both scripts, you'll have **10 CSV files** in `data/raw/`:

### Core Data Files (5)
1. `crypto_reference.csv` - 25 cryptocurrencies
2. `crypto_prices_daily_2020_2024.csv` - 66,291 price records
3. `portfolio_positions_current.csv` - 5,647 position snapshots
4. `trades_history_sample.csv` - 1,972,215 trades
5. `market_metrics_daily.csv` - 4,018 market indicators

### Pre-Calculated KPI Files (5)
6. `kpi_portfolio_volatility_timeseries.csv` - 11,038 volatility records
7. `kpi_portfolio_var_current.csv` - 3 VaR calculations
8. `kpi_portfolio_risk_adjusted_returns.csv` - 3 risk-adjusted metrics
9. `kpi_portfolio_concentration.csv` - 15 concentration metrics
10. `kpi_portfolio_24h_change.csv` - 1,092 daily changes

**Total Size**: ~250 MB

---

## 🐛 Troubleshooting

### Error: "yfinance not found"

```bash
pip install yfinance --upgrade
```

### Error: "No module named 'pandas'"

```bash
pip install pandas numpy
```

### Error: "externally-managed-environment" (macOS/Linux)

```bash
# Use the virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# OR use --break-system-packages (not recommended)
pip install -r requirements.txt --break-system-packages
```

### Error: "Permission denied: ./setup_env.sh"

```bash
chmod +x setup_env.sh
./setup_env.sh
```

### Scripts run slowly

- **Expected**: The first script (`prepare_crypto_data.py`) downloads real data from Yahoo Finance and can take 5-10 minutes depending on your internet speed.
- **Progress indicators**: The scripts show progress bars and status messages.

---

## ✅ Verification

After successful setup, verify your environment:

```bash
# Activate environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate.bat  # Windows

# Check installed packages
pip list

# Expected output should include:
# pandas        2.x.x
# numpy         1.x.x
# yfinance      0.2.x
```

---

## 🔄 Updating Dependencies

If you need to update packages:

```bash
# Activate environment first
source venv/bin/activate

# Update a specific package
pip install --upgrade yfinance

# Update all packages
pip install --upgrade -r requirements.txt
```

---

## 🧹 Cleanup

To remove the virtual environment:

```bash
# Deactivate first
deactivate

# Remove venv folder
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows
```

To regenerate data (if you modified the scripts):

```bash
# Remove old CSV files
rm data/raw/*.csv

# Re-run scripts
python3 scripts/prepare_crypto_data.py
python3 scripts/prepare_crypto_data_with_kpis.py
```

---

## 📚 Next Steps

After generating data:

1. **Upload CSV files** to Tableau Data Cloud
   - Follow guide: `docs/data_cloud_setup.md`

2. **Create DMOs** and relationships
   - Create 10 Data Model Objects
   - Set up 8 relationships

3. **Configure semantic layer**
   - Reference: `config/semantic_layer_config.yaml`
   - Guide: `docs/precalculated_kpis_guide.md`

---

## 💡 Tips

- **Run scripts in order**: Always run `prepare_crypto_data.py` before `prepare_crypto_data_with_kpis.py` (the second script depends on files created by the first)

- **Real data**: The scripts fetch real cryptocurrency data from Yahoo Finance up to the current date!

- **Data volume**: Scripts are configured to generate 250+ MB of data for a comprehensive demo

- **Re-running**: You can re-run scripts multiple times. They will overwrite existing CSV files.

---

**Questions?** Check the main README.md or documentation in the `docs/` folder.
