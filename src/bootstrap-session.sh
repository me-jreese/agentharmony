#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Allow callers to override workspace layout; defaults assume this script lives inside
# the AgentHarmony starter kit.
PROJECTS_DIR="${PROJECTS_DIR:-${ROOT_DIR}/projects}"
GLOBAL_AGENT_FILE="${GLOBAL_AGENT_FILE:-${ROOT_DIR}/agents.md}"
AGENTS_DIR="${AGENTS_DIR:-${ROOT_DIR}/agents}"
TEMPLATE_DIR="${TEMPLATE_DIR:-${ROOT_DIR}/agent-reference-template}"
PROJECT_AGENT_SUBDIR="${PROJECT_AGENT_SUBDIR:-agent-reference}"

usage() {
  cat <<'USAGE'
usage: bootstrap-session.sh [--env-only|--context-only]

Initialises a Codex session by exporting project metadata and, unless disabled,
streaming governance context files into stdout for the active PROJECT.

Options:
  --env-only        Export environment variables without streaming context files.
  --context-only    Stream context files without re-running env bootstrap.
  -h, --help        Show this message and exit.
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

log_warning() {
  printf '[WARNING] %s\n' "$*" >&2
}

log_error() {
  printf '[ERROR] %s\n' "$*" >&2
}

log_skip() {
  printf '[SKIP] %s\n' "$*"
}

DO_ENV=1
DO_CONTEXT=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env-only)
      DO_CONTEXT=0
      shift
      ;;
    --context-only)
      DO_ENV=0
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      log_error "Unknown option '$1'"
      usage >&2
      exit 1
      ;;
  esac
done

PROJECT_NAME="${PROJECT:-}"

if [[ -z "${PROJECT_NAME}" ]]; then
  log_error "PROJECT environment variable is not set."
  exit 1
fi

export PROJECT="${PROJECT_NAME}"

run_env_bootstrap() {
  log_start "Env bootstrap"
  local project_metadata_script="${ROOT_DIR}/tools/project_metadata.py"

  if [[ -x "${project_metadata_script}" ]]; then
    PROJECT_PREFIX="$("${project_metadata_script}" "${PROJECT_NAME}" prefix 2>/dev/null || true)"
    if [[ -n "${PROJECT_PREFIX}" ]]; then
      export PROJECT_PREFIX
      log_info "PROJECT_PREFIX=${PROJECT_PREFIX}"
    fi

    PROJECT_PATH_REL="$("${project_metadata_script}" "${PROJECT_NAME}" path 2>/dev/null || true)"
    if [[ -n "${PROJECT_PATH_REL}" ]]; then
      export PROJECT_PATH="${ROOT_DIR}/${PROJECT_PATH_REL}"
      log_info "PROJECT_PATH=${PROJECT_PATH}"
    fi

    PROJECT_LAST_SPRINT="$("${project_metadata_script}" "${PROJECT_NAME}" last_sprint 2>/dev/null || true)"
    if [[ -n "${PROJECT_LAST_SPRINT}" ]]; then
      export PROJECT_LAST_SPRINT
      log_info "PROJECT_LAST_SPRINT=${PROJECT_LAST_SPRINT}"
    fi
  else
    log_warning "project_metadata.py not executable; skipping project metadata enrichment."
  fi

  export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-${ROOT_DIR}/.config}"
  export WRANGLER_LOG_PATH="${WRANGLER_LOG_PATH:-${ROOT_DIR}/.wrangler/logs}"
  mkdir -p "${XDG_CONFIG_HOME}" "${WRANGLER_LOG_PATH}"

  log_info "PROJECT=${PROJECT_NAME}"
  log_end "Env bootstrap"
}

declare -a CONTEXT_PATHS=()

collect_context_files() {
  CONTEXT_PATHS=()
  local context_file

  local global_agent_file="${GLOBAL_AGENT_FILE}"
  local agents_dir="${AGENTS_DIR}"
  local template_dir="${TEMPLATE_DIR}"
  local project_agent_dir="${PROJECTS_DIR}/${PROJECT_NAME}/${PROJECT_AGENT_SUBDIR}"

  if [[ -f "${global_agent_file}" ]]; then
    CONTEXT_PATHS+=("${global_agent_file}")
  else
    log_warning "agents.md not found at ${global_agent_file#"${ROOT_DIR}"/}"
  fi

  if [[ -d "${agents_dir}" ]]; then
    while IFS= read -r context_file; do
      CONTEXT_PATHS+=("${context_file}")
    done < <(find "${agents_dir}" -type f -print | LC_ALL=C sort)
  else
    log_warning "agents/ directory missing (${agents_dir#"${ROOT_DIR}"/})"
  fi

  if [[ -d "${template_dir}" ]]; then
    while IFS= read -r context_file; do
      CONTEXT_PATHS+=("${context_file}")
    done < <(find "${template_dir}" -type f -print | LC_ALL=C sort)
  else
    log_info "agent-reference-template/ directory not present; skipping template context." >&2
  fi

  if [[ -d "${project_agent_dir}" ]]; then
    while IFS= read -r context_file; do
      CONTEXT_PATHS+=("${context_file}")
    done < <(find "${project_agent_dir}" -type f -print | LC_ALL=C sort)
  else
    log_warning "project agent-reference directory missing (${project_agent_dir#"${ROOT_DIR}"/})"
  fi
}

stream_context_files() {
  export CODEX_CONTEXT_LOADED=0

  if [[ -n "${CODEX_CONTEXT_SKIP:-}" ]]; then
    log_skip "Context bootstrap disabled via CODEX_CONTEXT_SKIP=${CODEX_CONTEXT_SKIP}"
    return
  fi

  collect_context_files

  if [[ "${#CONTEXT_PATHS[@]}" -eq 0 ]]; then
    export CODEX_CONTEXT_LOADED=0
    log_warning "Context loader discovered no files to stream."
    return
  fi

  local rel_path

  printf -v CODEX_CONTEXT_FILES '%s\n' "${CONTEXT_PATHS[@]}"
  CODEX_CONTEXT_FILES="${CODEX_CONTEXT_FILES%$'\n'}"
  export CODEX_CONTEXT_FILES
  export CODEX_CONTEXT_FILE_COUNT="${#CONTEXT_PATHS[@]}"

  log_start "Context bootstrap (${CODEX_CONTEXT_FILE_COUNT} files)"

  for context_path in "${CONTEXT_PATHS[@]}"; do
    rel_path="${context_path#"${ROOT_DIR}"/}"

    log_start "Context file: ${rel_path}"
    cat "${context_path}"
    log_end "Context file: ${rel_path}"
    printf '\n'
  done

  log_end "Context bootstrap"
  export CODEX_CONTEXT_LOADED=1
}

if [[ "${DO_ENV}" -eq 1 ]]; then
  run_env_bootstrap
fi

if [[ "${DO_CONTEXT}" -eq 1 ]]; then
  stream_context_files
fi
