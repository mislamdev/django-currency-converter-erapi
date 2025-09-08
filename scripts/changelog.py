#!/usr/bin/env python3
"""
Changelog maintenance script for django-currency-converter-erapi

This script helps maintain the CHANGELOG.md file by:
1. Adding new entries
2. Updating version numbers
3. Setting release dates
4. Validating changelog format

Usage:
    python scripts/changelog.py add --type added --message "New feature description"
    python scripts/changelog.py release --version 1.0.2
    python scripts/changelog.py validate
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path


class ChangelogManager:
    def __init__(self, changelog_path="CHANGELOG.md"):
        self.changelog_path = Path(changelog_path)
        self.changelog_content = ""
        if self.changelog_path.exists():
            self.changelog_content = self.changelog_path.read_text()

    def add_entry(self, entry_type, message):
        """Add a new entry to the Unreleased section"""
        valid_types = ["added", "changed", "deprecated", "removed", "fixed", "security"]
        
        if entry_type.lower() not in valid_types:
            print(f"Error: Invalid entry type '{entry_type}'. Must be one of: {', '.join(valid_types)}")
            return False

        entry_type = entry_type.capitalize()
        
        # Find the Unreleased section
        unreleased_pattern = r"(## \[Unreleased\].*?)(## \[.*?\]|---|\Z)"
        match = re.search(unreleased_pattern, self.changelog_content, re.DOTALL)
        
        if not match:
            print("Error: Could not find [Unreleased] section in changelog")
            return False

        unreleased_section = match.group(1)
        
        # Check if the entry type section exists
        type_pattern = f"### {entry_type}"
        if type_pattern in unreleased_section:
            # Add to existing section
            type_section_pattern = f"(### {entry_type}.*?)(\n### |\n## |\Z)"
            type_match = re.search(type_section_pattern, unreleased_section, re.DOTALL)
            if type_match:
                existing_section = type_match.group(1)
                new_section = existing_section + f"- {message}\n"
                unreleased_section = unreleased_section.replace(existing_section, new_section)
        else:
            # Create new section
            # Find where to insert (after existing sections or at the end)
            insert_position = unreleased_section.find("\n## ")
            if insert_position == -1:
                insert_position = len(unreleased_section)
            
            new_section = f"\n### {entry_type}\n- {message}\n"
            unreleased_section = unreleased_section[:insert_position] + new_section + unreleased_section[insert_position:]

        # Replace the unreleased section in the full content
        self.changelog_content = self.changelog_content.replace(match.group(1), unreleased_section)
        
        # Write back to file
        self.changelog_path.write_text(self.changelog_content)
        print(f"Added {entry_type.lower()} entry: {message}")
        return True

    def create_release(self, version):
        """Create a new release from the Unreleased section"""
        if not re.match(r"^\d+\.\d+\.\d+$", version):
            print(f"Error: Version '{version}' is not in semantic versioning format (x.y.z)")
            return False

        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Find the Unreleased section
        unreleased_pattern = r"(## \[Unreleased\].*?)(## \[.*?\])"
        match = re.search(unreleased_pattern, self.changelog_content, re.DOTALL)
        
        if not match:
            print("Error: Could not find [Unreleased] section or next version section")
            return False

        unreleased_content = match.group(1)
        
        # Check if there are any changes in unreleased
        if not re.search(r"### (Added|Changed|Deprecated|Removed|Fixed|Security)", unreleased_content):
            print("Warning: No changes found in [Unreleased] section")
            return False

        # Create new release section
        release_section = unreleased_content.replace(
            "## [Unreleased]",
            f"## [{version}] - {current_date}"
        )

        # Create new empty unreleased section
        new_unreleased = "## [Unreleased]\n\n"

        # Replace in content
        self.changelog_content = self.changelog_content.replace(
            match.group(1),
            new_unreleased + "\n" + release_section
        )

        # Write back to file
        self.changelog_path.write_text(self.changelog_content)
        print(f"Created release {version} ({current_date})")
        return True

    def validate(self):
        """Validate the changelog format"""
        issues = []
        
        if not self.changelog_path.exists():
            issues.append("CHANGELOG.md file does not exist")
            return issues

        content = self.changelog_content
        
        # Check for required sections
        if "# Changelog" not in content:
            issues.append("Missing main title '# Changelog'")
        
        if "## [Unreleased]" not in content:
            issues.append("Missing [Unreleased] section")
        
        # Check for Keep a Changelog format reference
        if "Keep a Changelog" not in content:
            issues.append("Missing reference to Keep a Changelog format")
        
        # Check for semantic versioning reference
        if "Semantic Versioning" not in content:
            issues.append("Missing reference to Semantic Versioning")
        
        # Validate version format in releases
        version_pattern = r"## \[(\d+\.\d+\.\d+)\] - \d{4}-\d{2}-\d{2}"
        versions = re.findall(version_pattern, content)
        
        # Check for duplicate versions
        if len(versions) != len(set(versions)):
            issues.append("Duplicate version numbers found")
        
        # Check version ordering (should be descending)
        for i in range(len(versions) - 1):
            current = [int(x) for x in versions[i].split('.')]
            next_version = [int(x) for x in versions[i + 1].split('.')]
            if current <= next_version:
                issues.append(f"Version ordering issue: {versions[i]} should come after {versions[i + 1]}")
        
        if issues:
            print("Changelog validation issues found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("Changelog validation passed!")
        
        return issues

    def get_latest_version(self):
        """Get the latest version from the changelog"""
        version_pattern = r"## \[(\d+\.\d+\.\d+)\]"
        versions = re.findall(version_pattern, self.changelog_content)
        return versions[0] if versions else "0.0.0"


def main():
    parser = argparse.ArgumentParser(description="Maintain CHANGELOG.md file")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add entry command
    add_parser = subparsers.add_parser("add", help="Add a new changelog entry")
    add_parser.add_argument("--type", "-t", required=True,
                           choices=["added", "changed", "deprecated", "removed", "fixed", "security"],
                           help="Type of change")
    add_parser.add_argument("--message", "-m", required=True, help="Description of the change")

    # Release command
    release_parser = subparsers.add_parser("release", help="Create a new release")
    release_parser.add_argument("--version", "-v", required=True, help="Version number (e.g., 1.0.2)")

    # Validate command
    subparsers.add_parser("validate", help="Validate changelog format")

    # Latest version command
    subparsers.add_parser("latest", help="Get the latest version")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    changelog = ChangelogManager()

    if args.command == "add":
        changelog.add_entry(args.type, args.message)
    elif args.command == "release":
        changelog.create_release(args.version)
    elif args.command == "validate":
        issues = changelog.validate()
        sys.exit(1 if issues else 0)
    elif args.command == "latest":
        print(changelog.get_latest_version())


if __name__ == "__main__":
    main()
