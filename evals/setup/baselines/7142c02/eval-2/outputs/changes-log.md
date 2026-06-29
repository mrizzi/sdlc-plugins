# Changes Log

## Summary

Incremental update to Project Configuration. One new Serena instance (`serena_ui`) was discovered and added. All existing configuration was preserved unchanged.

## Preserved (unchanged)

### Repository Registry
- **trustify-backend** row: Rust backend service | serena_backend | /home/user/trustify-backend

### Jira Configuration
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Code Intelligence
- Tool naming convention explanation preserved
- Example using `serena_backend` preserved
- Limitation for `serena_backend` preserved: "rust-analyzer may take 30-60 seconds to index on first use"

### Bug Configuration
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

## Added (new)

### Repository Registry
- **trustify-ui** row added: TypeScript frontend | serena_ui | /home/user/trustify-ui

### Code Intelligence -- Limitations
- **serena_ui** entry added: "No known limitations"

## Not Created (skipped)

### Jira Field Defaults
- Not present in existing configuration; MCP discovery not executed in this simulation

### Hierarchy Configuration
- Not present in existing configuration; MCP discovery not executed in this simulation

### Security Configuration
- User declined to enable security triage -- section not created
