# agentharmony Starter Kit

This directory packages the reusable files needed to spin up a brand-new project that follows the agentharmony documentation and automation workflow.

## What's Included
- `agents.md` and the `/agents` reference set for governance + numbering rules.
- `agent-reference-template/` markdown + YAML scaffolding for project-specific docs.
- `bootstrap-session.sh`, `codex-auto.sh`, and `claude-project` to bootstrap Codex/Claude sessions with consistent env vars.
- `tools/` helpers such as `project_metadata.py`, `lint-bootstrap.sh`, and placeholder prompt libraries.
- `repo-template/` – copy this into `projects/<project>/repo/` when creating a new Git repo.
- Supporting config files like `agents-ide.yaml` and `projects.yaml` that you should customize per environment.

## How To Use
1. **Copy this directory** into the root of your automation workspace (e.g., `~/codex`).
2. **Fill in placeholders**:
   - Update `agents.md`, `agents-ide.yaml`, and `projects.yaml` with your org, infra, and project details.
   - Duplicate `agent-reference-template/$PROJECT-reference-template.md` for each new project and rename it to `projects/<project>/agent-reference/<project>-reference.md`.
3. **Create a project repo**:
   - `cp -R repo-template projects/<project>/repo`
   - Initialize Git, add a remote, and start committing code/documentation.
4. **Bootstrap sessions** with `./codex-auto.sh <project>` (streams context + launches Codex) or `./claude-project <project>` (for Claude Desktop).
5. **Automate linting** via `tools/lint-bootstrap.sh` once shellcheck + markdownlint are installed.

Keep this starter kit clean—treat it as the canonical blank canvas you can archive, fork, or redistribute to peers who want the same agentic development workflow.

## Tips

- **One-command session startup**: Add shell aliases that point to the starter-kit scripts so you can simply run `codex <project>` or `claude <project>` from any terminal:
  ```bash
  alias codex="/path/to/starter-kit/src/codex-auto.sh"
  alias claude="/path/to/starter-kit/src/claude-project"
  ```
  These wrappers export `PROJECT=<project>` and (via `codex-auto.sh`) stream the governance context before handing off to the Codex/Claude CLIs. Override `PROJECTS_DIR` or `BOOTSTRAP_SCRIPT` env vars if your workspace layout differs.
