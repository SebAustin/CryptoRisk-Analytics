# CryptoRisk Analytics - Dashboard Wireframes

Complete specifications for 2 production-ready dashboards using Tableau Next visualization capabilities.

---

## Overview

**Dashboard Suite**: CryptoRisk Analytics
**Target Platform**: Tableau Next (Salesforce)
**User Personas**:
- Portfolio Managers (executive view, risk monitoring)
- Risk Analysts (detailed analytics, technical indicators)

**Design Principles**:
- Mobile-responsive layouts
- Accessible color palettes (WCAG AA compliant)
- Insight-oriented (clear risk decomposition and correlation analysis)
- Real-time refresh capability

---

## Dashboard 1: Portfolio Risk Radar

**Purpose**: Executive-level risk monitoring and portfolio health check
**Target Audience**: Portfolio Managers, CROs, Executives
**Refresh**: Real-time
**Size**: Desktop (1920x1080), Tablet-optimized

### Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  PORTFOLIO RISK RADAR                    [Last Updated: Now]    │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐  │
│  │ Total   │ │ 24h     │ │ VaR 95% │ │ Sharpe  │ │ Diversif │  │
│  │ Value   │ │ Change  │ │         │ │ Ratio   │ │ Score    │  │
│  │$850K    │ │+2.3%    │ │-$18.5K  │ │ 0.89    │ │ 75/100   │  │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └──────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────┐  ┌────────────────────────┐   │
│  │   RISK GAUGE                │  │  TOP HOLDINGS          │   │
│  │                             │  │  ┌──────────────────┐  │   │
│  │        ┌──────┐            │  │  │ BTC   $245K   ██ │  │   │
│  │        │  52  │            │  │  │ ETH   $182K   ██ │  │   │
│  │        │ /100 │            │  │  │ SOL   $115K   █  │  │   │
│  │        └──────┘            │  │  │ BNB   $98K    █  │  │   │
│  │   [Medium Risk Level]      │  │  │ AVAX  $87K    █  │  │   │
│  │                             │  │  └──────────────────┘  │   │
│  └─────────────────────────────┘  └────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │   PORTFOLIO COMPOSITION (Donut Chart)                     │  │
│  │                                                            │  │
│  │           Layer 1: 65% (BTC, ETH, SOL)                   │  │
│  │           DeFi: 15% (UNI, LINK)                          │  │
│  │           Layer 2: 12% (MATIC, AVAX)                     │  │
│  │           Other: 8%                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │   90-DAY PERFORMANCE (Line Chart)                         │  │
│  │   800K ┤                                    ╱─╲           │  │
│  │   750K ┤                     ╱─╲          ╱   ╲          │  │
│  │   700K ┤        ╱─╲        ╱   ╲        ╱     ╲         │  │
│  │   650K ┼──────╱───╲──────╱─────╲──────╱───────╲────    │  │
│  │        └──────────────────────────────────────────────   │  │
│  │         Oct        Nov         Dec         Jan           │  │
│  └──────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │   RISK HEATMAP BY ASSET CATEGORY                          │  │
│  │                                                            │  │
│  │   Layer 1     [██████░░░░] Low Risk                      │  │
│  │   DeFi        [████████░░] Medium Risk                   │  │
│  │   Layer 2     [███████░░░] Medium Risk                   │  │
│  │   Exchange    [█████░░░░░] Low-Medium Risk               │  │
│  │   Meme        [██████████] High Risk                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Component Specifications

#### 1. KPI Cards (Top Row)

**Total Value Card**:
- **Viz Type**: BAZ (Big Ass Zero) number card
- **Data**: `SUM(Position Value)`
- **Format**: Currency, $0.0K abbreviation
- **Color**: Green if up, Red if down
- **Tooltip**: "Portfolio value across all holdings"

**24h Change Card**:
- **Viz Type**: Number with trend indicator
- **Data**: `(Current Value - Value 24h ago) / Value 24h ago * 100`
- **Format**: Percentage, 1 decimal
- **Trend**: Up/Down arrow
- **Color**: Conditional (>0 green, <0 red, =0 gray)

