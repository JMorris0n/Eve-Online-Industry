#!/usr/bin/env python3
"""Check repository-local targets in Markdown links without third-party packages."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

LINK_PATTERN = re.compile(
    r"""!?\[[^\]]*\]\(\s*(<[^>]+>|[^)\s]+)(?:\s+["'][^"']*["'])?\s*\)"""
)
FENCE_PATTERN = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE_PATTERN = re.compile(r"`+[^\`]*`+")


def extract_links(markdown: str):
    """Yield (one-based line number, destination) for inline Markdown links/images.

    Fenced code blocks and inline code spans are ignored. Reference-style links,
    raw HTML links, and heading-anchor existence are intentionally out of scope.
    """
    in_fence = False
    fence_char = ""
    fence_length = 0

    for line_number, line in enumerate(markdown.splitlines(), start=1):
        fence = FENCE_PATTERN.match(line)
        if fence:
            marker = fence.group(1)
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
                fence_length = len(marker)
                continue
            if marker[0] == fence_char and len(marker) >= fence_length:
                in_fence = False
                fence_char = ""
                fence_length = 0
                continue

        if in_fence:
            continue

        searchable = INLINE_CODE_PATTERN.sub("", line)
        for match in LINK_PATTERN.finditer(searchable):
            destination = match.group(1)
            if destination.startswith("<") and destination.endswith(">"):
                destination = destination[1:-1]
            if destination:
                yield line_number, destination


def local_target_exists(root: Path, source_file: Path, destination: str) -> bool:
    """Return whether a relative or repository-root-relative file target exists.

    External URLs and fragment-only links are not checked. Directory links are
    accepted when they contain index.md or README.md. Paths that escape the
    repository root are rejected.
    """
    parsed = urlsplit(destination)
    if parsed.scheme or parsed.netloc or destination.startswith("//"):
        return True
    if not parsed.path:
        return True

    decoded_path = unquote(parsed.path)
    if decoded_path.startswith("/"):
        target = root / decoded_path.lstrip("/")
    else:
        target = source_file.parent / decoded_path

    root_resolved = root.resolve()
    target_resolved = target.resolve()
    try:
        target_resolved.relative_to(root_resolved)
    except ValueError:
        return False

    if target_resolved.is_dir():
        return any((target_resolved / name).is_file() for name in ("index.md", "README.md"))
    return target_resolved.is_file()


def markdown_files(root: Path):
    """Return Markdown files while excluding generated, cache, and VCS data."""
    excluded = {".git", ".venv", "__pycache__", "data"}
    for path in root.rglob("*.md"):
        relative = path.relative_to(root)
        if any(part in excluded for part in relative.parts):
            continue
        if relative.parts[:2] == ("exports", "generated"):
            continue
        yield path


def check_repository(root: Path):
    errors = []
    file_count = 0
    link_count = 0

    for source in markdown_files(root):
        file_count += 1
        relative_source = source.relative_to(root)
        markdown = source.read_text(encoding="utf-8")
        for line_number, destination in extract_links(markdown):
            parsed = urlsplit(destination)
            if parsed.scheme or parsed.netloc or destination.startswith("//") or not parsed.path:
                continue
            link_count += 1
            if not local_target_exists(root, source, destination):
                errors.append((relative_source.as_posix(), line_number, destination))

    return file_count, link_count, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="repository root (defaults to the parent of tools/)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        print(f"ERROR: repository root does not exist: {root}", file=sys.stderr)
        return 2

    try:
        file_count, link_count, errors = check_repository(root)
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: unable to scan repository: {exc}", file=sys.stderr)
        return 2

    if errors:
        print(f"Found {len(errors)} broken local Markdown link(s):")
        for source, line_number, destination in errors:
            print(f"{source}:{line_number}: {destination}")
        print(f"Checked {file_count} Markdown files and {link_count} local links.")
        return 1

    print(f"OK: checked {file_count} Markdown files and {link_count} local links.")
    print("External URLs and heading-anchor targets are not validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
