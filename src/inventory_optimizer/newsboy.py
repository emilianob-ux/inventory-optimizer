from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from scipy.stats import lognorm, norm, uniform


class NewsboyValidationError(ValueError):
    """Invalid optimizer configuration or input data."""


DistributionSpec = tuple[str, float, float] | tuple[str, Iterable[float]]


@dataclass
class NewsboyOptimizer:
    holding_cost: float
    shortage_cost: float

    def __post_init__(self) -> None:
        if self.holding_cost <= 0 or self.shortage_cost <= 0:
            raise NewsboyValidationError("Costs must be positive.")
        self._samples: np.ndarray | None = None

    def fit(self, distribution: DistributionSpec, n_samples: int = 100_000) -> "NewsboyOptimizer":
        """Fit demand distribution from parametric or empirical definition."""
        kind = distribution[0].lower()
        rng = np.random.default_rng(42)
        if kind == "normal":
            _, mu, sigma = distribution  # type: ignore[misc]
            self._samples = norm(loc=mu, scale=sigma).rvs(size=n_samples, random_state=rng)
        elif kind == "lognormal":
            _, mean, sigma = distribution  # type: ignore[misc]
            self._samples = lognorm(s=sigma, scale=np.exp(mean)).rvs(
                size=n_samples, random_state=rng
            )
        elif kind == "uniform":
            _, low, high = distribution  # type: ignore[misc]
            self._samples = uniform(loc=low, scale=high - low).rvs(size=n_samples, random_state=rng)
        elif kind == "empirical":
            _, values = distribution  # type: ignore[misc]
            arr = np.asarray(list(values), dtype=float)
            if arr.size == 0:
                raise NewsboyValidationError("Empirical distribution cannot be empty.")
            self._samples = rng.choice(arr, size=n_samples, replace=True)
        else:
            raise NewsboyValidationError(f"Unsupported distribution: {kind}")
        self._samples = np.clip(self._samples, 0, None)
        return self

    def optimal_order(self) -> float:
        if self._samples is None:
            raise NewsboyValidationError("Call fit() before optimal_order().")
        critical_ratio = self.shortage_cost / (self.shortage_cost + self.holding_cost)
        return float(np.quantile(self._samples, critical_ratio))

    def expected_cost(self, q: float) -> float:
        if self._samples is None:
            raise NewsboyValidationError("Call fit() before expected_cost().")
        over = np.maximum(q - self._samples, 0.0)
        under = np.maximum(self._samples - q, 0.0)
        return float(np.mean(self.holding_cost * over + self.shortage_cost * under))

    def predictive_distribution(self, q: float, n_scenarios: int = 1000) -> np.ndarray:
        if self._samples is None:
            raise NewsboyValidationError("Call fit() before predictive_distribution().")
        rng = np.random.default_rng(7)
        d = rng.choice(self._samples, size=n_scenarios, replace=True)
        return self.holding_cost * np.maximum(q - d, 0.0) + self.shortage_cost * np.maximum(
            d - q, 0.0
        )
