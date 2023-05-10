

.default: help

ifeq (${VIRTUAL_ENV},)
  INVENV = poetry run
else
  INVENV =
endif

.PHONY: help
help:
	@echo "usage:"
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

dev: install-dev
install-dev:
	poetry install

install:
	poetry install --only main

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
	${INVENV} mypy --config-file mypy.ini -p sblex

# build the project
build:
	poetry build

part := "patch"
# bump given part of version
bumpversion:
	${INVENV} bump2version ${part}