**VaR 95% Card**:
- **Viz Type**: Number with alert badge
- **Data**: `VaR 95%` KPI
- **Format**: Currency, negative highlighted
- **Alert**: Red badge if exceeds threshold
- **Tooltip**: "Maximum expected loss at 95% confidence"

**Sharpe Ratio Card**:
- **Viz Type**: Number with star rating
- **Data**: `Sharpe Ratio` KPI
- **Format**: Decimal, 2 places
- **Stars**: Visual rating (>2=5 stars, 1.5-2=4 stars, etc.)
- **Tooltip**: "Risk-adjusted return quality"

**Diversification Score Card**:
- **Viz Type**: Progress bar + number
- **Data**: `Diversification Score` KPI
- **Format**: Number/100
- **Color**: Red <60, Yellow 60-80, Green >80
- **Tooltip**: "Portfolio concentration (higher = better)"

#### 2. Risk Gauge

**Viz Type**: Gauge chart (semicircle)

**Dimension**: `Portfolio Name` (Portfolio Positions.portfolio_name)
- **Filter Required**: Select one portfolio to display
  - Options: "Conservative Growth", "Balanced Portfolio", "High Growth"
  - Or use dashboard parameter for portfolio selection

**Measure**: Composite Risk Score (0-100)
- **Formula**: 
  ```
  ([Portfolio Volatility (30d)] * 0.30 + 
   [Position Concentration (HHI)] * 100 * 0.40 + 
   ABS([Max Drawdown]) * 100 * 0.30)
  ```
- **Description**: Weighted risk score combining volatility (30%), concentration (40%), and max drawdown (30%)

**Ranges**:
- 0-35: Low Risk (Green) 🟢
- 35-65: Medium Risk (Yellow) 🟡
- 65-100: High Risk (Red) 🔴

**Display**:
- **Needle**: Current risk score
- **Label**: Risk level text below gauge ("Low Risk", "Medium Risk", "High Risk")
- **Tooltip**: Show breakdown of components

**Alternative Layout** (if showing all portfolios):
- Display 3 small gauges side-by-side, one per portfolio
- Each labeled with portfolio name

#### 3. Top Holdings

**Viz Type**: Horizontal bar chart
- **Data**: Top 5 positions by `Position Value`
- **Bars**: Length = value, color by category
- **Labels**: Symbol + USD value
- **Sort**: Descending by value
- **Interactivity**: Click to drill into Asset Performance dashboard

#### 4. Portfolio Composition

**Viz Type**: Donut chart
- **Data**: `Position Value` grouped by `Crypto Category`
- **Slices**: Colored by category
- **Labels**: Category name + percentage
- **Center**: Total portfolio value
- **Legend**: Right side, ordered by size
- **Interactivity**: Hover for detailed breakdown

#### 5. 90-Day Performance

**Viz Type**: Line chart with area fill
- **Data**: Daily `Total Portfolio Value` over last 90 days
- **X-axis**: Date (daily granularity)
- **Y-axis**: Portfolio value ($)
- **Line**: Blue, 2px thickness
- **Area fill**: Light blue gradient
- **Reference line**: Starting value (dotted)
- **Annotations**: Peak and trough values
- **Interactivity**: Hover for daily value + change %

#### 6. Risk Heatmap by Category

**Viz Type**: Horizontal bar chart with gradient
- **Data**: Average `Volatility_30d` by `Crypto Category`
- **Bars**: Full width, colored by risk level
- **Color scale**: Green (low) → Yellow (med) → Red (high)
- **Labels**: Category name + risk level text
- **Sort**: Descending by volatility

### Filters (Top Right)

- **Portfolio**: Dropdown (All | Conservative | Balanced | Aggressive)
- **Date Range**: Date picker (default: Last 90 Days)
- **Asset Category**: Multi-select (default: All)

### Actions

- **"View Details" button** → Navigate to Asset Performance dashboard
- **"Rebalance Portfolio" button** → Trigger Agentforce rebalancing flow
- **"Export Report" button** → Generate PDF summary

