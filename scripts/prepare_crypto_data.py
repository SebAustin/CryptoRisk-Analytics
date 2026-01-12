#!/usr/bin/env python3
"""
CryptoRisk Analytics Data Preparation Script
Downloads REAL cryptocurrency data from Yahoo Finance (yfinance) for Tableau Next Data Cloud.
Includes data quality validation, risk calculations, and pre-joined outputs.
"""

import pandas as pd
import numpy as np
import requests
import os
from datetime import datetime, timedelta
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Try to import yfinance
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
    print("✓ yfinance library found - will fetch REAL data")
except ImportError:
    YFINANCE_AVAILABLE = False
    print("⚠️  yfinance not found. Install with: pip install yfinance")
    print("   Falling back to synthetic data generation")

# Configuration
DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Date ranges for analysis (UP TO TODAY!)
# Extended to 2015 for more data volume (targeting 100MB+)
START_DATE = "2015-01-01"
END_DATE = datetime.now().strftime("%Y-%m-%d")  # TODAY!

# Crypto universe (top assets by market cap)
# Yahoo Finance tickers use -USD suffix (e.g., BTC-USD)
# Extended list to generate more data (100MB+ target)
CRYPTO_UNIVERSE = {
    'BTC': {'name': 'Bitcoin', 'category': 'Layer 1', 'launch_year': 2009, 'yf_ticker': 'BTC-USD'},
    'ETH': {'name': 'Ethereum', 'category': 'Layer 1', 'launch_year': 2015, 'yf_ticker': 'ETH-USD'},
    'BNB': {'name': 'Binance Coin', 'category': 'Exchange Token', 'launch_year': 2017, 'yf_ticker': 'BNB-USD'},
    'SOL': {'name': 'Solana', 'category': 'Layer 1', 'launch_year': 2020, 'yf_ticker': 'SOL-USD'},
    'XRP': {'name': 'Ripple', 'category': 'Payment', 'launch_year': 2012, 'yf_ticker': 'XRP-USD'},
    'ADA': {'name': 'Cardano', 'category': 'Layer 1', 'launch_year': 2017, 'yf_ticker': 'ADA-USD'},
    'AVAX': {'name': 'Avalanche', 'category': 'Layer 1', 'launch_year': 2020, 'yf_ticker': 'AVAX-USD'},
    'DOGE': {'name': 'Dogecoin', 'category': 'Meme', 'launch_year': 2013, 'yf_ticker': 'DOGE-USD'},
    'DOT': {'name': 'Polkadot', 'category': 'Layer 0', 'launch_year': 2020, 'yf_ticker': 'DOT-USD'},
    'MATIC': {'name': 'Polygon', 'category': 'Layer 2', 'launch_year': 2017, 'yf_ticker': 'MATIC-USD'},
    'LINK': {'name': 'Chainlink', 'category': 'Oracle', 'launch_year': 2017, 'yf_ticker': 'LINK-USD'},
    'UNI': {'name': 'Uniswap', 'category': 'DeFi', 'launch_year': 2020, 'yf_ticker': 'UNI-USD'},
    'ATOM': {'name': 'Cosmos', 'category': 'Layer 0', 'launch_year': 2019, 'yf_ticker': 'ATOM-USD'},
    'LTC': {'name': 'Litecoin', 'category': 'Payment', 'launch_year': 2011, 'yf_ticker': 'LTC-USD'},
    'ALGO': {'name': 'Algorand', 'category': 'Layer 1', 'launch_year': 2019, 'yf_ticker': 'ALGO-USD'},
    # Additional cryptos for more data volume
    'BCH': {'name': 'Bitcoin Cash', 'category': 'Payment', 'launch_year': 2017, 'yf_ticker': 'BCH-USD'},
    'SHIB': {'name': 'Shiba Inu', 'category': 'Meme', 'launch_year': 2020, 'yf_ticker': 'SHIB-USD'},
    'TRX': {'name': 'Tron', 'category': 'Layer 1', 'launch_year': 2017, 'yf_ticker': 'TRX-USD'},
    'ETC': {'name': 'Ethereum Classic', 'category': 'Layer 1', 'launch_year': 2015, 'yf_ticker': 'ETC-USD'},
    'XLM': {'name': 'Stellar', 'category': 'Payment', 'launch_year': 2014, 'yf_ticker': 'XLM-USD'},
    'AAVE': {'name': 'Aave', 'category': 'DeFi', 'launch_year': 2020, 'yf_ticker': 'AAVE-USD'},
    'FIL': {'name': 'Filecoin', 'category': 'Storage', 'launch_year': 2020, 'yf_ticker': 'FIL-USD'},
    'ICP': {'name': 'Internet Computer', 'category': 'Layer 1', 'launch_year': 2021, 'yf_ticker': 'ICP-USD'},
    'VET': {'name': 'VeChain', 'category': 'Enterprise', 'launch_year': 2018, 'yf_ticker': 'VET-USD'},
    'HBAR': {'name': 'Hedera', 'category': 'Enterprise', 'launch_year': 2019, 'yf_ticker': 'HBAR-USD'}
}

