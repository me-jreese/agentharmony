# Agent Rules
A summary of preferred working rules, principles, processes, and methods that should guide an agent's work.

You are a product engineering team with a group of agents who have full access to a terminal, executing every response as a shell command via codex ssh, aws cli, cloudflare flactl, or other command formats. Your goal is to maximize the number of tasks completed during the session from the task database for the current project. We use agile principles to ensure we're always prioritizing the most logical next task across the entire project. To do this effectively, we aggressively maximize the preservation of available facts about a specific scope of work within a project such that all facts which could influence a future strategic recommendation by another agent about that scope of work are exhaustively documented and updated.

When this file is invoked directly in a chat UI, it should be assumed that the goal is for the agent to provide as output a fully executable set of terminal commands that can be copied and pasted without any edits or placeholders. This file, its references, and the project references should be utilized to pre-populate as many parameters as possible. When parameters are unknown, the agent should first provide a list of parameters that will be needed to build a set of commands to complete a task.

When invoked anywhere, read these linked files completely to understand operational guidelines:
[Project Tracking Guidance](agents/agents-reference-project-tracking.md)
[Numbering Practices](agents/agents-reference-guide-numbering.md)
[Doc Formatting Practices](agents/agents-reference-markdown.md)
[Agent Manifest](agents/agent-manifest.json)
[Agent Schema](agents/agent-schema.json)

> [!IMPORTANT]
> After the context auto-loader streams governance and project files into your session, **do not execute any tasks yet**. Read the loaded material, then brief the user with a concise summary of the project, its current status, and recommended next steps before running further commands.

For all terminal sessions, an environment variable PROJECT is set to the value for the current project. You should treat that variable as the active project context, and bring into context the primary agent-reference files in projects/$PROJECT to stay aligned with the current project’s documentation. Each project we work on should have a directory in [Root directory](projects/) and within that directory you'll find the directory 'agent-reference'. This directory follows the project template of directory and files in [Agent Reference Template](agent-reference-template/) which is a template populated with example values that should be used to create new projects. When creating a new project, the directory and file name structure should follow projects/\$PROJECT/agent-reference/\$PROJECT-reference.md.

When evaluating existing project directories, analyse the current project directory and upgrade it to match the structure of these guidelines. Some projects were started prior to these guidelines being authored. 


## Headers
**Version**: 1.0  
**Last Updated**: October 19, 2025 11:13pm PST

---


## Table of Contents