---

## Dashboard 2: Asset Performance Deep Dive

**Purpose**: Detailed asset-level analytics and technical analysis
**Target Audience**: Portfolio Analysts, Traders
**Refresh**: Every 5 minutes
**Size**: Desktop (1920x1080)

### Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  ASSET PERFORMANCE                  [Asset: BTC ▼]              │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────────┐ │
│  │   PRICE CHART WITH VOLUME (Combo Chart)                   │ │
│  │   $45K ┤                                        ╱──╲      │ │
│  │   $40K ┤                     ╱────╲           ╱    ╲     │ │
│  │   $35K ┼────────────────────╱──────╲─────────╱──────╲   │ │
│  │   $30K ┤                              ╲────╱            │ │
│  │        └──────────────────────────────────────────────   │ │
│  │  Vol   │  ▁▂▃▅▇█▇▅▃▂▁▂▃▅▇█▇▅▃▂▁▂▃▅▇█▇▅▃▂▁       (bars) │ │
│  └───────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────┐  ┌──────────────────────────┐   │
│  │ RETURNS DISTRIBUTION     │  │  CORRELATION MATRIX      │   │
│  │  (Histogram)             │  │  (Heatmap)               │   │
│  │     │                    │  │                          │   │
│  │  30 ┤    ╭─╮            │  │     BTC ETH SOL BNB      │   │
│  │  20 ┤  ╭─┤ ├─╮          │  │  BTC[██][▓▓][░░][░░]    │   │
│  │  10 ┤╭─┤ │ │ ├─╮        │  │  ETH[▓▓][██][▓▓][░░]    │   │
│  │   0 ┴┴─┴─┴─┴─┴─┴──      │  │  SOL[░░][▓▓][██][▒▒]    │   │
│  └──────────────────────────┘  └──────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐ │
│  │   TECHNICAL INDICATORS (Multi-line Chart)                 │ │
│  │                                                            │ │
│  │   ─── Price (Close)                                       │ │
│  │   ─ ─ MA 7                                                │ │
│  │   ···· MA 30                                              │ │
│  │   [Lines showing price and moving averages over time]     │ │
│  └──────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────┐  ┌──────────────────────────┐   │
│  │ TRADE HISTORY (Table)    │  │  VS BENCHMARK (Scatter)  │   │
│  │ Date   Type Qty   Price  │  │                          │   │
│  │ 1/10   BUY  0.5   $42K   │  │      ●                   │   │
│  │ 1/05   SELL 0.3   $41K   │  │  ●       ● ●             │   │
│  │ 12/28  BUY  0.8   $39K   │  │      ● ●   ●             │   │
│  │ 12/15  BUY  1.2   $38K   │  │  ● ●   ●                 │   │
│  │ [pagination controls]    │  │  (Asset vs BTC returns)  │   │
│  └──────────────────────────┘  └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Component Specifications

#### 1. Price Chart with Volume

**Viz Type**: Dual-axis line and bar chart

**Primary Chart (Price)**:
- **Viz Type**: Line chart with range area
- **Data**: 
  - Line: `Close Price` by `Date`
  - Shaded area: Range between `High` and `Low` (use Gantt bar)
  - Color: Conditional based on daily return
    - Green if `Close > Open` (up day)
    - Red if `Close < Open` (down day)
- **Y-Axis**: Price (USD)
- **Moving Averages**: Add MA 7 and MA 30 as reference lines

**Secondary Chart (Volume)** - Separate sheet below:
- **Viz Type**: Bar chart
- **Data**: `Volume` by `Date`
- **Color**: Synchronized with price
  - Green if price up that day
  - Red if price down that day
- **Y-Axis**: Volume
- **Height**: 20% of dashboard height

**Dashboard Layout**:
```
┌────────────────────────────┐
│  Price Chart (80% height)  │
│  Line + High/Low range     │
├────────────────────────────┤
│  Volume Bars (20% height)  │
└────────────────────────────┘
```

