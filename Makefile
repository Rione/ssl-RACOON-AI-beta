ROOT     = $(shell git rev-parse --show-toplevel)
OS       = $(shell uname -s)
ARCH     = $(shell uname -m | sed -e 's/i.86/i386/' -e 's/aarch64/arm64/' -e 's/amd64/x86_64/')
PKG      = $(shell sed -n 's/^ *name.*=.*"\([^"]*\)".*/\1/p' pyproject.toml)
VERSION  = $(shell sed -n 's/^ *version.*=.*"\([^"]*\)".*/\1/p' pyproject.toml)

DIST_DIR		    = $(ROOT)/dist
CACHE_DIR		    = $(ROOT)/.cache
VENV_DIR        = $(ROOT)/.venv
BIN_DIR         = $(ROOT)/bin
PROJECT_DIR     = $(ROOT)/$(PKG)

MW_TMP_DIR      = $(CACHE_DIR)/racoon-mw
MW_OUT_DIR      = $(MW_TMP_DIR)/out
MW_FILENAME     = ssl-RACOON-MW_*_$(OS)_$(ARCH).tar.gz
MW_DOWNLOADED   = $(wildcard $(MW_TMP_DIR)/$(MW_FILENAME))

PROTO_SRCDIR    = $(PROJECT_DIR)/proto/pb_src
PROTO_GENDIR    = $(PROJECT_DIR)/proto/pb_gen