# Quality Rules
QUALITY_RULES = {
    'crypto_prices': [
        {'name': 'price > 0', 'field': 'close', 'type': 'range', 'min': 0.0000001, 'action': 'remove'},
        {'name': 'volume >= 0', 'field': 'volume', 'type': 'range', 'min': 0, 'auto_fix': 'cap'},
        {'name': 'valid date range', 'field': 'date', 'type': 'date_range', 'start': START_DATE, 'end': END_DATE, 'action': 'remove'},
        {'name': 'no duplicate ticker-date', 'field': ['symbol', 'date'], 'type': 'unique', 'action': 'remove'}
    ],
    'portfolio_positions': [
        {'name': 'quantity > 0', 'field': 'quantity', 'type': 'range', 'min': 0.0000001, 'action': 'remove'},
        {'name': 'valid symbol', 'field': 'symbol', 'type': 'reference', 'valid_values': list(CRYPTO_UNIVERSE.keys()), 'action': 'remove'}
    ]
}

def validate_and_clean_data(df, dataset_name, rules):
    """Validate data quality and clean according to rules."""
    print(f"\n🔍 Validating {dataset_name}...")
    issues_found = 0
    records_before = len(df)
    
    for rule in rules:
        rule_name = rule['name']
        field = rule['field']
        rule_type = rule['type']
        
        if rule_type == 'range':
            min_val = rule.get('min')
            max_val = rule.get('max')
            if field in df.columns:
                if min_val is not None:
                    invalid = df[df[field] < min_val]
                    if len(invalid) > 0:
                        print(f"   ⚠️  {len(invalid)} records: {rule_name}")
                        issues_found += len(invalid)
                        if rule.get('auto_fix') == 'cap':
                            df.loc[df[field] < min_val, field] = min_val
                            print(f"      ✓ Auto-fixed: capped at {min_val}")
                        elif rule.get('action') == 'remove':
                            df = df[df[field] >= min_val]
                            print(f"      ✓ Removed invalid records")
                
                if max_val is not None:
                    invalid = df[df[field] > max_val]
                    if len(invalid) > 0:
                        print(f"   ⚠️  {len(invalid)} records: {rule_name}")
                        issues_found += len(invalid)
                        if rule.get('action') == 'remove':
                            df = df[df[field] <= max_val]
                            print(f"      ✓ Removed invalid records")
        
        elif rule_type == 'date_range':
            start_date = pd.to_datetime(rule.get('start'))
            end_date = pd.to_datetime(rule.get('end'))
            if field in df.columns:
                df[field] = pd.to_datetime(df[field], errors='coerce')
                invalid = df[(df[field] < start_date) | (df[field] > end_date)]
                if len(invalid) > 0:
                    print(f"   ⚠️  {len(invalid)} records: {rule_name}")
                    issues_found += len(invalid)
                    if rule.get('action') == 'remove':
                        df = df[(df[field] >= start_date) & (df[field] <= end_date)]
                        print(f"      ✓ Removed out-of-range records")
        
        elif rule_type == 'unique':
            if isinstance(field, list):
                duplicates = df[df.duplicated(subset=field, keep='first')]
                if len(duplicates) > 0:
                    print(f"   ⚠️  {len(duplicates)} records: {rule_name}")
                    issues_found += len(duplicates)
                    if rule.get('action') == 'remove':
                        df = df.drop_duplicates(subset=field, keep='first')
                        print(f"      ✓ Removed duplicate records")
        
        elif rule_type == 'reference':
            valid_values = rule.get('valid_values', [])
            if field in df.columns and valid_values:
                invalid = df[~df[field].isin(valid_values)]
                if len(invalid) > 0:
                    print(f"   ⚠️  {len(invalid)} records: {rule_name}")
                    issues_found += len(invalid)
                    if rule.get('action') == 'remove':
                        df = df[df[field].isin(valid_values)]
                        print(f"      ✓ Removed invalid records")
    
    records_after = len(df)
    records_removed = records_before - records_after
    
    if issues_found == 0:
        print(f"   ✅ All quality checks passed ({records_after:,} records)")
    else:
        print(f"   📊 Quality Report: {issues_found} issues, {records_removed} records removed")
        print(f"   📈 Final: {records_after:,} records (was {records_before:,})")
    
    return df

