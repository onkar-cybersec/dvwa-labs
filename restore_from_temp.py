#!/usr/bin/env python3
"""
Restore temporary image filenames and update Markdown references.

Example:
  images/02-captcha-passed.__temp__.JPG
  -> images/02-captcha-passed.JPG

Run this from the dvwa-labs repository root.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
TEMP_MARKER = ".__temp__"
IGNORED_DIRS = {".git", ".agents", ".codex", "__pycache__"}

MARKDOWN_IMAGE_RE = re.compile(
    r"(?P<prefix>!\[[^\]]*\]\()"
    r"(?P<target>[^)\s]+)"
    r"(?P<suffix>\))",
    re.IGNORECASE,
)
FENCE_RE = re.compile(r"^\s*(```|~~~)")
EXTERNAL_TARGET_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)


def repo_root() -> Path:
    return Path(__file__).resolve().parent


def display_path(path: Path, root: Path) -> str:
    return path.absolute().relative_to(root.absolute()).as_posix()


def is_ignored(path: Path, root: Path) -> bool:
    return any(part in IGNORED_DIRS for part in path.relative_to(root).parts)


def is_image(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_EXTENSIONS


def restored_name(name: str) -> str:
    path = Path(name)
    if not path.stem.endswith(TEMP_MARKER):
        return name
    return f"{path.stem[: -len(TEMP_MARKER)]}{path.suffix}"


def find_temp_image_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and is_image(path)
        and not is_ignored(path, root)
        and path.stem.endswith(TEMP_MARKER)
    )


def find_markdown_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.md")
        if path.is_file() and not is_ignored(path, root)
    )


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")


def split_target(target: str) -> tuple[str, str]:
    for marker in ("#", "?"):
        if marker in target:
            path_part, rest = target.split(marker, 1)
            return path_part, marker + rest
    return target, ""


def is_external_target(target: str) -> bool:
    return target.startswith("//") or bool(EXTERNAL_TARGET_RE.match(target))


def build_restore_map(root: Path) -> dict[str, str]:
    restore_map: dict[str, str] = {}

    for image in find_temp_image_files(root):
        target = image.with_name(restored_name(image.name))
        if target.exists():
            print(f"Skipped existing restore target: {display_path(target, root)}")
            continue

        restore_map[display_path(image, root)] = display_path(target, root)

    return restore_map


def update_markdown_references(root: Path, restore_map: dict[str, str]) -> set[str]:
    updated_files: set[str] = set()
    lower_map = {old.lower(): new for old, new in restore_map.items()}

    for markdown in find_markdown_files(root):
        content = read_text(markdown)
        output: list[str] = []
        changed = False
        in_code_block = False

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

            def replace(match: re.Match[str]) -> str:
                nonlocal changed
                target = match.group("target")
                if is_external_target(target):
                    return match.group(0)

                path_part, suffix = split_target(unquote(target))
                target_path = Path(path_part)
                if target_path.is_absolute() or not is_image(target_path):
                    return match.group(0)

                absolute = (markdown.parent / target_path).resolve()
                try:
                    relative = display_path(absolute, root)
                except ValueError:
                    return match.group(0)

                new_relative = lower_map.get(relative.lower())
                if new_relative is None:
                    return match.group(0)

                new_target = Path(new_relative).relative_to(markdown.parent.relative_to(root)).as_posix()
                changed = True
                return f"{match.group('prefix')}{new_target}{suffix}{match.group('suffix')}"

            fixed_line = MARKDOWN_IMAGE_RE.sub(replace, line_body)
            output.append(fixed_line + line_ending)

        if changed:
            markdown.write_text("".join(output), encoding="utf-8")
            updated_files.add(display_path(markdown, root))

    return updated_files


def restore_images(root: Path, restore_map: dict[str, str]) -> int:
    count = 0
    for old_relative, new_relative in sorted(restore_map.items()):
        old_path = root / old_relative
        new_path = root / new_relative
        old_path.rename(new_path)
        count += 1
        print("Restored:")
        print(old_path.name)
        print("->")
        print(new_path.name)
        print()
    return count


def main() -> int:
    root = repo_root()
    restore_map = build_restore_map(root)

    if not restore_map:
        print("Images restored: 0")
        print("Done.")
        return 0

    updated_files = update_markdown_references(root, restore_map)
    restored_count = restore_images(root, restore_map)

    for markdown in sorted(updated_files):
        print(f"Updated reference: {markdown}")

    print()
    print(f"Images restored: {restored_count}")
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
