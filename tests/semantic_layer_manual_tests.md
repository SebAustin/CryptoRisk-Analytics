# Semantic Layer Manual Testing Checklist
## CryptoRisk Analytics - Tableau Data Cloud

This checklist provides step-by-step manual tests to validate your semantic layer configuration in Tableau Data Cloud.

---

## 📋 Pre-Test Setup

**Before starting tests**:
- [ ] Semantic layer is published to Tableau Data Cloud
- [ ] All 11 Data Streams are connected (5 core + 1 correlation + 5 KPI)
- [ ] All 11 DMOs are created with relationships properly configured
- [ ] **CRITICAL**: All KPI relationships include date joins (see Test 1.2)
- [ ] You have access to a Tableau workbook connected to the semantic layer

**Test Environment**:
- Tableau Data Cloud URL: _____________________
- Workbook Name: CryptoRisk Analytics Test
- Test Date: _____________________

---

## ✅ TEST CATEGORY 1: Data Model Objects (DMOs)

### Test 1.1: Verify All DMOs Exist
**Location**: Data Cloud → Data Model

**Core DMOs**:
- [ ] `dmo_cryptocurrency` exists
- [ ] `dmo_crypto_prices` exists (with Bollinger Bands fields!)
- [ ] `dmo_portfolio_positions` exists
- [ ] `dmo_trades` exists
- [ ] `dmo_market_metrics` exists
- [ ] `dmo_correlation_matrix` exists ⭐ **NEW!**

**KPI DMOs** (Pre-calculated):
- [ ] `dmo_kpi_volatility` exists
- [ ] `dmo_kpi_var` exists
- [ ] `dmo_kpi_risk_adjusted` exists
- [ ] `dmo_kpi_concentration` exists
- [ ] `dmo_kpi_24h_change` exists

**Expected**: All 11 DMOs visible in data model
**Status**: ☐ PASS ☐ FAIL

---

### Test 1.2: Verify DMO Relationships ⚠️ CRITICAL
**Location**: Data Cloud → Data Model → Relationships

**Core Relationships** (Symbol-based, no date join needed):
- [ ] **Rel 1**: `dmo_crypto_prices` → `dmo_cryptocurrency` (via `symbol`)
- [ ] **Rel 2**: `dmo_portfolio_positions` → `dmo_cryptocurrency` (via `symbol`)
- [ ] **Rel 3**: `dmo_trades` → `dmo_cryptocurrency` (via `symbol`)

**KPI Relationships** (⚠️ MUST include date joins):
- [ ] **Rel 4**: `dmo_kpi_volatility` → `dmo_portfolio_positions`
  - Join: `portfolio_id` **AND** `date = as_of_date` ✅
- [ ] **Rel 5**: `dmo_kpi_var` → `dmo_portfolio_positions`
  - Join: `portfolio_id` **AND** `as_of_date = as_of_date` ✅
- [ ] **Rel 6**: `dmo_kpi_risk_adjusted` → `dmo_portfolio_positions`
  - Join: `portfolio_id` **AND** `as_of_date = as_of_date` ✅
- [ ] **Rel 7a**: `dmo_kpi_concentration` → `dmo_cryptocurrency`
  - Join: `symbol`
- [ ] **Rel 7b**: `dmo_kpi_concentration` → `dmo_portfolio_positions`
  - Join: `portfolio_id` **AND** `symbol` **AND** `as_of_date = as_of_date` ✅
- [ ] **Rel 8**: `dmo_kpi_24h_change` → `dmo_portfolio_positions`
  - Join: `portfolio_id` **AND** `date = as_of_date` ✅

**Expected**: 9 relationships total (3 core + 6 KPI)
**Status**: ☐ PASS ☐ FAIL

**⚠️ VALIDATION**: If date joins are missing, you will see:
- Portfolio values 100-400x too large ($36M instead of $97K)
- VaR values 365x too large (-$6.6K instead of -$5K when filtered)
- Constant values across different dates
- Sharpe Ratio negative or incorrect

---

### Test 1.3: Check dmo_crypto_prices Fields
**Location**: Data Cloud → DMO → dmo_crypto_prices

