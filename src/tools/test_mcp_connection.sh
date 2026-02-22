#!/usr/bin/env bash
# Test MCP server connectivity and protocol handshake
# Usage: ./test_mcp_connection.sh [host] [port] [token]

HOST="${1:-localhost}"
PORT="${2:-${CODESIGN_MCP_PORT:-37667}}"
TOKEN="${3:-${CODESIGN_MCP_TOKEN:-}}"
BASE_URL="http://${HOST}:${PORT}"

pass=0
fail=0

check() {
  local label="$1" ok="$2"
  if [ "$ok" = "true" ]; then
    echo "  [PASS] $label"
    pass=$((pass + 1))
  else
    echo "  [FAIL] $label"
    fail=$((fail + 1))
  fi
}

# Extract a JSON string value by key (simple, no nested objects)
json_val() {
  python3 -c "import sys,json; d=json.load(sys.stdin); print($1)" 2>/dev/null <<< "$2"
}

echo "=== MCP Connection Test ==="
echo "Target: ${BASE_URL}"
echo ""

# 1. TCP reachability
echo "1. Reachability"
http_code=$(curl -s -o /dev/null -w '%{http_code}' \
  -H "Authorization: Bearer ${TOKEN}" \
  "${BASE_URL}/" 2>/dev/null || echo "000")
ok=$([ "$http_code" -ge 200 ] 2>/dev/null && [ "$http_code" -lt 500 ] 2>/dev/null && echo true || echo false)
check "HTTP response (got ${http_code})" "$ok"

# 2. MCP initialize handshake
echo "2. Protocol handshake"
init_resp=$(curl -s -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "${BASE_URL}/" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"mcp-test","version":"0.1.0"}}}' 2>/dev/null || echo "{}")

has_result=$(echo "$init_resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print('true' if 'result' in d else 'false')" 2>/dev/null || echo "false")
check "Initialize response contains result" "$has_result"

server_name=$(json_val "d['result']['serverInfo']['name']" "$init_resp" || echo "")
server_version=$(json_val "d['result']['serverInfo']['version']" "$init_resp" || echo "")
check "Server identified as '${server_name:-unknown}' v${server_version:-?}" "$([ -n "$server_name" ] && echo true || echo false)"

protocol=$(json_val "d['result']['protocolVersion']" "$init_resp" || echo "")
check "Protocol version: ${protocol:-none}" "$([ -n "$protocol" ] && echo true || echo false)"

# 3. List tools
echo "3. Tool discovery"
tools_resp=$(curl -s -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "${BASE_URL}/" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' 2>/dev/null || echo "{}")

tool_names=$(echo "$tools_resp" | python3 -c "
import sys, json
d = json.load(sys.stdin)
tools = d.get('result', {}).get('tools', [])
for t in tools:
    print(t['name'])
" 2>/dev/null || echo "")

tool_count=$(echo "$tool_names" | grep -c '.' || echo "0")
check "Tools discovered: ${tool_count}" "$([ "$tool_count" -gt 0 ] && echo true || echo false)"

if [ -n "$tool_names" ]; then
  echo "$tool_names" | while read -r t; do
    [ -n "$t" ] && echo "       - $t"
  done
fi

# Summary
echo ""
echo "=== Summary: ${pass} passed, ${fail} failed ==="
exit "$fail"
