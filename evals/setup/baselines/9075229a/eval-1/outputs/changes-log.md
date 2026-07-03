# Changes Log

## Preserved Content

The following pre-existing content from CLAUDE.md was preserved unchanged:

- `# my-project` heading and project description
- `## Documentation` section (architecture.md, api.md links)
- `## Getting Started` section (clone, install, start instructions)

## Added Sections

All Project Configuration sections were newly added (no prior configuration existed):

### `# Project Configuration` (new)

Top-level configuration heading added.

### `## Repository Registry` (new)

Added registry table with 2 rows:

| Repository | Serena Instance | Source |
|---|---|---|
| trustify-backend | serena_backend | User-provided mapping for discovered Serena instance |
| trustify-ui | serena_ui | User-provided mapping for discovered Serena instance |

### `## Jira Configuration` (new)

Added 5 fields, all user-provided:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)

Added tool naming convention documentation with `serena_backend` as the concrete example. Added `### Limitations` subheading noting no known limitations for either instance.

### `## Bug Configuration` (new)

Added 3 fields:

- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)

## Declined Sections

### `## Security Configuration` (declined)

User declined when asked whether to enable security triage. No Security Configuration section was added to the output.
