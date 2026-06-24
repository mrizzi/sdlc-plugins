# Changes Log

## Summary

All sections were added new -- the existing CLAUDE.md had no Project Configuration section.

## Added

### `# Project Configuration` (new heading)
- Created the top-level Project Configuration heading.

### `## Repository Registry` (new section)
- Added table with 2 repository entries:
  - trustify-backend (Rust backend service, serena_backend, /home/user/trustify-backend)
  - trustify-ui (TypeScript frontend, serena_ui, /home/user/trustify-ui)

### `## Jira Configuration` (new section)
- Added 5 fields:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new section)
- Added tool naming convention documentation with `mcp__<instance>__<tool>` pattern
- Added concrete example using serena_backend instance
- Added `### Limitations` subsection with no known limitations

### `## Bug Configuration` (new section)
- Added 3 fields:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks

## Preserved

- All existing content in the CLAUDE.md file (project header, documentation links, getting started section) was preserved. The Project Configuration section is appended at the end.

## Skipped

- **Jira Field Defaults**: Requires MCP calls to discover available priorities and fixVersions (simulation limitation)
- **Hierarchy Configuration**: Requires MCP calls to discover issue type hierarchy levels (simulation limitation)
- **Security Configuration**: User declined to enable security triage
- **Constraints template copy**: Skipped per simulation rules (no file system writes outside outputs/)
- **CONVENTIONS.md scaffolding**: Skipped per simulation rules (no file system writes outside outputs/)
- **Bug template file copy**: Skipped per simulation rules
