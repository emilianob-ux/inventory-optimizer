from inventory_optimizer import NewsboyOptimizer

opt = NewsboyOptimizer(holding_cost=1.0, shortage_cost=4.0)
opt.fit(("normal", 100.0, 20.0))
q = opt.optimal_order()
print({"optimal_q": round(q, 2), "expected_cost": round(opt.expected_cost(q), 2)})
