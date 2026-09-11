import pandas as pd


def build_dataset():
    return pd.DataFrame(
        {
            "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "budget": [200, 205, 210, 215, 220, 225],
            "forecast": [198, 208, 212, 218, 224, 228],
            "actual": [202, 211, 207, 221, 229, 231],
        }
    )


def analyze(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["variance_vs_budget"] = out["actual"] - out["budget"]
    out["variance_vs_budget_pct"] = out["variance_vs_budget"] / out["budget"]
    out["forecast_error"] = out["actual"] - out["forecast"]
    out["forecast_error_pct"] = out["forecast_error"] / out["forecast"]
    return out


if __name__ == "__main__":
    data = build_dataset()
    result = analyze(data)

    pd.set_option("display.float_format", lambda x: f"{x:,.2f}")
    print(result)

    total_budget = result["budget"].sum()
    total_actual = result["actual"].sum()
    total_variance = total_actual - total_budget

    print("\nManagement summary")
    print("------------------")
    print(f"Total Budget: {total_budget:,.2f}")
    print(f"Total Actual: {total_actual:,.2f}")
    print(f"Absolute Variance: {total_variance:,.2f}")
    print(f"Variance %: {total_variance / total_budget:.2%}")
