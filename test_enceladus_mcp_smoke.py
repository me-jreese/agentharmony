#!/usr/bin/env python3
"""Full MCP stdio smoke test for the Enceladus MCP server.

Requires: pip install mcp boto3 PyYAML

This script starts the enceladus MCP server as a subprocess via stdio transport,
initializes an MCP session, and calls `connection_health` + `governance_hash`
(same as install_profile.sh's smoke test).

Usage:
    # From the enceladus repo root:
    python3 test_enceladus_mcp_smoke.py

    # Or with explicit path:
    ENCELADUS_SERVER_PY=/path/to/server.py python3 test_enceladus_mcp_smoke.py

Environment variables:
    ENCELADUS_SERVER_PY               Path to server.py (auto-detected if not set)
    ENCELADUS_WORKSPACE_ROOT          Workspace root (auto-detected if not set)
    ENCELADUS_HEALTH_API_URL          (default: https://jreese.net/api/v1/health)
    ENCELADUS_TRACKER_API_BASE        (default: https://jreese.net/api/v1/tracker)
    ENCELADUS_GOVERNANCE_API_BASE     (default: https://jreese.net/api/v1/governance)
    ENCELADUS_PROJECTS_API_BASE       (default: https://jreese.net/api/v1/coordination/projects)
"""

from __future__ import annotations

import json
import os
import sys

# Verify dependencies before proceeding
try:
    import anyio
    from mcp.client.session import ClientSession
    from mcp.client.stdio import StdioServerParameters, stdio_client
except ImportError as e:
    print(f"[ERROR] Missing dependency: {e}")
    print("[ERROR] Install with: pip install mcp boto3 PyYAML")
    sys.exit(1)


def _find_server_py() -> str:
    """Auto-detect server.py location."""
    explicit = os.environ.get("ENCELADUS_SERVER_PY", "").strip()
    if explicit and os.path.isfile(explicit):
        return explicit

    candidates = [
        # Relative to this script (if placed alongside server.py)
        os.path.join(os.path.dirname(__file__), "server.py"),
        # Common clone locations
        "/tmp/enceladus/tools/enceladus-mcp-server/server.py",
        os.path.expanduser("~/enceladus/tools/enceladus-mcp-server/server.py"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path

    print("[ERROR] Cannot find server.py. Set ENCELADUS_SERVER_PY env var.")
    sys.exit(1)


def _find_workspace_root(server_py: str) -> str:
    """Auto-detect workspace root from server.py path."""
    explicit = os.environ.get("ENCELADUS_WORKSPACE_ROOT", "").strip()
    if explicit:
        return explicit
    # server.py is at tools/enceladus-mcp-server/server.py
    return os.path.normpath(os.path.join(os.path.dirname(server_py), "..", ".."))


async def main() -> None:
    server_py = _find_server_py()
    workspace_root = _find_workspace_root(server_py)
    python_bin = sys.executable

    print(f"[INFO] Server: {server_py}")
    print(f"[INFO] Workspace: {workspace_root}")
    print(f"[INFO] Python: {python_bin}")

    server_env = {
        "PYTHONUNBUFFERED": "1",
        "ENCELADUS_WORKSPACE_ROOT": workspace_root,
        "ENCELADUS_REGION": "us-west-2",
        "ENCELADUS_TRACKER_TABLE": "devops-project-tracker",
        "ENCELADUS_PROJECTS_TABLE": "projects",
        "ENCELADUS_DOCUMENTS_TABLE": "documents",
        "ENCELADUS_S3_BUCKET": "jreese-net",
        "ENCELADUS_S3_GOVERNANCE_PREFIX": "governance/live",
        "ENCELADUS_S3_GOVERNANCE_HISTORY_PREFIX": "governance/history",
        "ENCELADUS_TRACKER_API_BASE": os.environ.get(
            "ENCELADUS_TRACKER_API_BASE", "https://jreese.net/api/v1/tracker"
        ),
        "ENCELADUS_GOVERNANCE_API_BASE": os.environ.get(
            "ENCELADUS_GOVERNANCE_API_BASE", "https://jreese.net/api/v1/governance"
        ),
        "ENCELADUS_PROJECTS_API_BASE": os.environ.get(
            "ENCELADUS_PROJECTS_API_BASE",
            "https://jreese.net/api/v1/coordination/projects",
        ),
        "ENCELADUS_HEALTH_API_URL": os.environ.get(
            "ENCELADUS_HEALTH_API_URL", "https://jreese.net/api/v1/health"
        ),
    }

    # Forward API keys if set
    for key in (
        "ENCELADUS_COORDINATION_INTERNAL_API_KEY",
        "ENCELADUS_DOCUMENT_API_INTERNAL_API_KEY",
        "ENCELADUS_DEPLOY_API_INTERNAL_API_KEY",
        "ENCELADUS_TRACKER_API_INTERNAL_API_KEY",
        "ENCELADUS_GOVERNANCE_API_INTERNAL_API_KEY",
        "ENCELADUS_PROJECTS_API_INTERNAL_API_KEY",
    ):
        value = os.environ.get(key, "").strip()
        if value:
            server_env[key] = value

    aws_profile = os.environ.get("AWS_PROFILE", "").strip()
    if aws_profile:
        server_env["AWS_PROFILE"] = aws_profile

    params = StdioServerParameters(
        command=python_bin,
        args=[server_py],
        env=server_env,
    )

    print("[INFO] Starting MCP server via stdio...")

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("[OK] MCP session initialized")

            # Test 1: connection_health
            print("[INFO] Calling connection_health...")
            health_result = await session.call_tool("connection_health", {})
            health_text = health_result.content[0].text
            health_data = json.loads(health_text)
            print(f"[OK] connection_health response:")
            print(f"     DynamoDB: {health_data.get('dynamodb', 'unknown')}")
            print(f"     S3: {health_data.get('s3', 'unknown')}")
            print(f"     Governance hash: {health_data.get('governance_hash', 'unknown')[:16]}...")
            print(f"     Server version: {health_data.get('server_version', 'unknown')}")

            # Test 2: governance_hash
            print("[INFO] Calling governance_hash...")
            gov_result = await session.call_tool("governance_hash", {})
            gov_text = gov_result.content[0].text
            gov_data = json.loads(gov_text)
            print(f"[OK] governance_hash: {gov_data.get('governance_hash', gov_text)[:16]}...")

    print("[SUCCESS] MCP stdio smoke test passed")


if __name__ == "__main__":
    anyio.run(main)
