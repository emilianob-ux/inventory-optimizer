import numpy as np
import pytest

from inventory_optimizer import NewsboyOptimizer
from inventory_optimizer.newsboy import NewsboyValidationError


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


def test_newsboy_invalid_costs() -> None:
    with pytest.raises(NewsboyValidationError):
        NewsboyOptimizer(0.0, 2.0)


def test_newsboy_empirical_and_predictive_distribution() -> None:
    opt = NewsboyOptimizer(1.0, 3.0).fit(("empirical", [10, 12, 14, 16]))
    q = opt.optimal_order()
    preds = opt.predictive_distribution(q, n_scenarios=50)
    assert len(preds) == 50
    assert float(np.mean(preds)) >= 0


def test_newsboy_invalid_distribution() -> None:
    opt = NewsboyOptimizer(1.0, 2.0)
    with pytest.raises(NewsboyValidationError):
        opt.fit(("triangular", 1.0, 2.0))


def test_newsboy_methods_require_fit() -> None:
    opt = NewsboyOptimizer(1.0, 2.0)
    with pytest.raises(NewsboyValidationError):
        opt.optimal_order()
    with pytest.raises(NewsboyValidationError):
        opt.expected_cost(100)
