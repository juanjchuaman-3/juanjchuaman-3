from dataclasses import dataclass


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


def build_forecast(a: Assumptions):
    rows = []
    revenue_prev = a.revenue_0
    nwc_prev = revenue_prev * a.nwc_pct_sales

    for year in range(1, a.forecast_years + 1):
        revenue = revenue_prev * (1 + a.revenue_growth)
        ebit = revenue * a.ebit_margin
        nopat = ebit * (1 - a.tax_rate)
        da = revenue * a.da_pct_sales
        capex = revenue * a.capex_pct_sales
        nwc = revenue * a.nwc_pct_sales
        delta_nwc = nwc - nwc_prev
        fcff = nopat + da - capex - delta_nwc

        rows.append({
            "year": year,
            "revenue": revenue,
            "ebit": ebit,
            "nopat": nopat,
            "da": da,
            "capex": capex,
            "delta_nwc": delta_nwc,
            "fcff": fcff,
        })

        revenue_prev = revenue
        nwc_prev = nwc

    return rows


def value_dcf(a: Assumptions):
    forecast = build_forecast(a)

    pv_fcff = 0.0
    for row in forecast:
        row["discount_factor"] = 1 / ((1 + a.wacc) ** row["year"])
        row["pv_fcff"] = row["fcff"] * row["discount_factor"]
        pv_fcff += row["pv_fcff"]

    fcff_n = forecast[-1]["fcff"]
    fcff_next = fcff_n * (1 + a.terminal_growth)
    terminal_value = fcff_next / (a.wacc - a.terminal_growth)
    pv_terminal = terminal_value / ((1 + a.wacc) ** a.forecast_years)

    enterprise_value = pv_fcff + pv_terminal
    equity_value = enterprise_value - a.net_debt

    return {
        "forecast": forecast,
        "pv_explicit_fcff": pv_fcff,
        "terminal_value": terminal_value,
        "pv_terminal_value": pv_terminal,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
    }


def sensitivity(a: Assumptions, wacc_values, g_values):
    table = {}
    for wacc in wacc_values:
        row = {}
        for g in g_values:
            if wacc <= g:
                row[g] = None
                continue
            local = Assumptions(**{**a.__dict__, "wacc": wacc, "terminal_growth": g})
            row[g] = value_dcf(local)["equity_value"]
        table[wacc] = row
    return table


if __name__ == "__main__":
    assumptions = Assumptions()
    result = value_dcf(assumptions)

    print("DCF Valuation")
    print("-------------")
    for row in result["forecast"]:
        print(
            f"Year {row['year']}: Revenue={row['revenue']:.2f} | "
            f"FCFF={row['fcff']:.2f} | PV FCFF={row['pv_fcff']:.2f}"
        )

    print(f"\nEnterprise Value: {result['enterprise_value']:.2f}")
    print(f"Equity Value: {result['equity_value']:.2f}")

    sens = sensitivity(
        assumptions,
        wacc_values=[0.095, 0.105, 0.115],
        g_values=[0.02, 0.03, 0.04],
    )

    print("\nSensitivity: Equity Value")
    for wacc, values in sens.items():
        print(f"WACC {wacc:.1%}: {values}")
