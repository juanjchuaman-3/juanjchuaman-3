import numpy as np
import pandas as pd


TRADING_DAYS = 252
RISK_FREE_RATE = 0.04
N_PORTFOLIOS = 10_000
SEED = 42


def illustrative_returns() -> pd.DataFrame:
    """Small reproducible daily-return sample for four illustrative assets."""
    rng = np.random.default_rng(SEED)
    means = np.array([0.00045, 0.00035, 0.00030, 0.00025])
    vols = np.array([0.012, 0.010, 0.009, 0.007])
    corr = np.array(
        [
            [1.00, 0.55, 0.35, 0.20],
            [0.55, 1.00, 0.40, 0.25],
            [0.35, 0.40, 1.00, 0.30],
            [0.20, 0.25, 0.30, 1.00],
        ]
    )
    cov = np.outer(vols, vols) * corr
    data = rng.multivariate_normal(means, cov, size=500)
    return pd.DataFrame(data, columns=["Asset_A", "Asset_B", "Asset_C", "Asset_D"])


def annualized_inputs(returns: pd.DataFrame):
    mean_returns = returns.mean() * TRADING_DAYS
    cov_matrix = returns.cov() * TRADING_DAYS
    return mean_returns, cov_matrix


def portfolio_stats(weights, mean_returns, cov_matrix, risk_free_rate=RISK_FREE_RATE):
    expected_return = float(np.dot(weights, mean_returns))
    volatility = float(np.sqrt(weights @ cov_matrix.values @ weights))
    sharpe = (expected_return - risk_free_rate) / volatility
    return expected_return, volatility, sharpe


def simulate_portfolios(returns: pd.DataFrame, n_portfolios=N_PORTFOLIOS) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    mean_returns, cov_matrix = annualized_inputs(returns)
    rows = []

    for _ in range(n_portfolios):
        weights = rng.random(len(mean_returns))
        weights /= weights.sum()
        exp_return, vol, sharpe = portfolio_stats(weights, mean_returns, cov_matrix)
        rows.append(
            {
                "return": exp_return,
                "volatility": vol,
                "sharpe": sharpe,
                **{f"w_{asset}": weight for asset, weight in zip(mean_returns.index, weights)},
            }
        )

    return pd.DataFrame(rows)


def equal_weight_portfolio(returns: pd.DataFrame) -> dict:
    mean_returns, cov_matrix = annualized_inputs(returns)
    weights = np.repeat(1 / len(mean_returns), len(mean_returns))
    exp_return, vol, sharpe = portfolio_stats(weights, mean_returns, cov_matrix)
    return {
        "return": exp_return,
        "volatility": vol,
        "sharpe": sharpe,
        **{f"w_{asset}": weight for asset, weight in zip(mean_returns.index, weights)},
    }


def main():
    returns = illustrative_returns()
    simulated = simulate_portfolios(returns)

    min_vol = simulated.loc[simulated["volatility"].idxmin()]
    max_sharpe = simulated.loc[simulated["sharpe"].idxmax()]
    equal_weight = pd.Series(equal_weight_portfolio(returns), name="Equal Weight")

    summary = pd.DataFrame(
        [min_vol, max_sharpe, equal_weight],
        index=["Minimum Volatility", "Maximum Sharpe", "Equal Weight"],
    )

    cols = ["return", "volatility", "sharpe"] + [c for c in summary.columns if c.startswith("w_")]
    print("Portfolio comparison\n")
    print(summary[cols].round(4).to_string())


if __name__ == "__main__":
    main()
