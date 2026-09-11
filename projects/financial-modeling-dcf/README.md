# Financial Modeling & DCF Valuation

A compact corporate-finance project that illustrates a discounted cash flow (DCF) valuation using projected free cash flow to the firm (FCFF), WACC, terminal value, and sensitivity analysis.

## Objective

Estimate enterprise value and equity value from operating assumptions rather than relying only on market multiples.

## Methodology

1. Project revenue and operating margins.
2. Estimate EBIT and NOPAT.
3. Add back depreciation & amortization.
4. Deduct CAPEX and changes in net working capital.
5. Calculate FCFF.
6. Discount forecast cash flows using WACC.
7. Estimate terminal value using the Gordon Growth method.
8. Bridge enterprise value to equity value using net debt.
9. Test valuation sensitivity to WACC and terminal growth.

## Core formulas

```text
NOPAT = EBIT × (1 - Tax Rate)
FCFF = NOPAT + D&A - CAPEX - ΔNWC
Terminal Value = FCFF_(n+1) / (WACC - g)
Enterprise Value = PV(Explicit FCFF) + PV(Terminal Value)
Equity Value = Enterprise Value - Net Debt
```

## Files

- `dcf_model.py` — self-contained Python implementation using illustrative assumptions.

## What this demonstrates

- Integrated financial forecasting logic
- DCF valuation
- WACC and terminal-growth mechanics
- Scenario and sensitivity thinking
- Translation of operating assumptions into valuation outputs

## Disclaimer

All assumptions in this public project are illustrative and do not represent confidential information from any employer or client.
