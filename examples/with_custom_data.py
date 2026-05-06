from inventory_optimizer import NewsboyOptimizer

demand = [55, 62, 71, 74, 80, 86, 93, 101, 110]
opt = NewsboyOptimizer(holding_cost=1.5, shortage_cost=5.0)
opt.fit(("empirical", demand))
print(round(opt.optimal_order(), 2))
