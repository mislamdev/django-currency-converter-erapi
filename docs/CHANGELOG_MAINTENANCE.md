# Changelog Maintenance Guide

This document explains how to maintain the CHANGELOG.md file for the django-currency-converter-erapi project.

## Overview

We follow the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format and [Semantic Versioning](https://semver.org/) for this project.

## Using the Changelog Script

The project includes a Python script (`scripts/changelog.py`) to help maintain the changelog:

### Adding New Entries

```bash
# Add a new feature
python scripts/changelog.py add --type added --message "New currency support for cryptocurrency"

# Record a bug fix
python scripts/changelog.py add --type fixed --message "Fixed rate limiting issue with API calls"

# Document a change
python scripts/changelog.py add --type changed --message "Updated default cache timeout to 1 hour"

# Security updates
python scripts/changelog.py add --type security --message "Fixed potential XSS vulnerability in output"
```

### Creating Releases

```bash
# Create a new release (moves Unreleased items to a versioned release)
python scripts/changelog.py release --version 1.0.2
```

### Validation

```bash
# Validate changelog format
python scripts/changelog.py validate

# Get latest version
python scripts/changelog.py latest
```

## Entry Types

- **Added**: New features
- **Changed**: Changes in existing functionality  
- **Deprecated**: Soon-to-be removed features
- **Removed**: Now removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes

## Workflow Integration

### During Development

1. **For each PR/commit with user-facing changes:**
   ```bash
   python scripts/changelog.py add --type [TYPE] --message "Description of change"
   ```

2. **Before creating a release:**
   ```bash
   # Validate the changelog
   python scripts/changelog.py validate
   
   # Create the release
   python scripts/changelog.py release --version X.Y.Z
   ```

### Automated Checks

The CI pipeline includes changelog validation to ensure:
- Proper format is maintained
- No duplicate versions exist
- Versions are in descending order
- Required sections are present

## Best Practices

### Writing Good Changelog Entries

**Good examples:**
- "Added support for 50+ new currency codes including cryptocurrencies"
- "Fixed memory leak in cache management system"
- "Changed default API timeout from 5s to 10s for better reliability"

**Bad examples:**
- "Bug fix" (too vague)
- "Updated code" (no user impact)
- "Fixed issue #123" (not descriptive enough)

### When to Add Entries

**Always add entries for:**
- New features or functionality
- Bug fixes that affect users
- Breaking changes
- Security fixes
- Performance improvements
- API changes

**Don't add entries for:**
- Internal refactoring (unless it affects performance)
- Documentation updates (unless significant)
- Test additions/changes
- Development tool changes

### Version Numbering

Follow Semantic Versioning (MAJOR.MINOR.PATCH):

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes, incompatible API changes
- **MINOR** (1.0.0 → 1.1.0): New features, backwards-compatible
- **PATCH** (1.0.0 → 1.0.1): Bug fixes, backwards-compatible

## Manual Changelog Maintenance

If you prefer to edit the changelog manually:

1. Add entries to the `## [Unreleased]` section
2. Use the correct entry type headings (`### Added`, `### Fixed`, etc.)
3. Write clear, user-focused descriptions
4. When releasing, move entries from `[Unreleased]` to a new version section

## Example Workflow

```bash
# Start working on a new feature
git checkout -b feature/crypto-support

# Make your changes...
git add .
git commit -m "Add cryptocurrency support"

# Update changelog
python scripts/changelog.py add --type added --message "Added support for Bitcoin, Ethereum, and 20+ other cryptocurrencies"

# Push and create PR
git push origin feature/crypto-support

# After PR is merged and ready to release
git checkout main
git pull origin main

# Validate before release
python scripts/changelog.py validate

# Create release
python scripts/changelog.py release --version 1.1.0

# Update version in setup.py and commit
git add CHANGELOG.md setup.py
git commit -m "Release version 1.1.0"
git tag v1.1.0
git push origin main --tags
```

## Troubleshooting

### Common Issues

1. **"Could not find [Unreleased] section"**
   - Ensure the changelog has the exact heading `## [Unreleased]`

2. **"Version format error"**
   - Use semantic versioning: X.Y.Z (e.g., 1.0.0, not 1.0 or v1.0.0)

3. **"Validation failed"**
   - Run `python scripts/changelog.py validate` to see specific issues
   - Check for proper markdown formatting and section headers

### Getting Help

- Check the [Keep a Changelog](https://keepachangelog.com/) documentation
- Review existing entries in CHANGELOG.md for examples
- Run the validation tool for specific error messages
