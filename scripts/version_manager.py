#!/usr/bin/env python3
"""
Automated version management for django-currency-converter-erapi

This script automatically determines version bumps based on changelog entries
and follows semantic versioning (MAJOR.MINOR.PATCH).

Usage:
    python scripts/version_manager.py suggest
    python scripts/version_manager.py bump --type [major|minor|patch]
    python scripts/version_manager.py bump --auto
    python scripts/version_manager.py current
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class VersionManager:
    def __init__(self, setup_py_path="setup.py", changelog_path="CHANGELOG.md"):
        self.setup_py_path = Path(setup_py_path)
        self.changelog_path = Path(changelog_path)
        
    def get_current_version(self) -> str:
        """Get the current version from setup.py"""
        if not self.setup_py_path.exists():
            raise FileNotFoundError(f"setup.py not found at {self.setup_py_path}")
            
        content = self.setup_py_path.read_text()
        version_match = re.search(r"version=['\"]([^'\"]+)['\"]", content)
        
        if not version_match:
            raise ValueError("Could not find version in setup.py")
            
        return version_match.group(1)
    
    def parse_version(self, version: str) -> Tuple[int, int, int]:
        """Parse version string into major, minor, patch tuple"""
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version)
        if not match:
            raise ValueError(f"Invalid version format: {version}")
        return int(match.group(1)), int(match.group(2)), int(match.group(3))
    
    def format_version(self, major: int, minor: int, patch: int) -> str:
        """Format version tuple into string"""
        return f"{major}.{minor}.{patch}"
    
    def analyze_unreleased_changes(self) -> Dict[str, List[str]]:
        """Analyze unreleased changes in changelog to determine version bump type"""
        if not self.changelog_path.exists():
            return {}
            
        content = self.changelog_path.read_text()
        
        # Find unreleased section
        unreleased_pattern = r"## \[Unreleased\](.*?)(?=## \[|\Z)"
        match = re.search(unreleased_pattern, content, re.DOTALL)
        
        if not match:
            return {}
            
        unreleased_content = match.group(1)
        
        # Categorize changes
        changes = {
            'breaking': [],
            'features': [],
            'fixes': [],
            'other': []
        }
        
        # Look for breaking changes indicators
        breaking_patterns = [
            r"### Removed\n(.*?)(?=\n### |\Z)",
            r"### Changed\n(.*?)(?=\n### |\Z)",  # Some changes might be breaking
        ]
        
        for pattern in breaking_patterns:
            matches = re.findall(pattern, unreleased_content, re.DOTALL)
            for match in matches:
                items = re.findall(r"^- (.+)$", match, re.MULTILINE)
                if pattern.startswith(r"### Removed"):
                    changes['breaking'].extend(items)
                else:
                    # Check if changes mention breaking, incompatible, etc.
                    for item in items:
                        if any(word in item.lower() for word in ['breaking', 'incompatible', 'removed', 'deprecated']):
                            changes['breaking'].append(item)
                        else:
                            changes['other'].append(item)
        
        # Look for new features
        feature_pattern = r"### Added\n(.*?)(?=\n### |\Z)"
        matches = re.findall(feature_pattern, unreleased_content, re.DOTALL)
        for match in matches:
            items = re.findall(r"^- (.+)$", match, re.MULTILINE)
            changes['features'].extend(items)
        
        # Look for fixes
        fix_patterns = [
            r"### Fixed\n(.*?)(?=\n### |\Z)",
            r"### Security\n(.*?)(?=\n### |\Z)",
        ]
        
        for pattern in fix_patterns:
            matches = re.findall(pattern, unreleased_content, re.DOTALL)
            for match in matches:
                items = re.findall(r"^- (.+)$", match, re.MULTILINE)
                changes['fixes'].extend(items)
        
        return changes
    
    def suggest_version_bump(self) -> Tuple[str, str]:
        """Suggest version bump type based on changelog analysis"""
        changes = self.analyze_unreleased_changes()
        
        if not any(changes.values()):
            return "none", "No unreleased changes found"
        
        if changes['breaking']:
            return "major", f"Breaking changes detected: {len(changes['breaking'])} items"
        elif changes['features']:
            return "minor", f"New features detected: {len(changes['features'])} items"
        elif changes['fixes'] or changes['other']:
            return "patch", f"Bug fixes/patches detected: {len(changes['fixes']) + len(changes['other'])} items"
        else:
            return "patch", "Default to patch for unclear changes"
    
    def bump_version(self, bump_type: str) -> str:
        """Bump version according to type (major, minor, patch)"""
        current = self.get_current_version()
        major, minor, patch = self.parse_version(current)
        
        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        elif bump_type == "patch":
            patch += 1
        else:
            raise ValueError(f"Invalid bump type: {bump_type}")
        
        new_version = self.format_version(major, minor, patch)
        return new_version
    
    def update_setup_py(self, new_version: str) -> None:
        """Update version in setup.py"""
        content = self.setup_py_path.read_text()
        
        # Replace version
        new_content = re.sub(
            r"version=['\"]([^'\"]+)['\"]",
            f'version=\'{new_version}\'',
            content
        )
        
        if new_content == content:
            raise ValueError("Could not update version in setup.py")
        
        self.setup_py_path.write_text(new_content)
        print(f"Updated setup.py version to {new_version}")
    
    def display_analysis(self) -> None:
        """Display detailed analysis of changes"""
        changes = self.analyze_unreleased_changes()
        current_version = self.get_current_version()
        suggested_bump, reason = self.suggest_version_bump()
        
        if suggested_bump == "none":
            new_version = current_version
        else:
            new_version = self.bump_version(suggested_bump)
        
        print(f"📦 Current Version: {current_version}")
        print(f"🔄 Suggested Bump: {suggested_bump.upper()}")
        print(f"🎯 New Version: {new_version}")
        print(f"💡 Reason: {reason}")
        print()
        
        if any(changes.values()):
            print("📋 Change Analysis:")
            
            if changes['breaking']:
                print(f"  🚨 Breaking Changes ({len(changes['breaking'])}):")
                for change in changes['breaking'][:3]:  # Show first 3
                    print(f"    - {change}")
                if len(changes['breaking']) > 3:
                    print(f"    ... and {len(changes['breaking']) - 3} more")
                print()
            
            if changes['features']:
                print(f"  ✨ New Features ({len(changes['features'])}):")
                for change in changes['features'][:3]:
                    print(f"    - {change}")
                if len(changes['features']) > 3:
                    print(f"    ... and {len(changes['features']) - 3} more")
                print()
            
            if changes['fixes']:
                print(f"  🐛 Bug Fixes ({len(changes['fixes'])}):")
                for change in changes['fixes'][:3]:
                    print(f"    - {change}")
                if len(changes['fixes']) > 3:
                    print(f"    ... and {len(changes['fixes']) - 3} more")
                print()
        
        print("📖 Semantic Versioning Guide:")
        print("  • MAJOR: Breaking changes, incompatible API changes")
        print("  • MINOR: New features, backwards-compatible")
        print("  • PATCH: Bug fixes, backwards-compatible")


def main():
    parser = argparse.ArgumentParser(description="Manage project versions automatically")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Current version
    subparsers.add_parser("current", help="Show current version")
    
    # Suggest version bump
    subparsers.add_parser("suggest", help="Suggest version bump based on changelog")
    
    # Bump version
    bump_parser = subparsers.add_parser("bump", help="Bump version")
    bump_group = bump_parser.add_mutually_exclusive_group(required=True)
    bump_group.add_argument("--type", choices=["major", "minor", "patch"], 
                           help="Type of version bump")
    bump_group.add_argument("--auto", action="store_true",
                           help="Auto-determine bump type from changelog")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    vm = VersionManager()
    
    try:
        if args.command == "current":
            print(vm.get_current_version())
        
        elif args.command == "suggest":
            vm.display_analysis()
        
        elif args.command == "bump":
            if args.auto:
                suggested_bump, reason = vm.suggest_version_bump()
                if suggested_bump == "none":
                    print("No version bump needed - no unreleased changes found")
                    return
                bump_type = suggested_bump
                print(f"Auto-detected bump type: {bump_type} ({reason})")
            else:
                bump_type = args.type
            
            current_version = vm.get_current_version()
            new_version = vm.bump_version(bump_type)
            
            print(f"Bumping version from {current_version} to {new_version}")
            vm.update_setup_py(new_version)
            
            print(f"✅ Version successfully bumped to {new_version}")
            print("📝 Don't forget to:")
            print("   1. Update the changelog with the new version")
            print("   2. Commit the changes")
            print("   3. Create a git tag")
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
