# Changes Log

## Preserved (existing content)

The following sections from the original CLAUDE.md were preserved without modification:

- **Top-level heading**: `# my-project`
- **Description**: "A web application for managing inventory."
- **Documentation section**: Links to docs/architecture.md and docs/api.md
- **Getting Started section**: Clone, npm install, npm start instructions

## Added (new content)

The following sections were appended to the CLAUDE.md under a new `# Project Configuration` heading:

### Repository Registry
- Added table with 2 repositories:
  - trustify-backend (Rust backend service, Serena instance: serena_backend, path: /home/user/trustify-backend)
  - trustify-ui (TypeScript frontend, Serena instance: serena_ui, path: /home/user/trustify-ui)

### Jira Configuration
- Added Project key: TC
- Added Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Added Feature issue type ID: 10142
- Added Git Pull Request custom field: customfield_10875
- Added GitHub Issue custom field: customfield_10747

### Code Intelligence
- Added tool usage examples for both Serena instances (serena_backend, serena_ui)
- Added Limitations subsection noting no known limitations for either instance

### Bug Configuration
- Added Bug issue type ID: 10001
- Added Bug template: docs/bug-template.md
- Added Bug-to-Task link type: Blocks

### Hierarchy Configuration
- Added Default epic grouping strategy: by-sub-feature

## Skipped

### Security Configuration
- Not added — user declined security triage enablement

### Bug Template File
- Not copied — simulation mode (skip bug template file copy)