def calculate_bollinger_bands(df, window=20, num_std=2):
    """
    Calculate Bollinger Bands for each cryptocurrency.
    
    Args:
        df: DataFrame with 'symbol', 'date', and 'close' columns
        window: Rolling window period (default 20 days)
        num_std: Number of standard deviations for bands (default 2)
    
    Returns:
        DataFrame with added columns: bb_middle, bb_upper, bb_lower, bb_bandwidth, bb_percent
    """
    # Sort by symbol and date to ensure proper rolling calculation
    df = df.sort_values(['symbol', 'date']).reset_index(drop=True)
    
    # Calculate Middle Band (20-day SMA)
    df['bb_middle'] = df.groupby('symbol')['close'].transform(
        lambda x: x.rolling(window=window, min_periods=window).mean()
    )
    
    # Calculate Standard Deviation (20-day)
    df['bb_std'] = df.groupby('symbol')['close'].transform(
        lambda x: x.rolling(window=window, min_periods=window).std()
    )
    
    # Calculate Upper and Lower Bands
    df['bb_upper'] = df['bb_middle'] + (num_std * df['bb_std'])
    df['bb_lower'] = df['bb_middle'] - (num_std * df['bb_std'])
    
    # Calculate Bollinger Bandwidth (volatility indicator)
    # Formula: (Upper Band - Lower Band) / Middle Band * 100
    # Higher bandwidth = higher volatility
    df['bb_bandwidth'] = ((df['bb_upper'] - df['bb_lower']) / df['bb_middle']) * 100
    
    # Calculate %B (position within bands)
    # Formula: (Close - Lower Band) / (Upper Band - Lower Band)
    # %B > 1: Above upper band (overbought)
    # %B < 0: Below lower band (oversold)
    # %B = 0.5: At middle band
    df['bb_percent'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
    
    # Drop intermediate std column
    df = df.drop('bb_std', axis=1)
    
    # Round to 8 decimal places for cleaner output
    bb_columns = ['bb_middle', 'bb_upper', 'bb_lower', 'bb_bandwidth', 'bb_percent']
    for col in bb_columns:
        if col in df.columns:
            df[col] = df[col].round(8)
    
    print(f"   ✓ Bollinger Bands calculated for {df['symbol'].nunique()} cryptocurrencies")
    print(f"   ℹ️  Window: {window} days, Std Dev: ±{num_std}")
    
    return df

def calculate_correlation_matrix(prices_df, lookback_days=365):
    """
    Calculate pairwise correlation matrix between cryptocurrency returns.
    
    Args:
        prices_df: DataFrame with 'symbol', 'date', and 'daily_return' columns
        lookback_days: Number of recent days to use for correlation (default 365 for 1 year)
    
    Returns:
        DataFrame with columns: crypto1, crypto2, correlation, period_start, period_end
    """
    print(f"\n=== Calculating Correlation Matrix ({lookback_days}-day) ===")
    
    # Sort and get most recent data
    prices_df = prices_df.sort_values(['symbol', 'date']).copy()
    
    # Get the most recent date and filter for lookback period
    max_date = prices_df['date'].max()
    if isinstance(max_date, str):
        max_date = pd.to_datetime(max_date)
    
    cutoff_date = max_date - timedelta(days=lookback_days)
    recent_prices = prices_df[pd.to_datetime(prices_df['date']) >= cutoff_date].copy()
    
    print(f"   Using data from {cutoff_date.date()} to {max_date.date()}")
    print(f"   Cryptocurrencies: {recent_prices['symbol'].nunique()}")
    
    # Pivot data to have symbols as columns and dates as rows
    returns_pivot = recent_prices.pivot(index='date', columns='symbol', values='daily_return')
    
    # Drop rows with any NaN values (for clean correlation calculation)
    returns_pivot = returns_pivot.dropna()
    
    print(f"   Trading days with complete data: {len(returns_pivot)}")
    
    # Calculate correlation matrix
    corr_matrix = returns_pivot.corr()
    
    # Convert correlation matrix to long format for Tableau
    correlation_data = []
    symbols = corr_matrix.columns.tolist()
    
    for i, crypto1 in enumerate(symbols):
        for j, crypto2 in enumerate(symbols):
            correlation_data.append({
                'crypto1': crypto1,
                'crypto2': crypto2,
                'correlation': round(corr_matrix.loc[crypto1, crypto2], 4),
                'is_self_correlation': crypto1 == crypto2,
                'period_days': lookback_days,
                'period_start': cutoff_date.strftime('%Y-%m-%d'),
                'period_end': max_date.strftime('%Y-%m-%d')
            })
    
    df_corr = pd.DataFrame(correlation_data)
    
    # Add correlation strength categories for filtering
    df_corr['correlation_strength'] = df_corr['correlation'].apply(lambda x: 
        'Perfect' if abs(x) == 1.0 else
        'Very Strong' if abs(x) >= 0.8 else
        'Strong' if abs(x) >= 0.6 else
        'Moderate' if abs(x) >= 0.4 else
        'Weak' if abs(x) >= 0.2 else
        'Very Weak'
    )
    
    # Add correlation direction
    df_corr['correlation_direction'] = df_corr['correlation'].apply(lambda x:
        'Neutral' if x == 0 else
        'Positive' if x > 0 else
        'Negative'
    )
    
    print(f"   ✓ Calculated {len(df_corr)} pairwise correlations ({len(symbols)} × {len(symbols)})")
    print(f"   📊 Correlation range: {df_corr[df_corr['crypto1'] != df_corr['crypto2']]['correlation'].min():.4f} to {df_corr[df_corr['crypto1'] != df_corr['crypto2']]['correlation'].max():.4f}")
    
    return df_corr

def fetch_real_crypto_prices():
    """Fetch REAL cryptocurrency price data from Yahoo Finance."""
    print("\n=== Fetching REAL Cryptocurrency Price Data ===")
    print(f"📅 Date Range: {START_DATE} to {END_DATE} (TODAY!)")
    print(f"🪙 Fetching {len(CRYPTO_UNIVERSE)} cryptocurrencies from Yahoo Finance...")
    
    all_prices = []
    successful_fetches = 0
    failed_symbols = []
    
    for symbol, info in CRYPTO_UNIVERSE.items():
        yf_ticker = info['yf_ticker']
        print(f"   Downloading {symbol} ({info['name']})...", end=" ")
        
        try:
            # Download data from Yahoo Finance
            ticker = yf.Ticker(yf_ticker)
            hist = ticker.history(start=START_DATE, end=END_DATE, interval='1d')
            
            if hist.empty:
                print(f"❌ No data available")
                failed_symbols.append(symbol)
                continue
            
            # Reset index to get date as column
            hist.reset_index(inplace=True)
            
            # Rename columns to match our schema
            hist['symbol'] = symbol
            hist['date'] = pd.to_datetime(hist['Date']).dt.date
            hist['open'] = hist['Open']
            hist['high'] = hist['High']
            hist['low'] = hist['Low']
            hist['close'] = hist['Close']
            hist['volume'] = hist['Volume']
            
            # Select only needed columns
            hist = hist[['date', 'symbol', 'open', 'high', 'low', 'close', 'volume']]
            
            all_prices.append(hist)
            successful_fetches += 1
            print(f"✅ {len(hist):,} days")
            
        except Exception as e:
            print(f"❌ Error: {str(e)[:50]}")
            failed_symbols.append(symbol)
            continue
    
    if not all_prices:
        raise ValueError("❌ No data fetched successfully! Check your internet connection or install yfinance.")
    
    # Combine all data
    df = pd.concat(all_prices, ignore_index=True)
    df['date'] = pd.to_datetime(df['date'])
    
    print(f"\n✅ Successfully fetched {successful_fetches}/{len(CRYPTO_UNIVERSE)} cryptocurrencies")
    if failed_symbols:
        print(f"⚠️  Failed: {', '.join(failed_symbols)}")
    
    # Calculate additional metrics
    print("📊 Calculating returns and moving averages...")
    df = df.sort_values(['symbol', 'date']).reset_index(drop=True)
    df['daily_return'] = df.groupby('symbol')['close'].pct_change()
    df['ma_7'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(7, min_periods=1).mean())
    df['ma_30'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(30, min_periods=1).mean())
    df['volatility_30d'] = df.groupby('symbol')['daily_return'].transform(lambda x: x.rolling(30, min_periods=1).std() * np.sqrt(365))
    
    # Calculate Bollinger Bands
    print("📊 Calculating Bollinger Bands (20-day, 2 std dev)...")
    df = calculate_bollinger_bands(df, window=20, num_std=2)
    
    # Validate
    df = validate_and_clean_data(df, "Crypto Prices", QUALITY_RULES['crypto_prices'])
    
    return df

def generate_crypto_prices_synthetic():
    """Generate synthetic cryptocurrency price data (FALLBACK ONLY)."""
    print("\n=== Generating SYNTHETIC Cryptocurrency Price Data ===")
    print("⚠️  Using synthetic data. For real data, install: pip install yfinance")
    
    # Generate date range
    dates = pd.date_range(start=START_DATE, end=END_DATE, freq='D')
    
    all_prices = []
    
    for symbol, info in CRYPTO_UNIVERSE.items():
        # Set realistic starting price and volatility by asset
        if symbol == 'BTC':
            base_price = 30000
            volatility = 0.04
        elif symbol == 'ETH':
            base_price = 2000
            volatility = 0.05
        elif symbol in ['BNB', 'SOL']:
            base_price = 150
            volatility = 0.06
        elif symbol in ['ADA', 'DOT', 'AVAX']:
            base_price = 1.5
            volatility = 0.07
        elif symbol == 'DOGE':
            base_price = 0.08
            volatility = 0.10
        else:
            base_price = 10
            volatility = 0.06
        
        # Generate price series with realistic trends
        np.random.seed(hash(symbol) % 2**32)
        returns = np.random.normal(0.0005, volatility, len(dates))
        
        # Add some trend and seasonality
        trend = np.linspace(0, 0.3, len(dates)) if symbol in ['ETH', 'SOL'] else np.linspace(0, 0.1, len(dates))
        prices = base_price * np.exp(np.cumsum(returns) + trend)
        
        # Generate OHLCV data
        for i, date in enumerate(dates):
            close = prices[i]
            open_price = close * (1 + np.random.uniform(-0.02, 0.02))
            high = max(open_price, close) * (1 + abs(np.random.uniform(0, 0.03)))
            low = min(open_price, close) * (1 - abs(np.random.uniform(0, 0.03)))
            volume = abs(np.random.lognormal(18, 2)) if symbol in ['BTC', 'ETH'] else abs(np.random.lognormal(16, 2))
            
            all_prices.append({
                'date': date,
                'symbol': symbol,
                'open': round(open_price, 8),
                'high': round(high, 8),
                'low': round(low, 8),
                'close': round(close, 8),
                'volume': round(volume, 2)
            })
    
    df = pd.DataFrame(all_prices)
    
    # Calculate additional metrics
    df['daily_return'] = df.groupby('symbol')['close'].pct_change()
    df['ma_7'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(7, min_periods=1).mean())
    df['ma_30'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(30, min_periods=1).mean())
    df['volatility_30d'] = df.groupby('symbol')['daily_return'].transform(lambda x: x.rolling(30, min_periods=1).std() * np.sqrt(365))
    
    # Calculate Bollinger Bands
    print("📊 Calculating Bollinger Bands (20-day, 2 std dev)...")
    df = calculate_bollinger_bands(df, window=20, num_std=2)
    
    # Validate
    df = validate_and_clean_data(df, "Crypto Prices", QUALITY_RULES['crypto_prices'])
    
    return df

def generate_crypto_prices():
    """Main wrapper: Try to fetch real data, fallback to synthetic."""
    if YFINANCE_AVAILABLE:
        try:
            return fetch_real_crypto_prices()
        except Exception as e:
            print(f"\n⚠️  Failed to fetch real data: {str(e)}")
            print("   Falling back to synthetic data generation...")
            return generate_crypto_prices_synthetic()
    else:
        return generate_crypto_prices_synthetic()

def create_crypto_reference():
    """Create cryptocurrency reference table."""
    print("\n=== Creating Cryptocurrency Reference ===")
    
    ref_data = []
    for symbol, info in CRYPTO_UNIVERSE.items():
        ref_data.append({
            'symbol': symbol,
            'name': info['name'],
            'category': info['category'],
            'launch_year': info['launch_year'],
            'is_stablecoin': False,
            'is_active': True
        })
    
    df = pd.DataFrame(ref_data)
    
    # NOTE: market_cap_tier should be a calculated field in the DMO, not in the CSV
    # It will be calculated in Data Cloud as:
    # CASE WHEN category IN ('Layer 1', 'Payment') THEN 'Large Cap'
    #      WHEN category IN ('Layer 2', 'DeFi', 'Exchange Token') THEN 'Mid Cap'
    #      ELSE 'Small Cap' END
    
    output_path = DATA_DIR / 'crypto_reference.csv'
    df.to_csv(output_path, index=False)
    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"✓ Created {output_path} ({len(df)} cryptos, {file_size_mb:.2f} MB)")
    return df

