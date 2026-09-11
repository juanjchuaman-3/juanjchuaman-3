# Market Risk — Value at Risk (VaR)

A compact market-risk project illustrating parametric and historical Value at Risk for a simplified portfolio.

## Objective

Estimate potential portfolio losses over a chosen confidence level and holding period, while making the assumptions explicit.

## Methods

### Parametric VaR

Assumes returns are approximately normally distributed.

```text
VaR = Portfolio Value × z × σ × √t
```

Where:
- `z` is the standard-normal critical value,
- `σ` is daily volatility,
- `t` is the holding period in days.

### Historical VaR

Uses empirical portfolio returns and selects the relevant lower-tail percentile without imposing a normal distribution.

## Files

- `var_analysis.py` — illustrative implementation of parametric and historical VaR.

## What this demonstrates

- Market-risk measurement
- Volatility scaling
- Confidence-level interpretation
- Historical simulation
- Risk-reporting logic

## Disclaimer

This project is educational. The data and assumptions are illustrative and are not investment recommendations.
