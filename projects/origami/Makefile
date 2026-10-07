PYTHON ?= python3
VENV := .venv
VENV_PYTHON := $(VENV)/bin/python
HOST ?= 127.0.0.1
PORT ?= 8080
TORCH_HOME := $(CURDIR)/.local/torch

.PHONY: run venv test deploy
.NOTPARALLEL: venv

$(VENV_PYTHON):
	$(PYTHON) -m venv $(VENV)

$(VENV)/.app-deps: pyproject.toml $(VENV_PYTHON)
	$(VENV_PYTHON) -m pip install -e .
	@touch $@

$(VENV)/.test-deps: pyproject.toml $(VENV)/.app-deps
	$(VENV_PYTHON) -m pip install -e '.[test]'
	@touch $@

$(VENV)/.ml-deps: pyproject.toml $(VENV)/.app-deps
	$(VENV_PYTHON) -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
	@touch $@

venv: $(VENV)/.test-deps $(VENV)/.ml-deps
	@echo 'Virtual environment ready. Activate it with: source $(VENV)/bin/activate'

run: $(VENV)/.ml-deps
	@$(VENV_PYTHON) -c 'import uvicorn' || $(VENV_PYTHON) -m pip install -e .
	env TORCH_HOME="$(TORCH_HOME)" PYTHONPATH=. $(VENV_PYTHON) -m uvicorn app.main:create_app --factory --host $(HOST) --port $(PORT)

test: $(VENV)/.test-deps
	@$(VENV_PYTHON) -c 'import pytest' || $(VENV_PYTHON) -m pip install -e '.[test]'
	$(VENV_PYTHON) -m pytest -q
	node --check app/static/app.js
	node --test tests/test_*_frontend.cjs

deploy: test
	bash scripts/deploy.sh
