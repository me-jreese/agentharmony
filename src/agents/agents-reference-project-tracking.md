# Project Tracking Reference

## Table of Contents
- [1. Purpose](#1-purpose)
- [2. ID Format Standards](#2-id-format-standards)
  - [2.1 Three-Segment ID Pattern](#21-three-segment-id-pattern)
  - [2.2 Prefix Management](#22-prefix-management)
  - [2.3 Type Codes](#23-type-codes)
  - [2.4 Sequence Numbers](#24-sequence-numbers)
- [3. Nested Child ID Protocol](#3-nested-child-id-protocol)
- [4. YAML Structure Standards](#4-yaml-structure-standards)
  - [4.1 Global Attributes](#41-global-attributes)
  - [4.2 Feature-Specific Attributes](#42-feature-specific-attributes)
  - [4.3 Task-Specific Attributes](#43-task-specific-attributes)
  - [4.4 Issue-Specific Attributes](#44-issue-specific-attributes)
- [5. Relationship Management](#5-relationship-management)
  - [5.1 Parent-Child Relationships](#51-parent-child-relationships)
  - [5.2 Dependencies](#52-dependencies)
  - [5.3 Blockers](#53-blockers)
  - [5.4 Related Items](#54-related-items)
- [6. History & Logging](#6-history-logging)
  - [6.1 History Entry Structure](#61-history-entry-structure)
  - [6.2 Status Transitions](#62-status-transitions)
  - [6.3 Worklog Best Practices](#63-worklog-best-practices)
- [7. Status Management](#7-status-management)
  - [7.1 Feature Status Values](#71-feature-status-values)
  - [7.2 Task Status Values](#72-task-status-values)
  - [7.3 Issue Status Values](#73-issue-status-values)
- [8. Technical Notes & Metadata](#8-technical-notes-metadata)
- [9. Examples](#9-examples)
  - [9.1 Complete Feature Example](#91-complete-feature-example)
  - [9.2 Complete Task Example](#92-complete-task-example)
  - [9.3 Complete Issue Example](#93-complete-issue-example)

---

## 1. Purpose

The project-tracking reference establishes the universal SOP for how agents create, name, and manage entries in every `agents-reference` YAML file. It keeps every feature (`FTR`), task (`TSK`), and issue (`ISS`) traceable across the entire project portfolio, ensures future automation (Codex/Claude/CI) can reason about IDs, and maintains alignment with the attribute audit captured at `projects/agentharmony/docs/attribute_audit.md`.

**Key principles:**
- **Consistency**: All IDs follow the same three-segment pattern (PREFIX-TYPE-NUMBER)
- **Traceability**: Every item links to related work through standardized relationship fields
- **History**: All changes are logged with timestamps and descriptions in the `history` attribute
- **Automation-ready**: Structure enables parsing, validation, and cross-project reporting

---

## 2. ID Format Standards

### 2.1 Three-Segment ID Pattern

**CRITICAL**: All IDs must follow the format `XXX-YYY-ZZZ` where each segment is exactly 3 characters:
- **Segment 1 (XXX)**: Three uppercase letters representing the project prefix
- **Segment 2 (YYY)**: Three-character type code (FTR, TSK, ISS)
- **Segment 3 (ZZZ)**: Three-digit zero-padded sequence number (001, 002, 010, 999)

**Examples:**
- ✅ `AGH-TSK-001` (correct)
- ✅ `DVP-FTR-042` (correct)
- ✅ `JAP-ISS-100` (correct)
- ❌ `AGH-TASK-001` (wrong: type code is 4 characters)
- ❌ `AGH-TSK-1` (wrong: sequence not zero-padded to 3 digits)
- ❌ `AGENTHARMONY-TSK-001` (wrong: prefix exceeds 3 characters)

### 2.2 Prefix Management

Every project owns one uppercase, three-letter prefix derived from its name:
- `AGH` = AgentHarmony
- `HFY` = HarrisonFamily

**Prefix registry**: `projects.yaml` is the canonical source of truth for all prefixes, paths, and sprint cadences.

**Rules:**
1. Update `projects.yaml` immediately when creating a new project
2. Never double-prefix (check for existing `[A-Z]{3}-` before prepending)
3. All files under `projects/*/agent-reference` must use current prefix patterns
4. Historical references in markdown logs may retain legacy patterns but should be updated when touched

### 2.3 Type Codes

Use exactly these three-character codes:
- **`FTR`**: Feature or epic (large scope, multiple tasks)
- **`TSK`**: Task (actionable work item, can be assigned)
- **`ISS`**: Issue or bug (problem requiring investigation/resolution)

**Never use:**
- ❌ `TASK` (4 characters)
- ❌ `BUG` (use `ISS` instead)
- ❌ `FEAT` (use `FTR` instead)

### 2.4 Sequence Numbers

- Always three digits, zero-padded: `001`, `002`, ..., `999`
- Start at `000` or `001` depending on project preference (be consistent within a project)
- Increment sequentially within each type code
- Do not reuse numbers from deleted/abandoned items (preserve history)

---

## 3. Nested Child ID Protocol

When a feature/task/issue spawns subordinate entries, append a fourth segment using a dash and two-character suffix:

**Format**: `PREFIX-TYPE-NNN-XY`
- **X**: Single numeric digit (0-9) for grouping
- **Y**: Single uppercase letter (A-Z) for siblings within group

**Examples:**
- `AGH-ISS-001-0A` (first child, group 0)
- `AGH-ISS-001-0B` (second child, group 0)
- `AGH-ISS-001-1A` (first child in group 1, for logically distinct follow-ups)
- `MCP-FTR-001-0A`, `MCP-FTR-001-0B`, `MCP-FTR-001-0C` (three investigation subtasks)

**Rules:**
1. Numeric character starts at `0` and increments for logical groupings
2. Letter starts at `A` and increments alphabetically for siblings
3. Children **must** record their parent in the `parent` field
4. Parent IDs can be referenced in `related`, `depends_on`, or `blocked_by` for rollup automation

---

## 4. YAML Structure Standards

All YAML files follow the structure defined in `agents/yaml_structure.yaml`.

### 4.1 Global Attributes

These attributes apply to **all** item types (features, tasks, issues):

```yaml
- id: XXX-TSK-001
  parent: XXX-TSK-000  # Optional: only when this is a child item
  title: Short descriptive title
  status: open  # or closed
  description: >
    Detailed description of the work item, requirements, context,
    and any background information needed.
  acceptance_criteria:
    - First success criterion
    - Second success criterion
    - Nth success criterion
  technical_notes:
    - distribution-id: E2JCDK3QLQNNYB
    - account-id: 356364570033
    - system: cloudflare
    - any_key: any_value
  blocked_by:  # Optional: only when blocked
    - type: task  # feature, task, or issue
      ids: [XXX-TSK-007]
  depends_on:  # Optional: only when there are dependencies
    - type: feature
      ids: [XXX-FTR-001]
  related:  # Optional: for loose associations
    - type: issue
      ids: [XXX-ISS-000, XXX-ISS-001]
    - type: task
      ids: [ZZZ-TSK-001]
  history:  # Always present; must include 'created'
    - timestamp: 2025-11-07T18:15:00Z
      status: created
      description: Initial task creation for framework update
    - timestamp: 2025-11-08T09:30:00Z
      status: started
      description: Began implementation after stakeholder approval
    - timestamp: 2025-11-08T14:45:00Z
      status: worklog
      description: Completed first iteration, discovered dependency on XXX-FTR-001
    - timestamp: 2025-11-09T16:00:00Z
      status: closed
      description: All acceptance criteria met, deployed to production
```

**Key requirements:**
- `id` is **required** and must follow the 3-3-3 format
- `title` is **required** and should be concise (3-8 words)
- `status` is **required** (use type-specific allowed values)
- `description` is **required** and should be comprehensive
- `acceptance_criteria` is **strongly recommended** for clarity
- `history` is **required** and must contain at least one `created` entry
- `parent` is **required** for child items (format: `PREFIX-TYPE-NNN`)
- Use `blocked_by`, `depends_on`, and `related` to establish relationships
- `technical_notes` stores structured metadata as key-value pairs

### 4.2 Feature-Specific Attributes

Features use only these status values:

```yaml
- id: XXX-FTR-001
  title: Feature or Epic Title
  status: planned  # or in-progress, complete
  # ... all global attributes ...
```

**Allowed status values** (use ONLY these):
- `planned`: Feature defined but work not yet started
- `in-progress`: Active development underway
- `complete`: All acceptance criteria met and deployed

### 4.3 Task-Specific Attributes

Tasks add the `assigned_to` field:

```yaml
- id: XXX-TSK-001
  title: Task Title
  status: open  # or closed
  assigned_to: AGENT-003  # or user name
  # ... all global attributes ...
```

**Key points:**
- `assigned_to` can reference an agent from `agents/agent-manifest.json` or a user name
- Tasks use generic `open`/`closed` status (unlike features with specific statuses)

### 4.4 Issue-Specific Attributes

Issues add `hypothesis` and `severity`:

```yaml
- id: XXX-ISS-001
  title: Issue or Bug Title
  status: open  # or closed
  hypothesis: >
    Current theory about the root cause: X is failing because Y
    configuration is incorrect. Evidence includes Z log entries.
  severity: high  # low, medium, high, or critical
  # ... all global attributes ...
```

**Severity levels:**
- `low`: Minor inconvenience, workaround exists
- `medium`: Impacts functionality but not blocking
- `high`: Blocks important workflows, needs urgent attention
- `critical`: System down, data loss risk, security vulnerability

---

## 5. Relationship Management

### 5.1 Parent-Child Relationships

Use the `parent` field for hierarchical relationships:

```yaml
- id: AGH-TSK-001-0A
  parent: AGH-TSK-001
  title: Child task of AGH-TSK-001
  # ...
```

**Rules:**
1. Parent must be a valid ID that exists in the same or related YAML file
2. Only one parent allowed per item
3. Parent can be any type (feature can parent tasks, tasks can parent subtasks, etc.)
4. Automation should roll up status/completion from children to parents

### 5.2 Dependencies

Use `depends_on` for "must complete before" relationships:

```yaml
- id: AGH-TSK-005
  depends_on:
    - type: feature
      ids: [AGH-FTR-001]
    - type: task
      ids: [AGH-TSK-003, AGH-TSK-004]
```

**Semantics**: This item cannot start/complete until dependencies are resolved.

### 5.3 Blockers

Use `blocked_by` for "currently prevented by" relationships:

```yaml
- id: AGH-TSK-008
  blocked_by:
    - type: issue
      ids: [AGH-ISS-002]
```

**Semantics**: Work is stopped due to the blocking item(s).

### 5.4 Related Items

Use `related` for informational cross-references:

```yaml
- id: AGH-FTR-002
  related:
    - type: feature
      ids: [AGH-FTR-001, AGH-FTR-003]
    - type: issue
      ids: [DVP-ISS-007]
```

**Semantics**: Loosely connected work that agents should be aware of, but no strict dependency.

---

## 6. History & Logging

### 6.1 History Entry Structure

The `history` array replaces older logging fields (`debug_log`, `work_log`, `debug_notes`).

**Required structure:**

```yaml
history:
  - timestamp: 2025-11-09T14:23:00Z  # ISO 8601 format
    status: created  # see allowed values below
    description: What happened and why
```

**Allowed status values:**
- `created`: Initial entry creation (required, must be first)
- `started`: Work began (should appear only once)
- `worklog`: Progress update, investigation note, milestone
- `closed`: Item completed/resolved
- `reopened`: Closed item reopened due to new information

**Rules:**
1. Every item must have at least one `created` entry
2. Only one `started` entry allowed (signals transition from planned → active)
3. Any number of `worklog` entries for incremental updates
4. `closed` when work finishes; `reopened` if it needs more work
5. Always use ISO 8601 timestamps (YYYY-MM-DDTHH:MM:SSZ)
6. Descriptions should be concise but informative

### 6.2 Status Transitions

Recommended status flows:

**Features:**
```
created → started → worklog (0+) → closed → (reopened)
```

**Tasks:**
```
created → started → worklog (0+) → closed → (reopened)
```

**Issues:**
```
created → started → worklog (0+) → closed → (reopened)
```

### 6.3 Worklog Best Practices

- Log **meaningful** updates: architectural decisions, blockers encountered, solution attempts, milestone achievements
- Reference related IDs when relevant: "Discovered dependency on AGH-FTR-001"
- Include evidence: "Logs show timeout after 30s, increasing to 60s"
- Note pivot points: "Switching approach from X to Y after testing revealed Z"

---

## 7. Status Management

### 7.1 Feature Status Values

Use **only** these values for features:
- `planned`: Scoped but not started
- `in-progress`: Active development
- `complete`: Delivered and verified

### 7.2 Task Status Values

Use **only** these values for tasks:
- `open`: Not yet done
- `closed`: Completed

(Tasks can also include richer detail in `history` entries for nuance.)

### 7.3 Issue Status Values

Use **only** these values for issues:
- `open`: Under investigation or active work
- `closed`: Resolved or verified fixed

---

## 8. Technical Notes & Metadata

Use `technical_notes` for structured metadata that doesn't fit other fields:

```yaml
technical_notes:
  - distribution-id: A5XYZA7QLCCNAA
  - account-id: 1234509876
  - region: us-west-2
  - api-endpoint: https://api.example.com/v2
  - cloudfront-function: viewer-request
```

**Guidelines:**
1. Use kebab-case keys
2. Store ARNs, IDs, endpoints, account numbers
3. Reference external systems (AWS, Cloudflare, GitHub)
4. Keep values concise; full context goes in `description`

---

## 9. Examples

### 9.1 Complete Feature Example

```yaml
- id: AGH-FTR-002
  title: Starter Kit Distribution
  status: in-progress
  priority: P1
  description: >
    Package blank-canvas versions of all governance assets (agents.md, templates,
    repo scaffold, prompt library, IDE inventory, projects.yaml) inside repo/src
    with instructions on how to replicate them for new projects.
  acceptance_criteria:
    - repo/src/README.md explains copy/setup flow
    - repo-template/README.md includes tips for alias-based CLI launches
    - Templates contain placeholders only—no AgentHarmony-specific data
  technical_notes:
    - repo-path: projects/agentharmony/repo/src
    - target-audience: engineers bootstrapping new agent-driven projects
  depends_on:
    - type: feature
      ids: [AGH-FTR-001]
  related:
    - type: task
      ids: [AGH-TSK-001, AGH-TSK-002]
  history:
    - timestamp: 2025-11-07T08:15:00Z
      status: created
      description: Feature scoped to enable reusable starter kit for new projects
    - timestamp: 2025-11-07T09:30:00Z
      status: started
      description: Began packaging templates and documentation
```

### 9.2 Complete Task Example

```yaml
- id: AGH-TSK-003
  title: Define governance lint automation plan
  status: open
  priority: P1
  assigned_to: AGENT-004
  description: >
    Specify how lint-bootstrap, project_metadata, and future scripts will enforce
    documentation freshness (metrics, triggers, CI/Lambda target). Define alert
    thresholds and integration points with existing tooling.
  acceptance_criteria:
    - Automation spec document created in docs/
    - Freshness thresholds defined (e.g., 24h for architectural changes)
    - CI/Lambda integration plan outlined
  technical_notes:
    - tools-dir: projects/agentharmony/repo/src/tools
    - target-scripts: lint-bootstrap.sh, project_metadata.py
  related:
    - type: feature
      ids: [AGH-FTR-004]
    - type: issue
      ids: [AGH-ISS-001]
    - type: task
      ids: [AGH-TSK-004]
  history:
    - timestamp: 2025-11-07T09:10:00Z
      status: created
      description: Created to address documentation freshness gap identified in AGH-ISS-001
    - timestamp: 2025-11-07T10:00:00Z
      status: started
      description: Began analysis of existing lint-bootstrap capabilities
```

### 9.3 Complete Issue Example

```yaml
- id: AGH-ISS-001
  title: Documentation freshness checks missing
  status: open
  priority: P1
  severity: high
  hypothesis: >
    Manual discipline alone is insufficient to maintain 24h freshness KPI; automated
    validation with timestamp comparison is needed to detect documentation drift.
  description: >
    No automated process exists to detect stale sections or mismatched IDs between
    Markdown and YAML, creating risk that agents rely on outdated instructions.
  acceptance_criteria:
    - Automation detects YAML updates without corresponding MD updates
    - Alert triggered when doc age exceeds 24h after code changes
    - CI job fails if freshness check fails
  technical_notes:
    - kpi-target: 24h documentation freshness
    - affected-files: agentharmony-reference.md, agents-reference-*.yaml
  related:
    - type: feature
      ids: [AGH-FTR-001, AGH-FTR-002, AGH-FTR-003, AGH-FTR-004]
  history:
    - timestamp: 2025-11-07T08:55:00Z
      status: created
      description: Identified gap while bootstrapping project; logging as first issue
    - timestamp: 2025-11-07T09:10:00Z
      status: worklog
      description: Linked to AGH-TSK-003 to define automation requirements
    - timestamp: 2025-11-07T11:10:00Z
      status: worklog
      description: Starter kit documented; automation plan still pending, escalated to AGH-TSK-004 for implementation
```

---

**Document status**: This guide is the authoritative reference for project tracking standards across all AgentHarmony projects and should be updated whenever `yaml_structure.yaml` or `attribute_audit.md` evolve.
