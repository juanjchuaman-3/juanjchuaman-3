# Fixed Income & Bond Analytics

A practical fixed-income project covering **bond pricing, yield-to-maturity sensitivity, Macaulay duration, modified duration and convexity**.

## Base case

Illustrative bond assumptions:

- Face value: 1,000
- Annual coupon rate: 6.0%
- Yield to maturity: 7.0%
- Maturity: 5 years
- Coupon frequency: semiannual

Base-case outputs:

- Bond price: **958.42**
- Macaulay duration: **4.38 years**
- Modified duration: **4.23 years**
- Convexity: **21.46**

## Methodology

The project discounts each contractual cash flow at the periodic YTM, then measures interest-rate sensitivity using duration and convexity.

```text
Bond Price = Σ CF_t / (1 + y/m)^t
Macaulay Duration = Σ[t × PV(CF_t)] / Price
Modified Duration = Macaulay Duration / (1 + y/m)
```

Convexity is used to improve the linear duration approximation when yield changes are larger.

## Files

- `bond_analytics.py` — pricing, duration, convexity and price-yield curve.
- `outputs/bond_price_yield.svg` — visual price-yield relationship.
- `requirements.txt` — Python dependencies.

## Interpretation

The price-yield curve is downward sloping and convex: when market yields rise, the present value of fixed bond cash flows falls. Duration summarizes first-order sensitivity, while convexity captures the curvature of that relationship.

## Disclaimer

All inputs are illustrative and intended only for educational and portfolio purposes.
