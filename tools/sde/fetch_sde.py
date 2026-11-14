#!/usr/bin/env python3
"""Download and optionally extract the latest official EVE Online SDE.

Uses only the Python standard library. The CCP latest-build shortcut redirects
to a build-numbered archive; the resolved URL is recorded in manifest.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE = "https://developers.eveonline.com/static-data"
USER_AGENT = (
    "EveIndustrialKnowledge/0.1 "
    "(https://github.com/JMorris0n/Eve-Online-Industry)"
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def request(url: str, timeout: int = 90):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(req, timeout=timeout)


def fetch_bytes(url: str, timeout: int = 90, attempts: int = 4):
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            with request(url, timeout=timeout) as response:
                return response.read(), dict(response.headers.items()), response.geturl()
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(min(2 ** attempt, 20))
    raise RuntimeError(f"Failed to retrieve {url}: {last_error}")


def download_file(url: str, destination: Path, timeout: int = 90, attempts: int = 4):
    part = destination.with_suffix(destination.suffix + ".part")
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            digest = hashlib.sha256()
            total = 0
            with request(url, timeout=timeout) as response:
                resolved_url = response.geturl()
                headers = dict(response.headers.items())
                with part.open("wb") as output:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        output.write(chunk)
                        digest.update(chunk)
                        total += len(chunk)
            part.replace(destination)
            return {
                "resolved_url": resolved_url,
                "headers": headers,
                "bytes": total,
                "sha256": digest.hexdigest(),
            }
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
            part.unlink(missing_ok=True)
            if attempt + 1 < attempts:
                time.sleep(min(2 ** attempt, 20))
    raise RuntimeError(f"Failed to download {url}: {last_error}")


def safe_extract(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.infolist():
            target = (destination / member.filename).resolve()
            if target != root and root not in target.parents:
                raise RuntimeError(f"Unsafe path in SDE archive: {member.filename}")
        bundle.extractall(destination)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=("jsonl", "yaml"), default="jsonl")
    parser.add_argument("--output-dir", type=Path, default=Path("data/raw/sde"))
    parser.add_argument("--extract", action="store_true", help="Extract the downloaded archive")
    parser.add_argument("--force", action="store_true", help="Replace an existing archive")
    parser.add_argument("--timeout", type=int, default=90)
    args = parser.parse_args()

    latest_manifest_url = f"{BASE}/tranquility/latest.jsonl"
    latest_archive_url = f"{BASE}/eve-online-static-data-latest-{args.variant}.zip"

    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest_bytes, manifest_headers, manifest_resolved = fetch_bytes(
        latest_manifest_url, timeout=args.timeout
    )
    latest_manifest_path = args.output_dir / "latest.jsonl"
    latest_manifest_path.write_bytes(manifest_bytes)

    manifest_text = manifest_bytes.decode("utf-8-sig")
    sde_record: Any = None
    for line in manifest_text.splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if record.get("_key") == "sde":
            sde_record = record.get("_value", record)
            break

    # Download once to a staging file. The resolved URL contains the build
    # number, avoiding a separate HEAD request and a possible release race.
    staging = args.output_dir / f"eve-online-static-data-latest-{args.variant}.zip"
    if staging.exists():
        staging.unlink()
    info = download_file(latest_archive_url, staging, timeout=args.timeout)
    filename_pattern = re.compile(
        r"eve-online-static-data-(\\d+)-" + re.escape(args.variant) + r"\\.zip$"
    )
    match = filename_pattern.search(info["resolved_url"])
    if not match:
        staging.unlink(missing_ok=True)
        raise RuntimeError(
            "CCP archive URL did not contain the expected build number: "
            + info["resolved_url"]
        )

    build_number = match.group(1)
    target_dir = args.output_dir / build_number
    target_dir.mkdir(parents=True, exist_ok=True)
    archive = target_dir / f"eve-online-static-data-{build_number}-{args.variant}.zip"

    if archive.exists() and not args.force:
        existing_hash = hashlib.sha256(archive.read_bytes()).hexdigest()
        staging.unlink(missing_ok=True)
        if existing_hash != info["sha256"]:
            raise FileExistsError(
                f"{archive} exists but its checksum differs; use --force to replace it"
            )
    else:
        staging.replace(archive)

    if not zipfile.is_zipfile(archive):
        raise RuntimeError(f"Downloaded file is not a valid ZIP archive: {archive}")
    with zipfile.ZipFile(archive) as bundle:
        corrupt_member = bundle.testzip()
        if corrupt_member:
            raise RuntimeError(f"ZIP integrity test failed at member: {corrupt_member}")

    extracted_path = None
    if args.extract:
        extracted_path = target_dir / "extracted"
        safe_extract(archive, extracted_path)

    metadata = {
        "source": "CCP EVE Online Static Data Export",
        "build_number": build_number,
        "variant": args.variant,
        "retrieved_at": utc_now(),
        "latest_manifest_url": latest_manifest_url,
        "latest_manifest_resolved_url": manifest_resolved,
        "latest_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "latest_manifest_etag": manifest_headers.get("ETag"),
        "sde_record": sde_record,
        "archive_url": latest_archive_url,
        "archive_resolved_url": info["resolved_url"],
        "archive_bytes": info["bytes"],
        "archive_sha256": info["sha256"],
        "archive_etag": info["headers"].get("ETag"),
        "archive_last_modified": info["headers"].get("Last-Modified"),
        "zip_integrity_test": "passed",
        "extracted_to": str(extracted_path) if extracted_path else None,
    }
    manifest_path = target_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(metadata, indent=2, ensure_ascii=False))
    print(f"\nSDE saved to: {archive}")
    if extracted_path:
        print(f"Extracted to: {extracted_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
