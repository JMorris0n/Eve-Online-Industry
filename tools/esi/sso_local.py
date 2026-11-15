#!/usr/bin/env python3
"""Local, read-only EVE SSO/ESI character-data importer.

Refresh tokens are kept in the operating-system keyring. Authenticated
snapshots are written only below data/private/esi/, which is Git-ignored.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import http.server
import json
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SSO_METADATA_URL = "https://login.eveonline.com/.well-known/oauth-authorization-server"
ESI_BASE_URL = "https://esi.evetech.net/latest"
KEYRING_SERVICE = "EveOnlineIndustryLocal"
REGISTRY_PATH = Path("data/private/esi/authorized-characters.json")
DEFAULT_REDIRECT_URI = "http://127.0.0.1:8765/callback/"
DEFAULT_USER_AGENT = (
    "EveOnlineIndustryLocal/0.1 "
    "(https://github.com/JMorris0n/Eve-Online-Industry)"
)

# CCP documents both the host-name issuer and the HTTPS issuer without a trailing slash.
EVE_SSO_ISSUERS = ("https://login.eveonline.com", "login.eveonline.com")

REQUIRED_SCOPES = (
    "esi-skills.read_skills.v1",
    "esi-skills.read_skillqueue.v1",
    "esi-characters.read_blueprints.v1",
    "esi-assets.read_assets.v1",
    "esi-industry.read_character_jobs.v1",
    "esi-search.search_structures.v1",
    "esi-universe.read_structures.v1",
)


class SsoError(RuntimeError):
    """Raised when a local EVE SSO operation cannot safely continue."""


class EsiError(RuntimeError):
    """Raised when an ESI request fails."""


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def json_bytes(data: Any) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(json_bytes(data))
    temporary.replace(path)


def read_json(path: Path, default: Any = None) -> Any:
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SsoError(f"Could not read {path}: {exc}") from exc


def load_config(path: Path) -> dict[str, Any]:
    config = read_json(path)
    if not isinstance(config, dict):
        raise SsoError(
            f"Missing or invalid config: {path}. Copy tools/esi/sso-config.example.json "
            "to tools/esi/sso-config.json and enter your EVE SSO client ID."
        )
    client_id = config.get("client_id")
    if not isinstance(client_id, str) or not client_id.strip() or "YOUR_" in client_id:
        raise SsoError(f"Set a valid client_id in {path}.")
    redirect_uri = config.get("redirect_uri", DEFAULT_REDIRECT_URI)
    validate_redirect_uri(redirect_uri)
    user_agent = config.get("user_agent", DEFAULT_USER_AGENT)
    if not isinstance(user_agent, str) or not user_agent.strip():
        raise SsoError("user_agent must be a non-empty string.")
    return {
        "client_id": client_id.strip(),
        "redirect_uri": redirect_uri,
        "user_agent": user_agent.strip(),
    }


def validate_redirect_uri(uri: str) -> urllib.parse.ParseResult:
    if not isinstance(uri, str):
        raise SsoError("redirect_uri must be a string.")
    parsed = urllib.parse.urlparse(uri)
    if (
        parsed.scheme != "http"
        or parsed.hostname != "127.0.0.1"
        or parsed.port is None
        or parsed.path in {"", "/"}
        or parsed.query
        or parsed.fragment
        or parsed.username
        or parsed.password
    ):
        raise SsoError(
            "redirect_uri must be an HTTP loopback URL using 127.0.0.1, an explicit port, "
            "and a callback path, for example http://127.0.0.1:8765/callback/. "
            "Register the exact same URI in the EVE Developer Portal."
        )
    if not 1024 <= parsed.port <= 65535:
        raise SsoError("redirect_uri port must be between 1024 and 65535.")
    return parsed


def generate_pkce_pair() -> tuple[str, str]:
    """Return a high-entropy PKCE verifier and S256 challenge."""
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("ascii").rstrip("=")
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode("ascii")).digest()
    ).decode("ascii").rstrip("=")
    return verifier, challenge


def build_authorization_url(
    authorization_endpoint: str,
    client_id: str,
    redirect_uri: str,
    state: str,
    code_challenge: str,
    scopes: tuple[str, ...] = REQUIRED_SCOPES,
) -> str:
    query = urllib.parse.urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": " ".join(scopes),
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    })
    return f"{authorization_endpoint}?{query}"


def request_json(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: Any = None,
    timeout: int = 30,
) -> tuple[Any, dict[str, str]]:
    request_headers = {"Accept": "application/json"}
    if headers:
        request_headers.update(headers)
    data = None
    if body is not None:
        data = json_bytes(body)
        request_headers["Content-Type"] = "application/json"
    request = urllib.request.Request(
        url, data=data, headers=request_headers, method=method
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            payload = json.loads(raw.decode("utf-8")) if raw else None
            return payload, {
                key.lower(): value for key, value in response.headers.items()
            }
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        try:
            error = json.loads(detail)
            message = error.get("error", detail) if isinstance(error, dict) else detail
        except json.JSONDecodeError:
            message = detail
        raise SsoError(f"HTTP {exc.code} from {url}: {message}") from exc
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        raise SsoError(f"Request failed for {url}: {exc}") from exc


def get_sso_metadata() -> dict[str, Any]:
    metadata, _ = request_json(SSO_METADATA_URL)
    if not isinstance(metadata, dict):
        raise SsoError("EVE SSO metadata endpoint returned an invalid document.")
    required = ("authorization_endpoint", "token_endpoint", "jwks_uri")
    missing = [key for key in required if not isinstance(metadata.get(key), str)]
    if missing:
        raise SsoError("EVE SSO metadata is missing: " + ", ".join(missing))
    return metadata


def post_token_form(token_endpoint: str, payload: dict[str, str]) -> dict[str, Any]:
    encoded = urllib.parse.urlencode(payload).encode("utf-8")
    request = urllib.request.Request(
        token_endpoint,
        data=encoded,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            tokens = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SsoError(f"EVE SSO token request failed with HTTP {exc.code}: {detail}") from exc
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        raise SsoError(f"EVE SSO token request failed: {exc}") from exc
    if not isinstance(tokens, dict) or not tokens.get("access_token"):
        raise SsoError("EVE SSO token response did not contain an access token.")
    return tokens


def exchange_authorization_code(
    token_endpoint: str,
    client_id: str,
    code: str,
    code_verifier: str,
) -> dict[str, Any]:
    tokens = post_token_form(token_endpoint, {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "code_verifier": code_verifier,
    })
    if not tokens.get("refresh_token"):
        raise SsoError("EVE SSO did not return a refresh token.")
    return tokens


def refresh_access_token(
    token_endpoint: str,
    client_id: str,
    refresh_token: str,
) -> dict[str, Any]:
    return post_token_form(token_endpoint, {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
    })


def verify_access_token(
    token: str,
    *,
    client_id: str,
    jwks_uri: str,
) -> dict[str, Any]:
    """Validate signature, issuer, expiry, audience, and character subject."""
    try:
        import jwt
    except ImportError as exc:
        raise SsoError(
            "JWT validation requires PyJWT with crypto support. Install "
            "tools/esi/requirements-sso.txt."
        ) from exc

    try:
        signing_key = jwt.PyJWKClient(jwks_uri).get_signing_key_from_jwt(token).key
        claims = jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            issuer=EVE_SSO_ISSUERS,
            options={"verify_aud": False},
        )
    except Exception as exc:
        raise SsoError(f"EVE SSO access-token validation failed: {exc}") from exc

    audience = claims.get("aud", [])
    if isinstance(audience, str):
        audience = [audience]
    if not isinstance(audience, list) or not {"EVE Online", client_id}.issubset(set(audience)):
        raise SsoError("EVE SSO token audience does not match this application.")

    subject = claims.get("sub")
    prefix = "CHARACTER:EVE:"
    if not isinstance(subject, str) or not subject.startswith(prefix):
        raise SsoError("EVE SSO token subject is not a character identity.")
    try:
        character_id = int(subject[len(prefix):])
    except ValueError as exc:
        raise SsoError("EVE SSO token contains an invalid character ID.") from exc
    if character_id <= 0:
        raise SsoError("EVE SSO token contains an invalid character ID.")

    scopes = claims.get("scp", [])
    if isinstance(scopes, str):
        scopes = [scopes]
    if not isinstance(scopes, list) or not all(isinstance(scope, str) for scope in scopes):
        raise SsoError("EVE SSO token contains an invalid scope claim.")

    return {
        "character_id": character_id,
        "character_name": claims.get("name"),
        "scopes": sorted(set(scopes)),
        "owner_hash": claims.get("owner"),
        "expires_at": claims.get("exp"),
    }


def get_keyring():
    try:
        import keyring
    except ImportError as exc:
        raise SsoError(
            "Secure token storage requires keyring. Install tools/esi/requirements-sso.txt."
        ) from exc
    try:
        backend = keyring.get_keyring()
        if getattr(backend, "priority", 0) <= 0:
            raise SsoError(
                "No secure operating-system keyring is available. On Windows, use "
                "Windows Credential Manager. No plaintext token fallback is allowed."
            )
    except SsoError:
        raise
    except Exception as exc:
        raise SsoError(
            f"Could not initialize the operating-system credential store: {exc}"
        ) from exc
    return keyring


def store_refresh_token(character_id: int, refresh_token: str) -> None:
    get_keyring().set_password(KEYRING_SERVICE, str(character_id), refresh_token)


def get_refresh_token(character_id: int) -> str:
    token = get_keyring().get_password(KEYRING_SERVICE, str(character_id))
    if not token:
        raise SsoError(
            f"No refresh token is stored for character {character_id}. Authorize first."
        )
    return token


def delete_refresh_token(character_id: int) -> None:
    keyring = get_keyring()
    try:
        keyring.delete_password(KEYRING_SERVICE, str(character_id))
    except Exception:
        # A missing key is already the desired local state.
        pass


def load_registry() -> list[dict[str, Any]]:
    rows = read_json(REGISTRY_PATH, default=[])
    if not isinstance(rows, list):
        raise SsoError(f"Character registry is malformed: {REGISTRY_PATH}")
    return [row for row in rows if isinstance(row, dict)]


def save_registry(rows: list[dict[str, Any]]) -> None:
    unique = {
        int(row["character_id"]): row
        for row in rows if isinstance(row, dict) and "character_id" in row
    }
    write_json(REGISTRY_PATH, sorted(unique.values(), key=lambda row: row["character_id"]))


def add_authorized_character(identity: dict[str, Any]) -> None:
    rows = [
        row for row in load_registry()
        if row.get("character_id") != identity["character_id"]
    ]
    rows.append({
        "character_id": identity["character_id"],
        "character_name": identity.get("character_name"),
        "scopes": identity["scopes"],
        "authorized_at": utc_iso(),
    })
    save_registry(rows)


def callback_handler(expected_state: str, callback_path: str):
    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            result: dict[str, Any]
            if parsed.path != callback_path:
                result = {"error": "unexpected_callback_path"}
            elif params.get("state", [None])[0] != expected_state:
                result = {"error": "state_mismatch"}
            elif params.get("error"):
                result = {
                    "error": params["error"][0],
                    "error_description": params.get("error_description", [""])[0],
                }
            elif not params.get("code") or not params["code"][0]:
                result = {"error": "missing_authorization_code"}
            else:
                result = {"code": params["code"][0]}
            self.server.authorization_result = result  # type: ignore[attr-defined]

            success = "code" in result
            body = (
                "<html><body><h2>EVE authorization received.</h2>"
                "<p>Return to the local command window.</p></body></html>"
                if success else
                "<html><body><h2>EVE authorization was not completed.</h2>"
                "<p>Return to the local command window for details.</p></body></html>"
            ).encode("utf-8")
            self.send_response(200 if success else 400)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Pragma", "no-cache")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format, *args):
            # Never log callback query strings or authorization codes.
            return

    return CallbackHandler


def authorize_character(config: dict[str, Any]) -> dict[str, Any]:
    metadata = get_sso_metadata()
    verifier, challenge = generate_pkce_pair()
    state = secrets.token_urlsafe(32)
    parsed = validate_redirect_uri(config["redirect_uri"])
    server = http.server.HTTPServer(
        ("127.0.0.1", parsed.port),
        callback_handler(state, parsed.path),
    )
    server.timeout = 1
    server.authorization_result = None  # type: ignore[attr-defined]

    auth_url = build_authorization_url(
        metadata["authorization_endpoint"],
        config["client_id"],
        config["redirect_uri"],
        state,
        challenge,
    )
    print("Opening EVE SSO in your browser. Select the character to authorize.")
    print("The callback listener is bound only to 127.0.0.1.")
    if not webbrowser.open(auth_url, new=1, autoraise=True):
        print("Open this URL manually in your browser:")
        print(auth_url)

    try:
        deadline = time.monotonic() + 300
        while server.authorization_result is None and time.monotonic() < deadline:
            server.handle_request()
        result = server.authorization_result
    finally:
        server.server_close()

    if not isinstance(result, dict):
        raise SsoError("Timed out waiting for the EVE SSO callback after five minutes.")
    if result.get("error"):
        raise SsoError(
            f"EVE SSO authorization failed: {result['error']} "
            f"{result.get('error_description', '')}".strip()
        )

    tokens = exchange_authorization_code(
        metadata["token_endpoint"],
        config["client_id"],
        result["code"],
        verifier,
    )
    identity = verify_access_token(
        tokens["access_token"],
        client_id=config["client_id"],
        jwks_uri=metadata["jwks_uri"],
    )
    missing_scopes = sorted(set(REQUIRED_SCOPES) - set(identity["scopes"]))
    if missing_scopes:
        raise SsoError(
            "The token is missing required scopes: " + ", ".join(missing_scopes)
            + ". Verify the application's requested permissions and authorize again."
        )

    store_refresh_token(identity["character_id"], tokens["refresh_token"])
    add_authorized_character(identity)
    return identity


def refresh_character_token(
    character_id: int,
    config: dict[str, Any],
) -> tuple[str, dict[str, Any]]:
    metadata = get_sso_metadata()
    tokens = refresh_access_token(
        metadata["token_endpoint"],
        config["client_id"],
        get_refresh_token(character_id),
    )
    identity = verify_access_token(
        tokens["access_token"],
        client_id=config["client_id"],
        jwks_uri=metadata["jwks_uri"],
    )
    if identity["character_id"] != character_id:
        raise SsoError("The refreshed token belongs to a different character.")
    if tokens.get("refresh_token"):
        # EVE SSO native refresh tokens may rotate. Always replace the stored value.
        store_refresh_token(character_id, tokens["refresh_token"])
    return tokens["access_token"], identity


class EsiClient:
    def __init__(self, access_token: str, compatibility_date: str, user_agent: str):
        try:
            datetime.strptime(compatibility_date, "%Y-%m-%d")
        except ValueError as exc:
            raise SsoError("compatibility_date must use YYYY-MM-DD.") from exc
        self.access_token = access_token
        self.compatibility_date = compatibility_date
        self.user_agent = user_agent

    def get(
        self,
        path: str,
        *,
        params: dict[str, str] | None = None,
        authenticated: bool = True,
    ) -> tuple[Any, dict[str, str]]:
        query = urllib.parse.urlencode(params or {})
        url = f"{ESI_BASE_URL}{path}"
        if query:
            url = f"{url}?{query}"
        headers = {
            "Accept": "application/json",
            "User-Agent": self.user_agent,
            "X-Compatibility-Date": self.compatibility_date,
        }
        if authenticated:
            headers["Authorization"] = f"Bearer {self.access_token}"
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                raw = response.read()
                payload = json.loads(raw.decode("utf-8")) if raw else None
                return payload, {
                    key.lower(): value for key, value in response.headers.items()
                }
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code == 420:
                raise EsiError(
                    "ESI returned HTTP 420 error-limit. Stop requests and retry later."
                ) from exc
            if exc.code == 429:
                raise EsiError(
                    "ESI rate limited the request (HTTP 429). Retry-After: "
                    + exc.headers.get("Retry-After", "unspecified")
                ) from exc
            raise EsiError(f"ESI HTTP {exc.code} for {path}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            raise EsiError(f"ESI request failed for {path}: {exc}") from exc

    def get_all_pages(
        self,
        path: str,
        *,
        params: dict[str, str] | None = None,
    ) -> tuple[list[Any], dict[str, Any]]:
        merged_params = dict(params or {})
        merged_params["page"] = "1"
        first, first_headers = self.get(path, params=merged_params)
        if not isinstance(first, list):
            raise EsiError(f"Expected a paginated list from {path}.")
        try:
            page_count = int(first_headers.get("x-pages", "1"))
        except ValueError as exc:
            raise EsiError(f"Invalid X-Pages header from {path}.") from exc
        if page_count < 1 or page_count > 10000:
            raise EsiError(f"Unreasonable X-Pages value from {path}: {page_count}")

        combined = list(first)
        page_headers = [{"page": 1, "headers": first_headers}]
        for page in range(2, page_count + 1):
            page_params = dict(merged_params)
            page_params["page"] = str(page)
            rows, headers = self.get(path, params=page_params)
            if not isinstance(rows, list):
                raise EsiError(f"Expected a paginated list from {path}, page {page}.")
            combined.extend(rows)
            page_headers.append({"page": page, "headers": headers})

        return combined, {
            "pages": page_count,
            "record_count": len(combined),
            "page_response_headers": page_headers,
        }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sync_character(
    character_id: int,
    *,
    config: dict[str, Any],
    compatibility_date: str,
) -> Path:
    access_token, identity = refresh_character_token(character_id, config)
    missing_scopes = sorted(set(REQUIRED_SCOPES) - set(identity["scopes"]))
    if missing_scopes:
        raise SsoError("Stored grant is missing scopes: " + ", ".join(missing_scopes))

    client = EsiClient(access_token, compatibility_date, config["user_agent"])
    data: dict[str, Any] = {}
    endpoint_meta: dict[str, Any] = {}

    data["skills"], headers = client.get(f"/characters/{character_id}/skills/")
    endpoint_meta["skills"] = {
        "url": f"{ESI_BASE_URL}/characters/{character_id}/skills/",
        "headers": headers,
    }

    data["skill_queue"], headers = client.get(
        f"/characters/{character_id}/skillqueue/"
    )
    endpoint_meta["skill_queue"] = {
        "url": f"{ESI_BASE_URL}/characters/{character_id}/skillqueue/",
        "headers": headers,
    }

    for key, path, params in (
        ("blueprints", f"/characters/{character_id}/blueprints/", None),
        ("assets", f"/characters/{character_id}/assets/", None),
        (
            "industry_jobs",
            f"/characters/{character_id}/industry/jobs/",
            # Include recent completed jobs so ready-for-delivery work is not lost.
            # The importer counts active/paused/ready and ignores delivered/cancelled/reverted.
            {"include_completed": "true"},
        ),
    ):
        data[key], page_meta = client.get_all_pages(path, params=params)
        endpoint_meta[key] = {"url": f"{ESI_BASE_URL}{path}", **page_meta}

    data["public_industry_facilities"], headers = client.get(
        "/industry/facilities/", authenticated=False
    )
    endpoint_meta["public_industry_facilities"] = {
        "url": f"{ESI_BASE_URL}/industry/facilities/",
        "headers": headers,
        "authenticated": False,
    }

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output_dir = Path("data/private/esi/snapshots") / str(character_id) / timestamp
    output_dir.mkdir(parents=True, exist_ok=False)

    files = {}
    for name, payload in data.items():
        output_path = output_dir / f"{name}.json"
        write_json(output_path, payload)
        files[name] = {
            "file": output_path.name,
            "sha256": sha256_file(output_path),
            "record_count": len(payload) if isinstance(payload, list) else None,
        }

    manifest = {
        "snapshot_version": 1,
        "character_id": character_id,
        "character_name": identity.get("character_name"),
        "retrieved_at": utc_iso(),
        "compatibility_date": compatibility_date,
        "granted_scopes": identity["scopes"],
        "endpoint_metadata": endpoint_meta,
        "files": files,
        "privacy": {
            "contains_private_character_data": True,
            "must_remain_local": True,
            "contains_access_or_refresh_tokens": False,
        },
    }
    write_json(output_dir / "manifest.json", manifest)
    return output_dir


def command_authorize(args) -> int:
    identity = authorize_character(load_config(args.config))
    print(
        f"PASS: authorized {identity.get('character_name')} "
        f"({identity['character_id']})"
    )
    print(f"Granted scopes: {len(identity['scopes'])}")
    print("Refresh token stored in the operating-system credential store.")
    print("No private character snapshot has been uploaded or sent to GitHub.")
    return 0


def command_list(args) -> int:
    rows = load_registry()
    if not rows:
        print("No characters are authorized yet.")
        return 0
    for row in rows:
        print(f"{row.get('character_name')} ({row['character_id']})")
        print(f"  Authorized: {row.get('authorized_at')}")
        print(f"  Scopes: {len(row.get('scopes', []))}")
    return 0


def command_sync(args) -> int:
    config = load_config(args.config)
    registry = load_registry()
    targets = (
        [args.character_id]
        if args.character_id is not None
        else [int(row["character_id"]) for row in registry]
    )
    if not targets:
        raise SsoError("No authorized characters found. Run authorize first.")
    for character_id in targets:
        snapshot = sync_character(
            character_id,
            config=config,
            compatibility_date=args.compatibility_date,
        )
        print(f"PASS: wrote private ESI snapshot to {snapshot}")
    print("Keep snapshots under data/private/ local. Do not upload them to Dropbox or GitHub.")
    return 0


def command_forget(args) -> int:
    delete_refresh_token(args.character_id)
    rows = [
        row for row in load_registry()
        if row.get("character_id") != args.character_id
    ]
    save_registry(rows)
    print(f"Removed the local refresh token and registry entry for {args.character_id}.")
    print("This does not revoke the EVE SSO grant; revoke it separately in Authorized Applications.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("tools/esi/sso-config.json"),
        help="Private local SSO config (default: tools/esi/sso-config.json)",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    authorize = commands.add_parser("authorize", help="Authorize one character with EVE SSO")
    authorize.set_defaults(func=command_authorize)

    list_chars = commands.add_parser("list", help="List locally authorized characters")
    list_chars.set_defaults(func=command_list)

    sync = commands.add_parser("sync", help="Import one or all authorized characters")
    sync.add_argument("--character-id", type=int)
    sync.add_argument(
        "--compatibility-date",
        required=True,
        help="Reviewed ESI compatibility date (YYYY-MM-DD)",
    )
    sync.set_defaults(func=command_sync)

    forget = commands.add_parser("forget", help="Remove a local refresh token and registry entry")
    forget.add_argument("--character-id", type=int, required=True)
    forget.set_defaults(func=command_forget)

    args = parser.parse_args()
    try:
        return args.func(args)
    except (SsoError, EsiError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
