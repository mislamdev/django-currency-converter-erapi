# Running CI Locally

This guide explains how to run the same tests and checks locally that run in the GitHub Actions CI workflow.

## Prerequisites

1. Python 3.8+ installed
2. Virtual environment activated
3. Git repository cloned

## Setup

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt
pip install -e .
```

## Running Tests

### Basic Test Run
```bash
# Set environment variables
export DJANGO_SETTINGS_MODULE=tests.settings
export PYTHONPATH="${PYTHONPATH}:$(pwd):$(pwd)/tests"

# Run tests with coverage
pytest --cov=currency_converter_erapi --cov-report=xml --cov-report=term-missing --maxfail=1
```

### Test with API Key (Optional)
```bash
# Set your API key for testing premium features
export CURRENCY_API_KEY="your-api-key-here"

# Run tests
pytest --cov=currency_converter_erapi --cov-report=xml --cov-report=term-missing --maxfail=1
```

### Test Multiple Django Versions

```bash
# Test with Django 5.2
pip install "Django>=5.2,<5.3"
pytest --cov=currency_converter_erapi --maxfail=1

# Test with Django 4.2
pip install "Django>=4.2,<4.3"
pytest --cov=currency_converter_erapi --maxfail=1

# Test with Django 3.2
pip install "Django>=3.2,<3.3"
pytest --cov=currency_converter_erapi --maxfail=1
```

## Code Quality Checks

### Linting with flake8
```bash
flake8 currency_converter_erapi tests
```

### Code formatting with black
```bash
# Check formatting
black --check currency_converter_erapi tests

# Auto-format
black currency_converter_erapi tests
```

### Import sorting with isort
```bash
# Check imports
isort --check-only currency_converter_erapi tests

# Fix imports
isort currency_converter_erapi tests
```

### Type checking with mypy
```bash
mypy currency_converter_erapi
```

## Changelog Validation

```bash
# Validate changelog format
python scripts/changelog.py validate

# Add changelog entry
python scripts/changelog.py add --type added --message "Your change description"

# Create release
python scripts/changelog.py release --version 1.0.1
```

## Complete CI Simulation

Run this script to simulate the full CI pipeline:

```bash
#!/bin/bash
set -e

echo "🔧 Installing dependencies..."
pip install -r requirements-dev.txt
pip install -e .

echo "🧪 Running tests..."
export DJANGO_SETTINGS_MODULE=tests.settings
export PYTHONPATH="${PYTHONPATH}:$(pwd):$(pwd)/tests"
pytest --cov=currency_converter_erapi --cov-report=xml --cov-report=term-missing --maxfail=1

echo "📝 Validating changelog..."
python scripts/changelog.py validate

echo "🎨 Checking code formatting..."
black --check currency_converter_erapi tests

echo "📦 Checking imports..."
isort --check-only currency_converter_erapi tests

echo "🔍 Linting code..."
flake8 currency_converter_erapi tests

echo "✅ All checks passed!"
```

## Environment Variables

The following environment variables are used in CI and can be set locally:

- `DJANGO_SETTINGS_MODULE`: Set to `tests.settings`
- `CURRENCY_API_KEY`: Your ExchangeRate-API key (optional)
- `PYTHONPATH`: Include current directory and tests directory

## Troubleshooting

### ImportError: No module named 'tests'
Make sure `PYTHONPATH` includes both the current directory and tests directory:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd):$(pwd)/tests"
```

### Django Configuration Issues
Ensure Django settings module is properly set:
```bash
export DJANGO_SETTINGS_MODULE=tests.settings
```

### Test Database Issues
The tests use an in-memory SQLite database, so no setup is required. If you encounter issues, try:
```bash
python -c "import django; django.setup()"
```

## Docker Alternative

You can also run tests in a Docker container to match the CI environment exactly:

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements-dev.txt
RUN pip install -e .

ENV DJANGO_SETTINGS_MODULE=tests.settings
ENV PYTHONPATH="${PYTHONPATH}:/app:/app/tests"

CMD ["pytest", "--cov=currency_converter_erapi", "--cov-report=xml", "--cov-report=term-missing", "--maxfail=1"]
```

```bash
# Build and run
docker build -t currency-converter-test .
docker run --rm currency-converter-test
```
