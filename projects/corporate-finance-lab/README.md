# Corporate Finance & Portfolio Analytics Lab

An interactive financial-modeling case study focused on **FP&A, valuation, corporate finance and portfolio analytics**.

**All data are illustrative / synthetic**, not actual company financials or investment recommendations.

## Components
- `model.py`: five-year income statement, balance sheet, cash flow, FCFF and enterprise-to-equity DCF valuation.
- `portfolio.py`: deterministic synthetic market data, annualized Sharpe/volatility, historical 1-day VaR/CVaR and long-only minimum-variance allocation.
- `app.py`: Streamlit interface, sensitivity matrix, interactive financial drivers and CSV export.
- `tests/test_models.py`: unit tests for reconciliation, DCF identities and portfolio constraints.
- `requirements.txt`: Python dependencies.
- **Excel** and **Colab** companion versions are available in the downloadable portfolio archive.

## Run locally

```bash
cd projects/corporate-finance-lab
python -m pip install -r requirements.txt
python -m pytest -q
streamlit run app.py
```

## Model setup

Synthetic 2025 revenue = USD 1,000 million; revenue growth 6%; COGS/sales 60%; OPEX/sales 18%; D&A/sales 3%; CAPEX/sales 5%; tax 29.5%; WACC 10.5%; terminal growth 3%; opening cash 160; debt 220; 100 million shares.

Default result (USD millions): **EV 1,655.9607; equity 1,595.9607; value/share 15.9596**. Three-statement balances reconcile without a cash plug. The discount rate must exceed terminal growth.

FCFF = EBIT(1−tax) + D&A − CAPEX − ΔNWC. Net debt in the EV-to-equity bridge is measured in the initial 2025 period. A simplified tax treatment, stable leverage, no loss carryforwards and constant dividend policy are assumed.

## Data lineage / safeguards

No third-party live quotes or issuer financial data were ingested. To adapt to a real issuer, replace simulated inputs with audited financials and cite reporting dates, reporting units, market prices and WACC sources. Portfolio optimization is **in sample** and requires out-of-sample testing before any decision use.

Related original projects remain unchanged in this repository.
