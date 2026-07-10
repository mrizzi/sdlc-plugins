# Setup Changes Log

## Changes Applied to CLAUDE.md

The following sections were added to the project's CLAUDE.md under `# Project Configuration`:

### 1. Repository Registry (added)

Added table with 2 repositories:
- `backend` — Rust backend service (serena_backend, /home/user/backend)
- `frontend-ui` — TypeScript frontend (serena_ui, /home/user/frontend-ui)

### 2. Jira Configuration (added)

Added 5 fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 3. Code Intelligence (added)

Added section with:
- Tool naming convention (`mcp__<instance>__<tool>`)
- Example using serena_backend instance
- Limitations subsection (no limitations known)

### 4. Bug Configuration (added)

Added 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### 5. Security Configuration (added)

Added full Security Configuration section with:

**Product Lifecycle** — 5 fields:
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

**Version Streams** — 1 stream:
- 2.1.x (Konflux release repo: git.downstream.example.com/my-org/product-release.2.1.z, local path: /home/user/product-release.2.1.z, security matrix: security-matrix.md)

**Source Repositories** — 2 repositories:
- backend (https://github.com/example/backend, upstream)
- frontend-ui (https://github.com/example/frontend-ui, upstream)

## Files Not Modified (simulation)

- Bug template file (docs/bug-template.md): copy skipped (simulation mode)
- security-matrix.md: scaffolding skipped by user
- Supportability matrix: population declined by user
