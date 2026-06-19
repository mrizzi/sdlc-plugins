# Changes Log

## Summary

The existing CLAUDE.md had no `# Project Configuration` section. All sections were created new.

## Added

### `# Project Configuration` (new top-level section)

Appended to the end of the existing CLAUDE.md content.

### `## Repository Registry` (new)

Added table with 2 repositories:
- `trustify-backend` — Rust backend service, Serena instance `serena_backend`, path `/home/user/trustify-backend`
- `trustify-ui` — TypeScript frontend, Serena instance `serena_ui`, path `/home/user/trustify-ui`

### `## Jira Configuration` (new)

Added all 5 fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)

Added section with:
- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Example using `serena_backend` instance
- `### Limitations` subheading — no limitations known

### `## Bug Configuration` (new)

Added all 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

## Preserved

- All existing CLAUDE.md content (project title, documentation links, getting started section) was preserved unchanged.

## Skipped

- `## Security Configuration` — user declined to enable security triage
- Bug template file copy — skipped per simulation instructions
- `docs/constraints.md` scaffolding — skipped per simulation instructions
- `CONVENTIONS.md` scaffolding — skipped per simulation instructions
