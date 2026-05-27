# Changes Log

## Summary

The existing CLAUDE.md had no `# Project Configuration` section. The entire section was generated and should be appended to the end of the file.

## What Was Preserved

- All existing CLAUDE.md content is preserved unchanged:
  - `# my-project` heading and project description
  - `## Documentation` section with links to docs/architecture.md and docs/api.md
  - `## Getting Started` section with setup instructions

## What Was Added

### 1. `# Project Configuration` (new section)

Top-level heading for all project configuration subsections.

### 2. `## Repository Registry` (new subsection)

Added a table with two repository entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### 3. `## Jira Configuration` (new subsection)

Added all five configuration fields:

- Project key: TC (required)
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432 (required)
- Feature issue type ID: 10142 (required)
- Git Pull Request custom field: customfield_10875 (optional)
- GitHub Issue custom field: customfield_10747 (optional)

### 4. `## Code Intelligence` (new subsection)

Added:
- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Example using the `serena_backend` instance
- `### Limitations` subheading noting no known limitations for any instance