Verify these fields exist:
- [ ] `date` (Date)
- [ ] `symbol` (String)
- [ ] `open`, `high`, `low`, `close` (Decimal)
- [ ] `volume` (Decimal)
- [ ] `daily_return` (Decimal)
- [ ] `daily_return_pct` (Decimal)
- [ ] `year`, `month`, `quarter` (Integer)
- [ ] `day_of_week` (String)
- [ ] `is_weekend` (Boolean)
- [ ] `name`, `category` (from relationship)

**Expected**: All fields present with correct data types
**Status**: ☐ PASS ☐ FAIL

---

## ✅ TEST CATEGORY 2: Dimensions

### Test 2.1: Date Dimensions
**Location**: Tableau Workbook → Data Pane → Dimensions

Verify these date dimensions appear:
- [ ] Date
- [ ] Year
- [ ] Month
- [ ] Quarter
- [ ] Day of Week
- [ ] Is Weekend

**Test**: Drag `Date` to Rows → Should show date hierarchy
**Expected**: Date fields work and show proper values
**Status**: ☐ PASS ☐ FAIL

---

### Test 2.2: Crypto Dimensions
**Location**: Tableau Workbook → Data Pane → Dimensions

Verify these crypto dimensions appear:
- [ ] Crypto Symbol (BTC, ETH, SOL, etc.)
- [ ] Crypto Name (Bitcoin, Ethereum, etc.)
- [ ] Crypto Category (Layer 1, DeFi, Exchange Token, etc.)
- [ ] Market Cap Tier (Large Cap, Mid Cap, Small Cap)
- [ ] Is Stablecoin (True/False)

**Test**: Create a view with Symbol and Name
**Expected**: 15 cryptocurrencies shown with names
**Status**: ☐ PASS ☐ FAIL

---

### Test 2.3: Portfolio Dimensions
**Location**: Tableau Workbook → Data Pane → Dimensions

Verify these portfolio dimensions appear:
- [ ] Portfolio ID (PF001, PF002, PF003)
- [ ] Portfolio Name (Conservative Growth, Balanced, High Growth)
- [ ] Risk Tolerance (Low, Medium, High)
- [ ] Risk Category (Conservative, Balanced, Aggressive)

**Test**: Create a view showing all 3 portfolios
**Expected**: 3 portfolios displayed with correct names
**Status**: ☐ PASS ☐ FAIL

---

## ✅ TEST CATEGORY 3: Measures

### Test 3.1: Price Measures
**Location**: Tableau Workbook → Data Pane → Measures

Verify these measures exist and aggregate correctly:

| Measure | Aggregation | Format | Test Value Range |
|---------|-------------|---------|------------------|
| Close Price | AVG | Currency | $0.10 - $100K |
| Open Price | AVG | Currency | $0.10 - $100K |
| High Price | MAX | Currency | $0.10 - $100K |
| Low Price | MIN | Currency | $0.10 - $100K |
| Volume | SUM | Number | > 0 |

**Test**: Drag `Close Price` to Text → Show AVG(Close Price)
**Expected**: Displays average crypto prices in $ format
**Status**: ☐ PASS ☐ FAIL

---

### Test 3.2: Portfolio Measures
**Location**: Tableau Workbook → Data Pane → Measures

Test these portfolio measures:

| Measure | Expected Value | Format |
|---------|---------------|---------|
| Position Value | $750,000 (total) | Currency |
| Position Quantity | Various | 8 decimals |
| Unrealized PnL | Various (+/-) | Currency |
| Total Portfolio Value | $750,000 | Currency |
| Asset Count | 10 unique assets | Number |

**Test**: Create table with Portfolio Name + Position Value
**Expected**: 
- Conservative Growth: $100,000
- Balanced Portfolio: $250,000
- High Growth: $500,000

**Status**: ☐ PASS ☐ FAIL

---

### Test 3.3: Trade Measures
**Location**: Tableau Workbook → Data Pane → Measures

Verify trade measures:
- [ ] Trade Amount (SUM, Currency)
- [ ] Trade Fee (SUM, Currency)
- [ ] Trade Count (COUNT DISTINCT, Number)

