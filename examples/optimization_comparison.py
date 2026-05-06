from inventory_optimizer import NewsboyOptimizer, RobustNewsboyOptimizer

classic = NewsboyOptimizer(1.0, 4.0).fit(("normal", 100.0, 18.0))
robust = RobustNewsboyOptimizer(1.0, 4.0, a=40.0, b=180.0, mu=100.0)
print(
    {
        "classic_q": round(classic.optimal_order(), 2),
        "robust_q": round(robust.optimal_order_robust(), 2),
    }
)
