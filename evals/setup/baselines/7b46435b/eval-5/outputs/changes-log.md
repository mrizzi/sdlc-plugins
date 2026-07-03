# Changes Log

## Summary

All Project Configuration sections were newly added to the CLAUDE.md, including Security Configuration which was opted in by the user. The existing non-configuration content (project heading, Documentation, Getting Started) in the original CLAUDE.md was preserved.

## Sections Added

### Repository Registry — ADDED

- Added `backend` (serena_backend, Rust backend service, /home/user/backend)
- Added `frontend-ui` (serena_ui, TypeScript frontend, /home/user/frontend-ui)

### Jira Configuration — ADDED

- Added Project key: TC
- Added Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Added Feature issue type ID: 10142
- Added Git Pull Request custom field: customfield_10875
- Added GitHub Issue custom field: customfield_10747

### Code Intelligence — ADDED

- Added `mcp__<instance>__<tool>` naming convention documentation
- Added usage example with serena_backend instance
- Added Limitations subsection (no limitations known for either instance)

### Bug Configuration — ADDED

- Added Bug issue type ID: 10001
- Added Bug template: docs/bug-template.md
- Added Bug-to-Task link type: Blocks

### Security Configuration — ADDED

- Added Product Lifecycle section with all required and optional fields:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
  - Optional fields (Upstream Affected Component, PS Component, Stream, ProdSec contact, ProdSec Jira account ID, Embargo policy URL): left empty (user skipped)
- Added Version Streams table with 1 stream (2.1.x)
- Added Source Repositories table with 2 repositories (backend, frontend-ui)

## Sections Preserved

- Pre-existing non-configuration content from the original CLAUDE.md (project heading "my-project", Documentation section, Getting Started section) was preserved — only the new Project Configuration section was appended.

## Sections Skipped

- Jira Field Defaults: skipped (MCP auto-discovery not available in simulation mode)
- Hierarchy Configuration: skipped (MCP auto-discovery not available in simulation mode)
- Constraints template copy: skipped (simulation mode — would normally create docs/constraints.md)
- CONVENTIONS.md scaffolding: skipped (simulation mode — would normally offer to scaffold per repository)
- Bug template file copy: skipped (simulation mode)
- security-matrix.md scaffolding: skipped (user declined)
- Supportability matrix population: skipped (user declined)
