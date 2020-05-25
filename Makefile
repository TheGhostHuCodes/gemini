.PHONY: black-check, install, isort-check, lint-check, pytest, type-check

PY_TEST_FILES = $(shell find tests -name '*.py')
PY_FILES = $(shell find gemini -name '*.py')

check: isort-check black-check lint-check type-check pytest

lint-check:
	poetry run pylint --rcfile=.pylintrc $(PY_FILES)
	poetry run pylint --rcfile=tests.pylintrc $(PY_TEST_FILES)

black-check:
	poetry run black --check .

pytest:
	poetry run pytest

isort-check:
	poetry run isort --recursive --settings-path=isort.cfg --check-only

type-check:
	poetry run mypy -p gemini

install:
	poetry install
