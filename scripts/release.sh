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

# Analyze changes and suggest version bump
echo -e "${BLUE}🔍 Analyzing changes...${NC}"
python scripts/version_manager.py suggest

# Get suggested version bump
suggested_bump=$(python scripts/version_manager.py suggest 2>/dev/null | grep "Suggested Bump:" | awk '{print tolower($3)}')

if [ "$suggested_bump" = "none" ]; then
    echo -e "${YELLOW}⚠️  No unreleased changes found. Nothing to release.${NC}"
    exit 0
fi

# Get current and new version
current_version=$(python scripts/version_manager.py current)
echo -e "${BLUE}📦 Current version: $current_version${NC}"

# Ask for confirmation or allow override
echo -e "${YELLOW}🤔 Suggested version bump: $suggested_bump${NC}"
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

# Bump version
echo -e "${BLUE}⬆️  Bumping version ($bump_type)...${NC}"
python scripts/version_manager.py bump --type "$bump_type"

# Get new version
new_version=$(python scripts/version_manager.py current)
echo -e "${GREEN}🎯 New version: $new_version${NC}"

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
echo
echo -e "${YELLOW}📤 Next steps:${NC}"
echo "  1. Push to remote: git push origin main --tags"
echo "  2. GitHub Actions will automatically:"
echo "     - Run CI tests"
echo "     - Build and publish to PyPI (if configured)"
echo "     - Create GitHub release"
echo
echo -e "${BLUE}🔗 Commands to push:${NC}"
echo "  git push origin main --tags"
echo
echo -e "${GREEN}🎉 Happy releasing!${NC}"
