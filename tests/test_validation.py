import numpy as np
import pandas as pd

from inventory_optimizer.validation import (
    population_stability_index,
    purged_cv,
    walk_forward_validation,
)


def test_walk_forward() -> None:
    s = pd.Series(np.linspace(80, 120, 120))
    scores = walk_forward_validation(s, n_splits=4)
    assert len(scores) == 4


def test_psi_non_negative() -> None:
    rng = np.random.default_rng(2)
    e = rng.normal(100, 10, 500)
    a = rng.normal(102, 12, 500)
    assert population_stability_index(e, a) >= 0


def test_purged_cv() -> None:
    s = pd.Series(np.linspace(60, 140, 120))
    scores = purged_cv(s, n_splits=4, gap=3)
    assert len(scores) == 4
