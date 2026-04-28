# Changes Log

## Overview

This is a greenfield setup. The existing CLAUDE.md (`claude-md-empty.md`) contained no `# Project Configuration` section. All configuration sections were created from scratch.

## Preserved Content

The following existing content in CLAUDE.md was preserved (not modified):

- `# my-project` heading and description
- `## Documentation` section with links to `docs/architecture.md` and `docs/api.md`
- `## Getting Started` section with setup instructions

## Added Content

### `# Project Configuration` (new section)

The entire Project Configuration section was created, containing:

#### `## Repository Registry` (new)

Added a table with two repository entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

#### `## Jira Configuration` (new)

Added all five configuration fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

#### `## Code Intelligence` (new)

Added:
- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Concrete example using `serena_backend` instance
- `### Limitations` subheading noting no known limitations

## Summary

| Section | Status |
|---|---|
| Repository Registry | Created (2 entries) |
| Jira Configuration | Created (5 fields) |
| Code Intelligence | Created (with limitations subheading) |
