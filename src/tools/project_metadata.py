#!/usr/bin/env python3
"""
Lightweight helper for reading project metadata from projects.yaml.

Usage:
  project_metadata.py <project_name_or_prefix_or_path> [field]

Without a field argument, the script prints the JSON payload for the project.
When a field is supplied (e.g. `prefix`, `path`, `last_sprint`, `parent`),
only that value is printed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List


ROOT_DIR = Path(__file__).resolve().parents[1]
PROJECTS_FILE = ROOT_DIR / "projects.yaml"


def _load_projects() -> List[Dict[str, str]]:
    if not PROJECTS_FILE.exists():
        raise FileNotFoundError(f"projects.yaml not found at {PROJECTS_FILE}")

    projects: List[Dict[str, str]] = []
    current: Dict[str, str] | None = None
    collecting_summary = False
    summary_lines: List[str] = []

    for raw_line in PROJECTS_FILE.read_text().splitlines():
        stripped = raw_line.strip()

        if collecting_summary:
            if raw_line.startswith(" " * 4) and stripped:
                summary_lines.append(stripped)
                continue
            else:
                if current is not None:
                    current["summary"] = " ".join(summary_lines).strip()
                collecting_summary = False
                summary_lines = []
                # fall through to handle the current line

        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- name:"):
            if current is not None and collecting_summary:
                current["summary"] = " ".join(summary_lines).strip()
                collecting_summary = False
                summary_lines = []
            name = stripped.split(":", 1)[1].strip()
            current = {"name": name}
            projects.append(current)
            continue

        if current is None:
            continue

        if stripped.startswith("prefix:"):
            current["prefix"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("path:"):
            current["path"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("parent:"):
            current["parent"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("last_sprint:"):
            current["last_sprint"] = stripped.split(":", 1)[1].strip().strip('"')
        elif stripped.startswith("summary:"):
            if stripped.endswith(">"):
                collecting_summary = True
                summary_lines = []
            else:
                current["summary"] = stripped.split(":", 1)[1].strip()

    if collecting_summary and current is not None:
        current["summary"] = " ".join(summary_lines).strip()

    return projects


def _lookup(projects: List[Dict[str, str]], query: str) -> Dict[str, str] | None:
    for entry in projects:
        if query in (
            entry.get("name"),
            entry.get("prefix"),
            entry.get("path"),
        ):
            return entry
    return None


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("usage: project_metadata.py <project> [field]", file=sys.stderr)
        return 1

    query = argv[1]
    field = argv[2] if len(argv) > 2 else None

    try:
        projects = _load_projects()
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    entry = _lookup(projects, query)
    if entry is None:
        print(f"project '{query}' not found in {PROJECTS_FILE}", file=sys.stderr)
        return 1

    if field:
        value = entry.get(field)
        if value is None:
            print(
                f"field '{field}' not available for project '{query}'",
                file=sys.stderr,
            )
            return 1
        if isinstance(value, (dict, list)):
            print(json.dumps(value))
        else:
            print(value)
    else:
        print(json.dumps(entry))

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
