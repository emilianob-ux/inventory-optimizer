# Contributing

Gracias por contribuir.

## Flujo sugerido

1. Fork + branch (`feat/...` o `fix/...`).
2. Instalar dependencias: `pip install -e ".[dev]"`.
3. Ejecutar validaciones:
   - `ruff check src tests`
   - `ruff format --check src tests`
   - `pytest tests`
4. Abrir PR con contexto y evidencia.

## Estilo

- Type hints en API publica.
- Docstrings consistentes.
- Tests para cambios de comportamiento.
