# Guide Numbering Reference

## Table of Contents
- [1. Purpose](#1-purpose)
- [2. CLI Step IDs](#2-cli-step-ids)
- [3. Documentation Step IDs](#3-documentation-step-ids)
- [4. Sub-step Naming Convention](#4-sub-step-naming-convention)
- [5. Schema Examples](#5-schema-examples)

## 1. Purpose
This guide explains how agents should generate reproducible, user-facing step sequences in both command-line automation and longerform documentation. It sits beside the project-tracking reference so that every instruction set can be traced back to an ID-compliant artifact and so users always receive the same structured format whether they work in Codex, UIs, or through the docs.

## 2. CLI Step IDs
- When providing instructions in or for a CLI interface, wse random, readable alphanumeric IDs of at least six characters (e.g., `S4A6Tx`). Human readers and automation can log those prefixes directly without ambiguous numbering.
- Substeps under a CLI step append hyphenated suffixes (see Section 4 for new rules) so `codex exec` can target each action (`codex exec S4A6Tx-0B`).
- Always start each step list with a definition block listing the primary step and its direct substeps, exactly as automation previews in the Codex output.

## 3. Documentation Step IDs
- When working in an UI or generating a document resource, use the format `[PROJECT-PREFIX]-[SECTION][STEPID]-[SUBSTEPID]`; for example `EXP-A01` or `EXP-A01-0A`. This keeps sections navigable and anchors easily resolvable in user-facing docs.
- Section headers should follow `## EXP-A: Section Title` and the step headers should read `### 01: Step Title` so the structure mirrors the table of contents.
- Include metadata such as duration estimates (⏱️), verification checks (✅), and warnings (⚠️) near the step descriptions so users can quickly understand costs and risk.

## 4. Sub-step Naming Convention
- Whether in CLI substeps or document sub-steps, if necessary the suffix appended after a final dash must be **exactly two characters**: a digit followed immediately by an uppercase letter (e.g., `-0A`, `-0B`, `-1A`).
- Always start with `0A` and increment the letter (A→B→C…) for sequential sub-entries within the same numeric bucket. To express a logical grouping change, optionally increment the digit (0→1→2) while resetting the letter to `A` so readers know a new cluster begins.
- This pattern matches the child ID rule in the project-tracking reference and allows scripts to parse `parent=AGH-ISS-001` when seeing `AGH-ISS-001-0A` or `-1B` etc.
- Examples:
  - `S4A6Tx-0A`: first CLI substep, same grouping as parent.
  - `EXP-A00-0A`: first substep in a new grouping assigned to `EXP-A00-1A`.

## 5. Schema Examples
```yaml
step_id: S4A6Tx
description: Initialize AWS credentials
substeps:
  - step_id: S4A6Tx-0A
    description: Export access key
    command: export AWS_ACCESS_KEY_ID=xxxxxx
  - step_id: S4A6Tx-0B
    description: Export secret key
    command: export AWS_SECRET_ACCESS_KEY=xxxxxx
```

```json
{
  "project_code": "EXP",
  "sections": [
    {
      "id": "EXP-A",
      "title": "Initialize CLI Configuration",
      "steps": [
        {
          "id": "01",
          "title": "Install Dependencies",
          "estimated_time": "3 min",
          "substeps": [
            "EXP-A01-0A",
            "EXP-A01-0B"
          ],
          "verification": "pip list | grep requests",
          "warning": null
        }
      ]
    }
  ]
}
```

| Feature | CLI Mode | Docs Mode                                 |
|---------|----------|-------------------------------------------|
| Prefix | `S4A6Tx` | `EXP-L01`                                 |
| Format | Flat + CLI substeps | Hierarchical with Section/Step/Substep    |
| Reference Style | Because CLI actions may be executed out of order, only the ID matters | Step ID plus contextual header for humans |
| Use Case | Automation, Codex sessions | SOPs, wikis, long-form instructions       |
