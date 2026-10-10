# Portfolio Optimization & Risk

This project recreates part of the workflow I used when studying portfolio construction: compare individual assets, simulate combinations and inspect the trade-off between expected return and volatility.

The dataset is illustrative so the analysis can be reproduced without a paid market-data connection.

## Questions

- Which assets contribute most to portfolio volatility?
- What allocation produces the lowest simulated volatility?
- Which simulated portfolio has the highest Sharpe ratio?
- How different is an equal-weight portfolio from those two reference portfolios?

## Method

The script uses a small return matrix for four assets and:

1. annualizes mean returns and the covariance matrix;
2. simulates 10,000 long-only portfolios;
3. calculates expected return, volatility and Sharpe ratio for each one;
4. reports the minimum-volatility and maximum-Sharpe allocations;
5. compares them with an equal-weight portfolio.

The risk-free rate is an explicit input and can be changed in the script.

## Files

- `portfolio_optimization.py` — simulation and portfolio statistics.
- `requirements.txt` — Python dependencies.

## Run

```bash
pip install -r requirements.txt
python portfolio_optimization.py
```

## Why it is here

I participated in the Bloomberg Global Trading Challenge analyzing equities and ETFs with my team. We used Bloomberg Terminal for market information and Python for portfolio simulations. This public version keeps the same analytical logic but uses illustrative data rather than proprietary Bloomberg data.