**Alternative Option - Simpler Implementation**:
- Just use **Close Price line chart** with dual axis
- **Primary Axis**: Close Price (line)
- **Secondary Axis**: Volume (bars, semi-transparent)
- **Color**: Conditional formatting by daily return
- **Time Range Selector**: Parameter control (1M, 3M, 6M, 1Y, All)
- **Tooltip**: Date, Open, High, Low, Close, Volume, Daily % Change

#### 2. Returns Distribution

**Viz Type**: Histogram
- **Data**: `Daily Return %` distribution
- **Bins**: 20 bins from -10% to +10%
- **Color**: Blue bars
- **Overlay**: Normal distribution curve (dotted)
- **Reference lines**: 
  - Mean return (solid)
  - ±1 std dev (dashed)
- **Stats box**: Mean, Median, Std Dev displayed
- **Tooltip**: Bin range + count + percentage

#### 3. Correlation Matrix Heatmap

**Viz Type**: Heatmap (Square/Grid)

**Data Source**: `dmo_correlation_matrix` (pre-calculated in Python)

**Setup**:
- **Columns**: `Crypto1` (from Correlation Matrix)
- **Rows**: `Crypto2` (from Correlation Matrix)
- **Mark Type**: Square
- **Color**: `Correlation Coefficient`
- **Label**: `Correlation Coefficient` (show value in each cell)

**Color Scale** (Diverging):
- **Palette**: Red-White-Blue Diverging
- **Center**: 0 (White - no correlation)
- **High**: +1.0 (Dark Blue - perfect positive correlation)
- **Low**: -1.0 (Dark Red - perfect negative correlation)
- **Steps**: Continuous or 7 steps

**Recommended Color Breaks**:
```
-1.0 to -0.7: Dark Red (Strong negative)
-0.7 to -0.4: Light Red (Moderate negative)
-0.4 to -0.1: Pale Red (Weak negative)
-0.1 to +0.1: White (No correlation)
+0.1 to +0.4: Pale Blue (Weak positive)
+0.4 to +0.7: Light Blue (Moderate positive)
+0.7 to +1.0: Dark Blue (Strong positive)
```

**Filters**:
- **Option 1: Top N Assets**: 
  - Create parameter `Top N` (default: 10)
  - Filter to top N by market cap or portfolio holdings
  - Keeps matrix readable
- **Option 2: Portfolio Holdings**:
  - Filter to only assets in selected portfolio
  - Shows diversification through correlation
- **Option 3: Category Filter**:
  - Filter by crypto category (Layer 1, DeFi, etc.)
  - Shows intra-category correlations

**Formatting**:
- **Cell Size**: Auto or fixed (50x50 pixels)
- **Font**: Bold, size 10, white or black (contrast with background)
- **Borders**: Light gray, 1px
- **Diagonal Highlight**: Can use reference line or formatting rule to highlight self-correlations (always 1.0)

**Tooltip Template**:
```
<Crypto1> vs <Crypto2>
Correlation: <Correlation Coefficient>

Strength: <Correlation Strength>
Direction: <Correlation Direction>

Period: <Period Start> to <Period End> (<Period Days> days)

Interpretation:
• Perfect: ±1.0 (move identically/oppositely)
• Very Strong: ±0.8 to ±0.99
• Strong: ±0.6 to ±0.79
• Moderate: ±0.4 to ±0.59
• Weak: ±0.2 to ±0.39
• Very Weak: ±0.0 to ±0.19
```

**Calculated Fields** (Optional enhancements):
- **Absolute Correlation**: `ABS([Correlation Coefficient])` - Filter out weak correlations
- **Off-Diagonal Only**: `IF [Crypto1] != [Crypto2] THEN [Correlation Coefficient] END` - Exclude self-correlations from calculations

**Interactive Features**:
- **Click**: Select a crypto to highlight its row and column
- **Hover**: Show full tooltip with interpretation
- **Export**: Allow export as image or data for further analysis

**Business Insights**:
- **High positive correlation (>0.7)**: Assets move together - low diversification benefit
- **Low correlation (<0.3)**: Assets move independently - good diversification
- **Negative correlation (<-0.3)**: Assets move opposite - excellent hedging opportunity
- **Diagonal (1.0)**: Self-correlation, always perfect

