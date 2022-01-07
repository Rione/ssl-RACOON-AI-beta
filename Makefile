ROOT      := .

PROJECT   := racoon_ai
PROTO     := $(ROOT)/$(PROJECT)/proto
SRC       := $(ROOT)/$(PROJECT) $(ROOT)/cmd
VENV      := $(ROOT)/.venv

.PHONY: all
all: run

.PHONY: doctor
doctor:
	$(ROOT)/bin/verchew --exit-code


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
run: build install
	poetry run cmd/run.py

.PHONY: install
install: $(VENV) poetry.lock
	poetry install

.PHONY: build
build: build-proto build-src

.PHONY: build-proto
build-proto: $(PROTO) clean-deps
	@protoc \
		--proto_path=$(PROTO)/pb_src \
		--plugin=protoc-gen-mypy=$(VENV)/bin/protoc-gen-mypy \
		--python_out=$(PROTO)/pb_gen \
		--mypy_out=$(PROTO)/pb_gen \
			$(PROTO)/pb_src/*.proto

	@poetry run protol \
		--in-place \
		--python-out $(PROTO)/pb_gen \
		protoc --proto-path=$(PROTO)/pb_src \
			$(PROTO)/pb_src/*.proto

.PHONY: build-src
build-src: $(SRC) clean-deps
	poetry build -vv



# Cleanup #####################################################################

.PHONY: clean
clean: clean-deps clean-pyc

.PHONY: doctor clean-deps
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
lint: flake8 pylint mypy black-check isort-check

.PHONY: flake8
flake8:
	@echo ""
	@echo "Running flake8..."
	@poetry run flake8 --config $(ROOT)/.flake8 --statistics --exit-zero --benchmark $(SRC)

.PHONY: pylint
pylint:
	@echo ""
	@echo "Running pylint..."
	@poetry run pylint --exit-zero --rcfile=$(ROOT)/pyproject.toml --output-format=colorized --reports=y $(SRC)

.PHONY: mypy
mypy:
	@echo ""
	@echo "Running mypy..."
	@poetry run mypy --config-file=$(ROOT)/pyproject.toml --pretty $(SRC) || true

.PHONY: black-check
black-check:
	@echo ""
	@echo "Checking code formatting with black..."
	@poetry run black --verbose --check --color --config $(ROOT)/pyproject.toml $(SRC)

.PHONY: isort-check
isort-check:
	@echo ""
	@echo "Checking code formatting with isort..."
	@poetry run isort --verbose --check-only --settings-file $(ROOT)/pyproject.toml --color $(SRC)


# Format ######################################################################

.PHONY: format
format: black isort

.PHONY: black
black:
	poetry run black --config $(ROOT)/pyproject.toml $(SRC)

.PHONY: isort
isort:
	poetry run isort --verbose --setting-file $(ROOT)/pyproject.toml --color $(SRC)
