#!/usr/bin/env python3
"""Test connectivity to all Enceladus backend APIs used by the MCP server.

This script validates network reachability and basic HTTP response behavior
for every API endpoint that the enceladus-mcp-server talks to. It does NOT
require the `mcp` Python SDK — it uses only stdlib.

Usage:
    python3 test_enceladus_api_connectivity.py

Environment variables (all optional):
    ENCELADUS_HEALTH_API_URL          (default: https://jreese.net/api/v1/health)
    ENCELADUS_TRACKER_API_BASE        (default: https://jreese.net/api/v1/tracker)
    ENCELADUS_GOVERNANCE_API_BASE     (default: https://jreese.net/api/v1/governance)
    ENCELADUS_COORDINATION_API_BASE   (default: https://jreese.net/api/v1/coordination)
    ENCELADUS_PROJECTS_API_BASE       (default: https://jreese.net/api/v1/coordination/projects)
    ENCELADUS_DOCUMENT_API_BASE       (default: https://jreese.net/api/v1/documents)
    ENCELADUS_DEPLOY_API_BASE         (default: https://jreese.net/api/v1/deploy)
"""

from __future__ import annotations

import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

HEALTH_API_URL = os.environ.get(
    "ENCELADUS_HEALTH_API_URL", "https://jreese.net/api/v1/health"
)
TRACKER_API_BASE = os.environ.get(
    "ENCELADUS_TRACKER_API_BASE", "https://jreese.net/api/v1/tracker"
)
GOVERNANCE_API_BASE = os.environ.get(
    "ENCELADUS_GOVERNANCE_API_BASE", "https://jreese.net/api/v1/governance"
)
COORDINATION_API_BASE = os.environ.get(
    "ENCELADUS_COORDINATION_API_BASE", "https://jreese.net/api/v1/coordination"
)
PROJECTS_API_BASE = os.environ.get(
    "ENCELADUS_PROJECTS_API_BASE", "https://jreese.net/api/v1/coordination/projects"
)
DOCUMENT_API_BASE = os.environ.get(
    "ENCELADUS_DOCUMENT_API_BASE", "https://jreese.net/api/v1/documents"
)
DEPLOY_API_BASE = os.environ.get(
    "ENCELADUS_DEPLOY_API_BASE", "https://jreese.net/api/v1/deploy"
)

USER_AGENT = "enceladus-mcp-connectivity-test/1.0"
SSL_CTX = ssl.create_default_context()


def _request(url: str, method: str = "GET") -> dict:
    """Make an HTTP request and return a structured result."""
    req = urllib.request.Request(url, method=method)
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", USER_AGENT)
    try:
        with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as resp:
            body = resp.read().decode("utf-8")
            return {
                "status": resp.status,
                "ok": True,
                "body": body[:2000],
                "content_type": resp.headers.get("Content-Type", ""),
            }
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8")[:500]
        except Exception:
            pass
        return {
            "status": e.code,
            "ok": False,
            "reason": e.reason,
            "body": body,
        }
    except Exception as e:
        return {
            "status": 0,
            "ok": False,
            "reason": f"{type(e).__name__}: {e}",
            "body": "",
        }


def main() -> int:
    print(f"Enceladus MCP Server — API Connectivity Test")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print(f"{'=' * 60}")

    tests = [
        ("Health API", HEALTH_API_URL, 200),
        ("Tracker API", TRACKER_API_BASE, None),
        ("Governance API", f"{GOVERNANCE_API_BASE}/hash", None),
        ("Coordination API", f"{COORDINATION_API_BASE}/capabilities", None),
        ("Projects API", PROJECTS_API_BASE, None),
        ("Documents API", DOCUMENT_API_BASE, None),
        ("Deploy API", f"{DEPLOY_API_BASE}/pending", None),
    ]

    results = []
    for name, url, expected_status in tests:
        print(f"\n--- {name} ---")
        print(f"  URL: {url}")
        result = _request(url)
        status = result["status"]
        ok = result["ok"]

        if expected_status is not None:
            passed = status == expected_status
        else:
            # For authenticated endpoints, 401/403 means reachable but needs auth
            # 404 may mean no default route. All prove connectivity.
            passed = status > 0  # Any HTTP response = network OK

        status_label = "PASS" if passed else "FAIL"
        print(f"  Status: {status}")
        if ok:
            try:
                parsed = json.loads(result["body"])
                print(f"  Response: {json.dumps(parsed, indent=4)[:500]}")
            except (json.JSONDecodeError, KeyError):
                print(f"  Response: {result['body'][:200]}")
        else:
            print(f"  Reason: {result.get('reason', 'unknown')}")
            if result.get("body"):
                body = result["body"]
                # Skip HTML error pages
                if not body.strip().startswith("<!DOCTYPE"):
                    print(f"  Body: {body[:200]}")

        print(f"  Result: [{status_label}]")
        results.append((name, status, passed))

    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    all_passed = True
    for name, status, passed in results:
        icon = "PASS" if passed else "FAIL"
        print(f"  [{icon}] {name} (HTTP {status})")
        if not passed:
            all_passed = False

    if all_passed:
        print(f"\nAll {len(results)} endpoints reachable.")
    else:
        failed = sum(1 for _, _, p in results if not p)
        print(f"\n{failed}/{len(results)} endpoints unreachable.")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
