# 📘 io’s Numbering Systems for Instructions & Documentation

---

## 🧭 PART 1: CLI-FRIENDLY STEP EXECUTION SYSTEM (Codex & Automation)

### 🧠 Purpose
This system supports **automated task execution**, such as pasting into Codex or shell sessions. It emphasizes:
- Uniqueness
- Easy reference
- Non-sequential step invocation
- Ambiguity avoidance

### 🔢 Format Specification

| Attribute              | Value |
|------------------------|-------|
| **Step Prefix**        | Random, readable alphanumeric ID (e.g., `S4A6Tx`) |
| **Substeps**           | Hyphenated with suffixes: `S4A6Tx-a`, `S4A6Tx-b`, etc. |
| **Length**             | 6-character prefix minimum, mixed case alphanumeric |
| **Collision Handling** | All steps within a given sequence must be unique |
| **Ambiguity Avoidance** | Avoid easily confusable characters: `l`, `I`, `1`, `0`, `O` |

### 🛠️ Codex Execution Semantics

| Command                         | Description |
|----------------------------------|-------------|
| `codex exec S4A6Tx`             | Executes entire step tree (step + substeps) |
| `codex exec S4A6Tx-b`           | Executes single substep |
| `codex goto S4A6Tx-b`           | Jump reference for documentation or inline help |
| `codex log S4A6Tx`              | Retrieve status/log for step |

### 🧭 Behavior & UX Guidelines

- Do **not** use numeric labels like `1.` or `a.` — these **do not support automated referencing**
- Steps must be **referenced by their ID** (e.g., “Repeat `M7dK1a-b`”)
- Every instruction set must begin with a complete list of **step + description**, like:

```
T4y1Rc Initialize AWS credentials
T4y1Rc-a Export access key
T4y1Rc-b Export secret key
```

---

## 📚 PART 2: LOGICAL DOCUMENTATION SYSTEM (Human-Friendly Guides, SOPs)

### 🧠 Purpose
Used in **structured longform documentation**, wikis, SOPs, and project planning docs. Prioritizes:
- Readability
- Logical hierarchy
- Navigability
- Interoperability with automation references

### 🏗️ Structure Overview

```
[PROJECT-CODE]-[SECTION][STEP][SUBSECTION]
```

### 🔤 Element Definitions

| Component        | Description |
|------------------|-------------|
| **Project Code** | 2–3 letter identifier (e.g. `CC`, `GW`, `JDS`) |
| **Section**      | Capital letter `A`, `B`, `C`... |
| **Step**         | Integer step number: `1`, `2`, `3` |
| **Subsection**   | Optional lowercase suffix: `.1`, `.2` or letter `A`, `B`, etc. |

### 📑 Example Patterns

| ID        | Description |
|-----------|-------------|
| `EXP-A1`  | JDS doc, Section A, Step 1 |
| `CC-B2.3` | Claude Code, Section B, Step 2, Substep 3 |
| `GW-C4A`  | Google Workspace, Section C, Step 4, Sub-A |

### 📋 Table of Contents Format

```
| Step ID  | Title                       |
|----------|-----------------------------|
| EXP-A1   | Initialize CLI Configuration |
| EXP-B1   | Set up Proxy Credentials     |
| EXP-C1   | Run Main Script             |
```

### 🧱 SOP Implementation Guidelines

#### 🧩 Structure
- Begin each section with a header `## EXP-A: Section Title`
- Use **step headers** for each block: `### EXP-A1: Step Title`
- Include duration estimate, verification, and flags

#### 🧪 Verification Markers
- ✅ Completion box
- ⏱️ Estimated time
- ⚠️ Warnings or required conditions

#### 🔁 Cross-Referencing
- Always refer to prior sections by ID (`see EXP-A2.1`)
- Use anchors or collapsible blocks in rendered Markdown/Notion

---

## 🔁 Bridging the Two Systems

| Feature                    | CLI Mode                          | Docs Mode                        |
|----------------------------|-----------------------------------|----------------------------------|
| Prefix                    | Random alphanumeric (e.g. `T4y1Rc`) | Project-specific code (e.g. `JDS`) |
| Format                    | Flat + suffixes                    | Hierarchical alphanumeric        |
| Reference Style           | By step ID only                    | Step ID + context header         |
| Used In                   | Automation, Codex, CLI sessions    | Docs, wikis, SOPs, guides        |
| Rationale                 | Uniqueness, atomic execution       | Hierarchy, readability           |

---

## 📛 Project Tracking Prefixes (Global SOP)

- Every project maintains a unique three-letter uppercase prefix derived from its name (e.g., `ABC` for AppCore, `OPS` for OpsHub, `DVP` for DevPlatform).
- Apply this prefix to all feature (`FTR`), task (`TASK`), and issue (`BUG`) IDs so they become universally unique across repositories (`ABC-FTR-101`, `OPS-TASK-210`, etc.).
- When creating or editing IDs, ensure no double-prefixing—check for an existing `[A-Z]{3}-` prefix before adding a new one.
- The canonical list of prefixes, project paths, and sprint cadences lives in `projects.yaml`; update that file whenever a new project or subproject is introduced.
- Historical references outside the agent-reference directories can retain legacy IDs for archival accuracy, but all active registries and documentation must adopt the prefixed format.
---

## 🧩 YAML Schema: CLI Instruction Format

```yaml
step_id: S4A6Tx
description: Initialize AWS credentials
substeps:
  - step_id: S4A6Tx-a
    description: Export access key
    command: export AWS_ACCESS_KEY_ID=xxxxxx
  - step_id: S4A6Tx-b
    description: Export secret key
    command: export AWS_SECRET_ACCESS_KEY=xxxxxx
```

---

## 🧩 JSON Schema: Documentation Structure Format

```json
{
  "project_code": "EXP",
  "sections": [
    {
      "id": "EXP-A",
      "title": "Initialize CLI Configuration",
      "steps": [
        {
          "id": "EXP-A1",
          "title": "Install Dependencies",
          "estimated_time": "3 min",
          "verification": "pip list | grep requests",
          "warning": null
        },
        {
          "id": "EXP-A2.1",
          "title": "Set Environment Variables",
          "estimated_time": "1 min",
          "verification": "echo $ENV_VAR",
          "warning": "⚠️ Don’t expose secrets in logs"
        }
      ]
    }
  ]
}
```