**Implementation Note**: 
All correlations are pre-calculated in the Python ETL script (`prepare_crypto_data.py`) using 365-day rolling returns and stored in `correlation_matrix.csv`. Simply drag `Crypto1` and `Crypto2` to Columns/Rows and `Correlation Coefficient` to Color and Label.

#### 4. Technical Indicators with Bollinger Bands

**Viz Type**: Multi-line chart with shaded area

**Primary Chart (Price + Moving Averages)**:
- **Lines**:
  - `Close` price (solid blue line, 2px)
  - `MA 7` (dashed green line, 1px)
  - `MA 30` (dotted orange line, 1px)
  - `BB Middle` (solid black line, 1px, 20-day SMA)
  - `BB Upper` (dotted red line, 1px, +2σ)
  - `BB Lower` (dotted red line, 1px, -2σ)
- **Shaded Area**: Between `BB Upper` and `BB Lower` (light gray, 20% opacity)
- **X-axis**: Date
- **Y-axis**: Price ($)

**Secondary Chart (Below) - Bollinger Band Indicators**:
- **BB %B** (line chart, 0-1 scale):
  - Shows position within bands
  - Reference lines at 0, 0.5, 1.0
  - Color: Blue when 0.2-0.8 (normal), Red when >0.8 (overbought), Green when <0.2 (oversold)
- **BB Bandwidth** (bar chart):
  - Shows volatility (band width %)
  - Color gradient: Green (low vol) to Red (high vol)

**Data Fields Used**:
- From `dmo_crypto_prices`:
  - `close` - Current price
  - `ma_7` - 7-day moving average
  - `ma_30` - 30-day moving average
  - `bb_middle` - Bollinger Band middle line (20-day SMA)
  - `bb_upper` - Upper band (+2 standard deviations)
  - `bb_lower` - Lower band (-2 standard deviations)
  - `bb_percent` - %B indicator (position within bands)
  - `bb_bandwidth` - Band width percentage (volatility indicator)

**Trading Signals** (via calculated fields or color):
- **Overbought**: Price > `bb_upper` OR `bb_percent` > 1.0 (red highlight)
- **Oversold**: Price < `bb_lower` OR `bb_percent` < 0.0 (green highlight)
- **Squeeze**: `bb_bandwidth` < 10% (yellow background - low volatility)
- **Expansion**: `bb_bandwidth` increasing (potential breakout)

**Legend**: Top right, interactive (click to hide/show lines)

**Interactivity**: 
- Zoom with mouse drag
- Pan with arrow keys
- Reset zoom button
- Hover tooltip shows all values for that date

**Tooltip Template**:
```
Date: <Date>
Close: $<Close>
---
BB Upper: $<bb_upper>
BB Middle: $<bb_middle>
BB Lower: $<bb_lower>
---
%B: <bb_percent> (<Signal: Normal/Overbought/Oversold>)
Bandwidth: <bb_bandwidth>% (<Volatility: Low/Medium/High>)
---
MA(7): $<ma_7>
MA(30): $<ma_30>
```

**Implementation Note**: 
All Bollinger Band calculations are pre-computed in the Python ETL script (`prepare_crypto_data.py`) and stored in `crypto_prices_daily_2020_2024.csv`. Simply drag the fields to Rows and use dual-axis + synchronized axis to overlay them on the same chart.

#### 5. Trade History Table

**Viz Type**: Data table with sorting
- **Columns**:
  - Trade Date (date format)
  - Type (BUY/SELL with colored badge)
  - Quantity (8 decimals)
  - Price (currency)
  - Amount (currency)
  - Fee (currency)
  - Exchange (text)
- **Features**:
  - Sort by any column
  - Search/filter box
  - Pagination (10 rows/page)
  - Export to CSV
- **Conditional formatting**:
  - BUY rows: light green background
  - SELL rows: light red background

#### 6. Performance vs Benchmark

