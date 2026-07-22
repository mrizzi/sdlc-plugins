# Changes Log

## Summary

Incremental update to an existing Project Configuration. One new Serena instance (`serena_ui`) was discovered and added. All existing configuration entries were preserved unchanged.

## Changes by Section

### Repository Registry

- **Preserved**: `trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend`
- **Added**: `trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui`

### Jira Configuration

- **Preserved** (no changes): All fields retained as-is
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

### Jira Field Defaults

- **Not scaffolded**: Requires MCP calls to discover available priorities and fixVersions. Not available in this simulation.

### Code Intelligence

- **Preserved**: Tool naming convention explanation and `serena_backend` example
- **Preserved**: Existing limitation for `serena_backend` (rust-analyzer indexing delay)
- **Added**: Limitation entry for `serena_ui`: No known limitations

### Bug Configuration

- **Preserved** (no changes): All fields retained as-is
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks

### Hierarchy Configuration

- **Not scaffolded**: Requires MCP calls to discover issue type hierarchy. Not available in this simulation.

### Security Configuration

- **Not scaffolded**: User declined when asked whether to enable security triage.
