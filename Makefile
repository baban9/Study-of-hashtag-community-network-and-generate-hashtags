.PHONY: setup analyze whitepaper run test clean

PYTHON := .venv/bin/python
PIP := .venv/bin/pip
PYTEST := .venv/bin/pytest
MPLCONFIGDIR := $(CURDIR)/.matplotlib
export MPLCONFIGDIR

setup:
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

analyze:
	$(PYTHON) -m research.run_analysis

whitepaper: analyze
	$(PYTHON) -m research.generate_whitepaper

run:
	cd hashtagApp && ../$(PYTHON) app.py

test:
	$(PYTEST) tests/ -q

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
