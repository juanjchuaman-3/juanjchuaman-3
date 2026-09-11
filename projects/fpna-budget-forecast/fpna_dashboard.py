from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from fpna_analysis import analyze, build_dataset


def save_outputs(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    result = analyze(build_dataset())
    result.to_csv(output_dir / "fpna_output.csv", index=False)

    plt.figure(figsize=(8, 4.5))
    for column in ["budget", "forecast", "actual"]:
        plt.plot(result["month"], result[column], marker="o", label=column.title())
    plt.title("FP&A: Budget vs Forecast vs Actual")
    plt.xlabel("Month")
    plt.ylabel("Illustrative OPEX")
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(output_dir / "fpna_trend.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 4.5))
    plt.bar(result["month"], result["variance_vs_budget"])
    plt.axhline(0, linewidth=1)
    plt.title("Monthly Variance vs Budget")
    plt.xlabel("Month")
    plt.ylabel("Actual - Budget")
    plt.tight_layout()
    plt.savefig(output_dir / "fpna_variance.png", dpi=160)
    plt.close()


if __name__ == "__main__":
    save_outputs(Path("outputs"))
