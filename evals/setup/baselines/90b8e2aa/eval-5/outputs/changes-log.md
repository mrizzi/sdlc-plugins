# Changes Log

## Summary

The existing CLAUDE.md had no `# Project Configuration` section. All sections below were newly created and appended to the file.

## Sections Added

### 1. Project Configuration (heading)

- **Action**: Added
- **Details**: Created the top-level `# Project Configuration` heading.

### 2. Repository Registry

- **Action**: Added
- **Details**: Created table with 2 repository entries:
  - backend (Rust backend service) via serena_backend at /home/user/backend
  - frontend-ui (TypeScript frontend) via serena_ui at /home/user/frontend-ui

### 3. Jira Configuration

- **Action**: Added
- **Details**: Created section with all 5 fields populated:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

### 4. Code Intelligence

- **Action**: Added
- **Details**: Created section documenting Serena tool naming convention (`mcp__<instance>__<tool>`) with a concrete example using serena_backend. Added `### Limitations` subheading noting no known limitations.

### 5. Bug Configuration

- **Action**: Added
- **Details**: Created section with all 3 fields populated:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks

### 6. Security Configuration

- **Action**: Added (user accepted opt-in to enable security triage)
- **Details**: Created full Security Configuration section with three subsections:
  - **Product Lifecycle**: All 5 fields populated (Product pages URL, Jira version prefix, Vulnerability issue type ID, Component label pattern, VEX Justification custom field)
  - **Version Streams**: Table with 1 stream (2.1.x) including Konflux release repo URL, local path, and security matrix path
  - **Source Repositories**: Table with 2 entries (backend, frontend-ui) with GitHub URLs and upstream deployment context

## Files Not Modified

- No actual CLAUDE.md was modified (simulation mode -- output written to outputs/claude-md-result.md)
- Bug template file (docs/bug-template.md) was not copied (simulation mode)
- security-matrix.md was not scaffolded (user skipped)
- Supportability matrix was not populated (user declined)
