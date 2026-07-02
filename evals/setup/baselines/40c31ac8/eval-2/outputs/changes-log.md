# Changes Log

## Summary

Setup processed an existing CLAUDE.md with a complete Project Configuration.
One new Serena instance (`serena_ui`) was discovered and added.

## Preserved (unchanged)

### Repository Registry
- Row: `trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend` -- preserved

### Jira Configuration
- Project key: TC -- preserved
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432 -- preserved
- Feature issue type ID: 10142 -- preserved
- Git Pull Request custom field: customfield_10875 -- preserved
- GitHub Issue custom field: customfield_10747 -- preserved

### Code Intelligence
- Tool naming convention explanation -- preserved
- Example using `serena_backend` -- preserved
- Limitation for `serena_backend` (rust-analyzer indexing) -- preserved

### Bug Configuration
- Bug issue type ID: 10001 -- preserved
- Bug template: docs/bug-template.md -- preserved
- Bug-to-Task link type: Blocks -- preserved

### Non-configuration Content
- `# trustify-backend` heading and `## Documentation` section -- preserved

## Added

### Repository Registry
- New row: `trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui`

### Code Intelligence / Limitations
- New entry: `serena_ui`: No known limitations

## Not Configured (skipped)

### Jira Field Defaults
- Not present in original, not added -- MCP tool calls required for discovery (getJiraIssueTypeMetaWithFields) are unavailable in simulation mode

### Hierarchy Configuration
- Not present in original, not added -- MCP tool calls required for discovery (getJiraProjectIssueTypesMetadata) are unavailable in simulation mode

### Security Configuration
- Not present in original, not added -- user declined when asked whether to enable security triage
