#!/usr/bin/env python3
"""Inspect the file layout of an official EVE SDE ZIP or extracted directory."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path


KEYWORDS = (
    "blueprint",
    "schematic",
    "planet",
    "type",
    "industry",
    "reaction",
    "market",
    "map",
)


def inspect_archive(path: Path, limit: int) -> None:
    with zipfile.ZipFile(path) as archive:
        entries = sorted(archive.infolist(), key=lambda item: item.filename.lower())
        print(f"Archive: {path}")
        print(f"Entries: {len(entries)}")
        print("\nRelevant files:")
        relevant = [
            item for item in entries
            if any(word in item.filename.lower() for word in KEYWORDS)
        ]
        for item in relevant[:limit]:
            print(f"{item.file_size:>12,}  {item.filename}")
        if len(relevant) > limit:
            print(f"... {len(relevant) - limit} additional matching files")
        print("\nFirst JSONL record from selected files:")
        for item in relevant:
            if item.filename.lower().endswith(".jsonl") and item.file_size:
                with archive.open(item) as stream:
                    line = stream.readline().decode("utf-8-sig").strip()
                try:
                    sample = json.loads(line)
                except json.JSONDecodeError:
                    sample = line[:300]
                print(f"\n{item.filename}")
                print(json.dumps(sample, indent=2, ensure_ascii=False)[:1200])
                break


def inspect_directory(path: Path, limit: int) -> None:
    files = sorted((item for item in path.rglob("*") if item.is_file()), key=lambda p: str(p).lower())
    relevant = [
        item for item in files
        if any(word in item.name.lower() for word in KEYWORDS)
    ]
    print(f"Directory: {path}")
    print(f"Files: {len(files)}")
    print("\nRelevant files:")
    for item in relevant[:limit]:
        print(f"{item.stat().st_size:>12,}  {item.relative_to(path)}")
    if len(relevant) > limit:
        print(f"... {len(relevant) - limit} additional matching files")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="SDE ZIP archive or extracted directory")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    if not args.path.exists():
        parser.error(f"Path does not exist: {args.path}")
    if args.path.is_dir():
        inspect_directory(args.path, args.limit)
    elif zipfile.is_zipfile(args.path):
        inspect_archive(args.path, args.limit)
    else:
        parser.error("Path is neither a directory nor a valid ZIP archive")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
