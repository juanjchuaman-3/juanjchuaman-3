from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from var_analysis import historical_var, parametric_var


RETURNS = [
    0.0018, -0.0009, 0.0007, -0.0015, 0.0021,
    -0.0020, 0.0011, -0.0004, -0.0011, 0.0005,
    -0.0028, 0.0016, -0.0019, 0.0008, -0.0032,
    0.0013, -0.0007, 0.0020, -0.0014, -0.0024,
]


def save_outputs(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    portfolio_value = 10_000_000
    confidence = 0.95
    daily_volatility = 0.0012
    holding_days = 10

    p_var = parametric_var(portfolio_value, daily_volatility, confidence, holding_days)
    h_var = historical_var(portfolio_value, RETURNS, confidence)

    pd.DataFrame({"return": RETURNS}).to_csv(output_dir / "returns.csv", index=False)
    pd.DataFrame(
        {
            "metric": ["Portfolio Value", "Confidence", "Holding Days", "Parametric VaR", "Historical 1-day VaR"],
            "value": [portfolio_value, confidence, holding_days, p_var, h_var],
        }
    ).to_csv(output_dir / "var_summary.csv", index=False)

    plt.figure(figsize=(8, 4.5))
    plt.hist(RETURNS, bins=8, edgecolor="black")
    plt.axvline(-h_var / portfolio_value, linestyle="--", label="Historical VaR cutoff")
    plt.title("Illustrative Daily Return Distribution")
    plt.xlabel("Daily return")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "var_distribution.png", dpi=160)
    plt.close()


if __name__ == "__main__":
    save_outputs(Path("outputs"))
