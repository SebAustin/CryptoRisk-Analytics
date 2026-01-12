# CryptoRisk Analytics - Data Documentation

Complete documentation for all datasets used in the CryptoRisk Analytics platform.

---

## Table of Contents

- [Overview](#overview)
- [Dataset Summary](#dataset-summary)
- [Detailed Specifications](#detailed-specifications)
- [Data Quality Rules](#data-quality-rules)
- [Data Sources](#data-sources)
- [Licenses](#licenses)
- [Data Refresh](#data-refresh)

---

## Overview

The CryptoRisk Analytics platform uses **11 primary datasets** covering:
- Cryptocurrency price data (OHLCV) with technical indicators
- Portfolio positions and holdings
- Trade transaction history
- Market-wide metrics and indicators
- Cryptocurrency reference data
- Correlation matrix (625 pairwise correlations)
- 5 Pre-calculated KPI datasets (volatility, VaR, risk-adjusted returns, concentration, 24h changes)

All data covers **January 1, 2015 to January 11, 2026** (11+ years, real data up to today!).

**Total Records**: 2,050,000+
**Data Volume**: ~221 MB (uncompressed CSV)
**Update Frequency**: Daily (using yfinance for real data)

---

## Dataset Summary

| Dataset | Records | Date Range | Size | Purpose |
|---------|---------|------------|------|---------|
| `crypto_prices_daily_2020_2024.csv` | 66,314 | 2015-2026 | 18.5 MB | Daily OHLCV + **Bollinger Bands** |
| `portfolio_positions_current.csv` | 5,645 | 365 days | 0.72 MB | Historical position snapshots |
| `trades_history_sample.csv` | 1,978,275 | 2015-2026 | 201 MB | Trade transactions (massive volume) |
| `market_metrics_daily.csv` | 4,028 | 2015-2026 | 0.34 MB | Market aggregates |
| `crypto_reference.csv` | 25 | N/A | <1 KB | Crypto metadata (25 cryptos) |
| **`correlation_matrix.csv`** | **625** | **365-day** | **0.04 MB** | **Pairwise correlations (NEW!)** |
| `kpi_volatility.csv` | ~11,000 | Rolling | Pre-calc | Portfolio volatility KPIs |
| `kpi_var.csv` | 3 | Current | Pre-calc | VaR 95%/99% per portfolio |
| `kpi_risk_adjusted.csv` | 3 | Current | Pre-calc | Sharpe, Sortino, Beta, Alpha |
| `kpi_concentration.csv` | 15 | Current | Pre-calc | Position weights, HHI |
| `kpi_24h_change.csv` | ~1,100 | Daily | Pre-calc | Portfolio value changes |

**Total**: 11 datasets, 221+ MB

---

## Detailed Specifications

### 1. crypto_prices_daily_2020_2024.csv

**Description**: Daily OHLCV (Open, High, Low, Close, Volume) price data for 15 major cryptocurrencies, enriched with technical indicators and metadata.

**Schema**:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `date` | Date | Trading date | 2024-01-15 |
| `symbol` | Text(10) | Cryptocurrency ticker | BTC |
| `open` | Number(8) | Opening price (USD) | 42158.32 |
| `high` | Number(8) | High price (USD) | 43205.18 |
| `low` | Number(8) | Low price (USD) | 41890.45 |
| `close` | Number(8) | Closing price (USD) | 42987.62 |
| `volume` | Number | Trading volume (USD) | 28450632198.50 |
| `daily_return` | Number | Daily return % | 0.0197 |
| `ma_7` | Number(8) | 7-day moving average | 42345.78 |
| `ma_30` | Number(8) | 30-day moving average | 41203.92 |
| `volatility_30d` | Number | 30-day annualized volatility | 0.3542 |
| **`bb_middle`** | **Number(8)** | **Bollinger Band middle (20-day SMA)** | **42545.32** |
| **`bb_upper`** | **Number(8)** | **Bollinger Band upper (+2 std dev)** | **48231.15** |
| **`bb_lower`** | **Number(8)** | **Bollinger Band lower (-2 std dev)** | **36859.49** |
| **`bb_bandwidth`** | **Number(8)** | **Band width % (volatility indicator)** | **26.72** |
| **`bb_percent`** | **Number(8)** | **%B (position within bands, 0-1)** | **0.65** |
| `name` | Text | Full cryptocurrency name | Bitcoin |
| `category` | Text | Asset category | Layer 1 |
| `year` | Number | Year | 2024 |
| `month` | Number | Month (1-12) | 1 |
| `quarter` | Number | Quarter (1-4) | 1 |
| `day_of_week` | Text | Day name | Monday |
| `is_weekend` | Boolean | Weekend flag | false |

**Quality Checks**:
- ✅ All prices > 0
- ✅ No missing dates (complete series)
- ✅ No duplicate symbol-date combinations
- ✅ Volume >= 0
- ✅ Daily returns between -100% and +10000%

**Cryptocurrencies Included** (25):
1. **BTC** - Bitcoin (Layer 1)
2. **ETH** - Ethereum (Layer 1)
3. **BNB** - Binance Coin (Exchange Token)
4. **SOL** - Solana (Layer 1)
5. **XRP** - Ripple (Payment)
6. **ADA** - Cardano (Layer 1)
7. **AVAX** - Avalanche (Layer 1)
8. **DOGE** - Dogecoin (Meme)
9. **DOT** - Polkadot (Layer 0)
10. **MATIC** - Polygon (Layer 2)
11. **LINK** - Chainlink (Oracle)
12. **UNI** - Uniswap (DeFi)
13. **ATOM** - Cosmos (Layer 0)
14. **LTC** - Litecoin (Payment)
15. **ALGO** - Algorand (Layer 1)
16. **BCH** - Bitcoin Cash (Payment)
17. **SHIB** - Shiba Inu (Meme)
18. **TRX** - Tron (Layer 1)
19. **ETC** - Ethereum Classic (Layer 1)
20. **XLM** - Stellar (Payment)
21. **AAVE** - Aave (DeFi)
22. **FIL** - Filecoin (Storage)
23. **ICP** - Internet Computer (Layer 1)
24. **VET** - VeChain (Enterprise)
25. **HBAR** - Hedera (Enterprise)

---

### 2. portfolio_positions_current.csv

**Description**: Current portfolio holdings across 3 sample portfolios with different risk profiles.

**Schema**:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `portfolio_id` | Text(10) | Portfolio identifier | PF001 |
| `portfolio_name` | Text | Portfolio display name | Conservative Growth |
| `risk_tolerance` | Text | Risk profile | Low |
| `symbol` | Text(10) | Cryptocurrency ticker | BTC |
| `quantity` | Number(8) | Holdings quantity | 5.82304518 |
| `avg_cost` | Number(8) | Average cost basis | 38245.67 |
| `current_price` | Number(8) | Current market price | 42987.62 |
| `position_value` | Number | Current value (USD) | 250324.89 |
| `target_weight` | Number | Target allocation % | 0.50 |
| `as_of_date` | Date | Snapshot date | 2024-12-31 |
| `unrealized_pnl` | Number | Unrealized profit/loss | 27623.15 |
| `unrealized_pnl_pct` | Number | Unrealized return % | 12.42 |

**Portfolio Profiles**:

1. **PF001 - Conservative Growth** ($100K)
   - Risk Tolerance: Low
   - Allocation: 50% BTC, 30% ETH, 10% BNB, 10% ADA
   - Target Volatility: < 20%

2. **PF002 - Balanced Portfolio** ($250K)
   - Risk Tolerance: Medium
   - Allocation: 35% BTC, 25% ETH, 15% SOL, 10% AVAX, 10% LINK, 5% DOT
   - Target Volatility: 20-30%

3. **PF003 - High Growth** ($500K)
   - Risk Tolerance: High
   - Allocation: 25% ETH, 20% SOL, 15% AVAX, 10% each MATIC/UNI/ATOM/ALGO
   - Target Volatility: > 30%

---

### 3. trades_history_sample.csv

**Description**: Historical trade transactions for all portfolios, including buy/sell orders with fees.

**Schema**:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `trade_id` | Text(20) | Unique trade identifier | TRD000001 |
| `trade_date` | DateTime | Transaction timestamp | 2024-01-10 14:32:18 |
| `portfolio_id` | Text(10) | Portfolio identifier | PF001 |
| `portfolio_name` | Text | Portfolio display name | Conservative Growth |
| `symbol` | Text(10) | Cryptocurrency ticker | BTC |
| `trade_type` | Text | BUY or SELL | BUY |
| `quantity` | Number(8) | Trade quantity | 0.25348712 |
| `price` | Number(8) | Execution price | 42158.32 |
| `trade_amount` | Number | Total value (USD) | 10687.45 |
| `fee` | Number | Trading fee (USD) | 10.69 |
| `exchange` | Text | Exchange name | Coinbase |
| `order_type` | Text | Market or Limit | Market |

**Trade Statistics**:
- Total trades: 88
- Buy orders: 64 (73%)
- Sell orders: 24 (27%)
- Total volume: $1,335,765.49
- Total fees: $1,335.74
- Average fee rate: 0.1%

**Exchanges**:
- Coinbase
- Binance
- Kraken

---

### 4. market_metrics_daily.csv

**Description**: Daily market-wide aggregates and sentiment indicators.

**Schema**:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `date` | Date | Trading date | 2024-01-15 |
| `total_volume` | Number | Aggregate volume (USD) | 125487639287.50 |
| `avg_return` | Number | Average return % | 1.45 |
| `market_volatility` | Number | Market volatility | 0.0612 |
| `btc_dominance_pct` | Number | BTC market share % | 38.89 |
| `positive_movers` | Number | Assets with +return | 8 |
| `negative_movers` | Number | Assets with -return | 7 |
| `total_assets` | Number | Total assets tracked | 15 |
| `volatility_30d` | Number | 30-day rolling volatility | 0.0587 |
| `volume_ma_7` | Number | 7-day volume MA | 118234567890.25 |

**Insights**:
- Tracks overall market health
- BTC dominance ranges 35-45%
- Volatility spikes during major events
- Strong correlation between volume and returns

---

### 5. correlation_matrix.csv **(NEW!)**

**Description**: Pairwise correlation matrix between cryptocurrency daily returns (365-day rolling window). Essential for portfolio diversification analysis and risk management.

**Schema**:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `crypto1` | Text(10) | First cryptocurrency in pair | BTC |
| `crypto2` | Text(10) | Second cryptocurrency in pair | ETH |
| `correlation` | Number | Pearson correlation coefficient (-1 to +1) | 0.8412 |
| `is_self_correlation` | Boolean | True if crypto1 = crypto2 (always 1.0) | false |
| `period_days` | Number | Lookback period in days | 365 |
| `period_start` | Date | Start of correlation window | 2025-01-10 |
| `period_end` | Date | End of correlation window | 2026-01-10 |
| `correlation_strength` | Text | Category: Perfect/Very Strong/Strong/Moderate/Weak/Very Weak | Very Strong |
| `correlation_direction` | Text | Positive/Negative/Neutral | Positive |

**Correlation Statistics**:
- **Total pairs**: 625 (25 × 25 matrix)
- **Highest correlation**: UNI-BTC (0.9967) - Move almost identically
- **Lowest correlation**: ADA-LTC (0.3587) - Weak positive relationship
- **Perfect correlations**: 25 (diagonal, self-correlations)

**Interpretation Guide**:
| Range | Strength | Diversification Benefit |
|-------|----------|------------------------|
| 0.8 to 1.0 | Very Strong Positive | Low (assets move together) |
| 0.6 to 0.8 | Strong Positive | Moderate |
| 0.4 to 0.6 | Moderate Positive | Good |
| 0.2 to 0.4 | Weak Positive | Very Good |
| -0.2 to 0.2 | No Correlation | Excellent (independent) |
| -0.4 to -0.2 | Weak Negative | Excellent (slight hedge) |
| -0.6 to -0.4 | Moderate Negative | Outstanding (hedging) |
| -0.8 to -0.6 | Strong Negative | Exceptional (strong hedge) |
| -1.0 to -0.8 | Very Strong Negative | Perfect hedge |

**Use Cases**:
- **Portfolio Construction**: Select low-correlation assets for diversification
- **Risk Hedging**: Find negative correlations for offsetting risk
- **Concentration Detection**: Identify clusters of highly correlated holdings
- **Rebalancing**: Assess correlation drift over time

**Calculation Method**:
- Pearson correlation on daily returns
- 365-day rolling window (updated daily)
- Symmetric matrix: corr(A, B) = corr(B, A)
- Pre-calculated in Python for optimal performance

---

### 6. crypto_reference.csv

**Description**: Cryptocurrency reference data and metadata (expanded to 25 cryptocurrencies).

**Schema**:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `symbol` | Text(10) | Cryptocurrency ticker | BTC |
| `name` | Text | Full name | Bitcoin |
| `category` | Text | Asset category | Layer 1 |
| `launch_year` | Number | Launch year | 2009 |
| `is_stablecoin` | Boolean | Stablecoin flag | false |
| `is_active` | Boolean | Active trading flag | true |

**Categories**:
- **Layer 1**: BTC, ETH, SOL, ADA, AVAX, ALGO (6)
- **Layer 2**: MATIC (1)
- **Layer 0**: DOT, ATOM (2)
- **DeFi**: UNI, LINK (2)
- **Payment**: XRP, LTC (2)
- **Exchange Token**: BNB (1)
- **Meme**: DOGE (1)

---

### 7. risk_metrics_portfolio.csv

**Description**: Pre-calculated risk metrics for each portfolio (snapshot - legacy file, now replaced by 5 separate KPI files).

**Schema**:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `portfolio_id` | Text(10) | Portfolio identifier | PF001 |
| `portfolio_name` | Text | Portfolio display name | Conservative Growth |
| `risk_tolerance` | Text | Risk profile | Low |
| `total_value` | Number | Portfolio value (USD) | 100000.00 |
| `num_assets` | Number | Number of holdings | 4 |
| `volatility_30d` | Number | 30-day volatility | 0.1214 |
| `volatility_90d` | Number | 90-day volatility | 0.1156 |
| `volatility_365d` | Number | 365-day volatility | 0.1398 |
| `var_95` | Number | VaR 95% (% loss) | -2.10 |
| `var_99` | Number | VaR 99% (% loss) | -3.45 |
| `sharpe_ratio` | Number | Risk-adjusted return | 0.91 |
| `sortino_ratio` | Number | Downside risk return | 1.23 |
| `max_drawdown` | Number | Max % decline | -15.67 |
| `beta_vs_btc` | Number | Beta vs Bitcoin | 0.85 |
| `concentration_hhi` | Number | HHI index (0-1) | 0.36 |
| `diversification_score` | Number | Diversification (0-100) | 64.0 |
| `as_of_date` | Date | Calculation date | 2024-12-31 |

**Risk Profile Summary**:

| Portfolio | Volatility | VaR 95% | Sharpe | Diversification |
|-----------|------------|---------|--------|-----------------|
| Conservative | 12.14% | -2.10% | 0.91 | 64/100 |
| Balanced | 6.80% | -1.46% | 0.90 | 77/100 |
| Aggressive | 10.36% | -1.35% | 0.65 | 83.5/100 |

---

## Data Quality Rules

All datasets undergo validation before ingestion. See [`scripts/prepare_crypto_data.py`](../scripts/prepare_crypto_data.py) for implementation.

### Crypto Prices Rules

1. **Price Validation**: `close` must be > 0
2. **Volume Validation**: `volume` must be >= 0 (auto-fix: cap at 0)
3. **Date Range**: `date` must be between 2020-01-01 and 2024-12-31
4. **Uniqueness**: No duplicate `symbol` + `date` combinations
5. **Returns**: `daily_return` should be between -1 and 10 (sanity check)

### Portfolio Positions Rules

1. **Quantity**: `quantity` must be > 0
2. **Valid Symbol**: `symbol` must exist in crypto_reference
3. **Weight Sum**: Target weights should sum to ~1.0 per portfolio
4. **Position Value**: Must be >= 0

### Trades Rules

1. **Date**: `trade_date` must be <= today
2. **Quantity**: `quantity` must be > 0
3. **Price**: `price` must be > 0
4. **Trade Type**: Must be 'BUY' or 'SELL'
5. **Fee**: `fee` must be >= 0

---

## Data Sources

### Primary Source: Real Data via yfinance (UPDATED!)

The hackathon now uses **REAL cryptocurrency data** from Yahoo Finance via the `yfinance` Python library:
- **Historical prices**: Complete OHLCV data from 2015 to TODAY
- **Daily updates**: Fetches the latest data each time script runs
- **25 cryptocurrencies**: All major assets with full history
- **Quality**: Production-grade data from Yahoo Finance

**Advantages**:
- ✅ Real market data (not synthetic)
- ✅ Automatically updates to current date
- ✅ No API rate limits (yfinance is free)
- ✅ Historical accuracy for backtesting
- ✅ No licensing fees

**Fallback**: If yfinance fails, script falls back to synthetic data generation.

### Production Sources (Recommended)

For production deployment, replace with live APIs:

1. **Price Data**:
   - [CoinGecko API](https://www.coingecko.com/en/api) (Free tier: 50 calls/min)
   - [CoinMarketCap API](https://coinmarketcap.com/api/) (Free tier: 333 calls/day)
   - [Binance API](https://www.binance.com/en/binance-api) (No rate limit with account)
   - [Coinbase API](https://developers.coinbase.com/) (15 requests/sec)

2. **Portfolio Data**:
   - Exchange APIs (Coinbase, Binance, Kraken)
   - Wallet tracking services (Zapper, Zerion)
   - Manual CSV uploads

3. **Market Metrics**:
   - [CryptoCompare](https://www.cryptocompare.com/api/)
   - [Messari API](https://messari.io/api)
   - [Glassnode](https://glassnode.com/api) (on-chain metrics)

---

## Licenses

### Hackathon Synthetic Data

**License**: MIT
**Usage**: Free for any purpose
**Attribution**: Not required
**Source Code**: Available in [`scripts/prepare_crypto_data.py`](../scripts/prepare_crypto_data.py)

### Production Data Sources

**Important**: When using live APIs, review each provider's terms:

- **CoinGecko**: Free for non-commercial, attribution required
- **CoinMarketCap**: Free tier for personal use
- **Binance**: Free with account, subject to exchange ToS
- **Coinbase**: Free, subject to API terms

**Recommendation**: For commercial use, purchase API licenses or use enterprise tiers.

---

## Data Refresh

### Hackathon (Static)

Data is pre-generated and static:
- Run `prepare_crypto_data.py` once to generate CSVs
- No automatic refresh
- Snapshot date: December 31, 2024

### Production (Recommended)

Implement automated refresh:

1. **Scheduled ETL** (via Salesforce Scheduler or cron):
   ```python
   # Daily at 2 AM UTC
   python prepare_crypto_data.py --mode live --days 1
   ```

2. **Incremental Load**:
   - Fetch only new records (since last refresh)
   - Append to existing Data Lake Objects
   - Refresh Data Model Objects

3. **Real-time Streaming** (Advanced):
   - Connect WebSocket APIs (Binance, Coinbase)
   - Stream price updates to Data Cloud
   - Sub-second latency for dashboards

**Refresh Frequency**:
- **Prices**: Every 5 minutes (intraday) or Daily (end-of-day)
- **Portfolios**: Real-time (on trade) or Daily
- **Trades**: Real-time (on execution)
- **Market Metrics**: Daily
- **Risk Metrics**: Daily or on-demand

---

## Data Dictionary Quick Reference

**Fact Tables** (with embedded dimensions):
- `crypto_prices_daily_2020_2024.csv` → dmo_crypto_prices (includes date attributes: year, month, quarter, day_of_week)
- `portfolio_positions_current.csv` → dmo_portfolio_positions (includes portfolio_name, risk_tolerance)
- `trades_history_sample.csv` → dmo_trades (includes portfolio_id, portfolio_name)
- `market_metrics_daily.csv` → dmo_market_metrics

**Dimension Table**:
- `crypto_reference.csv` → dmo_cryptocurrency

**Grain**:
- Prices: One row per symbol per day (denormalized with date attributes)
- Positions: One row per portfolio per symbol (denormalized with portfolio attributes)
- Trades: One row per trade transaction
- Market: One row per day

---

## FAQs

**Q: Why synthetic data?**
A: For the hackathon, synthetic data avoids API rate limits, ensures consistency, and has no licensing restrictions. Production would use live APIs.

**Q: Can I add more cryptocurrencies?**
A: Yes! Update `CRYPTO_UNIVERSE` in `prepare_crypto_data.py`, re-run the script, and reload Data Cloud.

**Q: How accurate are the risk metrics?**
A: Calculations follow industry-standard formulas (historical VaR, annualized volatility, Sharpe ratio). For trading, validate against professional risk systems.

**Q: What about DeFi tokens?**
A: Current version focuses on major Layer 1/2 cryptos. DeFi tokens can be added in Phase 3 (see roadmap).

**Q: Can I use this for real trading?**
A: This is a demo platform. For real money, add proper authentication, audit logs, regulatory compliance, and connect to licensed trading APIs.

---

## File Locations

All generated CSV files are in: `/data/raw/`

```
data/raw/
├── crypto_prices_daily_2020_2024.csv  (66,314 records, 18.5 MB) - WITH Bollinger Bands!
├── portfolio_positions_current.csv    (5,645 records, 0.72 MB)
├── trades_history_sample.csv          (1,978,275 records, 201 MB)
├── market_metrics_daily.csv           (4,028 records, 0.34 MB)
├── crypto_reference.csv               (25 records, <1 KB)
├── correlation_matrix.csv             (625 records, 0.04 MB) ⭐ NEW!
├── kpi_volatility.csv                 (~11,000 records) - Pre-calculated
├── kpi_var.csv                        (3 records) - Pre-calculated
├── kpi_risk_adjusted.csv              (3 records) - Pre-calculated
├── kpi_concentration.csv              (15 records) - Pre-calculated
└── kpi_24h_change.csv                 (~1,100 records) - Pre-calculated
```

**Total Size**: ~221 MB (uncompressed)

---

## Contact & Support

For questions about the data:
- See [`scripts/prepare_crypto_data.py`](../scripts/prepare_crypto_data.py) for generation logic
- See [`docs/data_cloud_setup.md`](../docs/data_cloud_setup.md) for Data Cloud ingestion
- Open GitHub issue for bugs or feature requests

---

**Data prepared for the Tableau Next Hackathon 2026** 🚀
