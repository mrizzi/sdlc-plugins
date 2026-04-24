<!-- SYNTHETIC TEST DATA — CLAUDE.md with complete Project Configuration for define-feature eval testing -->

# trustify-backend

## Documentation

- [docs/architecture.md](docs/architecture.md) — System architecture overview
- [docs/api.md](docs/api.md) — REST API reference

# Project Configuration

## Repository Registry

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |

## Jira Configuration

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Code Intelligence

Tools are prefixed by Serena instance name: `mcp__<instance>__<tool>`.

For example, to search for a symbol in a repository whose Serena instance
is `serena_backend`:

    mcp__serena_backend__find_symbol(
      name_path_pattern="MyService",
      substring_matching=true,
      include_body=false
    )

### Limitations

- `serena_backend`: rust-analyzer may take 30-60 seconds to index on first use
