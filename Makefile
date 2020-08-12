.PHONY: docs

install:
	pip install --upgrade pip
	pip install -e .

develop: install
	pip install -e ".[dev]"
	python setup.py develop
	pre-commit install

lint:
	flake8 setup.py onefootball_network tests --count --statistics

test:
	pytest tests

docs:
	python -m pip install -e ".[docs]"
	mkdir -p theme
	mkdocs build --clean --site-dir public

serve-docs:
	mkdocs serve

clean:
	rm -rf .pytest_cache
	rm -rf build
	rm -rf dist
	rm -rf onefootball_network.egg-info
	rm -rf .ipynb_checkpoints
	rm -rf notebooks/.ipynb_checkpoints
	rm -rf .mypy_cache

build:
	docker build -t onefootball_network .