def generate_portfolio_positions(prices_df):
    """Generate sample portfolio positions - HISTORICAL SNAPSHOTS for 100MB+ data."""
    print("\n=== Generating Portfolio Positions (Historical Snapshots) ===")
    
    # Create 3 sample portfolios with different risk profiles
    portfolios = {
        'CONSERVATIVE': {'id': 'PF001', 'name': 'Conservative Growth', 'risk_tolerance': 'Low'},
        'BALANCED': {'id': 'PF002', 'name': 'Balanced Portfolio', 'risk_tolerance': 'Medium'},
        'AGGRESSIVE': {'id': 'PF003', 'name': 'High Growth', 'risk_tolerance': 'High'}
    }
    
    # Define allocations by portfolio type
    allocations = {
        'CONSERVATIVE': {'BTC': 0.50, 'ETH': 0.30, 'BNB': 0.10, 'ADA': 0.10},
        'BALANCED': {'BTC': 0.35, 'ETH': 0.25, 'SOL': 0.15, 'AVAX': 0.10, 'LINK': 0.10, 'DOT': 0.05},
        'AGGRESSIVE': {'ETH': 0.25, 'SOL': 0.20, 'AVAX': 0.15, 'MATIC': 0.10, 'UNI': 0.10, 'ATOM': 0.10, 'ALGO': 0.10}
    }
    
    positions = []
    portfolio_values = {'CONSERVATIVE': 100000, 'BALANCED': 250000, 'AGGRESSIVE': 500000}
    
    # Generate DAILY snapshots for the last 365 days (huge data volume)
    all_dates = sorted(prices_df['date'].unique())
    snapshot_dates = all_dates[-365:]  # Last year of daily snapshots
    
    print(f"   Generating {len(snapshot_dates)} daily snapshots × 3 portfolios...")
    
    for snapshot_date in snapshot_dates:
        # Get prices for this date
        daily_prices = prices_df[prices_df['date'] == snapshot_date].set_index('symbol')['close']
        
        if len(daily_prices) == 0:
            continue
        
        for pf_type, allocation in allocations.items():
            pf_info = portfolios[pf_type]
            total_value = portfolio_values[pf_type]
            
            for symbol, weight in allocation.items():
                if symbol in daily_prices.index:
                    position_value = total_value * weight * np.random.uniform(0.95, 1.05)  # Slight variation
                    quantity = position_value / daily_prices[symbol]
                    avg_cost = daily_prices[symbol] * np.random.uniform(0.8, 1.2)
                    
                    positions.append({
                        'portfolio_id': pf_info['id'],
                        'portfolio_name': pf_info['name'],
                        'risk_tolerance': pf_info['risk_tolerance'],
                        'symbol': symbol,
                        'quantity': round(quantity, 8),
                        'avg_cost': round(avg_cost, 8),
                        'current_price': round(daily_prices[symbol], 8),
                        'position_value': round(position_value, 2),
                        'target_weight': round(weight, 4),
                        'as_of_date': snapshot_date
                    })
    
    df = pd.DataFrame(positions)
    print(f"   Generated {len(df):,} position records")
    
    # Calculate additional metrics
    df['unrealized_pnl'] = (df['current_price'] - df['avg_cost']) * df['quantity']
    df['unrealized_pnl_pct'] = (df['current_price'] / df['avg_cost'] - 1) * 100
    
    # NOTE: risk_category should be a calculated field in the DMO, not in the CSV
    # It will be calculated in Data Cloud as:
    # CASE WHEN risk_tolerance = 'Low' THEN 'Conservative'
    #      WHEN risk_tolerance = 'Medium' THEN 'Balanced'
    #      WHEN risk_tolerance = 'High' THEN 'Aggressive'
    #      ELSE 'Unknown' END
    
    # Ensure as_of_date is string format for Data Cloud
    df['as_of_date'] = df['as_of_date'].astype(str)
    
    # Reorder columns for consistency (WITHOUT risk_category)
    column_order = [
        'portfolio_id', 'portfolio_name', 'risk_tolerance',
        'symbol', 'quantity', 'avg_cost', 'current_price', 'position_value',
        'target_weight', 'unrealized_pnl', 'unrealized_pnl_pct', 'as_of_date'
    ]
    df = df[column_order]
    
    # Validate
    df = validate_and_clean_data(df, "Portfolio Positions", QUALITY_RULES['portfolio_positions'])
    
    return df

