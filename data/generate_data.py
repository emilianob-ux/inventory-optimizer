from __future__ import annotations

import numpy as np
import pandas as pd


def main() -> None:
    rng = np.random.default_rng(42)
    dates = pd.date_range("2023-01-01", periods=365 * 3, freq="D")
    t = np.arange(len(dates))
    trend = 0.015 * t
    season = 20 * np.sin(2 * np.pi * t / 365)
    noise = rng.normal(0, 8, size=len(dates))
    promo_flag = rng.choice([0, 1], size=len(dates), p=[0.85, 0.15])
    demand = np.maximum(20, 90 + trend + season + 8 * promo_flag + noise)
    price = np.maximum(1, 18 + 0.02 * trend + rng.normal(0, 0.8, size=len(dates)))
    df = pd.DataFrame({"date": dates, "demand": demand, "price": price, "promo_flag": promo_flag})
    df.to_csv("data/synthetic_demand.csv", index=False)
    print("generated data/synthetic_demand.csv")


if __name__ == "__main__":
    main()
