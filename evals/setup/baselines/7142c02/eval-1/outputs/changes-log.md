# Changes Log

## Preserved (existing content from CLAUDE.md)

- `# my-project` heading and project description.
- `## Documentation` section with links to architecture.md and api.md.
- `## Getting Started` section with setup instructions.

## Added (new sections appended to CLAUDE.md)

### `# Project Configuration` (new)

Top-level heading for all sdlc-workflow configuration sections.

### `## Repository Registry` (new)

Added table with 2 repository entries:

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

Note: `### Jira Field Defaults` subsection was not created (no values discovered or provided in simulation).

### `## Code Intelligence` (new)

- Documented the `mcp__<instance>__<tool>` naming convention.
- Added example using `serena_backend` instance.
- Added `### Limitations` subsection noting no known limitations.

### `## Bug Configuration` (new)

Added 3 fields:

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### `## Hierarchy Configuration` (new)

Added 1 field:

- Default epic grouping strategy: by-sub-feature

## Not Added

- `### Jira Field Defaults` -- skipped (no priority/fixVersion values available in simulation).
- `## Security Configuration` -- user declined to enable security triage.
- `docs/constraints.md` -- file copy skipped (simulation mode).
- `CONVENTIONS.md` -- file scaffolding skipped (simulation mode).
- Bug template file (`docs/bug-template.md`) -- file copy skipped (simulation mode).