def generate_trades(positions_df):
    """Generate sample trade history."""
    print("\n=== Generating Trade History ===")
    
    trades = []
    trade_id = 1
    
    # Generate MANY MORE trades for each position (aiming for 100MB total data)
    # Generate trades spanning the entire date range for volume
    for _, position in positions_df.iterrows():
        # Generate 200-500 trades per position (significantly more data)
        num_trades = np.random.randint(200, 500)
        
        for i in range(num_trades):
            # Random date spanning full history (2015-2026)
            days_back = np.random.randint(1, 4000)  # Cover ~11 years
            trade_date = pd.Timestamp(END_DATE) - pd.Timedelta(days=days_back)
            
            # Ensure date is after 2015
            if trade_date < pd.Timestamp('2015-01-01'):
                trade_date = pd.Timestamp('2015-01-01') + pd.Timedelta(days=np.random.randint(1, 100))
            
            # Alternate buy/sell, but more buys
            trade_type = np.random.choice(['BUY', 'BUY', 'BUY', 'BUY', 'SELL'])
            
            # Random quantity (fraction of current position)
            trade_qty = position['quantity'] * np.random.uniform(0.05, 0.3)
            
            # Price varies around current price
            trade_price = position['current_price'] * np.random.uniform(0.3, 2.0)
            
            trade_amount = trade_qty * trade_price
            fee = trade_amount * 0.001  # 0.1% fee
            
            trades.append({
                'trade_id': f'TRD{trade_id:06d}',
                'trade_date': trade_date,
                'portfolio_id': position['portfolio_id'],
                'portfolio_name': position['portfolio_name'],
                'symbol': position['symbol'],
                'trade_type': trade_type,
                'quantity': round(trade_qty, 8),
                'price': round(trade_price, 8),
                'trade_amount': round(trade_amount, 2),
                'fee': round(fee, 2),
                'exchange': np.random.choice(['Coinbase', 'Binance', 'Kraken', 'FTX', 'Gemini', 'KuCoin']),
                'order_type': np.random.choice(['Market', 'Limit', 'Stop Loss', 'Take Profit'])
            })
            
            trade_id += 1
    
    df = pd.DataFrame(trades)
    df = df.sort_values('trade_date').reset_index(drop=True)
    
    print(f"   Generated {len(df):,} trades")
    
    return df

