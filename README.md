# aloof-union

Transmute service desk workflows between formats. Turn FreshService and JSM configurations into clear, visual representations.

## Requirements

* Python 3.9 over

## Setup

`python -m venv /path/to/venv`

`/path/to/venv/bin/python -m pip install aloof-union`

## Test Coverage

View the latest test coverage report [here](https://ocasazza.github.io/aloof-union/coverage/).

Quick coverage summary:
- Module coverage
- Line coverage
- Branch coverage

[Detailed Coverage Report](https://ocasazza.github.io/aloof-union/coverage/index.html)

## Local Development

To generate and view coverage reports locally:

```bash
# Run tests with coverage
tox -e py39

# View the report
open htmlcov/index.html
```