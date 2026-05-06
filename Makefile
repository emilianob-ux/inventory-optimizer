.PHONY: install test lint format clean

install:
	python -m pip install -e ".[dev]"

test:
	pytest tests/ --cov=inventory_optimizer --cov-report=term

lint:
	ruff check src tests
	ruff format --check src tests

format:
	ruff check --fix src tests
	ruff format src tests

clean:
	python -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ['build','dist','htmlcov','.pytest_cache','.ruff_cache']]"
