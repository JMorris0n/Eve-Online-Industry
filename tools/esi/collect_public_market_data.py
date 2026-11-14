#!/usr/bin/env python3
"""Collect selected public EVE ESI market and industry data with cache support.

Uses only the Python standard library. No EVE SSO token is required.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any

BASE_URL = "https://esi.evetech.net"
DEFAULT_USER_AGENT = (
    "EveIndustrialKnowledge/0.1 "
    "(https://github.com/JMorris0n/Eve-Online-Industry)"
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat(timespec="seconds").replace("+00:00", "Z")


def parse_http_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except (TypeError, ValueError, OverflowError):
        return None


def retry_after_seconds(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        parsed = parse_http_date(value)
        if parsed is None:
            return None
        return max(0.0, (parsed - utc_now()).total_seconds())


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


class ESIClient:
    def __init__(
        self,
        cache_dir: Path,
        compatibility_date: str,
        user_agent: str,
        timeout: int = 60,
        max_retries: int = 3,
    ) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.compatibility_date = compatibility_date
        self.user_agent = user_agent
        self.timeout = timeout
        self.max_retries = max_retries
        self.request_log: list[dict[str, Any]] = []

    def _cache_paths(self, url: str) -> tuple[Path, Path]:
        key = hashlib.sha256(url.encode("utf-8")).hexdigest()
        return self.cache_dir / f"{key}.json", self.cache_dir / f"{key}.meta.json"

    def get_json(self, url: str) -> tuple[Any, dict[str, Any]]:
        body_path, meta_path = self._cache_paths(url)
        cached_meta: dict[str, Any] = {}
        cached_body: bytes | None = None

        if body_path.exists() and meta_path.exists():
            try:
                cached_meta = json.loads(meta_path.read_text(encoding="utf-8"))
                cached_body = body_path.read_bytes()
            except (OSError, json.JSONDecodeError):
                cached_meta = {}
                cached_body = None

        if cached_body is not None:
            expires = parse_http_date(cached_meta.get("expires"))
            if expires and utc_now() < expires:
                info = {
                    "url": url,
                    "status": "cache-hit",
                    "retrieved_at": iso_now(),
                    "from_cache": True,
                    "requested_compatibility_date": self.compatibility_date,
                    "matched_compatibility_date": cached_meta.get("headers", {}).get(
                        "x-compatibility-date"
                    ),
                    "headers": cached_meta.get("headers", {}),
                    "sha256": hashlib.sha256(cached_body).hexdigest(),
                }
                self.request_log.append(info)
                return json.loads(cached_body), info

        headers = {
            "Accept": "application/json",
            "User-Agent": self.user_agent,
            "X-Compatibility-Date": self.compatibility_date,
        }
        if cached_meta.get("etag"):
            headers["If-None-Match"] = cached_meta["etag"]
        if cached_meta.get("last_modified"):
            headers["If-Modified-Since"] = cached_meta["last_modified"]

        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            request = urllib.request.Request(url, headers=headers)
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    body = response.read()
                    response_headers = {key.lower(): value for key, value in response.headers.items()}
                    info = {
                        "url": url,
                        "status": response.status,
                        "retrieved_at": iso_now(),
                        "from_cache": False,
                        "requested_compatibility_date": self.compatibility_date,
                        "matched_compatibility_date": response_headers.get(
                            "x-compatibility-date"
                        ),
                        "headers": response_headers,
                        "sha256": hashlib.sha256(body).hexdigest(),
                    }
                    body_path.write_bytes(body)
                    metadata = {
                        "url": url,
                        "etag": response_headers.get("etag"),
                        "last_modified": response_headers.get("last-modified"),
                        "expires": response_headers.get("expires"),
                        "headers": response_headers,
                        "saved_at": info["retrieved_at"],
                    }
                    write_json(meta_path, metadata)
                    self.request_log.append(info)
                    return json.loads(body), info

            except urllib.error.HTTPError as exc:
                response_headers = {key.lower(): value for key, value in exc.headers.items()} if exc.headers else {}

                if exc.code == 304 and cached_body is not None:
                    metadata = {
                        **cached_meta,
                        "etag": response_headers.get("etag", cached_meta.get("etag")),
                        "last_modified": response_headers.get(
                            "last-modified", cached_meta.get("last_modified")
                        ),
                        "expires": response_headers.get("expires", cached_meta.get("expires")),
                        "headers": {**cached_meta.get("headers", {}), **response_headers},
                        "saved_at": iso_now(),
                    }
                    write_json(meta_path, metadata)
                    info = {
                        "url": url,
                        "status": 304,
                        "retrieved_at": iso_now(),
                        "from_cache": True,
                        "requested_compatibility_date": self.compatibility_date,
                        "matched_compatibility_date": metadata["headers"].get(
                            "x-compatibility-date"
                        ),
                        "headers": metadata["headers"],
                        "sha256": hashlib.sha256(cached_body).hexdigest(),
                    }
                    self.request_log.append(info)
                    return json.loads(cached_body), info

                if exc.code == 420:
                    remain = response_headers.get("x-esi-error-limit-remain")
                    reset = response_headers.get("x-esi-error-limit-reset")
                    raise RuntimeError(
                        "ESI returned HTTP 420 (error limit). Stop requests and wait "
                        f"for the reset. Remaining={remain}, reset_seconds={reset}"
                    ) from exc

                if exc.code == 429:
                    wait = retry_after_seconds(response_headers.get("retry-after"))
                    if wait is None or attempt >= self.max_retries:
                        raise RuntimeError(
                            "ESI returned HTTP 429; Retry-After was missing or retry "
                            "limit was reached. Stop and retry later."
                        ) from exc
                    time.sleep(wait)
                    continue

                if 500 <= exc.code < 600 and attempt < self.max_retries:
                    time.sleep(min(2 ** attempt, 20))
                    continue

                raise RuntimeError(
                    f"ESI request failed with HTTP {exc.code}: {url}"
                ) from exc

            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(min(2 ** attempt, 20))
                    continue
                raise RuntimeError(f"ESI request failed: {url}: {last_error}") from exc

        raise RuntimeError(f"ESI request failed after retries: {url}: {last_error}")

    def get_pages(self, url: str) -> list[tuple[Any, dict[str, Any]]]:
        first_url = url + ("&" if "?" in url else "?") + "page=1"
        first_data, first_info = self.get_json(first_url)
        page_count = int(first_info.get("headers", {}).get("x-pages", "1"))
        pages = [(first_data, first_info)]

        for page_number in range(2, page_count + 1):
            page_url = url + ("&" if "?" in url else "?") + f"page={page_number}"
            pages.append(self.get_json(page_url))
        return pages


def endpoint_url(path: str, params: dict[str, Any] | None = None) -> str:
    query = urllib.parse.urlencode(params or {})
    return f"{BASE_URL}{path}" + (f"?{query}" if query else "")


def save_response(
    output_dir: Path,
    filename: str,
    data: Any,
    info: dict[str, Any],
) -> dict[str, Any]:
    path = output_dir / filename
    write_json(path, data)
    return {
        "file": str(path),
        "url": info["url"],
        "status": info["status"],
        "retrieved_at": info["retrieved_at"],
        "from_cache": info["from_cache"],
        "sha256": info["sha256"],
        "expires": info.get("headers", {}).get("expires"),
        "etag": info.get("headers", {}).get("etag"),
        "requested_compatibility_date": info.get("requested_compatibility_date"),
        "matched_compatibility_date": info.get("matched_compatibility_date"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--compatibility-date", required=True, help="Reviewed ESI date, YYYY-MM-DD")
    parser.add_argument("--output-dir", type=Path, default=Path("data/raw/esi"))
    parser.add_argument("--cache-dir", type=Path, default=Path("data/cache/esi"))
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args()

    try:
        datetime.strptime(args.compatibility_date, "%Y-%m-%d")
    except ValueError:
        parser.error("--compatibility-date must use YYYY-MM-DD")

    config = json.loads(args.config.read_text(encoding="utf-8"))
    regions = sorted(set(int(value) for value in config.get("regions", [])))
    type_ids = sorted(set(int(value) for value in config.get("type_ids", [])))

    run_id = utc_now().strftime("%Y%m%dT%H%M%SZ")
    output_dir = args.output_dir / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    client = ESIClient(
        cache_dir=args.cache_dir,
        compatibility_date=args.compatibility_date,
        user_agent=args.user_agent,
        timeout=args.timeout,
    )
    outputs: list[dict[str, Any]] = []

    if config.get("include_industry_systems", True):
        data, info = client.get_json(endpoint_url("/industry/systems/"))
        outputs.append(save_response(output_dir, "industry-systems.json", data, info))

    if config.get("include_market_prices", True):
        data, info = client.get_json(endpoint_url("/markets/prices/"))
        outputs.append(save_response(output_dir, "market-prices.json", data, info))

    for region_id in regions:
        for type_id in type_ids:
            orders_url = endpoint_url(
                f"/markets/{region_id}/orders/",
                {"datasource": "tranquility", "order_type": "all", "type_id": type_id},
            )
            pages = client.get_pages(orders_url)
            for page_number, (data, info) in enumerate(pages, start=1):
                filename = f"market-orders-region-{region_id}-type-{type_id}-page-{page_number}.json"
                outputs.append(save_response(output_dir, filename, data, info))

            history_url = endpoint_url(
                f"/markets/{region_id}/history/",
                {"datasource": "tranquility", "type_id": type_id},
            )
            data, info = client.get_json(history_url)
            filename = f"market-history-region-{region_id}-type-{type_id}.json"
            outputs.append(save_response(output_dir, filename, data, info))

    manifest = {
        "project": "EVE Online Industrial Knowledge Base",
        "retrieved_at": iso_now(),
        "esi_base_url": BASE_URL,
        "compatibility_date": args.compatibility_date,
        "user_agent": args.user_agent,
        "regions": regions,
        "type_ids": type_ids,
        "outputs": outputs,
        "requests": client.request_log,
        "notes": [
            "Public read-only endpoints only; no EVE SSO token is used.",
            "ESI cache headers and ETags are respected.",
            "HTTP 420 stops collection; HTTP 429 honors Retry-After.",
            "Market orders and history are separate observations.",
        ],
    }
    write_json(output_dir / "manifest.json", manifest)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"\nRaw ESI data saved to: {output_dir}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
