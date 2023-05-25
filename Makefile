

.default: help

ifeq (${VIRTUAL_ENV},)
  INVENV = poetry run
else
  INVENV =
endif

.PHONY: help
help:
	@echo "USAGE"
	@echo "====="
	@echo ""
	@echo "install-dev (alias: dev)"
	@echo "		installs the project for development"

	@echo "install"
	@echo "		installs the project for deployment"

	@echo "install-ci"
	@echo "		installs the project for CI"

	@echo "test"
	@echo "		run given test(s) (default: tests='tests')"

	@echo "test-w-coverage"
	@echo "		run given test(s) with coverage information (default: all_tests='tests')"

	@echo "lint"
	@echo "		lint all code"

	@echo "fmt"
	@echo "		format all python files"

	@echo "check-fmt"
	@echo "		check formatting for all python files"

	@echo "serve-dev"
	@echo "		serve sblex-server with reloading"

	@echo "quick-dev"
	@echo "		run examples against sblex-server with reloading"
	@echo "		'REPL-driven development'"

	@echo "serve-fm-server"
	@echo "		serve fm-server with reloading"

dev: install-dev
install-dev:
	poetry install

install:
	poetry install --only main --sync

# setup CI environment
install-ci: install-dev
	poetry install --only ci

default_cov := "--cov=src/sblex"
cov_report := "term-missing"
cov := ${default_cov}

all_tests := tests
tests := tests

.PHONY: test
test:
	${INVENV} pytest -vv ${tests}

.PHONY: test-w-coverage
test-w-coverage:
	${INVENV} pytest -vv ${cov} --cov-report=${cov_report} ${all_tests}

.PHONY: lint
lint:
	${INVENV} ruff src tests

fmt:
	${INVENV} black src tests

.PHONY: check-fmt
check-fmt:
	${INVENV} black --check src tests

# type-check the code
.PHONY: type-check
type-check:
	${INVENV} mypy --config-file mypy.ini src tests

# build the project
build:
	poetry build

part := "patch"
# bump given part of version
bumpversion:
	${INVENV} bump2version ${part}

serve-dev:
	${INVENV} watchfiles "uvicorn --port 8000 --factory sblex.webapp.main:create_webapp" src

quick-dev:
	${INVENV} watchfiles "python examples/quick_dev.py" examples/quick_dev.py templates

serve-fm-server:
	${INVENV} watchfiles "uvicorn --port 8765 --factory sblex.fm_server.main:create_fm_server" src/sblex/fm_server
