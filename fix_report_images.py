#!/usr/bin/env python3
"""
Convert screenshot references in DVWA lab reports to GitHub image links.

The script scans for report.md and comparison-report.md files, looks for lines
such as "**Screenshot:** `01_target_page.jpg`", and rewrites them to Markdown
image syntax. It also normalizes supported image filenames in images/ folders
to use a .JPG extension and updates existing Markdown image links to match.
Fenced code blocks are left alone.
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
NORMALIZED_EXTENSION = ".JPG"

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
IMAGE_LINK_RE = re.compile(
    r"(?P<prefix>!\[[^\]]*\]\(images/)"
    r"(?P<filename>[^)]+\.(?:jpe?g|png|gif|webp))"
    r"(?P<suffix>\))",
    re.IGNORECASE,
)


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
    return path.absolute().relative_to(root.absolute()).as_posix()


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


def normalized_name(filename: str) -> str:
    """Return the filename with the repository-standard .JPG extension."""
    return f"{Path(filename).stem}{NORMALIZED_EXTENSION}"


def normalize_images(images_dir: Path, root: Path, dry_run: bool) -> set[str]:
    """Rename supported image files in an images/ folder to use .JPG."""
    if not images_dir.is_dir():
        return set()

    images = [
        image
        for image in images_dir.iterdir()
        if image.is_file() and image.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    target_groups: dict[str, list[Path]] = {}
    collisions: set[str] = set()

    for image in images:
        target_name = normalized_name(image.name)
        target_groups.setdefault(target_name.lower(), []).append(image)

    for target_key, grouped_images in target_groups.items():
        if len(grouped_images) > 1:
            collisions.add(target_key)
            names = ", ".join(sorted(image.name for image in grouped_images))
            print(f"Name collision, skipped image rename: {names}")

    for image in images:
        target_name = normalized_name(image.name)
        target = image.with_name(target_name)

        if target_name.lower() in collisions or image.name == target_name:
            continue

        label = "Would rename image" if dry_run else "Renamed image"
        print(
            f"{label}: {display_path(image, root)} -> "
            f"{display_path(target, root)}"
        )

        if dry_run:
            continue

        # Case-only renames on Windows need a temporary filename so the final
        # extension is actually written as .JPG.
        if image.name.lower() == target.name.lower():
            temp = image.with_name(f"{image.stem}.tmp-renaming{image.suffix}")
            image.rename(temp)
            temp.rename(target)
        else:
            image.rename(target)

    return collisions


def load_images(images_dir: Path, collisions: set[str]) -> dict[str, str]:
    """Map old and normalized lowercase image filenames to normalized names."""
    if not images_dir.is_dir():
        return {}

    images: dict[str, str] = {}
    for image in images_dir.iterdir():
        if not image.is_file():
            continue
        if image.suffix.lower() in SUPPORTED_EXTENSIONS:
            fixed_name = normalized_name(image.name)
            if fixed_name.lower() in collisions:
                images.setdefault(image.name.lower(), image.name)
            else:
                for extension in SUPPORTED_EXTENSIONS:
                    images.setdefault(f"{image.stem}{extension}".lower(), fixed_name)
                images.setdefault(fixed_name.lower(), fixed_name)
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


def fix_image_links(line: str, images: dict[str, str]) -> tuple[str, bool, bool]:
    """Normalize already-existing Markdown image links outside code blocks."""
    changed = False
    found_link = False

    def replace(match: re.Match[str]) -> str:
        nonlocal changed, found_link
        found_link = True
        requested_name = match.group("filename")
        actual_name = images.get(requested_name.lower(), normalized_name(requested_name))
        replacement = f"{match.group('prefix')}{actual_name}{match.group('suffix')}"
        if replacement != match.group(0):
            changed = True
        return replacement

    return IMAGE_LINK_RE.sub(replace, line), changed, found_link


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

        fixed_link_line, link_changed, found_link = fix_image_links(line_body, images)
        if found_link:
            already_correct = True
            changed = changed or link_changed
            output.append(fixed_link_line + line_ending)
            continue

        fixed_line = replacement_for(line_body, images, images_dir, root, missing)
        if fixed_line != line_body:
            changed = True

        output.append(fixed_line + line_ending)

    return "".join(output), changed, already_correct


def process_report(
    path: Path,
    root: Path,
    dry_run: bool,
    image_collisions: dict[Path, set[str]],
) -> tuple[bool, bool, set[str]]:
    images_dir = path.parent / "images"
    images = load_images(images_dir, image_collisions.get(images_dir, set()))
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
    reports = find_reports(root)
    image_collisions: dict[Path, set[str]] = {}

    for images_dir in sorted({report.parent / "images" for report in reports}):
        image_collisions[images_dir] = normalize_images(images_dir, root, args.dry_run)

    for report in reports:
        changed, already_correct, missing = process_report(
            report, root, args.dry_run, image_collisions
        )
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
