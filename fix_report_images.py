#!/usr/bin/env python3
"""
Fix image links in DVWA lab Markdown files for GitHub.

The script recursively scans report.md, comparison-report.md, and README.md
files. It fixes old screenshot references and existing Markdown image links so
they point to the local images/ folder. Before fixing Markdown, it renames
lowercase .jpg files in every images/ folder to uppercase .JPG so links and
files use the same GitHub-safe extension case. Fenced code blocks and external
URLs are left unchanged.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote


REPORT_NAMES = {"report.md", "comparison-report.md", "README.md"}
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
IGNORED_DIRS = {".git", ".agents", ".codex", "__pycache__"}

SCREENSHOT_RE = re.compile(
    r"""^(?P<indent>\s*)
        (?P<prefix>\*\*)?
        Screenshot:
        (?P=prefix)?
        \s*
        `?
        (?P<filename>[^`\s/\\]+\.(?:jpe?g|png|gif|webp))
        `?
        \s*$""",
    re.IGNORECASE | re.VERBOSE,
)

MARKDOWN_IMAGE_RE = re.compile(
    r"(?P<prefix>!\[[^\]]*\]\()"
    r"(?P<target>[^)\s]+)"
    r"(?P<suffix>\))",
    re.IGNORECASE,
)

FENCE_RE = re.compile(r"^\s*(```|~~~)")
EXTERNAL_TARGET_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)


@dataclass
class ChangeLog:
    fixed_paths: set[str] = field(default_factory=set)
    corrected_filenames: set[tuple[str, str]] = field(default_factory=set)
    corrected_folders: set[tuple[str, str]] = field(default_factory=set)
    renamed_images: set[tuple[str, str]] = field(default_factory=set)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fix DVWA report image links for GitHub."
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
    return path.absolute().relative_to(root.absolute()).as_posix()


def is_ignored(path: Path, root: Path) -> bool:
    return any(part in IGNORED_DIRS for part in path.relative_to(root).parts)


def find_markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if path.is_file() and path.name in REPORT_NAMES and not is_ignored(path, root):
            files.append(path)
    return sorted(files)


def find_images_dirs(root: Path) -> list[Path]:
    dirs: list[Path] = []
    for path in root.rglob("*"):
        if path.is_dir() and path.name.lower() == "images" and not is_ignored(path, root):
            dirs.append(path)
    return sorted(dirs)


def rename_lowercase_jpg_files(root: Path, dry_run: bool, log: ChangeLog) -> None:
    """Rename every images/*.jpg file to images/*.JPG across the repository."""
    for images_dir in find_images_dirs(root):
        for image in sorted(images_dir.iterdir()):
            if not image.is_file() or image.suffix != ".jpg":
                continue

            target = image.with_suffix(".JPG")
            old_display = display_path(image, root)
            new_display = display_path(target, root)
            log.renamed_images.add((old_display, new_display))

            if dry_run:
                continue

            # Windows treats .jpg and .JPG as the same path, so use a temporary
            # filename to force a case-only rename to be persisted.
            temp = image.with_name(f"{image.stem}.tmp-renaming{image.suffix}")
            image.rename(temp)
            temp.rename(target)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")


def load_local_images(markdown_file: Path) -> dict[str, str]:
    """Map lowercase filenames in the nearby images/ folder to real filenames."""
    images_dir = markdown_file.parent / "images"
    if not images_dir.is_dir():
        return {}

    images: dict[str, str] = {}
    for image in images_dir.iterdir():
        if image.is_file() and image.suffix.lower() in SUPPORTED_EXTENSIONS:
            images.setdefault(image.name.lower(), image.name)

    return images


def clean_markdown_target(target: str) -> tuple[str, str]:
    """Split a Markdown link target into path and optional #anchor/?query suffix."""
    for marker in ("#", "?"):
        if marker in target:
            path_part, rest = target.split(marker, 1)
            return path_part, marker + rest
    return target, ""


def is_external_target(target: str) -> bool:
    return target.startswith("//") or bool(EXTERNAL_TARGET_RE.match(target))


def folder_label(path_text: str) -> str:
    parent = Path(path_text).parent.as_posix()
    if parent in ("", "."):
        return ""
    return parent.rstrip("/") + "/"


def resolve_image_name(requested_name: str, images: dict[str, str]) -> str | None:
    return images.get(requested_name.lower())


