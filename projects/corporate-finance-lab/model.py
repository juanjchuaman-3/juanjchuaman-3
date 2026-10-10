"""Reproducible five-year financial model and unlevered DCF.
All financial inputs are synthetic, in USD millions.
"""
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class Assumptions:
    revenue_base: float = 1000.0
    sales_growth: float = 0.06
    cogs_pct: float = 0.60
    opex_pct: float = 0.18
    da_pct: float = 0.03
    capex_pct: float = 0.05
    ar_pct: float = 0.12
    inventory_pct_cogs: float = 0.15
    ap_pct_cogs: float = 0.125
    tax_rate: float = 0.295
    debt_interest_rate: float = 0.08
    payout_ratio: float = 0.20
    wacc: float = 0.105
    terminal_growth: float = 0.03
    cash_base: float = 160.0
    ppe_base: float = 500.0
    debt_base: float = 220.0
    shares: float = 100.0
    forecast_years: int = 5

def validate(a: Assumptions) -> None:
    if not 1 <= a.forecast_years <= 20:
        raise ValueError("Forecast horizon must be between 1 and 20 years")
    if a.revenue_base <= 0 or a.shares <= 0 or a.cash_base < 0 or a.ppe_base < 0 or a.debt_base < 0:
        raise ValueError("Invalid baseline amounts")
    for key in ("sales_growth", "cogs_pct", "opex_pct", "da_pct", "capex_pct", "ar_pct", "inventory_pct_cogs", "ap_pct_cogs", "tax_rate", "debt_interest_rate", "payout_ratio", "wacc", "terminal_growth"):
        if not -0.99 < getattr(a, key) < 1:
            raise ValueError("Invalid assumption: " + key)
    for key in ("cogs_pct", "opex_pct", "da_pct", "capex_pct", "ar_pct", "inventory_pct_cogs", "ap_pct_cogs", "tax_rate", "debt_interest_rate", "payout_ratio", "wacc"):
        if getattr(a, key) < 0:
            raise ValueError(key + " cannot be negative")
    if a.wacc <= a.terminal_growth:
        raise ValueError("WACC must exceed terminal growth")

def integrated_forecast(a: Assumptions) -> list[dict]:
    validate(a)
    last_sales = a.revenue_base
    last_cogs = last_sales * a.cogs_pct
    last_ar = last_sales * a.ar_pct
    last_inv = last_cogs * a.inventory_pct_cogs
    last_ap = last_cogs * a.ap_pct_cogs
    last_cash, last_ppe, debt = a.cash_base, a.ppe_base, a.debt_base
    equity = last_cash + last_ar + last_inv + last_ppe - last_ap - debt
    result = []
    for year in range(1, a.forecast_years + 1):
        sales = last_sales * (1 + a.sales_growth)
        cogs, opex = sales * a.cogs_pct, sales * a.opex_pct
        da, capex = sales * a.da_pct, sales * a.capex_pct
        ebit = sales - cogs - opex - da
        interest = debt * a.debt_interest_rate
        ebt = ebit - interest
        taxes = max(ebt, 0) * a.tax_rate
        ni = ebt - taxes
        ar = sales * a.ar_pct
        inv = cogs * a.inventory_pct_cogs
        ap = cogs * a.ap_pct_cogs
        d_nwc = (ar-last_ar)+(inv-last_inv)-(ap-last_ap)
        cfo = ni+da-d_nwc
        dividends = max(ni,0)*a.payout_ratio
        end_cash = last_cash+cfo-capex-dividends
        end_ppe = last_ppe+capex-da
        equity += ni-dividends
        assets = end_cash+ar+inv+end_ppe
        liabilities_equity = ap+debt+equity
        fcff = ebit*(1-a.tax_rate)+da-capex-d_nwc
        row = dict(year=2025+year,t=year,revenue=sales,cogs=cogs,opex=opex,
            da=da,ebit=ebit,interest=interest,taxes=taxes,net_income=ni,
            ar=ar,inventory=inv,ap=ap,nwc=ar+inv-ap,d_nwc=d_nwc,capex=capex,
            cfo=cfo,dividends=dividends,cash=end_cash,ppe=end_ppe,
            debt=debt,equity=equity,assets=assets,
            liabilities_equity=liabilities_equity,
            balance_check=assets-liabilities_equity,fcff=fcff)
        if abs(row["balance_check"]) > 1e-7:
            raise ArithmeticError("Financial statements do not balance")
        result.append(row)
        last_sales,last_ar,last_inv,last_ap = sales,ar,inv,ap
        last_cash,last_ppe = end_cash,end_ppe
    return result

def dcf(a: Assumptions) -> dict:
    forecast = integrated_forecast(a)
    pv_flows = [r["fcff"]/(1+a.wacc)**r["t"] for r in forecast]
    terminal_value = forecast[-1]["fcff"]*(1+a.terminal_growth)/(a.wacc-a.terminal_growth)
    pv_terminal = terminal_value/(1+a.wacc)**a.forecast_years
    ev = sum(pv_flows)+pv_terminal
    net_debt = a.debt_base-a.cash_base
    equity = ev-net_debt
    return dict(forecast=forecast,pv_fcff=sum(pv_flows),
        terminal_value=terminal_value,pv_terminal_value=pv_terminal,
        enterprise_value=ev,net_debt=net_debt,equity_value=equity,
        equity_per_share=equity/a.shares,terminal_weight=pv_terminal/ev)

def sensitivity(a: Assumptions, wacc_values: list[float], growth_values: list[float]) -> list[dict]:
    rows=[]
    for wacc in wacc_values:
        for growth in growth_values:
            try:
                val=dcf(replace(a,wacc=wacc,terminal_growth=growth))["equity_value"]
            except ValueError:
                val=None
            rows.append({"wacc":wacc,"g":growth,"equity_value":val})
    return rows

if __name__=="__main__":
    output=dcf(Assumptions())
    for key in ("enterprise_value","equity_value","equity_per_share","terminal_weight"):
        print(f"{key}: {output[key]:.4f}")