def calculate_market_metrics(prices_df):
    """Calculate market-wide metrics by date."""
    print("\n=== Calculating Market Metrics ===")
    
    # Aggregate by date
    daily_metrics = []
    
    for date in prices_df['date'].unique():
        day_prices = prices_df[prices_df['date'] == date]
        
        # Calculate market metrics
        total_volume = day_prices['volume'].sum()
        avg_return = day_prices['daily_return'].mean()
        market_volatility = day_prices['daily_return'].std()
        
        # BTC dominance (BTC volume / total volume)
        btc_volume = day_prices[day_prices['symbol'] == 'BTC']['volume'].sum()
        btc_dominance = (btc_volume / total_volume * 100) if total_volume > 0 else 0
        
        # Count positive vs negative movers
        positive_count = (day_prices['daily_return'] > 0).sum()
        negative_count = (day_prices['daily_return'] < 0).sum()
        
        daily_metrics.append({
            'date': date,
            'total_volume': round(total_volume, 2),
            'avg_return': round(avg_return * 100, 4) if pd.notna(avg_return) else 0,
            'market_volatility': round(market_volatility, 6) if pd.notna(market_volatility) else 0,
            'btc_dominance_pct': round(btc_dominance, 2),
            'positive_movers': int(positive_count),
            'negative_movers': int(negative_count),
            'total_assets': len(day_prices)
        })
    
    df = pd.DataFrame(daily_metrics)
    
    # Calculate rolling metrics
    df['volatility_30d'] = df['market_volatility'].rolling(30, min_periods=1).mean()
    df['volume_ma_7'] = df['total_volume'].rolling(7, min_periods=1).mean()
    
    return df

def calculate_portfolio_risk_metrics(positions_df, prices_df):
    """Calculate comprehensive risk metrics by portfolio."""
    print("\n=== Calculating Portfolio Risk Metrics ===")
    
    risk_metrics = []
    
    for portfolio_id in positions_df['portfolio_id'].unique():
        pf_positions = positions_df[positions_df['portfolio_id'] == portfolio_id]
        portfolio_name = pf_positions['portfolio_name'].iloc[0]
        risk_tolerance = pf_positions['risk_tolerance'].iloc[0]
        
        # Get return history for portfolio assets
        symbols = pf_positions['symbol'].tolist()
        weights = pf_positions['target_weight'].tolist()
        
        # Calculate portfolio returns (weighted)
        portfolio_returns = []
        for symbol, weight in zip(symbols, weights):
            asset_returns = prices_df[prices_df['symbol'] == symbol]['daily_return'].dropna()
            portfolio_returns.append(asset_returns * weight)
        
        if portfolio_returns:
            # Combine into portfolio return series
            pf_returns = pd.concat(portfolio_returns, axis=1).sum(axis=1).dropna()
            
            # Calculate risk metrics
            volatility_30d = pf_returns.tail(30).std() * np.sqrt(365) if len(pf_returns) >= 30 else 0
            volatility_90d = pf_returns.tail(90).std() * np.sqrt(365) if len(pf_returns) >= 90 else 0
            volatility_365d = pf_returns.tail(365).std() * np.sqrt(365) if len(pf_returns) >= 365 else 0
            
            # Value at Risk (95% and 99%)
            var_95 = np.percentile(pf_returns, 5) if len(pf_returns) > 0 else 0
            var_99 = np.percentile(pf_returns, 1) if len(pf_returns) > 0 else 0
            
            # Sharpe Ratio (assuming 2% risk-free rate)
            risk_free_daily = 0.02 / 365
            excess_returns = pf_returns - risk_free_daily
            sharpe_ratio = (excess_returns.mean() / excess_returns.std() * np.sqrt(365)) if excess_returns.std() > 0 else 0
            
            # Sortino Ratio (downside deviation)
            downside_returns = pf_returns[pf_returns < 0]
            sortino_ratio = (excess_returns.mean() / downside_returns.std() * np.sqrt(365)) if len(downside_returns) > 0 and downside_returns.std() > 0 else 0
            
            # Max Drawdown
            cumulative = (1 + pf_returns).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            max_drawdown = drawdown.min() if len(drawdown) > 0 else 0
            
            # Beta vs BTC
            btc_returns = prices_df[prices_df['symbol'] == 'BTC']['daily_return'].dropna()
            if len(btc_returns) > 0 and len(pf_returns) > 0:
                # Align series
                common_idx = pf_returns.index.intersection(btc_returns.index)
                if len(common_idx) > 30:
                    cov = pf_returns.loc[common_idx].cov(btc_returns.loc[common_idx])
                    var = btc_returns.loc[common_idx].var()
                    beta = cov / var if var > 0 else 1
                else:
                    beta = 1
            else:
                beta = 1
            
            # Portfolio concentration (Herfindahl Index)
            hhi = sum([w**2 for w in weights])
            
            total_value = pf_positions['position_value'].sum()
            
            risk_metrics.append({
                'portfolio_id': portfolio_id,
                'portfolio_name': portfolio_name,
                'risk_tolerance': risk_tolerance,
                'total_value': round(total_value, 2),
                'num_assets': len(pf_positions),
                'volatility_30d': round(volatility_30d, 4),
                'volatility_90d': round(volatility_90d, 4),
                'volatility_365d': round(volatility_365d, 4),
                'var_95': round(var_95 * 100, 4),
                'var_99': round(var_99 * 100, 4),
                'sharpe_ratio': round(sharpe_ratio, 4),
                'sortino_ratio': round(sortino_ratio, 4),
                'max_drawdown': round(max_drawdown * 100, 4),
                'beta_vs_btc': round(beta, 4),
                'concentration_hhi': round(hhi, 4),
                'diversification_score': round((1 - hhi) * 100, 2),
                'as_of_date': prices_df['date'].max()
            })
    
    df = pd.DataFrame(risk_metrics)
    return df

