from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


@dataclass
class Assumptions:
    revenue_0: float = 1000.0
    revenue_growth: float = 0.06
    ebit_margin: float = 0.15
    tax_rate: float = 0.295
    da_pct_sales: float = 0.03
    capex_pct_sales: float = 0.04
    nwc_pct_sales: float = 0.10
    wacc: float = 0.105
    terminal_growth: float = 0.03
    net_debt: float = 220.0
    forecast_years: int = 5


def build_forecast(a: Assumptions) -> pd.DataFrame:
    rows = []
    revenue_prev = a.revenue_0
    nwc_prev = revenue_prev * a.nwc_pct_sales

    for year in range(1, a.forecast_years + 1):
        revenue = revenue_prev * (1 + a.revenue_growth)
        ebit = revenue * a.ebit_margin
        taxes = ebit * a.tax_rate
        nopat = ebit - taxes
        da = revenue * a.da_pct_sales
        ebitda = ebit + da
        capex = revenue * a.capex_pct_sales
        nwc = revenue * a.nwc_pct_sales
        delta_nwc = nwc - nwc_prev
        fcff = nopat + da - capex - delta_nwc
        discount_factor = 1 / ((1 + a.wacc) ** year)
        pv_fcff = fcff * discount_factor

        rows.append({
            "Year": year,
            "Revenue": revenue,
            "EBITDA": ebitda,
            "EBIT": ebit,
            "Taxes": taxes,
            "NOPAT": nopat,
            "D&A": da,
            "CAPEX": capex,
            "NWC": nwc,
            "Delta NWC": delta_nwc,
            "FCFF": fcff,
            "Discount Factor": discount_factor,
            "PV FCFF": pv_fcff,
        })
        revenue_prev = revenue
        nwc_prev = nwc

    return pd.DataFrame(rows)


def valuation(a: Assumptions, forecast: pd.DataFrame) -> dict:
    fcff_n = forecast["FCFF"].iloc[-1]
    terminal_value = fcff_n * (1 + a.terminal_growth) / (a.wacc - a.terminal_growth)
    pv_terminal = terminal_value / ((1 + a.wacc) ** a.forecast_years)
    pv_explicit = forecast["PV FCFF"].sum()
    enterprise_value = pv_explicit + pv_terminal
    equity_value = enterprise_value - a.net_debt
    return {
        "PV Explicit FCFF": pv_explicit,
        "Terminal Value": terminal_value,
        "PV Terminal Value": pv_terminal,
        "Enterprise Value": enterprise_value,
        "Net Debt": a.net_debt,
        "Equity Value": equity_value,
    }


def sensitivity_matrix(a: Assumptions, forecast: pd.DataFrame) -> pd.DataFrame:
    wacc_values = [0.090, 0.095, 0.100, 0.105, 0.110, 0.115, 0.120]
    growth_values = [0.020, 0.025, 0.030, 0.035, 0.040]
    matrix = pd.DataFrame(
        index=[f"{w:.1%}" for w in wacc_values],
        columns=[f"{g:.1%}" for g in growth_values],
        dtype=float,
    )

    for wacc in wacc_values:
        for growth in growth_values:
            pv_explicit = sum(
                row["FCFF"] / ((1 + wacc) ** int(row["Year"]))
                for _, row in forecast.iterrows()
            )
            terminal_value = forecast["FCFF"].iloc[-1] * (1 + growth) / (wacc - growth)
            pv_terminal = terminal_value / ((1 + wacc) ** a.forecast_years)
            matrix.loc[f"{wacc:.1%}", f"{growth:.1%}"] = pv_explicit + pv_terminal - a.net_debt
    return matrix


def save_outputs(forecast: pd.DataFrame, sensitivity: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    forecast.to_csv(output_dir / "dcf_forecast.csv", index=False)
    sensitivity.to_csv(output_dir / "dcf_sensitivity.csv")

    plt.figure(figsize=(8, 4.5))
    plt.plot(forecast["Year"], forecast["Revenue"], marker="o", label="Revenue")
    plt.plot(forecast["Year"], forecast["FCFF"], marker="o", label="FCFF")
    plt.title("DCF Forecast: Revenue and FCFF")
    plt.xlabel("Forecast Year")
    plt.ylabel("Illustrative monetary units")
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(output_dir / "dcf_forecast.png", dpi=160)
    plt.close()

    plt.figure(figsize=(7, 4.5))
    image = plt.imshow(sensitivity.values.astype(float), aspect="auto")
    plt.xticks(range(len(sensitivity.columns)), sensitivity.columns)
    plt.yticks(range(len(sensitivity.index)), sensitivity.index)
    plt.xlabel("Terminal growth")
    plt.ylabel("WACC")
    plt.title("Equity Value Sensitivity")
    for i in range(sensitivity.shape[0]):
        for j in range(sensitivity.shape[1]):
            plt.text(j, i, f"{sensitivity.iloc[i, j]:.0f}", ha="center", va="center", fontsize=8)
    plt.colorbar(image, label="Equity value")
    plt.tight_layout()
    plt.savefig(output_dir / "dcf_sensitivity.png", dpi=160)
    plt.close()


if __name__ == "__main__":
    assumptions = Assumptions()
    forecast = build_forecast(assumptions)
    values = valuation(assumptions, forecast)
    sensitivity = sensitivity_matrix(assumptions, forecast)

    print("\nProjected financial model")
    print(forecast.round(2).to_string(index=False))

    print("\nValuation summary")
    for key, value in values.items():
        print(f"{key}: {value:,.2f}")

    print("\nEquity value sensitivity")
    print(sensitivity.round(2))

    save_outputs(forecast, sensitivity, Path("outputs"))
