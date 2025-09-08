#!/usr/bin/env python3
"""
Simple version manager for django-currency-converter-erapi
"""

import argparse
import re
import sys
from pathlib import Path


def get_current_version():
    """Get current version from setup.py"""
    try:
        with open('setup.py', 'r') as f:
            content = f.read()

        match = re.search(r"version=['\"]([^'\"]+)['\"]", content)
        if match:
            return match.group(1)
        else:
            print("Could not find version in setup.py", file=sys.stderr)
            return None
    except Exception as e:
        print(f"Error reading setup.py: {e}", file=sys.stderr)
        return None


def suggest_bump():
    """Suggest version bump based on changelog"""
    try:
        with open('CHANGELOG.md', 'r') as f:
            content = f.read()

        # Find unreleased section
        match = re.search(r"## \[Unreleased\](.*?)(?=## \[|\Z)", content, re.DOTALL)
        if not match:
            return "none", "No unreleased section found"

        unreleased = match.group(1)

        # Check for breaking changes
        if "### Removed" in unreleased or any(word in unreleased.lower() for word in ["breaking", "incompatible"]):
            return "major", "Breaking changes detected"

        # Check for new features
        if "### Added" in unreleased:
            return "minor", "New features detected"

        # Check for fixes
        if "### Fixed" in unreleased or "### Security" in unreleased:
            return "patch", "Bug fixes detected"

        # Default
        if "### Changed" in unreleased:
            return "patch", "Changes detected"

        return "none", "No significant changes found"

    except Exception as e:
        print(f"Error analyzing changelog: {e}", file=sys.stderr)
        return "none", "Error analyzing changelog"


def bump_version(current_version, bump_type):
    """Bump version according to type"""
    try:
        parts = current_version.split('.')
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        elif bump_type == "patch":
            patch += 1

        return f"{major}.{minor}.{patch}"
    except Exception as e:
        print(f"Error bumping version: {e}", file=sys.stderr)
        return None


def update_setup_py(new_version):
    """Update version in setup.py"""
    try:
        with open('setup.py', 'r') as f:
            content = f.read()

        new_content = re.sub(
            r"version=['\"]([^'\"]+)['\"]",
            f"version='{new_version}'",
            content
        )
        
        with open('setup.py', 'w') as f:
            f.write(new_content)

        return True
    except Exception as e:
        print(f"Error updating setup.py: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("current")
    subparsers.add_parser("suggest")

    bump_parser = subparsers.add_parser("bump")
    bump_group = bump_parser.add_mutually_exclusive_group(required=True)
    bump_group.add_argument("--type", choices=["major", "minor", "patch"])
    bump_group.add_argument("--auto", action="store_true")

    args = parser.parse_args()
    
    if args.command == "current":
        version = get_current_version()
        if version:
            print(version)
        else:
            sys.exit(1)

    elif args.command == "suggest":
        current = get_current_version()
        if not current:
            sys.exit(1)

        bump_type, reason = suggest_bump()
        if bump_type == "none":
            new_version = current
        else:
            new_version = bump_version(current, bump_type)

        print(f"📦 Current Version: {current}")
        print(f"🔄 Suggested Bump: {bump_type.upper()}")
        print(f"🎯 New Version: {new_version}")
        print(f"💡 Reason: {reason}")

    elif args.command == "bump":
        current = get_current_version()
        if not current:
            sys.exit(1)

        if args.auto:
            bump_type, reason = suggest_bump()
            if bump_type == "none":
                print("No changes to release")
                return
        else:
            bump_type = args.type

        new_version = bump_version(current, bump_type)
        if new_version and update_setup_py(new_version):
            print(f"✅ Version bumped from {current} to {new_version}")
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