**Test**: Filter to recent 30 days, show total trade amount
**Expected**: Trade data displays, fees < 0.2% of amount
**Status**: ☐ PASS ☐ FAIL

---

### Test 3.4: Bollinger Bands Measures ⭐ NEW!
**Location**: Tableau Workbook → Data Pane → Measures

Verify Bollinger Bands measures exist:
- [ ] BB Middle (AVG, Currency) - 20-day SMA
- [ ] BB Upper (AVG, Currency) - Upper band (+2 std dev)
- [ ] BB Lower (AVG, Currency) - Lower band (-2 std dev)
- [ ] BB Bandwidth (AVG, Percentage) - Volatility indicator
- [ ] BB %B (AVG, Number 0-1) - Position within bands

**Test Procedure**:
1. Create a line chart with `Date` and `Close Price` for BTC
2. Add `BB Upper`, `BB Middle`, `BB Lower` to the chart
3. Synchronize axes (dual axis)
4. Filter to last 90 days

**Expected Results**:
- BB Middle ≈ Close Price (20-day average)
- BB Upper > BB Middle (typically 5-15% higher)
- BB Lower < BB Middle (typically 5-15% lower)
- Price oscillates between bands (~95% of time within bands)
- BB Bandwidth increases during volatile periods
- BB %B = 0.5 when price = BB Middle
- BB %B > 1.0 indicates price above upper band (overbought)
- BB %B < 0.0 indicates price below lower band (oversold)

**Sample Expected Values** (BTC, recent data):
- Close: $42,987.62
- BB Middle: $42,545.32
- BB Upper: $48,231.15
- BB Lower: $36,859.49
- BB Bandwidth: 26.72%
- BB %B: 0.65 (between middle and upper)

**Status**: ☐ PASS ☐ FAIL

---

### Test 3.5: Correlation Matrix Measures ⭐ NEW!
**Location**: Tableau Workbook → Data Pane → Measures

Verify correlation measures exist:
- [ ] Correlation Coefficient (AVG, Number -1 to 1)
- [ ] Correlation Period (Days) (AVG, Number)

**Test Procedure**:
1. Create a crosstab with `Crypto1` (rows) and `Crypto2` (columns)
2. Add `Correlation Coefficient` to Text
3. Format as heatmap (Red-White-Blue diverging color scale)
4. Center color scale at 0

**Expected Results**:
- Diagonal (self-correlations) = 1.0 (BTC-BTC, ETH-ETH, etc.)
- Matrix is symmetric: corr(A,B) = corr(B,A)
- Most values are positive (0.3 to 0.9) - crypto assets tend to move together
- All values between -1.0 and +1.0
- No NULL values

**Sample Expected Correlations**:
- BTC-BTC: 1.0000 (perfect self-correlation)
- BTC-ETH: 0.8412 (very strong positive - move together)
- UNI-BTC: 0.9967 (highest correlation in dataset)
- ADA-LTC: 0.3587 (lowest positive correlation - more independent)

**Interpretation Test**:
- [ ] High correlation (>0.7): Low diversification benefit
- [ ] Moderate correlation (0.4-0.7): Good diversification
- [ ] Low correlation (<0.4): Excellent diversification
- [ ] Negative correlation (<0): Hedging opportunity

**Status**: ☐ PASS ☐ FAIL

---

## ✅ TEST CATEGORY 4: Calculated Fields / KPIs

### Test 4.1: Volatility KPIs
**Location**: Tableau Workbook → Analytics Pane

**IMPORTANT**: Volatility measures use LOD expressions that require date filters to work correctly.

**Test A: Portfolio Volatility (30d)**
1. Create a new sheet
2. Add filter: Date → Relative Date → Last 30 days
3. Add Portfolio Name to Rows
4. Add Portfolio Volatility (30d) to Text
5. Format as percentage

**Expected**: 
- Values range: 15-50% (typical for crypto)
- Conservative Growth: ~20-25%
- Balanced Portfolio: ~25-35%
- High Growth: ~30-45%

**Status**: ☐ PASS ☐ FAIL

---

