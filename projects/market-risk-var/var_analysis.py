from statistics import NormalDist
import math


def parametric_var(portfolio_value, daily_volatility, confidence=0.95, holding_days=10):
    z = NormalDist().inv_cdf(confidence)
    return portfolio_value * z * daily_volatility * math.sqrt(holding_days)


def historical_var(portfolio_value, returns, confidence=0.95):
    if not returns:
        raise ValueError("returns must contain at least one observation")

    losses = sorted([-r * portfolio_value for r in returns])
    index = min(len(losses) - 1, math.ceil(confidence * len(losses)) - 1)
    return losses[index]


if __name__ == "__main__":
    portfolio_value = 10_000_000
    daily_volatility = 0.0012
    confidence = 0.95
    holding_days = 10

    illustrative_returns = [
        0.0018, -0.0009, 0.0007, -0.0015, 0.0021,
        -0.0020, 0.0011, -0.0004, -0.0011, 0.0005,
        -0.0028, 0.0016, -0.0019, 0.0008, -0.0032,
        0.0013, -0.0007, 0.0020, -0.0014, -0.0024,
    ]

    p_var = parametric_var(
        portfolio_value,
        daily_volatility,
        confidence,
        holding_days,
    )

    h_var = historical_var(
        portfolio_value,
        illustrative_returns,
        confidence,
    )

    print("Market Risk Summary")
    print("-------------------")
    print(f"Portfolio Value: {portfolio_value:,.2f}")
    print(f"Confidence Level: {confidence:.0%}")
    print(f"Holding Period: {holding_days} days")
    print(f"Parametric VaR: {p_var:,.2f}")
    print(f"Historical 1-day VaR: {h_var:,.2f}")
