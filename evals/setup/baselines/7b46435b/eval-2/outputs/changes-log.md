# Changes Log

## Summary

Incremental update to an existing Project Configuration. Added newly discovered Serena instance (serena_ui / trustify-ui) to the Registry and Code Intelligence sections. All existing configuration preserved.

## Added

### Repository Registry
- Added row: `trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui`

### Code Intelligence -- Limitations
- Added entry: `serena_ui`: No known limitations

## Preserved (unchanged)

### Repository Registry
- Existing row preserved: `trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend`

### Jira Configuration
- Project key: TC (preserved)
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432 (preserved)
- Feature issue type ID: 10142 (preserved)
- Git Pull Request custom field: customfield_10875 (preserved)
- GitHub Issue custom field: customfield_10747 (preserved)

### Code Intelligence
- Naming convention documentation preserved
- Example using serena_backend preserved
- Existing limitation for serena_backend preserved: "rust-analyzer may take 30-60 seconds to index on first use"

### Bug Configuration
- Bug issue type ID: 10001 (preserved)
- Bug template: docs/bug-template.md (preserved)
- Bug-to-Task link type: Blocks (preserved)

## Skipped

### Jira Field Defaults
- Not present in existing configuration
- Skipped: requires Atlassian MCP calls for priority/fixVersion discovery (not available in simulation mode)

### Hierarchy Configuration
- Not present in existing configuration
- Skipped: requires Atlassian MCP calls for issue type hierarchy discovery (not available in simulation mode)

### Security Configuration
- Not present in existing configuration
- Skipped: user declined when asked whether to enable security triage

### Constraints Template (docs/constraints.md)
- Not checked: simulation mode, no filesystem operations performed

### CONVENTIONS.md Scaffolding
- Not checked: simulation mode, no filesystem operations performed