**Test B: Portfolio Volatility (90d)**
1. Create a new sheet
2. Add filter: Date → Relative Date → Last 90 days
3. Add Portfolio Name to Rows
4. Add Portfolio Volatility (90d) to Text

**Expected**:
- Values slightly lower/smoother than 30d
- Range: 15-45%

**Status**: ☐ PASS ☐ FAIL

---

**Test C: Portfolio Volatility (365d)**
1. Create a new sheet
2. Add filter: Date → Relative Date → Last 365 days
3. Add Portfolio Name to Rows
4. Add Portfolio Volatility (365d) to Text

**Expected**:
- Smoothest values (captures full year)
- Range: 20-40%

**Status**: ☐ PASS ☐ FAIL

---

### Test 4.2: Value at Risk (VaR)
**Location**: Tableau Workbook → Create Calculated Field

**IMPORTANT**: VaR uses LOD expression. Filter to latest date to avoid summing across all dates.

**Test VaR 95%**:
1. Create a new sheet
2. Add filter: as_of_date = MAX(as_of_date) OR as_of_date = '2026-01-09'
3. Add Portfolio Name to Rows
4. Add VaR 95% to Text
5. Check values are negative and reasonable

**Expected Values** (with latest date filter, from pre-calculated KPIs):
- Conservative Growth: **-$5,055** (5.2% of $97,288 portfolio value)
- Balanced Portfolio: **-$11,829** (4.7% of $251,740 portfolio value)
- High Growth: **-$23,403** (5.9% of $396,600 portfolio value)

**Validation**:
- [ ] All values are NEGATIVE
- [ ] Displayed in currency format
- [ ] Values are in thousands, NOT millions
- [ ] Larger portfolios have larger absolute VaR
- [ ] VaR is ~1.5-2.5% of portfolio value

**Status**: ☐ PASS ☐ FAIL

---

**Test VaR 99%**:
Repeat above test with VaR 99%

**Expected Values** (from pre-calculated KPIs):
- VaR 99% should be ~1.8x larger (more negative) than VaR 95%
- Conservative Growth: **-$9,126** (vs VaR 95%: -$5,055)
- Balanced Portfolio: **-$21,264** (vs VaR 95%: -$11,829)
- High Growth: **-$42,066** (vs VaR 95%: -$23,403)

**Validation**:
- [ ] VaR 99% ≠ VaR 95% (they must be different)
- [ ] VaR 99% is more negative than VaR 95%

**Status**: ☐ PASS ☐ FAIL

---

### Test 4.3: Sharpe Ratio
**Location**: Tableau Workbook

**Test**:
1. Create table: Portfolio Name × Sharpe Ratio
2. Add color: Red (< 0.5), Yellow (0.5-1.0), Green (> 1.0)

**Expected Values**:
- Conservative Growth: ~0.82
- Balanced Portfolio: ~0.80
- High Growth: ~0.75

**Validation**:
- [ ] All values between 0 and 3
- [ ] Decimal format (e.g., 0.82)
- [ ] Higher values = better risk-adjusted returns

**Status**: ☐ PASS ☐ FAIL

---

### Test 4.4: Beta vs BTC
**Location**: Tableau Workbook

**Test**:
1. Show Beta vs BTC for each portfolio
2. Add reference line at Beta = 1.0

**Expected**:
- Values between 0.5 and 1.5
- Beta = 1.0 means moves exactly with Bitcoin
- Beta < 1.0 = less volatile than BTC
- Beta > 1.0 = more volatile than BTC

**Validation**:
- [ ] Numeric format (e.g., 0.85)
- [ ] Values make sense relative to portfolio composition
- [ ] Reference line at 1.0 appears

**Status**: ☐ PASS ☐ FAIL

---

### Test 4.5: Position Concentration (HHI)
**Location**: Tableau Workbook

**Test**:
1. Show HHI for each portfolio
2. Add Diversification Score

**Expected HHI Values**:
- High Growth: ~0.145 (most diversified)
- Balanced: ~0.23
- Conservative: ~0.36 (most concentrated)

**Expected Diversification Scores**:
- High Growth: 85.5/100
- Balanced: 77.0/100
- Conservative: 64.0/100

