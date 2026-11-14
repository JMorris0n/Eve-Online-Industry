"""Regression tests for local EVE SSO/ESI helper functions."""

from __future__ import annotations

import base64
import hashlib
import unittest
import urllib.parse

from sso_local import (
    DEFAULT_REDIRECT_URI,
    REQUIRED_SCOPES,
    SsoError,
    build_authorization_url,
    generate_pkce_pair,
    validate_redirect_uri,
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


if __name__ == "__main__":
    unittest.main()
