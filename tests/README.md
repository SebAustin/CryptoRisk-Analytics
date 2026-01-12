# CryptoRisk Analytics - Testing Suite

This directory contains comprehensive tests for validating the semantic layer configuration and Concierge AI responses.

## Files

### 1. `semantic_layer_manual_tests.md`
**Purpose**: Manual testing checklist for semantic layer validation in Tableau Data Cloud

**Test Coverage** (32 tests across 9 categories):
- ✅ Data Model Objects (DMOs) - 3 tests
- ✅ Dimensions (Date, Crypto, Portfolio) - 3 tests
- ✅ Measures (Prices, Portfolio, Trades) - 3 tests
- ✅ KPIs/Calculated Fields (Volatility, VaR, Sharpe, Beta, etc.) - 8 tests
- ✅ Formulas & Calculations (LOD, Table Calcs) - 3 tests
- ✅ Business Preferences - 4 tests
- ✅ Data Quality - 3 tests
- ✅ Edge Cases - 3 tests
- ✅ Performance - 2 tests

**How to Use**: Open file and follow step-by-step checklist in Tableau Data Cloud

### 2. `concierge_test_prompts.yaml`
**Purpose**: Comprehensive test suite for validating Concierge AI accuracy

**Test Categories** (33 total tests):
1. **Basic Portfolio Queries** (3 tests)
   - Largest portfolios identification
   - Position listing with correct fields
   - Total portfolio value calculations

2. **Crypto Price Queries** (3 tests)
   - Current price retrieval
   - Performance rankings
   - Volatility analysis

3. **Risk Analysis** (3 tests)
   - Risk portfolio identification
   - Value at Risk (VaR) calculations
   - Sharpe Ratio interpretation

4. **Portfolio Management** (3 tests)
   - Rebalancing recommendations
   - Overweight/underweight detection
   - Diversification scoring

5. **Trading History** (3 tests)
   - Recent trades filtering
   - Most traded crypto (by USD volume)
   - Trading fees analysis

6. **Market Analysis** (2 tests)
   - Market sentiment assessment
   - Market volatility trends

7. **Comparative Analysis** (2 tests)
   - Portfolio vs Bitcoin (Beta, Alpha)
   - Asset-to-asset comparisons

8. **Business Preferences** (3 tests)
   - Domain language interpretation
   - Liquid assets calculation
   - Default sorting behaviors

9. **Time-Based Queries** (2 tests)
   - Date range filtering
   - YTD calculations

10. **Alerts & Actions** (2 tests)
    - Risk alert triggers
    - Action recommendations

## How to Use

### Performing Semantic Layer Manual Tests

1. **Open** `tests/semantic_layer_manual_tests.md`
2. **Follow** the step-by-step checklist
3. **Test in** Tableau Data Cloud workbook
4. **Check** boxes as you complete each test
5. **Record** results in the Summary Report section

**Estimated Time**: 45-60 minutes for all 32 tests

### Using Concierge Test Prompts

1. **Open Tableau Data Cloud** Concierge AI
2. **Navigate to** `tests/concierge_test_prompts.yaml`
3. **For each test**:
   - Copy the `prompt` field
   - Paste into Concierge AI
   - Compare response with `expected_answer`
   - Check that all `key_elements` are present
   - Verify correct `data_sources` are used
   - Confirm `business_logic` is applied

4. **Pass Criteria**:
   - ✅ 90% of key elements present
   - ✅ Correct DMOs referenced
   - ✅ Business logic correctly applied
   - ✅ Proper formatting (%, $, dates)

### Example Test Workflow

**Test ID: BP-001**

```yaml
prompt: "What are my largest portfolios?"

expected_answer: |
  The largest portfolios by total value are:
  1. High Growth (PF003): $500,000
  2. Balanced Portfolio (PF002): $250,000
  3. Conservative Growth (PF001): $100,000

key_elements:
  - "Sorted by portfolio value (descending)"
  - "All three portfolio names shown"
  - "Correct portfolio values"
```

**How to Test**:
1. Ask Concierge: "What are my largest portfolios?"
2. Check response includes:
   - ✅ Three portfolios listed
   - ✅ Sorted by value (highest first)
   - ✅ Values shown ($500K, $250K, $100K)
3. Mark as PASS if all key elements present

## Test Results Tracking