**Validation**:
- [ ] HHI between 0.1 and 0.4
- [ ] Diversification Score = (1 - HHI) × 100
- [ ] Higher score = more diversified

**Status**: ☐ PASS ☐ FAIL

---

### Test 4.6: Max Drawdown
**Location**: Tableau Workbook

**Test**:
1. Create line chart with Date and Portfolio Value
2. Add Max Drawdown as reference line
3. Set to compute using Date

**Expected**:
- Negative percentage (e.g., -30%)
- Shows worst peak-to-trough decline
- Updates as you change date range

**Validation**:
- [ ] Displayed as negative %
- [ ] Value between -80% and 0%
- [ ] Makes sense visually on chart

**Status**: ☐ PASS ☐ FAIL

---

### Test 4.7: Current Weight & Weight Drift
**Location**: Tableau Workbook

**Test**:
1. Create table: Symbol × Current Weight × Target Weight × Weight Drift
2. Filter to one portfolio
3. Add conditional formatting: Red if ABS(drift) > 10%

**Expected**:
- Current Weight sums to ~100% per portfolio
- Weight Drift = Current - Target
- Some positions flagged red if drift > 10%

**Validation**:
- [ ] Current Weight shown as %
- [ ] Weights sum to 100% per portfolio
- [ ] Drift calculated correctly
- [ ] Conditional formatting works

**Status**: ☐ PASS ☐ FAIL

---

### Test 4.8: Liquid Assets %
**Location**: Tableau Workbook

**Test**:
1. Show Liquid Assets % for each portfolio
2. Add detail: Which assets count as "liquid"

**Expected**:
- Percentage between 40-80%
- "Liquid" = Layer 1 + Exchange Token categories
- Includes: BTC, ETH, BNB, SOL, ADA, XRP, LTC

**Validation**:
- [ ] Percentage format
- [ ] Reasonable value (not 0% or 100%)
- [ ] Only includes correct categories

**Status**: ☐ PASS ☐ FAIL

---

## ✅ TEST CATEGORY 5: Formulas & Calculations

### Test 5.1: Daily Return % Calculation
**Location**: Tableau Workbook

**Test**:
1. Show Daily Return % for BTC over last 30 days
2. Manually verify one day's calculation

**Formula**: `(Today's Close - Yesterday's Close) / Yesterday's Close × 100`

**Example**:
- Jan 9: $90,513.10
- Jan 8: Calculate expected return

**Validation**:
- [ ] Values are percentages (-10% to +10% typical)
- [ ] Can be positive or negative
- [ ] Match manual calculation

**Status**: ☐ PASS ☐ FAIL

---

### Test 5.2: LOD Expression - Position Weight %
**Location**: Tableau Workbook

**Test**:
1. Show Position Weight % for all positions in one portfolio
2. Sum the weights

**Formula**: `Position Value / TOTAL(Position Value) within Portfolio`

**Expected**:
- Each position shows weight as %
- All weights sum to 100%
- Changes correctly when filtering

**Validation**:
- [ ] Weights are percentages
- [ ] Sum = 100% per portfolio
- [ ] LOD calculation works with filters

**Status**: ☐ PASS ☐ FAIL

---

### Test 5.3: Table Calculation - WINDOW_STDEV
**Location**: Tableau Workbook

**Test Volatility Formula**:
1. Create view with Date × Daily Return %
2. Add table calculation: WINDOW_STDEV over -29 to 0
3. Multiply by SQRT(365) for annualization

**Expected**:
- Rolling 30-day standard deviation
- Properly computed along Date
- Annualized value (typically 20-50%)

**Validation**:
- [ ] Values update as date range changes
- [ ] Blank for first 29 days (insufficient data)
- [ ] Reasonable values (5-100%)

**Status**: ☐ PASS ☐ FAIL

---

## ✅ TEST CATEGORY 6: Business Preferences

### Test 6.1: Default Currency (USD)
**Location**: All currency fields

**Test**:
1. Check multiple currency fields
2. Verify $ symbol displayed

**Expected**: All monetary values show $ prefix
**Status**: ☐ PASS ☐ FAIL

