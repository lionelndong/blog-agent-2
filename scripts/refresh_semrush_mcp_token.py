#!/usr/bin/env python3
"""
refresh_semrush_mcp_token.py — headless Semrush MCP access-token minter.

Reads `SEMRUSH_MCP_REFRESH_TOKEN` (from Doppler) and exchanges it for a fresh
short-lived `access_token`. Prints the access token to stdout (no trailing
newline) so callers can:

    export SEMRUSH_MCP_ACCESS_TOKEN=$(python3 scripts/refresh_semrush_mcp_token.py)
    claude --print …

…and the access token will reach Claude Code's MCP HTTP client via the
`Authorization: Bearer ${SEMRUSH_MCP_ACCESS_TOKEN}` header in `.mcp.json`.

Exits non-zero with a stderr message if no refresh token is available or the
token-endpoint call fails.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

TOKEN_ENDPOINT = "https://api.semrush.com/apis/v4-raw/auth/v1/oauth2/access_token"
CLIENT_ID = "a98b9f89-5a0c-46d7-805d-3f07bdb93c4d"


def mint_access_token(refresh_token: str, timeout: int = 30) -> dict:
    body = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
    }).encode()
    req = urllib.request.Request(
        TOKEN_ENDPOINT,
        data=body,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"Semrush token endpoint returned HTTP {e.code}\n")
        sys.stderr.write(e.read().decode("utf-8", errors="ignore") + "\n")
        sys.exit(2)
    except Exception as e:
        sys.stderr.write(f"Semrush token endpoint call failed: {e}\n")
        sys.exit(2)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--print-json",
        action="store_true",
        help="Print the full JSON token response (default: print only access_token)",
    )
    parser.add_argument(
        "--rotate",
        action="store_true",
        help="If the response contains a new refresh_token, write it back to Doppler.",
    )
    args = parser.parse_args()

    refresh = os.environ.get("SEMRUSH_MCP_REFRESH_TOKEN")
    if not refresh:
        sys.stderr.write(
            "SEMRUSH_MCP_REFRESH_TOKEN is not set. Run scripts/auth_semrush_mcp.py once "
            "on a workstation with a browser, then `doppler secrets set "
            "SEMRUSH_MCP_REFRESH_TOKEN=...`.\n"
        )
        sys.exit(1)

    tokens = mint_access_token(refresh)
    access = tokens.get("access_token")
    if not access:
        sys.stderr.write("Token endpoint succeeded but returned no access_token.\n")
        sys.stderr.write(json.dumps(tokens, indent=2) + "\n")
        sys.exit(2)

    new_refresh = tokens.get("refresh_token")
    if args.rotate and new_refresh and new_refresh != refresh:
        # Some IdPs rotate refresh tokens. Write the new one back to Doppler.
        import shutil
        import subprocess
        if shutil.which("doppler"):
            try:
                subprocess.run(
                    ["doppler", "secrets", "set", f"SEMRUSH_MCP_REFRESH_TOKEN={new_refresh}",
                     "--project", "pleasurai", "--config", "dev"],
                    check=True,
                    stdout=subprocess.DEVNULL,
                )
                sys.stderr.write("Rotated SEMRUSH_MCP_REFRESH_TOKEN in Doppler.\n")
            except subprocess.CalledProcessError as e:
                sys.stderr.write(f"Refresh-token rotation failed: {e}\n")

    if args.print_json:
        sys.stdout.write(json.dumps(tokens))
    else:
        sys.stdout.write(access)


if __name__ == "__main__":
    main()
