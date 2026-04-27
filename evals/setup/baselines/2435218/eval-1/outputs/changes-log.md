# Changes Log

## Existing Content -- Preserved

The original CLAUDE.md (`claude-md-empty.md`) contained the following sections, all of which are preserved unchanged:

- `# my-project` -- project title and description
- `## Documentation` -- links to architecture and API docs
- `## Getting Started` -- setup instructions (clone, npm install, npm start)

## New Content -- Added

The entire `# Project Configuration` section was added, as no prior configuration existed.

### `## Repository Registry` (new)

Added a table with 2 repository entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### `## Jira Configuration` (new)

Added 5 configuration fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)

Added:

- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Concrete example using `serena_backend` instance
- `### Limitations` subheading with note that no limitations are known

## Summary

| Section | Action |
|---|---|
| `# my-project` | Preserved (no changes) |
| `## Documentation` | Preserved (no changes) |
| `## Getting Started` | Preserved (no changes) |
| `# Project Configuration` | **Added** (new) |
| `## Repository Registry` | **Added** (new, 2 entries) |
| `## Jira Configuration` | **Added** (new, 5 fields) |
| `## Code Intelligence` | **Added** (new, with limitations subsection) |
