#!/usr/bin/env python3
"""
Remove Markdown backup files created by fix_report_images.py.

By default this deletes report.md.bak and comparison-report.md.bak files
recursively from the repository root. Use --dry-run to preview the files first.
"""

from __future__ import annotations

import argparse
from pathlib import Path


BACKUP_NAMES = {"report.md.bak", "comparison-report.md.bak"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Remove report backup files.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show backup files that would be deleted without removing them",
    )
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parent


def display_path(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def find_backups(root: Path) -> list[Path]:
    ignored_dirs = {".git", ".agents", ".codex", "__pycache__"}
    backups: list[Path] = []

    for path in root.rglob("*"):
        if not path.is_file() or path.name not in BACKUP_NAMES:
            continue
        if any(part in ignored_dirs for part in path.relative_to(root).parts):
            continue
        backups.append(path)

    return sorted(backups)


def main() -> int:
    args = parse_args()
    root = repo_root()
    backups = find_backups(root)

    if not backups:
        print("No backup files found.")
        return 0

    for backup in backups:
        label = "Would remove" if args.dry_run else "Removed"
        print(f"{label}: {display_path(backup, root)}")
        if not args.dry_run:
            backup.unlink()

    print()
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
