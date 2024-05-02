.DEFAULT_GOAL := all

project_dirs = postgresql_geometry
tests_dirs = postgresql_geometry_tests

.PHONY: install
install:
	poetry install \
		--with django \
		--with factoryboy \
		--with faker \
		--with rest_framework \
		--with sqlalchemy \
		--with dev \
		--sync

.PHONY: format
format:
	ruff check --fix-only --exit-zero $(project_dirs) $(tests_dirs)
	ruff format --quiet $(project_dirs) $(tests_dirs)

.PHONY: check
check:
	ruff check $(project_dirs) $(tests_dirs)
	ruff format --check $(project_dirs) $(tests_dirs)

.PHONY: test
test:
	pytest

.PHONY: all
all: check test

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]'`
	rm -f `find . -type f -name '*~'`
	rm -f `find . -type f -name '.*~'`
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -f .coverage
	rm -f .coverage.*
	rm -rf coverage.xml
