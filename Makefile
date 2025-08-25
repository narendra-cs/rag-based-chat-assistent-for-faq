# Makefile for RAG-based Chat Assistant

# Python/Backend variables
PYTHON_SRC=src/
PYTHON_VENV=venv
PYTHON_BIN=$(PYTHON_VENV)/bin
PYTHON=$(PYTHON_BIN)/python
PIP=$(PYTHON_BIN)/pip
BLACK=$(PYTHON_BIN)/black
FLAKE8=$(PYTHON_BIN)/flake8
ISORT=$(PYTHON_BIN)/isort
MYPY=$(PYTHON_BIN)/mypy

# Frontend variables
UI_SRC=src/ui_source
NPM=npm

# Default target
all: lint

# Setup development environment
.PHONY: setup-dev
setup-dev: venv install-dev-deps

# Python environment setup
.PHONY: venv
venv: $(PYTHON_VENV)/bin/activate

$(PYTHON_VENV)/bin/activate: requirements.txt
	python3 -m venv $(PYTHON_VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	touch $(PYTHON_VENV)/bin/activate

# Install development dependencies
.PHONY: install-dev-deps
install-dev-deps: venv requirements_dev.txt
	$(PIP) install -r requirements_dev.txt

# Python linting
.PHONY: lint-python
lint-python: venv install-dev-deps
	@echo "Running Black..."
	@$(BLACK) --check --diff $(PYTHON_SRC) || (echo "Black check failed. Run 'make format' to fix formatting." && exit 1)
	@echo "Running isort..."
	@$(ISORT) --check-only --diff --profile=black $(PYTHON_SRC) || (echo "isort check failed. Run 'make format' to fix imports." && exit 1)


# Python formatting
.PHONY: format-python
format-python: venv install-dev-deps
	$(BLACK) $(PYTHON_SRC)
	$(ISORT) --profile=black $(PYTHON_SRC)

# Frontend linting
.PHONY: lint-ui
lint-ui:
	@echo "Running ESLint..."
	@cd $(UI_SRC) && $(NPM) run lint:fix

# Frontend formatting
.PHONY: format-ui
format-ui:
	@echo "Formatting frontend code..."
	@cd $(UI_SRC) && $(NPM) run format

# Combined linting
.PHONY: lint
lint: lint-python lint-ui

# Combined formatting
.PHONY: format
format: format-python format-ui

# Clean up
.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  setup-dev      - Set up development environment (venv + dev deps)"
	@echo "  venv           - Create Python virtual environment"
	@echo "  install-dev-deps - Install development dependencies"
	@echo "  lint           - Run all linters (Python and UI)"
	@echo "  lint-python    - Run Python linters"
	@echo "  lint-ui        - Run frontend linters"
	@echo "  format         - Format all code (Python and UI)"
	@echo "  format-python  - Format Python code"
	@echo "  format-ui      - Format frontend code"
	@echo "  clean          - Remove Python virtual environment and cache files"
	@echo "  help           - Show this help message"