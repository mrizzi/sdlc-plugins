# Changes Log

## Summary

The existing CLAUDE.md had no `# Project Configuration` section. All configuration sections were created new. No existing content was modified or removed.

## Added

### # Project Configuration (new top-level section)

Appended to CLAUDE.md since no Project Configuration section existed.

### ## Repository Registry (new)

Added table with 2 repositories:
- `backend` — Rust backend service, Serena instance `serena_backend`, path `/home/user/backend`
- `frontend-ui` — TypeScript frontend, Serena instance `serena_ui`, path `/home/user/frontend-ui`

### ## Jira Configuration (new)

Added all 5 fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### ## Code Intelligence (new)

Added section documenting:
- Tool naming convention: `mcp__<instance>__<tool>`
- Example using `serena_backend` instance
- Limitations subsection (no limitations reported)

### ## Security Configuration (new)

Added full Security Configuration section with:

#### ### Product Lifecycle
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

#### ### Version Streams
Added 1 stream:
- 2.1.x: git.downstream.example.com/my-org/product-release.2.1.z

#### ### Source Repositories
Added 2 repositories:
- backend: https://github.com/example/backend
- frontend-ui: https://github.com/example/frontend-ui

## Preserved

- All existing CLAUDE.md content (project title, Documentation section, Getting Started section) was preserved unchanged. The Project Configuration section was appended after existing content.

## Not Modified

- No existing configuration entries were removed or overwritten (none existed).
- docs/constraints.md — not scaffolded (eval instructions: write only to outputs/).
- CONVENTIONS.md — not scaffolded (eval instructions: write only to outputs/).
- security-matrix.md — user skipped scaffolding.
- Supportability matrix — user declined population.
