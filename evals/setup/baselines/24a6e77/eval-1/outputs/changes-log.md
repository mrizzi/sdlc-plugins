# Changes Log

## Preserved (unchanged)

The following content from the existing CLAUDE.md was preserved without modification:

- `# my-project` heading and project description
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions

## Added

The following sections were added to the end of the CLAUDE.md file:

### 1. `# Project Configuration` (new heading)

Top-level heading added to contain all project configuration subsections.

### 2. `## Repository Registry` (new section)

Added a table with two repository entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

**Source**: Serena instances discovered from MCP tool listing; repository details provided by user.

### 3. `## Jira Configuration` (new section)

Added five configuration fields:

- Project key: `TC`
- Cloud ID: `2b9e35e3-6bd3-4cec-b838-f4249ee02432`
- Feature issue type ID: `10142`
- Git Pull Request custom field: `customfield_10875`
- GitHub Issue custom field: `customfield_10747`

**Source**: All values provided by user. Atlassian MCP tools were detected but not called (simulation mode).

### 4. `## Code Intelligence` (new section)

Added the Serena tool naming convention documentation with:

- Explanation of the `mcp__<instance>__<tool>` naming pattern
- Concrete example using the `serena_backend` instance
- `### Limitations` subheading noting no known limitations

**Source**: Naming convention from project-config template; limitations status confirmed by user (none reported).

## Removed

Nothing was removed. The setup skill is additive-only.

## Modified

Nothing was modified. All existing content was preserved as-is.
