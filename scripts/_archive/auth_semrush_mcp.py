#!/usr/bin/env python3
"""
auth_semrush_mcp.py — one-time interactive Semrush MCP OAuth bootstrap.

Run this ONCE on a workstation with a browser. It walks the PKCE flow,
captures the refresh token, and prints a `doppler secrets set` command you
copy-paste to persist the token in `pleasurai/dev`.

After this runs, the headless Paperclip pipeline can mint short-lived access
tokens via `refresh_semrush_mcp_token.py` without ever needing interactive
consent again.

Usage:
    python3 scripts/auth_semrush_mcp.py
        # opens browser, listens on localhost:56340, exchanges code for tokens

    python3 scripts/auth_semrush_mcp.py --port 56341
        # use a different callback port if 56340 is busy

The script is intentionally stdlib-only so it runs anywhere Python 3.9+ is
installed (no `pip install` step Neo has to remember).
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import http.server
import json
import secrets
import socketserver
import sys
import threading
import urllib.parse
import urllib.request
import webbrowser

# Discovered from https://api.semrush.com/apis/v4/auth/.well-known/oauth-authorization-server
AUTH_ENDPOINT = "https://api.semrush.com/apis/v4/auth/v0/oauth2/auth"
TOKEN_ENDPOINT = "https://api.semrush.com/apis/v4-raw/auth/v1/oauth2/access_token"

# Default Power-1 MCP client (the one Claude Code's MCP HTTP client uses for the
# Semrush MCP). If Semrush ever rotates this, update here.
CLIENT_ID = "a98b9f89-5a0c-46d7-805d-3f07bdb93c4d"
RESOURCE = "https://mcp.semrush.com/v1/mcp"
SCOPE = "mcp.access offline_access"


def make_pkce() -> tuple[str, str]:
    """Return (code_verifier, code_challenge) per RFC 7636 S256."""
    verifier = secrets.token_urlsafe(64)[:128]
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).decode().rstrip("=")
    return verifier, challenge


class _CallbackHandler(http.server.BaseHTTPRequestHandler):
    captured: dict[str, str] = {}

    def do_GET(self):  # noqa: N802 (BaseHTTPRequestHandler API)
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/callback":
            self.send_response(404)
            self.end_headers()
            return
        params = urllib.parse.parse_qs(parsed.query)
        type(self).captured["code"] = params.get("code", [""])[0]
        type(self).captured["state"] = params.get("state", [""])[0]
        type(self).captured["error"] = params.get("error", [""])[0]
        type(self).captured["error_description"] = params.get("error_description", [""])[0]
        body = (
            "<html><body><h2>Semrush MCP authorization received.</h2>"
            "<p>You can close this tab and return to the terminal.</p></body></html>"
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # Silence default access-log noise so the terminal output is clean
    def log_message(self, format, *args):  # noqa: A002
        pass


def listen_for_callback(port: int) -> dict[str, str]:
    """Block until the OAuth callback hits localhost:{port}/callback."""
    captured: dict[str, str] = {}
    _CallbackHandler.captured = captured

    with socketserver.TCPServer(("127.0.0.1", port), _CallbackHandler) as httpd:
        httpd.timeout = 300  # 5 minutes is plenty for a human click
        # Serve until we got a code (or error)
        while not captured.get("code") and not captured.get("error"):
            httpd.handle_request()
    return captured


def exchange_code_for_tokens(code: str, code_verifier: str, redirect_uri: str) -> dict:
    body = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "code_verifier": code_verifier,
        "client_id": CLIENT_ID,
        "redirect_uri": redirect_uri,
    }).encode()
    req = urllib.request.Request(
        TOKEN_ENDPOINT,
        data=body,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"\nToken exchange failed: HTTP {e.code}\n")
        sys.stderr.write(e.read().decode("utf-8", errors="ignore") + "\n")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--port", type=int, default=56340, help="Local callback port (default: 56340)")
    parser.add_argument("--no-browser", action="store_true", help="Don't auto-open browser; print URL instead")
    parser.add_argument(
        "--write-doppler",
        action="store_true",
        help="Run `doppler secrets set` automatically (requires doppler CLI authenticated to pleasurai/dev)",
    )
    args = parser.parse_args()

    redirect_uri = f"http://localhost:{args.port}/callback"
    code_verifier, code_challenge = make_pkce()
    state = secrets.token_urlsafe(24)

    auth_url = AUTH_ENDPOINT + "?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": redirect_uri,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": state,
        "scope": SCOPE,
        "resource": RESOURCE,
    })

    print()
    print("===============================================================")
    print(" Semrush MCP — one-time OAuth bootstrap")
    print("===============================================================")
    print()
    print(f"Listening for callback on {redirect_uri}")
    print()

    server_thread = threading.Thread(
        target=lambda: listen_for_callback(args.port),
        daemon=True,
    )
    server_thread.start()

    if args.no_browser:
        print("Open this URL in your browser, sign in to Semrush, and approve:")
        print()
        print(f"   {auth_url}")
        print()
    else:
        print("Opening browser… If nothing opens, paste this URL manually:")
        print()
        print(f"   {auth_url}")
        print()
        webbrowser.open(auth_url)

    server_thread.join(timeout=600)  # max 10 minutes
    captured = _CallbackHandler.captured

    if captured.get("error"):
        print(f"OAuth error: {captured['error']} - {captured.get('error_description','')}")
        sys.exit(1)
    if captured.get("state") != state:
        print(f"State mismatch — expected {state!r}, got {captured.get('state')!r}. Aborting.")
        sys.exit(1)
    if not captured.get("code"):
        print("No authorization code received — did the browser redirect actually hit /callback?")
        sys.exit(1)

    print("Authorization code received. Exchanging for tokens…")
    tokens = exchange_code_for_tokens(captured["code"], code_verifier, redirect_uri)

    refresh = tokens.get("refresh_token")
    access = tokens.get("access_token")
    expires = tokens.get("expires_in")
    rscope = tokens.get("scope")

    if not refresh:
        print()
        print("WARNING: token endpoint did not return a refresh_token.")
        print("The pipeline cannot be made fully autonomous without one.")
        print("Token response:")
        print(json.dumps(tokens, indent=2))
        sys.exit(2)

    print()
    print("===============================================================")
    print(" SUCCESS")
    print("===============================================================")
    print(f"  access_token  : (length {len(access or '')}, expires in {expires}s)")
    print(f"  refresh_token : (length {len(refresh)})")
    print(f"  scope         : {rscope}")
    print()
    print("Persist the refresh token in Doppler `pleasurai/dev` so the headless")
    print("pipeline can mint access tokens without interactive consent:")
    print()
    print(f"  doppler secrets set SEMRUSH_MCP_REFRESH_TOKEN='{refresh}' --project pleasurai --config dev")
    print()

    if args.write_doppler:
        import shutil
        import subprocess
        if not shutil.which("doppler"):
            print("(--write-doppler requested but `doppler` CLI is not on PATH; skipping)")
            return
        try:
            subprocess.run(
                ["doppler", "secrets", "set", f"SEMRUSH_MCP_REFRESH_TOKEN={refresh}",
                 "--project", "pleasurai", "--config", "dev"],
                check=True,
            )
            print("Refresh token written to Doppler pleasurai/dev as SEMRUSH_MCP_REFRESH_TOKEN.")
        except subprocess.CalledProcessError as e:
            print(f"doppler write failed: {e}")


if __name__ == "__main__":
    main()
