from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from inventory_optimizer import NewsboyOptimizer, RobustNewsboyOptimizer
from inventory_optimizer.simulation import simulate_inventory
from inventory_optimizer.validation import walk_forward_validation


def main() -> None:
    out = Path("docs/images")
    out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv("data/synthetic_demand.csv")
    demand = df["demand"].to_numpy(dtype=float)

    classic = NewsboyOptimizer(holding_cost=1.0, shortage_cost=4.0).fit(("empirical", demand))
    robust = RobustNewsboyOptimizer(
        1.0, 4.0, float(demand.min()), float(demand.max()), float(demand.mean())
    )
    q_classic = classic.optimal_order()
    q_robust = robust.optimal_order_robust()

    qs = np.linspace(np.quantile(demand, 0.1), np.quantile(demand, 0.95), 50)
    costs = []
    fills = []
    for q in qs:
        m = simulate_inventory(q, demand, 1.0, 4.0)
        costs.append(m["expected_cost"])
        fills.append(m["fill_rate"])
    plt.figure(figsize=(7, 4))
    plt.plot(costs, fills, label="Pareto frontier")
    plt.scatter(
        [classic.expected_cost(q_classic), classic.expected_cost(q_robust)],
        [
            simulate_inventory(q_classic, demand, 1.0, 4.0)["fill_rate"],
            simulate_inventory(q_robust, demand, 1.0, 4.0)["fill_rate"],
        ],
        c=["tab:blue", "tab:orange"],
        label="Classic vs Robust",
    )
    plt.xlabel("Expected cost")
    plt.ylabel("Fill rate")
    plt.title("Pareto: cost vs fill rate")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "pareto.png", dpi=140)
    plt.close()

    base = classic.expected_cost(q_classic)
    params = {"holding_cost": 1.2, "shortage_cost": 3.4, "demand_mean": demand.mean() * 1.06}
    impacts = {k: abs(v - base) for k, v in params.items()}
    plt.figure(figsize=(7, 4))
    names = list(impacts.keys())
    vals = list(impacts.values())
    plt.barh(names, vals)
    plt.title("Sensitivity tornado (proxy)")
    plt.xlabel("Absolute impact vs baseline cost")
    plt.tight_layout()
    plt.savefig(out / "sensitivity.png", dpi=140)
    plt.close()

    s = pd.Series(demand)
    wf = walk_forward_validation(s, n_splits=6)
    plt.figure(figsize=(7, 4))
    plt.plot(range(1, len(wf) + 1), wf, marker="o")
    plt.title("Walk-forward validation (MAE by fold)")
    plt.xlabel("Fold")
    plt.ylabel("MAE")
    plt.tight_layout()
    plt.savefig(out / "walk_forward.png", dpi=140)
    plt.close()

    n_steps = np.arange(100, 5100, 100)
    converg = []
    rng = np.random.default_rng(13)
    for n in n_steps:
        sample = rng.choice(demand, size=n, replace=True)
        converg.append(float(np.mean(sample)))
    plt.figure(figsize=(7, 4))
    plt.plot(n_steps, converg)
    plt.axhline(demand.mean(), color="red", linestyle="--", label="Full-sample mean")
    plt.title("Monte Carlo convergence")
    plt.xlabel("Simulation draws")
    plt.ylabel("Estimated demand mean")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "convergence.png", dpi=140)
    plt.close()

    print("Generated docs/images/*.png")


if __name__ == "__main__":
    main()
