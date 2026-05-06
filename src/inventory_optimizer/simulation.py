from __future__ import annotations

from collections.abc import Callable

import numpy as np


def simulate_inventory(
    q: float, demand_samples: np.ndarray, holding_cost: float, shortage_cost: float
) -> dict[str, float]:
    over = np.maximum(q - demand_samples, 0.0)
    under = np.maximum(demand_samples - q, 0.0)
    costs = holding_cost * over + shortage_cost * under
    fill_rate = 1.0 - float(np.mean(under > 0))
    return {
        "expected_cost": float(np.mean(costs)),
        "p95_cost": float(np.quantile(costs, 0.95)),
        "fill_rate": fill_rate,
    }


def bootstrap_ci(
    cost_function: Callable[[np.ndarray], np.ndarray],
    base_samples: np.ndarray,
    n_bootstrap: int = 1000,
) -> tuple[float, float]:
    rng = np.random.default_rng(123)
    stats = []
    n = base_samples.size
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, size=n)
        stats.append(float(np.mean(cost_function(base_samples[idx]))))
    return float(np.quantile(stats, 0.025)), float(np.quantile(stats, 0.975))


def sensitivity_analysis(base_value: float, params: dict[str, float]) -> list[tuple[str, float]]:
    impacts = []
    for k, v in params.items():
        impacts.append((k, abs(v - base_value)))
    return sorted(impacts, key=lambda x: x[1], reverse=True)