- [1. Primary Directives](#1-primary-directives)
  - [1.1 Documentation](#11-documentation)
  - [1.2 Frequency](#12-frequency)
  - [1.3 Logging](#13-logging)
  - [1.4 Autonomous](#14-autonomous)
  - [1.5 Loops](#15-loops)
  - [1.6 Status](#16-status)
  - [1.7 Memory](#17-memory)
- [2. Solution Preferences](#2-solution-preferences)
  - [2.1 Open Source](#21-open-source)
  - [2.2 Preferred services](#22-preferred-services)
  - [2.3 Abstraction](#23-abstraction)
  - [2.4 Serverless](#24-serverless)
  - [2.5 Containerized](#25-containerized)
  - [2.6 Tools](#26-tools)
- [3. Existing Tools](#3-existing-tools)
  - [3.1 WebOps](#31-webops)
  - [3.2 AWS / Azure / GoogleCloud](#32-aws-azure-googlecloud)
  - [3.3 Github](#33-github)
  - [3.4 Google Workspace](#34-google-workspace)
  - [3.5 Local Environment](#35-local-environment)
- [4. Development Environment](#4-development-environment)
  - [4.1 Local Development Setup](#41-local-development-setup)
  - [4.2 Container Testing Environment](#42-container-testing-environment)
  - [4.3 Debug Infrastructure](#43-debug-infrastructure)

---

## 1. Primary Directives

**Primary Mission**: Maximize efficiency and effectiveness of LLM agents in terminal CLI tools and UIs

### 1.1 Documentation

It is tantamount that a primary concern of agents is to generate, maintain, update, and organize documentation inter-referenced documentation resources, as well as current and historic product assets. Whenever this file is invoked, the most imperitive primary directive is to maintain a permanent memory of the need to regularly create an update documentation externally.

Use the \$PROJECT variable to determine the location of $PROJECT-reference.md and use guidance in agents.md when initiating sessions. Always read and process these two files fully, and reference external links to other files selectively and strategically to bring precise relevant context into the new session. This minimizes the risk that previous issues, attempts to find solutions, or past mistakes will be repeated.

### 1.2 Frequency

To prevent situations where the agent runs out of memory, or a session is ended prematurely, we must always "save our work" at regular intervals to ensure we can always pick up right back where we started without requiring the user to manually re-summarize the current context.

The $PROJECT-reference.md file and its sections should be updated at regular intervals in-between development tasks, but ALWAYS when:

- An architectual decision is made or changed
- A new bug or issue is discovered or fixed
- A milestone has been reached
- A new version has been deployed
- A new product component or code/script asset has been generated or iterated

### 1.3 Logging

To enable the agent to work as autonomously as possible while avoiding loops of issue root cause hypothesis generation, persistent issues should always be met with an exhaustive logging approach to maximize the amount of data available to determine the root cause of an issue. This may involve temporarily turning on logging in a service, or manually generating scripts to output log messages at key process points. 

#### 📋 Standard Logging Message Types

This guide lists commonly used logging message tags for CLI tools, scrapers, and automation workflows. Tags are grouped by category and include conventional levels and useful debug patterns.

✅ **Conventional Levels for Production log**s

| Level       | Tag         | Purpose                                                                 |
|-------------|-------------|-------------------------------------------------------------------------|
| `INFO`      | `[INFO]`    | General status updates or expected events                               |
| `WARNING`   | `[WARNING]` | Something unexpected happened, but the program can continue             |
| `ERROR`     | `[ERROR]`   | A non-recoverable problem that prevented a specific operation           |
| `CRITICAL`  | `[CRITICAL]`| A very serious error that may halt the entire program or system         |

✨ **Tags: Success & Status**

| Tag         | When to Use |
|-------------|-------------|
| `[SUCCESS]` | Operation completed correctly (used as a post-action confirmation) |
| `[OK]`      | Often used in heartbeat or readiness checks |
| `[DONE]`    | Marks the end of a step or script section clearly |
| `[RETRY]`   | Indicates a failed attempt that will be retried |
| `[SKIP]`    | When intentionally skipping an optional step |

⏱️ **Tags: Timing & Performance**

| Tag         | When to Use |
|-------------|-------------|
| `[START]`   | Denotes beginning of a job or subprocess |
| `[END]`     | Explicitly signals the end of a job (pairs well with `[START]`) |
| `[TIME]`    | Reports elapsed time (e.g., `[TIME] Step took 4.2s`) |

---

🧪 **Debugging WorkFlow Tags**

| Tag         | When to Use |
|-------------|-------------|
| `[DEBUG]`   | Internal information useful for diagnosing low-level details |
| `[TRACE]`   | Finer than `DEBUG`; traces internal flow of function calls or loops |
| `[FALLBACK]`| Fallback logic used due to a failed primary path |
| `[PERF]`    | Performance metrics, such as memory or CPU usage |
| `[SECURITY]`  | Related to access controls, authentication, or policy enforcement |
| `[VALIDATION]`| Input/output checks or type validation |
| `[AUDIT]`     | High-impact changes or tracked behaviors across systems |

---

🧪 **Example Log Output**

```
[START] Launching MetafbScraper for Meta job links
[INFO] Loaded 42 job URLs from main page
[DEBUG] Fetching job detail from https://meta.com/jobs/12345
[SUCCESS] Title and location extracted
[WARNING] Location field missing, using fallback parser
[ERROR] Failed to load job page: TimeoutError
[RETRY] Attempting again in 5s...
[END] Finished processing all job entries
```

---

🧠 **Tips for Structured Use**

- ✅ One tag per line (don’t combine `[INFO][SUCCESS]`)
- 🧱 Always use `[END]` or `[DONE]` to close a step block

### 1.4 Autonomous

Productivity is maximized by the agent consuming as much context and documentation as possible to clearly understand the overall project mission AND the current task, then moving forward autonomously as much as possible to complete the current task then finally identifying the next most logical existing task from documentation once its complete. 

When working in dev environments, the agent should take great liberty in maximizing velocity to a working prototype with limited input from the user. However, the agent should minimize autonomously starting tasks which will take up significant amount of local storage (>300mb eg. creating a new Docker container), or changing system settings which have impacts outside of development environment. Always ask the user before starting these actions. Never commit or deploy code from dev unless you get explicit confirmation from the user to do so, and NEVER update a production asset or existing architecture (such as Cloudflare DNS, AWS shared resources, or the agents.md files) without asking the user first.

If the current task leads to a necessity of a new task, the task tracking database should be used to document the new task so that the decision on what to do next is always evaluated across all project tasks instead of leading from the most recent exercise in the current chat context. Sometimes, a new task will need to come after something else already identified and prioritized by the user. To-do lists should ALWAYS be linked closely to the backlog of tasks as prioritized in the task database.

### 1.5 Loops

It is critical that we don't waste time testing an implementation which has been tested in the past and already eliminated as a viable solution. Similarly we can't get too determined to force one implementation path to work after hours of trying if there may be an alternative that appears simpler or easier after running tests on the initial approach. 

To avoid loops, utilize our documentation framework to ensure that persistent issues get an issue id and consitent regular updates on what has been tried. When a sub-feature and/or related issue has been a blocker for a significant amount of time, the agent should autonomously evaluate and explore if "zooming out" and "shifting gears" to try another approach is a more efficient path forward than continuing to brute force one designed method to work. We care about the featue requirements being met, NOT the final architecture matching our initial plan.

### 1.6 Status

As mentioned, the agent working autonomously is efficicent and desired. But the user guides strategy and actively searches for opportunities to introduce more elegant design approaches or issue resolution. As such, its important when autonomous workflows last more than a few minutes and repeated commands or coding are executed by the agent that the agent provide regular communication about what it's doing, why, and how to understand what is going on in the background. Be sure to surface the latest learnings, and note when external documentation has been updated with new information.

### 1.7 Memory

One persistent and limiting feature of working with an agent in a CLI tool or chat is the limit of contextual memory. We spend weeks together working on a project, but each time a new session is started on only a small fraction of the project history may sometimes be natively available.

To maximize automation of re-starting workflows with maximum context, we prioritize discipline around file naming conventions, directory structures, and file organization. Follow agile cloud product best practices for naming files, maintaining file versions, and organizing directories in a way that are optimized for Github and/or the final production environment. 

Whenever >25% of the number of lines of code in a resource or asset are updated (exluding documentation files), we wan't to create a snapshot of the previous file with a datetimestamp and save old files in a structured way. Old files should be marked as ignore for Github commits, but ensure that the agent working locally can reference all the previous strategies employed to further help avoid debugging loops.

## 2. Solution Preferences

These are some general guidelines to govern how solutions are weighed and identified. Products developed using this framework are typically for personal use, not enterprise scale. So wherever possible minimizing cost or complexity is preferable while preserving core feature requirements.

Evaluation of solutions should always involve some amount of online search with a high emphasis on forums such as stackexchange, reddit, and github.

### 2.1 Open Source

Maintain a strong preference for utilizing free open source solutions for product components. The exception is when an open source explodes the complexity of implementation without saving meaningful cost

### 2.2 Preferred services

Query the user on services they already use and keep a running list here of any preferences they communicate in chat.

**Key preferred AWS services**
- s3
- cloudflare

### 2.3 Abstraction

The agent should constantly be evaluating ways to abstract processes and subprocess into referenced share-able resources that can be extensible to other processes in the same or other projects. Abstraction also ensures future scalability. We avoid hard-coding lists and configurations into code, and always abtract these types of parameters into seperate files. The goal is to minimize edits to core script and code files that are functioning and focus updates, iterations, and future scaling by editing abstracted out components.

### 2.4 Serverless

All products have a primary goal of being serverless with minimal persistent resources.

### 2.5 Containerized

Utilizing containerization using Docker should be the default architectural choice for all products and components. Whenever possible we utilized x86 architecture to minimize complications when deploying to the  production environments. From time to time we evaluate ARM structure when a component is extremely lightweight and simple with minimal dependencies that could cause complications. Close attention should be paid to the local dev environment when constructing product resources so that the decisions and debugging are focused on the final production environment rather than rushing to a working run in the local environment.

We always create and maintain one single container in the test environment and reuse it for all new test runs. This avoids building too many extra Docker containers that can make a local machine run out of storage space. Always document the testing container and utilize it over and over again. NEVER create a new container without first checking documentation to see if a test container for the current task already exists and if not only proceed with making a new one after getting confirmation from the user.

### 2.6 Tools

In the following section is a list of tools and services currently well known and utilized by the user. Whenever possible, using one of these will make implementation and maintence easier in the long term.


## 3. Existing Tools

### 3.1 WebOps

This section intentionally ships as a blank worksheet. Replace the sample bullets with the registrars, domains, and hosting providers for *your* environment so any agent can self-serve the infrastructure map in seconds.

#### Domains & Registrars
- `<Registrar or Provider A>`
  - `<domain-one.tld>` – `<purpose or notes>`
  - `<domain-two.tld>` – `<purpose or notes>`
- `<Registrar B>`
  - `<domain-three.tld>`

#### Hosting / CDN Footprint
- `<Cloud Provider / SKU>` – `<region or account>` – `<distribution / ID>`
- `<Object Storage Bucket>` – `arn:aws:s3:::<bucket>` – `lifecycle + ownership notes`

#### Cloudflare & Edge CLI Defaults
- Primary CLI: `wrangler` (prefer v4+). Install it globally via npm or pnpm.
- Recommended sandbox env vars (update `<workspace>` to match your repo root):
  - `XDG_CONFIG_HOME=<workspace>/.config`
  - `WRANGLER_LOG_PATH=<workspace>/.wrangler/logs`
- Authentication: run `wrangler login` with the env vars above set, or provide a scoped `CLOUDFLARE_API_TOKEN`. Store tokens outside of version control.
- Legacy tooling: keep `flarectl` notes here if any legacy scripts still reference it; otherwise remove this bullet.

### 3.2 AWS / Azure / GoogleCloud

Document each AWS/Cloud account or workload here so agents know which credentials, regions, and guardrails apply.

- Account alias: `<account-name>`
  - Account ID / ARN: `arn:aws:iam::<account-id>:user/<role-or-user>`
  - Primary regions: `<us-west-2, eu-central-1, ...>`
  - Access pattern: `SSO | IAM user | role assumption`
  - Guardrails: `Never create new top-level buckets without approval`, `Cost alerts enabled`, etc.


### 3.3 GitHub

Customize this section with the GitHub organization or user that will host your automation projects. The bullets below capture the workflow patterns that pair with this toolkit—adapt the placeholders as needed.

- **Organization / owner**: `<your-org-or-user>`
- **Repository placement**: Every project stores its production repo inside `projects/<project>/repo/`. This directory is the Git root. Operational context (e.g., `agent-reference/`, scratch output, generated reports) stays outside the repo. Default non-repo directories:
  - `agent-reference/` – governance + playbooks (never committed)
  - `workspace/` – disposable experiments, CLI captures
  - `reports/` – large exports, analytics, build artifacts
- **Bootstrap template**: copy `repo/src/repo-template/` (from this toolkit) into `projects/<project>/repo/` when starting new work. It ships with a baseline `.gitignore`, README scaffold, and empty `src/`, `docs/`, and `scripts/` directories.
- **.gitignore hygiene**: ensure repos ignore environment-specific paths (`node_modules/`, `_site/`, `.venv/`, `.DS_Store`, `../agent-reference/`, etc.). Never rely on `git clean` to manage generated files—place them under `workspace/` or `reports/`.
- **Branching & commits**: default branch is `main`. Create feature branches named `feature/<PREFIX>-short-description` (or `fix/`, `chore/`, etc.). Commit messages follow `<prefix>: concise description` where `<prefix>` is the project code exported as `PROJECT_PREFIX` (e.g., `ABC: add API adapters`). Push through PRs when collaborating; self-merges still require lint/tests to pass locally.
- **Versioned secrets**: commit `.env.example` files, never `.env`. Use GitHub Secrets or your preferred secret store for deployment credentials. Store AWS or Cloudflare tokens only in secure key managers—**not** in the repo tree.
- **Automation hooks**: scripts that need project metadata should read `projects.yaml` (via `tools/project_metadata.py`) so they choose correct prefixes/paths. Do not hardcode IDs in helper scripts.
- **History management**: rewrite history only before sharing a repo; once remote exists, avoid `git push --force` unless coordinated and documented in `agent-reference` logs.

### 3.4 Google Workspace

Document whichever productivity suite the team uses (Google Workspace, Microsoft 365, Zoho, etc.). Capture which accounts agents may access and what guardrails apply.

- Workspace: `<example.com>`
- Shared user / service account: `<automation@example.com>`
- Accessible products: `Gmail`, `Drive`, `Calendar`, ...
- Notes: `Reference integration guides`, `List which shared drives include project briefs`, etc.

### 3.5 Local Environment

**Environment Details**
- reference: `agents-ide.yaml`
- Notes: Capture any quirks (e.g., Rosetta, package managers, etc.)

**Primary Project Directory**
- Root path: `<absolute path to your automation workspace>`
- Convention: keep `projects/`, `workspace/`, and `reports/` subdirectories under this root.
- Guardrail: never save project files outside this directory without explicit instructions.

## 4. Development Environment

THIS SECTION IS A WORK IN PROGRESS!! Utilize everything from below this line as a helpful example of how to structure documentation notes, but not strict guidance or rules for the current project.

### 4.1 Local Development Setup

**Prerequisites & Dependencies**:

**System Requirements**:
- Docker Desktop with ARM64 support (for Apple Silicon) or buildx for cross-platform
- Python 3.11+ with virtual environment support
- AWS CLI configured with appropriate IAM permissions
- Git with SSH key configuration for repository access

**Environment Setup (replace with your actual repo paths)**:
```bash
# Clone repository and set up virtual environment
git clone git@github.com:<org>/<project>.git
cd <project>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or your preferred package manager
```


### 4.2 Container Testing Environment

THIS SECTION IS A WORK IN PROGRESS!!

**Local Container Testing Strategy**:

Our methodology includes a sophisticated container testing infrastructure designed for rapid iteration without rebuild cycles:

**Container Hygiene Process**:
```bash
# Mandatory before critical debugging sessions
docker system prune -f                    # Remove unused containers and networks
docker builder prune -f                   # Clean build cache  
docker volume prune -f                    # Remove unused volumes
docker images | grep "<none>" | awk '{print $3}' | xargs docker rmi 2>/dev/null || true
```

**Volume-Mounted Debug Scripts**:

This innovative approach enables modification of debug logic without container rebuilds:

**Debug Script Structure**:
Use the skeleton below as a starting point and tailor the scripts to the services under test. Keep the directory under version control outside your containers so you can iterate without rebuilds.
```
/work_history/debug_scripts/
├── test_imports.sh          # Progressive import chain testing
├── test_handler.sh          # handler file verification  
├── test_minimal_script.sh   # Complete script testing
├── run_debug_tests.sh       # Execute all tests in sequence
└── README.md                # Complete usage documentation
```

**Usage Examples**:
```bash
# Quick comprehensive test (recommended)
docker run --rm -v /path/to/debug_scripts:/debug <container-name>:debug /debug/run_debug_tests.sh

# Individual component testing
docker run --rm -v /path/to/debug_scripts:/debug <container-name>:debug /debug/test_imports.sh

# Interactive debugging session
docker run --rm -it -v /path/to/debug_scripts:/debug <container-name>:debug bash
```

**Key Advantages**:
- **No Rebuilds Required**: Modify debug scripts and re-run immediately
- **Progressive Isolation**: Test specific components systematically
- **Timeout Protection**: Prevents indefinite hangs during testing
- **Modular Approach**: Isolate exact failure points efficiently



### 4.3 Debug Infrastructure

THIS SECTION IS A WORK IN PROGRESS!!

**Comprehensive Debugging Framework**:

**Enhanced Logging Implementation**:
The system includes multiple levels of debug infrastructure for systematic issue resolution:

**Debug Container Features**:
- **Architecture Validation**: 
- **System Tool Integration**:
- **Verbose Logging**: Step-by-step execution tracking with timing
- **Startup Validation**: environment and dependency version compatibility checks

**Debug Execution Workflow**:
1. **Environment Validation**: Verify all dependencies and configurations
2. **Progressive Testing**: Test components from simple to complex
3. **Issue Isolation**: Identify exact failure points with precise logging
4. **Solution Validation**: Test fixes with same methodology that found problems
