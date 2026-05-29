# Changes Log

## Setup Type

Greenfield setup — the existing CLAUDE.md (claude-md-empty.md) contained no Project Configuration section. All sections below are newly added.

## Sections Added

### Repository Registry (new)

Added a table with 2 repositories mapped to their Serena instances:

| Repository | Role | Serena Instance |
|---|---|---|
| trustify-backend | Rust backend service | serena_backend |
| trustify-ui | TypeScript frontend | serena_ui |

### Jira Configuration (new)

Added Jira project settings with 5 fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Code Intelligence (new)

Added Code Intelligence section with:

- Explanation of Serena tool naming convention (`mcp__<instance>__<tool>`)
- Example showing how to invoke `find_symbol` on a Serena instance
- Limitations subsection noting no known limitations for either instance

## Sections Preserved

No existing sections were modified. The original CLAUDE.md content (project title, Documentation, Getting Started) remains unchanged and is not included in the output, which contains only the new Project Configuration section.