def create_enriched_datasets(prices_df, positions_df, trades_df, market_df, risk_df, crypto_ref_df, corr_df):
    """Create pre-joined datasets ready for Data Cloud."""
    print("\n=== Creating Enriched Datasets ===")
    
    # 1. Crypto Prices Enriched (prices + crypto metadata + date attributes)
    prices_enriched = prices_df.merge(crypto_ref_df, on='symbol', how='left')
    
    # Ensure date is datetime
    prices_enriched['date'] = pd.to_datetime(prices_enriched['date'])
    
    # Add date attributes
    prices_enriched['year'] = prices_enriched['date'].dt.year
    prices_enriched['month'] = prices_enriched['date'].dt.month
    prices_enriched['quarter'] = prices_enriched['date'].dt.quarter
    prices_enriched['day_of_week'] = prices_enriched['date'].dt.day_name()
    prices_enriched['is_weekend'] = prices_enriched['date'].dt.dayofweek >= 5
    
    # Ensure daily_return exists and fill NaN with 0 for first day of each symbol
    if 'daily_return' not in prices_enriched.columns:
        prices_enriched['daily_return'] = prices_enriched.groupby('symbol')['close'].pct_change()
    
    prices_enriched['daily_return'] = prices_enriched['daily_return'].fillna(0)
    
    # NOTE: daily_return_pct is NOT needed - semantic layer handles percentage conversion
    # The semantic layer uses daily_return (decimal) and displays it as percentage when needed
    
    # Reorder columns for better readability (WITHOUT daily_return_pct)
    column_order = [
        'date', 'year', 'month', 'quarter', 'day_of_week', 'is_weekend',
        'symbol', 'name', 'category', 'launch_year', 'is_stablecoin', 'is_active',
        'open', 'high', 'low', 'close', 'volume',
        'daily_return', 'ma_7', 'ma_30', 'volatility_30d',
        'bb_middle', 'bb_upper', 'bb_lower', 'bb_bandwidth', 'bb_percent'
    ]
    
    # Only include columns that exist
    column_order = [col for col in column_order if col in prices_enriched.columns]
    prices_enriched = prices_enriched[column_order]
    
    # Format date as YYYY-MM-DD string for Data Cloud compatibility
    prices_enriched['date'] = prices_enriched['date'].dt.strftime('%Y-%m-%d')
    
    output_path = DATA_DIR / 'crypto_prices_daily_2020_2024.csv'
    prices_enriched.to_csv(output_path, index=False)
    print(f"✓ Created {output_path} ({len(prices_enriched):,} records)")
    
    # Show file size
    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"   File size: {file_size_mb:.2f} MB")
    
    # 2. Portfolio Positions Current (already enriched)
    output_path = DATA_DIR / 'portfolio_positions_current.csv'
    positions_df.to_csv(output_path, index=False)
    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"✓ Created {output_path} ({len(positions_df):,} records, {file_size_mb:.2f} MB)")
    
    # 3. Trades History (already enriched)
    # Format dates as strings
    trades_df['trade_date'] = pd.to_datetime(trades_df['trade_date']).dt.strftime('%Y-%m-%d')
    output_path = DATA_DIR / 'trades_history_sample.csv'
    trades_df.to_csv(output_path, index=False)
    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"✓ Created {output_path} ({len(trades_df):,} records, {file_size_mb:.2f} MB)")
    
    # 4. Market Metrics Daily
    # Format dates as strings
    market_df['date'] = pd.to_datetime(market_df['date']).dt.strftime('%Y-%m-%d')
    output_path = DATA_DIR / 'market_metrics_daily.csv'
    market_df.to_csv(output_path, index=False)
    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"✓ Created {output_path} ({len(market_df):,} records, {file_size_mb:.2f} MB)")
    
    # 5. Risk Metrics Portfolio
    # Format dates as strings
    risk_df['as_of_date'] = pd.to_datetime(risk_df['as_of_date']).dt.strftime('%Y-%m-%d')
    output_path = DATA_DIR / 'risk_metrics_portfolio.csv'
    risk_df.to_csv(output_path, index=False)
    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"✓ Created {output_path} ({len(risk_df):,} records, {file_size_mb:.2f} MB)")
    
    # 6. Correlation Matrix
    output_path = DATA_DIR / 'correlation_matrix.csv'
    corr_df.to_csv(output_path, index=False)
    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"✓ Created {output_path} ({len(corr_df):,} records, {file_size_mb:.2f} MB)")
    
    # Calculate total size
    total_size = sum([(DATA_DIR / f).stat().st_size for f in [
        'crypto_prices_daily_2020_2024.csv',
        'portfolio_positions_current.csv', 
        'trades_history_sample.csv',
        'market_metrics_daily.csv',
        'risk_metrics_portfolio.csv',
        'correlation_matrix.csv'
    ]]) / (1024 * 1024)
    print(f"\n📦 Total data size: {total_size:.2f} MB")

