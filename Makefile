default: build

build: format check

format:
	black --line-length 79 .
	isort --multi-line 3 --profile black .

check:
	flake8 --max-doc-length=72 .