---

### Test 6.2: Default Date Range (Last 90 Days)
**Location**: Dashboard initial load

**Test**:
1. Open fresh dashboard
2. Check date filter default

**Expected**: Filter set to "Last 90 Days"
**Status**: ☐ PASS ☐ FAIL

---

### Test 6.3: Precision Settings
**Location**: Measure formatting

**Test**:
- [ ] Prices: 2 decimal places ($90,513.10)
- [ ] Percentages: 2 decimal places (7.85%)
- [ ] Quantities: 8 decimal places (0.12345678)

**Status**: ☐ PASS ☐ FAIL

---

### Test 6.4: Risk Thresholds
**Location**: Conditional formatting rules

**Test**:
1. Check volatility conditional formatting
2. High risk = Red (> 25%)
3. Medium risk = Yellow (> 15%)
4. Low risk = Green (< 15%)

**Expected**: Colors apply correctly based on volatility
**Status**: ☐ PASS ☐ FAIL

---

## ✅ TEST CATEGORY 7: Data Quality

### Test 7.1: No NULL Values in Key Fields
**Location**: Data pane

**Test**: Create view showing COUNT and COUNT(DISTINCT) for:
- [ ] Symbol: 15 unique values, no nulls
- [ ] Date: ~2,200 dates, no nulls
- [ ] Portfolio ID: 3 unique values, no nulls
- [ ] Close Price: No nulls, all > 0

**Status**: ☐ PASS ☐ FAIL

---

### Test 7.2: Date Range Coverage
**Location**: Date field

**Test**:
1. Show MIN(Date) and MAX(Date)
2. Verify continuous coverage

**Expected**:
- MIN: 2020-01-01
- MAX: 2026-01-09 (or latest data)
- No gaps in daily data

**Status**: ☐ PASS ☐ FAIL

---

### Test 7.3: Portfolio Value Sum
**Location**: Measures

**Test**: Sum all Position Values across all portfolios

**Expected Total**: $750,000
- Conservative: $100,000 (13.3%)
- Balanced: $250,000 (33.3%)
- High Growth: $500,000 (66.7%)

**Status**: ☐ PASS ☐ FAIL

---

## ✅ TEST CATEGORY 8: Edge Cases

### Test 8.1: Weekend Data
**Location**: Filter on Is Weekend = TRUE

**Test**:
1. Filter to weekends only
2. Check if crypto data exists (should exist - crypto trades 24/7)

**Expected**: Data exists for weekends
**Status**: ☐ PASS ☐ FAIL

---

### Test 8.2: Zero Position Handling
**Location**: Portfolio positions

**Test**: Filter to Position Value < $100

**Expected**: 
- Small positions may be hidden (per min_position_size preference)
- No divide-by-zero errors
- Weights still calculate correctly

**Status**: ☐ PASS ☐ FAIL

---

### Test 8.3: Negative Returns
**Location**: Daily Return %

**Test**: Find days with negative returns

**Expected**:
- Negative values display correctly
- Charts show below zero
- Calculations work with negative inputs

**Status**: ☐ PASS ☐ FAIL

---

## ✅ TEST CATEGORY 9: Performance

### Test 9.1: Query Response Time
**Test**: Load a dashboard with all KPIs

**Timing**:
- Initial load: ______ seconds
- Filter change: ______ seconds
- Drill down: ______ seconds

**Expected**: < 5 seconds for most operations
**Status**: ☐ PASS ☐ FAIL

---

### Test 9.2: Large Date Range
**Test**: Set filter to "All Time" (2020-2026)

**Validation**:
- [ ] Dashboard loads without timeout
- [ ] All KPIs calculate
- [ ] Charts render correctly

**Status**: ☐ PASS ☐ FAIL

---

## 📊 SUMMARY REPORT

**Test Date**: _____________________
**Tester**: _____________________

### Results Overview

