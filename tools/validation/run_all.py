#!/usr/bin/env python3
"""Run the repository's local calculation, validation, and Markdown-link checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKS = [
    (
        "Calculation unit tests",
        [
            sys.executable, "-m", "unittest", "discover",
            "-s", "tools/calculations", "-p", "test_*.py", "-v",
        ],
    ),
    (
        "Validation-tool unit tests",
        [
            sys.executable, "-m", "unittest", "discover",
            "-s", "tools/validation", "-p", "test_*.py", "-v",
        ],
    ),
    (
        "Operating-profile unit tests",
        [
            sys.executable, "-m", "unittest", "discover",
            "-s", "tools/profile", "-p", "test_*.py", "-v",
        ],
    ),
    (
        "SDE recipe parser unit tests",
        [
            sys.executable, "-m", "unittest", "discover",
            "-s", "tools/sde", "-p", "test_*.py", "-v",
        ],
    ),
    (
        "Local Markdown links",
        [sys.executable, "tools/validation/check_markdown_links.py"],
    ),
]


def main() -> int:
    failed = []
    for label, command in CHECKS:
        print(f"\n=== {label} ===", flush=True)
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode != 0:
            failed.append((label, result.returncode))

    print("\n=== Validation summary ===")
    if failed:
        for label, return_code in failed:
            print(f"FAIL: {label} (exit {return_code})")
        print(f"{len(failed)} check group(s) failed.")
        return 1

    print(f"PASS: all {len(CHECKS)} check groups completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
