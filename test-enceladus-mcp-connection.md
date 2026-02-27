# Enceladus MCP Server Connection Test

**Date:** 2026-02-27T05:32:15Z
**Source repo:** https://github.com/NX-2021-L/enceladus
**Server path:** `tools/enceladus-mcp-server/server.py`
**Transport:** stdio (local), streamable_http (Lambda)

## Full API Connectivity Test Results

All 7 backend API endpoints are **reachable** from this environment.

| Endpoint | URL | HTTP Status | Result |
|---|---|---|---|
| Health API | `/api/v1/health` | 200 OK | **PASS** |
| Tracker API | `/api/v1/tracker` | 403 Forbidden | **PASS** (auth required) |
| Governance API | `/api/v1/governance/hash` | 401 Unauthorized | **PASS** (auth required) |
| Coordination API | `/api/v1/coordination/capabilities` | 200 OK | **PASS** |
| Projects API | `/api/v1/coordination/projects` | 401 Unauthorized | **PASS** (auth required) |
| Documents API | `/api/v1/documents` | 401 Unauthorized | **PASS** (auth required) |
| Deploy API | `/api/v1/deploy/pending` | 404 Not Found | **PASS** (reachable) |

### Health API Response

```json
{
  "dynamodb": "ok",
  "s3": "ok",
  "governance_hash": "dc656afe5ee44541cdc0e247fc5cf7448790a9519ef7a1e59f831b5763934e13",
  "checked_at": "2026-02-27T05:32:16Z"
}
```

### Coordination Capabilities Response

```json
{
  "success": true,
  "capabilities": {
    "contract_version": "0.3.0",
    "execution_modes": [
      {"mode": "preflight", "supported": true},
      ...
    ]
  }
}
```

## MCP Server Configuration

Written to `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "enceladus": {
      "command": "/usr/bin/python3",
      "args": ["/tmp/enceladus/tools/enceladus-mcp-server/server.py"],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "ENCELADUS_WORKSPACE_ROOT": "/tmp/enceladus",
        "ENCELADUS_REGION": "us-west-2",
        "ENCELADUS_TRACKER_TABLE": "devops-project-tracker",
        "ENCELADUS_PROJECTS_TABLE": "projects",
        "ENCELADUS_DOCUMENTS_TABLE": "documents",
        "ENCELADUS_S3_BUCKET": "jreese-net",
        "ENCELADUS_S3_GOVERNANCE_PREFIX": "governance/live",
        "ENCELADUS_S3_GOVERNANCE_HISTORY_PREFIX": "governance/history",
        "ENCELADUS_TRACKER_API_BASE": "https://jreese.net/api/v1/tracker",
        "ENCELADUS_GOVERNANCE_API_BASE": "https://jreese.net/api/v1/governance",
        "ENCELADUS_PROJECTS_API_BASE": "https://jreese.net/api/v1/coordination/projects",
        "ENCELADUS_HEALTH_API_URL": "https://jreese.net/api/v1/health"
      }
    }
  }
}
```

## Test Scripts

- **`test_enceladus_api_connectivity.py`** — Stdlib-only test that validates HTTP reachability of all 7 API endpoints. No external deps required.
- **`test_enceladus_mcp_smoke.py`** — Full MCP stdio smoke test (requires `pip install mcp boto3 PyYAML`). Starts the server via stdio, initializes session, calls `connection_health` and `governance_hash`.

## Environment Blockers

- **PyPI blocked:** `pypi.org` and `files.pythonhosted.org` are not on the egress proxy allowlist. The `mcp` Python SDK (v1.26.0), `boto3`, and all transitive dependencies cannot be installed. Attempted: pip, uv, git+https, Artifactory mirror — all fail at the PyPI download step.
- **No AWS credentials:** AWS CLI is not configured, so DynamoDB/S3 direct access is unavailable (HTTP API fallback works).

## How to Run the Full MCP Smoke Test

In an environment with PyPI access:

```bash
# 1. Clone the repo
git clone https://github.com/NX-2021-L/enceladus.git /tmp/enceladus

# 2. Install dependencies
pip install mcp boto3 PyYAML

# 3. Run the full smoke test
ENCELADUS_SERVER_PY=/tmp/enceladus/tools/enceladus-mcp-server/server.py \
  python3 test_enceladus_mcp_smoke.py

# Or use the official installer:
cd /tmp/enceladus && ./tools/enceladus-mcp-server/install_profile.sh
```

## Conclusion

- **Network connectivity:** All 7 Enceladus backend APIs at `jreese.net` are reachable. Health endpoint confirms DynamoDB and S3 are both healthy. Coordination capabilities endpoint returns contract v0.3.0.
- **MCP config:** Profile written to `~/.claude/mcp.json` with correct server command and env vars.
- **Stdio server:** Cannot start in this sandbox (missing `mcp` SDK). Ready-to-run smoke test script provided for environments with PyPI access.
