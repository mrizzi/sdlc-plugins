# Changes Log

## Preserved (from existing CLAUDE.md)

- `# my-project` heading and project description
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions

## Added

### `# Project Configuration` (new section)

Appended at end of CLAUDE.md since no existing Project Configuration section was found.

### `## Repository Registry` (new)

Added table with 2 rows:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### `## Jira Configuration` (new)

Added 5 fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)

- Added tool naming convention explanation with `mcp__<instance>__<tool>` pattern
- Added concrete example using `serena_backend` instance
- Added `### Limitations` subsection noting no known limitations

### `## Bug Configuration` (new)

Added 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

## Not Added

- `## Security Configuration` -- user declined security triage enablement
- `## Hierarchy Configuration` -- not included (step not exercised in this simulation)
