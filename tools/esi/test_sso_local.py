"""Regression tests for local EVE SSO/ESI helper functions."""

from __future__ import annotations

import base64
import sys
import types
from unittest.mock import patch
import hashlib
import unittest
import urllib.parse

from sso_local import (
    DEFAULT_REDIRECT_URI,
    EVE_SSO_ISSUERS,
    REQUIRED_SCOPES,
    SsoError,
    build_authorization_url,
    generate_pkce_pair,
    validate_redirect_uri,
    verify_access_token,
)


class SsoLocalTests(unittest.TestCase):
    def test_pkce_pair_uses_urlsafe_unpadded_s256_values(self):
        verifier, challenge = generate_pkce_pair()
        self.assertEqual(len(verifier), 43)
        self.assertEqual(len(challenge), 43)
        self.assertNotIn("=", verifier)
        self.assertNotIn("=", challenge)
        expected = base64.urlsafe_b64encode(
            hashlib.sha256(verifier.encode("ascii")).digest()
        ).decode("ascii").rstrip("=")
        self.assertEqual(challenge, expected)

    def test_authorization_url_requests_only_minimum_scopes(self):
        url = build_authorization_url(
            "https://login.eveonline.com/v2/oauth/authorize/",
            "client-123",
            DEFAULT_REDIRECT_URI,
            "state-random",
            "challenge-value",
        )
        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed.query)
        self.assertEqual(query["client_id"], ["client-123"])
        self.assertEqual(query["redirect_uri"], [DEFAULT_REDIRECT_URI])
        self.assertEqual(query["state"], ["state-random"])
        self.assertEqual(query["code_challenge"], ["challenge-value"])
        self.assertEqual(query["code_challenge_method"], ["S256"])
        self.assertEqual(set(query["scope"][0].split()), set(REQUIRED_SCOPES))
        self.assertEqual(query["response_type"], ["code"])

    def test_accepts_ipv4_loopback_callback(self):
        parsed = validate_redirect_uri(DEFAULT_REDIRECT_URI)
        self.assertEqual(parsed.hostname, "127.0.0.1")
        self.assertEqual(parsed.port, 8765)
        self.assertEqual(parsed.path, "/callback/")

    def test_rejects_non_loopback_or_ambiguous_callback_uri(self):
        invalid = (
            "https://example.com/callback/",
            "http://example.com:8765/callback/",
            "http://localhost:8765/callback/",
            "http://127.0.0.1/callback/",
            "http://127.0.0.1:8765/",
            "http://127.0.0.1:8765/callback/?next=https://evil.example",
            "http://user@127.0.0.1:8765/callback/",
        )
        for uri in invalid:
            with self.subTest(uri=uri):
                with self.assertRaises(SsoError):
                    validate_redirect_uri(uri)


    def _fake_jwt_module(self, issuer_value):
        class FakePyJWKClient:
            def __init__(self, jwks_uri):
                self.jwks_uri = jwks_uri

            def get_signing_key_from_jwt(self, token):
                return types.SimpleNamespace(key="test-public-key")

        def decode(token, key, algorithms, issuer, options):
            if issuer_value not in issuer:
                raise ValueError("Invalid issuer")
            return {
                "iss": issuer_value,
                "aud": ["client-123", "EVE Online"],
                "sub": "CHARACTER:EVE:123456",
                "name": "Test Character",
                "scp": list(REQUIRED_SCOPES),
                "owner": "test-owner-hash",
                "exp": 2000000000,
            }

        return types.SimpleNamespace(PyJWKClient=FakePyJWKClient, decode=decode)

    def test_accepts_both_ccp_documented_issuer_values(self):
        self.assertEqual(
            EVE_SSO_ISSUERS,
            ("https://login.eveonline.com", "login.eveonline.com"),
        )
        for issuer in EVE_SSO_ISSUERS:
            with self.subTest(issuer=issuer):
                fake_jwt = self._fake_jwt_module(issuer)
                with patch.dict(sys.modules, {"jwt": fake_jwt}):
                    identity = verify_access_token(
                        "test.jwt.token",
                        client_id="client-123",
                        jwks_uri="https://login.eveonline.com/oauth/jwks",
                    )
                self.assertEqual(identity["character_id"], 123456)
                self.assertEqual(identity["character_name"], "Test Character")
                self.assertEqual(set(identity["scopes"]), set(REQUIRED_SCOPES))

    def test_rejects_issuer_with_undocumented_trailing_slash(self):
        fake_jwt = self._fake_jwt_module("https://login.eveonline.com/")
        with patch.dict(sys.modules, {"jwt": fake_jwt}):
            with self.assertRaisesRegex(SsoError, "Invalid issuer"):
                verify_access_token(
                    "test.jwt.token",
                    client_id="client-123",
                    jwks_uri="https://login.eveonline.com/oauth/jwks",
                )


if __name__ == "__main__":
    unittest.main()