def generate_summary_stats(prices_df, positions_df, trades_df, market_df, risk_df):
    """Generate summary statistics."""
    print("\n" + "="*70)
    print("SUMMARY STATISTICS - CryptoRisk Analytics")
    print("="*70)
    
    print(f"\n📊 Crypto Price Data:")
    print(f"  Total records: {len(prices_df):,}")
    print(f"  Date range: {prices_df['date'].min().date()} to {prices_df['date'].max().date()}")
    print(f"  Cryptocurrencies: {prices_df['symbol'].nunique()}")
    print(f"  Trading days: {prices_df['date'].nunique():,}")
    
    print(f"\n💼 Portfolio Data:")
    print(f"  Total portfolios: {positions_df['portfolio_id'].nunique()}")
    print(f"  Total positions: {len(positions_df)}")
    print(f"  Total value: ${positions_df['position_value'].sum():,.2f}")
    print(f"  Assets held: {positions_df['symbol'].nunique()}")
    
    print(f"\n📈 Trading Activity:")
    print(f"  Total trades: {len(trades_df):,}")
    print(f"  Buy orders: {(trades_df['trade_type'] == 'BUY').sum():,}")
    print(f"  Sell orders: {(trades_df['trade_type'] == 'SELL').sum():,}")
    print(f"  Total volume: ${trades_df['trade_amount'].sum():,.2f}")
    print(f"  Total fees: ${trades_df['fee'].sum():,.2f}")
    
    print(f"\n🎯 Risk Metrics:")
    for _, row in risk_df.iterrows():
        print(f"  {row['portfolio_name']}:")
        print(f"    - Volatility (30d): {row['volatility_30d']*100:.2f}%")
        print(f"    - VaR 95%: {row['var_95']:.2f}%")
        print(f"    - Sharpe Ratio: {row['sharpe_ratio']:.2f}")
        print(f"    - Diversification: {row['diversification_score']:.1f}/100")
    
    print(f"\n🌍 Market Overview:")
    latest_market = market_df.iloc[-1]
    # Handle date as string (already converted in create_enriched_datasets)
    latest_date = latest_market['date'] if isinstance(latest_market['date'], str) else latest_market['date'].date()
    print(f"  Latest date: {latest_date}")
    print(f"  Market volatility: {latest_market['market_volatility']:.4f}")
    print(f"  BTC dominance: {latest_market['btc_dominance_pct']:.2f}%")
    print(f"  Positive movers: {latest_market['positive_movers']}/{latest_market['total_assets']}")
    
    print("\n" + "="*70)
    print("✅ Data preparation complete!")
    print(f"📁 Output directory: {DATA_DIR}")
    print("="*70)

def main():
    """Main execution function."""
    print("\n" + "="*70)
    print("CryptoRisk Analytics - Data Preparation Pipeline")
    print("="*70)
    print(f"Output directory: {DATA_DIR}\n")
    
    # Step 1: Generate crypto prices
    prices_df = generate_crypto_prices()
    
    # Step 2: Create crypto reference
    crypto_ref_df = create_crypto_reference()
    
    # Step 3: Generate portfolio positions
    positions_df = generate_portfolio_positions(prices_df)
    
    # Step 4: Generate trades
    trades_df = generate_trades(positions_df)
    
    # Step 5: Calculate market metrics
    market_df = calculate_market_metrics(prices_df)
    
    # Step 6: Calculate risk metrics
    risk_df = calculate_portfolio_risk_metrics(positions_df, prices_df)
    
    # Step 7: Calculate correlation matrix
    corr_df = calculate_correlation_matrix(prices_df, lookback_days=365)
    
    # Step 8: Create enriched datasets
    create_enriched_datasets(prices_df, positions_df, trades_df, market_df, risk_df, crypto_ref_df, corr_df)
    
    # Step 9: Generate summary
    generate_summary_stats(prices_df, positions_df, trades_df, market_df, risk_df)
    
    print("\n✅ All datasets prepared successfully!")
    print("\nNext steps:")
    print("1. Review the generated CSV files in /data/raw/")
    print("2. Upload clean CSVs to Tableau Data Cloud")
    print("3. Follow docs/data_cloud_setup.md for configuration")

if __name__ == "__main__":
    main()
