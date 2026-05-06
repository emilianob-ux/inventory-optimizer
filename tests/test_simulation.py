import numpy as np

from inventory_optimizer.simulation import bootstrap_ci, simulate_inventory


def test_simulation_metrics() -> None:
    d = np.array([80, 100, 120, 90, 110], dtype=float)
    m = simulate_inventory(100, d, 1.0, 4.0)
    assert "expected_cost" in m
    assert 0 <= m["fill_rate"] <= 1


def test_bootstrap_ci_order() -> None:
    d = np.random.default_rng(1).normal(100, 20, 300)

    def f(x: np.ndarray) -> np.ndarray:
        return np.abs(x - 100)

    lo, hi = bootstrap_ci(f, d, n_bootstrap=200)
    assert lo <= hi
