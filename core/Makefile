#!make

default: isort flake8 test mypy clean

isort:
	isort .

flake8:
	flake8 .

mypy:
	mypy .

test:
	pytest

clean:
	@rm -rf .mypy_cache
	@rm -rf .pytest_cache
