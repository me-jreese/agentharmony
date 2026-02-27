# Enceladus MCP Server Connection Test

**Date:** 2026-02-27T05:15:10Z
**Source repo:** https://github.com/NX-2021-L/enceladus
**Server path:** `tools/enceladus-mcp-server/server.py`
**Transport:** stdio

## Test Results

### Health API (`https://jreese.net/api/v1/health`)

**Status:** 200 OK

```json
{
  "dynamodb": "ok",
  "s3": "ok",
  "governance_hash": "dc656afe5ee44541cdc0e247fc5cf7448790a9519ef7a1e59f831b5763934e13",
  "checked_at": "2026-02-27T05:15:10Z"
}
```

### Tracker API (`https://jreese.net/api/v1/tracker`)

**Status:** 403 Forbidden (expected without API key)

### Governance API (`https://jreese.net/api/v1/governance`)

**Status:** 404 Not Found (expected without API key / specific path)

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

## Environment Blockers

- **PyPI blocked:** The `mcp` Python SDK (v1.26.0) cannot be installed in this sandboxed environment because PyPI (`pypi.org`) is not on the egress proxy allowlist. The stdio MCP server cannot start without this dependency.
- **boto3 blocked:** Same proxy restriction prevents `boto3` installation.
- **No AWS credentials:** AWS CLI is not configured, limiting DynamoDB/S3 direct access (HTTP API fallback works).

## Conclusion

- Backend connectivity to `jreese.net` is **confirmed working** (health endpoint returns 200 with DynamoDB and S3 both OK).
- MCP server profile has been written to `~/.claude/mcp.json`.
- Full MCP stdio server startup requires installing `mcp` and `boto3` packages, which needs PyPI access or a pre-built environment.
- To complete setup locally, run: `./tools/enceladus-mcp-server/install_profile.sh` from the enceladus repo clone.
