# Changes Log

## Summary

The existing CLAUDE.md had no `# Project Configuration` section. All configuration sections were added new. No existing content was modified or removed.

## Added

### `# Project Configuration` (new top-level section)

Appended to end of existing CLAUDE.md content.

### `## Repository Registry` (new)

Added table with 2 repositories:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### `## Jira Configuration` (new)

Added with 5 fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)

Added with:
- Tool naming convention (`mcp__<instance>__<tool>`)
- Example using `serena_backend` instance
- `### Limitations` subsection — no limitations reported for either instance

### `## Bug Configuration` (new)

Added with 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### `## Hierarchy Configuration` (new)

Added with 1 field:
- Default epic grouping strategy: by-sub-feature

## Preserved

All existing CLAUDE.md content preserved unchanged:
- `# my-project` heading and description
- `## Documentation` section with links
- `## Getting Started` section with instructions

## Skipped

- **Jira Field Defaults** — Not configured (MCP tools unavailable for priority/fixVersion discovery in simulation mode)
- **Security Configuration** — User declined to enable security triage
- **Constraints template** — Not copied (simulation mode, only writing to outputs/)
- **CONVENTIONS.md scaffolding** — Not created (simulation mode, only writing to outputs/)
- **Bug template file** — Not copied (simulation mode, as instructed)
