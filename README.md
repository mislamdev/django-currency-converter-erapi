# Django Currency Converter

A Django application for converting currencies using real-time exchange rates.

## Installation

1. Install the package:
```bash
pip install django-currency-converter
```

2. Add `currency_converter` to your Django project's `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = [
    # ... other apps
    'currency_converter',
]
```

## Configuration

Add the following settings to your Django `settings.py`:

```python
# Currency Converter Settings
CURRENCY_API_KEY = 'your_api_key_here'  # Optional: for premium API access
CURRENCY_CACHE_TIMEOUT = 3600  # Cache exchange rates for 1 hour
```

## Usage

### Using the Management Command

Convert currency using the management command:

```bash
python manage.py convert_currency 100 USD EUR
```

### Using the Converter Class

```python
from currency_converter.converter import CurrencyConverter

converter = CurrencyConverter()
result = converter.convert(100, 'USD', 'EUR')
print(f"100 USD = {result} EUR")
```

## Features

- Real-time currency conversion
- Caching for performance
- Custom Django management commands
- Error handling for API failures
- Support for multiple currency APIs

## Requirements

- Python 3.8+
- Django 3.2+
- requests 2.25.0+

## License

MIT License
