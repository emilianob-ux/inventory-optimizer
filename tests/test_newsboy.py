import numpy as np

from inventory_optimizer import NewsboyOptimizer


def test_newsboy_optimal_order_positive() -> None:
    opt = NewsboyOptimizer(1.0, 4.0).fit(("normal", 100.0, 20.0))
    assert opt.optimal_order() > 0


def test_newsboy_expected_cost_changes_with_q() -> None:
    opt = NewsboyOptimizer(1.0, 4.0).fit(("normal", 100.0, 15.0))
    q1, q2 = 80.0, 120.0
    c1 = opt.expected_cost(q1)
    c2 = opt.expected_cost(q2)
    assert np.isfinite(c1)
    assert np.isfinite(c2)