Create a simple tracking sheet:

| Test ID | Category | Status | Notes |
|---------|----------|--------|-------|
| BP-001  | Portfolio | ✅ PASS | All elements present |
| BP-002  | Portfolio | ⚠️ PARTIAL | Missing current weight |
| CP-001  | Prices | ✅ PASS | Correct price shown |
| RA-001  | Risk | ✅ PASS | Risk metrics correct |

## Critical Tests (Must Pass)

These tests are essential for core functionality:

- ✅ **BP-001**: Largest portfolios
- ✅ **CP-001**: Bitcoin price
- ✅ **RA-001**: Highest risk portfolio
- ✅ **RA-002**: Value at Risk calculation
- ✅ **PM-001**: Rebalancing needs
- ✅ **BP-001** (Business): Business preference validation

## Known Issues

### Semantic Layer Tests
1. **Table Calculations**: May need manual configuration of "Compute Using" direction
   - **Solution**: Set to compute along Date dimension
   - **Affects**: Volatility, Max Drawdown calculations

2. **LOD Expressions**: May require Portfolio ID in view context
   - **Solution**: Add Portfolio ID to detail shelf
   - **Affects**: Position Weight %, Current Weight

### Concierge AI Tests
1. **Data Freshness**: Tests assume latest data (Jan 9, 2026)
   - **Mitigation**: Update expected values when data refreshes

2. **Portfolio Values**: Based on current positions
   - **Mitigation**: Re-run data generation if values change

## Continuous Testing

### Before Deployment
- [ ] Complete all 32 semantic layer manual tests
- [ ] Achieve 90%+ pass rate
- [ ] Document any failures and workarounds

### After Data Refresh
- [ ] Re-test KPI calculations (Tests 4.1-4.8)
- [ ] Verify data quality (Tests 7.1-7.3)
- [ ] Update expected values in test checklist
- [ ] Re-run Concierge test prompts

### Before Demo/Presentation
- [ ] Quick test: Top 10 critical tests from checklist
- [ ] Test 10 critical Concierge prompts
- [ ] Verify all dashboards load
- [ ] Check Agentforce actions work

## Test Automation Opportunities

**Future Enhancements**:
1. Convert manual tests to automated Tableau API tests
2. Add performance benchmarks (query response time)
3. Implement regression tests for formula changes
4. Create visual diff tool for dashboard changes
5. Add data quality tests for uploaded CSVs

## Troubleshooting

### Test Failures

**Issue**: KPI shows NULL or blank
```
Solution: 
1. Check DMO relationships are configured
2. Verify data exists in all related tables
3. Check if minimum data required (e.g., 30 days for volatility)
```

**Issue**: Table calculation not computing correctly
```
Solution:
1. Right-click measure → Edit Table Calculation
2. Set "Compute Using" to appropriate dimension (usually Date)
3. Verify "Specific Dimensions" if using multiple
```

**Issue**: Concierge gives unexpected results
- Check business preferences are loaded
- Verify semantic layer is published
- Confirm data is up-to-date
- Review grounding rules in concierge_config.yaml

## Success Metrics

**Semantic Layer Manual Tests**:
- ✅ 28+ tests passing (out of 32) = 90%+ pass rate
- ✅ All Category 4 (KPI) tests passing
- ✅ All Category 3 (Measures) tests passing
- ✅ Performance tests < 5 seconds
- ✅ Zero critical errors

**Concierge AI Tests**:
- ✅ 30+ prompts passing (out of 33) = 90%+ pass rate
- ✅ All key elements present in responses
- ✅ Correct data sources used
- ✅ Business logic applied correctly
- ✅ Formatting consistent (%, $)

## Quick Reference

**Testing Files**:
- `semantic_layer_manual_tests.md` - Complete 32-test checklist (45-60 min)
- `concierge_test_prompts.yaml` - 33 AI validation prompts
- `README.md` (this file) - Testing overview and guide

**Key Resources**:
- `config/semantic_layer_config.yaml` - Formula definitions and KPI specs
- `docs/data_cloud_setup.md` - DMO configuration guide
- `docs/dashboard_wireframes.md` - Dashboard specifications

**For Questions**:
1. Check troubleshooting section in manual test file
2. Review semantic layer YAML for formula definitions
3. See Concierge test prompts for expected AI behaviors
