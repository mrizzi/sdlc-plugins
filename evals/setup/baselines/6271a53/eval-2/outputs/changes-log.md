# Changes Log

## Summary

Incremental update to Project Configuration. One new Serena instance (serena_ui) was discovered and added. All existing configuration was preserved unchanged.

## Preserved (unchanged)

### Repository Registry
- **trustify-backend** entry: Role "Rust backend service", Serena Instance "serena_backend", Path "/home/user/trustify-backend"

### Jira Configuration
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Code Intelligence
- Naming convention description (`mcp__<instance>__<tool>`)
- Example using serena_backend (`mcp__serena_backend__find_symbol`)
- Limitation for serena_backend: "rust-analyzer may take 30-60 seconds to index on first use"

## Added (new)

### Repository Registry
- **trustify-ui** entry: Role "TypeScript frontend", Serena Instance "serena_ui", Path "/home/user/trustify-ui"

### Code Intelligence — Limitations
- **serena_ui**: "No known limitations"
