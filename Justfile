default: test

INVENV := if env_var_or_default('VIRTUAL_ENV', "") == "" { "poetry run" } else { "" }


alias dev := install-dev
# installs the project for development
install-dev:
	poetry install

# installs the project for deployment
install:
	poetry install --only main

# setup CI environment
install-ci: install-dev
	poetry install --only ci


default-cov := "--cov=sblex"
cov-report := "term-missing"
cov := default-cov

# run given test(s)
test *tests="tests":
	{{INVENV}} pytest -vv {{tests}}

# run given test(s) with coverage information
test-w-coverage +tests="tests":
	{{INVENV}} pytest -vv {{cov}} --cov-report={{cov-report}} {{tests}}

# lint all code
lint *flags="":
	{{INVENV}} ruff {{flags}} src test

# type-check the code
type-check:
    {{INVENV}} mypy --config-file mypy.ini -p sblex

# format all python files
fmt:
	{{INVENV}} black src tests

# check formatting for all python files
check-fmt:
	{{INVENV}} black --check src tests

serve-dev:
	{{INVENV}} watchfiles "uvicorn --factory sblex.webapp.main:create_webapp" src

quick-dev:
	{{INVENV}} watchfiles "python examples/quick_dev.py" examples/quick_dev.py templates
