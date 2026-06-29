# Changes Log

## Summary

This log documents changes made to the Project Configuration during the setup process.

## Preserved (Existing Entries)

The following entries were already present in the CLAUDE.md and were preserved without modification:

### Repository Registry
- **trustify-backend** entry — preserved verbatim (1 row)

### Jira Configuration
All five fields preserved as-is:
- Project key
- Cloud ID
- Feature issue type ID
- Git Pull Request custom field
- GitHub Issue custom field

### Code Intelligence
- Section body text preserved verbatim
- Existing Limitations entries for serena_backend preserved verbatim (2 entries)

## Added (New Entries)

### Repository Registry — New Row
Added a new row for the newly discovered Serena instance serena_ui:
- Repository: trustify-ui
- Role: TypeScript frontend
- Serena Instance: serena_ui
- Path: /home/user/trustify-ui

### Code Intelligence — New Limitation
Added a Limitations entry for the new Serena instance:
- `serena_ui`: No known limitations

### Bug Configuration — New Section
Added the entire Bug Configuration section with three fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

## Not Added

### Security Configuration
The user declined to enable security triage. No Security Configuration section was created.

### Hierarchy Configuration
Skipped due to simulation constraints (MCP/REST API not available for hierarchy discovery).

### Jira Field Defaults
Skipped due to simulation constraints (MCP/REST API not available for priority/fixVersion discovery).
