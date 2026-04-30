# TellDNS Makefile

.PHONY: help install install-dev clean test run

help:
	@echo "TellDNS Commands:"
	@echo "  make install     - Install TellDNS"
	@echo "  make install-dev - Install with dev dependencies"
	@echo "  make clean       - Clean cache files"
	@echo "  make test        - Run tests"
	@echo "  make run         - Run TellDNS (example)"
	@echo "  make build       - Build package"

install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements.txt
	pip install -e .
	pip install pytest pytest-asyncio black flake8

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

test:
	pytest tests/ -v

run:
	python -m telldns -d example.com --stealth

build:
	python setup.py sdist bdist_wheel

lint:
	flake8 telldns/ --max-line-length=120
	black telldns/ --check

format:
	black telldns/ --line-length=100
