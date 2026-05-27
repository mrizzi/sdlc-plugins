# Changes Log

## Summary

Incremental update to an existing Project Configuration. One new Serena instance (`serena_ui`) was discovered and added. All existing configuration was preserved unchanged.

## Repository Registry

### Preserved (unchanged)

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |

### Added

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

## Jira Configuration

### Preserved (unchanged)

All fields retained exactly as configured:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Added

No changes — Jira Configuration was already complete.

## Code Intelligence

### Preserved (unchanged)

- Naming convention explanation (`mcp__<instance>__<tool>`)
- `serena_backend` example (`find_symbol` call)
- Existing limitation: `serena_backend`: rust-analyzer may take 30-60 seconds to index on first use

### Added

- `serena_ui` entry under Limitations: No known limitations
