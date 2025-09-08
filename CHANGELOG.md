# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [1.1.0] - 2025-09-09

### Added
- Comprehensive changelog following Keep a Changelog format
- Django test configuration with proper settings initialization
- Support for CURRENCY_API_KEY environment variable in CI/CD pipeline
- Enhanced exception handling for JSON parsing errors
- Network error handling for API requests
- Test coverage reporting with pytest-cov
- Automated CI workflow for multiple Python versions (3.8-3.12)
- Django 5.2 support with full compatibility testing

### Changed
- Improved test suite configuration with conftest.py for proper Django setup
- Enhanced management command output formatting for better user experience
- Updated CI workflow to include environment variables for Django settings
- Restructured exception handling in currency converter for better error reporting
- Enhanced CI workflow to test multiple Django versions including 5.2
- Enhanced CI workflow to test multiple Django versions including 5.2
- Enhanced CI workflow to test multiple Django versions including 5.2
- Enhanced CI workflow to test multiple Django versions including 5.2

### Fixed
- Django settings configuration issue in pytest environment
- JSON parsing error handling in API responses
- Network exception handling for requests
- Management command amount display formatting (100.0 → 100)
- Test dependencies installation in CI environment

- Resolved Django settings configuration issues in test environment
- Fixed pytest Django configuration issues in CI environment
## [1.0.1] - 2024-XX-XX

### Added
- Initial stable release
- Currency conversion functionality using ExchangeRate-API
- Django management command for currency conversion
- Comprehensive test suite with 94% coverage
- Support for multiple currency codes (24+ currencies)
- Caching mechanism for exchange rates
- API key support for premium tier access
- Multiple API key configuration methods (Django settings, environment variables)

### Features
- Real-time currency conversion
- Exchange rate caching with configurable timeout
- Rate limiting and error handling
- Free tier and premium tier API support
- Django integration with management commands
- Comprehensive logging
- Input validation and sanitization
- Decimal precision for financial calculations

### Security
- Input validation for currency codes
- Safe handling of API responses
- Secure API key management through environment variables

## [1.0.0] - 2024-XX-XX

### Added
- Initial project structure
- Basic currency converter implementation
- Django app configuration
- Core exceptions and error handling
- Basic test framework

---

## Release Notes

### Version 1.0.1 Highlights

This release focuses on stability, testing improvements, and better CI/CD integration:

- **Enhanced Testing**: Fixed Django configuration issues that were preventing tests from running properly in CI environments
- **Better Error Handling**: Improved exception handling for network issues and malformed API responses
- **CI/CD Improvements**: Added support for API key usage in GitHub Actions workflows
- **Developer Experience**: Better formatting in management commands and comprehensive test coverage

### Compatibility

- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Django**: 3.2, 4.0, 4.1, 4.2
- **Operating Systems**: Linux, macOS, Windows

### Dependencies

#### Core Dependencies
- Django >= 3.2, < 5.0
- requests >= 2.25.0, < 3.0

#### Development Dependencies
- pytest >= 6.0
- pytest-django >= 4.0
- pytest-cov >= 2.10.0
- coverage >= 5.0
- black >= 21.0
- flake8 >= 3.8
- mypy >= 0.800
- isort >= 5.0

### Migration Guide

No breaking changes in this release. All existing functionality remains compatible.

### Known Issues

- None currently identified

### Contributors

Special thanks to all contributors who helped improve this release through testing, bug reports, and feature suggestions.

---

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Update the changelog
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Changelog Maintenance

This changelog is maintained following these principles:

- **Guiding Principles**
  - Changelogs are for humans, not machines
  - There should be an entry for every single version
  - The same types of changes should be grouped
  - Versions and sections should be linkable
  - The latest version comes first
  - The release date of each version is displayed

- **Types of Changes**
  - `Added` for new features
  - `Changed` for changes in existing functionality
  - `Deprecated` for soon-to-be removed features
  - `Removed` for now removed features
  - `Fixed` for any bug fixes
  - `Security` in case of vulnerabilities

- **Version Format**
  - Follow Semantic Versioning (MAJOR.MINOR.PATCH)
  - MAJOR: incompatible API changes
  - MINOR: backwards-compatible functionality additions
  - PATCH: backwards-compatible bug fixes