**Viz Type**: Scatter plot
- **X-axis**: Benchmark return (BTC)
- **Y-axis**: Asset return
- **Points**: Each point = 1 day
- **Color**: By month
- **Size**: By volume
- **Reference lines**:
  - X=0 (vertical, benchmark flat)
  - Y=0 (horizontal, asset flat)
  - Y=X (diagonal, perfect correlation)
- **Trend line**: Linear regression
- **Tooltip**: Date + both returns + volume

### Filters & Parameters

**Top Bar**:
- **Asset Selector**: Dropdown (all cryptos)
- **Date Range**: Date picker
- **Comparison Asset**: Dropdown (for benchmark)
- **Chart Type**: Toggle (Candlestick | Line | Area)

**Parameters**:
- **MA Periods**: Inputs for moving average windows (default 7, 30)
- **Correlation Window**: Days for correlation calc (default 90)

### Actions

- **"Add to Watchlist"** → Save asset to custom watch list
- **"Trade"** → Open trade entry form (if connected to exchange)
- **"Set Alert"** → Create price alert trigger
- **"Compare Assets"** → Open comparison view

---

## Visualization Type Summary

Across both dashboards, we use:

✅ **Tables**: Data grids with sorting/filtering
✅ **Bar Charts**: Horizontal, stacked, grouped
✅ **Line Charts**: Single, multi-line, with area fill
✅ **Donut/Pie Charts**: Portfolio composition
✅ **Treemaps**: Concentration visualization
✅ **Scatter Plots**: Correlation analysis
✅ **Heatmaps**: Correlation matrix, risk matrix
✅ **Gauges**: Risk score indicator
✅ **KPI Cards**: Big number displays
✅ **Histograms**: Return distribution
✅ **Candlestick Charts**: Price OHLC data
✅ **Combo Charts**: Price + volume
✅ **Area Charts**: Drawdown analysis

---

## Color Palette

**Primary Colors**:
- Blue: #1E40AF (Primary actions, lines)
- Green: #10B981 (Positive, buy, low risk)
- Red: #EF4444 (Negative, sell, high risk)
- Yellow: #F59E0B (Warning, medium risk)
- Purple: #8B5CF6 (Accent, highlights)

**Neutral Colors**:
- Dark Gray: #1F2937 (Text)
- Medium Gray: #6B7280 (Secondary text)
- Light Gray: #F3F4F6 (Backgrounds)
- White: #FFFFFF (Cards, panels)

**Accessibility**:
- All color combinations meet WCAG AA standards
- Colorblind-safe palette (uses shapes + colors)
- High contrast mode available

---

## Responsive Design

**Desktop** (1920x1080):
- Full layout as shown above
- Side-by-side visualizations
- Hover tooltips enabled

**Tablet** (768x1024):
- Stack visualizations vertically
- Collapse filters into dropdown
- Touch-optimized buttons (larger)

**Mobile** (375x667):
- Single column layout
- KPI cards in 2x2 grid
- Tables become scrollable cards
- Charts simplified (fewer data points)

---

## Performance Optimization

- **Lazy loading**: Load charts as user scrolls
- **Data extracts**: Pre-aggregate for fast rendering
- **Caching**: 5-minute cache for expensive calculations
- **Progressive rendering**: Show skeleton UI while loading
- **Query optimization**: Use Data Cloud indexed fields

---

## Next Steps

1. ✅ Dashboard designs complete (2 dashboards)
2. → Implement Dashboard 1 (Portfolio Risk Radar) in Tableau Next
3. → Implement Dashboard 2 (Asset Performance Deep Dive) in Tableau Next
4. → Connect to Data Cloud DMOs (11 DMOs, 8 relationships)
5. → Test cross-filtering and drill-downs
6. → Validate all formulas and calculated fields
7. → Optional: Implement Dashboard 3 (Risk Alert Center) with Agentforce actions

---

## References

- [Tableau Best Practices](https://help.tableau.com/current/pro/desktop/en-us/dashboards_best_practices.htm)
- [Data Visualization Catalog](https://datavizcatalogue.com/)
- [Salesforce Lightning Design System](https://www.lightningdesignsystem.com/)
