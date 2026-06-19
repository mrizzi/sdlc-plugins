# Setup Changes Log

## Summary

Added a complete `# Project Configuration` section to the project's CLAUDE.md. All pre-existing content (project description, Documentation section, Getting Started section) was preserved unchanged above the new configuration block.

## Sections Added

### 1. Repository Registry (new)

Added `## Repository Registry` with a table containing 2 repositories:

- **backend** — Rust backend service, Serena instance `serena_backend`, path `/home/user/backend`
- **frontend-ui** — TypeScript frontend, Serena instance `serena_ui`, path `/home/user/frontend-ui`

### 2. Jira Configuration (new)

Added `## Jira Configuration` with all required and optional fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 3. Code Intelligence (new)

Added `## Code Intelligence` section documenting:

- The `mcp__<instance>__<tool>` naming convention with an example using `serena_backend`
- A `### Limitations` subsection noting no known limitations for either instance

### 4. Bug Configuration (new)

Added `## Bug Configuration` with:

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### 5. Security Configuration (new)

Added `## Security Configuration` with three subsections:

- **Product Lifecycle** — Product pages URL, Jira version prefix, Vulnerability issue type ID, component label pattern, VEX Justification custom field
- **Version Streams** — 1 stream (2.1.x) with Konflux release repo, local path, and security matrix path
- **Source Repositories** — 2 repositories (backend, frontend-ui) with their URLs

## Pre-existing Content Preserved

The following sections from the original CLAUDE.md were preserved without modification:

- `# my-project` heading and description
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions
