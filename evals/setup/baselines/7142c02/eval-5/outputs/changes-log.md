# Changes Log

## Summary

All sections were newly created — the original CLAUDE.md had no Project Configuration section.

## Preserved Content

- Original CLAUDE.md content (heading, documentation links, getting started section) — preserved in full, unchanged.

## Added Sections

### `# Project Configuration`

- Added top-level heading to anchor all configuration subsections.

### `## Repository Registry`

- Added table with 2 entries:
  - `backend` — Rust backend service, Serena instance `serena_backend`, path `/home/user/backend`
  - `frontend-ui` — TypeScript frontend, Serena instance `serena_ui`, path `/home/user/frontend-ui`

### `## Jira Configuration`

- Added all 5 fields:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

### `## Code Intelligence`

- Added `mcp__<instance>__<tool>` naming convention documentation.
- Added example using `serena_backend` instance.
- Added `### Limitations` subsection — no limitations known.

### `## Bug Configuration`

- Added all 3 fields:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks

### `## Security Configuration`

- Added `### Product Lifecycle` subsection with all 5 fields:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
- Added `### Version Streams` subsection with 1 stream:
  - 2.1.x — Konflux release repo, local path, security matrix path
- Added `### Source Repositories` subsection with 2 entries:
  - backend: https://github.com/example/backend
  - frontend-ui: https://github.com/example/frontend-ui
