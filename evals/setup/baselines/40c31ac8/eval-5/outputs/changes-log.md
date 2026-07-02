# Setup Changes Log

## Summary

All sections created from scratch -- the existing CLAUDE.md had no Project Configuration section.

## Sections Added

### 1. Project Configuration (top-level heading)

- Added `# Project Configuration` heading appended after existing CLAUDE.md content

### 2. Repository Registry

- Created `## Repository Registry` table with 2 rows:
  - `backend` | Rust backend service | serena_backend | /home/user/backend
  - `frontend-ui` | TypeScript frontend | serena_ui | /home/user/frontend-ui

### 3. Jira Configuration

- Created `## Jira Configuration` with all fields:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

### 4. Code Intelligence

- Created `## Code Intelligence` section with:
  - Tool naming convention: `mcp__<instance>__<tool>`
  - Example using `serena_backend` instance
  - `### Limitations` subsection (no limitations reported)

### 5. Bug Configuration

- Created `## Bug Configuration` with:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks
- Bug template file copy skipped (simulation)

### 6. Security Configuration

- Created `## Security Configuration` with subsections:
  - `### Product Lifecycle` -- 4 required fields + VEX Justification populated; 6 optional fields left blank
  - `### Version Streams` -- 1 stream (2.1.x)
  - `### Source Repositories` -- 2 repos (backend, frontend-ui) with upstream deployment context

### 7. Hierarchy Configuration

- Created `## Hierarchy Configuration` with:
  - Default epic grouping strategy: by-sub-feature

## Sections Not Created

- `### Jira Field Defaults` -- skipped, requires MCP discovery of available priorities and fixVersions (can be configured in a subsequent /setup run)

## Files Not Modified (simulation)

- `docs/constraints.md` -- would be created from constraints.template.md
- `docs/bug-template.md` -- would be created from bug-template.md template
- `/home/user/backend/CONVENTIONS.md` -- scaffolding not performed (simulation)
- `/home/user/frontend-ui/CONVENTIONS.md` -- scaffolding not performed (simulation)
- `security-matrix.md` -- scaffolding skipped by user
