#!/usr/bin/env python3
"""
Convert plain screenshot references in DVWA lab reports to GitHub image links.

The script scans for report.md and comparison-report.md files, looks for lines
such as "**Screenshot:** `01_target_page.jpg`", and rewrites them to Markdown
image syntax using the exact case of the matching file in the local images/
folder. Fenced code blocks and already-correct Markdown images are left alone.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


REPORT_NAMES = {"report.md", "comparison-report.md"}
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

# Matches simple screenshot references, with optional Markdown bold and/or
# backticks around the filename. It intentionally handles one reference per line.
SCREENSHOT_RE = re.compile(
    r"""^(?P<indent>\s*)
        (?P<prefix>\*\*)?
        Screenshot:
        (?P=prefix)?
        \s*
        `?
        (?P<filename>[^`\s]+\.(?:jpe?g|png|gif|webp))
        `?
        \s*$""",
    re.IGNORECASE | re.VERBOSE,
)

FENCE_RE = re.compile(r"^\s*(```|~~~)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fix screenshot references in report Markdown files."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would change without editing files or creating backups",
    )
    parser.add_argument(
        "--git-add",
        action="store_true",
        help="run 'git add .' after files are updated",
    )
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parent


def display_path(path: Path, root: Path) -> str:
    """Return a stable, forward-slash path for status output."""
    return path.resolve().relative_to(root.resolve()).as_posix()


def find_reports(root: Path) -> list[Path]:
    ignored_dirs = {".git", ".agents", ".codex", "__pycache__"}
    reports: list[Path] = []

    for path in root.rglob("*"):
        if not path.is_file() or path.name not in REPORT_NAMES:
            continue
        if any(part in ignored_dirs for part in path.relative_to(root).parts):
            continue
        reports.append(path)

    return sorted(reports)


def load_images(images_dir: Path) -> dict[str, str]:
    """Map lowercase image filenames to their actual case-sensitive filenames."""
    if not images_dir.is_dir():
        return {}

    images: dict[str, str] = {}
    for image in images_dir.iterdir():
        if not image.is_file():
            continue
        if image.suffix.lower() in SUPPORTED_EXTENSIONS:
            images.setdefault(image.name.lower(), image.name)
    return images


def replacement_for(
    line: str,
    images: dict[str, str],
    images_dir: Path,
    root: Path,
    missing: set[str],
) -> str:
    match = SCREENSHOT_RE.match(line)
    if not match:
        return line

    requested_name = match.group("filename")
    actual_name = images.get(requested_name.lower())
    if actual_name is None:
        missing_path = images_dir / requested_name
        missing.add(display_path(missing_path, root))
        print(f"Missing image: {requested_name}")
        print(f"Path: {display_path(images_dir, root)}/")
        return line

    alt_text = Path(actual_name).stem
    return f"{match.group('indent')}![{alt_text}](images/{actual_name})"


def fix_content(
    content: str,
    images: dict[str, str],
    images_dir: Path,
    root: Path,
    missing: set[str],
) -> tuple[str, bool, bool]:
    lines = content.splitlines(keepends=True)
    output: list[str] = []
    in_code_block = False
    changed = False
    already_correct = False

    for raw_line in lines:
        line_body = raw_line.rstrip("\r\n")
        line_ending = raw_line[len(line_body) :]

        if FENCE_RE.match(line_body):
            in_code_block = not in_code_block
            output.append(raw_line)
            continue

        if in_code_block:
            output.append(raw_line)
            continue

        if re.search(r"!\[[^\]]*\]\(images/[^)]+\)", line_body, re.IGNORECASE):
            already_correct = True
            output.append(raw_line)
            continue

        fixed_line = replacement_for(line_body, images, images_dir, root, missing)
        if fixed_line != line_body:
            changed = True

        output.append(fixed_line + line_ending)

    return "".join(output), changed, already_correct


def process_report(path: Path, root: Path, dry_run: bool) -> tuple[bool, bool, set[str]]:
    images_dir = path.parent / "images"
    images = load_images(images_dir)
    missing: set[str] = set()

    content = path.read_text(encoding="utf-8")
    fixed_content, changed, already_correct = fix_content(
        content, images, images_dir, root, missing
    )

    if changed and not dry_run:
        backup_path = path.with_name(path.name + ".bak")
        shutil.copy2(path, backup_path)
        path.write_text(fixed_content, encoding="utf-8")

    return changed, already_correct, missing


def run_git_add(root: Path) -> int:
    try:
        result = subprocess.run(["git", "add", "."], cwd=root, check=False)
    except FileNotFoundError:
        print("Git staging failed: git was not found on PATH.")
        return 1

    if result.returncode == 0:
        print("Git staging complete.")
    else:
        print("Git staging failed.")

    return result.returncode


def main() -> int:
    args = parse_args()
    root = repo_root()

    updated: list[str] = []
    skipped: list[str] = []
    missing_all: set[str] = set()

    for report in find_reports(root):
        changed, already_correct, missing = process_report(report, root, args.dry_run)
        report_display = display_path(report, root)

        if changed:
            label = "Would update" if args.dry_run else "Updated"
            print(f"{label}: {report_display}")
            updated.append(report_display)
        elif already_correct:
            print(f"Skipped: {report_display} (already correct)")
            skipped.append(report_display)

        missing_all.update(missing)

    for missing_path in sorted(missing_all):
        print(f"Missing: {missing_path}")

    if args.git_add:
        if args.dry_run:
            print("Git staging skipped in dry-run mode.")
        else:
            git_status = run_git_add(root)
            if git_status != 0:
                print()
                print("Done.")
                return git_status

    print()
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
