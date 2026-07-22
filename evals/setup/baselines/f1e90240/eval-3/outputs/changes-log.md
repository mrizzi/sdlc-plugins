# Changes Log

## Preserved (from existing CLAUDE.md)

- Project title: `# my-project`
- Documentation section with architecture and API links
- Getting Started section with setup instructions

## Added

### `# Project Configuration` (new top-level section)

All subsections below are newly created since no Project Configuration existed previously.

### `## Repository Registry`

- Added table with headers only (Repository, Role, Serena Instance, Path)
- No data rows: no Serena instances were discovered

### `## Jira Configuration`

- Added Project key: MYPROJ
- Added Cloud ID: abc123
- Added Feature issue type ID: 10001
- Git Pull Request custom field: omitted (user did not provide)
- GitHub Issue custom field: omitted (user did not provide)

### `## Code Intelligence`

- Added note: "No Serena MCP servers are configured. Code intelligence is not available."
- Added `### Limitations` subsection: "No limitations known -- no Serena instances configured."

### `## Bug Configuration`

- Added Bug issue type ID: 10001
- Added Bug template: docs/bug-template.md
- Added Bug-to-Task link type: Blocks

## Not Created

- **Jira Field Defaults**: No MCP or REST API available to discover priorities and fixVersions
- **Hierarchy Configuration**: No MCP or REST API available to discover issue type hierarchy
- **Security Configuration**: User declined to enable security triage
