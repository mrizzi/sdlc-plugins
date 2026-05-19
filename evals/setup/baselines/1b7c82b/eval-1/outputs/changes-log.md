# Changes Log

## Summary

The existing CLAUDE.md had no `# Project Configuration` section. All configuration sections were created new. No existing content was modified or removed.

## Added

### `# Project Configuration` (new top-level section)

Appended to the end of the existing CLAUDE.md content.

### `## Repository Registry` (new section)

Added a repository registry table with two entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### `## Jira Configuration` (new section)

Added Jira configuration with all five fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new section)

Added Code Intelligence section with:
- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Concrete example using `serena_backend` instance
- `### Limitations` subheading noting no known limitations

## Preserved

All existing CLAUDE.md content was preserved unchanged:
- `# my-project` heading and description
- `## Documentation` section with architecture and API doc links
- `## Getting Started` section with setup instructions