def fix_markdown_image_link(
    match: re.Match[str],
    images: dict[str, str],
    log: ChangeLog,
) -> str:
    target = match.group("target")
    if is_external_target(target):
        return match.group(0)

    path_part, suffix = clean_markdown_target(unquote(target))
    requested_path = Path(path_part)

    if requested_path.is_absolute() or requested_path.name == "":
        return match.group(0)

    if requested_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return match.group(0)

    actual_name = resolve_image_name(requested_path.name, images)
    if actual_name is None:
        return match.group(0)

    fixed_target = f"images/{actual_name}{suffix}"

    if requested_path.name != actual_name:
        log.corrected_filenames.add((requested_path.name, actual_name))

    old_folder = folder_label(path_part)
    if old_folder != "images/":
        log.corrected_folders.add((old_folder or "(none)", "images/"))

    return f"{match.group('prefix')}{fixed_target}{match.group('suffix')}"


def fix_screenshot_reference(
    line: str,
    images: dict[str, str],
    images_dir: Path,
    root: Path,
    missing: set[str],
    log: ChangeLog,
) -> str:
    match = SCREENSHOT_RE.match(line)
    if not match:
        return line

    requested_name = match.group("filename")
    actual_name = resolve_image_name(requested_name, images)
    if actual_name is None:
        missing_path = images_dir / requested_name
        missing.add(display_path(missing_path, root))
        print(f"Missing image: {requested_name}")
        print(f"Path: {display_path(images_dir, root)}/")
        return line

    if requested_name != actual_name:
        log.corrected_filenames.add((requested_name, actual_name))

    alt_text = Path(actual_name).stem
    return f"{match.group('indent')}![{alt_text}](images/{actual_name})"


def fix_content(
    content: str,
    markdown_file: Path,
    root: Path,
    log: ChangeLog,
    missing: set[str],
) -> tuple[str, bool, bool]:
    images = load_local_images(markdown_file)
    images_dir = markdown_file.parent / "images"
    output: list[str] = []
    in_code_block = False
    changed = False
    saw_image_link = False

    for raw_line in content.splitlines(keepends=True):
        line_body = raw_line.rstrip("\r\n")
        line_ending = raw_line[len(line_body) :]

        if FENCE_RE.match(line_body):
            in_code_block = not in_code_block
            output.append(raw_line)
            continue

        if in_code_block:
            output.append(raw_line)
            continue

        fixed_line = MARKDOWN_IMAGE_RE.sub(
            lambda match: fix_markdown_image_link(match, images, log),
            line_body,
        )

        if fixed_line != line_body:
            changed = True
            saw_image_link = True
            output.append(fixed_line + line_ending)
            continue

        if MARKDOWN_IMAGE_RE.search(line_body):
            saw_image_link = True

        fixed_line = fix_screenshot_reference(
            line_body, images, images_dir, root, missing, log
        )
        if fixed_line != line_body:
            changed = True

        output.append(fixed_line + line_ending)

    return "".join(output), changed, saw_image_link


def process_markdown_file(
    path: Path,
    root: Path,
    dry_run: bool,
    log: ChangeLog,
) -> tuple[bool, bool, set[str]]:
    missing: set[str] = set()
    original_content = read_text(path)
    fixed_content, changed, saw_image_link = fix_content(
        original_content, path, root, log, missing
    )

    if changed:
        log.fixed_paths.add(display_path(path, root))
        if not dry_run:
            backup_path = path.with_name(path.name + ".bak")
            shutil.copy2(path, backup_path)
            path.write_text(fixed_content, encoding="utf-8")

    return changed, saw_image_link, missing


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


def print_summary(log: ChangeLog, missing_all: set[str], dry_run: bool) -> None:
    image_label = "Would rename image" if dry_run else "Renamed image"
    for old_path, new_path in sorted(log.renamed_images):
        print(f"{image_label}: {old_path} -> {new_path}")

    path_label = "Would fix path" if dry_run else "Fixed path"
    for path in sorted(log.fixed_paths):
        print(f"{path_label}: {path}")

    for old_name, new_name in sorted(log.corrected_filenames):
        print()
        print("Corrected filename:")
        print(old_name)
        print("->")
        print(new_name)

    for old_folder, new_folder in sorted(log.corrected_folders):
        print()
        print("Corrected folder:")
        print(old_folder)
        print("->")
        print(new_folder)

    for missing_path in sorted(missing_all):
        print(f"Missing: {missing_path}")


def main() -> int:
    args = parse_args()
    root = repo_root()
    log = ChangeLog()
    missing_all: set[str] = set()

    rename_lowercase_jpg_files(root, args.dry_run, log)

    for markdown_file in find_markdown_files(root):
        changed, saw_image_link, missing = process_markdown_file(
            markdown_file, root, args.dry_run, log
        )
        if not changed and saw_image_link:
            print(
                f"Skipped: {display_path(markdown_file, root)} "
                "(already correct)"
            )
        missing_all.update(missing)

    print_summary(log, missing_all, args.dry_run)

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
