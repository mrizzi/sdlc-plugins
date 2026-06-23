# Changes Log

## Summary

Incremental update to Project Configuration. All existing entries preserved; only new entries added for the newly discovered `serena_ui` Serena instance.

## Preserved (no changes)

### Repository Registry
- **Preserved**: `trustify-backend` | Rust backend service | serena_backend | /home/user/trustify-backend

### Jira Configuration
- **Preserved**: Project key: TC
- **Preserved**: Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Preserved**: Feature issue type ID: 10142
- **Preserved**: Git Pull Request custom field: customfield_10875
- **Preserved**: GitHub Issue custom field: customfield_10747

### Code Intelligence
- **Preserved**: Tool naming convention explanation (`mcp__<instance>__<tool>`)
- **Preserved**: Example using `serena_backend`
- **Preserved**: Limitation entry for `serena_backend` (rust-analyzer indexing delay)

### Bug Configuration
- **Preserved**: Bug issue type ID: 10001
- **Preserved**: Bug template: docs/bug-template.md
- **Preserved**: Bug-to-Task link type: Blocks

## Added (new entries)

### Repository Registry
- **Added**: `trustify-ui` | TypeScript frontend | serena_ui | /home/user/trustify-ui

### Code Intelligence > Limitations
- **Added**: `serena_ui`: No known limitations

## Not Created (skipped)

- **Jira Field Defaults**: Requires MCP discovery of priorities/fixVersions (simulated run, no MCP calls)
- **Hierarchy Configuration**: Requires MCP discovery of issue type hierarchy (simulated run, no MCP calls)
- **Security Configuration**: User declined opt-in prompt
