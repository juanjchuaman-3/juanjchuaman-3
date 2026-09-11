from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def bond_metrics(face=1000.0, coupon_rate=0.06, ytm=0.07, maturity=5, frequency=2):
    periods = maturity * frequency
    coupon = face * coupon_rate / frequency
    period_yield = ytm / frequency
    cash_flows = np.array([coupon] * (periods - 1) + [coupon + face], dtype=float)
    times = np.arange(1, periods + 1)
    present_values = cash_flows / ((1 + period_yield) ** times)

    price = present_values.sum()
    macaulay_periods = (times * present_values).sum() / price
    macaulay_years = macaulay_periods / frequency
    modified_duration = macaulay_years / (1 + period_yield)

    convexity_periods = sum(
        cf * t * (t + 1) / ((1 + period_yield) ** (t + 2))
        for cf, t in zip(cash_flows, times)
    ) / price
    convexity_years = convexity_periods / (frequency ** 2)

    return {
        "price": price,
        "macaulay_duration": macaulay_years,
        "modified_duration": modified_duration,
        "convexity": convexity_years,
    }


def price_yield_curve(face=1000.0, coupon_rate=0.06, maturity=5, frequency=2):
    yields = np.arange(0.03, 0.111, 0.005)
    prices = []
    periods = maturity * frequency
    coupon = face * coupon_rate / frequency
    cash_flows = [coupon] * (periods - 1) + [coupon + face]

    for ytm in yields:
        period_yield = ytm / frequency
        price = sum(cf / ((1 + period_yield) ** t) for t, cf in enumerate(cash_flows, start=1))
        prices.append(price)

    return pd.DataFrame({"yield": yields, "price": prices})


def save_outputs(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics = bond_metrics()
    curve = price_yield_curve()

    pd.DataFrame(
        {
            "metric": ["Price", "Macaulay Duration", "Modified Duration", "Convexity"],
            "value": [metrics["price"], metrics["macaulay_duration"], metrics["modified_duration"], metrics["convexity"]],
        }
    ).to_csv(output_dir / "bond_summary.csv", index=False)
    curve.to_csv(output_dir / "bond_price_yield.csv", index=False)

    plt.figure(figsize=(8, 4.5))
    plt.plot(curve["yield"], curve["price"], marker="o")
    plt.axvline(0.07, linestyle="--", label="Base YTM: 7.0%")
    plt.axhline(metrics["price"], linestyle=":", label=f"Base price: {metrics['price']:.2f}")
    plt.title("Bond Price-Yield Relationship")
    plt.xlabel("Yield to Maturity")
    plt.ylabel("Bond Price")
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(output_dir / "bond_price_yield.png", dpi=160)
    plt.close()

    return metrics


if __name__ == "__main__":
    result = save_outputs(Path("outputs"))
    print("Bond Analytics")
    print("--------------")
    for key, value in result.items():
        print(f"{key}: {value:,.4f}")