| Category | Tests | Passed | Failed | Notes |
|----------|-------|--------|--------|-------|
| 1. DMOs | 3 | ___ | ___ | |
| 2. Dimensions | 3 | ___ | ___ | |
| 3. Measures | 3 | ___ | ___ | |
| 4. KPIs | 8 | ___ | ___ | |
| 5. Formulas | 3 | ___ | ___ | |
| 6. Preferences | 4 | ___ | ___ | |
| 7. Data Quality | 3 | ___ | ___ | |
| 8. Edge Cases | 3 | ___ | ___ | |
| 9. Performance | 2 | ___ | ___ | |
| **TOTAL** | **32** | **___** | **___** | |

### Pass Rate: _____%

### Critical Issues Found:
1. _____________________________________
2. _____________________________________
3. _____________________________________

### Recommendations:
1. _____________________________________
2. _____________________________________
3. _____________________________________

### Sign-off:
- [ ] Semantic layer is production-ready
- [ ] Minor issues documented, not blocking
- [ ] Major issues require fixes before demo

**Tested By**: _____________________
**Date**: _____________________
**Signature**: _____________________

---

## 🔧 Troubleshooting Guide

### Issue: Measure shows NULL
**Solution**: 
- Check DMO relationships are active
- Verify data exists in source DMO
- Check filter isn't excluding all data

### Issue: KPI calculation error
**Solution**:
- Verify all required fields exist
- Check table calculation compute direction
- Ensure LOD expression uses correct dimension

### Issue: Weight doesn't sum to 100%
**Solution**:
- Check Position Weight % LOD expression
- Verify Portfolio ID is in context
- Ensure no missing positions

### Issue: Volatility shows as blank
**Solution**:
- Volatility uses LOD expressions that require date filters
- Add filter: Date → Relative Date → Last 30/90/365 days
- For 30d volatility: Filter to last 30 days
- For 90d volatility: Filter to last 90 days
- For 365d volatility: Filter to last 365 days
- The measure calculates volatility for the filtered period

### Issue: VaR values are in millions instead of thousands
**Root Cause**: Missing date join in DMO relationships causing cross-join across all dates.

**Solutions** (in order of priority):
1. **Fix DMO Relationships** (BEST FIX):
   - Navigate: Data Cloud → Data Model → Relationships
   - Edit: `dmo_kpi_var → dmo_portfolio_positions` relationship
   - Add second join condition: `as_of_date = as_of_date`
   - This prevents cross-joining VaR with all 365 position dates
   
2. **Temporary Workaround**:
   - Add filter in Tableau: `as_of_date = '2026-01-09'` (latest date)
   - This filters out extra dates but doesn't fix the underlying issue

**Expected After Fix**: VaR values should be -$5K to -$23K (not millions)

### Issue: Portfolio Values 100-400x too large ($36M instead of $97K)
**Root Cause**: Missing date joins on KPI relationships, causing summing across all 365 daily snapshots.

**Solution**:
- Verify ALL KPI relationships (4, 5, 6, 7b, 8) include date joins
- `dmo_kpi_volatility.date` = `dmo_portfolio_positions.as_of_date`
- `dmo_kpi_var.as_of_date` = `dmo_portfolio_positions.as_of_date`
- `dmo_kpi_risk_adjusted.as_of_date` = `dmo_portfolio_positions.as_of_date`
- `dmo_kpi_concentration.as_of_date` = `dmo_portfolio_positions.as_of_date`
- `dmo_kpi_24h_change.date` = `dmo_portfolio_positions.as_of_date`

### Issue: Sharpe Ratio is negative or wrong
**Root Cause**: Missing date join on `dmo_kpi_risk_adjusted` relationship, causing averaging across multiple dates.

**Solution**:
- Fix relationship with date join (see above)
- Add filter: `as_of_date = MAX(as_of_date)`
- Expected values: Conservative=0.19, Balanced=0.02, High Growth=0.04

### Issue: Values don't change across dates (constant)
**Root Cause**: Using `Crypto Prices.date` but portfolio data uses `Portfolio Positions.as_of_date` - wrong date field.

**Solution**:
- Use `Portfolio Positions.as_of_date` as dimension (not Crypto Prices.date)
- Or create a shared date dimension that joins both tables

---

## 📝 Notes Section

Use this space for additional observations during testing:

________________________________________
________________________________________
________________________________________
________________________________________
________________________________________
