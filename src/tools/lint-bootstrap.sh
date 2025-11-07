#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

LOG_PREFIX="[LINT]"
declare -a SHELLCHECK_TARGETS=(
  "${ROOT_DIR}/bootstrap-session.sh"
  "${ROOT_DIR}/codex-auto.sh"
)
declare -a MARKDOWN_TARGETS=()
while IFS= read -r markdown_path; do
  MARKDOWN_TARGETS+=("$markdown_path")
done < <(
  {
    if [[ -f "${ROOT_DIR}/agents.md" ]]; then
      printf '%s\n' "${ROOT_DIR}/agents.md"
    fi
    if [[ -d "${ROOT_DIR}/agent-reference-template" ]]; then
      find "${ROOT_DIR}/agent-reference-template" -type f -name "*.md" -print
    fi
    if [[ -d "${ROOT_DIR}/projects" ]]; then
      find "${ROOT_DIR}/projects" -path "*/agent-reference/*.md" -print
    fi
  } | LC_ALL=C sort
)

ensure_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "[ERROR] Required command '$1' not found in PATH." >&2
    exit 127
  fi
}

run_shellcheck() {
  echo "[START] shellcheck (${#SHELLCHECK_TARGETS[@]} files)"
  shellcheck "${SHELLCHECK_TARGETS[@]}"
  echo "[END] shellcheck"
}

run_markdownlint() {
  echo "[START] markdownlint (${#MARKDOWN_TARGETS[@]} files)"
  if ! markdownlint "${MARKDOWN_TARGETS[@]}"; then
    echo "[ERROR] markdownlint reported issues; see output above." >&2
    return 1
  fi
  echo "[END] markdownlint"
}

main() {
  ensure_command shellcheck
  ensure_command markdownlint

  run_shellcheck
  run_markdownlint
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi
