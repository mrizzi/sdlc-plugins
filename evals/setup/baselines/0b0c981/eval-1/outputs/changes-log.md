# Changes Log

## Existing Content — Preserved

The following content from the original CLAUDE.md (`claude-md-empty.md`) was preserved unchanged:

- `# my-project` heading and description
- `## Documentation` section with links to `docs/architecture.md` and `docs/api.md`
- `## Getting Started` section with setup instructions

## New Content — Added

All Project Configuration sections were created from scratch since none existed in the original file.

### `# Project Configuration` (new)

Top-level heading added to contain all configuration subsections.

### `## Repository Registry` (new)

Added a table with 2 entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### `## Jira Configuration` (new)

Added all 5 configuration fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)

Added:

- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Example using `serena_backend` instance with `find_symbol` tool
- `### Limitations` subheading noting no known limitations

## Summary

- Sections preserved: 3 (project heading, Documentation, Getting Started)
- Sections added: 4 (Project Configuration, Repository Registry, Jira Configuration, Code Intelligence)
- Sections modified: 0
- Sections removed: 0
