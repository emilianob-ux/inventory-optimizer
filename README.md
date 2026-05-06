# inventory-optimizer

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/OWNER/inventory-optimizer/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/inventory-optimizer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Optimizacion de inventario bajo demanda incierta con enfoque clasico Newsboy y variante robusta.

## Ecuacion central

\[
Q^* = F_D^{-1}\left(\frac{p}{p+h}\right)
\]

## Demo rapida

```python
from inventory_optimizer import NewsboyOptimizer

opt = NewsboyOptimizer(holding_cost=1.0, shortage_cost=4.0)
opt.fit(("normal", 100.0, 20.0))
print(round(opt.optimal_order(), 2))
```

## Instalacion

```bash
pip install -e ".[dev]"
```

## Estructura

- `src/inventory_optimizer`: libreria principal
- `tests`: pruebas unitarias
- `examples`: ejemplos ejecutables
- `notebooks`: tutoriales interactivos
- `docs`: documentacion MkDocs

## Estado

- v0.1.0: implementacion base clasica, robusta simplificada, simulacion, validacion temporal y CI.

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md).
