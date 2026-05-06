from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .newsboy import NewsboyOptimizer


@dataclass
class RobustNewsboyOptimizer:
    holding_cost: float
    shortage_cost: float
    a: float
    b: float
    mu: float

    def __post_init__(self) -> None:
        if not (self.a <= self.mu <= self.b):
            raise ValueError("mu must be inside [a, b].")

    def optimal_order_robust(self) -> float:
        """Simple minimax-regret proxy over support [a,b] and mean mu."""
        alpha = (self.mu - self.a) / (self.b - self.a + 1e-12)
        q = (1 - alpha) * self.a + alpha * self.b
        return float(np.clip(q, self.a, self.b))

    def compare_with_classic(self, sigma: float = 10.0) -> tuple[float, float]:
        classic = NewsboyOptimizer(self.holding_cost, self.shortage_cost)
        classic.fit(("normal", self.mu, sigma))
        return classic.optimal_order(), self.optimal_order_robust()
