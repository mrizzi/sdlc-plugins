# Changes Log

## Summary

The existing CLAUDE.md had no Project Configuration section. A complete Project Configuration was generated from scratch.

## Added

### `# Project Configuration` (new section)

The entire section was created, including all subsections below.

### `## Repository Registry` (new)

Added a table with two repository entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### `## Jira Configuration` (new)

Added all five configuration fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)

Added the tool naming convention documentation with:
- Explanation of `mcp__<instance>__<tool>` pattern
- Concrete example using `serena_backend`
- `### Limitations` subheading noting no known limitations for either instance

## Preserved

- All existing content in the original CLAUDE.md was preserved (project title, documentation links, getting started section).
- No existing content was modified or removed.

## Skipped

- **Security Configuration**: User declined to enable security triage. No `## Security Configuration` section was added.
