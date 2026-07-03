# Changes Log

## Project Configuration Sections Added

All sections were newly added (no prior Project Configuration existed in CLAUDE.md).

### 1. Repository Registry (NEW)

Added `## Repository Registry` with a table containing 2 rows:
- `backend` (Rust backend service) mapped to Serena instance `serena_backend` at `/home/user/backend`
- `frontend-ui` (TypeScript frontend) mapped to Serena instance `serena_ui` at `/home/user/frontend-ui`

### 2. Jira Configuration (NEW)

Added `## Jira Configuration` with 5 fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 3. Code Intelligence (NEW)

Added `## Code Intelligence` with:
- Tool naming convention documentation (`mcp__<instance>__<tool>`)
- Example using `serena_backend` instance
- `### Limitations` subsection (no limitations known)

### 4. Bug Configuration (NEW)

Added `## Bug Configuration` with 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### 5. Security Configuration (NEW)

Added `## Security Configuration` with 3 subsections:
- `### Product Lifecycle` with 5 fields (Product pages URL, Jira version prefix, Vulnerability issue type ID, Component label pattern, VEX Justification custom field)
- `### Version Streams` table with 1 row (2.1.x stream)
- `### Source Repositories` table with 2 rows (backend, frontend-ui)
