GIT_ROOT  := $(shell git rev-parse --show-toplevel)

PRJ_NAME  := racoon_ai
PROJECT   := $(GIT_ROOT)/$(PRJ_NAME)
SRC       := $(PROJECT) $(GIT_ROOT)/cmd
VENV      := $(GIT_ROOT)/.venv

.PHONY: all
all: run


# help ########################################################################

.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "  run:        run the runner script"
	@echo "  install:    install dependencies"
	@echo "  build:      build this project"
	@echo "  clean:      clean this project"
	@echo "  lint:       run the all linters"
	@echo "  format:     run the all formatters"
	@echo "  help:       show more verbose help"

.PHONY: help-long
help-long:
	@echo "Usage: make <target>"
	@echo ""
	@echo "[help]"
	@echo "  help:       show help"
	@echo "  help-long:  show more verbose help"
	@echo ""
	@echo "[main]"
	@echo "  run:        run the runner script"
	@echo "  install:    install dependencies"
	@echo "  build:      build this project"
	@echo ""
	@echo "[cleanup]"
	@echo "  clean:      clean this project"
	@echo "  clean-deps: auto-remove unlisted packages"
	@echo "  clean-pyc:  remove python chache files"
	@echo ""
	@echo "[lint]"
	@echo "  lint:       run the all linters"
	@echo "  pylint:     lint code with pylint"
	@echo "  flake8:     lint code with flake8"
	@echo ""
	@echo "[format]"
	@echo "  format:     run the all formatters"
	@echo "  black:      format code with black"
	@echo "  isort:      format code with isort"


# Main ########################################################################

.PHONY: run
run: build
	poetry run cmd/run.py

.PHONY: install
install: $(VENV)
	poetry install

.PHONY: build
build: clean-deps $(SRC)
	protoc --proto_path=$(GIT_ROOT)/proto/ --plugin=protoc-gen-mypy=$(VENV)/bin/protoc-gen-mypy --python_out=$(PROJECT)/proto_py --mypy_out=$(PROJECT)/proto_py $(GIT_ROOT)/proto/*.proto
	poetry build -vv



# Cleanup #####################################################################

.PHONY: clean
clean: clean-deps clean-pyc

.PHONY: clean-deps
clean-deps:
	poetry install --remove-untracked --no-root

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


# Lint ########################################################################

.PHONY: lint
lint: flake8 pylint black-check isort-check

.PHONY: flake8
flake8:
	@echo ""
	@echo "Running flake8..."
	@poetry run flake8 --config ./.flake8 --statistics --exit-zero --benchmark $(SRC)

.PHONY: pylint
pylint:
	@echo ""
	@echo "Running pylint..."
	@poetry run pylint --exit-zero --rcfile=$(GIT_ROOT)/pyproject.toml --output-format=colorized --reports=y $(SRC)

.PHONY: black-check
black-check:
	@echo ""
	@echo "Checking code formatting with black..."
	@poetry run black --verbose --check --color --config $(GIT_ROOT)/pyproject.toml $(SRC)

.PHONY: isort-check
isort-check:
	@echo ""
	@echo "Checking code formatting with isort..."
	@poetry run isort --verbose --check-only --settings-file $(GIT_ROOT)/pyproject.toml --color $(SRC)


# Format ######################################################################

.PHONY: format
format: black isort

.PHONY: black
black:
	poetry run black --config $(GIT_ROOT)/pyproject.toml $(SRC)

.PHONY: isort
isort:
	poetry run isort --verbose --setting-file $(GIT_ROOT)/pyproject.toml --color $(SRC)
