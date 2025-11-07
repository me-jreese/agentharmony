#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
usage: codex-auto.sh [--init-context|--help] <project> [codex-args...]

Bootstrap a Codex session for <project>, exporting environment variables,
streaming governance context, and launching the Codex CLI. When --init-context
is supplied the script only streams the scoped context files and exits.
USAGE
}

log_start() {
  printf '[START] %s\n' "$*"
}

log_end() {
  printf '[END] %s\n' "$*"
}

log_info() {
  printf '[INFO] %s\n' "$*"
}

log_error() {
  printf '[ERROR] %s\n' "$*" >&2
}

MODE="run"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --init-context)
      MODE="context"
      shift
      break
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    *)
      break
      ;;
  esac
done

if [[ $# -lt 1 ]]; then
  log_error "Project argument missing."
  usage >&2
  exit 1
fi

PROJECT_NAME="$1"
shift

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOTSTRAP_SCRIPT="${BOOTSTRAP_SCRIPT:-${SCRIPT_DIR}/bootstrap-session.sh}"
CODEX_BIN="${CODEX_BIN:-codex}"

if [[ ! -x "${BOOTSTRAP_SCRIPT}" ]]; then
  log_error "bootstrap script not found or not executable: ${BOOTSTRAP_SCRIPT}"
  exit 1
fi

export PROJECT="${PROJECT_NAME}"

case "${MODE}" in
  context)
    log_start "codex-auto init-context (project=${PROJECT_NAME})"
    "${BOOTSTRAP_SCRIPT}" --context-only
    log_end "codex-auto init-context (project=${PROJECT_NAME})"
    ;;
  run)
    log_start "codex-auto bootstrap (project=${PROJECT_NAME})"
    "${BOOTSTRAP_SCRIPT}"
    log_end "codex-auto bootstrap (project=${PROJECT_NAME})"
    log_info "Handing off to codex CLI (${CODEX_BIN}) for project=${PROJECT_NAME}"
    exec env PROJECT="${PROJECT_NAME}" "${CODEX_BIN}" "${PROJECT_NAME}" "$@"
    ;;
  *)
    log_error "Unknown codex-auto mode: ${MODE}"
    exit 1
    ;;
esac
