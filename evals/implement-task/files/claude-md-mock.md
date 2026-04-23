<!-- SYNTHETIC TEST DATA — mock CLAUDE.md with Project Configuration for implement-task eval testing -->

# trustify-backend

## Documentation

- [docs/architecture.md](docs/architecture.md) — System architecture overview
- [docs/api.md](docs/api.md) — REST API reference

# Project Configuration

## Repository Registry

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | ./ |

## Jira Configuration

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Code Intelligence

Serena MCP servers provide code intelligence for repository analysis.

### Tool naming convention

Tools are called as `mcp__<serena-instance>__<tool>`.

### Configured instances

| Serena Instance | Repository | Language Server |
|---|---|---|
| serena_backend | trustify-backend | rust-analyzer |

### Limitations

- rust-analyzer may take 30-60 seconds to index on first use
