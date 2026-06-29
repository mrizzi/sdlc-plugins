# Changes Log

## Preserved (existing content)

- `# my-project` heading and description
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions

## Added

### `# Project Configuration` (new section)

Appended at the end of the existing CLAUDE.md content.

### `## Repository Registry` (new subsection)

- Added table with headers (Repository, Role, Serena Instance, Path) and no data rows
- Reason: no Serena MCP servers discovered; user chose to continue without code intelligence

### `## Jira Configuration` (new subsection)

- Added Project key: MYPROJ
- Added Cloud ID: abc123
- Added Feature issue type ID: 10001
- No Git Pull Request custom field (user had none)
- No GitHub Issue custom field (user had none)
- No Jira Field Defaults subsection (MCP unavailable for priority/fixVersion discovery)

### `## Code Intelligence` (new subsection)

- Added note that no Serena MCP servers are configured
- Added `### Limitations` subheading with note that no Serena instances are configured

### `## Bug Configuration` (new subsection)

- Added Bug issue type ID: 10001
- Added Bug template: docs/bug-template.md
- Added Bug-to-Task link type: Blocks

## Not Added

- **Hierarchy Configuration**: skipped — no Atlassian MCP or REST API available to discover issue type hierarchy
- **Jira Field Defaults**: skipped — no Atlassian MCP or REST API available to discover priorities and fixVersions
- **Security Configuration**: skipped — user declined to enable security triage
- **CONVENTIONS.md**: skipped — no repositories in the Registry to scaffold for
- **docs/constraints.md**: skipped — simulation mode, no file operations
- **Bug template file**: skipped — simulation mode, no file copy
