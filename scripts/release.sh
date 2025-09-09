#!/bin/bash
set -e

# Automated Release Script for django-currency-converter-erapi
# This script automates the entire release process with version management

echo "🚀 Starting automated release process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're on main branch
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ] && [ "$current_branch" != "master" ]; then
    echo -e "${RED}❌ Error: Must be on main/master branch for release${NC}"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${RED}❌ Error: Uncommitted changes found. Please commit or stash changes first.${NC}"
    exit 1
fi

# Validate changelog
echo -e "${BLUE}📝 Validating changelog...${NC}"
if ! python scripts/changelog.py validate; then
    echo -e "${RED}❌ Changelog validation failed${NC}"
    exit 1
fi

# Get current version directly from setup.py
current_version=$(python -c "
import re
with open('setup.py', 'r') as f:
    content = f.read()
match = re.search(r\"version=['\\\"']([^'\\\"]+)['\\\"']\", content)
print(match.group(1) if match else 'unknown')
")

echo -e "${BLUE}📦 Current version: $current_version${NC}"

# Analyze changelog to suggest version bump
suggested_bump=$(python -c "
import re
try:
    with open('CHANGELOG.md', 'r') as f:
        content = f.read()

    # Find unreleased section
    match = re.search(r'## \[Unreleased\](.*?)(?=## \[|\Z)', content, re.DOTALL)
    if not match:
        print('none')
        exit()

    unreleased = match.group(1)

    # Check for breaking changes
    if '### Removed' in unreleased or any(word in unreleased.lower() for word in ['breaking', 'incompatible']):
        print('major')
    # Check for new features
    elif '### Added' in unreleased:
        print('minor')
    # Check for fixes or changes
    elif '### Fixed' in unreleased or '### Security' in unreleased or '### Changed' in unreleased:
        print('patch')
    else:
        print('none')
except:
    print('none')
")

if [ "$suggested_bump" = "none" ]; then
    echo -e "${YELLOW}⚠️  No unreleased changes found. Nothing to release.${NC}"
    exit 0
fi

# Show analysis
echo -e "${BLUE}🔍 Analysis complete!${NC}"
echo -e "${YELLOW}🤔 Suggested version bump: $suggested_bump${NC}"

# Ask for confirmation or allow override
read -p "Press Enter to proceed with suggested bump, or type 'major', 'minor', or 'patch' to override: " user_input

if [ ! -z "$user_input" ]; then
    if [[ "$user_input" =~ ^(major|minor|patch)$ ]]; then
        bump_type="$user_input"
        echo -e "${BLUE}✏️  Using override: $bump_type${NC}"
    else
        echo -e "${RED}❌ Invalid bump type. Must be major, minor, or patch.${NC}"
        exit 1
    fi
else
    bump_type="$suggested_bump"
fi

# Calculate new version
new_version=$(python -c "
import sys
current = '$current_version'
bump_type = '$bump_type'

try:
    parts = current.split('.')
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'patch':
        patch += 1

    print(f'{major}.{minor}.{patch}')
except Exception as e:
    print('error', file=sys.stderr)
    sys.exit(1)
")

if [ "$new_version" = "error" ]; then
    echo -e "${RED}❌ Error calculating new version${NC}"
    exit 1
fi

echo -e "${GREEN}🎯 New version will be: $new_version${NC}"

# Update version in setup.py
echo -e "${BLUE}⬆️  Updating version in setup.py...${NC}"
python -c "
import re
import sys
new_version = '$new_version'
with open('setup.py', 'r') as f:
    content = f.read()

new_content = re.sub(
    r\"version=['\\\"']([^'\\\"]+)['\\\"']\",
    f\"version='{new_version}'\",
    content
)

with open('setup.py', 'w') as f:
    f.write(new_content)

print('✅ Version updated successfully')
"

# Create changelog release
echo -e "${BLUE}📋 Creating changelog release...${NC}"
python scripts/changelog.py release --version "$new_version"

# Run tests to make sure everything works
echo -e "${BLUE}🧪 Running tests...${NC}"
export DJANGO_SETTINGS_MODULE=tests.settings
export PYTHONPATH="${PYTHONPATH}:$(pwd):$(pwd)/tests"

if ! pytest --cov=currency_converter_erapi --maxfail=1 -q; then
    echo -e "${RED}❌ Tests failed. Aborting release.${NC}"
    # Restore files
    git checkout setup.py CHANGELOG.md
    echo -e "${YELLOW}🔄 Restored files to previous state${NC}"
    exit 1
fi

# Commit changes
echo -e "${BLUE}💾 Committing release...${NC}"
git add setup.py CHANGELOG.md
git commit -m "Release version $new_version

- Updated version to $new_version
- Moved unreleased changes to changelog
- Automated release via release script"

# Create tag
echo -e "${BLUE}🏷️  Creating git tag...${NC}"
git tag "v$new_version" -m "Release version $new_version"

# Show summary
echo -e "${GREEN}✅ Release $new_version completed successfully!${NC}"
echo
echo -e "${BLUE}📋 Summary:${NC}"
echo "  - Version bumped from $current_version to $new_version ($bump_type)"
echo "  - Changelog updated"
echo "  - Tests passed"
echo "  - Git commit and tag created"
git add setup.py CHANGELOG.md currency_converter_erapi/__init__.py
echo -e "${YELLOW}📤 Next steps:${NC}"
echo "  1. Push to remote: git push origin main --tags"
- Updated version to $new_version in setup.py and __init__.py
echo "     - Run CI tests"
echo "     - Build and publish to PyPI (if configured)"
echo "     - Create GitHub release"
echo
echo -e "${BLUE}🔗 Commands to push:${NC}"
echo "  git push origin main --tags"
echo
echo -e "${GREEN}🎉 Happy releasing!${NC}"
