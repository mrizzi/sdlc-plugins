# Changes Log

## Summary

Incremental update to existing Project Configuration. Added newly discovered Serena instance `serena_ui` (repository: trustify-ui). All existing configuration was preserved without modification.

## Changes by Section

### Repository Registry

| Change | Details |
|---|---|
| **Preserved** | `trustify-backend` row (Rust backend service, serena_backend, /home/user/trustify-backend) |
| **Added** | `trustify-ui` row (TypeScript frontend, serena_ui, /home/user/trustify-ui) |

### Jira Configuration

| Change | Details |
|---|---|
| **Preserved** | Project key: TC |
| **Preserved** | Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| **Preserved** | Feature issue type ID: 10142 |
| **Preserved** | Git Pull Request custom field: customfield_10875 |
| **Preserved** | GitHub Issue custom field: customfield_10747 |

No changes — Jira Configuration was already complete.

### Code Intelligence

| Change | Details |
|---|---|
| **Preserved** | Tool naming convention explanation and serena_backend example |
| **Preserved** | `serena_backend` limitation (rust-analyzer indexing delay) |
| **Added** | `serena_ui` limitation entry (no known limitations) |

### Bug Configuration

| Change | Details |
|---|---|
| **Preserved** | Bug issue type ID: 10001 |
| **Preserved** | Bug template: docs/bug-template.md |
| **Preserved** | Bug-to-Task link type: Blocks |

No changes — Bug Configuration was already complete.

### Hierarchy Configuration

| Change | Details |
|---|---|
| **Not scaffolded** | Hierarchy discovery requires Jira MCP calls (getJiraProjectIssueTypesMetadata) which were not invoked in this simulated run |

### Security Configuration

| Change | Details |
|---|---|
| **Not scaffolded** | User declined when asked whether to enable security triage |

## Sections Not Modified

The following content outside `# Project Configuration` was preserved without changes:
- `# trustify-backend` heading
- `## Documentation` section with architecture and API doc links
