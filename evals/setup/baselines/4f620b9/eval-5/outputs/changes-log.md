# Setup Changes Log

## Summary

Full Project Configuration created from scratch. The existing CLAUDE.md had no Project Configuration section.

## Changes Made

### 1. Repository Registry (NEW)

Added 2 repositories:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### 2. Jira Configuration (NEW)

Added all configuration fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 3. Code Intelligence (NEW)

- Documented `mcp__<instance>__<tool>` naming convention
- Added example using `serena_backend` instance
- Added Limitations subsection (no limitations reported)

### 4. Bug Configuration (NEW)

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### 5. Security Configuration (NEW)

- Product Lifecycle section with all required fields
- 1 Version Stream: 2.1.x
- 2 Source Repositories: backend, frontend-ui
- Optional fields left blank: Upstream Affected Component, PS Component, Stream custom field

### 6. Hierarchy Configuration (NEW)

- Default epic grouping strategy: by-sub-feature

### 7. Skipped Actions (Simulation Mode)

- `docs/constraints.md` copy: skipped
- `CONVENTIONS.md` scaffolding: skipped
- Bug template file copy: skipped
- `security-matrix.md` scaffolding: skipped (user declined)
- Supportability matrix population: skipped (user declined)
