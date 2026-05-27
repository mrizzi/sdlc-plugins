# Changes Log

## Summary

Incremental update: 1 new Serena instance added to existing configuration. All other sections preserved unchanged.

## Repository Registry

### Preserved (no changes)

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |

### Added

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

## Jira Configuration

### Preserved (no changes)

All fields already populated — no changes made.

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Code Intelligence

### Preserved (no changes)

- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Example using `serena_backend`
- Existing limitation: `serena_backend`: rust-analyzer may take 30-60 seconds to index on first use

### Added

- Limitation entry for `serena_ui`: No known limitations

## Non-Configuration Content

### Preserved (no changes)

- `# trustify-backend` heading and documentation links at top of file
- All content outside `# Project Configuration` section
