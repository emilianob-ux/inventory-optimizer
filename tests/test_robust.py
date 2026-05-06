import pytest

from inventory_optimizer import RobustNewsboyOptimizer


def test_robust_order_in_bounds() -> None:
    r = RobustNewsboyOptimizer(1.0, 4.0, a=20, b=200, mu=90)
    q = r.optimal_order_robust()
    assert 20 <= q <= 200


def test_robust_invalid_mu() -> None:
    with pytest.raises(ValueError):
        RobustNewsboyOptimizer(1.0, 4.0, a=20, b=200, mu=250)
