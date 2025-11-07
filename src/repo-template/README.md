# Repo Template

This directory provides the baseline layout for new project repositories.

## Usage

1. Copy the entire `repo-template` directory into your project and rename it to `projects/<project-name>/repo`.
2. Update the `README.md` to describe the actual project.
3. Remove or replace placeholder `.gitkeep` files once real assets exist.
4. Initialize Git from inside the new `repo` directory:
   ```bash
   cd projects/<project-name>/repo
   git init
   git checkout -b main
   ```
5. Configure the remote repository in your GitHub organization/user namespace before the first push.

## Layout

```
repo/
├── README.md          # Project overview, environment setup, deployment scripts
├── .gitignore         # Common exclusions (node_modules, build artifacts, venvs, etc.)
├── docs/              # Project documentation to ship with the repo
├── scripts/           # Utility scripts committed to the repo
└── src/               # Application source code
```

Additional directories (e.g., `tests/`, `infrastructure/`) can be added as needed. Keep generated output (logs, coverage reports, build artifacts) outside the repo or ensure they are excluded via `.gitignore`.