PKG_FILENAME    = $(PKG)-$(VERSION)
WHEEL           = $(DIST_DIR)/$(PKG_FILENAME)-py3-none-any.whl
TGZ             = $(DIST_DIR)/$(PKG_FILENAME).tar.gz
TARGETS         = $(WHEEL) $(TGZ)
PROTO_SRCS      = $(wildcard $(PROTO_SRCDIR)/*.proto)

PROTO_PYS       = $(PROTO_SRCS:$(PROTO_SRCDIR)/%.proto=$(PROTO_GENDIR)/%_pb2.py)
PROTO_STUBS     = $(PROTO_SRCS:$(PROTO_SRCDIR)/%.proto=$(PROTO_GENDIR)/%_pb2.pyi)

PY_SRCS         = $(ROOT)/$(PKG) $(ROOT)/cmd
PY_LOCKFILE     = $(ROOT)/$(PKG)/poetry.lock

PROTOC          = protoc
RACOON_MW       = $(BIN_DIR)/RACOON-MW.exe
VERCHEW         = $(BIN_DIR)/verchew

PROTOC_GEN_MYPY = $(VENV_DIR)/bin/protoc-gen-mypy
PROTOL          = $(VENV_DIR)/bin/protol
BLACK           = $(VENV_DIR)/bin/black
ISORT           = $(VENV_DIR)/bin/isort

# *************************************************************************** #

.PHONY: all
all: clean build

.PHONY: build
build: doctor $(WHEEL)

$(TGZ):
	@echo ""
	$(error [ERROR] Please compile with `make` to cleanup and build, or use just `make build`)

$(WHEEL): $(PROJECT_DIR) $(PROTO_GENDIR)/%.pyi
	@echo ""
	$(info ----------------------------------------------)
	@echo "Creating $(PKG)@$(VERSION) distribution..."
	@poetry build -vv

$(PROTO_GENDIR)/%.pyi: $(PROTO_GENDIR)/%.py $(PROTOL)
	@echo ""
	$(info ----------------------------------------------)
	$(info Editing stub files...)
	@poetry run protol \
		--in-place \
		--python-out $(@D) \
		$(PROTOC) --proto-path=$(PROTO_SRCDIR) $(PROTO_SRCS)

$(PROTO_GENDIR)/%.py: $(PROTO_SRCS) $(PROTOC_GEN_MYPY)
	@echo ""
	$(info ----------------------------------------------)
	$(info Compiling protobuf files...)
	@$(PROTOC) \
		--proto_path=$(<D) \
		--plugin=protoc-gen-mypy=$(PROTOC_GEN_MYPY) \
		--python_out=$(@D) \
	  --mypy_out=$(@D) \
		$(PROTO_SRCS)

$(PROTOL):
$(PROTOC_GEN_MYPY): $(VENV_DIR)
$(VENV_DIR): poetry.lock clean-deps $(BIN_DIR)/%

$(BIN_DIR)/%: $(MW_OUT_DIR)/%
	@echo ""
	$(info ----------------------------------------------)
	$(info Linking RACOON-MW...)
	@ln -sf $(<D)/ssl-RACOON-MW $(RACOON_MW)

$(MW_OUT_DIR)/%:
	@echo ""
	$(info ----------------------------------------------)
	$(info Downloading RACOON-MW...)
	@gh release download \
		--repo Rione/ssl-RACOON-MW \
		--dir $(MW_TMP_DIR) \
		--pattern $(MW_FILENAME)
	$(info ----------------------------------------------)
	$(info Extracting RACOON-MW...)
	@mkdir -p $(@D)
	@tar xzvf $(wildcard $(MW_TMP_DIR)/$(MW_FILENAME)) -C $(@D)

# *************************************************************************** #

.PHONY: doctor
doctor:
	@echo ""
	$(info ----------------------------------------------)
	$(info Checking dependencies versions for $(PKG)@$(VERSION) ...)
	@$(VERCHEW) --exit-code

.PHONY: install
install:
	@echo ""
	$(info ----------------------------------------------)
	$(info Installing ...)
	@poetry install
	@poetry run pre-commit install

.PHONY: run
run: doctor $(TGZ) install
	@echo ""
	$(info ----------------------------------------------)
	@poetry run python -m $(PKG)

.PHONY: clean
clean: clean-dirs clean-deps

clean-dirs:
	@echo ""
	$(info ----------------------------------------------)
	$(info Cleaning up...)
	@rm -f $(TARGETS) $(PROTO_PYS) $(PROTO_STUBS) $(RACOON_MW) $(MW_OUT_DIR)/* $(wildcard $(MW_TMP_DIR)/$(MW_FILENAME))
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-deps
clean-deps:
	@echo ""
	$(info ----------------------------------------------)
	@poetry install --remove-untracked --no-root

# *************************************************************************** #

.PHONY: lint
lint: flake8 pylint mypy black-check isort-check

.PHONY: flake8
flake8:
	@echo ""
	$(info ----------------------------------------------)
	@echo "Running flake8..."
	@poetry run flake8 --config $(ROOT)/.flake8 --statistics --exit-zero --benchmark $(ROOT)

.PHONY: pylint
pylint:
	@echo ""
	$(info ----------------------------------------------)
	$(info "Running pylint...")
	@poetry run pylint --exit-zero --rcfile=$(ROOT)/pyproject.toml --output-format=colorized --reports=y $(PKG)

.PHONY: mypy
mypy:
	@echo ""
	$(info ----------------------------------------------)
	$(info "Running mypy...")
	@poetry run mypy --config-file=$(ROOT)/pyproject.toml --pretty $(ROOT) || true

.PHONY: black-check
black-check:
	@echo ""
	$(info ----------------------------------------------)
	$(info "Checking code formatting with black...")
	@poetry run black --verbose --check --color --config $(ROOT)/pyproject.toml $(ROOT)

.PHONY: isort-check
isort-check:
	@echo ""
	$(info ----------------------------------------------)
	$(info "Checking code formatting with isort...")
	@poetry run isort --verbose --check-only --settings-file $(ROOT)/pyproject.toml --color $(ROOT)

# *************************************************************************** #

.PHONY: format
format: black isort

.PHONY: black
black:
	@echo ""
	$(info ----------------------------------------------)
	$(info "Formatting code with black...")
	poetry run black --config $(ROOT)/pyproject.toml $(ROOT)

.PHONY: isort
isort:
	@echo ""
	$(info ----------------------------------------------)
	$(info "Formatting code with isort...")
	poetry run isort --verbose --settings-file $(ROOT)/pyproject.toml --color $(ROOT)

# *************************************************************************** #

.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "  run:        just run the runner script (withoud building)"
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
	@echo "  help-long:  show more verbose help (this one)"
	@echo ""
	@echo "[main]"
	@echo "  run:        run the runner script (withoud building)"
	@echo "  install:    install dependencies"
	@echo "  build:      build this project"
	@echo ""
	@echo "[cleanup]"
	@echo "  clean:      clean this project"
	@echo "  clean-deps: auto-remove unlisted packages"
	@echo "  clean-dirs: remove chaches and compiled files"
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
